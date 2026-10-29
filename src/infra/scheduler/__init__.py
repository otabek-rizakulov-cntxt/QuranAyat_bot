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
from infra.scheduler.enqueue import enqueue, idempotency_key, schedule_daily
from infra.scheduler.registry import (
    SEND_HANDLERS,
    SendCtx,
    register_send_handler,
    registered_kinds,
    send_handler,
)
from infra.scheduler.runner import POLL_INTERVAL_SECONDS, catch_up, run_scheduler
from infra.scheduler.tick import CATCH_UP_WINDOW, CLAIM_LIMIT, CLAIM_TIMEOUT, TickResult, tick

__all__ = [
    "POLL_INTERVAL_SECONDS",
    "CLAIM_LIMIT",
    "CLAIM_TIMEOUT",
    "CATCH_UP_WINDOW",
    "SEND_HANDLERS",
    "SendCtx",
    "TickResult",
    "send_handler",
    "register_send_handler",
    "registered_kinds",
    "idempotency_key",
    "enqueue",
    "schedule_daily",
    "tick",
    "catch_up",
    "run_scheduler",
]


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
