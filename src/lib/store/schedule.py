# The due-queue the in-process scheduler drains.
#
# The app only wakes on webhooks, so anything timed has to be a row in a table
# that a background loop polls. `idempotency_key` — conventionally
# "(kind, target, local_date)" — is the whole safety story: a restart, a double
# boot or a retry all try to insert the same key and only one row survives, so a
# user can never be pushed the same portion twice.
#
# States: pending -> claimed -> sent | failed. A claim that crashes leaves a row
# stuck in 'claimed'; `release_stale_claims` is how boot recovers it, and
# `drop_stale` is how a window missed overnight gets dropped rather than
# delivered at 3 a.m.

import abc
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence

import ujson as json

from ._state import MemoryState

STATE_PENDING = "pending"
STATE_CLAIMED = "claimed"
STATE_SENT = "sent"
STATE_FAILED = "failed"


@dataclass
class ScheduledSend:
  """A row of `scheduled_send`. `payload` is always a dict on the way in and out;
  the JSONB encoding never leaks past this module."""

  id: int
  kind: str
  target_chat_id: int
  due_at: datetime
  idempotency_key: str
  payload: Dict[str, Any] = field(default_factory=dict)
  thread_id: Optional[int] = None
  state: str = STATE_PENDING
  claimed_at: Optional[datetime] = None


_COLUMNS = ("id, kind, target_chat_id, thread_id, due_at, payload, state, "
            "idempotency_key, claimed_at")


class ScheduleStore(abc.ABC):
  """The due-queue: enqueue, claim, resolve."""

  @abc.abstractmethod
  async def enqueue(self, kind: str, target_chat_id: int, due_at: datetime,
                    idempotency_key: str, payload: Optional[Dict[str, Any]] = None,
                    thread_id: Optional[int] = None) -> Optional[ScheduledSend]:
    """Queue one send. Returns the row, or None if `idempotency_key` already exists.

    Enqueuing the same key twice inserts one row and raises nothing.
    """

  @abc.abstractmethod
  async def get(self, send_id: int) -> Optional[ScheduledSend]:
    """One queued send by id, or None."""

  @abc.abstractmethod
  async def get_by_key(self, idempotency_key: str) -> Optional[ScheduledSend]:
    """One queued send by its idempotency key, or None."""

  @abc.abstractmethod
  async def claim_due(self, now: datetime, limit: int = 20) -> List[ScheduledSend]:
    """Atomically claim up to `limit` pending rows due at or before `now`.

    Oldest due first. Claimed rows are returned to exactly one caller — the SQL
    implementation uses `FOR UPDATE SKIP LOCKED`, so a second instance polling
    the same queue would be correct, just unnecessary.
    """

  @abc.abstractmethod
  async def mark_sent(self, send_id: int) -> Optional[ScheduledSend]:
    """Move a row to 'sent'. Returns the row, or None if it does not exist."""

  @abc.abstractmethod
  async def mark_failed(self, send_id: int) -> Optional[ScheduledSend]:
    """Move a row to 'failed' so the loop never retries it blindly."""

  @abc.abstractmethod
  async def release_stale_claims(self, claimed_before: datetime) -> int:
    """Return rows claimed before `claimed_before` to 'pending'; count released.

    Boot recovery: a crash between claim and send would otherwise strand them.
    """

  @abc.abstractmethod
  async def drop_stale(self, due_before: datetime,
                       states: Sequence[str] = (STATE_PENDING, STATE_CLAIMED)) -> int:
    """Delete rows in `states` that came due before `due_before`; count deleted.

    A reminder is only worth delivering while it is still same-day-relevant.
    """


class InMemoryScheduleStore(ScheduleStore):
  """Dict-backed `ScheduleStore`, used when DATABASE_URL is unset."""

  def __init__(self, state: MemoryState):
    self._state = state

  @staticmethod
  def _copy(row):
    return replace(row, payload=dict(row.payload))

  async def enqueue(self, kind, target_chat_id, due_at, idempotency_key, payload=None,
                    thread_id=None):
    if any(r.idempotency_key == idempotency_key
           for r in self._state.scheduled_send.values()):
      return None
    row = ScheduledSend(id=self._state.next_id(), kind=kind,
                        target_chat_id=target_chat_id, due_at=due_at,
                        idempotency_key=idempotency_key, payload=dict(payload or {}),
                        thread_id=thread_id, state=STATE_PENDING)
    self._state.scheduled_send[row.id] = row
    return self._copy(row)

  async def get(self, send_id):
    row = self._state.scheduled_send.get(send_id)
    return self._copy(row) if row is not None else None

  async def get_by_key(self, idempotency_key):
    for row in self._state.scheduled_send.values():
      if row.idempotency_key == idempotency_key:
        return self._copy(row)
    return None

  async def claim_due(self, now, limit=20):
    due = [r for r in self._state.scheduled_send.values()
           if r.state == STATE_PENDING and r.due_at <= now]
    due.sort(key=lambda r: (r.due_at, r.id))
    claimed = []
    for row in due[:limit]:
      row.state = STATE_CLAIMED
      row.claimed_at = datetime.now(timezone.utc)
      claimed.append(self._copy(row))
    return claimed

  def _resolve(self, send_id, state):
    row = self._state.scheduled_send.get(send_id)
    if row is None:
      return None
    row.state = state
    return self._copy(row)

  async def mark_sent(self, send_id):
    return self._resolve(send_id, STATE_SENT)

  async def mark_failed(self, send_id):
    return self._resolve(send_id, STATE_FAILED)

  async def release_stale_claims(self, claimed_before):
    released = 0
    for row in self._state.scheduled_send.values():
      if row.state == STATE_CLAIMED and row.claimed_at is not None \
         and row.claimed_at < claimed_before:
        row.state = STATE_PENDING
        row.claimed_at = None
        released += 1
    return released

  async def drop_stale(self, due_before, states=(STATE_PENDING, STATE_CLAIMED)):
    doomed = [r.id for r in self._state.scheduled_send.values()
              if r.state in tuple(states) and r.due_at < due_before]
    for send_id in doomed:
      del self._state.scheduled_send[send_id]
    return len(doomed)


