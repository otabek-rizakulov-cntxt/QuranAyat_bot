"""Derived hifz percentages (`lib.hifz_progress`), C2.

The spec pins two numbers and this file exists mainly to hold them: marking
67:1-8 must report Al-Mulk **27%**, and re-marking 67:5-10 must report **33%**.
Both are checked end to end through the real interval store, because "33%" is
only correct if the merge worked — two overlapping rows would say 47%, and the
percentage is exactly where that bug would first become visible to a user.

Everything else here defends the property the module is built on: nothing is
stored as a counter, so every number is recomputed from the intervals and cannot
drift. The tests therefore mostly assert *relationships* — the 30 juz partition
the Qur'an, a surah's total equals its corpus length, the whole-Qur'an count is
the sum of the per-surah counts — rather than transcribing expected integers.
"""

import random
from datetime import datetime, timezone

import pytest

from lib.hifz_progress import (
    TOTAL_AYAHS,
    TOTAL_PAGES,
    JuzProgress,
    PageProgress,
    Progress,
    ProgressSummary,
    SurahProgress,
    format_percent,
    juz_page_progress,
    juz_progress,
    load_summary,
    quran_page_progress,
    quran_progress,
    round_percent,
    started_juzs,
    started_surahs,
    summarize,
    surah_progress,
)
from lib.store import get_store
from lib.store.hifz import HifzInterval
from modules import Quran

USER = 1
AL_MULK = 67          # 30 ayahs, juz 29
AL_BAQARAH = 2        # 286 ayahs, spread over juz 1, 2 and 3
AN_NAS = 114          # 6 ayahs, juz 30


def _at(minute: int) -> datetime:
    """A fixed `marked_at`, so "most recent" never depends on the wall clock."""
    return datetime(2026, 7, 31, 12, minute, tzinfo=timezone.utc)


# --- The two numbers the spec names --------------------------------------------

class TestSpecAcceptance:
    async def test_marking_67_1_8_reports_al_mulk_at_27_percent(self):
        store = await get_store()
        await store.hifz.add_interval(USER, AL_MULK, 1, 8)
        progress = surah_progress(await store.hifz.list_intervals(USER), AL_MULK)
        assert (progress.done, progress.total) == (8, 30)      # 26.67%
        assert progress.percent_text == "27"

    async def test_re_marking_67_5_10_reports_33_percent_not_47(self):
        """The merge and the percentage tested as one thing.

        8 ayahs plus 6 ayahs is 14 (47%) if the two marks were stored as separate
        rows, and 10 (33%) if 67:5-10 merged into 67:1-8 the way it must. This
        assertion is the cheapest place in the suite to catch a regression in the
        merge, because it fails with a number a human recognizes as wrong.
        """
        store = await get_store()
        await store.hifz.add_interval(USER, AL_MULK, 1, 8)
        await store.hifz.add_interval(USER, AL_MULK, 5, 10)
        progress = surah_progress(await store.hifz.list_intervals(USER), AL_MULK)
        assert (progress.done, progress.total) == (10, 30)      # 33.33%
        assert progress.percent_text == "33"

    async def test_forgetting_the_middle_lowers_the_percentage_by_exactly_what_was_removed(self):
        store = await get_store()
        await store.hifz.add_interval(USER, AL_MULK, 1, 10)
        await store.hifz.remove_range(USER, AL_MULK, 5, 6)
        progress = surah_progress(await store.hifz.list_intervals(USER), AL_MULK)
        assert (progress.done, progress.total) == (8, 30)
        assert progress.percent_text == "27"


# --- The rounding rule ---------------------------------------------------------

