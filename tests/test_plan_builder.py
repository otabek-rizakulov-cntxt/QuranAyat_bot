"""The plan generator (`lib.plan_builder`).

D2's acceptance criterion is exact and is asserted exactly: al-Mulk over
weekdays produces 15 advancing days ending on 67:30, with a consolidation day
at each page boundary and at the surah boundary.

The generator is pure — target, pace, weekday set, start date in; portions out
— which is what lets D1 promise that the preview calendar matches what is later
pushed, day for day. These tests lean on that: they call it twice and compare,
and they never construct a store.
"""

from datetime import date, timedelta

import pytest

from hifz.refs import juz_ref, page_ref, parse_reference, surah_ref
from lib.plan_builder import (
    AUTO_PACE,
    DRILL_PAGE,
    DRILL_RANGE,
    DRILL_SURAH,
    Portion,
    advancing,
    auto_pace,
    build_plan,
    next_scheduled_date,
    to_day_specs,
)
from modules import Quran

WEEKDAYS = [1, 2, 3, 4, 5]
EVERY_DAY = [1, 2, 3, 4, 5, 6, 7]

# 2026-08-03 is a Monday; 2026-08-01 a Saturday.
MONDAY = date(2026, 8, 3)
SATURDAY = date(2026, 8, 1)


def spans(portions):
    """(surah, start, end) of each portion — the shape assertions read best in."""
    return [(p.surah, p.start_ayah, p.end_ayah) for p in portions]


def assert_covers_target_once(target, portions):
    """Advancing days tile the target exactly: no gap, no overlap, no overshoot."""
    steps = advancing(portions)
    assert steps, "a non-empty target must produce at least one advancing day"
    cursor = target.start
    for portion in steps:
        assert (portion.surah, portion.start_ayah) == cursor
        assert portion.start_ayah <= portion.end_ayah
        cursor = Quran.get_next_ayah(portion.surah, portion.end_ayah)
    last = steps[-1]
    assert (last.surah, last.end_ayah) == target.end
    assert sum(p.ayahs for p in steps) == target.count()


def assert_well_formed(target, portions):
    """Invariants every plan must hold, whatever the target or pace."""
    assert_covers_target_once(target, portions)
    dates = [p.scheduled_date for p in portions]
    assert dates == sorted(dates)
    assert len(set(dates)) == len(dates), "one portion per calendar date"
    for portion in portions:
        # Single-surah by construction — `PlanDaySpec` has no room for anything else.
        assert Quran.exists(portion.surah, portion.start_ayah)
        assert Quran.exists(portion.surah, portion.end_ayah)
        assert portion.start_ayah <= portion.end_ayah
        # Nothing is ever drilled outside the target.
        assert target.start <= (portion.surah, portion.start_ayah)
        assert (portion.surah, portion.end_ayah) <= target.end


class TestAlMulkAcceptance:
    """D2: "al-Mulk over weekdays produces 15 days ending exactly at 67:30,
    with a consolidation day at each page and surah boundary"."""

    @pytest.fixture
    def plan(self):
        return build_plan(surah_ref(67), 2, WEEKDAYS, MONDAY)

    def test_fifteen_advancing_days(self, plan):
        assert len(advancing(plan)) == 15

    def test_ends_exactly_at_the_last_ayah(self, plan):
        assert spans(advancing(plan))[-1] == (67, 29, 30)
        assert advancing(plan)[-1].end_ayah == Quran.get_surah_length(67)

    def test_every_advancing_day_is_two_whole_ayahs(self, plan):
        assert all(p.ayahs == 2 for p in advancing(plan))

    def test_advancing_days_tile_the_surah(self, plan):
        assert spans(advancing(plan)) == [(67, a, a + 1) for a in range(1, 31, 2)]

    def test_a_consolidation_day_at_each_page_boundary(self, plan):
        pages = [p for p in plan if p.drill == DRILL_PAGE]
        # Al-Mulk occupies pages 562 (67:1-12) and 563 (67:13-26); page 564 runs
        # on into surah 68, so the plan never finishes it and no page day fires.
        assert [(p.unit, p.surah, p.start_ayah, p.end_ayah) for p in pages] == [
            (562, 67, 1, 12), (563, 67, 13, 26)]

    def test_a_consolidation_day_at_the_surah_boundary(self, plan):
        surahs = [p for p in plan if p.drill == DRILL_SURAH]
        assert [(p.unit, p.surah, p.start_ayah, p.end_ayah) for p in surahs] == [
            (67, 67, 1, 30)]

    def test_consolidation_follows_the_day_that_finished_the_unit(self, plan):
        # The page day sits immediately after the day ending on 67:12, and the
        # surah day immediately after the day ending on 67:30.
        by_index = {i: p for i, p in enumerate(plan)}
        for i, portion in by_index.items():
            if portion.is_consolidation:
                assert by_index[i - 1].end_ayah == portion.end_ayah
                assert not by_index[i - 1].is_consolidation

    def test_the_plan_is_eighteen_calendar_days(self, plan):
        # 15 advancing + 2 page days + 1 surah day, each on its own weekday.
        assert len(plan) == 18
        assert plan[0].scheduled_date == MONDAY
        assert plan[-1].scheduled_date == date(2026, 8, 26)

    def test_every_day_is_a_weekday(self, plan):
        assert all(p.scheduled_date.isoweekday() in WEEKDAYS for p in plan)

    def test_well_formed(self, plan):
        assert_well_formed(surah_ref(67), plan)


