"""Streak arithmetic (G1) and milestone/percentile copy (G3).

The pure-function tests are where the day boundary is pinned down; the async
tests check that a session logged through `record_session` lands on the user's
*local* day and leaves the denormalized counters on `user_profile` correct.
"""

from datetime import date, datetime, timedelta, timezone

from lib.store import get_store
from lib.store.sessions import KIND_DRILL, KIND_RECALL_CHECK
from lib.streaks import (
    GRACE_DAYS,
    MILESTONE_DAYS,
    PERCENTILE_MIN_USERS,
    compute_streak,
    milestone_for,
    percentile_band,
    record_session,
    refresh_streaks,
    streak_summary,
)

TODAY = date(2026, 3, 18)                       # a Wednesday


def days_back(*offsets):
    """Active dates expressed as "n days before TODAY"."""
    return [TODAY - timedelta(days=n) for n in offsets]


class TestComputeStreak:
    def test_no_history_is_a_zero_streak(self):
        counts = compute_streak([], TODAY)
        assert (counts.current, counts.longest, counts.last_active) == (0, 0, None)
        assert counts.active_today is False

    def test_a_single_day_today_is_a_streak_of_one(self):
        counts = compute_streak(days_back(0), TODAY)
        assert (counts.current, counts.longest) == (1, 1)
        assert counts.active_today is True

    def test_two_sessions_on_the_same_local_date_tick_once(self):
        # The store de-duplicates distinct dates; passing the same date twice must
        # not be able to inflate the count either.
        assert compute_streak([TODAY, TODAY], TODAY).current == 1

    def test_consecutive_days_accumulate(self):
        assert compute_streak(days_back(0, 1, 2, 3), TODAY).current == 4

    def test_a_gap_breaks_the_streak(self):
        # active 6,5,4 days ago then nothing until today: the run is today alone.
        counts = compute_streak(days_back(6, 5, 4, 0), TODAY)
        assert counts.current == 1
        assert counts.longest == 3

    def test_a_streak_ending_yesterday_is_still_current(self):
        # The day is not over; the user can still save it. It reads 3, not 4 —
        # grace never *extends* the count.
        counts = compute_streak(days_back(3, 2, 1), TODAY)
        assert counts.current == 3
        assert counts.active_today is False

    def test_a_streak_ending_two_days_ago_is_broken(self):
        counts = compute_streak(days_back(4, 3, 2), TODAY)
        assert counts.current == 0
        assert counts.longest == 3
        assert counts.last_active == TODAY - timedelta(days=2)

    def test_the_grace_window_is_exactly_one_day(self):
        for gap in range(0, 4):
            counts = compute_streak(days_back(gap), TODAY)
            assert (counts.current > 0) is (gap <= GRACE_DAYS), gap

    def test_longest_survives_a_break(self):
        counts = compute_streak(days_back(30, 29, 28, 27, 26, 1, 0), TODAY)
        assert counts.current == 2
        assert counts.longest == 5

    def test_dates_may_arrive_unsorted_and_duplicated(self):
        messy = days_back(2, 0, 1, 2, 0)
        assert compute_streak(messy, TODAY).current == 3

    def test_a_future_date_counts_as_today(self):
        # Only reachable by moving one's UTC offset far east mid-streak; it must
        # not read as a gap.
        counts = compute_streak([TODAY, TODAY + timedelta(days=1)], TODAY)
        assert counts.current == 2
        assert counts.active_today is True


class TestMilestones:
    def test_a_milestone_is_reached_only_on_the_exact_day(self):
        assert milestone_for(7).reached == 7
        assert milestone_for(8).reached is None
        assert milestone_for(6).reached is None

    def test_every_fixed_milestone_fires(self):
        for days in MILESTONE_DAYS:
            assert milestone_for(days).reached == days

    def test_the_identifier_is_a_key_not_prose(self):
        milestone = milestone_for(30)
        assert milestone.key == "streak_milestone_30"
        assert milestone.next == 100
        assert milestone.next_key == "streak_milestone_100"
        assert milestone.days_to_next == 70

    def test_past_the_last_milestone_there_is_no_next(self):
        milestone = milestone_for(400)
        assert milestone.reached is None
        assert milestone.next is None
        assert milestone.days_to_next is None

    def test_a_zero_streak_still_points_at_the_first_milestone(self):
        assert milestone_for(0).next == 7


