"""One pass over the queue: claim due rows, deliver them, then mark each one
sent, failed or released for retry (F1, F3)."""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

import telegram

from domain.localtime import local_date
from infra.file_facade import File
from infra.scheduler.registry import PERMANENT_ERRORS, SEND_HANDLERS, TRANSIENT_ERRORS, SendCtx
from infra.store import get_store
from infra.store.schedule import ScheduledSend

logger = logging.getLogger(__name__)


# Rows claimed per pass. A batch is sent sequentially — this bounds how long one
# tick can hold the loop, not how many users can be served.
CLAIM_LIMIT = 20


# How long a row may sit in 'claimed' before the scheduler assumes the process
# that claimed it died. Must be comfortably longer than the slowest send (a
# stitched multi-ayah audio upload), or a live send would be released out from
# under itself and delivered twice.
CLAIM_TIMEOUT = timedelta(minutes=5)


# F3's "still same-day-relevant" bound. A reminder that came due while the
# instance was restarting is worth delivering an hour or two late; the same
# reminder surfacing after an overnight outage is not — nobody wants their
# 07:00 portion at 03:00 the next morning. Rows overdue by more than this are
# deleted unsent.
CATCH_UP_WINDOW = timedelta(hours=6)


@dataclass
class TickResult:
    """What one pass did. Returned so tests (and the boot log) can assert on it
    instead of scraping stdout."""

    claimed: int = 0
    sent: int = 0
    failed: int = 0
    dropped: int = 0  # too late to be worth delivering
    released: int = 0  # claims recovered from a dead process
    deferred: int = 0  # transient failure, back on the queue for the next tick
    errors: list = field(default_factory=list)  # (send_id, exception) per failure

    def __bool__(self) -> bool:
        return bool(self.claimed or self.dropped or self.released)


def _lock() -> asyncio.Lock:
    global _tick_lock_obj, _tick_lock_loop
    loop = asyncio.get_running_loop()
    if _tick_lock_obj is None or _tick_lock_loop is not loop:
        _tick_lock_obj = asyncio.Lock()
        _tick_lock_loop = loop
    return _tick_lock_obj


def _utcnow(now: Optional[datetime] = None) -> datetime:
    """`now` as an aware UTC datetime, defaulting to the clock. A naive datetime
    is read as UTC — callers building instants by hand routinely produce one, and
    comparing naive to aware raises."""
    if now is None:
        return datetime.now(timezone.utc)
    return now.replace(tzinfo=timezone.utc) if now.tzinfo is None else now.astimezone(timezone.utc)


def _is_stale(row: ScheduledSend, now: datetime) -> bool:
    """Whether `row` came due too long ago to still be worth delivering (F3).

    Two rules, the second only when the payload says what local day the row
    belongs to:

      * more than `CATCH_UP_WINDOW` overdue — a restart that took two minutes
        still delivers, an outage that spanned the night does not;
      * past the recipient's local midnight. A 23:30 reminder recovered at 00:10
        is only 40 minutes late but belongs to yesterday, and yesterday's portion
        is not what tomorrow's streak needs.
    """
    due_at = _utcnow(row.due_at)
    if now - due_at > CATCH_UP_WINDOW:
        return True
    offset = (row.payload or {}).get("offset")
    if offset:
        try:
            return local_date(now, offset) != local_date(due_at, offset)
        except (ValueError, TypeError):
            return False  # unparseable offset: fall back to the window alone
    return False


async def _deliver(ctx: SendCtx) -> None:
    """Run the handler registered for this row's kind."""
    handler = SEND_HANDLERS.get(ctx.kind)
    if handler is None:
        raise LookupError(
            "no handler registered for scheduled kind %r (registered: %s)"
            % (ctx.kind, ", ".join(sorted(SEND_HANDLERS)) or "none")
        )
    await handler(ctx)


async def tick(
    bot,
    data: Optional[dict] = None,
    now: Optional[datetime] = None,
    store=None,
    limit: int = CLAIM_LIMIT,
    release_before: Optional[datetime] = None,
) -> TickResult:
    """One complete pass: recover, prune, claim, send.

    In order, because the order is the correctness argument:

      1. **release** claims older than `CLAIM_TIMEOUT` (or than `release_before`,
         which boot sets to *now* — see `catch_up`). A process that died mid-send
         left rows stranded in 'claimed'; nothing else ever frees them.
      2. **drop** rows more than `CATCH_UP_WINDOW` overdue, so step 4 cannot
         deliver last night's reminder this morning.
      3. **claim** what is due, atomically. Rows due in the future are not
         touched, which is what stops a reminder firing early.
      4. **send** each claimed row, one at a time, and mark it 'sent' or
         'failed'. Every failure is contained to its own row: a raising handler
         is caught, printed *with a traceback*, and the loop continues to the
         next row.

    `now` and `store` are injectable so the whole thing is testable without
    sleeping and without a real clock.
    """
    async with _lock():
        return await _tick(bot, data, now, store, limit, release_before)


