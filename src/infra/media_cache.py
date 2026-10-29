"""The Telegram file_id cache: once Telegram has a file, send its id, not the bytes."""

from typing import Optional

from config import RedisSingleton

# Telegram file_ids are stable far longer; two days bounds how long a stale one
# can linger before it is simply re-uploaded.
TTL_SECONDS = 60 * 60 * 24 * 2


def _key(name: str) -> str:
    return "file:" + name


def get(name: str) -> Optional[str]:
    """The cached file_id for `name` (a URL or a key like "page:255"), or None."""
    return RedisSingleton().connection.get(_key(name))


def save(name: str, file_id: str) -> None:
    """Cache `file_id` under `name`. An empty id is ignored."""
    if file_id:
        RedisSingleton().connection.set(_key(name), file_id, ex=TTL_SECONDS)