class TestPercentile:
    def test_no_population_means_no_claim(self):
        assert percentile_band(500) is None

    def test_below_the_threshold_no_percentile_is_ever_produced(self):
        # Every streak length, against a population one user short of the gate.
        population = list(range(1, PERCENTILE_MIN_USERS))
        assert len(population) == PERCENTILE_MIN_USERS - 1
        for streak in (1, 7, 30, 100, 365, 10_000):
            assert percentile_band(streak, population) is None

    def test_users_without_a_streak_do_not_count_towards_the_threshold(self):
        # 199 real streaks padded with zeros stays dark: the assumption says
        # "200 users have a streak", not "200 rows exist".
        population = [1] * (PERCENTILE_MIN_USERS - 1) + [0] * 50
        assert percentile_band(5, population) is None

    def test_at_the_threshold_a_band_appears(self):
        population = [1] * (PERCENTILE_MIN_USERS - 1) + [500]
        assert percentile_band(500, population) == 1

    def test_the_band_widens_as_the_streak_shortens(self):
        population = list(range(1, PERCENTILE_MIN_USERS + 1))     # 200 users, 1..200
        assert percentile_band(200, population) == 1              # nobody ahead
        assert percentile_band(180, population) == 10             # 20 ahead -> 10%
        assert percentile_band(101, population) == 50             # 99 ahead -> 49.5%

    def test_the_bottom_half_gets_no_line(self):
        population = list(range(1, PERCENTILE_MIN_USERS + 1))
        assert percentile_band(50, population) is None

    def test_a_zero_streak_never_gets_a_line(self):
        assert percentile_band(0, [1] * 1000) is None


class TestRecordSession:
    """The async path: local dates, denormalization, idempotence."""

    async def _profile(self, user_id, offset="+05:00"):
        store = await get_store()
        await store.profiles.set_timezone(user_id, offset)
        return store

    async def test_a_session_lands_on_the_users_local_date(self):
        await self._profile(1, "+05:00")
        # 20:30 UTC is already the next day at UTC+5.
        outcome = await record_session(
            1, KIND_DRILL, utc_now=datetime(2026, 3, 17, 20, 30, tzinfo=timezone.utc))
        assert outcome.local_date == date(2026, 3, 18)
        assert outcome.logged is True
        assert outcome.streak.current == 1

    async def test_two_sessions_on_one_local_date_tick_the_streak_once(self):
        await self._profile(1, "+05:00")
        morning = datetime(2026, 3, 18, 4, 0, tzinfo=timezone.utc)     # 09:00 local
        evening = datetime(2026, 3, 18, 15, 0, tzinfo=timezone.utc)    # 20:00 local
        first = await record_session(1, KIND_DRILL, utc_now=morning)
        second = await record_session(1, KIND_RECALL_CHECK, utc_now=evening)
        assert first.local_date == second.local_date
        assert second.streak.current == 1

    async def test_2359_then_0001_local_ticks_the_streak_twice(self):
        await self._profile(1, "+05:00")
        # 18:59 UTC = 23:59 local; 19:01 UTC = 00:01 local the next day.
        before = await record_session(
            1, KIND_DRILL, utc_now=datetime(2026, 3, 17, 18, 59, tzinfo=timezone.utc))
        after = await record_session(
            1, KIND_DRILL, utc_now=datetime(2026, 3, 17, 19, 1, tzinfo=timezone.utc))
        assert before.local_date == date(2026, 3, 17)
        assert after.local_date == date(2026, 3, 18)
        assert before.streak.current == 1
        assert after.streak.current == 2

    async def test_the_same_two_minutes_are_one_day_for_a_utc_user(self):
        await self._profile(2, "+00:00")
        first = await record_session(
            2, KIND_DRILL, utc_now=datetime(2026, 3, 17, 18, 59, tzinfo=timezone.utc))
        second = await record_session(
            2, KIND_DRILL, utc_now=datetime(2026, 3, 17, 19, 1, tzinfo=timezone.utc))
        assert first.local_date == second.local_date
        assert second.streak.current == 1

    async def test_a_duplicate_session_is_reported_but_still_counts_once(self):
        await self._profile(1)
        when = datetime(2026, 3, 18, 6, 0, tzinfo=timezone.utc)
        first = await record_session(1, KIND_DRILL, utc_now=when, surah=2,
                                     start_ayah=1, end_ayah=5)
        second = await record_session(1, KIND_DRILL, utc_now=when, surah=2,
                                      start_ayah=1, end_ayah=5)
        assert first.logged is True
        assert second.logged is False
        assert second.streak.current == 1

    async def test_the_counters_are_denormalized_onto_the_profile(self):
        store = await self._profile(1, "+00:00")
        for day in range(3):
            await record_session(
                1, KIND_DRILL,
                utc_now=datetime(2026, 3, 16 + day, 9, 0, tzinfo=timezone.utc))
        profile = await store.profiles.get_profile(1)
        assert (profile.current_streak, profile.longest_streak) == (3, 3)

    async def test_a_missing_profile_falls_back_to_utc(self):
        outcome = await record_session(
            99, KIND_DRILL, utc_now=datetime(2026, 3, 18, 23, 0, tzinfo=timezone.utc))
        assert outcome.local_date == date(2026, 3, 18)

    async def test_an_unparseable_stored_offset_falls_back_to_utc(self):
        store = await get_store()
        await store.profiles.set_timezone(1, "Mars/Olympus")
        outcome = await record_session(
            1, KIND_DRILL, utc_now=datetime(2026, 3, 18, 23, 0, tzinfo=timezone.utc))
        assert outcome.local_date == date(2026, 3, 18)

    async def test_a_milestone_comes_back_with_the_outcome(self):
        store = await get_store()
        await store.profiles.set_timezone(1, "+00:00")
        for day in range(7):
            outcome = await record_session(
                1, KIND_DRILL,
                utc_now=datetime(2026, 3, 12 + day, 9, 0, tzinfo=timezone.utc))
        assert outcome.streak.current == 7
        assert outcome.milestone.reached == 7
        assert outcome.milestone.key == "streak_milestone_7"