class TestAutoPace:
    def test_zero_means_auto(self):
        assert build_plan(surah_ref(67), AUTO_PACE, WEEKDAYS, MONDAY) == \
            build_plan(surah_ref(67), 2, WEEKDAYS, MONDAY)

    def test_al_mulk_auto_paces_to_two_a_day(self):
        # A fifth of a mushaf page: al-Mulk is 30 ayahs over 3 pages.
        assert auto_pace(surah_ref(67)) == 2

    @pytest.mark.parametrize("surah, expected", [
        (1, 1),      # al-Fatihah: 7 ayahs on one page
        (2, 1),      # al-Baqarah: long ayahs, ~6 to a page
        (18, 2),     # al-Kahf
        (36, 3),     # Ya-Sin
        (78, 4),     # an-Naba': 40 short ayahs over 2 pages
        (112, 1),    # al-Ikhlas: 4 ayahs
    ])
    def test_density_based_pace(self, surah, expected):
        assert auto_pace(surah_ref(surah)) == expected

    def test_juz_thirty_auto_paces_to_five(self):
        assert auto_pace(juz_ref(30)) == 5

    def test_pace_never_exceeds_the_target(self):
        tiny = parse_reference("67:1-67:2")
        assert auto_pace(tiny) == 1
        assert len(advancing(build_plan(tiny, AUTO_PACE, EVERY_DAY, MONDAY))) == 2

    def test_auto_pace_is_at_least_one_ayah_everywhere(self):
        for surah in range(1, 115):
            pace = auto_pace(surah_ref(surah))
            assert 1 <= pace <= Quran.get_surah_length(surah)

    def test_a_negative_pace_is_treated_as_auto(self):
        # Defensive: the wizard only ever sends 0 or a positive integer.
        assert build_plan(surah_ref(67), -3, WEEKDAYS, MONDAY) == \
            build_plan(surah_ref(67), AUTO_PACE, WEEKDAYS, MONDAY)

    def test_a_pace_larger_than_the_target_is_clamped(self):
        plan = build_plan(parse_reference("67:1-67:5"), 100, EVERY_DAY, MONDAY)
        assert spans(plan) == [(67, 1, 5)]


class TestCrossSurahTargets:
    def test_juz_thirty_runs_from_78_1_to_114_6(self):
        target = juz_ref(30)
        assert target.as_tuple() == (78, 1, 114, 6)
        plan = build_plan(target, 5, EVERY_DAY, MONDAY)
        assert_well_formed(target, plan)

    def test_juz_thirty_terminates_at_the_end_of_the_quran(self):
        # `get_next_ayah` wraps 114:6 back to 1:1, so a naive loop never ends.
        plan = build_plan(juz_ref(30), 5, EVERY_DAY, MONDAY)
        assert advancing(plan)[-1].as_ref().end == (114, 6)

    def test_no_portion_ever_spans_two_surahs(self):
        # `PlanDaySpec` is single-surah; an advancing day stops at the surah end.
        for portion in build_plan(juz_ref(30), 7, EVERY_DAY, MONDAY):
            assert 1 <= portion.start_ayah <= portion.end_ayah
            assert portion.end_ayah <= Quran.get_surah_length(portion.surah)

    def test_a_range_spanning_surahs(self):
        target = parse_reference("67:1-68:5")
        plan = build_plan(target, 3, WEEKDAYS, MONDAY)
        assert_well_formed(target, plan)
        assert spans(advancing(plan))[-1] == (68, 4, 5)
        # The surah boundary inside the range still earns its consolidation day.
        assert (67, 1, 30) in spans([p for p in plan if p.drill == DRILL_SURAH])

    def test_a_range_starting_mid_surah_and_ending_mid_surah(self):
        target = parse_reference("2:280-3:10")
        plan = build_plan(target, 4, EVERY_DAY, MONDAY)
        assert_well_formed(target, plan)
        assert spans(advancing(plan))[0] == (2, 280, 283)

    def test_a_juz_that_starts_mid_surah(self):
        target = juz_ref(2)          # 2:142 - 2:252
        plan = build_plan(target, 3, EVERY_DAY, MONDAY)
        assert_well_formed(target, plan)
        assert advancing(plan)[0].start_ayah == 142

    def test_a_page_target(self):
        target = page_ref(604)       # 112:1 - 114:6
        plan = build_plan(target, 2, EVERY_DAY, MONDAY)
        assert_well_formed(target, plan)
        assert {p.surah for p in plan} == {112, 113, 114}


