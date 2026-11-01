"""The platform-neutral vocabulary every channel speaks.

A handler talks to a `Channel` that is already bound to one conversation, so it
never handles an address: `await ctx.channel.send_text(text, choices)`. Each
platform adapter (channels/telegram.py, later channels/whatsapp.py) turns these
calls into its own API and degrades by its `Caps` — Telegram renders `Choices`
as an inline keyboard, WhatsApp as reply buttons, a list, or numbered text.

Message text is Telegram HTML (docs/MULTI_PLATFORM_PLAN.md §2): pass `html=True`
and a non-HTML channel converts it (channels/whatsapp_format.py).
"""

from dataclasses import dataclass
from typing import Any, Awaitable, Callable, List, Optional, Protocol, Union

TELEGRAM = "telegram"
WHATSAPP = "whatsapp"


@dataclass(frozen=True)
class Choice:
    """One button. Exactly one action: `data`, `url`, `web_app` or `switch_inline`.

    `data` is the same string Telegram carries as callback_data (≤64 bytes), and
    is also what a WhatsApp reply id carries back, so `router.dispatch_callback`
    serves both platforms unchanged.
    """

    label: str
    data: Optional[str] = None  # callback, routed by bot/router.py
    url: Optional[str] = None  # opens a link
    web_app: Optional[str] = None  # opens the Mini App at this URL (Telegram only)
    switch_inline: Optional[str] = None  # share via inline mode (Telegram only)

    def __post_init__(self):
        actions = [self.data, self.url, self.web_app, self.switch_inline]
        if sum(a is not None for a in actions) != 1:
            raise ValueError("a Choice needs exactly one action: %r" % (self,))


# Rows of buttons, top to bottom. A channel that cannot show rows flattens them.
Choices = List[List[Choice]]

# Media is a URL, raw bytes / a file-like object, or a coroutine function that
# builds one — called only when the channel actually has to upload.
MediaSource = Union[str, bytes, Any, Callable[[], Awaitable[Any]]]


@dataclass(frozen=True)
class Caps:
    """What a platform can render; adapters and handlers degrade by it."""

    max_buttons: int  # interactive choices in one message
    list_rows: int  # rows in a list picker (0 = no list picker)
    can_edit: bool  # can rewrite a message already sent
    inline_mode: bool  # "@bot 2:255" in any chat
    web_app: bool  # in-chat Mini App buttons


@dataclass(frozen=True)
class Incoming:
    """One inbound event, normalized from whatever the platform delivered."""

    platform: str
    external_id: str  # the sender on that platform: a Telegram id, a WhatsApp wa_id
    user_id: int  # our id for the sender (infra/store/identity.py)
    chat_id: int  # where replies go; equals user_id outside Telegram groups
    text: Optional[str] = None
    callback_data: Optional[str] = None  # a tapped Choice's `data`
    callback_id: Optional[str] = None  # to acknowledge the tap, where that exists
    message_id: Optional[Any] = None  # the platform's id for the message
    voice_media_id: Optional[str] = None
    raw: Any = None  # the platform's own update object, for adapter-only needs


class Channel(Protocol):
    """A conversation on one platform. Every send goes to the bound chat."""

    platform: str
    caps: Caps

    async def send_text(
        self, text: str, choices: Optional[Choices] = None, *, html: bool = False, **opts
    ) -> Any: ...

    async def edit_text(
        self,
        message_id: Any,
        text: str,
        choices: Optional[Choices] = None,
        *,
        html: bool = False,
        **opts,
    ) -> bool: ...

    async def send_image(
        self,
        source: MediaSource,
        *,
        caption: Optional[str] = None,
        choices: Optional[Choices] = None,
        cache_key: Optional[str] = None,
        **opts,
    ) -> Any: ...

    async def send_audio(
        self,
        source: MediaSource,
        *,
        title: Optional[str] = None,
        performer: Optional[str] = None,
        caption: Optional[str] = None,
        choices: Optional[Choices] = None,
        cache_key: Optional[str] = None,
        **opts,
    ) -> Any: ...

    async def answer(
        self, callback_id: Optional[str], text: Optional[str] = None, alert: bool = False
    ) -> None: ...

    async def typing(self, kind: str = "text") -> None: ...

    async def send_template(self, name: str, lang: str, params: List[str]) -> Any: ...
