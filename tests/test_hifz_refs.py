"""Cross-surah reference parsing (`hifz.refs`).

The reader's `main.parse_ayah_range` is single-surah by construction, which is
right for a verse card and wrong for a hifz target: a `range` plan may span
surahs, and every juz target does. This module parses into a normalized
(start_surah, start_ayah, end_surah, end_ayah) and validates both ends exist.

`parse_ayah_range` itself must stay untouched — it is pinned by
tests/test_parsing.py and by every reader path in main.py.
"""

import pytest

from hifz.refs import (
    KIND_JUZ,
    KIND_PAGE,
    KIND_RANGE,
    KIND_SURAH,
    ayah_count,
    clamp_to_quran,
    contains,
    format_ref,
    juz_ref,
    page_ref,
    parse_range,
    parse_reference,
    surah_ref,
)
from modules import Quran

AL_MULK = 67          # 30 ayahs
AL_QALAM = 68         # 52 ayahs


class TestWholeSurah:
    def test_bare_number_is_the_whole_surah(self):
        ref = parse_reference("67")
        assert ref.kind == KIND_SURAH
        assert ref.as_tuple() == (67, 1, 67, 30)
        assert ref.n == 67

    def test_surah_ref_matches_the_corpus_length(self):
        for surah in (1, 2, 67, 114):
            ref = surah_ref(surah)
            assert ref.end_ayah == Quran.get_surah_length(surah)
            assert ref.start_ayah == 1

    @pytest.mark.parametrize("bad", [0, 115, 999, -1])
    def test_out_of_range_surah_is_none(self, bad):
        assert surah_ref(bad) is None
        assert parse_reference(str(bad)) is None


class TestWithinOneSurah:
    def test_simple_range(self):
        assert parse_reference("67:1-8").as_tuple() == (67, 1, 67, 8)

    def test_single_ayah_is_a_degenerate_range(self):
        ref = parse_reference("67:5")
        assert ref.as_tuple() == (67, 5, 67, 5)
        assert ref.count() == 1

    @pytest.mark.parametrize("text", ["67:1-8", "67.1-8", "67;1-8", "67,1-8",
                                      "67 1-8", "67:1 - 8", "/67:1-8"])
    def test_separator_and_whitespace_tolerance(self, text):
        assert parse_reference(text).as_tuple() == (67, 1, 67, 8)

    @pytest.mark.parametrize("dash", ["-", "–", "—"])
    def test_en_and_em_dashes(self, dash):
        assert parse_reference("67:1%s8" % dash).as_tuple() == (67, 1, 67, 8)

    def test_reversed_range_is_swapped_not_rejected(self):
        assert parse_reference("67:8-1").as_tuple() == (67, 1, 67, 8)

    def test_ayah_past_the_end_of_the_surah_is_rejected(self):
        # Al-Mulk has 30 ayahs
        assert parse_reference("67:1-31") is None
        assert parse_reference("67:31") is None


class TestAcrossSurahs:
    """The reason this module exists."""

    def test_cross_surah_range(self):
        ref = parse_reference("67:1-68:5")
        assert ref.kind == KIND_RANGE
        assert ref.as_tuple() == (67, 1, 68, 5)
        assert ref.is_single_surah() is False

    def test_the_reader_parser_cannot_express_this(self):
        from main import parse_ayah_range
        # main's parser reads "67:1-68:5" as surah 67 ayahs 1..68 — wrong, and
        # exactly why hifz has its own. Pinning it here so the difference is
        # deliberate rather than discovered later.
        assert parse_ayah_range("67:1-68:5")[0] == 67
        assert parse_reference("67:1-68:5").end_surah == 68

    def test_reversed_cross_surah_range_is_swapped(self):
        assert parse_reference("68:5-67:1").as_tuple() == (67, 1, 68, 5)

    def test_cross_surah_with_a_nonexistent_end_is_rejected(self):
        assert parse_reference("67:1-68:53") is None      # Al-Qalam has 52

    def test_spanning_many_surahs(self):
        ref = parse_reference("112:1-114:6")
        assert ref.as_tuple() == (112, 1, 114, 6)