class TestSmallAndAwkwardTargets:
    def test_target_smaller_than_one_days_pace(self):
        target = parse_reference("67:1-67:3")
        plan = build_plan(target, 10, WEEKDAYS, MONDAY)
        assert spans(plan) == [(67, 1, 3)]
        assert plan[0].drill == DRILL_RANGE

    def test_a_single_ayah_target(self):
        target = parse_reference("67:5")
        plan = build_plan(target, 5, EVERY_DAY, MONDAY)
        assert spans(plan) == [(67, 5, 5)]

    def test_a_whole_short_surah_in_one_day_gets_no_duplicate_consolidation(self):
        # Drilling 112:1-4 and then "consolidating" over 112:1-4 the next day is
        # the same day twice; a rung is only climbed when it widens.
        plan = build_plan(surah_ref(112), 10, EVERY_DAY, MONDAY)
        assert spans(plan) == [(112, 1, 4)]

    def test_a_target_that_does_not_divide_evenly_ends_short_not_over(self):
        plan = build_plan(surah_ref(67), 4, EVERY_DAY, MONDAY)
        steps = advancing(plan)
        assert [p.ayahs for p in steps] == [4, 4, 4, 4, 4, 4, 4, 2]
        assert spans(steps)[-1] == (67, 29, 30)

    def test_pace_of_one(self):
        target = surah_ref(67)
        plan = build_plan(target, 1, EVERY_DAY, MONDAY)
        assert len(advancing(plan)) == 30
        assert_well_formed(target, plan)

    def test_a_target_ending_mid_page_gets_no_page_day(self):
        # 67:1-67:20 stops inside page 563, which therefore never completes.
        target = parse_reference("67:1-67:20")
        plan = build_plan(target, 2, EVERY_DAY, MONDAY)
        assert [p.unit for p in plan if p.drill == DRILL_PAGE] == [562]
        assert not [p for p in plan if p.drill == DRILL_SURAH]


class TestDayOfWeekFiltering:
    def test_a_start_date_outside_the_set_moves_to_the_next_included_day(self):
        plan = build_plan(surah_ref(67), 2, WEEKDAYS, SATURDAY)
        assert SATURDAY.isoweekday() == 6
        assert plan[0].scheduled_date == MONDAY

    def test_a_start_date_inside_the_set_is_used_as_is(self):
        plan = build_plan(surah_ref(67), 2, WEEKDAYS, MONDAY)
        assert plan[0].scheduled_date == MONDAY

    def test_a_single_day_a_week_spaces_portions_seven_days_apart(self):
        plan = build_plan(surah_ref(67), 10, [5], MONDAY)      # Fridays only
        dates = [p.scheduled_date for p in plan]
        assert all(d.isoweekday() == 5 for d in dates)
        assert all(b - a == timedelta(days=7) for a, b in zip(dates, dates[1:]))

    def test_seven_days_a_week_is_consecutive(self):
        plan = build_plan(surah_ref(67), 2, EVERY_DAY, MONDAY)
        dates = [p.scheduled_date for p in plan]
        assert all(b - a == timedelta(days=1) for a, b in zip(dates, dates[1:]))

    def test_weekend_only(self):
        plan = build_plan(surah_ref(67), 5, [6, 7], MONDAY)
        assert all(p.scheduled_date.isoweekday() in (6, 7) for p in plan)
        assert plan[0].scheduled_date == date(2026, 8, 8)      # the Saturday

    def test_days_are_iso_numbered_monday_is_one(self):
        plan = build_plan(surah_ref(112), 1, [1], MONDAY)
        assert all(p.scheduled_date.weekday() == 0 for p in plan)

    @pytest.mark.parametrize("bad", [[], (), None, [0], [8], [1, 9], [-1]])
    def test_an_impossible_weekday_set_is_rejected(self, bad):
        with pytest.raises(ValueError):
            build_plan(surah_ref(67), 2, bad, MONDAY)

    def test_next_scheduled_date_is_inclusive_of_the_start(self):
        assert next_scheduled_date(MONDAY, WEEKDAYS) == MONDAY
        assert next_scheduled_date(SATURDAY, WEEKDAYS) == MONDAY
        assert next_scheduled_date(SATURDAY, [6]) == SATURDAY
        assert next_scheduled_date(MONDAY, [7]) == date(2026, 8, 9)

    def test_duplicate_days_are_harmless(self):
        assert build_plan(surah_ref(67), 2, [1, 1, 3, 3], MONDAY) == \
            build_plan(surah_ref(67), 2, [1, 3], MONDAY)