class TestRounding:
    def test_the_spec_percentages_land_on_27_and_33(self):
        assert round_percent(8 / 30) == 27.0
        assert round_percent(10 / 30) == 33.0

    def test_half_rounds_up_not_to_even(self):
        """The builtin `round` is banker's rounding and would answer 26 here.

        26.5% is the kind of number that shows up constantly at these
        denominators, and "rounds down half the time for reasons involving
        floating point parity" is not something a user will ever be told.
        """
        assert round(26.5) == 26            # what we are deliberately not doing
        assert round_percent(0.265) == 27.0
        assert round_percent(0.255) == 26.0

    def test_nothing_memorized_is_zero(self):
        assert round_percent(0) == 0.0
        assert format_percent(0) == "0"

    def test_something_memorized_is_never_reported_as_zero(self):
        """The rule that matters most: a single ayah must not read as 0%.

        One ayah of the Qur'an is 0.016%. Rounding that to "0%" tells someone who
        has genuinely memorized something that they have memorized nothing, which
        is the one output this module must never produce.
        """
        assert round_percent(1 / 6236) == 0.1
        assert round_percent(1 / 1_000_000) == 0.1
        assert format_percent(8 / 6236) == "0.1"
        assert format_percent(10 / 6236) == "0.2"

    def test_below_one_percent_keeps_one_decimal(self):
        assert round_percent(0.004) == 0.4
        assert format_percent(0.004) == "0.4"

    def test_one_hundred_means_finished(self):
        """99.77% of a juz must not be rounded up into a completion claim."""
        assert round_percent(430 / 431) == 99.0
        assert round_percent(6235 / 6236) == 99.0
        assert round_percent(1.0) == 100.0
        assert format_percent(1.0) == "100"

    def test_format_percent_carries_no_percent_sign(self):
        """The sign lives in the locale string, so RTL and "٪" locales can move it."""
        for fraction in (0, 0.001, 0.5, 1.0):
            assert "%" not in format_percent(fraction)


# --- Per-surah -----------------------------------------------------------------

class TestSurahProgress:
    def test_totals_come_from_the_corpus(self):
        for surah in (1, 2, 36, 67, 114):
            assert surah_progress([], surah).total == Quran.get_surah_length(surah)

    def test_a_whole_surah_is_one_hundred_percent(self):
        progress = surah_progress([(AL_MULK, 1, 30)], AL_MULK)
        assert progress.is_complete
        assert progress.percent_text == "100"
        assert progress.remaining == 0

    def test_only_the_asked_for_surah_counts(self):
        intervals = [(AL_MULK, 1, 10), (AL_BAQARAH, 1, 50)]
        assert surah_progress(intervals, AL_MULK).done == 10
        assert surah_progress(intervals, AL_BAQARAH).done == 50

    def test_several_intervals_in_one_surah_add_up(self):
        assert surah_progress([(AL_MULK, 1, 4), (AL_MULK, 10, 15)], AL_MULK).done == 10

    def test_an_unstarted_surah_is_zero_of_its_real_length(self):
        progress = surah_progress([(AL_MULK, 1, 10)], AL_BAQARAH)
        assert (progress.done, progress.total) == (0, 286)
        assert not progress.is_started
        assert progress.remaining == 286

    def test_a_surah_that_does_not_exist_is_zero_of_zero(self):
        """0/0 rather than a crash: `/progress` should not 500 on a bad row."""
        progress = surah_progress([(AL_MULK, 1, 10)], 200)
        assert (progress.done, progress.total) == (0, 0)
        assert progress.fraction == 0.0
        assert progress.percent_text == "0"

    def test_a_row_running_past_the_end_of_its_surah_cannot_exceed_one_hundred(self):
        """Defence in depth against a bad write.

        The store does not know how long a surah is — it holds intervals, not the
        corpus — so nothing there stops a caller storing 67:1-999. Clipping every
        interval to the real surah before counting means the worst such a row can
        do is overstate `count_ayahs`; it can never produce a percentage above 100,
        which is the version a user would actually see and disbelieve.
        """
        progress = surah_progress([(AL_MULK, 1, 999)], AL_MULK)
        assert (progress.done, progress.total) == (30, 30)
        assert progress.percent_text == "100"

    def test_started_surahs_lists_only_started_ones_in_mushaf_order(self):
        intervals = [(AN_NAS, 1, 6), (AL_MULK, 1, 8), (AL_BAQARAH, 1, 3)]
        assert [s.surah for s in started_surahs(intervals)] == [AL_BAQARAH, AL_MULK,
                                                               AN_NAS]

    def test_started_surahs_is_empty_for_a_new_user(self):
        assert started_surahs([]) == []


# --- Per-juz (the cross-surah case) --------------------------------------------

