"""The send-handler registry and the context a handler receives.

The scheduler knows how to claim a row, when to give up on it and how to keep
the queue moving. It deliberately knows nothing about what a 'plan_day' *is* —
that is the drill's business. Feature modules register a coroutine per `kind`,
exactly as `src/bot/features/__init__.py` registers commands, so nobody has to edit
this file to add a scheduled send:

    # src/bot/features/memorize.py
    from infra.scheduler import SendCtx, send_handler

    @send_handler("plan_day")
    async def push_plan_day(ctx: SendCtx) -> None:
        plan_day_id = ctx.payload["plan_day_id"]
        claimed = await ctx.store.plans.claim_plan_day(plan_day_id)
        if claimed is None:
            return                      # already delivered; nothing to do
        await send_quran(ctx.bot, ctx.data, ...)

Contract for a handler:
  * it is `async def handler(ctx: SendCtx) -> None`,
  * returning normally means delivered — the row is marked 'sent',
  * raising means not delivered — the row is marked 'failed' and the loop moves
    on to the next row. There is no retry (see the note on `mark_failed`
    below), so raise only when the send genuinely did not happen,
  * `telegram.error.Forbidden` is swallowed as terminal: the user blocked the
    bot, and no amount of retrying fixes that,
  * it must be idempotent where it can be. `claim_plan_day` is a conditional
    write for exactly this reason: it returns None the second time.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Awaitable, Callable, Dict, Optional

import telegram

from infra.store.schedule import ScheduledSend

SendHandler = Callable[["SendCtx"], Awaitable[None]]


SEND_HANDLERS: Dict[str, SendHandler] = {}


def register_send_handler(kind: str, handler: SendHandler) -> SendHandler:
    """Bind `kind` to `handler`. Registering a kind twice raises.

    A silent overwrite would mean one feature module quietly stealing another's
    sends, so this fails at import time instead — same rule as `bot.features.command`.
    """
    existing = SEND_HANDLERS.get(kind)
    if existing is not None and existing is not handler and not _same_origin(existing, handler):
        raise ValueError(
            "scheduled kind %r is already handled by %s"
            % (kind, getattr(existing, "__module__", "?"))
        )
    SEND_HANDLERS[kind] = handler
    return handler


def _same_origin(a, b) -> bool:
    """Whether two functions are the same declaration, across a module reload.

    Identity is the obvious test and the wrong one: `bot.features.load_features` reloads
    already-imported feature modules so their decorators run again, and a reload
    produces a *new* function object for the same `def`. Under identity that reads
    as a second module stealing the kind and raises. Module plus qualified name is
    stable across a reload and still distinct between two real features, which is
    the collision this guard exists to catch.
    """
    return getattr(a, "__module__", None) == getattr(b, "__module__", None) and getattr(
        a, "__qualname__", None
    ) == getattr(b, "__qualname__", None)


def send_handler(kind: str):
    """Decorator form: `@send_handler("plan_day")`."""

    def decorate(handler: SendHandler) -> SendHandler:
        return register_send_handler(kind, handler)

    return decorate


def registered_kinds() -> Dict[str, str]:
    """`{kind: defining module}` — for the boot log and for debugging."""
    return {kind: getattr(fn, "__module__", "?") for kind, fn in SEND_HANDLERS.items()}


@dataclass(frozen=True)
class SendCtx:
    """Everything a scheduled-send handler needs, assembled once per row.

    Deliberately shaped like `bot.features.Ctx`: a handler reads its context and writes
    through `store`. There is no `ui_lang` here — a scheduled push happens
    outside any update, so the handler looks the recipient's settings up itself
    (`store.profiles.get_settings`), which is also what makes a group post in one
    admin-chosen language possible in Phase 2.
    """

    bot: Any  # telegram.Bot (an AsyncMock under test)
    data: dict  # the shared corpora dict built by main.build_data
    file: Any  # infra.file_facade.File — media cache + nav state
    store: Any  # infra.store.Store
    send: ScheduledSend  # the row being delivered
    # The tick's notion of "now". A handler that queues a follow-up (the next
    # portion, next week's board) computes it from this, not from the wall
    # clock, so a tick run with an injected time stays consistent with itself.
    now: Optional[datetime] = None

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
    telegram.error.BadRequest,  # malformed request — retrying cannot help
    telegram.error.InvalidToken,
    telegram.error.ChatMigrated,
)


TRANSIENT_ERRORS = (
    telegram.error.RetryAfter,  # rate limited; not a NetworkError subclass
    telegram.error.TimedOut,
    telegram.error.NetworkError,  # must come after BadRequest is excluded
)
