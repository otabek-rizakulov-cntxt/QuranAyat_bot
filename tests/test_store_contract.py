"""One contract, two implementations (`lib.store`).

Every test in this file runs twice: once against `InMemoryStore` and once against
`PostgresStore`. That is the entire point of the file — the in-memory store is
what `pytest`, local dev and any deployment without DATABASE_URL actually use, so
nothing stops it drifting away from the SQL one except a suite that refuses to
let them answer differently.

The SQL leg **skips** unless `TEST_DATABASE_URL` points at a throwaway Postgres
(CI has none). It applies `src/common/schema.sql` and truncates every table it
owns before each test, so pointing it at a database with real data would be a
very bad idea.
"""

import os
from datetime import date, datetime, time, timedelta, timezone

import pytest

from lib.store import InMemoryStore, PostgresStore
from lib.store.plans import (
    DAY_COMPLETED,
    DAY_PENDING,
    DAY_SENT,
    PLAN_ACTIVE,
    PLAN_COMPLETE,
    PLAN_PAUSED,
    PlanDaySpec,
)
from lib.store.schedule import STATE_CLAIMED, STATE_FAILED, STATE_PENDING, STATE_SENT
from lib.store.sessions import KIND_DRILL, KIND_RECALL_CHECK

# Child-first, so the plan_day -> plan foreign key never blocks the truncate.
_TABLES = ("scheduled_send", "session_log", "plan_day", "plan", "hifz_interval",
           "user_profile", "user_settings")

UTC = timezone.utc


@pytest.fixture(params=["memory", "postgres"])
async def store(request):
    """The store under test, one parametrization per implementation."""
    if request.param == "memory":
        yield InMemoryStore()
        return

    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL is not set — no Postgres to run the SQL leg against")

    import asyncpg

    pool = await asyncpg.create_pool(url, min_size=1, max_size=4, command_timeout=10,
                                     statement_cache_size=0)
    try:
        sql_store = PostgresStore(pool)
        await sql_store.apply_schema()
        await pool.execute("TRUNCATE %s RESTART IDENTITY CASCADE" % ", ".join(_TABLES))
        yield sql_store
    finally:
        await pool.close()


def _spans(intervals):
    return [(i.surah, i.start_ayah, i.end_ayah) for i in intervals]


async def _make_plan(store, user_id=1, days=None, status=PLAN_ACTIVE):
    return await store.plans.create_plan(
        user_id=user_id, target_kind="surah", start_surah=67, start_ayah=1,
        end_surah=67, end_ayah=30, pace=2, days_of_week=[1, 2, 3, 4, 5],
        days=days if days is not None else [
            PlanDaySpec(date(2026, 8, 3), 67, 1, 2),
            PlanDaySpec(date(2026, 8, 4), 67, 3, 4),
            PlanDaySpec(date(2026, 8, 5), 67, 5, 6),
        ],
        status=status)


