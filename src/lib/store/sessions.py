# The streak and leaderboard substrate: one row per completed session.
#
# A "session" is a drill run through or a passed recall check — never a command
# invocation — so neither the streak nor the board can be farmed. `local_date` is
# the user's local day, computed by the caller from their stored UTC offset; it
# is what decides which day a session counts for, so a session at 23:59 and one
# at 00:01 local are two days even though they are a minute apart.
#
# Writes are idempotent on (user, local_date, kind, portion): tapping "I know
# this by heart" twice on the same portion logs once.

import abc
from dataclasses import dataclass, replace
from datetime import date, datetime, timezone
from typing import List, Optional

from ._state import MemoryState

KIND_DRILL = "drill"
KIND_RECALL_CHECK = "recall_check"


@dataclass
class SessionRow:
  """A row of `session_log`. The portion columns are None for a session that is
  not tied to a specific range."""

  id: int
  user_id: int
  local_date: date
  kind: str
  surah: Optional[int] = None
  start_ayah: Optional[int] = None
  end_ayah: Optional[int] = None
  occurred_at: Optional[datetime] = None


@dataclass
class LeaderboardEntry:
  """One row of the weekly board, already ordered and ranked."""

  user_id: int
  display_name: Optional[str]
  sessions: int
  current_streak: int
  position: int


_COLUMNS = "id, user_id, local_date, kind, surah, start_ayah, end_ayah, occurred_at"

# Sessions in a date window, joined to opted-in profiles, ordered the one way the
# spec defines: most sessions first, longest streak breaks the tie, user id makes
# it total so a rank is stable between two reads.
_BOARD_CTE = (
  "WITH board AS ("
  "  SELECT s.user_id AS user_id, COUNT(*)::int AS sessions,"
  "         p.display_name AS display_name, p.current_streak AS current_streak"
  "    FROM session_log s"
  "    JOIN user_profile p ON p.telegram_user_id = s.user_id"
  "   WHERE s.local_date >= $1 AND s.local_date <= $2 AND p.leaderboard_opt_in"
  "   GROUP BY s.user_id, p.display_name, p.current_streak"
  "), ranked AS ("
  "  SELECT user_id, display_name, sessions, current_streak,"
  "         ROW_NUMBER() OVER (ORDER BY sessions DESC, current_streak DESC, user_id ASC)"
  "           ::int AS position"
  "    FROM board"
  ") ")


class SessionStore(abc.ABC):
  """Completed sessions — the only thing a streak or a board is ever computed from."""

  @abc.abstractmethod
  async def log_session(self, user_id: int, local_date: date, kind: str,
                        surah: Optional[int] = None, start_ayah: Optional[int] = None,
                        end_ayah: Optional[int] = None) -> Optional[SessionRow]:
    """Record one completed session, idempotently.

    Returns the inserted row, or None if an identical session (same user, local
    date, kind and portion) was already logged.
    """

  @abc.abstractmethod
  async def list_sessions(self, user_id: int, start: Optional[date] = None,
                          end: Optional[date] = None) -> List[SessionRow]:
    """The user's sessions in an inclusive local-date window, ascending."""

  @abc.abstractmethod
  async def list_active_dates(self, user_id: int, since: Optional[date] = None,
                              until: Optional[date] = None) -> List[date]:
    """Distinct local dates on which the user completed at least one session, ascending.

    The streak computation and the 12-week activity grid both read exactly this.
    """

  @abc.abstractmethod
  async def count_sessions(self, user_id: int, start: date, end: date) -> int:
    """How many sessions the user completed in the inclusive local-date window."""

  @abc.abstractmethod
  async def weekly_leaderboard(self, week_start: date, week_end: date,
                               limit: int = 10) -> List[LeaderboardEntry]:
    """The top `limit` opted-in users for the inclusive local-date window.

    Opted-out users are absent from the result, not merely hidden in rendering.
    """

  @abc.abstractmethod
  async def weekly_rank(self, user_id: int, week_start: date,
                        week_end: date) -> Optional[LeaderboardEntry]:
    """The user's own row and 1-based position on that board, or None if unranked.

    Unranked means opted out, or no sessions in the window. Lets `/leaderboard`
    always show "you", even at position 400.
    """