class TestJuzProgress:
    def test_the_thirty_juz_partition_the_quran(self):
        """Nothing double-counted and nothing missed, checked against the corpus."""
        assert sum(juz_progress([], n).total for n in range(1, 31)) == TOTAL_AYAHS

    def test_a_juz_that_starts_mid_surah_only_counts_its_own_share(self):
        """Juz 1 is 1:1-2:141, so memorizing all of Al-Baqarah does not complete it.

        This is the case a per-surah counter cannot express at all, and the reason
        juz progress has to be an intersection rather than a lookup.
        """
        whole_baqarah = [(AL_BAQARAH, 1, 286)]
        first = juz_progress(whole_baqarah, 1)
        assert (first.done, first.total) == (141, 148)     # missing Al-Fatihah's 7
        assert not first.is_complete
        assert juz_progress(whole_baqarah, 2) == JuzProgress(juz=2, done=111, total=111)
        assert juz_progress(whole_baqarah, 3).done == 34   # 2:253-2:286

    def test_a_juz_is_complete_only_when_every_surah_it_touches_is(self):
        intervals = [(1, 1, 7), (AL_BAQARAH, 1, 141)]
        assert juz_progress(intervals, 1).is_complete
        assert juz_progress(intervals, 1).percent_text == "100"

    def test_an_interval_outside_the_juz_contributes_nothing(self):
        assert juz_progress([(AL_MULK, 1, 30)], 1).done == 0
        assert juz_progress([(AL_MULK, 1, 30)], 30).done == 0
        assert juz_progress([(AL_MULK, 1, 30)], 29).done == 30

    def test_an_interval_strictly_inside_a_mid_surah_juz(self):
        """Juz 2 is 2:142-2:252 — both ends of the juz fall inside one surah."""
        assert juz_progress([(AL_BAQARAH, 150, 160)], 2).done == 11
        assert juz_progress([(AL_BAQARAH, 100, 130)], 2).done == 0
        assert juz_progress([(AL_BAQARAH, 130, 150)], 2).done == 9    # 142-150
        assert juz_progress([(AL_BAQARAH, 250, 260)], 2).done == 3    # 250-252

    def test_a_juz_that_does_not_exist_is_zero_of_zero(self):
        assert juz_progress([(AL_MULK, 1, 8)], 0) == JuzProgress(juz=0, done=0, total=0)
        assert juz_progress([(AL_MULK, 1, 8)], 31).total == 0

    def test_started_juzs_lists_only_started_ones_ascending(self):
        intervals = [(AL_MULK, 1, 8), (AL_BAQARAH, 1, 286)]
        assert [j.juz for j in started_juzs(intervals)] == [1, 2, 3, 29]

    def test_started_juzs_is_empty_for_a_new_user(self):
        assert started_juzs([]) == []


# --- Whole Qur'an --------------------------------------------------------------

class TestQuranProgress:
    def test_the_total_is_the_corpus_size(self):
        assert TOTAL_AYAHS == 6236
        assert quran_progress([]).total == 6236
        assert quran_progress([]).percent_text == "0"

    def test_memorizing_everything_is_one_hundred_percent(self):
        everything = [(surah, 1, Quran.get_surah_length(surah))
                      for surah in range(1, 115)]
        progress = quran_progress(everything)
        assert (progress.done, progress.total) == (6236, 6236)
        assert progress.percent_text == "100"

    def test_it_equals_the_sum_of_the_surahs_and_of_the_juz(self):
        """Three routes to the same number; if they ever disagree, one is wrong."""
        intervals = [(1, 1, 7), (AL_BAQARAH, 100, 200), (AL_MULK, 1, 8),
                     (AN_NAS, 1, 6)]
        total = quran_progress(intervals).done
        assert sum(s.done for s in started_surahs(intervals)) == total
        assert sum(juz_progress(intervals, n).done for n in range(1, 31)) == total

    @pytest.mark.parametrize("seed", [1, 2, 3, 4, 5])
    def test_the_three_routes_agree_for_random_interval_sets(self, seed):
        """The partition property, fuzzed.

        A juz boundary that fell in the wrong place, or a clip that was off by one
        at a surah edge, would show up as the juz sum drifting from the surah sum
        — and only for intervals that happen to straddle that boundary, which is
        exactly what a handful of hand-written cases would miss.
        """
        rng = random.Random(seed)
        intervals = []
        for _ in range(12):
            surah = rng.randint(1, 114)
            length = Quran.get_surah_length(surah)
            start = rng.randint(1, length)
            intervals.append((surah, start, min(length, start + rng.randint(0, 120))))
        # De-overlap by surah so the sums are comparable (the store guarantees this).
        merged = {}
        for surah, start, end in intervals:
            low, high = merged.get(surah, (start, end))
            merged[surah] = (min(low, start), max(high, end))
        spans = [(surah, start, end) for surah, (start, end) in merged.items()]

        total = quran_progress(spans).done
        assert sum(s.done for s in started_surahs(spans)) == total
        assert sum(juz_progress(spans, n).done for n in range(1, 31)) == total