class TestSettings:
    async def test_unknown_user_has_no_settings_row(self, store):
        assert await store.profiles.get_settings(1) is None

    async def test_ensure_inserts_and_returns_the_row(self, store):
        row = await store.profiles.ensure_settings_row(1, "ru", "tr", "Alafasy_128kbps")
        assert (row.telegram_user_id, row.ui_lang, row.translation_lang, row.reciter) == (
            1, "ru", "tr", "Alafasy_128kbps")
        assert (await store.profiles.get_settings(1)).ui_lang == "ru"

    async def test_ensure_returns_none_when_the_row_already_exists(self, store):
        await store.profiles.ensure_settings_row(1, "ru", "ru", "Husary_128kbps")
        # The "you lost the insert race" signal the legacy Redis migration reads.
        assert await store.profiles.ensure_settings_row(1, "fr", "fr", "x") is None
        assert (await store.profiles.get_settings(1)).ui_lang == "ru"

    async def test_each_setting_round_trips_independently(self, store):
        await store.profiles.ensure_settings_row(1, "en", "en", "Husary_128kbps")
        await store.profiles.set_ui_lang(1, "uz-Cyrl")
        await store.profiles.set_translation_lang(1, "ru")
        await store.profiles.set_reciter(1, "Alafasy_128kbps")
        row = await store.profiles.get_settings(1)
        assert (row.ui_lang, row.translation_lang, row.reciter) == (
            "uz-Cyrl", "ru", "Alafasy_128kbps")

    async def test_setters_are_a_no_op_when_the_row_is_missing(self, store):
        # UPDATE ... WHERE telegram_user_id = $1 matches nothing; the in-memory
        # store must not helpfully invent a row where SQL would not.
        await store.profiles.set_ui_lang(404, "ru")
        assert await store.profiles.get_settings(404) is None

    async def test_settings_are_per_user(self, store):
        await store.profiles.ensure_settings_row(1, "ru", "ru", "Husary_128kbps")
        await store.profiles.ensure_settings_row(2, "fr", "fr", "Husary_128kbps")
        await store.profiles.set_ui_lang(1, "tr")
        assert (await store.profiles.get_settings(2)).ui_lang == "fr"

    async def test_returned_rows_are_snapshots(self, store):
        row = await store.profiles.ensure_settings_row(1, "en", "en", "Husary_128kbps")
        row.ui_lang = "mutated"
        assert (await store.profiles.get_settings(1)).ui_lang == "en"


class TestProfiles:
    async def test_unknown_user_has_no_profile(self, store):
        assert await store.profiles.get_profile(1) is None

    async def test_ensure_creates_an_all_defaults_profile(self, store):
        profile = await store.profiles.ensure_profile(1)
        assert profile.telegram_user_id == 1
        assert profile.display_name is None
        assert profile.leaderboard_opt_in is False
        assert profile.timezone is None
        assert profile.reminder_time is None
        assert (profile.current_streak, profile.longest_streak) == (0, 0)

    async def test_ensure_is_idempotent(self, store):
        await store.profiles.set_display_name(1, "Abu Bakr")
        again = await store.profiles.ensure_profile(1)
        assert again.display_name == "Abu Bakr"

    async def test_display_name_round_trips_and_can_be_cleared(self, store):
        await store.profiles.set_display_name(1, "Abu Bakr")
        assert (await store.profiles.get_profile(1)).display_name == "Abu Bakr"
        await store.profiles.set_display_name(1, None)
        assert (await store.profiles.get_profile(1)).display_name is None

    async def test_leaderboard_opt_in_round_trips(self, store):
        assert (await store.profiles.set_leaderboard_opt_in(1, True)).leaderboard_opt_in
        assert not (await store.profiles.set_leaderboard_opt_in(1, False)).leaderboard_opt_in

    async def test_timezone_is_a_fixed_utc_offset_string(self, store):
        await store.profiles.set_timezone(1, "+05:00")
        assert (await store.profiles.get_profile(1)).timezone == "+05:00"

    async def test_reminder_time_round_trips(self, store):
        await store.profiles.set_reminder_time(1, time(6, 30))
        assert (await store.profiles.get_profile(1)).reminder_time == time(6, 30)

    async def test_streaks_round_trip(self, store):
        profile = await store.profiles.set_streaks(1, 7, 42)
        assert (profile.current_streak, profile.longest_streak) == (7, 42)
        assert (await store.profiles.get_profile(1)).longest_streak == 42

    async def test_setters_create_the_profile_when_it_is_missing(self, store):
        await store.profiles.set_timezone(9, "+03:00")
        assert (await store.profiles.get_profile(9)).timezone == "+03:00"

    async def test_setters_leave_the_other_columns_alone(self, store):
        await store.profiles.set_display_name(1, "Abu Bakr")
        await store.profiles.set_streaks(1, 3, 3)
        await store.profiles.set_reminder_time(1, time(21, 0))
        profile = await store.profiles.get_profile(1)
        assert profile.display_name == "Abu Bakr"
        assert profile.current_streak == 3
        assert profile.reminder_time == time(21, 0)

    async def test_list_reminder_profiles_skips_users_without_one(self, store):
        await store.profiles.set_reminder_time(2, time(6, 0))
        await store.profiles.ensure_profile(1)
        await store.profiles.set_reminder_time(3, time(7, 0))
        assert [p.telegram_user_id for p in await store.profiles.list_reminder_profiles()] == [2, 3]


