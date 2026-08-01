# Shared mutable state for the in-memory store implementation.
#
# One object holds every "table" so the five in-memory repositories can join
# across each other exactly as the SQL ones do (the weekly leaderboard reads
# session_log *and* user_profile, for instance). Handing all of them the same
# MemoryState instance is what keeps those joins honest.

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class MemoryState:
  """The in-memory stand-in for the Postgres tables in `common/schema.sql`.

  Deliberately dumb: plain dicts and lists holding the same row dataclasses the
  asyncpg implementation returns. Nothing here is thread-safe, and it does not
  need to be — every repository method completes without awaiting, so the event
  loop never interleaves two of them.
  """

  user_settings: Dict[int, object] = field(default_factory=dict)   # user_id -> UserSettingsRow
  user_profile: Dict[int, object] = field(default_factory=dict)    # user_id -> ProfileRow
  hifz_interval: List[object] = field(default_factory=list)        # HifzInterval
  plan: Dict[int, object] = field(default_factory=dict)            # plan_id -> PlanRow
  plan_day: Dict[int, object] = field(default_factory=dict)        # id -> PlanDayRow
  session_log: List[object] = field(default_factory=list)          # SessionRow
  scheduled_send: Dict[int, object] = field(default_factory=dict)  # id -> ScheduledSend
  # Phase 2 — the group cluster.
  group_config: Dict[int, object] = field(default_factory=dict)    # chat_id -> GroupConfig
  group_plan: Dict[int, object] = field(default_factory=dict)      # id -> GroupPlanRow
  group_plan_day: Dict[int, object] = field(default_factory=dict)  # id -> GroupPlanDayRow
  group_member_link: List[object] = field(default_factory=list)    # GroupMemberLink
  sequence: int = 0

  def next_id(self) -> int:
    """Hand out the next surrogate key, standing in for BIGSERIAL.

    One counter across all tables rather than one per table: ids are opaque to
    callers, and a single sequence makes a mixed-up id obvious in a failing test
    instead of silently addressing the wrong row.
    """
    self.sequence += 1
    return self.sequence

  def clear(self) -> None:
    """Drop every row and reset the sequence (used by `reset_for_tests`)."""
    self.user_settings.clear()
    self.user_profile.clear()
    self.hifz_interval.clear()
    self.plan.clear()
    self.plan_day.clear()
    self.session_log.clear()
    self.scheduled_send.clear()
    self.group_config.clear()
    self.group_plan.clear()
    self.group_plan_day.clear()
    self.group_member_link.clear()
    self.sequence = 0
