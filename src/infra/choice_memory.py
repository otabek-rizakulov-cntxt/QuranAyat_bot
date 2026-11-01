"""The numbered menu a chat was last shown, for platforms without buttons.

When a menu has more options than WhatsApp can render as buttons or a list, the
channel sends it as numbered lines and remembers which `Choice.data` each number
stands for; a reply of "3" is then routed as if the third button were tapped.
Short-lived like `pending_input`: it answers the menu just sent, nothing older.
"""

from typing import List, Optional

import ujson as json

from infra.redis_client import RedisSingleton

TTL_SECONDS = 60 * 60


def _key(chat_id: int) -> str:
    return "choices:" + str(chat_id)


def remember(chat_id: int, data: List[str]) -> None:
    """Number `data` from 1 for `chat_id`, replacing any earlier menu."""
    RedisSingleton().connection.set(_key(chat_id), json.dumps(list(data)), ex=TTL_SECONDS)


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