# --- The summary `/progress` renders -------------------------------------------

class TestSummarize:
    def test_it_carries_every_number_the_motivation_line_needs(self):
        """"Al-Mulk 8/30 · 27% · juz 29 4% · Qur'an 0.4%" as structured data.

        The renderer supplies the surah name, the separators and the percent sign
        from the string table; everything numeric in that line comes from here.
        """
        summary = summarize([(AL_MULK, 1, 8)])
        assert summary.focus == SurahProgress(surah=67, done=8, total=30)
        assert summary.focus.percent_text == "27"
        assert summary.focus_juz.juz == 29
        assert summary.quran == Progress(done=8, total=6236)
        assert summary.quran.percent_text == "0.1"
        assert not summary.is_empty

    def test_no_string_in_the_summary_is_a_sentence(self):
        """Guards the Wave 2A contract: nothing here is pre-formatted prose."""
        summary = summarize([(AL_MULK, 1, 8)])
        assert isinstance(summary, ProgressSummary)
        for value in (summary.quran, summary.focus, summary.focus_juz):
            assert not isinstance(value, str)
        assert all(isinstance(s, SurahProgress) for s in summary.surahs)
        assert all(isinstance(j, JuzProgress) for j in summary.juzs)

    def test_an_empty_summary_is_flagged_rather_than_faked(self):
        summary = summarize([])
        assert summary.is_empty
        assert summary.focus is None and summary.focus_juz is None
        assert summary.surahs == () and summary.juzs == ()
        assert summary.quran == Progress(done=0, total=6236)

    def test_the_breakdown_only_lists_what_was_started(self):
        summary = summarize([(AL_MULK, 1, 8), (AN_NAS, 1, 6)])
        assert [s.surah for s in summary.surahs] == [AL_MULK, AN_NAS]
        assert [j.juz for j in summary.juzs] == [29, 30]

    def test_an_explicit_focus_wins_over_the_most_recent_mark(self):
        summary = summarize([(AL_MULK, 1, 8), (AN_NAS, 1, 6)], focus_surah=AN_NAS)
        assert summary.focus.surah == AN_NAS
        assert summary.focus_juz.juz == 30

    def test_a_focus_on_an_unstarted_surah_still_reports_it(self):
        """`/progress 2` after only marking Al-Mulk should say "0/286", not nothing."""
        summary = summarize([(AL_MULK, 1, 8)], focus_surah=AL_BAQARAH)
        assert summary.focus == SurahProgress(surah=2, done=0, total=286)
        assert summary.focus_juz is None      # no marked ayah to locate a juz from

    def test_a_focus_on_a_surah_that_does_not_exist_is_dropped(self):
        summary = summarize([(AL_MULK, 1, 8)], focus_surah=999)
        assert summary.focus is None

    def test_the_focus_juz_is_the_one_the_last_marked_ayah_sits_in(self):
        """Al-Baqarah spans three juz; the line should name the one being worked on."""
        assert summarize([(AL_BAQARAH, 1, 100)]).focus_juz.juz == 1
        assert summarize([(AL_BAQARAH, 1, 200)]).focus_juz.juz == 2
        assert summarize([(AL_BAQARAH, 1, 286)]).focus_juz.juz == 3

    def test_the_focus_defaults_to_the_most_recently_marked_surah(self):
        """What the user just worked on is what the line should lead with."""
        older = HifzInterval(1, USER, AL_BAQARAH, 1, 20, _at(9))
        newer = HifzInterval(2, USER, AL_MULK, 1, 8, _at(10))
        assert summarize([older, newer]).focus.surah == AL_MULK
        assert summarize([newer, older]).focus.surah == AL_MULK    # order-independent

    def test_identical_timestamps_break_toward_the_higher_row_id(self):
        """The clock is only good to a microsecond and ties are common.

        Two marks inside one handler routinely land on the same `marked_at`; if
        that were the only term, which surah `/progress` led with would depend on
        how busy the machine was. Both store legs mint ids from a monotonic
        sequence and every merge inserts a fresh row, so the higher id is reliably
        the later write.
        """
        stamp = _at(10)
        first = HifzInterval(1, USER, AL_BAQARAH, 1, 20, stamp)
        second = HifzInterval(2, USER, AL_MULK, 1, 8, stamp)
        assert summarize([first, second]).focus.surah == AL_MULK
        assert summarize([second, first]).focus.surah == AL_MULK

    async def test_the_focus_follows_the_user_through_the_real_store(self):
        """End to end: the last surah written is the one the summary leads with."""
        store = await get_store()
        await store.hifz.add_interval(USER, AL_BAQARAH, 1, 20)
        await store.hifz.add_interval(USER, AL_MULK, 1, 8)
        assert summarize(await store.hifz.list_intervals(USER)).focus.surah == AL_MULK

        await store.hifz.add_interval(USER, AL_BAQARAH, 21, 30)
        assert summarize(await store.hifz.list_intervals(USER)).focus.surah == AL_BAQARAH

    async def test_forgetting_does_not_move_the_focus(self):
        """`/forgot` is not progress, and the focus follows progress.

        A split deliberately carries the original `marked_at` onto both halves —
        forgetting the middle of a page does not re-date the edges — so the surah
        that was last *learned* keeps the line, even though the split minted newer
        rows in another surah. `/forgot` gets its own confirmation message; it does
        not need to hijack the motivation line as well.
        """
        store = await get_store()
        await store.hifz.add_interval(USER, AL_BAQARAH, 1, 20)
        await store.hifz.add_interval(USER, AL_MULK, 1, 8)
        await store.hifz.remove_range(USER, AL_BAQARAH, 5, 6)
        assert summarize(await store.hifz.list_intervals(USER)).focus.surah == AL_MULK


