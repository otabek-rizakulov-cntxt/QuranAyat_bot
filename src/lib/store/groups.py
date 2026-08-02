# The group cluster's storage (Phase 2, items 5-7).
#
# A configured supergroup runs one study circle: `group_config` holds its
# settings and the forum topic the bot created and owns; `group_plan` /
# `group_plan_day` mirror the personal `plan` / `plan_day` shape, keyed by chat
# rather than user; `group_member_link` records who consented to appear on the
# board. The bot ignores any group without a `group_config` row — that is how the
# Phase-1 blanket ban on `chat_id < 0` becomes a selective one.

import abc
from dataclasses import dataclass, field, replace
from datetime import date, datetime, time, timezone
from typing import Any, Dict, List, Optional, Sequence

from ._state import MemoryState
from .plans import PlanDaySpec

CONFIG_SETUP = "setup"
CONFIG_ACTIVE = "active"
CONFIG_PAUSED = "paused"

GPLAN_ACTIVE = "active"
GPLAN_PAUSED = "paused"
GPLAN_COMPLETE = "complete"

GDAY_PENDING = "pending"
GDAY_SENT = "sent"


@dataclass
class GroupConfig:
  """A row of `group_config`. `thread_id` is the forum topic the bot created."""

  chat_id: int
  admin_user_id: int
  thread_id: Optional[int] = None
  translation_lang: str = "en"
  reciter: str = "Husary_128kbps"
  timezone: Optional[str] = None          # fixed UTC offset, e.g. "+05:00"
  post_time: Optional[time] = None        # local to the group
  days_of_week: List[int] = field(default_factory=list)   # 1=Mon … 7=Sun
  content_flags: Dict[str, Any] = field(default_factory=dict)
  status: str = CONFIG_SETUP


@dataclass
class GroupPlanRow:
  """A row of `group_plan` — same shape as `PlanRow`, keyed by chat_id."""

  id: int
  chat_id: int
  target_kind: str
  start_surah: int
  start_ayah: int
  end_surah: int
  end_ayah: int
  pace: int
  days_of_week: List[int] = field(default_factory=list)
  status: str = GPLAN_ACTIVE
  created_at: Optional[datetime] = None


@dataclass
class GroupPlanDayRow:
  """A row of `group_plan_day` — one day's portion for the whole circle."""

  id: int
  group_plan_id: int
  scheduled_date: date
  surah: int
  start_ayah: int
  end_ayah: int
  state: str = GDAY_PENDING


@dataclass
class GroupMemberLink:
  user_id: int
  chat_id: int
  linked_at: Optional[datetime] = None


class GroupStore(abc.ABC):
  """Everything the group cluster reads and writes. No SQL escapes this layer."""

  # --- config --------------------------------------------------------------
  @abc.abstractmethod
  async def get_config(self, chat_id: int) -> Optional[GroupConfig]: ...

  @abc.abstractmethod
  async def ensure_config(self, chat_id: int, admin_user_id: int) -> GroupConfig:
    """Create the row on first setup, or return the existing one. Adopting a bot
    into a group it already knows must not reset its config, so this never
    overwrites an existing admin."""

  @abc.abstractmethod
  async def update_config(self, chat_id: int, **fields) -> Optional[GroupConfig]:
    """Set any subset of the mutable columns; returns the updated row or None."""

  @abc.abstractmethod
  async def list_active_configs(self) -> List[GroupConfig]:
    """Every group whose status is 'active' and has a post_time — the scan a
    per-day enqueue walks."""

  @abc.abstractmethod
  async def delete_config(self, chat_id: int) -> None: ...

  # --- plan ----------------------------------------------------------------
  @abc.abstractmethod
  async def create_plan(self, chat_id: int, target_kind: str, start_surah: int,
                        start_ayah: int, end_surah: int, end_ayah: int, pace: int,
                        days_of_week: Sequence[int], days: Sequence[PlanDaySpec],
                        status: str = GPLAN_ACTIVE) -> GroupPlanRow: ...

  @abc.abstractmethod
  async def get_active_plan(self, chat_id: int) -> Optional[GroupPlanRow]: ...

  @abc.abstractmethod
  async def set_plan_status(self, plan_id: int, status: str) -> Optional[GroupPlanRow]: ...

  @abc.abstractmethod
  async def list_plan_days(self, plan_id: int, state: Optional[str] = None,
                           on_or_before: Optional[date] = None) -> List[GroupPlanDayRow]: ...

  @abc.abstractmethod
  async def get_plan_day(self, day_id: int) -> Optional[GroupPlanDayRow]: ...

  @abc.abstractmethod
  async def claim_plan_day(self, day_id: int) -> Optional[GroupPlanDayRow]:
    """pending -> sent, conditional. The row to the first caller, None after —
    the same double-send guard the personal plan uses."""

  # --- member links --------------------------------------------------------
  @abc.abstractmethod
  async def link_member(self, user_id: int, chat_id: int) -> GroupMemberLink: ...

  @abc.abstractmethod
  async def unlink_member(self, user_id: int, chat_id: int) -> None: ...

  @abc.abstractmethod
  async def is_linked(self, user_id: int, chat_id: int) -> bool: ...

  @abc.abstractmethod
  async def list_linked(self, chat_id: int) -> List[int]:
    """The user ids consented to this group's board, ascending."""


