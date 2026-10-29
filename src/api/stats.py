# GET /streak (counters, milestone, 12-week activity) and GET /leaderboard.

from datetime import date, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from lib.leaderboard import weekly_board
from lib.localtime import week_bounds
from lib.store import get_store
from lib.streak_image import GRID_WEEKS
from lib.streaks import streak_summary

from .auth import require_user

router = APIRouter()


class MilestoneOut(BaseModel):
    reached: Optional[int] = None
    key: Optional[str] = None
    next: Optional[int] = None
    next_key: Optional[str] = None
    days_to_next: Optional[int] = None


class DayCount(BaseModel):
    date: date
    sessions: int


class StreakOut(BaseModel):
    today: date
    current: int
    longest: int
    active_today: bool
    at_risk: bool
    milestone: MilestoneOut
    # The graph window: GRID_WEEKS whole weeks, Monday-aligned, ending this week —
    # the same window as the bot's PNG. Days with no session are omitted.
    window_start: date
    activity: List[DayCount]


@router.get("/streak", response_model=StreakOut)
async def streak(user_id: int = Depends(require_user)) -> StreakOut:
    summary = await streak_summary(user_id)
    monday, _ = week_bounds(summary.today)
    start = monday - timedelta(weeks=GRID_WEEKS - 1)
    store = await get_store()
    counts: dict = {}
    for row in await store.sessions.list_sessions(user_id, start=start, end=summary.today):
        counts[row.local_date] = counts.get(row.local_date, 0) + 1
    m = summary.milestone
    return StreakOut(
        today=summary.today,
        current=summary.current,
        longest=summary.longest,
        active_today=summary.active_today,
        at_risk=summary.at_risk,
        milestone=MilestoneOut(
            reached=m.reached,
            key=m.key,
            next=m.next,
            next_key=m.next_key,
            days_to_next=m.days_to_next,
        ),
        window_start=start,
        activity=[DayCount(date=d, sessions=n) for d, n in sorted(counts.items())],
    )


class BoardEntry(BaseModel):
    position: int
    display_name: Optional[str]
    sessions: int
    current_streak: int
    is_me: bool


class BoardMe(BaseModel):
    position: int
    sessions: int


class LeaderboardOut(BaseModel):
    week_start: date
    week_end: date
    entries: List[BoardEntry]
    me: Optional[BoardMe] = None
    me_in_top: bool
    opted_in: bool


@router.get("/leaderboard", response_model=LeaderboardOut)
async def leaderboard(user_id: int = Depends(require_user)) -> LeaderboardOut:
    """This week's board. Only opted-in users are on it — an opted-out user is
    absent from the data, not merely hidden — and other users' Telegram ids are
    never sent. The caller's own rank is attached when they are opted in."""
    board = await weekly_board(user_id)
    return LeaderboardOut(
        week_start=board.week_start,
        week_end=board.week_end,
        entries=[
            BoardEntry(
                position=e.position,
                display_name=e.display_name,
                sessions=e.sessions,
                current_streak=e.current_streak,
                is_me=e.user_id == user_id,
            )
            for e in board.entries
        ],
        me=BoardMe(position=board.me.position, sessions=board.me.sessions)
        if board.me is not None
        else None,
        me_in_top=board.me_in_top,
        opted_in=board.opted_in,
    )
