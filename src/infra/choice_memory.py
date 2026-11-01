"""The numbered menu a chat was last shown, for platforms without buttons.

When a menu has more options than WhatsApp can render as buttons or a list, the
channel sends it as numbered lines and remembers which `Choice.data` each number
stands for; a reply of "3" is then routed as if the third button were tapped.

It answers only while that menu is the *latest* message: every later outgoing
message forgets it, so a number typed into a wizard prompt ("how many ayat a
day?", "which surah?") is that answer, not option 3 of an older menu. The TTL
is the backstop for a menu nobody answers.
"""

from typing import List, Optional

import ujson as json

from infra.redis_client import RedisSingleton

TTL_SECONDS = 15 * 60  # a typed "5" is a surah again once the menu is stale


def _key(chat_id: int) -> str:
    return "choices:" + str(chat_id)


def remember(chat_id: int, data: List[str]) -> None:
    """Number `data` from 1 for `chat_id`, replacing any earlier menu."""
    RedisSingleton().connection.set(_key(chat_id), json.dumps(list(data)), ex=TTL_SECONDS)


def forget(chat_id: int) -> None:
    """Drop the chat's numbered menu (a newer message has superseded it)."""
    RedisSingleton().connection.delete(_key(chat_id))


def pick(chat_id: int, text: str) -> Optional[str]:
    """The `data` behind a numbered reply like "3", or None if `text` is not one."""
    text = (text or "").strip().rstrip(".")
    if not text.isdigit():
        return None
    raw = RedisSingleton().connection.get(_key(chat_id))
    if raw is None:
        return None
    options = json.loads(raw)
    n = int(text)
    return options[n - 1] if 1 <= n <= len(options) else None