# --- in-memory ---------------------------------------------------------------

class InMemoryGroupStore(GroupStore):
  def __init__(self, state: MemoryState):
    self._state = state

  def _copy(self, row):
    return replace(row) if row is not None else None

  async def get_config(self, chat_id):
    return self._copy(self._state.group_config.get(chat_id))

  async def ensure_config(self, chat_id, admin_user_id):
    row = self._state.group_config.get(chat_id)
    if row is None:
      row = GroupConfig(chat_id=chat_id, admin_user_id=admin_user_id)
      self._state.group_config[chat_id] = row
    return self._copy(row)

  async def update_config(self, chat_id, **fields):
    row = self._state.group_config.get(chat_id)
    if row is None:
      return None
    for k, v in fields.items():
      setattr(row, k, v)
    return self._copy(row)

  async def list_active_configs(self):
    return [self._copy(r) for r in self._state.group_config.values()
            if r.status == CONFIG_ACTIVE and r.post_time is not None]

  async def delete_config(self, chat_id):
    self._state.group_config.pop(chat_id, None)

  async def create_plan(self, chat_id, target_kind, start_surah, start_ayah,
                        end_surah, end_ayah, pace, days_of_week, days,
                        status=GPLAN_ACTIVE):
    plan_id = self._state.next_id()
    row = GroupPlanRow(id=plan_id, chat_id=chat_id, target_kind=target_kind,
                       start_surah=start_surah, start_ayah=start_ayah,
                       end_surah=end_surah, end_ayah=end_ayah, pace=pace,
                       days_of_week=list(days_of_week), status=status,
                       created_at=datetime.now(timezone.utc))
    self._state.group_plan[plan_id] = row
    for spec in days:
      day_id = self._state.next_id()
      self._state.group_plan_day[day_id] = GroupPlanDayRow(
          id=day_id, group_plan_id=plan_id, scheduled_date=spec.scheduled_date,
          surah=spec.surah, start_ayah=spec.start_ayah, end_ayah=spec.end_ayah)
    return self._copy(row)

  async def get_active_plan(self, chat_id):
    active = [r for r in self._state.group_plan.values()
              if r.chat_id == chat_id and r.status == GPLAN_ACTIVE]
    active.sort(key=lambda r: r.id, reverse=True)
    return self._copy(active[0]) if active else None

  async def set_plan_status(self, plan_id, status):
    row = self._state.group_plan.get(plan_id)
    if row is None:
      return None
    row.status = status
    return self._copy(row)

  async def list_plan_days(self, plan_id, state=None, on_or_before=None):
    rows = [r for r in self._state.group_plan_day.values()
            if r.group_plan_id == plan_id
            and (state is None or r.state == state)
            and (on_or_before is None or r.scheduled_date <= on_or_before)]
    rows.sort(key=lambda r: (r.scheduled_date, r.id))
    return [self._copy(r) for r in rows]

  async def get_plan_day(self, day_id):
    return self._copy(self._state.group_plan_day.get(day_id))

  async def claim_plan_day(self, day_id):
    row = self._state.group_plan_day.get(day_id)
    if row is None or row.state != GDAY_PENDING:
      return None
    row.state = GDAY_SENT
    return self._copy(row)

  async def link_member(self, user_id, chat_id):
    for link in self._state.group_member_link:
      if link.user_id == user_id and link.chat_id == chat_id:
        return self._copy(link)
    link = GroupMemberLink(user_id=user_id, chat_id=chat_id,
                           linked_at=datetime.now(timezone.utc))
    self._state.group_member_link.append(link)
    return self._copy(link)

  async def unlink_member(self, user_id, chat_id):
    self._state.group_member_link[:] = [
        l for l in self._state.group_member_link
        if not (l.user_id == user_id and l.chat_id == chat_id)]

  async def is_linked(self, user_id, chat_id):
    return any(l.user_id == user_id and l.chat_id == chat_id
               for l in self._state.group_member_link)

  async def list_linked(self, chat_id):
    return sorted(l.user_id for l in self._state.group_member_link
                  if l.chat_id == chat_id)


