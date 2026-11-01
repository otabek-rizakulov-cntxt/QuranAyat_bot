"""Messaging platforms behind one interface (docs/MULTI_PLATFORM_PLAN.md §3).

Business logic sends through a `Channel` bound to one conversation; each module
here adapts that to one platform's API.
"""

from typing import Optional

from channels.base import TELEGRAM, WHATSAPP, Caps, Channel, Choice, Choices, Incoming

__all__ = [
    "TELEGRAM",
    "WHATSAPP",
    "Caps",
    "Channel",
    "Choice",
    "Choices",
    "Incoming",
    "for_platform",
]


def for_platform(
    platform: str,
    *,
    external_id,
    bot=None,
    thread_id: Optional[int] = None,
    chat_id: Optional[int] = None,
    client=None,
) -> Channel:
    """The channel for one conversation, from where a send is addressed.

    The scheduler holds `(platform, external id, topic)` on each queued row and
    builds the channel through this, so a send handler never branches on platform.
    Telegram needs the `bot`; WhatsApp needs the Graph `client` and our `chat_id`
    (the user id) for the sender's `external_id` (their wa_id).
    """
    if platform == TELEGRAM:
        from channels.telegram import TelegramChannel

        return TelegramChannel(bot, int(external_id), thread_id)
    if platform == WHATSAPP:
        from channels.whatsapp import WhatsAppChannel

        if client is None or chat_id is None:
            raise ValueError("a WhatsApp channel needs the Graph client and a chat_id")
        return WhatsAppChannel(client, str(external_id), chat_id)
    raise ValueError("no channel for platform %r" % platform)