class TestHifzIntervals:
    async def test_marking_a_range_stores_it(self, store):
        await store.hifz.add_interval(1, 67, 1, 8)
        assert _spans(await store.hifz.list_intervals(1)) == [(67, 1, 8)]

    async def test_partial_overlap_merges(self, store):
        await store.hifz.add_interval(1, 67, 1, 8)
        merged = await store.hifz.add_interval(1, 67, 5, 10)
        assert (merged.start_ayah, merged.end_ayah) == (1, 10)
        assert _spans(await store.hifz.list_intervals(1)) == [(67, 1, 10)]

    async def test_adjacent_ranges_coalesce(self, store):
        await store.hifz.add_interval(1, 67, 1, 8)
        await store.hifz.add_interval(1, 67, 9, 10)
        assert _spans(await store.hifz.list_intervals(1)) == [(67, 1, 10)]

    async def test_containment_is_a_no_op(self, store):
        first = await store.hifz.add_interval(1, 67, 1, 10)
        again = await store.hifz.add_interval(1, 67, 3, 5)
        assert (again.start_ayah, again.end_ayah) == (1, 10)
        assert again.id == first.id            # the covering row survives untouched
        assert _spans(await store.hifz.list_intervals(1)) == [(67, 1, 10)]

    async def test_a_bridging_range_absorbs_several_intervals(self, store):
        await store.hifz.add_interval(1, 67, 1, 3)
        await store.hifz.add_interval(1, 67, 7, 9)
        await store.hifz.add_interval(1, 67, 12, 14)
        await store.hifz.add_interval(1, 67, 2, 13)
        assert _spans(await store.hifz.list_intervals(1)) == [(67, 1, 14)]

    async def test_disjoint_ranges_stay_separate(self, store):
        await store.hifz.add_interval(1, 67, 1, 3)
        await store.hifz.add_interval(1, 67, 10, 12)
        assert _spans(await store.hifz.list_intervals(1)) == [(67, 1, 3), (67, 10, 12)]

    async def test_reversed_endpoints_are_normalized(self, store):
        await store.hifz.add_interval(1, 67, 8, 1)
        assert _spans(await store.hifz.list_intervals(1)) == [(67, 1, 8)]

    async def test_intervals_are_per_user_and_per_surah(self, store):
        await store.hifz.add_interval(1, 67, 1, 5)
        await store.hifz.add_interval(1, 36, 1, 5)
        await store.hifz.add_interval(2, 67, 1, 5)
        assert _spans(await store.hifz.list_intervals(1)) == [(36, 1, 5), (67, 1, 5)]
        assert _spans(await store.hifz.list_intervals(1, surah=67)) == [(67, 1, 5)]

    async def test_count_ayahs_sums_the_spans(self, store):
        await store.hifz.add_interval(1, 67, 1, 8)
        await store.hifz.add_interval(1, 36, 1, 2)
        assert await store.hifz.count_ayahs(1) == 10
        assert await store.hifz.count_ayahs(1, surah=67) == 8
        assert await store.hifz.count_ayahs(2) == 0

    async def test_removing_the_middle_splits_the_interval(self, store):
        await store.hifz.add_interval(1, 67, 1, 10)
        left_right = await store.hifz.remove_range(1, 67, 5, 6)
        assert [(i.start_ayah, i.end_ayah) for i in left_right] == [(1, 4), (7, 10)]
        assert _spans(await store.hifz.list_intervals(1)) == [(67, 1, 4), (67, 7, 10)]

    async def test_removing_a_head_trims(self, store):
        await store.hifz.add_interval(1, 67, 1, 10)
        await store.hifz.remove_range(1, 67, 1, 4)
        assert _spans(await store.hifz.list_intervals(1)) == [(67, 5, 10)]

    async def test_removing_a_tail_trims(self, store):
        await store.hifz.add_interval(1, 67, 1, 10)
        await store.hifz.remove_range(1, 67, 7, 30)
        assert _spans(await store.hifz.list_intervals(1)) == [(67, 1, 6)]

    async def test_removing_everything_leaves_nothing(self, store):
        await store.hifz.add_interval(1, 67, 1, 10)
        assert await store.hifz.remove_range(1, 67, 1, 30) == []
        assert await store.hifz.list_intervals(1) == []

    async def test_removing_across_several_intervals(self, store):
        await store.hifz.add_interval(1, 67, 1, 5)
        await store.hifz.add_interval(1, 67, 10, 15)
        await store.hifz.remove_range(1, 67, 4, 11)
        assert _spans(await store.hifz.list_intervals(1)) == [(67, 1, 3), (67, 12, 15)]

    async def test_removing_an_unmarked_range_changes_nothing(self, store):
        await store.hifz.add_interval(1, 67, 1, 5)
        assert await store.hifz.remove_range(1, 67, 20, 25) == []
        assert _spans(await store.hifz.list_intervals(1)) == [(67, 1, 5)]

    async def test_removing_does_not_touch_another_users_intervals(self, store):
        await store.hifz.add_interval(1, 67, 1, 10)
        await store.hifz.add_interval(2, 67, 1, 10)
        await store.hifz.remove_range(1, 67, 1, 10)
        assert _spans(await store.hifz.list_intervals(2)) == [(67, 1, 10)]


