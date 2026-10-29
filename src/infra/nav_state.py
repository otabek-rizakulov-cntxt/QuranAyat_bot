"""Where each user stopped reading: (surah, ayah, view)."""

from typing import Optional

import ujson as json

from infra.redis_client import RedisSingleton
from infra.store import get_store  # lazy: infra.store imports lib, which imports this


async def save(chat_id: int, surah: int, ayah: int, view: str) -> None:
    """Remember the reader's position. Durable — it lives in the store
    (`reader_position`); the old two-day Redis key meant a reader who paused for a
    few days restarted at 1:1."""

    store = await get_store()
    await store.profiles.save_reader_position(chat_id, surah, ayah, view)


async def get(chat_id: int) -> Optional[list]:
    """`[surah, ayah, view]` where the user stopped reading, or None.

    Falls back to the legacy Redis key so positions saved before the move to the
    store survive the deploy that introduced it.
    """

    store = await get_store()
    position = await store.profiles.get_reader_position(chat_id)
    if position is not None:
        return list(position)
    legacy = RedisSingleton().connection.get(str(chat_id))
    return json.loads(legacy) if legacy is not None else None
