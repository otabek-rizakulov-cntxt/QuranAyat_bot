"""The weekly board (H1) and the composition H2 renders.

Two properties carry the workstream: the week window is the *viewer's* week, and
an opted-out user is absent from the aggregation itself — not filtered out on the
way to the screen.
"""

from datetime import date, datetime, timedelta, timezone

from lib.leaderboard import DEFAULT_LIMIT, weekly_board, week_window
from lib.store import get_store
from lib.store.sessions import KIND_DRILL

MONDAY = date(2026, 3, 16)
SUNDAY = date(2026, 3, 22)


async def make_user(user_id, sessions=0, opt_in=True, streak=0, tz="+00:00",
                    name=None, day=None):
    """A profile plus `sessions` sessions in the current week."""
    store = await get_store()
    await store.profiles.set_timezone(user_id, tz)
    await store.profiles.set_leaderboard_opt_in(user_id, opt_in)
    await store.profiles.set_display_name(user_id, name or ("user%d" % user_id))
    await store.profiles.set_streaks(user_id, streak, streak)
    for n in range(sessions):
        # Distinct portions so the store's idempotence does not collapse them.
        await store.sessions.log_session(user_id, day or MONDAY, KIND_DRILL,
                                         surah=1, start_ayah=1, end_ayah=n + 1)
    return store


class TestWeekWindow:
    def test_the_window_is_monday_to_sunday_inclusive(self):
        assert week_window(datetime(2026, 3, 18, 12, 0, tzinfo=timezone.utc),
                           "+00:00") == (MONDAY, SUNDAY)

    def test_two_offsets_can_disagree_about_which_week_it_is(self):
        # 22:00 UTC on Sunday: still Sunday in London, already Monday in Tashkent.
        instant = datetime(2026, 3, 22, 22, 0, tzinfo=timezone.utc)
        assert week_window(instant, "+00:00") == (MONDAY, SUNDAY)
        assert week_window(instant, "+05:00") == (MONDAY + timedelta(days=7),
                                                  SUNDAY + timedelta(days=7))

    def test_a_western_offset_can_still_be_in_the_previous_week(self):
        # 01:00 UTC on Monday is still Sunday evening in New York.
        instant = datetime(2026, 3, 23, 1, 0, tzinfo=timezone.utc)
        assert week_window(instant, "+00:00") == (MONDAY + timedelta(days=7),
                                                  SUNDAY + timedelta(days=7))
        assert week_window(instant, "-05:00") == (MONDAY, SUNDAY)


class TestWeeklyBoard:
    NOW = datetime(2026, 3, 18, 12, 0, tzinfo=timezone.utc)      # Wednesday

    async def test_an_empty_week_is_an_empty_board(self):
        await make_user(1)
        board = await weekly_board(1, utc_now=self.NOW)
        assert board.entries == ()
        assert board.me is None
        assert (board.week_start, board.week_end) == (MONDAY, SUNDAY)

    async def test_the_board_is_ordered_by_sessions_then_streak(self):
        await make_user(1, sessions=2, streak=1)
        await make_user(2, sessions=5, streak=3)
        await make_user(3, sessions=5, streak=90)
        board = await weekly_board(1, utc_now=self.NOW)
        assert [e.user_id for e in board.entries] == [3, 2, 1]
        assert [e.position for e in board.entries] == [1, 2, 3]

    async def test_an_opted_out_user_is_absent_from_the_query_result(self):
        await make_user(1, sessions=1)
        await make_user(2, sessions=99, opt_in=False)             # would be first
        board = await weekly_board(1, utc_now=self.NOW)
        assert [e.user_id for e in board.entries] == [1]
        assert all(e.user_id != 2 for e in board.entries)

    async def test_an_opted_out_viewer_sees_the_board_but_no_own_row(self):
        await make_user(1, sessions=3, opt_in=False)
        await make_user(2, sessions=1)
        board = await weekly_board(1, utc_now=self.NOW)
        assert [e.user_id for e in board.entries] == [2]
        assert board.me is None
        assert board.opted_in is False

    async def test_the_viewer_inside_the_top_n_is_marked_as_such(self):
        await make_user(1, sessions=4)
        await make_user(2, sessions=1)
        board = await weekly_board(1, utc_now=self.NOW)
        assert board.me_in_top is True
        assert board.me.position == 1
        assert board.me == board.entries[0]

    async def test_a_user_outside_the_top_n_still_gets_a_rank(self):
        # 12 users ahead of the viewer, so they are 13th on a board of 10.
        for user_id in range(2, 14):
            await make_user(user_id, sessions=10)
        await make_user(1, sessions=1)
        board = await weekly_board(1, utc_now=self.NOW)
        assert len(board.entries) == DEFAULT_LIMIT
        assert all(e.user_id != 1 for e in board.entries)
        assert board.me_in_top is False
        assert board.me is not None
        assert board.me.position == 13
        assert board.me.sessions == 1

    async def test_a_viewer_with_no_sessions_has_no_row(self):
        await make_user(1, sessions=0)
        await make_user(2, sessions=2)
        board = await weekly_board(1, utc_now=self.NOW)
        assert board.me is None
        assert board.opted_in is True

    async def test_last_weeks_sessions_do_not_count(self):
        await make_user(1, sessions=3, day=MONDAY - timedelta(days=1))   # last Sunday
        board = await weekly_board(1, utc_now=self.NOW)
        assert board.entries == ()

    async def test_a_sunday_session_counts_and_the_next_monday_does_not(self):
        await make_user(1, sessions=1, day=SUNDAY)
        await make_user(2, sessions=1, day=SUNDAY + timedelta(days=1))
        board = await weekly_board(1, utc_now=self.NOW)
        assert [e.user_id for e in board.entries] == [1]

    async def test_the_window_follows_the_viewers_own_offset(self):
        # One session on Monday 2026-03-23. At 22:00 UTC on Sunday the 22nd the
        # UTC+5 viewer is already in that week; the UTC viewer is not.
        instant = datetime(2026, 3, 22, 22, 0, tzinfo=timezone.utc)
        await make_user(1, sessions=1, tz="+05:00", day=MONDAY + timedelta(days=7))
        await make_user(2, sessions=0, tz="+00:00")
        assert (await weekly_board(1, utc_now=instant)).week_start == MONDAY + timedelta(days=7)
        assert (await weekly_board(2, utc_now=instant)).week_start == MONDAY
        assert [e.user_id for e in (await weekly_board(1, utc_now=instant)).entries] == [1]
        assert (await weekly_board(2, utc_now=instant)).entries == ()

    async def test_the_limit_is_honoured(self):
        for user_id in range(1, 6):
            await make_user(user_id, sessions=user_id)
        board = await weekly_board(1, utc_now=self.NOW, limit=2)
        assert len(board.entries) == 2
        assert board.me.user_id == 1
        assert board.me.position == 5
        assert board.me_in_top is False

    async def test_an_unknown_viewer_still_gets_the_board(self):
        await make_user(2, sessions=1)
        board = await weekly_board(777, utc_now=self.NOW)
        assert [e.user_id for e in board.entries] == [2]
        assert board.me is None
        assert board.opted_in is False