class TestPlans:
    async def test_create_plan_writes_the_plan_and_its_days(self, store):
        plan = await _make_plan(store)
        assert plan.user_id == 1
        assert plan.target_kind == "surah"
        assert plan.days_of_week == [1, 2, 3, 4, 5]
        assert plan.pace == 2
        assert plan.status == PLAN_ACTIVE
        days = await store.plans.list_plan_days(plan.id)
        assert [(d.scheduled_date, d.surah, d.start_ayah, d.end_ayah, d.state) for d in days] == [
            (date(2026, 8, 3), 67, 1, 2, DAY_PENDING),
            (date(2026, 8, 4), 67, 3, 4, DAY_PENDING),
            (date(2026, 8, 5), 67, 5, 6, DAY_PENDING),
        ]

    async def test_a_plan_with_no_days_is_allowed(self, store):
        plan = await _make_plan(store, days=[])
        assert await store.plans.list_plan_days(plan.id) == []

    async def test_get_plan_and_missing_plan(self, store):
        plan = await _make_plan(store)
        assert (await store.plans.get_plan(plan.id)).id == plan.id
        assert await store.plans.get_plan(plan.id + 10_000) is None

    async def test_get_active_plan(self, store):
        assert await store.plans.get_active_plan(1) is None
        plan = await _make_plan(store)
        assert (await store.plans.get_active_plan(1)).id == plan.id

    async def test_a_paused_plan_is_not_the_active_one(self, store):
        plan = await _make_plan(store)
        await store.plans.set_plan_status(plan.id, PLAN_PAUSED)
        assert await store.plans.get_active_plan(1) is None
        assert (await store.plans.get_plan(plan.id)).status == PLAN_PAUSED

    async def test_set_plan_status_on_a_missing_plan_returns_none(self, store):
        assert await store.plans.set_plan_status(999_999, PLAN_COMPLETE) is None

    async def test_list_plans_is_newest_first_and_filterable(self, store):
        first = await _make_plan(store, days=[])
        await store.plans.set_plan_status(first.id, PLAN_COMPLETE)
        second = await _make_plan(store, days=[])
        assert [p.id for p in await store.plans.list_plans(1)] == [second.id, first.id]
        assert [p.id for p in await store.plans.list_plans(1, PLAN_COMPLETE)] == [first.id]

    async def test_plans_are_per_user(self, store):
        await _make_plan(store, user_id=1, days=[])
        assert await store.plans.get_active_plan(2) is None

    async def test_list_plan_days_filters_by_state_and_date(self, store):
        plan = await _make_plan(store)
        days = await store.plans.list_plan_days(plan.id)
        await store.plans.claim_plan_day(days[0].id)
        assert len(await store.plans.list_plan_days(plan.id, state=DAY_PENDING)) == 2
        assert len(await store.plans.list_plan_days(plan.id, state=DAY_SENT)) == 1
        due = await store.plans.list_plan_days(plan.id, on_or_before=date(2026, 8, 4))
        assert [d.scheduled_date for d in due] == [date(2026, 8, 3), date(2026, 8, 4)]

    async def test_get_plan_day(self, store):
        plan = await _make_plan(store)
        day = (await store.plans.list_plan_days(plan.id))[0]
        assert (await store.plans.get_plan_day(day.id)).start_ayah == 1
        assert await store.plans.get_plan_day(day.id + 10_000) is None

    async def test_claiming_a_day_succeeds_exactly_once(self, store):
        plan = await _make_plan(store)
        day = (await store.plans.list_plan_days(plan.id))[0]
        claimed = await store.plans.claim_plan_day(day.id)
        assert claimed is not None and claimed.state == DAY_SENT
        assert await store.plans.claim_plan_day(day.id) is None

    async def test_claiming_a_missing_day_returns_none(self, store):
        assert await store.plans.claim_plan_day(999_999) is None

    async def test_completing_a_day_succeeds_exactly_once(self, store):
        plan = await _make_plan(store)
        day = (await store.plans.list_plan_days(plan.id))[0]
        completed = await store.plans.complete_plan_day(day.id)
        assert completed is not None and completed.state == DAY_COMPLETED
        # A second tap on "I know this by heart" must not re-fire anything.
        assert await store.plans.complete_plan_day(day.id) is None

    async def test_a_day_can_be_completed_without_being_claimed_first(self, store):
        plan = await _make_plan(store)
        day = (await store.plans.list_plan_days(plan.id))[0]
        assert (await store.plans.complete_plan_day(day.id)).state == DAY_COMPLETED

    async def test_count_plan_days(self, store):
        plan = await _make_plan(store)
        days = await store.plans.list_plan_days(plan.id)
        await store.plans.complete_plan_day(days[0].id)
        assert await store.plans.count_plan_days(plan.id) == 3
        assert await store.plans.count_plan_days(plan.id, DAY_COMPLETED) == 1
        assert await store.plans.count_plan_days(plan.id, DAY_PENDING) == 2


