# Shared mutable state for the in-memory store implementation.
#
# One object holds every "table" so the five in-memory repositories can join
# across each other exactly as the SQL ones do (the weekly leaderboard reads
# session_log *and* user_profile, for instance). Handing all of them the same
# MemoryState instance is what keeps those joins honest.

from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class MemoryState:
    """The in-memory stand-in for the Postgres tables in `common/schema.sql`.

    Deliberately dumb: plain dicts and lists holding the same row dataclasses the
    asyncpg implementation returns. Nothing here is thread-safe, and it does not
    need to be — every repository method completes without awaiting, so the event
    loop never interleaves two of them.
    """

    user_settings: Dict[int, object] = field(default_factory=dict)  # user_id -> UserSettingsRow
    user_profile: Dict[int, object] = field(default_factory=dict)  # user_id -> ProfileRow
    reader_position: Dict[int, tuple] = field(
        default_factory=dict
    )  # user_id -> (surah, ayah, view)
    hifz_interval: List[object] = field(default_factory=list)  # HifzInterval
    plan: Dict[int, object] = field(default_factory=dict)  # plan_id -> PlanRow
    plan_day: Dict[int, object] = field(default_factory=dict)  # id -> PlanDayRow
    session_log: List[object] = field(default_factory=list)  # SessionRow
    scheduled_send: Dict[int, object] = field(default_factory=dict)  # id -> ScheduledSend
    # Phase 2 — the group cluster.
    group_config: Dict[int, object] = field(default_factory=dict)  # chat_id -> GroupConfig
    group_plan: Dict[int, object] = field(default_factory=dict)  # id -> GroupPlanRow
    group_plan_day: Dict[int, object] = field(default_factory=dict)  # id -> GroupPlanDayRow
    group_member_link: List[object] = field(default_factory=list)  # GroupMemberLink
    # Multi-platform — (platform, external_id) -> IdentityRow.
    identity: Dict[tuple, object] = field(default_factory=dict)
    daily_ayah_sub: Dict[int, object] = field(default_factory=dict)  # user_id -> DailySubRow
    tajweed_approval: Dict[str, object] = field(default_factory=dict)  # lesson_id -> ApprovalRow
    tajweed_progress: Dict[int, Set[str]] = field(default_factory=dict)  # user_id -> lesson ids
    sequence: int = 0
    # Stands in for the `non_telegram_user_id` sequence; see store/identity.py.
    user_id_sequence: int = 2**52 - 1

    def next_id(self) -> int:
        """Hand out the next surrogate key, standing in for BIGSERIAL.

        One counter across all tables rather than one per table: ids are opaque to
        callers, and a single sequence makes a mixed-up id obvious in a failing test
        instead of silently addressing the wrong row.
        """
        self.sequence += 1
        return self.sequence

    def next_user_id(self) -> int:
        """Hand out the next non-Telegram `user_id`, from 2^52 up."""
        self.user_id_sequence += 1
        return self.user_id_sequence

    def clear(self) -> None:
        """Drop every row and reset the sequence (used by `reset_for_tests`)."""
        self.user_settings.clear()
        self.user_profile.clear()
        self.reader_position.clear()
        self.hifz_interval.clear()
        self.plan.clear()
        self.plan_day.clear()
        self.session_log.clear()
        self.scheduled_send.clear()
        self.group_config.clear()
        self.group_plan.clear()
        self.group_plan_day.clear()
        self.group_member_link.clear()
        self.identity.clear()
        self.daily_ayah_sub.clear()
        self.tajweed_approval.clear()
        self.tajweed_progress.clear()
        self.sequence = 0
        self.user_id_sequence = 2**52 - 1
