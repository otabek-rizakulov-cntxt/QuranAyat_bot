# Verse-of-the-day subscriptions (docs/MULTI_PLATFORM_PLAN.md P2.5).
#
# One row per user: on which platform they read it, at what local time, and
# whether it is on. The time zone is the profile's (`user_profile.timezone`), so
# it is shared with hifz reminders rather than asked for twice. Turning it off
# keeps the row, so turning it back on remembers the time.

import abc
from dataclasses import dataclass, replace
from datetime import datetime, time
from typing import Optional

from ._state import MemoryState


@dataclass
class DailySubRow:
    """A row of `daily_ayah_sub`."""

    user_id: int
    platform: str
    send_time: time
    enabled: bool = True
    created_at: Optional[datetime] = None


_COLUMNS = "user_id, platform, send_time, enabled, created_at"


class DailyStore(abc.ABC):
    @abc.abstractmethod
    async def get(self, user_id: int) -> Optional[DailySubRow]:
        """The user's subscription, on or off, or None if they never had one."""

    @abc.abstractmethod
    async def upsert(
        self, user_id: int, platform: str, send_time: time, enabled: bool = True
    ) -> DailySubRow:
        """Create or replace the subscription's platform, time and state."""

    @abc.abstractmethod
    async def set_enabled(self, user_id: int, enabled: bool) -> Optional[DailySubRow]:
        """Turn an existing subscription on or off; None if there is none."""


class InMemoryDailyStore(DailyStore):
    def __init__(self, state: MemoryState):
        self._state = state

    async def get(self, user_id):
        row = self._state.daily_ayah_sub.get(user_id)
        return replace(row) if row is not None else None

    async def upsert(self, user_id, platform, send_time, enabled=True):
        existing = self._state.daily_ayah_sub.get(user_id)
        row = DailySubRow(
            user_id=user_id,
            platform=platform,
            send_time=send_time,
            enabled=enabled,
            created_at=existing.created_at if existing else datetime.now().astimezone(),
        )
        self._state.daily_ayah_sub[user_id] = row
        return replace(row)

    async def set_enabled(self, user_id, enabled):
        row = self._state.daily_ayah_sub.get(user_id)
        if row is None:
            return None
        row.enabled = enabled
        return replace(row)


class PostgresDailyStore(DailyStore):
    def __init__(self, pool):
        self._pool = pool

    @staticmethod
    def _row(record) -> Optional[DailySubRow]:
        return DailySubRow(**dict(record)) if record is not None else None

    async def get(self, user_id):
        return self._row(
            await self._pool.fetchrow(
                "SELECT " + _COLUMNS + " FROM daily_ayah_sub WHERE user_id = $1", user_id
            )
        )

    async def upsert(self, user_id, platform, send_time, enabled=True):
        return self._row(
            await self._pool.fetchrow(
                "INSERT INTO daily_ayah_sub (user_id, platform, send_time, enabled) "
                "VALUES ($1, $2, $3, $4) ON CONFLICT (user_id) DO UPDATE SET "
                "platform = EXCLUDED.platform, send_time = EXCLUDED.send_time, "
                "enabled = EXCLUDED.enabled, updated_at = now() RETURNING " + _COLUMNS,
                user_id,
                platform,
                send_time,
                enabled,
            )
        )

    async def set_enabled(self, user_id, enabled):
        return self._row(
            await self._pool.fetchrow(
                "UPDATE daily_ayah_sub SET enabled = $2, updated_at = now() "
                "WHERE user_id = $1 RETURNING " + _COLUMNS,
                user_id,
                enabled,
            )
        )