# --- Reading it straight out of the store ---------------------------------------

class TestLoadSummary:
    async def test_it_summarizes_everything_the_user_has_marked(self):
        store = await get_store()
        await store.hifz.add_interval(USER, AL_MULK, 1, 8)
        await store.hifz.add_interval(USER, AN_NAS, 1, 6)
        summary = await load_summary(store, USER)
        assert summary.quran.done == 14
        assert [s.surah for s in summary.surahs] == [AL_MULK, AN_NAS]

    async def test_a_user_with_nothing_marked_gets_an_empty_summary(self):
        store = await get_store()
        assert (await load_summary(store, 999)).is_empty

    async def test_one_users_progress_is_not_another_users(self):
        store = await get_store()
        await store.hifz.add_interval(1, AL_MULK, 1, 30)
        await store.hifz.add_interval(2, AL_MULK, 1, 3)
        assert (await load_summary(store, 1)).quran.done == 30
        assert (await load_summary(store, 2)).quran.done == 3

    async def test_the_focus_can_be_pinned_to_the_active_plans_target(self):
        store = await get_store()
        await store.hifz.add_interval(USER, AN_NAS, 1, 6)
        summary = await load_summary(store, USER, focus_surah=AL_MULK)
        assert summary.focus == SurahProgress(surah=67, done=0, total=30)


# --- Input shapes ---------------------------------------------------------------

class TestInputHandling:
    async def test_store_rows_and_plain_tuples_give_the_same_answer(self):
        """Tuples are accepted so a plan preview can be costed before it is saved."""
        store = await get_store()
        await store.hifz.add_interval(USER, AL_MULK, 1, 8)
        rows = await store.hifz.list_intervals(USER)
        assert surah_progress(rows, AL_MULK) == surah_progress([(AL_MULK, 1, 8)],
                                                               AL_MULK)

    def test_a_reversed_tuple_is_normalized_rather_than_counted_as_nothing(self):
        assert surah_progress([(AL_MULK, 8, 1)], AL_MULK).done == 8

    def test_none_and_empty_are_both_a_blank_slate(self):
        assert quran_progress(None).done == 0
        assert quran_progress([]).done == 0
        assert summarize(None).is_empty


# --- Counting in pages ----------------------------------------------------------
# The surah figure is quoted in ayahs because that is how a surah is learned; the
# juz and whole-Qur'an figures are quoted in mushaf pages because that is how a
# hafiz measures them. A juz is "twenty pages", never "431 ayahs".

