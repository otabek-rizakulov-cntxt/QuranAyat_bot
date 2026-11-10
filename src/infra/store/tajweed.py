# Tajweed lesson approvals (docs/TAJWEED_PLAN.md §6).
#
# One row per lesson: who approved it, when, and the content hash of the text they
# read. A lesson is published only while that hash equals the lesson's current hash
# (domain.tajweed_lessons), so editing the text after approval quietly turns the
# lesson back into a draft until a reviewer looks at it again.
#
# Progress: the lessons each user has marked done (✅ Oʻqidim), in either track.
# Practice: per user and lesson, how many quiz/drill sessions and the best score.

import abc
from dataclasses import dataclass, replace
from datetime import datetime
from typing import Dict, Optional, Set, Tuple

from ._state import MemoryState


@dataclass
class ApprovalRow:
    """A row of `tajweed_approval`."""

    lesson_id: str
    content_hash: str
    approved_by: int
    approved_at: Optional[datetime] = None


_COLUMNS = "lesson_id, content_hash, approved_by, approved_at"


class TajweedStore(abc.ABC):
    @abc.abstractmethod
    async def approvals(self) -> Dict[str, ApprovalRow]:
        """Every approval, by lesson id."""

    @abc.abstractmethod
    async def approve(self, lesson_id: str, content_hash: str, approved_by: int) -> ApprovalRow:
        """Record (or replace) the approval of this exact lesson text."""

    @abc.abstractmethod
    async def revoke(self, lesson_id: str) -> bool:
        """Back to draft. True if there was an approval to remove."""

    @abc.abstractmethod
    async def done(self, user_id: int) -> Set[str]:
        """The lesson ids this user has marked done."""

    @abc.abstractmethod
    async def mark_done(self, user_id: int, lesson_id: str) -> bool:
        """Mark a lesson done. True if it was not done before."""

    @abc.abstractmethod
    async def practice(self, user_id: int) -> Dict[str, Tuple[int, int]]:
        """lesson_id -> (sessions, best_pct) for this user."""

    @abc.abstractmethod
    async def record_practice(self, user_id: int, lesson_id: str, pct: int) -> Tuple[int, int]:
        """Count one session and keep the best score; returns (sessions, best_pct)."""


class InMemoryTajweedStore(TajweedStore):
    def __init__(self, state: MemoryState):
        self._state = state

    async def approvals(self):
        return {k: replace(v) for k, v in self._state.tajweed_approval.items()}

    async def approve(self, lesson_id, content_hash, approved_by):
        row = ApprovalRow(lesson_id, content_hash, approved_by, datetime.now().astimezone())
        self._state.tajweed_approval[lesson_id] = row
        return replace(row)

    async def revoke(self, lesson_id):
        return self._state.tajweed_approval.pop(lesson_id, None) is not None

    async def done(self, user_id):
        return set(self._state.tajweed_progress.get(user_id, ()))

    async def mark_done(self, user_id, lesson_id):
        mine = self._state.tajweed_progress.setdefault(user_id, set())
        if lesson_id in mine:
            return False
        mine.add(lesson_id)
        return True

    async def practice(self, user_id):
        return {k[1]: v for k, v in self._state.tajweed_practice.items() if k[0] == user_id}

    async def record_practice(self, user_id, lesson_id, pct):
        sessions, best = self._state.tajweed_practice.get((user_id, lesson_id), (0, 0))
        row = (sessions + 1, max(best, pct))
        self._state.tajweed_practice[(user_id, lesson_id)] = row
        return row


class PostgresTajweedStore(TajweedStore):
    def __init__(self, pool):
        self._pool = pool

    async def approvals(self):
        rows = await self._pool.fetch("SELECT " + _COLUMNS + " FROM tajweed_approval")
        return {r["lesson_id"]: ApprovalRow(**dict(r)) for r in rows}

    async def approve(self, lesson_id, content_hash, approved_by):
        record = await self._pool.fetchrow(
            "INSERT INTO tajweed_approval (lesson_id, content_hash, approved_by) "
            "VALUES ($1, $2, $3) ON CONFLICT (lesson_id) DO UPDATE SET "
            "content_hash = EXCLUDED.content_hash, approved_by = EXCLUDED.approved_by, "
            "approved_at = now() RETURNING " + _COLUMNS,
            lesson_id,
            content_hash,
            approved_by,
        )
        return ApprovalRow(**dict(record))

    async def revoke(self, lesson_id):
        status = await self._pool.execute(
            "DELETE FROM tajweed_approval WHERE lesson_id = $1", lesson_id
        )
        return status.endswith(" 1")

    async def done(self, user_id):
        rows = await self._pool.fetch(
            "SELECT lesson_id FROM tajweed_progress WHERE user_id = $1", user_id
        )
        return {r["lesson_id"] for r in rows}

    async def mark_done(self, user_id, lesson_id):
        status = await self._pool.execute(
            "INSERT INTO tajweed_progress (user_id, lesson_id) VALUES ($1, $2) "
            "ON CONFLICT (user_id, lesson_id) DO NOTHING",
            user_id,
            lesson_id,
        )
        return status.endswith(" 1")

    async def practice(self, user_id):
        rows = await self._pool.fetch(
            "SELECT lesson_id, sessions, best_pct FROM tajweed_practice WHERE user_id = $1",
            user_id,
        )
        return {r["lesson_id"]: (r["sessions"], r["best_pct"]) for r in rows}

    async def record_practice(self, user_id, lesson_id, pct):
        row = await self._pool.fetchrow(
            "INSERT INTO tajweed_practice (user_id, lesson_id, sessions, best_pct) "
            "VALUES ($1, $2, 1, $3) ON CONFLICT (user_id, lesson_id) DO UPDATE SET "
            "sessions = tajweed_practice.sessions + 1, "
            "best_pct = GREATEST(tajweed_practice.best_pct, EXCLUDED.best_pct), "
            "last_at = now() RETURNING sessions, best_pct",
            user_id,
            lesson_id,
            pct,
        )
        return row["sessions"], row["best_pct"]
