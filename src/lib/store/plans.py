# Memorization plans and the daily portions they are materialized into.
#
# A plan is written once, whole: the wizard shows the user a preview calendar and
# then saves the plan row together with every `plan_day` it generated, in one
# transaction, so a preview can never disagree with what is later pushed.
#
# `plan_day.state` is a one-way ratchet: pending -> sent -> completed. Both the
# claim and the completion are conditional writes, which is what makes a double
# tap on "I know this by heart" (or a double delivery after a restart) harmless.

import abc
from dataclasses import dataclass, field, replace
from datetime import date, datetime, timezone
from typing import List, Optional, Sequence

from ._state import MemoryState

PLAN_ACTIVE = "active"
PLAN_PAUSED = "paused"
PLAN_COMPLETE = "complete"

DAY_PENDING = "pending"
DAY_SENT = "sent"
DAY_COMPLETED = "completed"


@dataclass
class PlanDaySpec:
  """One row of the preview calendar, before it has an id."""

  scheduled_date: date
  surah: int
  start_ayah: int
  end_ayah: int


@dataclass
class PlanRow:
  """A row of `plan`. `days_of_week` is 1=Mon … 7=Sun."""

  id: int
  user_id: int
  target_kind: str
  start_surah: int
  start_ayah: int
  end_surah: int
  end_ayah: int
  pace: int
  days_of_week: List[int] = field(default_factory=list)
  status: str = PLAN_ACTIVE
  created_at: Optional[datetime] = None


@dataclass
class PlanDayRow:
  """A row of `plan_day` — one day's portion, local to the user."""

  id: int
  plan_id: int
  scheduled_date: date
  surah: int
  start_ayah: int
  end_ayah: int
  state: str = DAY_PENDING


_PLAN_COLUMNS = ("id, user_id, target_kind, start_surah, start_ayah, end_surah, end_ayah, "
                 "pace, days_of_week, status, created_at")
_DAY_COLUMNS = "id, plan_id, scheduled_date, surah, start_ayah, end_ayah, state"


class PlanStore(abc.ABC):
  """Plans and their materialized daily portions."""

  @abc.abstractmethod
  async def create_plan(self, user_id: int, target_kind: str, start_surah: int,
                        start_ayah: int, end_surah: int, end_ayah: int, pace: int,
                        days_of_week: Sequence[int], days: Sequence[PlanDaySpec],
                        status: str = PLAN_ACTIVE) -> PlanRow:
    """Write the plan and all of its `plan_day` rows atomically.

    `days` is the preview calendar the user just approved, in order. Callers are
    responsible for the one-active-plan-per-user rule (pause or complete the old
    plan first) — the store does not silently retire anything.
    """

  @abc.abstractmethod
  async def get_plan(self, plan_id: int) -> Optional[PlanRow]:
    """One plan by id, or None."""

  @abc.abstractmethod
  async def get_active_plan(self, user_id: int) -> Optional[PlanRow]:
    """The user's active plan, or None. Newest first if more than one somehow exists."""

  @abc.abstractmethod
  async def list_plans(self, user_id: int,
                       status: Optional[str] = None) -> List[PlanRow]:
    """Every plan of the user, newest first, optionally filtered by status."""

  @abc.abstractmethod
  async def set_plan_status(self, plan_id: int, status: str) -> Optional[PlanRow]:
    """Move a plan to 'active' / 'paused' / 'complete'. Returns the row, or None if absent."""

  @abc.abstractmethod
  async def list_plan_days(self, plan_id: int, state: Optional[str] = None,
                           on_or_before: Optional[date] = None) -> List[PlanDayRow]:
    """The plan's days ascending by (scheduled_date, id), optionally filtered.

    `on_or_before` is how the scheduler asks "what is due by this local date".
    """

  @abc.abstractmethod
  async def get_plan_day(self, plan_day_id: int) -> Optional[PlanDayRow]:
    """One plan day by id, or None."""

  @abc.abstractmethod
  async def claim_plan_day(self, plan_day_id: int) -> Optional[PlanDayRow]:
    """Move a day from 'pending' to 'sent', once.

    Returns the updated row to whoever won, and None to everyone else — so a
    duplicate delivery after a restart sends nothing.
    """

  @abc.abstractmethod
  async def complete_plan_day(self, plan_day_id: int) -> Optional[PlanDayRow]:
    """Mark a day 'completed', once.

    Returns the updated row the first time and None afterwards, which is what
    makes a second tap on "I know this by heart" not double-log a session.
    """

  @abc.abstractmethod
  async def count_plan_days(self, plan_id: int, state: Optional[str] = None) -> int:
    """How many days the plan has, optionally in one state — the completion check."""


