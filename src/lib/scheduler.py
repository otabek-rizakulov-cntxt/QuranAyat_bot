# The in-process due-queue scheduler (workstream F).
#
# The app only wakes on webhooks, so anything timed has to be a row in
# `scheduled_send` that a background loop drains. There is no cron, no worker
# process and no job broker: on a 512 MB single-worker instance an asyncio loop
# over a Postgres queue is the whole design (see §2 "Scheduler" in
# docs/HIFZ_PLATFORM.md).
#
# Three properties are load-bearing, and each has a test named after it:
#
#   F1  the loop survives a poisoned row — one send raising must not stop the
#       queue, and must not stop the *next* row in the same batch,
#   F2  enqueueing is idempotent on `(kind, target, local_date)`, so a restart, a
#       double boot or a retry cannot double-send,
#   F3  a window missed while the instance was restarting fires on the next boot
#       *if it is still same-day-relevant*, and is dropped rather than delivered
#       at 3 a.m. otherwise.
#
# **Claim, then send — never send, then mark.** `claim_due` flips a row to
# 'claimed' in one atomic statement (`FOR UPDATE SKIP LOCKED`), and only then is
# the message sent. A crash between the two therefore leaves a claimed-but-unsent
# row, which is recoverable, instead of a sent-but-pending row, which would be
# re-sent. The residual window is described under `catch_up` below.
#
# **Testability.** Nothing here sleeps to make progress: `tick()` performs one
# complete claim-and-send pass and returns what it did, and `run_scheduler()` is
# a thin loop over it. Every acceptance criterion is asserted against `tick()`
# with an injected `now` and an injected store — no monkeypatched `asyncio.sleep`
# anywhere in the suite.

import asyncio
import traceback
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from typing import Any, Awaitable, Callable, Dict, Optional

import telegram

from lib.localtime import local_date, next_due_utc
from lib.store.schedule import ScheduledSend

__all__ = [
    "POLL_INTERVAL_SECONDS", "CLAIM_LIMIT", "CLAIM_TIMEOUT", "CATCH_UP_WINDOW",
    "SEND_HANDLERS", "SendCtx", "TickResult",
    "send_handler", "register_send_handler", "registered_kinds",
    "idempotency_key", "enqueue", "schedule_daily",
    "tick", "catch_up", "run_scheduler",
]


# --- Knobs ---------------------------------------------------------------------

# F1 says "polls every 60 s". A minute of jitter on a daily reminder is invisible
# to a user and costs one trivial query per minute against a table that holds a
# few rows per user per day.
POLL_INTERVAL_SECONDS = 60

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


# --- The handler registry ------------------------------------------------------
#
# The scheduler knows how to claim a row, when to give up on it and how to keep
# the queue moving. It deliberately knows nothing about what a 'plan_day' *is* —
# that is the drill's business. Feature modules register a coroutine per `kind`,
# exactly as `src/hifz/__init__.py` registers commands, so nobody has to edit
# this file to add a scheduled send:
#
#     # src/hifz/memorize.py
#     from lib.scheduler import SendCtx, send_handler
#
#     @send_handler("plan_day")
#     async def push_plan_day(ctx: SendCtx) -> None:
#         plan_day_id = ctx.payload["plan_day_id"]
#         claimed = await ctx.store.plans.claim_plan_day(plan_day_id)
#         if claimed is None:
#             return                      # already delivered; nothing to do
#         await send_quran(ctx.bot, ctx.data, ctx.file, ...)
#
# Contract for a handler:
#   * it is `async def handler(ctx: SendCtx) -> None`,
#   * returning normally means delivered — the row is marked 'sent',
#   * raising means not delivered — the row is marked 'failed' and the loop moves
#     on to the next row. There is no retry (see the note on `mark_failed`
#     below), so raise only when the send genuinely did not happen,
#   * `telegram.error.Forbidden` is swallowed as terminal: the user blocked the
#     bot, and no amount of retrying fixes that,
#   * it must be idempotent where it can be. `claim_plan_day` is a conditional
#     write for exactly this reason: it returns None the second time.

SendHandler = Callable[["SendCtx"], Awaitable[None]]

