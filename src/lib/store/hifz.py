# What the user knows by heart, stored as non-overlapping ayah intervals.
#
# Every percentage the bot reports is derived arithmetic over these rows, so the
# one invariant that matters is: for a given (user_id, surah) the stored spans
# never overlap and never touch. Marking 67:1-8 and then 67:5-10 must leave one
# 67:1-10 row, and 67:9-10 straight after 67:1-8 must coalesce too — otherwise a
# count of memorized ayahs would double-count and drift.
#
# The merge/split arithmetic is pure and lives in `_merge_span` / `_split_span`
# so both implementations run exactly the same rules; only the read/write around
# it differs.

import abc
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import List, Optional, Sequence, Tuple

from ._state import MemoryState


@dataclass
class HifzInterval:
  """A contiguous run of ayahs in one surah that the user has marked memorized."""

  id: int
  user_id: int
  surah: int
  start_ayah: int
  end_ayah: int
  marked_at: datetime


_COLUMNS = "id, user_id, surah, start_ayah, end_ayah, marked_at"


def _normalize(start_ayah: int, end_ayah: int) -> Tuple[int, int]:
  """Order the endpoints and reject a nonsensical span."""
  start, end = int(start_ayah), int(end_ayah)
  if start > end:
    start, end = end, start
  if start < 1:
    raise ValueError("ayah numbers start at 1, got %r" % (start_ayah,))
  return start, end


def _touches(span_start: int, span_end: int, start: int, end: int) -> bool:
  """Whether [span_start, span_end] overlaps or is adjacent to [start, end].

  Adjacency counts (`end + 1`, `start - 1`): 1-8 followed by 9-10 is one run of
  ten ayahs, not two runs, and storing it as two rows would be a lie about the
  shape of what the user knows.
  """
  return span_start <= end + 1 and span_end >= start - 1


def _overlaps(span_start: int, span_end: int, start: int, end: int) -> bool:
  """Whether [span_start, span_end] shares at least one ayah with [start, end].

  The strict sibling of `_touches`, and the reason unmarking is not the inverse of
  marking: `/forgot 67:5-6` must leave a neighbouring 67:7-10 completely alone,
  where *marking* 67:5-6 would have absorbed it. Removal that reached one ayah
  further would silently erase hifz the user never said they had forgotten.
  """
  return span_start <= end and span_end >= start


def _covers(span_start: int, span_end: int, start: int, end: int) -> bool:
  """Whether [span_start, span_end] already contains all of [start, end].

  Both legs check this before writing anything, because re-marking ayahs already
  known has to be a true no-op: rewriting the row would hand it a fresh id and a
  fresh `marked_at`, turning "when did you learn this" into "when did you last
  say so". A user re-reading a memorized page should not reset that.
  """
  return span_start <= start and span_end >= end


def _merge_span(spans: Sequence[Tuple[int, int]], start: int,
                end: int) -> Tuple[int, int]:
  """The union of [start, end] with every span it overlaps or touches.

  Precondition: every span in `spans` satisfies `_touches`. The union of a
  contiguous run is just its extremes, so this is min/max rather than a sweep —
  feed it a span that does *not* touch and it will happily swallow the gap.
  """
  low, high = start, end
  for span_start, span_end in spans:
    low = min(low, span_start)
    high = max(high, span_end)
  return low, high


def _split_span(span_start: int, span_end: int, start: int,
                end: int) -> List[Tuple[int, int]]:
  """What is left of [span_start, span_end] after removing [start, end].

  Zero pieces (fully covered), one (trimmed from an end), or two (a hole punched
  in the middle) — the `/forgot 67:5-6` case that splits 67:1-10 in two.
  """
  remainder = []
  if span_start < start:
    remainder.append((span_start, min(span_end, start - 1)))
  if span_end > end:
    remainder.append((max(span_start, end + 1), span_end))
  return remainder