class InMemoryPlanStore(PlanStore):
  """Dict-backed `PlanStore`, used when DATABASE_URL is unset."""

  def __init__(self, state: MemoryState):
    self._state = state

  async def create_plan(self, user_id, target_kind, start_surah, start_ayah, end_surah,
                        end_ayah, pace, days_of_week, days, status=PLAN_ACTIVE):
    plan = PlanRow(
      id=self._state.next_id(), user_id=user_id, target_kind=target_kind,
      start_surah=start_surah, start_ayah=start_ayah, end_surah=end_surah,
      end_ayah=end_ayah, pace=int(pace), days_of_week=[int(d) for d in days_of_week],
      status=status, created_at=datetime.now(timezone.utc))
    self._state.plan[plan.id] = plan
    for spec in days:
      row = PlanDayRow(self._state.next_id(), plan.id, spec.scheduled_date, spec.surah,
                       spec.start_ayah, spec.end_ayah, DAY_PENDING)
      self._state.plan_day[row.id] = row
    return replace(plan, days_of_week=list(plan.days_of_week))

  async def get_plan(self, plan_id):
    plan = self._state.plan.get(plan_id)
    return replace(plan, days_of_week=list(plan.days_of_week)) if plan is not None else None

  async def get_active_plan(self, user_id):
    plans = await self.list_plans(user_id, PLAN_ACTIVE)
    return plans[0] if plans else None

  async def list_plans(self, user_id, status=None):
    plans = [p for p in self._state.plan.values()
             if p.user_id == user_id and (status is None or p.status == status)]
    plans.sort(key=lambda p: p.id, reverse=True)
    return [replace(p, days_of_week=list(p.days_of_week)) for p in plans]

  async def set_plan_status(self, plan_id, status):
    plan = self._state.plan.get(plan_id)
    if plan is None:
      return None
    plan.status = status
    return replace(plan, days_of_week=list(plan.days_of_week))

  async def list_plan_days(self, plan_id, state=None, on_or_before=None):
    rows = [d for d in self._state.plan_day.values()
            if d.plan_id == plan_id
            and (state is None or d.state == state)
            and (on_or_before is None or d.scheduled_date <= on_or_before)]
    rows.sort(key=lambda d: (d.scheduled_date, d.id))
    return [replace(d) for d in rows]

  async def get_plan_day(self, plan_day_id):
    row = self._state.plan_day.get(plan_day_id)
    return replace(row) if row is not None else None

  async def claim_plan_day(self, plan_day_id):
    row = self._state.plan_day.get(plan_day_id)
    if row is None or row.state != DAY_PENDING:
      return None
    row.state = DAY_SENT
    return replace(row)

  async def complete_plan_day(self, plan_day_id):
    row = self._state.plan_day.get(plan_day_id)
    if row is None or row.state == DAY_COMPLETED:
      return None
    row.state = DAY_COMPLETED
    return replace(row)

  async def count_plan_days(self, plan_id, state=None):
    return len(await self.list_plan_days(plan_id, state))