# Which Telegram failures are worth trying again in a minute, and which are not.
#
# The ordering trap: `telegram.error.BadRequest` **subclasses** `NetworkError` in
# python-telegram-bot, so `except NetworkError: retry` would quietly retry a
# malformed request every 60 s until `drop_stale` buried it. PERMANENT_ERRORS is
# therefore caught first, and lists BadRequest explicitly.
#
# Retrying is bounded by time, not by count: `drop_stale` deletes a row once it
# stops being same-day-relevant, which caps a transient failure at roughly six
# hours of 60-second retries and then gives up silently. `attempts` on the row
# does not change that cap — it exists purely so a row retried unusually often
# is observable instead of only visible in scrolled-past logs.
PERMANENT_ERRORS = (
    telegram.error.BadRequest,      # malformed request — retrying cannot help
    telegram.error.InvalidToken,
    telegram.error.ChatMigrated,
)
TRANSIENT_ERRORS = (
    telegram.error.RetryAfter,      # rate limited; not a NetworkError subclass
    telegram.error.TimedOut,
    telegram.error.NetworkError,    # must come after BadRequest is excluded
)

SEND_HANDLERS: Dict[str, SendHandler] = {}


def register_send_handler(kind: str, handler: SendHandler) -> SendHandler:
    """Bind `kind` to `handler`. Registering a kind twice raises.

    A silent overwrite would mean one feature module quietly stealing another's
    sends, so this fails at import time instead — same rule as `hifz.command`.
    """
    existing = SEND_HANDLERS.get(kind)
    if existing is not None and existing is not handler \
            and not _same_origin(existing, handler):
        raise ValueError("scheduled kind %r is already handled by %s"
                         % (kind, getattr(existing, "__module__", "?")))
    SEND_HANDLERS[kind] = handler
    return handler


def _same_origin(a, b) -> bool:
    """Whether two functions are the same declaration, across a module reload.

    Identity is the obvious test and the wrong one: `hifz.load_features` reloads
    already-imported feature modules so their decorators run again, and a reload
    produces a *new* function object for the same `def`. Under identity that reads
    as a second module stealing the kind and raises. Module plus qualified name is
    stable across a reload and still distinct between two real features, which is
    the collision this guard exists to catch.
    """
    return (getattr(a, "__module__", None) == getattr(b, "__module__", None)
            and getattr(a, "__qualname__", None) == getattr(b, "__qualname__", None))


def send_handler(kind: str):
    """Decorator form: `@send_handler("plan_day")`."""
    def decorate(handler: SendHandler) -> SendHandler:
        return register_send_handler(kind, handler)
    return decorate


def registered_kinds() -> Dict[str, str]:
    """`{kind: defining module}` — for the boot log and for debugging."""
    return {kind: getattr(fn, "__module__", "?") for kind, fn in SEND_HANDLERS.items()}


# --- The handler context -------------------------------------------------------

@dataclass(frozen=True)
class SendCtx:
    """Everything a scheduled-send handler needs, assembled once per row.

    Deliberately shaped like `hifz.Ctx`: a handler reads its context and writes
    through `store`. There is no `ui_lang` here — a scheduled push happens
    outside any update, so the handler looks the recipient's settings up itself
    (`store.profiles.get_settings`), which is also what makes a group post in one
    admin-chosen language possible in Phase 2.
    """

    bot: Any                  # telegram.Bot (an AsyncMock under test)
    data: dict                # the shared corpora dict built by main.build_data
    file: Any                 # lib.utils.File — media cache + nav state
    store: Any                # lib.store.Store
    send: ScheduledSend       # the row being delivered

    @property
    def kind(self) -> str:
        return self.send.kind

    @property
    def chat_id(self) -> int:
        return self.send.target_chat_id

    @property
    def thread_id(self) -> Optional[int]:
        """The forum topic to post into, or None for a plain chat (Phase 2)."""
        return self.send.thread_id

    @property
    def payload(self) -> Dict[str, Any]:
        return self.send.payload

    async def reply(self, text: str, **kwargs) -> Any:
        """Send a message to the target chat, into the bound topic if there is one."""
        if self.thread_id is not None:
            kwargs.setdefault("message_thread_id", self.thread_id)
        return await self.bot.send_message(chat_id=self.chat_id, text=text, **kwargs)


# --- Enqueueing (F2) -----------------------------------------------------------

