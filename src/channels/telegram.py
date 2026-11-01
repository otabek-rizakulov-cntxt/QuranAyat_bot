"""The Telegram channel: `Channel` calls onto python-telegram-bot.

Byte-for-byte what the bot sends today — `to_markup` builds the same
InlineKeyboardMarkup the keyboards built by hand, media goes through the same
file_id cache (`send_cached`), and nothing is added to a send unless the caller
asked for it.

Transport only, in the infra tier (tests/test_layering.py): this module may not
import `bot`, so the Telegram plumbing the bot layer used to own — the file_id
cache and "not modified" handling — lives here, and `bot` re-exports it.
"""

import logging
from contextlib import contextmanager
from typing import Any, List, Optional

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from channels.base import TELEGRAM, Caps, Choice, Choices, MediaSource
from infra import media_cache

logger = logging.getLogger(__name__)

# Telegram allows up to 100 inline buttons; there is no separate list picker.
CAPS = Caps(max_buttons=100, list_rows=0, can_edit=True, inline_mode=True, web_app=True)

_ACTIONS = {
    "text": telegram.constants.ChatAction.TYPING,
    "photo": telegram.constants.ChatAction.UPLOAD_PHOTO,
    "audio": telegram.constants.ChatAction.UPLOAD_VOICE,
}


@contextmanager
def ignore_not_modified():
    """Swallow Telegram's "message is not modified", re-raise every other BadRequest.

    Re-tapping the view a message already shows edits it into an identical
    message, and Telegram rejects that edit. Nothing went wrong: the message
    already says what the tap asked for.
    """
    try:
        yield
    except telegram.error.BadRequest as err:
        if "not modified" not in str(err).lower():
            raise


async def _send(bot, kind: str, source, **kwargs) -> str:
    """Send a photo or an audio file and return the file_id Telegram assigned."""
    if kind == "photo":
        result = await bot.send_photo(photo=source, **kwargs)
        return result.photo[-1].file_id
    result = await bot.send_audio(audio=source, **kwargs)
    return result.audio.file_id


async def send_cached(
    bot, kind: str, key: str, build, *, chat_id: int, upload_action: bool = True, **kwargs
) -> str:
    """Send media through the file_id cache: replay the id cached under `key`,
    or — on a miss, or when Telegram rejects the cached id (e.g. expired) —
    upload what `build()` returns and cache the new id under `key`.

    `kind` is "photo" or "audio". `build` is a coroutine function, called only
    when an upload is needed, returning a URL or a file-like object. On an upload
    the chat sees "uploading…" first, unless `upload_action=False` (when the
    caller has shown it already).
    """
    cached_id = media_cache.get(key)
    if cached_id is not None:
        try:
            return await _send(bot, kind, cached_id, chat_id=chat_id, **kwargs)
        except telegram.error.TelegramError as err:
            # a file_id can go stale; treat the rejection as a miss, not a failure
            logger.warning("cached file_id for %s rejected (%s); re-uploading", key, err)

    if upload_action:
        await bot.send_chat_action(chat_id=chat_id, action=_ACTIONS[kind])
    file_id = await _send(bot, kind, await build(), chat_id=chat_id, **kwargs)
    media_cache.save(key, file_id)
    return file_id


def to_button(choice: Choice) -> InlineKeyboardButton:
    if choice.data is not None:
        return InlineKeyboardButton(choice.label, callback_data=choice.data)
    if choice.url is not None:
        return InlineKeyboardButton(choice.label, url=choice.url)
    if choice.web_app is not None:
        return InlineKeyboardButton(choice.label, web_app=WebAppInfo(url=choice.web_app))
    return InlineKeyboardButton(choice.label, switch_inline_query=choice.switch_inline)


def to_markup(choices: Optional[Choices]) -> Optional[InlineKeyboardMarkup]:
    """`Choices` as an inline keyboard; None (no keyboard) for None or no rows."""
    if not choices:
        return None
    return InlineKeyboardMarkup([[to_button(c) for c in row] for row in choices])


async def _build(source: MediaSource) -> Any:
    """Resolve a media source: call a builder, pass anything else through."""
    return await source() if callable(source) else source