class InMemorySessionStore(SessionStore):
  """List-backed `SessionStore`, used when DATABASE_URL is unset."""

  def __init__(self, state: MemoryState):
    self._state = state

  @staticmethod
  def _key(row):
    return (row.user_id, row.local_date, row.kind, row.surah, row.start_ayah, row.end_ayah)

  async def log_session(self, user_id, local_date, kind, surah=None, start_ayah=None,
                        end_ayah=None):
    row = SessionRow(0, user_id, local_date, kind, surah, start_ayah, end_ayah)
    if any(self._key(existing) == self._key(row) for existing in self._state.session_log):
      return None
    row.id = self._state.next_id()
    row.occurred_at = datetime.now(timezone.utc)
    self._state.session_log.append(row)
    return replace(row)

  async def list_sessions(self, user_id, start=None, end=None):
    rows = [r for r in self._state.session_log
            if r.user_id == user_id
            and (start is None or r.local_date >= start)
            and (end is None or r.local_date <= end)]
    rows.sort(key=lambda r: (r.local_date, r.id))
    return [replace(r) for r in rows]

  async def list_active_dates(self, user_id, since=None, until=None):
    return sorted({r.local_date for r in await self.list_sessions(user_id, since, until)})

  async def count_sessions(self, user_id, start, end):
    return len(await self.list_sessions(user_id, start, end))

  def _board(self, week_start, week_end):
    profiles = self._state.user_profile
    tally = {}
    for row in self._state.session_log:
      profile = profiles.get(row.user_id)
      if profile is None or not profile.leaderboard_opt_in:
        continue
      if row.local_date < week_start or row.local_date > week_end:
        continue
      tally[row.user_id] = tally.get(row.user_id, 0) + 1
    entries = [
      LeaderboardEntry(user_id, profiles[user_id].display_name, sessions,
                       profiles[user_id].current_streak, 0)
      for user_id, sessions in tally.items()
    ]
    entries.sort(key=lambda e: (-e.sessions, -e.current_streak, e.user_id))
    for position, entry in enumerate(entries, start=1):
      entry.position = position
    return entries

  async def weekly_leaderboard(self, week_start, week_end, limit=10):
    return self._board(week_start, week_end)[:limit]

  async def weekly_rank(self, user_id, week_start, week_end):
    for entry in self._board(week_start, week_end):
      if entry.user_id == user_id:
        return entry
    return None


class PostgresSessionStore(SessionStore):
  """asyncpg-backed `SessionStore`."""

  def __init__(self, pool):
    self._pool = pool

  @staticmethod
  def _row(record) -> Optional[SessionRow]:
    if record is None:
      return None
    return SessionRow(record["id"], record["user_id"], record["local_date"],
                      record["kind"], record["surah"], record["start_ayah"],
                      record["end_ayah"], record["occurred_at"])

  @staticmethod
  def _entry(record) -> LeaderboardEntry:
    return LeaderboardEntry(record["user_id"], record["display_name"],
                            record["sessions"], record["current_streak"],
                            record["position"])

  async def log_session(self, user_id, local_date, kind, surah=None, start_ayah=None,
                        end_ayah=None):
    # No conflict target: the dedupe index is an expression index over COALESCEd
    # portion columns (NULLs are distinct otherwise), and a bare DO NOTHING covers
    # it without repeating the expression here.
    return self._row(await self._pool.fetchrow(
      "INSERT INTO session_log (user_id, local_date, kind, surah, start_ayah, end_ayah) "
      "VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT DO NOTHING RETURNING " + _COLUMNS,
      user_id, local_date, kind, surah, start_ayah, end_ayah))

  async def list_sessions(self, user_id, start=None, end=None):
    records = await self._pool.fetch(
      "SELECT " + _COLUMNS + " FROM session_log WHERE user_id = $1 "
      "AND ($2::date IS NULL OR local_date >= $2) "
      "AND ($3::date IS NULL OR local_date <= $3) "
      "ORDER BY local_date, id", user_id, start, end)
    return [self._row(r) for r in records]

  async def list_active_dates(self, user_id, since=None, until=None):
    records = await self._pool.fetch(
      "SELECT DISTINCT local_date FROM session_log WHERE user_id = $1 "
      "AND ($2::date IS NULL OR local_date >= $2) "
      "AND ($3::date IS NULL OR local_date <= $3) "
      "ORDER BY local_date", user_id, since, until)
    return [r["local_date"] for r in records]

  async def count_sessions(self, user_id, start, end):
    value = await self._pool.fetchval(
      "SELECT COUNT(*) FROM session_log WHERE user_id = $1 "
      "AND local_date >= $2 AND local_date <= $3", user_id, start, end)
    return int(value or 0)

  async def weekly_leaderboard(self, week_start, week_end, limit=10):
    records = await self._pool.fetch(
      _BOARD_CTE + "SELECT user_id, display_name, sessions, current_streak, position "
      "FROM ranked ORDER BY position LIMIT $3", week_start, week_end, limit)
    return [self._entry(r) for r in records]

  async def weekly_rank(self, user_id, week_start, week_end):
    record = await self._pool.fetchrow(
      _BOARD_CTE + "SELECT user_id, display_name, sessions, current_streak, position "
      "FROM ranked WHERE user_id = $3", week_start, week_end, user_id)
    return self._entry(record) if record is not None else None
