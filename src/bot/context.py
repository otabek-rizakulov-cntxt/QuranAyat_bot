"""The handler context: everything a command, callback or wizard handler needs."""

from dataclasses import dataclass
from typing import Any

from bot.errors import ignore_not_modified
from lib.wizard import Wizard
from locales import t


@dataclass(frozen=True)
class Ctx:
    """Everything a hifz handler needs, assembled once by the seam.

    Frozen: a handler reads its context and writes through `store`, never by
    mutating what it was handed.
    """

    bot: Any  # telegram.Bot (an AsyncMock under test)
    data: dict  # the shared corpora dict built by main.build_data
    file: Any  # lib.utils.File — media cache + nav state
    store: Any  # lib.store.Store — profiles/hifz/plans/sessions/schedule
    chat_id: int
    user_id: int
    ui_lang: str
    translation_lang: str
    reciter: str
    argument: str = ""  # text after the command: "/check 67" -> "67"
    callback_query: Any = None  # telegram.CallbackQuery, on a callback dispatch
    message: Any = None  # telegram.Message, on a message dispatch

    # --- construction ---------------------------------------------------------

    @classmethod
    async def build(cls, bot, data, file, chat_id: int, user_id: int, settings, **kwargs) -> "Ctx":
        """Build a Ctx from the dispatcher's per-update values.

        `settings` is the UserSettingsRow-shaped object `_resolve_settings`
        returns. The store is fetched here so no call site has to know that
        storage is a coroutine-guarded singleton.
        """
        from lib.store import get_store

        return cls(
            bot=bot,
            data=data,
            file=file,
            store=await get_store(),
            chat_id=chat_id,
            user_id=user_id,
            ui_lang=settings.ui_lang,
            translation_lang=settings.translation_lang,
            reciter=settings.reciter,
            **kwargs,
        )

    # --- conveniences ---------------------------------------------------------

    @property
    def wiz(self) -> Wizard:
        """The user's wizard-draft store (see lib/wizard.py)."""
        return Wizard()

    def tr(self, key: str, **fmt: Any) -> str:
        """A localized string in the caller's UI language, formatted.

        `ctx.tr("plan_saved", first_date="2026-08-01")` — placeholders are named,
        and every one is multiplied by 47 translators, so keep them few.
        """
        text = t(key, self.ui_lang)
        return text.format(**fmt) if fmt else text

    async def reply(self, text: str, **kwargs) -> Any:
        """Send a message to the caller's chat."""
        return await self.bot.send_message(chat_id=self.chat_id, text=text, **kwargs)

    async def answer(self, text: str = None, show_alert: bool = False) -> None:
        """Acknowledge the tap, so the client stops spinning. No-op off a callback."""
        if self.callback_query is None:
            return
        if text is None:
            await self.bot.answer_callback_query(self.callback_query.id)
        else:
            await self.bot.answer_callback_query(
                self.callback_query.id, text=text, show_alert=show_alert
            )

    async def edit(self, text: str, **kwargs) -> bool:
        """Edit the tapped message in place; send a fresh one if that isn't possible.

        Returns True if the message was edited. Re-tapping the view you are
        already in produces an identical message, and Telegram answers "message
        is not modified" — that is a no-op, not an error (bot.errors).
        """
        msg = getattr(self.callback_query, "message", None)
        if msg is None or msg.photo or msg.audio:
            await self.reply(text, **kwargs)
            return False
        with ignore_not_modified():
            await self.bot.edit_message_text(
                text=text, chat_id=self.chat_id, message_id=msg.message_id, **kwargs
            )
        return True