class TestSessions:
    async def test_logging_a_session_returns_the_row(self, store):
        row = await store.sessions.log_session(1, date(2026, 8, 3), KIND_DRILL, 67, 1, 8)
        assert (row.user_id, row.local_date, row.kind) == (1, date(2026, 8, 3), KIND_DRILL)
        assert (row.surah, row.start_ayah, row.end_ayah) == (67, 1, 8)
        assert row.occurred_at is not None

    async def test_the_same_session_twice_logs_once(self, store):
        await store.sessions.log_session(1, date(2026, 8, 3), KIND_DRILL, 67, 1, 8)
        assert await store.sessions.log_session(1, date(2026, 8, 3), KIND_DRILL, 67, 1, 8) is None
        assert await store.sessions.count_sessions(1, date(2026, 8, 3), date(2026, 8, 3)) == 1

    async def test_a_portionless_session_also_dedupes(self, store):
        # NULL portion columns must still collide — that is why the unique index
        # COALESCEs them.
        assert await store.sessions.log_session(1, date(2026, 8, 3), KIND_RECALL_CHECK) is not None
        assert await store.sessions.log_session(1, date(2026, 8, 3), KIND_RECALL_CHECK) is None

    async def test_a_different_kind_portion_or_day_is_a_different_session(self, store):
        day = date(2026, 8, 3)
        assert await store.sessions.log_session(1, day, KIND_DRILL, 67, 1, 8) is not None
        assert await store.sessions.log_session(1, day, KIND_RECALL_CHECK, 67, 1, 8) is not None
        assert await store.sessions.log_session(1, day, KIND_DRILL, 67, 9, 10) is not None
        assert await store.sessions.log_session(1, day + timedelta(days=1), KIND_DRILL,
                                                67, 1, 8) is not None
        assert await store.sessions.count_sessions(1, day, day + timedelta(days=1)) == 4

    async def test_list_active_dates_is_distinct_and_sorted(self, store):
        await store.sessions.log_session(1, date(2026, 8, 4), KIND_DRILL, 67, 1, 2)
        await store.sessions.log_session(1, date(2026, 8, 3), KIND_DRILL, 67, 3, 4)
        await store.sessions.log_session(1, date(2026, 8, 3), KIND_RECALL_CHECK, 67, 3, 4)
        assert await store.sessions.list_active_dates(1) == [date(2026, 8, 3), date(2026, 8, 4)]

    async def test_list_active_dates_windows(self, store):
        for day in (1, 5, 9):
            await store.sessions.log_session(1, date(2026, 8, day), KIND_DRILL, 67, 1, 2)
        assert await store.sessions.list_active_dates(
            1, since=date(2026, 8, 2), until=date(2026, 8, 8)) == [date(2026, 8, 5)]

    async def test_list_sessions_windows_and_orders(self, store):
        await store.sessions.log_session(1, date(2026, 8, 5), KIND_DRILL, 67, 1, 2)
        await store.sessions.log_session(1, date(2026, 8, 3), KIND_DRILL, 67, 3, 4)
        rows = await store.sessions.list_sessions(1, date(2026, 8, 3), date(2026, 8, 5))
        assert [r.local_date for r in rows] == [date(2026, 8, 3), date(2026, 8, 5)]

    async def test_count_sessions_excludes_the_outside_of_the_window(self, store):
        for day in (2, 3, 4):
            await store.sessions.log_session(1, date(2026, 8, day), KIND_DRILL, 67, 1, 2)
        assert await store.sessions.count_sessions(1, date(2026, 8, 3), date(2026, 8, 3)) == 1
        assert await store.sessions.count_sessions(1, date(2026, 8, 2), date(2026, 8, 4)) == 3

    async def test_sessions_are_per_user(self, store):
        await store.sessions.log_session(1, date(2026, 8, 3), KIND_DRILL, 67, 1, 2)
        assert await store.sessions.list_active_dates(2) == []


