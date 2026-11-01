"""The handler context: everything a command, callback or wizard handler needs."""

from dataclasses import dataclass
from typing import Any

from channels import TELEGRAM
from channels.telegram import TelegramChannel
from infra.store import get_store
from infra.wizard_store import Wizard
from locales import t


@dataclass(frozen=True)
class Ctx:
    """Everything a hifz handler needs, assembled once by the seam.

    Frozen: a handler reads its context and writes through `store`, never by
    mutating what it was handed.
    """

    bot: Any  # telegram.Bot (an AsyncMock under test)
    data: dict  # the shared corpora dict built by main.build_data
    file: Any  # infra.file_facade.File — media cache + nav state
    store: Any  # infra.store.Store — profiles/hifz/plans/sessions/schedule
    chat_id: int
    user_id: int
    ui_lang: str
    translation_lang: str
    reciter: str
    argument: str = ""  # text after the command: "/check 67" -> "67"
    callback_query: Any = None  # telegram.CallbackQuery, on a callback dispatch
    message: Any = None  # telegram.Message, on a message dispatch
    # channels.Channel bound to this chat. Every send goes through it; `bot`
    # stays only for the hifz features not yet converted (MULTI_PLATFORM_PLAN P3.5).
    channel: Any = None
    platform: str = TELEGRAM

    def __post_init__(self):
        if self.channel is None:
            object.__setattr__(self, "channel", TelegramChannel(self.bot, self.chat_id))

    # --- construction ---------------------------------------------------------

    @classmethod
    async def build(cls, bot, data, file, chat_id: int, user_id: int, settings, **kwargs) -> "Ctx":
        """Build a Ctx from the dispatcher's per-update values.

        `settings` is the UserSettingsRow-shaped object `_resolve_settings`
        returns. The store is fetched here so no call site has to know that
        storage is a coroutine-guarded singleton.
        """

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
        """The user's wizard-draft store (see infra/wizard_store.py)."""
        return Wizard()

    def tr(self, key: str, **fmt: Any) -> str:
        """A localized string in the caller's UI language, formatted.

        `ctx.tr("plan_saved", first_date="2026-08-01")` — placeholders are named,
        and every one is multiplied by 47 translators, so keep them few.
        """
        text = t(key, self.ui_lang)
        return text.format(**fmt) if fmt else text

    @property
    def from_inline(self) -> bool:
        """A tap on a card shared through inline mode: there is no message of ours
        to edit, and the tapper may never have opened a DM with the bot."""
        return self.callback_query is not None and self.callback_query.message is None

    def _editable(self):
        """The tapped message, if this channel can rewrite it; else None."""
        if not self.channel.caps.can_edit:
            return None
        return getattr(self.callback_query, "message", None)

    async def reply(self, text: str, choices=None, **kwargs) -> Any:
        """Send a message to the caller's chat.

        `choices` are neutral buttons (channels.Choice rows); `html=True` marks
        the text as Telegram HTML. Telegram-only kwargs (`reply_markup`,
        `parse_mode`) still pass straight through for unconverted callers.
        """
        return await self.channel.send_text(text, choices, **kwargs)

    async def answer(self, text: str = None, show_alert: bool = False) -> None:
        """Acknowledge the tap, so the client stops spinning. No-op off a callback."""
        if self.callback_query is None:
            return
        await self.channel.answer(self.callback_query.id, text, show_alert)

    async def edit(self, text: str, choices=None, **kwargs) -> bool:
        """Edit the tapped message in place; send a fresh one if that isn't possible.

        Returns True if the message was edited. A fresh message goes out when there
        is nothing of ours to edit (an inline-mode card), the tapped message is a
        photo or audio, or the platform cannot edit at all. Re-tapping the view you
        are already in produces an identical message, which is a no-op, not an error.
        """
        msg = self._editable()
        if msg is None or msg.photo or msg.audio:
            await self.reply(text, choices, **kwargs)
            return False
        return await self.channel.edit_text(msg.message_id, text, choices, **kwargs)

    async def edit_choices(self, choices, text_if_new: str = None) -> bool:
        """Swap the tapped message's buttons, keeping its text.

        Where the platform cannot edit, `text_if_new` is sent with the new buttons
        instead (nothing is sent without it). Off a message of ours, does nothing.
        """
        if self.callback_query is None or self.callback_query.message is None:
            return False
        msg = self._editable()
        if msg is None:
            if text_if_new is not None:
                await self.reply(text_if_new, choices)
            return False
        return await self.channel.edit_choices(msg.message_id, choices)