class PostgresScheduleStore(ScheduleStore):
  """asyncpg-backed `ScheduleStore`."""

  def __init__(self, pool):
    self._pool = pool

  @staticmethod
  def _row(record) -> Optional[ScheduledSend]:
    if record is None:
      return None
    payload = record["payload"]
    return ScheduledSend(
      id=record["id"], kind=record["kind"], target_chat_id=record["target_chat_id"],
      due_at=record["due_at"], idempotency_key=record["idempotency_key"],
      payload=json.loads(payload) if isinstance(payload, str) else (payload or {}),
      thread_id=record["thread_id"], state=record["state"],
      claimed_at=record["claimed_at"])

  async def enqueue(self, kind, target_chat_id, due_at, idempotency_key, payload=None,
                    thread_id=None):
    return self._row(await self._pool.fetchrow(
      "INSERT INTO scheduled_send (kind, target_chat_id, thread_id, due_at, payload, "
      "idempotency_key) VALUES ($1, $2, $3, $4, $5::jsonb, $6) "
      "ON CONFLICT (idempotency_key) DO NOTHING RETURNING " + _COLUMNS,
      kind, target_chat_id, thread_id, due_at, json.dumps(dict(payload or {})),
      idempotency_key))

  async def get(self, send_id):
    return self._row(await self._pool.fetchrow(
      "SELECT " + _COLUMNS + " FROM scheduled_send WHERE id = $1", send_id))

  async def get_by_key(self, idempotency_key):
    return self._row(await self._pool.fetchrow(
      "SELECT " + _COLUMNS + " FROM scheduled_send WHERE idempotency_key = $1",
      idempotency_key))

  async def claim_due(self, now, limit=20):
    # The CTE is atomic on its own, but the explicit transaction is what makes
    # the row locks the SKIP LOCKED clause takes actually span the update.
    async with self._pool.acquire() as conn:
      async with conn.transaction():
        records = await conn.fetch(
          "WITH due AS ("
          "  SELECT id FROM scheduled_send WHERE state = $2 AND due_at <= $1"
          "   ORDER BY due_at, id LIMIT $3 FOR UPDATE SKIP LOCKED"
          ") UPDATE scheduled_send s SET state = $4, claimed_at = now(), "
          "updated_at = now() FROM due WHERE s.id = due.id "
          "RETURNING s.id, s.kind, s.target_chat_id, s.thread_id, s.due_at, s.payload, "
          "s.state, s.idempotency_key, s.claimed_at",
          now, STATE_PENDING, limit, STATE_CLAIMED)
        rows = [self._row(r) for r in records]
        rows.sort(key=lambda r: (r.due_at, r.id))
        return rows

  async def _resolve(self, send_id, state):
    return self._row(await self._pool.fetchrow(
      "UPDATE scheduled_send SET state = $2, updated_at = now() WHERE id = $1 "
      "RETURNING " + _COLUMNS, send_id, state))

  async def mark_sent(self, send_id):
    return await self._resolve(send_id, STATE_SENT)

  async def mark_failed(self, send_id):
    return await self._resolve(send_id, STATE_FAILED)

  async def release_stale_claims(self, claimed_before):
    records = await self._pool.fetch(
      "UPDATE scheduled_send SET state = $2, claimed_at = NULL, updated_at = now() "
      "WHERE state = $3 AND claimed_at < $1 RETURNING id",
      claimed_before, STATE_PENDING, STATE_CLAIMED)
    return len(records)

  async def drop_stale(self, due_before, states=(STATE_PENDING, STATE_CLAIMED)):
    records = await self._pool.fetch(
      "DELETE FROM scheduled_send WHERE due_at < $1 AND state = ANY($2::text[]) "
      "RETURNING id", due_before, list(states))
    return len(records)
