# Streaks: the one number a memorizer checks every day.
#
# A streak is a run of consecutive *local* dates on which a session was completed
# (G1). Everything here is computed from `session_log` — `user_profile`'s
# `current_streak` / `longest_streak` are a denormalized cache of this module's
# answer, written on every session so `/leaderboard` and `/streak` can read a
# streak without walking a user's whole history.
#
# The day unit is the user's local date, never UTC: 23:59 and 00:01 local are two
# days one minute apart, and a UTC boundary would silently move a UTC+5 user's
# rollover to 05:00. `domain.localtime` owns that arithmetic; nothing here adds or
# subtracts hours by hand.
#
# The one genuinely contested piece of arithmetic is what "current" means before
# the user has acted today — see `GRACE_DAYS`.
import logging
from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Optional, Sequence

from domain.localtime import local_date
from domain.streaks import (  # re-exported: callers read streaks from one place
    GRACE_DAYS,
    MILESTONE_DAYS,
    PERCENTILE_BANDS,
    PERCENTILE_MIN_USERS,
    Milestone,
    StreakCounts,
    compute_streak,
    milestone_for,
    offset_of,
    percentile_band,
)
from infra.store import get_store

logger = logging.getLogger(__name__)

__all__ = [
    "GRACE_DAYS",
    "MILESTONE_DAYS",
    "PERCENTILE_MIN_USERS",
    "PERCENTILE_BANDS",
    "StreakCounts",
    "Milestone",
    "StreakSummary",
    "SessionOutcome",
    "compute_streak",
    "milestone_for",
    "percentile_band",
    "offset_of",
    "user_offset",
    "user_today",
    "refresh_streaks",
    "record_session",
    "streak_summary",
]


@dataclass(frozen=True)
class StreakSummary:
    """Everything `/streak` needs, as data. No strings, no percent signs.

    `at_risk` is the streak's live product question: the run is still standing but
    today has not been earned yet, so today is the day it can be lost.
    """

    user_id: int
    today: date
    current: int
    longest: int
    active_today: bool
    at_risk: bool
    milestone: Milestone
    percentile: Optional[int] = None


@dataclass(frozen=True)
class SessionOutcome:
    """The result of logging one session: whether it was new, which local day it
    landed on, and the streak as it stands afterwards."""

    logged: bool
    local_date: date
    streak: StreakCounts
    milestone: Milestone


async def user_offset(user_id: int) -> str:
    """`offset_of` for a user id, for callers that hold no profile row."""
    store = await get_store()
    return offset_of(await store.profiles.get_profile(user_id))


async def user_today(user_id: int, utc_now: Optional[datetime] = None) -> date:
    """The date it is right now where the user is — the streak's "today"."""
    return local_date(utc_now or datetime.now(timezone.utc), await user_offset(user_id))


async def refresh_streaks(
    user_id: int, today: Optional[date] = None, utc_now: Optional[datetime] = None
) -> StreakCounts:
    """Recompute both counters from `session_log` and write them to the profile.

    Recomputed from scratch rather than incremented: an incremented counter drifts
    the first time a write is retried or a session is logged out of order, and the
    history is a few hundred rows at most.

    `longest` never decreases — the stored value wins if it is larger. It should
    not be (the history is the source of truth), but if history is ever trimmed,
    losing someone's lifetime best is not an acceptable failure mode.
    """
    store = await get_store()
    if today is None:
        today = await user_today(user_id, utc_now)

    counts = compute_streak(await store.sessions.list_active_dates(user_id), today)
    profile = await store.profiles.get_profile(user_id)
    longest = max(counts.longest, profile.longest_streak if profile is not None else 0)
    counts = StreakCounts(counts.current, longest, counts.last_active, counts.active_today)

    await store.profiles.set_streaks(user_id, counts.current, counts.longest)
    return counts


async def record_session(
    user_id: int,
    kind: str,
    utc_now: Optional[datetime] = None,
    surah: Optional[int] = None,
    start_ayah: Optional[int] = None,
    end_ayah: Optional[int] = None,
) -> SessionOutcome:
    """Log one completed session and recompute the streak in the same breath.

    The single entry point for "the user finished a drill / passed a recall
    check". The session's day is the user's local date at `utc_now`, so a session
    finished at 23:59 and one at 00:01 land on different days and tick the streak
    twice, while two on the same evening tick it once (the store dedupes on
    (user, local_date, kind, portion), and `compute_streak` works on distinct
    dates regardless).

    `logged` is False when the store recognized this exact session as a duplicate;
    the streak is still refreshed, because it costs one query and keeps the
    denormalized counters honest after any earlier failure.
    """
    store = await get_store()
    now = utc_now or datetime.now(timezone.utc)
    day = local_date(now, await user_offset(user_id))

    row = await store.sessions.log_session(user_id, day, kind, surah, start_ayah, end_ayah)
    counts = await refresh_streaks(user_id, today=day)
    return SessionOutcome(row is not None, day, counts, milestone_for(counts.current))


async def streak_summary(
    user_id: int, utc_now: Optional[datetime] = None, population: Optional[Sequence[int]] = None
) -> StreakSummary:
    """Everything `/streak` renders, read from the denormalized counters.

    Reads `user_profile`, not `session_log`: the counters are written on every
    session, so this is a single row read on a command that is pressed often.

    `population` is the opt-in hook for the percentile line — omit it (as every
    caller does today) and no percentile is produced. See `percentile_band`.
    """
    store = await get_store()
    today = await user_today(user_id, utc_now)
    profile = await store.profiles.get_profile(user_id)
    current = profile.current_streak if profile is not None else 0
    longest = profile.longest_streak if profile is not None else 0

    # "Has today been earned?" is not on the profile, and it is the difference
    # between "7 days 🔥" and "7 days — don't lose it today". One day's worth of
    # rows answers it; no history walk.
    active_today = bool(await store.sessions.list_active_dates(user_id, since=today))

    return StreakSummary(
        user_id=user_id,
        today=today,
        current=current,
        longest=longest,
        active_today=active_today,
        at_risk=current > 0 and not active_today,
        milestone=milestone_for(current),
        percentile=percentile_band(current, population),
    )
