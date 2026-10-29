"""A one-turn "the next message is an answer to my question" flag per chat.

Used by reciter search: after tapping "🔍 Search reciter", the next free text is
a name, not an ayah reference. Short-lived on purpose — it is a live exchange,
not a setting.
"""

from typing import Optional

from config import RedisSingleton

TTL_SECONDS = 120


def _key(chat_id: int) -> str:
    return "awaiting:" + str(chat_id)


def expect(chat_id: int, kind: str) -> None:
    """Expect the next free-text message from `chat_id` to be input for `kind`."""
    RedisSingleton().connection.set(_key(chat_id), kind, ex=TTL_SECONDS)


def take(chat_id: int) -> Optional[str]:
    """Return and clear the pending kind for `chat_id`, or None."""
    redis = RedisSingleton().connection
    kind = redis.get(_key(chat_id))
    if kind is not None:
        redis.delete(_key(chat_id))
    return kind
