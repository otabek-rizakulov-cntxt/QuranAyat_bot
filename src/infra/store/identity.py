# Who a sender is, across messaging platforms (docs/MULTI_PLATFORM_PLAN.md §5).
#
# Every other table is keyed on one BIGINT `user_id`. A Telegram user's id *is*
# their Telegram id, as it always was — computed, never stored, so a Telegram
# update costs no write here. Every other platform maps its own sender id (a
# WhatsApp wa_id) to a `user_id` drawn from a sequence that starts at 2^52:
# above every Telegram user id (≤52 bits), positive so the `chat_id < 0` ⇒ group
# rule elsewhere never misfires, and below JavaScript's 2^53 safe-integer limit
# for the Mini App's JSON.
#
# The row also carries what WhatsApp's policy needs: when the sender last wrote
# (the free 24-hour service window) and their consent to scheduled pushes.

import abc
from dataclasses import dataclass, replace
from datetime import datetime
from typing import Optional

from channels.base import TELEGRAM

from ._state import MemoryState

NON_TELEGRAM_ID_START = 2**52


@dataclass
class IdentityRow:
    """A row of `identity`."""

    platform: str
    external_id: str
    user_id: int
    created_at: Optional[datetime] = None
    last_inbound_at: Optional[datetime] = None
    opted_in_at: Optional[datetime] = None
    opted_out_at: Optional[datetime] = None

    @property
    def consented(self) -> bool:
        """Opted in to scheduled pushes, and not opted out since."""
        return self.opted_in_at is not None and self.opted_out_at is None


_COLUMNS = "platform, external_id, user_id, created_at, last_inbound_at, opted_in_at, opted_out_at"


def _stored(platform: str) -> None:
    if platform == TELEGRAM:
        raise ValueError("Telegram identity is computed, not stored (until account linking)")


class IdentityStore(abc.ABC):
    """Map a platform's sender id to our `user_id`, and track what its policy needs."""

    async def resolve(self, platform: str, external_id: str) -> int:
        """The `user_id` for this sender, allocating one on first contact.

        Telegram: the id itself, with no I/O. Elsewhere idempotent, and safe under
        concurrency — two first messages racing get the same id.
        """
        if platform == TELEGRAM:
            return int(external_id)
        return await self._resolve(platform, str(external_id))

    async def external_id(self, user_id: int, platform: str) -> Optional[str]:
        """Where to send to reach `user_id` on `platform`, or None if they never wrote."""
        if platform == TELEGRAM:
            return str(user_id) if user_id < NON_TELEGRAM_ID_START else None
        row = await self.get_by_user(user_id, platform)
        return row.external_id if row is not None else None

    @abc.abstractmethod
    async def _resolve(self, platform: str, external_id: str) -> int: ...

    @abc.abstractmethod
    async def get(self, platform: str, external_id: str) -> Optional[IdentityRow]:
        """One identity by sender, or None."""

    @abc.abstractmethod
    async def get_by_user(self, user_id: int, platform: str) -> Optional[IdentityRow]:
        """One identity by our id, or None."""

    @abc.abstractmethod
    async def touch_inbound(self, user_id: int, platform: str, at: datetime) -> None:
        """Record that the user just wrote — this (re)opens the 24-hour window."""

    @abc.abstractmethod
    async def opt_in(self, user_id: int, platform: str, at: datetime) -> None:
        """Record consent to scheduled pushes; clears an earlier opt-out."""

    @abc.abstractmethod
    async def opt_out(self, user_id: int, platform: str, at: datetime) -> None:
        """Record withdrawal of consent ("STOP"); honoured from this moment."""


class InMemoryIdentityStore(IdentityStore):
    """Dict-backed `IdentityStore`, used when DATABASE_URL is unset."""

    def __init__(self, state: MemoryState):
        self._state = state

    def _find(self, user_id, platform):
        for row in self._state.identity.values():
            if row.user_id == user_id and row.platform == platform:
                return row
        return None

    async def _resolve(self, platform, external_id):
        row = self._state.identity.get((platform, external_id))
        if row is None:
            row = IdentityRow(
                platform=platform,
                external_id=external_id,
                user_id=self._state.next_user_id(),
                created_at=datetime.now().astimezone(),
            )
            self._state.identity[(platform, external_id)] = row
        return row.user_id

    async def get(self, platform, external_id):
        row = self._state.identity.get((platform, str(external_id)))
        return replace(row) if row is not None else None

    async def get_by_user(self, user_id, platform):
        row = self._find(user_id, platform)
        return replace(row) if row is not None else None

    def _update(self, user_id, platform, **fields):
        _stored(platform)
        row = self._find(user_id, platform)
        if row is not None:
            for name, value in fields.items():
                setattr(row, name, value)

    async def touch_inbound(self, user_id, platform, at):
        self._update(user_id, platform, last_inbound_at=at)

    async def opt_in(self, user_id, platform, at):
        self._update(user_id, platform, opted_in_at=at, opted_out_at=None)

    async def opt_out(self, user_id, platform, at):
        self._update(user_id, platform, opted_out_at=at)


class PostgresIdentityStore(IdentityStore):
    """asyncpg-backed `IdentityStore`."""

    def __init__(self, pool):
        self._pool = pool

    @staticmethod
    def _row(record) -> Optional[IdentityRow]:
        return IdentityRow(**dict(record)) if record is not None else None

    async def _resolve(self, platform, external_id):
        # ON CONFLICT DO NOTHING returns no row when another request won the race
        # (or the sender is known); the SELECT then reads the winner's id. A burnt
        # sequence value on conflict is harmless — ids are opaque.
        user_id = await self._pool.fetchval(
            "INSERT INTO identity (platform, external_id, user_id) "
            "VALUES ($1, $2, nextval('non_telegram_user_id')) "
            "ON CONFLICT (platform, external_id) DO NOTHING RETURNING user_id",
            platform,
            external_id,
        )
        if user_id is None:
            user_id = await self._pool.fetchval(
                "SELECT user_id FROM identity WHERE platform = $1 AND external_id = $2",
                platform,
                external_id,
            )
        return user_id

    async def get(self, platform, external_id):
        return self._row(
            await self._pool.fetchrow(
                "SELECT " + _COLUMNS + " FROM identity WHERE platform = $1 AND external_id = $2",
                platform,
                str(external_id),
            )
        )

    async def get_by_user(self, user_id, platform):
        return self._row(
            await self._pool.fetchrow(
                "SELECT " + _COLUMNS + " FROM identity WHERE user_id = $1 AND platform = $2",
                user_id,
                platform,
            )
        )

    async def touch_inbound(self, user_id, platform, at):
        _stored(platform)
        await self._pool.execute(
            "UPDATE identity SET last_inbound_at = $3 WHERE user_id = $1 AND platform = $2",
            user_id,
            platform,
            at,
        )

    async def opt_in(self, user_id, platform, at):
        _stored(platform)
        await self._pool.execute(
            "UPDATE identity SET opted_in_at = $3, opted_out_at = NULL "
            "WHERE user_id = $1 AND platform = $2",
            user_id,
            platform,
            at,
        )

    async def opt_out(self, user_id, platform, at):
        _stored(platform)
        await self._pool.execute(
            "UPDATE identity SET opted_out_at = $3 WHERE user_id = $1 AND platform = $2",
            user_id,
            platform,
            at,
        )
