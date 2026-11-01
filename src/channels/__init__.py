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


def for_platform(platform: str, *, bot, external_id, thread_id: Optional[int] = None) -> Channel:
    """The channel for one conversation, from where a send is addressed.

    The scheduler holds `(platform, external id, topic)` on each queued row and
    builds the channel through this, so a send handler never branches on platform.
    """
    if platform == TELEGRAM:
        from channels.telegram import TelegramChannel

        return TelegramChannel(bot, int(external_id), thread_id)
    raise ValueError("no channel for platform %r" % platform)