class TestJuzAndPage:
    @pytest.mark.parametrize("text", ["juz 30", "juz30", "j30", "30 juz", "JUZ 30"])
    def test_juz_spellings(self, text):
        ref = parse_reference(text)
        assert ref.kind == KIND_JUZ and ref.n == 30

    def test_juz_matches_the_corpus_division(self):
        assert juz_ref(30).as_tuple() == Quran.juz_range(30)

    def test_juz_30_spans_surahs(self):
        assert juz_ref(30).is_single_surah() is False

    @pytest.mark.parametrize("bad", [0, 31, 99])
    def test_juz_out_of_range(self, bad):
        assert juz_ref(bad) is None

    @pytest.mark.parametrize("text", ["page 604", "p604", "604 page", "pg 604"])
    def test_page_spellings(self, text):
        ref = parse_reference(text)
        assert ref.kind == KIND_PAGE and ref.n == 604

    def test_page_matches_the_corpus_division(self):
        assert page_ref(1).as_tuple() == Quran.page_range(1)

    @pytest.mark.parametrize("bad", [0, 605, 999])
    def test_page_out_of_range(self, bad):
        assert page_ref(bad) is None

    def test_every_juz_and_page_parses(self):
        for n in range(1, Quran.JUZ_COUNT + 1):
            assert juz_ref(n) is not None, n
        for n in range(1, Quran.PAGE_COUNT + 1):
            assert page_ref(n) is not None, n


class TestRejection:
    @pytest.mark.parametrize("bad", ["", "   ", "hello", "surah 67", "67:", ":8",
                                     "67:1-", "abc:def", "2:255:1", None])
    def test_junk_is_none_not_an_exception(self, bad):
        assert parse_reference(bad) is None

    def test_parse_range_mirrors_parse_reference(self):
        assert parse_range("67:1-8") == (67, 1, 67, 8)
        assert parse_range("nonsense") is None


class TestAyahCount:
    def test_within_one_surah(self):
        assert ayah_count(67, 1, 67, 30) == 30
        assert ayah_count(67, 5, 67, 5) == 1

    def test_across_two_surahs(self):
        # all 30 of Al-Mulk plus the first 5 of Al-Qalam
        assert ayah_count(67, 1, 68, 5) == 35

    def test_across_three_surahs_includes_the_whole_middle_one(self):
        expected = (Quran.get_surah_length(112) + Quran.get_surah_length(113)
                    + Quran.get_surah_length(114))
        assert ayah_count(112, 1, 114, Quran.get_surah_length(114)) == expected

    def test_inverted_span_is_zero_not_negative(self):
        assert ayah_count(68, 5, 67, 1) == 0

    def test_the_whole_quran_is_6236_ayahs(self):
        assert ayah_count(1, 1, 114, Quran.get_surah_length(114)) == 6236

    def test_ref_count_agrees(self):
        assert parse_reference("67").count() == 30
        assert parse_reference("67:1-68:5").count() == 35

    def test_juz_counts_are_positive_and_sum_to_the_quran(self):
        total = sum(juz_ref(n).count() for n in range(1, 31))
        assert total == 6236


class TestFormatting:
    def test_single_ayah(self):
        assert format_ref(parse_reference("67:5")) == "67:5"

    def test_within_one_surah_omits_the_repeated_surah(self):
        assert format_ref(parse_reference("67:1-8")) == "67:1-8"

    def test_cross_surah_shows_both(self):
        assert format_ref(parse_reference("67:1-68:5")) == "67:1-68:5"

    def test_whole_surah(self):
        assert format_ref(parse_reference("67")) == "67:1-30"

    def test_round_trips_through_the_parser(self):
        for text in ("67:5", "67:1-8", "67:1-68:5"):
            assert format_ref(parse_reference(format_ref(parse_reference(text)))) == \
                format_ref(parse_reference(text))


class TestContainsAndClamp:
    def test_contains_within_a_surah(self):
        ref = parse_reference("67:1-8")
        assert contains(ref, 67, 1) and contains(ref, 67, 8)
        assert not contains(ref, 67, 9)
        assert not contains(ref, 66, 1)

    def test_contains_across_surahs(self):
        ref = parse_reference("67:1-68:5")
        assert contains(ref, 67, 30)
        assert contains(ref, 68, 1)
        assert not contains(ref, 68, 6)

    def test_clamp_pulls_back_into_the_corpus(self):
        assert clamp_to_quran(67, 999) == (67, 30)
        assert clamp_to_quran(67, 0) == (67, 1)
        assert clamp_to_quran(0, 5) == (1, 5)
        assert clamp_to_quran(200, 1) == (114, 1)

    def test_clamp_leaves_a_real_ayah_alone(self):
        assert clamp_to_quran(67, 5) == (67, 5)


class TestEveryParsedRefIsReal:
    """A Ref is a promise that both ends exist — assert it holds broadly."""

    def test_across_all_surahs(self):
        for surah in range(1, 115):
            ref = surah_ref(surah)
            assert Quran.exists(*ref.start)
            assert Quran.exists(*ref.end)
            assert ref.start <= ref.end
