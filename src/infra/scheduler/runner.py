"""Running the scheduler: catch up once at boot, then tick on a fixed interval
until the app shuts down."""

import asyncio
import logging
from datetime import datetime
from typing import Optional

from infra.scheduler.registry import SEND_HANDLERS
from infra.scheduler.tick import TickResult, _utcnow, tick

logger = logging.getLogger(__name__)


# F1 says "polls every 60 s". A minute of jitter on a daily reminder is invisible
# to a user and costs one trivial query per minute against a table that holds a
# few rows per user per day.
POLL_INTERVAL_SECONDS = 60


async def catch_up(
    bot, data: Optional[dict] = None, now: Optional[datetime] = None, store=None
) -> TickResult:
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


async def run_scheduler(
    bot,
    data: Optional[dict] = None,
    interval: float = POLL_INTERVAL_SECONDS,
    store=None,
    stop_event: Optional[asyncio.Event] = None,
    max_ticks: Optional[int] = None,
) -> None:
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
    logger.info(
        "Scheduler: started (poll every %ss, handlers: %s)"
        % (interval, ", ".join(sorted(SEND_HANDLERS)) or "none")
    )
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
                logger.exception("Scheduler: tick failed: %s: %s" % (type(err).__name__, err))
            ticks += 1
            if stop_event is not None and stop_event.is_set():
                break
            if max_ticks is not None and ticks >= max_ticks:
                break
            await _wait(interval, stop_event)
            if stop_event is not None and stop_event.is_set():
                break
    except asyncio.CancelledError:
        logger.info("Scheduler: cancelled after %d tick(s)" % ticks)
        raise
    logger.info("Scheduler: stopped after %d tick(s)" % ticks)


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