class TestConsolidationDays:
    """The widening ladder: range -> mushaf page -> whole surah."""

    def test_a_page_day_always_ends_on_the_last_ayah_of_its_page(self):
        for target in (surah_ref(2), juz_ref(30), surah_ref(36)):
            for portion in build_plan(target, 4, EVERY_DAY, MONDAY):
                if portion.drill == DRILL_PAGE:
                    span = Quran.page_range(portion.unit)
                    assert (span[2], span[3]) == (portion.surah, portion.end_ayah)

    def test_a_surah_day_always_ends_on_the_last_ayah_of_its_surah(self):
        for portion in build_plan(juz_ref(30), 6, EVERY_DAY, MONDAY):
            if portion.drill == DRILL_SURAH:
                assert portion.unit == portion.surah
                assert portion.end_ayah == Quran.get_surah_length(portion.surah)

    def test_a_consolidation_re_drills_covered_ground_and_never_advances(self):
        plan = build_plan(juz_ref(30), 5, EVERY_DAY, MONDAY)
        covered_to = None
        for portion in plan:
            if portion.is_consolidation:
                assert (portion.surah, portion.end_ayah) <= covered_to
                assert portion.ayahs > 1
            else:
                covered_to = (portion.surah, portion.end_ayah)

    def test_a_page_day_is_wider_than_the_day_before_it(self):
        plan = build_plan(surah_ref(36), 3, EVERY_DAY, MONDAY)
        for before, portion in zip(plan, plan[1:]):
            if portion.is_consolidation:
                assert portion.ayahs > before.ayahs

    def test_the_ladder_widens_page_then_surah(self):
        # Surah 66 ends at 66:12, which is also the end of page 561, so both
        # rungs fire on the same day — the page first, then the whole surah.
        plan = build_plan(surah_ref(66), 3, EVERY_DAY, MONDAY)
        tail = [(p.drill, p.start_ayah, p.end_ayah) for p in plan[-2:]]
        assert tail == [(DRILL_PAGE, 8, 12), (DRILL_SURAH, 1, 12)]

    def test_a_page_day_is_clamped_to_the_target(self):
        # The plan never showed the user 67:1-4, so the page day must not either.
        plan = build_plan(parse_reference("67:5-67:30"), 2, EVERY_DAY, MONDAY)
        pages = [(p.unit, p.start_ayah, p.end_ayah)
                 for p in plan if p.drill == DRILL_PAGE]
        assert pages == [(562, 5, 12), (563, 13, 26)]

    def test_a_surah_day_is_clamped_to_the_target(self):
        plan = build_plan(parse_reference("67:5-68:5"), 3, EVERY_DAY, MONDAY)
        surahs = [(p.unit, p.start_ayah, p.end_ayah)
                  for p in plan if p.drill == DRILL_SURAH]
        assert surahs == [(67, 5, 30)]

    def test_a_page_day_straddling_a_surah_is_clamped_to_the_later_surah(self):
        # Page 564 is 67:27-68:15; the plan finishes it inside surah 68, so the
        # page day covers 68:1-15 — one surah, one `plan_day` row.
        plan = build_plan(parse_reference("67:1-68:20"), 5, EVERY_DAY, MONDAY)
        page_564 = [p for p in plan if p.drill == DRILL_PAGE and p.unit == 564]
        assert spans(page_564) == [(68, 1, 15)]

    def test_consolidations_are_extra_days_not_replacements(self):
        plan = build_plan(surah_ref(67), 2, WEEKDAYS, MONDAY)
        assert len(plan) == len(advancing(plan)) + 3

    def test_is_consolidation_flags_exactly_the_two_wider_drills(self):
        plan = build_plan(surah_ref(67), 2, WEEKDAYS, MONDAY)
        for portion in plan:
            assert portion.is_consolidation == (portion.drill != DRILL_RANGE)


