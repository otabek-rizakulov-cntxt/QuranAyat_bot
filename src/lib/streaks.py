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
# rollover to 05:00. `lib.localtime` owns that arithmetic; nothing here adds or
# subtracts hours by hand.
#
# The one genuinely contested piece of arithmetic is what "current" means before
# the user has acted today — see `GRACE_DAYS`.

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Iterable, List, Optional, Sequence, Tuple

from lib.localtime import DEFAULT_OFFSET, local_date, parse_offset
from lib.store import get_store

__all__ = [
    "GRACE_DAYS", "MILESTONE_DAYS", "PERCENTILE_MIN_USERS", "PERCENTILE_BANDS",
    "StreakCounts", "Milestone", "StreakSummary", "SessionOutcome",
    "compute_streak", "milestone_for", "percentile_band", "offset_of",
    "user_offset", "user_today", "refresh_streaks", "record_session", "streak_summary",
]

# How stale the last active day may be and still count as a live streak.
#
# 1 = "a streak that ended yesterday is still yours". The user woke up on day 8
# of a 7-day streak and has not drilled *yet*; the day is not over, and telling
# them at 08:00 that they are back to zero would be both wrong and the fastest
# way to lose them. The streak dies only once a whole local day has passed with
# no session — i.e. when the last active date is the day before yesterday.
#
# Note what this does NOT do: it never *extends* the count. A streak last touched
# yesterday still reads 7, not 8. Acting today is what makes it 8.
GRACE_DAYS = 1

# G3's fixed milestones. Deliberately few and far apart — a milestone that fires
# every other day is not a milestone.
MILESTONE_DAYS: Tuple[int, ...] = (7, 30, 100, 365)

# Assumption 2, not overridden: no percentile claim until the population is big
# enough for one to mean anything. "Top 10% of users" out of nine users is a
# joke at the bot's expense.
PERCENTILE_MIN_USERS = 200

# The only percentages ever claimed. Bands rather than an exact figure: "top 4.7%"
# reads as false precision on a number that changes every hour.
PERCENTILE_BANDS: Tuple[int, ...] = (1, 5, 10, 25, 50)


@dataclass(frozen=True)
class StreakCounts:
    """The pair of numbers denormalized onto `user_profile`, plus the context
    needed to render them without a second pass over the history."""

    current: int
    longest: int
    last_active: Optional[date] = None
    active_today: bool = False


@dataclass(frozen=True)
class Milestone:
    """Which fixed milestone the streak just hit, and which one is next.

    `key` / `next_key` are *identifiers*, not prose: the localized string table
    (Wave 2C) turns them into a sentence in the user's language. A milestone
    congratulating the user in English from inside a library would be
    untranslatable by construction.
    """

    reached: Optional[int] = None
    key: Optional[str] = None
    next: Optional[int] = None
    next_key: Optional[str] = None
    days_to_next: Optional[int] = None


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


def compute_streak(active_dates: Iterable[date], today: date) -> StreakCounts:
    """Current and longest run of consecutive active days, as of `today`.

    `active_dates` is what `store.sessions.list_active_dates` returns: distinct
    local dates, in any order (they are de-duplicated here anyway, which is what
    makes two sessions on one local date tick the streak exactly once).

    The current run counts only if it reaches into the last `GRACE_DAYS` days —
    a run that ended yesterday is still alive, one that ended the day before is
    broken. A last active date in the future (only reachable by moving one's UTC
    offset far east) is treated as today rather than as a gap.
    """
    days: List[date] = sorted(set(active_dates))
    if not days:
        return StreakCounts(0, 0, None, False)

    longest = run = 1
    one_day = timedelta(days=1)
    for previous, current in zip(days, days[1:]):
        run = run + 1 if current - previous == one_day else 1
        longest = max(longest, run)

    last = days[-1]
    gap = (today - last).days
    return StreakCounts(
        current=run if gap <= GRACE_DAYS else 0,
        longest=longest,
        last_active=last,
        active_today=last >= today,
    )


def milestone_for(current_streak: int) -> Milestone:
    """The milestone a streak of `current_streak` days sits on and heads towards.

    `reached` is set only on the exact day the streak equals a milestone, so the
    congratulation fires once instead of every day thereafter.
    """
    reached = current_streak if current_streak in MILESTONE_DAYS else None
    upcoming = next((m for m in MILESTONE_DAYS if m > current_streak), None)
    return Milestone(
        reached=reached,
        key=_milestone_key(reached),
        next=upcoming,
        next_key=_milestone_key(upcoming),
        days_to_next=(upcoming - current_streak) if upcoming is not None else None,
    )


def _milestone_key(days: Optional[int]) -> Optional[str]:
    return None if days is None else "streak_milestone_%d" % days


def percentile_band(current_streak: int,
                    population: Optional[Sequence[int]] = None) -> Optional[int]:
    """The "top N% of users" band this streak earns, or None to stay dark.

    None — meaning *render no percentile claim at all* — whenever:

      * no population sample was supplied (the default, and the only state the
        bot is in today: nothing collects one yet),
      * fewer than `PERCENTILE_MIN_USERS` users actually have a streak, which is
        assumption 2's threshold, or
      * the user is not in the top half, where the line would be a taunt.

    `population` is every user's current streak. Users on zero are dropped before
    counting: "200 users with a streak" is the threshold, not "200 rows".
    """
    if not population or current_streak < 1:
        return None
    streaks = [s for s in population if s and s >= 1]
    if len(streaks) < PERCENTILE_MIN_USERS:
        return None

    ahead = sum(1 for s in streaks if s > current_streak)
    share = 100.0 * ahead / len(streaks)
    return next((band for band in PERCENTILE_BANDS if share <= band), None)


def offset_of(profile) -> str:
    """A `ProfileRow`'s UTC offset, falling back to UTC.

    A profile that has never been through timezone setup has `timezone = None`;
    a stored value that no longer parses (a hand-edited row) is treated the same
    way rather than raising in the middle of logging a session. Takes the row
    rather than a user id so a caller that already holds the profile — the
    leaderboard does — needs no second read.
    """
    offset = profile.timezone if profile is not None else None
    if not offset:
        return DEFAULT_OFFSET
    try:
        parse_offset(offset)
    except (ValueError, TypeError):
        print("streaks: unparseable timezone %r, using UTC" % (offset,))
        return DEFAULT_OFFSET
    return offset


async def user_offset(user_id: int) -> str:
    """`offset_of` for a user id, for callers that hold no profile row."""
    store = await get_store()
    return offset_of(await store.profiles.get_profile(user_id))


async def user_today(user_id: int, utc_now: Optional[datetime] = None) -> date:
    """The date it is right now where the user is — the streak's "today"."""
    return local_date(utc_now or datetime.now(timezone.utc), await user_offset(user_id))


async def refresh_streaks(user_id: int, today: Optional[date] = None,
                          utc_now: Optional[datetime] = None) -> StreakCounts:
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


async def record_session(user_id: int, kind: str, utc_now: Optional[datetime] = None,
                         surah: Optional[int] = None, start_ayah: Optional[int] = None,
                         end_ayah: Optional[int] = None) -> SessionOutcome:
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


async def streak_summary(user_id: int, utc_now: Optional[datetime] = None,
                         population: Optional[Sequence[int]] = None) -> StreakSummary:
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