class TestRefreshAndSummary:
    async def _log(self, user_id, *offsets, tz="+00:00"):
        store = await get_store()
        await store.profiles.set_timezone(user_id, tz)
        for n in offsets:
            await store.sessions.log_session(user_id, TODAY - timedelta(days=n), KIND_DRILL)
        return store

    async def test_refresh_writes_both_counters(self):
        store = await self._log(1, 5, 4, 3, 1, 0)
        counts = await refresh_streaks(1, today=TODAY)
        assert (counts.current, counts.longest) == (2, 3)
        profile = await store.profiles.get_profile(1)
        assert (profile.current_streak, profile.longest_streak) == (2, 3)

    async def test_longest_survives_a_break_in_storage(self):
        store = await self._log(1, 10, 9, 8, 7, 6)
        await refresh_streaks(1, today=TODAY)
        profile = await store.profiles.get_profile(1)
        assert profile.current_streak == 0            # broken: last active 6 days ago
        assert profile.longest_streak == 5            # but the record stands

    async def test_a_stored_longest_is_never_lowered(self):
        store = await self._log(1, 0)
        await store.profiles.set_streaks(1, 0, 42)
        counts = await refresh_streaks(1, today=TODAY)
        assert counts.longest == 42
        assert (await store.profiles.get_profile(1)).longest_streak == 42

    async def test_summary_reports_a_live_streak_as_at_risk_before_today(self):
        await self._log(1, 2, 1)
        await refresh_streaks(1, today=TODAY)
        summary = await streak_summary(
            1, utc_now=datetime(TODAY.year, TODAY.month, TODAY.day, 9, 0,
                                tzinfo=timezone.utc))
        assert summary.current == 2
        assert summary.active_today is False
        assert summary.at_risk is True
        assert summary.percentile is None

    async def test_summary_is_not_at_risk_once_today_is_earned(self):
        await self._log(1, 1, 0)
        await refresh_streaks(1, today=TODAY)
        summary = await streak_summary(
            1, utc_now=datetime(TODAY.year, TODAY.month, TODAY.day, 9, 0,
                                tzinfo=timezone.utc))
        assert summary.active_today is True
        assert summary.at_risk is False

    async def test_summary_of_an_unknown_user_is_all_zeros(self):
        summary = await streak_summary(4242)
        assert (summary.current, summary.longest) == (0, 0)
        assert summary.at_risk is False
        assert summary.milestone.next == 7
        assert summary.percentile is None

    async def test_no_percentile_with_a_small_user_base(self):
        # The end-to-end version of G3's acceptance criterion: even handed the
        # whole (small) population, the summary renders no claim.
        store = await self._log(1, 1, 0)
        await refresh_streaks(1, today=TODAY)
        population = []
        for user_id in range(2, 60):
            await store.profiles.set_streaks(user_id, 1, 1)
            population.append(1)
        summary = await streak_summary(1, population=population)
        assert summary.percentile is None