def idempotency_key(kind: str, target_chat_id: int, local_day) -> str:
    """The canonical `(kind, target, local_date)` key, e.g. `plan_day:42:2026-08-01`.

    The uniqueness of this string is the entire duplicate-send defence, so it is
    built in one place rather than formatted at each call site. `local_day` may
    be a `date` or an ISO string.
    """
    day = local_day.isoformat() if isinstance(local_day, date) else str(local_day)
    return "%s:%d:%s" % (kind, target_chat_id, day)


async def enqueue(store, kind: str, target_chat_id: int, due_at: datetime,
                  local_day=None, payload: Optional[Dict[str, Any]] = None,
                  thread_id: Optional[int] = None,
                  key: Optional[str] = None) -> Optional[ScheduledSend]:
    """Queue one send. Returns the row, or None if that key is already queued.

    Enqueueing the same key twice inserts one row and raises nothing — that is
    F2, and it is what makes a double boot or a re-run of the day's scheduling
    pass harmless. Pass either `local_day` (the key is derived) or an explicit
    `key`.
    """
    if key is None:
        if local_day is None:
            raise ValueError("enqueue needs either local_day or an explicit key")
        key = idempotency_key(kind, target_chat_id, local_day)
    return await store.schedule.enqueue(kind, target_chat_id, due_at, key,
                                        payload=payload, thread_id=thread_id)


async def schedule_daily(store, kind: str, target_chat_id: int, reminder_time: time,
                         offset: str, now: Optional[datetime] = None,
                         payload: Optional[Dict[str, Any]] = None,
                         thread_id: Optional[int] = None) -> Optional[ScheduledSend]:
    """Queue the next occurrence of a daily push at the user's local `reminder_time`.

    `offset` is a fixed UTC offset (`"+05:00"`); all the arithmetic goes through
    `lib.localtime`, never through hand-rolled timedeltas. The due instant is the
    first one strictly after `now` at which the recipient's wall clock reads
    `reminder_time`, and the key is keyed on the *local* date of that instant —
    so scheduling twice in the same local day is a no-op, and the row for
    tomorrow can be queued the moment today's fires.

    The recipient's offset is copied into the payload (unless the caller already
    put one there) because staleness is a local-day question: see `_is_stale`.
    """
    now = _utcnow(now)
    due_at = next_due_utc(reminder_time, offset, now)
    day = local_date(due_at, offset)
    body = dict(payload or {})
    body.setdefault("offset", offset)
    return await enqueue(store, kind, target_chat_id, due_at, local_day=day,
                         payload=body, thread_id=thread_id)


# --- The loop (F1, F3) ---------------------------------------------------------

@dataclass
class TickResult:
    """What one pass did. Returned so tests (and the boot log) can assert on it
    instead of scraping stdout."""

    claimed: int = 0
    sent: int = 0
    failed: int = 0
    dropped: int = 0        # too late to be worth delivering
    released: int = 0       # claims recovered from a dead process
    deferred: int = 0       # transient failure, back on the queue for the next tick
    errors: list = field(default_factory=list)   # (send_id, exception) per failure

    def __bool__(self) -> bool:
        return bool(self.claimed or self.dropped or self.released)


# An asyncio primitive binds to the loop it is first awaited in, and pytest gives
# every test its own loop, so a module-level Lock would hang the second test that
# touched it. Rebuild it whenever the running loop changes — the same pattern as
# `lib/page_image.py`'s stitch semaphore and `lib/store/__init__.py`'s creation
# lock. The lock itself exists so a manual `tick()` (boot catch-up, a test) can
# never interleave with the polling loop's tick and claim the same batch twice.
_tick_lock_obj = None
_tick_lock_loop = None


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
            return False        # unparseable offset: fall back to the window alone
    return False


async def _deliver(ctx: SendCtx) -> None:
    """Run the handler registered for this row's kind."""
    handler = SEND_HANDLERS.get(ctx.kind)
    if handler is None:
        raise LookupError(
            "no handler registered for scheduled kind %r (registered: %s)"
            % (ctx.kind, ", ".join(sorted(SEND_HANDLERS)) or "none"))
    await handler(ctx)


