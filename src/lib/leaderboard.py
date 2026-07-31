# The weekly board: sessions completed Mon 00:00 → Sun 23:59, in the user's own
# timezone (H1).
#
# Two things are load-bearing here and neither is negotiable:
#
#   * The week is computed from the *viewer's* local date. Every row of
#     `session_log` already carries the local date it counted for, so the window
#     is a plain date comparison and two users at different offsets can honestly
#     disagree about which week a Sunday-night session fell in. That is correct,
#     not a rounding error: the session happened on Sunday for one of them and on
#     Monday for the other.
#   * Opted-out users are excluded by the *query* (`store.sessions` joins on
#     `leaderboard_opt_in`), never by the renderer. A board that filters at render
#     time leaks a position count, and one forgotten template puts a private user
#     on a public list.
#
# This module adds no SQL and no second aggregation — it composes the two store
# calls the board needs and returns data, never a formatted line.

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Optional, Tuple

from lib.localtime import local_date, week_bounds
from lib.store import get_store
from lib.store.sessions import LeaderboardEntry
from lib.streaks import offset_of, user_offset

__all__ = [
    "DEFAULT_LIMIT", "LeaderboardEntry", "WeeklyBoard",
    "week_window", "user_week_window", "weekly_board",
]

# Ten rows is what fits in a Telegram message without scrolling past the point
# where anyone reads. H2 shows the caller's own row underneath when they miss it.
DEFAULT_LIMIT = 10


@dataclass(frozen=True)
class WeeklyBoard:
    """One rendered-nothing board: the top rows, plus where the viewer stands.

    `me` is the viewer's own entry — present even when they placed 400th, absent
    when they are opted out or completed nothing this week. `me_in_top` says
    whether it is already among `entries`, so the renderer knows whether to draw
    the extra "…and you" row rather than duplicating a row it already drew.
    """

    week_start: date
    week_end: date
    entries: Tuple[LeaderboardEntry, ...]
    me: Optional[LeaderboardEntry] = None
    me_in_top: bool = False
    opted_in: bool = False


def week_window(utc_now: datetime, offset: str) -> Tuple[date, date]:
    """The Mon→Sun local-date window containing `utc_now` for a user at `offset`.

    Inclusive on both ends, because `session_log.local_date` is a date: "Sunday
    23:59" is simply "Sunday".
    """
    return week_bounds(local_date(utc_now, offset))


async def user_week_window(user_id: int,
                           utc_now: Optional[datetime] = None) -> Tuple[date, date]:
    """`week_window` for a user's stored offset (UTC if they have none yet)."""
    return week_window(utc_now or datetime.now(timezone.utc), await user_offset(user_id))


async def weekly_board(user_id: int, utc_now: Optional[datetime] = None,
                       limit: int = DEFAULT_LIMIT) -> WeeklyBoard:
    """The current week's board as seen by `user_id`, with their own row attached.

    The viewer's rank costs a second query only when they are *not* already in the
    top `limit` — the common case for a small board is one query, and the
    fallback is a single indexed row lookup, never a second full scan.

    An opted-out viewer gets the board (it is a public list) but no `me` row:
    they are not on it, and the store would not return them anyway. The
    `opted_in` flag is what lets `/leaderboard` offer them the opt-in.
    """
    store = await get_store()
    profile = await store.profiles.get_profile(user_id)
    opted_in = bool(profile.leaderboard_opt_in) if profile is not None else False

    start, end = week_window(utc_now or datetime.now(timezone.utc), offset_of(profile))
    entries = tuple(await store.sessions.weekly_leaderboard(start, end, limit))

    me = next((e for e in entries if e.user_id == user_id), None)
    if me is not None:
        return WeeklyBoard(start, end, entries, me, True, opted_in)

    if opted_in:
        me = await store.sessions.weekly_rank(user_id, start, end)
    return WeeklyBoard(start, end, entries, me, False, opted_in)
