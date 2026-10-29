"""Streak arithmetic: pure functions over dates and counts, no I/O.

A streak is a run of consecutive *local* dates on which a session was
completed. services/streaks.py reads the dates from the store and calls these.
"""

import logging
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable, List, Optional, Sequence, Tuple

from domain.localtime import DEFAULT_OFFSET, parse_offset

logger = logging.getLogger(__name__)

# The activity graph's window: 12 columns x 7 rows = 84 days, one quarter. Shared
# by the rendered /streak image and the Mini App's stats endpoint.
GRID_WEEKS = 12


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


def percentile_band(
    current_streak: int, population: Optional[Sequence[int]] = None
) -> Optional[int]:
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
        logger.warning("streaks: unparseable timezone %r, using UTC" % (offset,))
        return DEFAULT_OFFSET
    return offset