class TestLeaderboard:
    """`H1 — done when: an opted-out user is absent from the query result, not
    merely hidden in rendering.`"""

    WEEK = (date(2026, 8, 3), date(2026, 8, 9))

    async def _seed(self, store, user_id, name, sessions, streak=0, opted_in=True):
        await store.profiles.set_display_name(user_id, name)
        await store.profiles.set_leaderboard_opt_in(user_id, opted_in)
        await store.profiles.set_streaks(user_id, streak, streak)
        for n in range(sessions):
            await store.sessions.log_session(user_id, date(2026, 8, 3), KIND_DRILL,
                                             67, n + 1, n + 1)

    async def test_empty_board(self, store):
        assert await store.sessions.weekly_leaderboard(*self.WEEK) == []

    async def test_board_is_ordered_by_sessions_then_streak(self, store):
        await self._seed(store, 1, "one", sessions=2, streak=1)
        await self._seed(store, 2, "two", sessions=5, streak=1)
        await self._seed(store, 3, "three", sessions=2, streak=9)
        board = await store.sessions.weekly_leaderboard(*self.WEEK)
        assert [(e.user_id, e.sessions, e.position) for e in board] == [
            (2, 5, 1), (3, 2, 2), (1, 2, 3)]
        assert board[0].display_name == "two"
        assert board[1].current_streak == 9

    async def test_opted_out_users_are_absent(self, store):
        await self._seed(store, 1, "one", sessions=3, opted_in=True)
        await self._seed(store, 2, "two", sessions=9, opted_in=False)
        board = await store.sessions.weekly_leaderboard(*self.WEEK)
        assert [e.user_id for e in board] == [1]

    async def test_a_user_with_no_profile_is_absent(self, store):
        await store.sessions.log_session(7, date(2026, 8, 3), KIND_DRILL, 67, 1, 2)
        assert await store.sessions.weekly_leaderboard(*self.WEEK) == []

    async def test_sessions_outside_the_week_do_not_count(self, store):
        await self._seed(store, 1, "one", sessions=2)
        await store.sessions.log_session(1, date(2026, 7, 20), KIND_DRILL, 67, 1, 2)
        board = await store.sessions.weekly_leaderboard(*self.WEEK)
        assert board[0].sessions == 2

    async def test_limit_truncates_the_board(self, store):
        for user_id in range(1, 6):
            await self._seed(store, user_id, "u%d" % user_id, sessions=user_id)
        board = await store.sessions.weekly_leaderboard(*self.WEEK, limit=2)
        assert [e.user_id for e in board] == [5, 4]

    async def test_weekly_rank_finds_a_user_outside_the_top(self, store):
        for user_id in range(1, 6):
            await self._seed(store, user_id, "u%d" % user_id, sessions=user_id)
        entry = await store.sessions.weekly_rank(1, *self.WEEK)
        assert (entry.user_id, entry.sessions, entry.position) == (1, 1, 5)

    async def test_weekly_rank_is_none_for_an_opted_out_user(self, store):
        await self._seed(store, 1, "one", sessions=3, opted_in=False)
        assert await store.sessions.weekly_rank(1, *self.WEEK) is None

    async def test_weekly_rank_is_none_without_sessions(self, store):
        await self._seed(store, 1, "one", sessions=0)
        assert await store.sessions.weekly_rank(1, *self.WEEK) is None