async def tick(bot, data: Optional[dict] = None, now: Optional[datetime] = None,
               store=None, limit: int = CLAIM_LIMIT,
               release_before: Optional[datetime] = None) -> TickResult:
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
    from lib.store import get_store
    from lib.utils import File

    now = _utcnow(now)
    store = store if store is not None else await get_store()
    result = TickResult()

    result.released = await store.schedule.release_stale_claims(
        _utcnow(release_before) if release_before is not None else now - CLAIM_TIMEOUT)
    if result.released:
        print("Scheduler: released %d stale claim(s) from a previous run"
              % result.released)

    result.dropped = await store.schedule.drop_stale(now - CATCH_UP_WINDOW)
    if result.dropped:
        print("Scheduler: dropped %d send(s) overdue by more than %s"
              % (result.dropped, CATCH_UP_WINDOW))

    rows = await store.schedule.claim_due(now, limit=limit)
    result.claimed = len(rows)

    file = File() if rows else None
    for row in rows:
        try:
            if _is_stale(row, now):
                # Claimed, then found to belong to a day that has passed. Marked
                # rather than deleted: a 'failed' row is a record that the window
                # was missed, and it can never be claimed again.
                print("Scheduler: skipping stale send #%d (%s -> %d, due %s)"
                      % (row.id, row.kind, row.target_chat_id, row.due_at))
                await store.schedule.mark_failed(row.id)
                result.dropped += 1
                continue
            await _deliver(SendCtx(bot=bot, data=data if data is not None else {},
                                   file=file, store=store, send=row))
        except asyncio.CancelledError:
            # Shutdown mid-send. Leave the row 'claimed'; the next boot's
            # catch_up() releases it, and _is_stale decides whether it is still
            # worth delivering.
            raise
        except telegram.error.Forbidden as err:
            # The user blocked or removed the bot. Terminal for this row — there
            # is nothing to retry and no traceback worth printing.
            print("Scheduler: #%d (%s) not delivered — %d has blocked the bot"
                  % (row.id, row.kind, row.target_chat_id))
            await _resolve(store, row, sent=False, result=result, error=err)
            continue
        except PERMANENT_ERRORS as err:
            # Caught *before* TRANSIENT_ERRORS on purpose: telegram.error.BadRequest
            # subclasses NetworkError, so the obvious "except NetworkError: retry"
            # would retry a malformed request every 60 s until drop_stale buried it.
            print("Scheduler: send #%d (%s -> %d) rejected: %s: %s"
                  % (row.id, row.kind, row.target_chat_id, type(err).__name__, err))
            traceback.print_exc()
            await _resolve(store, row, sent=False, result=result, error=err)
            continue
        except TRANSIENT_ERRORS as err:
            # The reminder is still worth delivering a minute from now, so the row
            # goes back to 'pending' rather than being failed. A thirty-second
            # blip at the reminder instant must not cost the user their day.
            # Bounded by drop_stale: once the row stops being same-day-relevant it
            # is deleted unsent. `attempts` does not cap the retrying — it only
            # makes a row retried unusually often visible in this log line.
            print("Scheduler: send #%d (%s -> %d) deferred (attempt %d): %s: %s — retrying"
                  % (row.id, row.kind, row.target_chat_id, row.attempts + 1,
                     type(err).__name__, err))
            await _release(store, row, result=result, error=err)
            continue
        except Exception as err:
            # F1: one poisoned payload must never stop the queue. Print the
            # traceback, not just the type and message — a bare
            # "Error: KeyError 'plan_day_id'" costs an afternoon.
            print("Scheduler: send #%d (%s -> %d) failed: %s: %s"
                  % (row.id, row.kind, row.target_chat_id, type(err).__name__, err))
            traceback.print_exc()
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
        print("Scheduler: could not release #%d: %s: %s — left claimed for the "
              "next boot to recover" % (row.id, type(err).__name__, err))
        traceback.print_exc()


async def _resolve(store, row: ScheduledSend, sent: bool, result: TickResult,
                   error) -> None:
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
        print("Scheduler: could not mark #%d as %s: %s: %s — left claimed for the "
              "next boot to recover" % (row.id, "sent" if sent else "failed",
                                        type(err).__name__, err))
        traceback.print_exc()