class TestPortionShape:
    def test_ayahs_counts_whole_ayahs(self):
        assert Portion(MONDAY, 67, 1, 2).ayahs == 2
        assert Portion(MONDAY, 67, 5, 5).ayahs == 1

    def test_as_ref_round_trips_through_format(self):
        from hifz.refs import format_ref
        assert format_ref(Portion(MONDAY, 67, 1, 12, DRILL_PAGE, 562).as_ref()) \
            == "67:1-12"
        assert format_ref(Portion(MONDAY, 67, 5, 5).as_ref()) == "67:5"

    def test_as_ref_is_a_range_not_a_page_claim(self):
        # A page day is clamped, so labelling its span "page 562" would lie; the
        # page number lives in `unit` instead.
        ref = Portion(MONDAY, 67, 5, 12, DRILL_PAGE, 562).as_ref()
        assert ref.kind == "range" and ref.n is None

    def test_portions_are_immutable(self):
        with pytest.raises(Exception):
            Portion(MONDAY, 67, 1, 2).surah = 68

    def test_default_drill_is_an_advancing_range(self):
        portion = Portion(MONDAY, 67, 1, 2)
        assert portion.drill == DRILL_RANGE and portion.unit is None
        assert not portion.is_consolidation


class TestStorageShape:
    def test_to_day_specs_is_one_row_per_portion(self):
        plan = build_plan(surah_ref(67), 2, WEEKDAYS, MONDAY)
        specs = to_day_specs(plan)
        assert len(specs) == len(plan)
        for spec, portion in zip(specs, plan):
            assert (spec.scheduled_date, spec.surah, spec.start_ayah, spec.end_ayah) \
                == (portion.scheduled_date, portion.surah,
                    portion.start_ayah, portion.end_ayah)

    def test_specs_are_ordered_by_date(self):
        specs = to_day_specs(build_plan(juz_ref(30), 5, WEEKDAYS, SATURDAY))
        dates = [s.scheduled_date for s in specs]
        assert dates == sorted(dates)

    def test_a_cross_surah_target_still_yields_single_surah_rows(self):
        specs = to_day_specs(build_plan(juz_ref(30), 9, EVERY_DAY, MONDAY))
        assert all(Quran.exists(s.surah, s.end_ayah) for s in specs)


class TestPurity:
    def test_the_same_inputs_give_the_same_plan(self):
        args = (juz_ref(30), AUTO_PACE, WEEKDAYS, MONDAY)
        assert build_plan(*args) == build_plan(*args)

    def test_the_target_is_not_mutated(self):
        target = surah_ref(67)
        before = target.as_tuple()
        build_plan(target, 2, WEEKDAYS, MONDAY)
        assert target.as_tuple() == before

    def test_the_weekday_sequence_is_not_mutated(self):
        days = [5, 1, 3]
        build_plan(surah_ref(67), 2, days, MONDAY)
        assert days == [5, 1, 3]

    def test_a_later_start_date_only_shifts_the_calendar(self):
        early = build_plan(surah_ref(67), 2, WEEKDAYS, MONDAY)
        later = build_plan(surah_ref(67), 2, WEEKDAYS, MONDAY + timedelta(days=7))
        assert spans(early) == spans(later)
        assert [p.drill for p in early] == [p.drill for p in later]


class TestAcrossTheWholeQuran:
    """Every surah, every juz — the invariants must not depend on the target."""

    @pytest.mark.parametrize("surah", list(range(1, 115)))
    def test_every_surah_auto_paces_into_a_well_formed_plan(self, surah):
        target = surah_ref(surah)
        assert_well_formed(target, build_plan(target, AUTO_PACE, WEEKDAYS, MONDAY))

    @pytest.mark.parametrize("n", list(range(1, 31)))
    def test_every_juz_auto_paces_into_a_well_formed_plan(self, n):
        target = juz_ref(n)
        assert_well_formed(target, build_plan(target, AUTO_PACE, EVERY_DAY, SATURDAY))

    @pytest.mark.parametrize("pace", [1, 2, 3, 7, 25])
    def test_a_long_surah_at_several_paces(self, pace):
        target = surah_ref(2)
        assert_well_formed(target, build_plan(target, pace, WEEKDAYS, MONDAY))