class PostgresPlanStore(PlanStore):
  """asyncpg-backed `PlanStore`."""

  def __init__(self, pool):
    self._pool = pool

  @staticmethod
  def _plan(record) -> Optional[PlanRow]:
    if record is None:
      return None
    return PlanRow(
      id=record["id"], user_id=record["user_id"], target_kind=record["target_kind"],
      start_surah=record["start_surah"], start_ayah=record["start_ayah"],
      end_surah=record["end_surah"], end_ayah=record["end_ayah"], pace=record["pace"],
      days_of_week=list(record["days_of_week"] or []), status=record["status"],
      created_at=record["created_at"])

  @staticmethod
  def _day(record) -> Optional[PlanDayRow]:
    if record is None:
      return None
    return PlanDayRow(record["id"], record["plan_id"], record["scheduled_date"],
                      record["surah"], record["start_ayah"], record["end_ayah"],
                      record["state"])

  async def create_plan(self, user_id, target_kind, start_surah, start_ayah, end_surah,
                        end_ayah, pace, days_of_week, days, status=PLAN_ACTIVE):
    async with self._pool.acquire() as conn:
      async with conn.transaction():
        record = await conn.fetchrow(
          "INSERT INTO plan (user_id, target_kind, start_surah, start_ayah, end_surah, "
          "end_ayah, pace, days_of_week, status) "
          "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING " + _PLAN_COLUMNS,
          user_id, target_kind, start_surah, start_ayah, end_surah, end_ayah,
          int(pace), [int(d) for d in days_of_week], status)
        plan_id = record["id"]
        if days:
          await conn.executemany(
            "INSERT INTO plan_day (plan_id, scheduled_date, surah, start_ayah, end_ayah, "
            "state) VALUES ($1, $2, $3, $4, $5, $6)",
            [(plan_id, d.scheduled_date, d.surah, d.start_ayah, d.end_ayah, DAY_PENDING)
             for d in days])
        return self._plan(record)

  async def get_plan(self, plan_id):
    return self._plan(await self._pool.fetchrow(
      "SELECT " + _PLAN_COLUMNS + " FROM plan WHERE id = $1", plan_id))

  async def get_active_plan(self, user_id):
    return self._plan(await self._pool.fetchrow(
      "SELECT " + _PLAN_COLUMNS + " FROM plan WHERE user_id = $1 AND status = $2 "
      "ORDER BY id DESC LIMIT 1", user_id, PLAN_ACTIVE))

  async def list_plans(self, user_id, status=None):
    if status is None:
      records = await self._pool.fetch(
        "SELECT " + _PLAN_COLUMNS + " FROM plan WHERE user_id = $1 ORDER BY id DESC",
        user_id)
    else:
      records = await self._pool.fetch(
        "SELECT " + _PLAN_COLUMNS + " FROM plan WHERE user_id = $1 AND status = $2 "
        "ORDER BY id DESC", user_id, status)
    return [self._plan(r) for r in records]

  async def set_plan_status(self, plan_id, status):
    return self._plan(await self._pool.fetchrow(
      "UPDATE plan SET status = $2, updated_at = now() WHERE id = $1 "
      "RETURNING " + _PLAN_COLUMNS, plan_id, status))

  async def list_plan_days(self, plan_id, state=None, on_or_before=None):
    records = await self._pool.fetch(
      "SELECT " + _DAY_COLUMNS + " FROM plan_day WHERE plan_id = $1 "
      "AND ($2::text IS NULL OR state = $2) "
      "AND ($3::date IS NULL OR scheduled_date <= $3) "
      "ORDER BY scheduled_date, id", plan_id, state, on_or_before)
    return [self._day(r) for r in records]

  async def get_plan_day(self, plan_day_id):
    return self._day(await self._pool.fetchrow(
      "SELECT " + _DAY_COLUMNS + " FROM plan_day WHERE id = $1", plan_day_id))

  async def claim_plan_day(self, plan_day_id):
    return self._day(await self._pool.fetchrow(
      "UPDATE plan_day SET state = $2, updated_at = now() WHERE id = $1 AND state = $3 "
      "RETURNING " + _DAY_COLUMNS, plan_day_id, DAY_SENT, DAY_PENDING))

  async def complete_plan_day(self, plan_day_id):
    return self._day(await self._pool.fetchrow(
      "UPDATE plan_day SET state = $2, updated_at = now() WHERE id = $1 AND state <> $2 "
      "RETURNING " + _DAY_COLUMNS, plan_day_id, DAY_COMPLETED))

  async def count_plan_days(self, plan_id, state=None):
    value = await self._pool.fetchval(
      "SELECT COUNT(*) FROM plan_day WHERE plan_id = $1 "
      "AND ($2::text IS NULL OR state = $2)", plan_id, state)
    return int(value or 0)