class HifzStore(abc.ABC):
  """The memorized-ayah interval set."""

  @abc.abstractmethod
  async def add_interval(self, user_id: int, surah: int, start_ayah: int,
                         end_ayah: int) -> HifzInterval:
    """Mark [start_ayah, end_ayah] of `surah` memorized, coalescing on insert.

    Returns the single interval the range now belongs to. Overlapping and
    adjacent existing intervals are absorbed into it, so the stored set is always
    minimal and disjoint. Marking a range that is already fully covered is a
    no-op that returns the covering interval unchanged.
    """

  @abc.abstractmethod
  async def remove_range(self, user_id: int, surah: int, start_ayah: int,
                         end_ayah: int) -> List[HifzInterval]:
    """Unmark [start_ayah, end_ayah], splitting intervals as needed.

    Returns the intervals that replaced the ones removed, ascending by start
    ayah (empty when the range was not memorized at all, or was fully erased).
    """

  @abc.abstractmethod
  async def list_intervals(self, user_id: int,
                           surah: Optional[int] = None) -> List[HifzInterval]:
    """Every interval for the user, ascending by (surah, start_ayah).

    Pass `surah` to restrict to one surah — the read `/progress` does per surah.
    """

  @abc.abstractmethod
  async def count_ayahs(self, user_id: int, surah: Optional[int] = None) -> int:
    """How many distinct ayahs the user has marked memorized (optionally in one surah)."""


class InMemoryHifzStore(HifzStore):
  """List-backed `HifzStore`, used when DATABASE_URL is unset."""

  def __init__(self, state: MemoryState):
    self._state = state

  def _rows(self, user_id, surah):
    return [r for r in self._state.hifz_interval
            if r.user_id == user_id and r.surah == surah]

  async def add_interval(self, user_id, surah, start_ayah, end_ayah):
    start, end = _normalize(start_ayah, end_ayah)
    overlapping = [r for r in self._rows(user_id, surah)
                   if _touches(r.start_ayah, r.end_ayah, start, end)]
    if len(overlapping) == 1 and _covers(overlapping[0].start_ayah,
                                         overlapping[0].end_ayah, start, end):
      return replace(overlapping[0])        # already covered; keep the original marked_at
    low, high = _merge_span([(r.start_ayah, r.end_ayah) for r in overlapping], start, end)
    for row in overlapping:
      self._state.hifz_interval.remove(row)
    merged = HifzInterval(self._state.next_id(), user_id, surah, low, high,
                          datetime.now(timezone.utc))
    self._state.hifz_interval.append(merged)
    return replace(merged)

  async def remove_range(self, user_id, surah, start_ayah, end_ayah):
    start, end = _normalize(start_ayah, end_ayah)
    affected = [r for r in self._rows(user_id, surah)
                if _overlaps(r.start_ayah, r.end_ayah, start, end)]
    replacements = []
    for row in affected:
      self._state.hifz_interval.remove(row)
      for piece_start, piece_end in _split_span(row.start_ayah, row.end_ayah, start, end):
        piece = HifzInterval(self._state.next_id(), user_id, surah, piece_start,
                             piece_end, row.marked_at)
        self._state.hifz_interval.append(piece)
        replacements.append(piece)
    replacements.sort(key=lambda r: r.start_ayah)
    return [replace(r) for r in replacements]

  async def list_intervals(self, user_id, surah=None):
    rows = [r for r in self._state.hifz_interval
            if r.user_id == user_id and (surah is None or r.surah == surah)]
    rows.sort(key=lambda r: (r.surah, r.start_ayah))
    return [replace(r) for r in rows]

  async def count_ayahs(self, user_id, surah=None):
    return sum(r.end_ayah - r.start_ayah + 1
               for r in await self.list_intervals(user_id, surah))