# --- asyncpg -----------------------------------------------------------------

_CONFIG_COLS = ("chat_id, admin_user_id, thread_id, translation_lang, reciter, "
                "timezone, post_time, days_of_week, content_flags, status")
_MUTABLE = ("thread_id", "translation_lang", "reciter", "timezone", "post_time",
            "days_of_week", "content_flags", "status", "admin_user_id")


class PostgresGroupStore(GroupStore):
  def __init__(self, pool):
    self._pool = pool

  def _config(self, r):
    if r is None:
      return None
    import ujson as json
    flags = r["content_flags"]
    if isinstance(flags, str):
      flags = json.loads(flags)
    return GroupConfig(
        chat_id=r["chat_id"], admin_user_id=r["admin_user_id"],
        thread_id=r["thread_id"], translation_lang=r["translation_lang"],
        reciter=r["reciter"], timezone=r["timezone"], post_time=r["post_time"],
        days_of_week=list(r["days_of_week"] or []), content_flags=flags or {},
        status=r["status"])

  def _plan(self, r):
    if r is None:
      return None
    return GroupPlanRow(
        id=r["id"], chat_id=r["chat_id"], target_kind=r["target_kind"],
        start_surah=r["start_surah"], start_ayah=r["start_ayah"],
        end_surah=r["end_surah"], end_ayah=r["end_ayah"], pace=r["pace"],
        days_of_week=list(r["days_of_week"] or []), status=r["status"],
        created_at=r["created_at"])

  def _day(self, r):
    if r is None:
      return None
    return GroupPlanDayRow(
        id=r["id"], group_plan_id=r["group_plan_id"],
        scheduled_date=r["scheduled_date"], surah=r["surah"],
        start_ayah=r["start_ayah"], end_ayah=r["end_ayah"], state=r["state"])

  async def get_config(self, chat_id):
    return self._config(await self._pool.fetchrow(
        "SELECT " + _CONFIG_COLS + " FROM group_config WHERE chat_id = $1", chat_id))

  async def ensure_config(self, chat_id, admin_user_id):
    await self._pool.execute(
        "INSERT INTO group_config (chat_id, admin_user_id) VALUES ($1, $2) "
        "ON CONFLICT (chat_id) DO NOTHING", chat_id, admin_user_id)
    return await self.get_config(chat_id)

  async def update_config(self, chat_id, **fields):
    import ujson as json
    sets, args = [], []
    for k, v in fields.items():
      if k not in _MUTABLE:
        raise ValueError("group_config has no mutable column %r" % k)
      args.append(json.dumps(v) if k == "content_flags" else v)
      sets.append("%s = $%d" % (k, len(args) + 1))
    if not sets:
      return await self.get_config(chat_id)
    q = ("UPDATE group_config SET " + ", ".join(sets) + ", updated_at = now() "
         "WHERE chat_id = $1 RETURNING " + _CONFIG_COLS)
    return self._config(await self._pool.fetchrow(q, chat_id, *args))

  async def list_active_configs(self):
    rows = await self._pool.fetch(
        "SELECT " + _CONFIG_COLS + " FROM group_config "
        "WHERE status = $1 AND post_time IS NOT NULL ORDER BY chat_id",
        CONFIG_ACTIVE)
    return [self._config(r) for r in rows]

  async def delete_config(self, chat_id):
    await self._pool.execute("DELETE FROM group_config WHERE chat_id = $1", chat_id)

  async def create_plan(self, chat_id, target_kind, start_surah, start_ayah,
                        end_surah, end_ayah, pace, days_of_week, days,
                        status=GPLAN_ACTIVE):
    async with self._pool.acquire() as conn:
      async with conn.transaction():
        row = await conn.fetchrow(
            "INSERT INTO group_plan (chat_id, target_kind, start_surah, "
            "start_ayah, end_surah, end_ayah, pace, days_of_week, status) "
            "VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) RETURNING id, chat_id, "
            "target_kind, start_surah, start_ayah, end_surah, end_ayah, pace, "
            "days_of_week, status, created_at",
            chat_id, target_kind, start_surah, start_ayah, end_surah, end_ayah,
            pace, list(days_of_week), status)
        for spec in days:
          await conn.execute(
              "INSERT INTO group_plan_day (group_plan_id, scheduled_date, surah, "
              "start_ayah, end_ayah) VALUES ($1,$2,$3,$4,$5)",
              row["id"], spec.scheduled_date, spec.surah, spec.start_ayah,
              spec.end_ayah)
    return self._plan(row)

  async def get_active_plan(self, chat_id):
    return self._plan(await self._pool.fetchrow(
        "SELECT id, chat_id, target_kind, start_surah, start_ayah, end_surah, "
        "end_ayah, pace, days_of_week, status, created_at FROM group_plan "
        "WHERE chat_id = $1 AND status = $2 ORDER BY id DESC LIMIT 1",
        chat_id, GPLAN_ACTIVE))

  async def set_plan_status(self, plan_id, status):
    return self._plan(await self._pool.fetchrow(
        "UPDATE group_plan SET status = $2 WHERE id = $1 RETURNING id, chat_id, "
        "target_kind, start_surah, start_ayah, end_surah, end_ayah, pace, "
        "days_of_week, status, created_at", plan_id, status))

  async def list_plan_days(self, plan_id, state=None, on_or_before=None):
    q = ("SELECT id, group_plan_id, scheduled_date, surah, start_ayah, end_ayah, "
         "state FROM group_plan_day WHERE group_plan_id = $1")
    args = [plan_id]
    if state is not None:
      args.append(state); q += " AND state = $%d" % len(args)
    if on_or_before is not None:
      args.append(on_or_before); q += " AND scheduled_date <= $%d" % len(args)
    q += " ORDER BY scheduled_date, id"
    return [self._day(r) for r in await self._pool.fetch(q, *args)]

  async def get_plan_day(self, day_id):
    return self._day(await self._pool.fetchrow(
        "SELECT id, group_plan_id, scheduled_date, surah, start_ayah, end_ayah, "
        "state FROM group_plan_day WHERE id = $1", day_id))

  async def claim_plan_day(self, day_id):
    return self._day(await self._pool.fetchrow(
        "UPDATE group_plan_day SET state = $2 WHERE id = $1 AND state = $3 "
        "RETURNING id, group_plan_id, scheduled_date, surah, start_ayah, "
        "end_ayah, state", day_id, GDAY_SENT, GDAY_PENDING))

  async def link_member(self, user_id, chat_id):
    row = await self._pool.fetchrow(
        "INSERT INTO group_member_link (user_id, chat_id) VALUES ($1, $2) "
        "ON CONFLICT (user_id, chat_id) DO UPDATE SET user_id = EXCLUDED.user_id "
        "RETURNING user_id, chat_id, linked_at", user_id, chat_id)
    return GroupMemberLink(user_id=row["user_id"], chat_id=row["chat_id"],
                           linked_at=row["linked_at"])

  async def unlink_member(self, user_id, chat_id):
    await self._pool.execute(
        "DELETE FROM group_member_link WHERE user_id = $1 AND chat_id = $2",
        user_id, chat_id)

  async def is_linked(self, user_id, chat_id):
    return await self._pool.fetchval(
        "SELECT EXISTS(SELECT 1 FROM group_member_link "
        "WHERE user_id = $1 AND chat_id = $2)", user_id, chat_id)

  async def list_linked(self, chat_id):
    rows = await self._pool.fetch(
        "SELECT user_id FROM group_member_link WHERE chat_id = $1 "
        "ORDER BY user_id", chat_id)
    return [r["user_id"] for r in rows]