class TestPageProgress:
    def test_a_juz_is_about_twenty_pages(self):
        """604 pages over 30 juz averages 20.1, and none strays far from it.

        Juz 30 is the real outlier at 23 pages: it is the short surahs, which
        start a new page far more often than a page of Al-Baqarah does. That is a
        property of the mushaf, not of this arithmetic, so it is asserted rather
        than smoothed away.
        """
        totals = [juz_page_progress([], j).total_pages for j in range(1, 31)]
        for juz, total in enumerate(totals, start=1):
            assert 19 <= total <= 23, (juz, total)
        assert round(sum(totals) / 30, 1) == 20.1
        assert totals[29] == max(totals)      # juz 30, the longest in pages

    def test_juz_29_is_exactly_twenty_pages(self):
        assert juz_page_progress([], 29).total_pages == 20.0

    def test_the_thirty_juz_totals_sum_to_the_whole_mushaf(self):
        """A page straddling a juz boundary is shared, not double-counted.

        Counting such a page whole in both juz would make the thirty totals add up
        to more than the mushaf — the arithmetic would be quietly inflating every
        boundary juz.
        """
        total = sum(juz_page_progress([], j).total_pages for j in range(1, 31))
        assert round(total, 6) == float(TOTAL_PAGES)

    def test_pages_are_fractional_within_a_page(self):
        """Two thirds of a page is two thirds of a page, not 0 and not 1."""
        # page 562 is 67:1-12, so eight ayahs is 8/12 of it
        eight = quran_page_progress([(67, 1, 8)])
        assert 0.6 < eight.done_pages < 0.7
        assert eight.is_started

    def test_pages_and_ayahs_disagree_which_is_the_whole_point(self):
        """Juz 29's ayahs are short and its pages are not."""
        by_ayah = juz_progress([(67, 1, 8)], 29)
        by_page = juz_page_progress([(67, 1, 8)], 29)
        assert by_page.fraction > by_ayah.fraction

    def test_a_finished_juz_reads_one_hundred(self):
        whole = _whole_quran_spans()
        assert juz_page_progress(whole, 30).percent == 100.0
        assert juz_page_progress(whole, 30).is_complete

    def test_a_finished_quran_reads_one_hundred(self):
        done = quran_page_progress(_whole_quran_spans())
        assert round(done.done_pages, 6) == float(TOTAL_PAGES)
        assert done.percent == 100.0
        assert done.is_complete

    def test_nothing_memorized_is_zero_not_a_division_error(self):
        blank = quran_page_progress([])
        assert blank.done_pages == 0.0
        assert blank.percent == 0.0
        assert blank.is_started is False
        assert blank.total_pages == float(TOTAL_PAGES)

    def test_a_started_page_is_never_reported_as_zero_percent(self):
        """The floor that stops "0%" being shown to someone who has begun."""
        one_ayah = quran_page_progress([(2, 255, 255)])
        assert one_ayah.is_started
        assert one_ayah.percent > 0
        assert one_ayah.percent_text != "0"

    def test_page_progress_never_exceeds_one_hundred(self):
        """A row running past the end of its surah must not inflate the total."""
        assert quran_page_progress([(67, 1, 999)]).percent <= 100.0
        assert juz_page_progress([(67, 1, 999)], 29).percent <= 100.0

    def test_an_unreal_juz_is_empty_rather_than_an_error(self):
        for bad in (0, 31, 99):
            empty = juz_page_progress([(67, 1, 8)], bad)
            assert empty.total_pages == 0.0
            assert empty.fraction == 0.0

    def test_pages_text_is_a_bare_token(self):
        assert quran_page_progress([]).pages_text == "0"
        assert "%" not in quran_page_progress([(67, 1, 8)]).pages_text

    def test_summary_carries_both_units(self):
        summary = summarize([(67, 1, 8)])
        assert summary.focus.done == 8 and summary.focus.total == 30
        assert summary.focus.percent_text == "27"          # ayahs, per the done-when
        assert isinstance(summary.quran_pages, PageProgress)
        assert isinstance(summary.focus_juz_pages, PageProgress)
        assert summary.focus_juz_pages.total_pages == 20.0  # juz 29
        # the ayah-based readings survive for the breakdown
        assert summary.quran.total == TOTAL_AYAHS

    def test_a_blank_summary_still_has_page_figures(self):
        summary = summarize([])
        assert summary.is_empty
        assert summary.quran_pages.percent == 0.0
        assert summary.focus_juz_pages is None


def _whole_quran_spans():
    return [(s, 1, Quran.get_surah_length(s)) for s in range(1, 115)]