class TestSchedule:
    NOW = datetime(2026, 8, 3, 6, 0, tzinfo=UTC)

    async def test_enqueue_returns_the_row(self, store):
        row = await store.schedule.enqueue(
            "plan_day", 4242, self.NOW, "plan_day:4242:2026-08-03",
            payload={"plan_day_id": 7}, thread_id=11)
        assert (row.kind, row.target_chat_id, row.thread_id) == ("plan_day", 4242, 11)
        assert row.due_at == self.NOW
        assert row.payload == {"plan_day_id": 7}
        assert row.state == STATE_PENDING
        assert row.claimed_at is None

    async def test_enqueue_defaults_to_an_empty_payload(self, store):
        row = await store.schedule.enqueue("weekly_board", 1, self.NOW, "wb:1")
        assert row.payload == {}
        assert row.thread_id is None

    async def test_the_same_idempotency_key_inserts_once_and_raises_nothing(self, store):
        first = await store.schedule.enqueue("plan_day", 1, self.NOW, "k")
        assert await store.schedule.enqueue("plan_day", 1, self.NOW, "k") is None
        assert (await store.schedule.get_by_key("k")).id == first.id

    async def test_get_and_get_by_key(self, store):
        row = await store.schedule.enqueue("plan_day", 1, self.NOW, "k")
        assert (await store.schedule.get(row.id)).idempotency_key == "k"
        assert (await store.schedule.get_by_key("k")).id == row.id
        assert await store.schedule.get(999_999) is None
        assert await store.schedule.get_by_key("nope") is None

    async def test_claim_due_takes_only_what_is_due(self, store):
        due = await store.schedule.enqueue("plan_day", 1, self.NOW - timedelta(minutes=1), "a")
        await store.schedule.enqueue("plan_day", 2, self.NOW + timedelta(hours=1), "b")
        claimed = await store.schedule.claim_due(self.NOW)
        assert [c.id for c in claimed] == [due.id]
        assert claimed[0].state == STATE_CLAIMED
        assert claimed[0].claimed_at is not None
        assert (await store.schedule.get_by_key("b")).state == STATE_PENDING

    async def test_claim_due_is_oldest_first_and_respects_the_limit(self, store):
        for n in (3, 1, 2):
            await store.schedule.enqueue("plan_day", n, self.NOW - timedelta(minutes=n), str(n))
        claimed = await store.schedule.claim_due(self.NOW, limit=2)
        assert [c.idempotency_key for c in claimed] == ["3", "2"]

    async def test_a_claimed_row_is_not_claimed_twice(self, store):
        await store.schedule.enqueue("plan_day", 1, self.NOW, "a")
        assert len(await store.schedule.claim_due(self.NOW)) == 1
        assert await store.schedule.claim_due(self.NOW) == []

    async def test_mark_sent_and_mark_failed(self, store):
        row = await store.schedule.enqueue("plan_day", 1, self.NOW, "a")
        assert (await store.schedule.mark_sent(row.id)).state == STATE_SENT
        assert (await store.schedule.mark_failed(row.id)).state == STATE_FAILED
        assert await store.schedule.mark_sent(999_999) is None

    async def test_a_sent_row_is_never_claimed_again(self, store):
        row = await store.schedule.enqueue("plan_day", 1, self.NOW - timedelta(hours=1), "a")
        await store.schedule.mark_sent(row.id)
        assert await store.schedule.claim_due(self.NOW) == []

    async def test_release_stale_claims_requeues_a_crashed_claim(self, store):
        await store.schedule.enqueue("plan_day", 1, self.NOW - timedelta(hours=2), "a")
        await store.schedule.claim_due(self.NOW)
        assert await store.schedule.release_stale_claims(
            datetime.now(UTC) + timedelta(minutes=1)) == 1
        assert (await store.schedule.get_by_key("a")).state == STATE_PENDING
        assert len(await store.schedule.claim_due(self.NOW)) == 1

    async def test_release_stale_claims_leaves_a_fresh_claim_alone(self, store):
        await store.schedule.enqueue("plan_day", 1, self.NOW - timedelta(hours=2), "a")
        await store.schedule.claim_due(self.NOW)
        assert await store.schedule.release_stale_claims(
            datetime.now(UTC) - timedelta(hours=1)) == 0
        assert (await store.schedule.get_by_key("a")).state == STATE_CLAIMED

    async def test_drop_stale_removes_windows_that_are_no_longer_relevant(self, store):
        await store.schedule.enqueue("plan_day", 1, self.NOW - timedelta(days=1), "old")
        await store.schedule.enqueue("plan_day", 2, self.NOW, "fresh")
        assert await store.schedule.drop_stale(self.NOW - timedelta(hours=6)) == 1
        assert await store.schedule.get_by_key("old") is None
        assert await store.schedule.get_by_key("fresh") is not None

    async def test_drop_stale_leaves_already_sent_rows_alone(self, store):
        row = await store.schedule.enqueue("plan_day", 1, self.NOW - timedelta(days=1), "old")
        await store.schedule.mark_sent(row.id)
        assert await store.schedule.drop_stale(self.NOW) == 0
        assert (await store.schedule.get_by_key("old")).state == STATE_SENT