class TelegramChannel:
    """One Telegram chat — a DM, or a group optionally pinned to a forum topic."""

    platform = TELEGRAM
    caps = CAPS

    def __init__(self, bot, chat_id: int, thread_id: Optional[int] = None):
        self.bot = bot
        self.chat_id = chat_id
        self.thread_id = thread_id

    def __repr__(self) -> str:
        return "TelegramChannel(chat_id=%r, thread_id=%r)" % (self.chat_id, self.thread_id)

    def _opts(self, choices: Optional[Choices], html: bool, opts: dict) -> dict:
        """Merge the neutral arguments into Telegram kwargs; explicit ones win."""
        markup = to_markup(choices)
        if markup is not None:
            opts.setdefault("reply_markup", markup)
        if html:
            opts.setdefault("parse_mode", "HTML")
        if self.thread_id is not None:
            opts.setdefault("message_thread_id", self.thread_id)
        return opts

    async def send_text(
        self, text: str, choices: Optional[Choices] = None, *, html: bool = False, **opts
    ) -> Any:
        return await self.bot.send_message(
            chat_id=self.chat_id, text=text, **self._opts(choices, html, opts)
        )

    async def edit_text(
        self,
        message_id: Any,
        text: str,
        choices: Optional[Choices] = None,
        *,
        html: bool = False,
        **opts,
    ) -> bool:
        """Edit a sent message in place. "Not modified" (a re-tap) is not an error."""
        opts = self._opts(choices, html, opts)
        opts.pop("message_thread_id", None)  # an edit addresses the message, not a topic
        with ignore_not_modified():
            await self.bot.edit_message_text(
                text=text, chat_id=self.chat_id, message_id=message_id, **opts
            )
        return True

    async def edit_choices(self, message_id: Any, choices: Optional[Choices]) -> bool:
        """Swap the keyboard under a sent message. A re-tap is not an error."""
        with ignore_not_modified():
            await self.bot.edit_message_reply_markup(
                chat_id=self.chat_id, message_id=message_id, reply_markup=to_markup(choices)
            )
        return True

    async def _send_media(self, kind: str, source, choices, cache_key, upload_action, opts) -> Any:
        opts = self._opts(choices, False, opts)
        if cache_key is not None:

            async def build():
                return await _build(source)

            return await send_cached(
                self.bot,
                kind,
                cache_key,
                build,
                chat_id=self.chat_id,
                upload_action=upload_action,
                **opts,
            )
        if upload_action:
            await self.typing(kind)
        media = await _build(source)
        if kind == "photo":
            return await self.bot.send_photo(chat_id=self.chat_id, photo=media, **opts)
        return await self.bot.send_audio(chat_id=self.chat_id, audio=media, **opts)

    async def send_image(
        self,
        source: MediaSource,
        *,
        caption: Optional[str] = None,
        choices: Optional[Choices] = None,
        cache_key: Optional[str] = None,
        upload_action: bool = True,
        **opts,
    ) -> Any:
        if caption is not None:
            opts["caption"] = caption
        return await self._send_media("photo", source, choices, cache_key, upload_action, opts)

    async def send_audio(
        self,
        source: MediaSource,
        *,
        title: Optional[str] = None,
        performer: Optional[str] = None,
        caption: Optional[str] = None,
        choices: Optional[Choices] = None,
        cache_key: Optional[str] = None,
        upload_action: bool = True,
        **opts,
    ) -> Any:
        for key, value in (("title", title), ("performer", performer), ("caption", caption)):
            if value is not None:
                opts[key] = value
        return await self._send_media("audio", source, choices, cache_key, upload_action, opts)

    async def answer(
        self, callback_id: Optional[str], text: Optional[str] = None, alert: bool = False
    ) -> None:
        """Acknowledge a tap so the client stops spinning. No-op without a tap."""
        if callback_id is None:
            return
        if text is None:
            await self.bot.answer_callback_query(callback_id)
        else:
            await self.bot.answer_callback_query(callback_id, text=text, show_alert=alert)

    async def typing(self, kind: str = "text") -> None:
        await self.bot.send_chat_action(chat_id=self.chat_id, action=_ACTIONS[kind])

    async def send_template(self, name: str, lang: str, params: List[str]) -> Any:
        raise NotImplementedError("Telegram has no message templates; send a session message")