async def _tick(bot, data, now, store, limit, release_before) -> TickResult:

    now = _utcnow(now)
    store = store if store is not None else await get_store()
    result = TickResult()

    result.released = await store.schedule.release_stale_claims(
        _utcnow(release_before) if release_before is not None else now - CLAIM_TIMEOUT
    )
    if result.released:
        logger.info("Scheduler: released %d stale claim(s) from a previous run" % result.released)

    result.dropped = await store.schedule.drop_stale(now - CATCH_UP_WINDOW)
    if result.dropped:
        logger.warning(
            "Scheduler: dropped %d send(s) overdue by more than %s"
            % (result.dropped, CATCH_UP_WINDOW)
        )

    rows = await store.schedule.claim_due(now, limit=limit)
    result.claimed = len(rows)

    file = File() if rows else None
    for row in rows:
        try:
            if _is_stale(row, now):
                # Claimed, then found to belong to a day that has passed. Marked
                # rather than deleted: a 'failed' row is a record that the window
                # was missed, and it can never be claimed again.
                logger.warning(
                    "Scheduler: skipping stale send #%d (%s -> %d, due %s)"
                    % (row.id, row.kind, row.target_chat_id, row.due_at)
                )
                await store.schedule.mark_failed(row.id)
                result.dropped += 1
                continue
            await _deliver(
                SendCtx(
                    bot=bot,
                    data=data if data is not None else {},
                    file=file,
                    store=store,
                    send=row,
                    now=now,
                )
            )
        except asyncio.CancelledError:
            # Shutdown mid-send. Leave the row 'claimed'; the next boot's
            # catch_up() releases it, and _is_stale decides whether it is still
            # worth delivering.
            raise
        except telegram.error.Forbidden as err:
            # The user blocked or removed the bot. Terminal for this row — there
            # is nothing to retry and no traceback worth printing.
            logger.warning(
                "Scheduler: #%d (%s) not delivered — %d has blocked the bot"
                % (row.id, row.kind, row.target_chat_id)
            )
            await _resolve(store, row, sent=False, result=result, error=err)
            continue
        except PERMANENT_ERRORS as err:
            # Caught *before* TRANSIENT_ERRORS on purpose: telegram.error.BadRequest
            # subclasses NetworkError, so the obvious "except NetworkError: retry"
            # would retry a malformed request every 60 s until drop_stale buried it.
            logger.exception(
                "Scheduler: send #%d (%s -> %d) rejected: %s: %s"
                % (row.id, row.kind, row.target_chat_id, type(err).__name__, err)
            )
            await _resolve(store, row, sent=False, result=result, error=err)
            continue
        except TRANSIENT_ERRORS as err:
            # The reminder is still worth delivering a minute from now, so the row
            # goes back to 'pending' rather than being failed. A thirty-second
            # blip at the reminder instant must not cost the user their day.
            # Bounded by drop_stale: once the row stops being same-day-relevant it
            # is deleted unsent. `attempts` does not cap the retrying — it only
            # makes a row retried unusually often visible in this log line.
            logger.warning(
                "Scheduler: send #%d (%s -> %d) deferred (attempt %d): %s: %s — retrying"
                % (row.id, row.kind, row.target_chat_id, row.attempts + 1, type(err).__name__, err)
            )
            await _release(store, row, result=result, error=err)
            continue
        except Exception as err:
            # F1: one poisoned payload must never stop the queue. Print the
            # traceback, not just the type and message — a bare
            # "Error: KeyError 'plan_day_id'" costs an afternoon.
            logger.exception(
                "Scheduler: send #%d (%s -> %d) failed: %s: %s"
                % (row.id, row.kind, row.target_chat_id, type(err).__name__, err)
            )
            await _resolve(store, row, sent=False, result=result, error=err)
            continue
        await _resolve(store, row, sent=True, result=result, error=None)

    return result


async def _release(store, row: ScheduledSend, result: TickResult, error) -> None:
    """Put a transiently-failed row back on the queue, never raising out of the loop."""
    try:
        await store.schedule.release(row.id)
        result.deferred += 1
        result.errors.append((row.id, error))
    except Exception as err:
        logger.exception(
            "Scheduler: could not release #%d: %s: %s — left claimed for the "
            "next boot to recover" % (row.id, type(err).__name__, err)
        )


async def _resolve(store, row: ScheduledSend, sent: bool, result: TickResult, error) -> None:
    """Move a row out of 'claimed', and never let *that* raise out of the loop.

    If the mark itself fails (the connection died between the send and the
    write), the row stays 'claimed' and `catch_up` will release it on the next
    boot — the one window where a re-send is possible. Documented, not papered
    over.
    """
    try:
        if sent:
            await store.schedule.mark_sent(row.id)
            result.sent += 1
        else:
            await store.schedule.mark_failed(row.id)
            result.failed += 1
            result.errors.append((row.id, error))
    except Exception as err:
        logger.exception(
            "Scheduler: could not mark #%d as %s: %s: %s — left claimed for the "
            "next boot to recover" % (row.id, "sent" if sent else "failed", type(err).__name__, err)
        )


# An asyncio primitive binds to the loop it is first awaited in, and pytest gives
# every test its own loop, so a module-level Lock would hang the second test that
# touched it. Rebuild it whenever the running loop changes — the same pattern as
# `infra/page_image.py`'s stitch semaphore and `infra/store/__init__.py`'s creation
# lock. The lock itself exists so a manual `tick()` (boot catch-up, a test) can
# never interleave with the polling loop's tick and claim the same batch twice.
_tick_lock_obj = None


_tick_lock_loop = None