async def catch_up(bot, data: Optional[dict] = None, now: Optional[datetime] = None,
                   store=None) -> TickResult:
    """The first pass after boot (F3).

    Identical to `tick`, except that *every* outstanding claim is released rather
    than only those older than `CLAIM_TIMEOUT`. The deployment runs a single
    uvicorn worker (see `Procfile`), so at boot no other process can be holding a
    claim: a row still marked 'claimed' can only be one this instance's
    predecessor died on, and waiting five minutes to recover it would delay a
    reminder for no reason.

    **The one window where a duplicate is possible.** If the process died after
    Telegram accepted the message but before `mark_sent` committed, the row is
    still 'claimed', this call returns it to 'pending', and it is delivered a
    second time. Closing that would need a distributed transaction with
    Telegram's API, which does not exist. It is bounded instead:

      * it requires a crash inside the milliseconds between the two calls,
      * `_is_stale` still applies, so it can only ever re-send *today's* portion,
        never a backlog, and
      * handlers make it a no-op where they can — `claim_plan_day` is a
        conditional write, so a re-delivered plan day sends nothing the second
        time.

    The alternative (mark sent first, then send) would turn every crash into a
    silently *missed* reminder, which is worse and undetectable.
    """
    return await tick(bot, data, now=now, store=store, release_before=_utcnow(now))


async def run_scheduler(bot, data: Optional[dict] = None,
                        interval: float = POLL_INTERVAL_SECONDS, store=None,
                        stop_event: Optional[asyncio.Event] = None,
                        max_ticks: Optional[int] = None) -> None:
    """Poll the due-queue forever. Started from `_initialize()` in `src/main.py`.

    The first pass is `catch_up` (boot recovery), every later one is a plain
    `tick`. A tick that raises is logged with a traceback and the loop continues:
    the queue outliving a bad row is the entire point of F1, and it must outlive
    a transient database blip too.

    Stops on: `stop_event` being set, `max_ticks` passes (tests only), or task
    cancellation — which is how production stops it, when uvicorn tears the loop
    down. Nothing is left half-done by a cancellation; an in-flight row stays
    'claimed' and the next boot recovers it.
    """
    print("Scheduler: started (poll every %ss, handlers: %s)"
          % (interval, ", ".join(sorted(SEND_HANDLERS)) or "none"))
    ticks = 0
    try:
        while max_ticks is None or ticks < max_ticks:
            try:
                if ticks == 0:
                    await catch_up(bot, data, store=store)
                else:
                    await tick(bot, data, store=store)
            except asyncio.CancelledError:
                raise
            except Exception as err:
                print("Scheduler: tick failed: %s: %s" % (type(err).__name__, err))
                traceback.print_exc()
            ticks += 1
            if stop_event is not None and stop_event.is_set():
                break
            if max_ticks is not None and ticks >= max_ticks:
                break
            await _wait(interval, stop_event)
            if stop_event is not None and stop_event.is_set():
                break
    except asyncio.CancelledError:
        print("Scheduler: cancelled after %d tick(s)" % ticks)
        raise
    print("Scheduler: stopped after %d tick(s)" % ticks)


async def _wait(interval: float, stop_event: Optional[asyncio.Event]) -> None:
    """Sleep `interval` seconds, cut short by `stop_event`.

    Waiting on the event rather than sleeping blindly means shutdown is prompt
    instead of taking up to a minute.
    """
    if stop_event is None:
        await asyncio.sleep(interval)
        return
    try:
        await asyncio.wait_for(stop_event.wait(), timeout=interval)
    except asyncio.TimeoutError:
        pass


# --- Built-in kinds ------------------------------------------------------------

@send_handler("message")
async def _send_plain_message(ctx: SendCtx) -> None:
    """`kind="message"` — deliver `payload["text"]` to the target chat.

    The simplest possible scheduled send, and a real one: the weekly leaderboard
    post (H) and any future announcement need nothing more. It also means the
    loop is exercised end to end before the drill exists.

    Payload: `{"text": str, "parse_mode": str | None}` — `parse_mode` defaults to
    HTML, matching every other send in this codebase.
    """
    text = ctx.payload.get("text")
    if not text:
        raise ValueError("message payload has no 'text' (send #%d)" % ctx.send.id)
    kwargs = {}
    if "parse_mode" in ctx.payload:
        if ctx.payload["parse_mode"] is not None:
            kwargs["parse_mode"] = ctx.payload["parse_mode"]
    else:
        kwargs["parse_mode"] = "HTML"
    await ctx.reply(text, **kwargs)