class PostgresHifzStore(HifzStore):
  """asyncpg-backed `HifzStore`.

  The read-modify-write in `add_interval` / `remove_range` runs inside an
  explicit transaction that first takes an advisory lock on (user_id, surah), so
  two concurrent marks on the same surah cannot both read the pre-merge state and
  leave overlapping rows behind.

  `SELECT ... FOR UPDATE` alone is **not** enough here and that is worth being
  explicit about, because it looks like it should be. FOR UPDATE locks the rows a
  query found; the dangerous case is the one where it finds none. Two requests
  marking 67:1-8 and 67:5-10 at the same moment on an empty surah each lock
  nothing, each see no neighbour to merge with, and each INSERT — leaving exactly
  the pair of overlapping rows the whole design exists to prevent, with no
  constraint to catch it. Serializing on the *key* rather than on the rows is what
  actually closes it. The lock is per (user, surah), so it costs nothing in
  practice: no two people ever contend, and one person double-tapping "I know this"
  is the only real contender.
  """

  def __init__(self, pool):
    self._pool = pool

  @staticmethod
  def _row(record) -> HifzInterval:
    return HifzInterval(record["id"], record["user_id"], record["surah"],
                        record["start_ayah"], record["end_ayah"], record["marked_at"])

  @staticmethod
  def _lock_key(user_id: int, surah: int) -> int:
    """One bigint identifying (user_id, surah) for `pg_advisory_xact_lock`.

    Postgres offers a two-int4 form, but a Telegram user id does not fit in
    int4 — so the pair is packed into the single-bigint form instead. 115 is one
    past the last surah number, which keeps the mapping injective for every real
    surah and leaves the product far short of a bigint even for the largest id
    Telegram issues.
    """
    return int(user_id) * 115 + int(surah)

  async def _lock_surah(self, conn, user_id: int, surah: int) -> None:
    """Serialize every writer of one user's surah for the rest of the transaction."""
    await conn.execute("SELECT pg_advisory_xact_lock($1::bigint)",
                       self._lock_key(user_id, surah))

  async def add_interval(self, user_id, surah, start_ayah, end_ayah):
    start, end = _normalize(start_ayah, end_ayah)
    async with self._pool.acquire() as conn:
      async with conn.transaction():
        await self._lock_surah(conn, user_id, surah)
        # `start_ayah <= end + 1 AND end_ayah >= start - 1` is `_touches` written
        # as a WHERE clause — the widened bounds are what make an abutting row
        # come back so it can be coalesced.
        overlapping = await conn.fetch(
          "SELECT " + _COLUMNS + " FROM hifz_interval "
          "WHERE user_id = $1 AND surah = $2 AND start_ayah <= $3 AND end_ayah >= $4 "
          "ORDER BY start_ayah FOR UPDATE",
          user_id, surah, end + 1, start - 1)
        if len(overlapping) == 1 and _covers(overlapping[0]["start_ayah"],
                                             overlapping[0]["end_ayah"], start, end):
          return self._row(overlapping[0])
        low, high = _merge_span([(r["start_ayah"], r["end_ayah"]) for r in overlapping],
                                start, end)
        if overlapping:
          await conn.execute("DELETE FROM hifz_interval WHERE id = ANY($1::bigint[])",
                             [r["id"] for r in overlapping])
        return self._row(await conn.fetchrow(
          "INSERT INTO hifz_interval (user_id, surah, start_ayah, end_ayah) "
          "VALUES ($1, $2, $3, $4) RETURNING " + _COLUMNS,
          user_id, surah, low, high))

  async def remove_range(self, user_id, surah, start_ayah, end_ayah):
    start, end = _normalize(start_ayah, end_ayah)
    async with self._pool.acquire() as conn:
      async with conn.transaction():
        await self._lock_surah(conn, user_id, surah)
        # `_overlaps`, not `_touches`: the un-widened bounds are the whole point,
        # so unmarking 67:5-6 cannot reach the row that starts at 67:7.
        affected = await conn.fetch(
          "SELECT " + _COLUMNS + " FROM hifz_interval "
          "WHERE user_id = $1 AND surah = $2 AND start_ayah <= $3 AND end_ayah >= $4 "
          "ORDER BY start_ayah FOR UPDATE",
          user_id, surah, end, start)
        if not affected:
          return []
        await conn.execute("DELETE FROM hifz_interval WHERE id = ANY($1::bigint[])",
                           [r["id"] for r in affected])
        replacements = []
        for record in affected:
          for piece_start, piece_end in _split_span(record["start_ayah"], record["end_ayah"],
                                                    start, end):
            replacements.append(self._row(await conn.fetchrow(
              "INSERT INTO hifz_interval (user_id, surah, start_ayah, end_ayah, marked_at) "
              "VALUES ($1, $2, $3, $4, $5) RETURNING " + _COLUMNS,
              user_id, surah, piece_start, piece_end, record["marked_at"])))
        replacements.sort(key=lambda r: r.start_ayah)
        return replacements

  async def list_intervals(self, user_id, surah=None):
    if surah is None:
      records = await self._pool.fetch(
        "SELECT " + _COLUMNS + " FROM hifz_interval WHERE user_id = $1 "
        "ORDER BY surah, start_ayah", user_id)
    else:
      records = await self._pool.fetch(
        "SELECT " + _COLUMNS + " FROM hifz_interval WHERE user_id = $1 AND surah = $2 "
        "ORDER BY surah, start_ayah", user_id, surah)
    return [self._row(r) for r in records]

  async def count_ayahs(self, user_id, surah=None):
    if surah is None:
      value = await self._pool.fetchval(
        "SELECT COALESCE(SUM(end_ayah - start_ayah + 1), 0) FROM hifz_interval "
        "WHERE user_id = $1", user_id)
    else:
      value = await self._pool.fetchval(
        "SELECT COALESCE(SUM(end_ayah - start_ayah + 1), 0) FROM hifz_interval "
        "WHERE user_id = $1 AND surah = $2", user_id, surah)
    return int(value or 0)
