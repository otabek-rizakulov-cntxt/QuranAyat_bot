# Tests for the recall-check question builder.
#
# The load-bearing one is `test_correct_option_is_never_a_length_outlier`: the
# whole feature is worthless if a user can pass by tapping the longest button
# without reading Arabic. It sweeps every one of the 114 surahs.
#
# Everything here goes through `lib.recall_check`, which parses translations/ar.txt
# on the first question and caches it at class level for the process. That is one
# 1.3 MB parse for the whole file — no test may pull in a second language, because
# translations/ totals 71 MB and the production instance has 512 MB.

import datetime
import os
import unicodedata

import pytest

from lib import recall_check as rc
from modules.quran import Quran, TranslationRegistry


def _nfc(text: str) -> str:
    """Canonical form, for comparing corpus text against a hand-typed literal."""
    return unicodedata.normalize("NFC", text)


TODAY = datetime.date(2026, 7, 31)
TOMORROW = datetime.date(2026, 8, 1)
USER = 4242

# Surahs short enough that "distractors from the same surah" is impossible.
AL_ASR, AL_KAWTHAR, AL_IKHLAS = 103, 108, 112


def sweep_refs():
    """Every surah, sampled: all of a short surah, ten spread across a long one.

    The done-when asks for all 114 surahs. Sampling inside the long ones still
    covers every surah, both ends of every surah, and both question modes, while
    keeping this file at ~2.5 s.

    Set RECALL_CHECK_FULL_SWEEP=1 for the exhaustive 6236-ayah version. It passes
    — verified — and costs ~9 s for this file, roughly doubling the suite, which
    is why it is opt-in rather than the default. Every sweeping test shares the
    `swept` fixture, so the cost is one pass however many assertions read it.
    """
    full = os.environ.get("RECALL_CHECK_FULL_SWEEP") == "1"
    for surah in range(1, 115):
        length = Quran.get_surah_length(surah)
        if full or length <= 10:
            ayahs = range(1, length + 1)
        else:
            step = length / 10.0
            ayahs = sorted({1, length} | {int(i * step) + 1 for i in range(10)})
        for ayah in ayahs:
            yield surah, ayah


@pytest.fixture(scope="module")
def swept():
    """The sweep, built once and shared.

    Every sweeping test asks a different question of the same corpus of generated
    questions, and building them is the expensive part — one pass, not eight.
    """
    return [(surah, ayah, rc.build_question(USER, surah, ayah, TODAY))
            for surah, ayah in sweep_refs()]


# --- the done-when ------------------------------------------------------------

def test_correct_option_is_never_a_length_outlier(swept):
    """Across all 114 surahs, no answer stands out by how long it is.

    "Wide margin" is pinned to the documented tolerance rather than left to taste:
    every option, right or wrong, sits within max(4 chars, 25%) of the correct
    one's display length. Display length, not len() — vowelling is not width.
    """
    offenders = []
    for surah, ayah, question in swept:
        correct = rc.display_length(question.correct)
        for option in question.options:
            if not rc.is_similar_length(rc.display_length(option), correct):
                offenders.append((surah, ayah, correct, rc.display_length(option)))
    assert offenders == []


def test_correct_option_is_never_the_extreme_by_a_wide_ratio(swept):
    """A second, tolerance-independent cut at the same question.

    Even if someone widens LENGTH_SLACK_RATIO later, the longest and shortest
    options in a question must stay within a factor of two of each other, so the
    correct one can never be the sole extreme of a lopsided set.
    """
    for surah, ayah, question in swept:
        lengths = [rc.display_length(o) for o in question.options]
        assert max(lengths) <= 2 * min(lengths) + rc.LENGTH_SLACK_MIN, (surah, ayah, lengths)


def test_the_answer_is_not_findable_by_sorting_on_length(swept):
    """Over the whole sweep, the answer is the longest option about as often as chance.

    The per-question tolerance can hold while a systematic bias still leaks — if
    the correct option were the longest 60% of the time, "pick the longest" would
    beat guessing without reading a word of Arabic. Four options, so chance is 25%.
    """
    longest = shortest = 0
    for _, _, question in swept:
        lengths = [rc.display_length(o) for o in question.options]
        correct = lengths[question.correct_index]
        longest += correct == max(lengths)
        shortest += correct == min(lengths)
    total = len(swept)
    assert 0.15 < longest / total < 0.40, longest / total
    assert 0.15 < shortest / total < 0.40, shortest / total


def test_sweep_produces_a_well_formed_question_everywhere(swept):
    """Four distinct options, a real prompt, and a correct index that points at it."""
    for surah, ayah, question in swept:
        assert len(question.options) == rc.OPTION_COUNT
        assert len(set(question.options)) == rc.OPTION_COUNT, (surah, ayah)
        assert 0 <= question.correct_index < rc.OPTION_COUNT
        assert question.is_correct(question.correct_index)
        assert question.prompt.strip()
        assert all(o.strip() for o in question.options)
        assert question.ref == (surah, ayah)


def test_options_are_distinct_even_ignoring_vowelling(swept):
    """Two options that differ only in harakat would read as the same button."""
    for surah, ayah, question in swept:
        keys = {rc._key(o) for o in question.options}
        assert len(keys) == rc.OPTION_COUNT, (surah, ayah, question.options)


def test_prompt_is_never_offered_back_as_an_option(swept):
    """The cue must not also be one of the answers."""
    for _, _, question in swept:
        assert rc._key(question.prompt) not in {rc._key(o) for o in question.options}


# --- the correct answer is actually correct -----------------------------------

def test_correct_option_really_follows_the_prompt(swept):
    """In continuation mode, prompt + correct option is a prefix of the ayah.

    Guards the split arithmetic: an off-by-one in the prompt length would make the
    "correct" answer skip or repeat a word, and every user who actually knows the
    ayah would answer wrong.
    """
    for surah, ayah, question in swept:
        if question.mode != rc.MODE_CONTINUATION:
            continue
        words = rc._words(surah, ayah)
        joined = (question.prompt + " " + question.correct).split()
        assert words[:len(joined)] == joined, (surah, ayah)


def test_both_question_modes_show_up_in_the_sweep(swept):
    """The sweep only means something if it exercises the short-ayah path too."""
    assert {q.mode for _, _, q in swept} == {rc.MODE_CONTINUATION, rc.MODE_NEXT_AYAH}


def test_next_ayah_mode_answers_with_the_whole_short_ayah():
    """For a three-word ayah the answer is the ayah, cued by the one before it."""
    question = rc.build_question(USER, 2, 1, TODAY)
    assert question.mode == rc.MODE_NEXT_AYAH
    assert question.correct == " ".join(rc._words(2, 1))
    assert question.prompt_ref == (1, 7)          # crosses the surah boundary
    assert question.prompt == " ".join(rc._words(1, 7))


def test_prompt_is_the_opening_of_the_ayah_in_continuation_mode():
    question = rc.build_question(USER, 67, 1, TODAY)
    assert question.mode == rc.MODE_CONTINUATION
    assert question.prompt_ref == (67, 1)
    assert question.prompt_truncated is False
    assert rc._words(67, 1)[0].startswith(question.prompt.split()[0])
    assert rc.MIN_PROMPT_WORDS <= len(question.prompt.split()) <= rc.MAX_PROMPT_WORDS


def test_long_ayah_prompt_and_options_stay_button_sized():
    """2:282 is the longest ayah in the Qur'an and must not produce a wall of text."""
    question = rc.build_question(USER, 2, 282, TODAY)
    assert len(question.prompt.split()) <= rc.MAX_PROMPT_WORDS
    for option in question.options:
        assert len(option.split()) <= rc.MAX_OPTION_WORDS
        assert rc.display_length(option) <= rc.MAX_OPTION_LENGTH


def test_next_ayah_prompt_is_truncated_and_says_so(swept):
    """A short ayah preceded by a long one gets a tail, and flags that it is one."""
    long_tail = [(s, a, q) for s, a, q in swept if q.prompt_truncated]
    assert long_tail, "expected at least one next-ayah prompt to need trimming"
    for surah, ayah, question in long_tail[:5]:
        assert question.mode == rc.MODE_NEXT_AYAH
        assert len(question.prompt.split()) == rc.MAX_CONTEXT_WORDS


def test_every_option_carries_the_same_word_count(swept):
    """Word count must not be the tell either — that is why distractors are tails."""
    for surah, ayah, question in swept:
        if question.mode != rc.MODE_CONTINUATION:
            continue          # whole short ayahs vary by a word, by construction
        counts = {len(o.split()) for o in question.options}
        assert len(counts) == 1, (surah, ayah, question.options)


# --- determinism ---------------------------------------------------------------

def test_same_inputs_give_the_same_question():
    """A retry must not be a reroll — same options, same order, same index."""
    for _ in range(3):
        first = rc.build_question(USER, 36, 5, TODAY)
        second = rc.build_question(USER, 36, 5, TODAY)
        assert first == second


def test_a_different_date_gives_a_different_question():
    """Tomorrow's check on the same ayah is a new question, not yesterday's."""
    today = rc.build_question(USER, 36, 5, TODAY)
    tomorrow = rc.build_question(USER, 36, 5, TOMORROW)
    assert today.correct == tomorrow.correct
    assert today.options != tomorrow.options


def test_a_different_user_gets_a_different_question():
    mine = rc.build_question(USER, 36, 5, TODAY)
    theirs = rc.build_question(USER + 1, 36, 5, TODAY)
    assert mine.options != theirs.options


def test_dates_and_iso_strings_are_interchangeable():
    """Callers hold a `date`; stored rows hold "2026-07-31". Both must key the same."""
    assert rc.build_question(USER, 36, 5, TODAY) == rc.build_question(USER, 36, 5, "2026-07-31")


def test_the_global_random_module_is_never_touched():
    """Seeding the global RNG must not change what a user sees.

    `modules.quran` imports `random.randint` for /random, and any other test may
    seed the global RNG. If this builder used it, a question would depend on
    whatever ran before it.
    """
    import random

    random.seed(1)
    first = rc.build_question(USER, 36, 5, TODAY)
    random.seed(999)
    random.random()
    assert rc.build_question(USER, 36, 5, TODAY) == first


def test_the_answer_does_not_always_land_in_the_same_slot():
    """If the correct option were always index 0, tapping the first button wins."""
    slots = {rc.build_question(USER, 36, ayah, TODAY).correct_index
             for ayah in range(1, 40)}
    assert slots == {0, 1, 2, 3}


# --- degenerate spans -----------------------------------------------------------

@pytest.mark.parametrize("surah", [AL_ASR, AL_KAWTHAR, AL_IKHLAS])
def test_short_surahs_still_get_four_distinct_options(surah):
    """Al-Kawthar has three ayahs, so same-surah distractors cannot fill a question.

    The neighbourhood fallback has to, and the result still has to be four
    distinct, similar-length options.
    """
    for ayah in range(1, Quran.get_surah_length(surah) + 1):
        question = rc.build_question(USER, surah, ayah, TODAY)
        assert len(set(question.options)) == rc.OPTION_COUNT
        correct = rc.display_length(question.correct)
        for option in question.options:
            assert rc.is_similar_length(rc.display_length(option), correct)


@pytest.mark.parametrize("surah", range(1, 115))
def test_the_last_ayah_of_every_surah_produces_a_question(surah):
    """There is no "next ayah" inside the surah to continue into — still fine."""
    question = rc.build_question(USER, surah, Quran.get_surah_length(surah), TODAY)
    assert len(set(question.options)) == rc.OPTION_COUNT
    assert question.correct in question.options


def test_the_first_and_last_ayah_of_the_quran():
    """1:1 has nothing before it and 114:6 nothing after it.

    1:1 is always split rather than cued from a preceding ayah, because there is
    none. 114:6 falls back into a neighbourhood that wraps to the start, the way a
    khatm does.
    """
    opening = rc.build_question(USER, 1, 1, TODAY)
    assert opening.mode == rc.MODE_CONTINUATION
    assert opening.prompt_ref == (1, 1)
    assert len(set(opening.options)) == rc.OPTION_COUNT

    closing = rc.build_question(USER, 114, 6, TODAY)
    assert len(set(closing.options)) == rc.OPTION_COUNT


def test_muqattaat_get_muqattaat_shaped_distractors():
    """"الم" is three characters; three fully-vocalized ayahs beside it would be a tell."""
    question = rc.build_question(USER, 2, 1, TODAY)
    lengths = [rc.display_length(o) for o in question.options]
    assert max(lengths) <= rc.display_length(question.correct) + rc.LENGTH_SLACK_MIN


def test_unknown_ayahs_are_rejected():
    with pytest.raises(ValueError):
        rc.build_question(USER, 108, 4, TODAY)
    with pytest.raises(ValueError):
        rc.build_question(USER, 115, 1, TODAY)


# --- corpus hygiene --------------------------------------------------------------

def test_the_basmala_heading_is_not_part_of_the_question():
    """Tanzil prepends the basmala to ayah 1 of every surah but At-Tawbah.

    Left in, every "first ayah" option would open with the same 38 characters —
    a giveaway and a length distortion. Surah 1 is the exception: there the
    basmala is the ayah.
    """
    basmala = rc._basmala_prefix()
    assert rc._words(2, 1) == ["الم"]

    # Compared under NFC because Tanzil's text is *not* normalized: it stores
    # noon + shadda + fatha, while typing the same words by hand yields
    # noon + fatha + shadda. The two are canonically equivalent and render
    # identically, so a byte comparison here tests the typist, not the code.
    stripped = " ".join(rc._words(108, 1))
    assert _nfc(stripped) == _nfc("إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ")
    # ...and independently of any literal: it is exactly the ayah minus the heading
    raw = TranslationRegistry.get("ar").get_ayah_text(108, 1)
    assert stripped == raw[len(basmala):].strip()

    assert " ".join(rc._words(1, 1)) == basmala
    assert " ".join(rc._words(9, 1)).startswith("بَرَاءَةٌ")
    for surah in range(2, 115):
        assert not " ".join(rc._words(surah, 1)).startswith(basmala)


def test_no_option_carries_a_reference_suffix_or_a_bom(swept):
    """`get_ayah` would append " (67:1)" — the answer, printed beside the question."""
    for surah, ayah, question in swept:
        for text in (question.prompt,) + question.options:
            assert "(" not in text and ")" not in text
            assert "﻿" not in text


def test_options_need_no_html_escaping_beyond_the_callers(swept):
    """The Arabic corpus holds no <, > or &, so a caller escaping is belt-and-braces."""
    for surah, ayah, question in swept:
        for text in (question.prompt,) + question.options:
            assert not set(text) & set("<>&")


def test_display_length_ignores_vowelling():
    assert rc.display_length("الم") == 3
    assert rc.display_length("بِسْمِ") == len("بسم")
    assert rc.display_length("  a   b  ") == 3


def test_is_similar_length_bands():
    assert rc.is_similar_length(100, 100)
    assert rc.is_similar_length(75, 100)
    assert not rc.is_similar_length(74, 100)
    assert rc.is_similar_length(7, 3)             # absolute floor for muqatta'at
    assert not rc.is_similar_length(8, 3)


# --- picking which ayah to test ---------------------------------------------------

def test_pick_ayah_stays_inside_the_span():
    span = (67, 1, 67, 30)
    for user in range(30):
        surah, ayah = rc.pick_ayah(user, span, TODAY)
        assert surah == 67 and 1 <= ayah <= 30


def test_pick_ayah_handles_a_cross_surah_span():
    """Juz 30 runs 78:1-114:6, so a plan portion routinely crosses surahs."""
    span = (78, 1, 114, 6)
    seen = {rc.pick_ayah(user, span, TODAY) for user in range(60)}
    assert len(seen) > 1
    for surah, ayah in seen:
        assert (78, 1) <= (surah, ayah) <= (114, 6)
        assert Quran.exists(surah, ayah)


def test_pick_ayah_is_deterministic_per_user_and_date():
    span = (67, 1, 67, 30)
    assert rc.pick_ayah(USER, span, TODAY) == rc.pick_ayah(USER, span, TODAY)
    picks = {rc.pick_ayah(USER, span, datetime.date(2026, 8, day)) for day in range(1, 20)}
    assert len(picks) > 1


def test_pick_ayahs_returns_distinct_ayahs():
    span = (2, 1, 2, 286)
    picked = rc.pick_ayahs(USER, span, TODAY, 5)
    assert len(picked) == len(set(picked)) == 5
    assert picked == sorted(picked)          # mushaf order
    assert picked == rc.pick_ayahs(USER, span, TODAY, 5)


def test_pick_ayahs_cannot_exceed_the_span():
    assert len(rc.pick_ayahs(USER, (108, 1, 108, 3), TODAY, 10)) == 3
    assert rc.pick_ayahs(USER, (108, 1, 108, 3), TODAY, 0) == []


def test_pick_ayah_accepts_anything_with_as_tuple():
    """i.e. a `hifz.refs.Ref`, without this module importing the hifz package."""

    class FakeRef:
        def as_tuple(self):
            return (67, 1, 67, 30)

    assert rc.pick_ayah(USER, FakeRef(), TODAY)[0] == 67


def test_pick_ayah_on_an_inverted_or_empty_span():
    assert rc.pick_ayah(USER, (67, 30, 67, 1), TODAY) is None
    with pytest.raises(ValueError):
        rc.pick_ayah(USER, (67, 1, 67), TODAY)


def test_the_whole_quran_is_a_valid_span():
    """`/check` with no argument would test the user on anything they have learnt."""
    surah, ayah = rc.pick_ayah(USER, (1, 1, 114, 6), TODAY)
    assert Quran.exists(surah, ayah)
    assert rc.build_question(USER, surah, ayah, TODAY).ref == (surah, ayah)


def test_pick_then_build_is_the_whole_check_flow():
    """/check 67 -> an ayah of Al-Mulk -> a four-option question about it."""
    surah, ayah = rc.pick_ayah(USER, (67, 1, 67, 30), TODAY)
    question = rc.build_question(USER, surah, ayah, TODAY)
    assert question.surah == 67
    assert question.options[question.correct_index] == question.correct


# --- loading -----------------------------------------------------------------------

async def test_preload_corpus_returns_the_same_cached_object():
    """Wave 2C can warm the 1.3 MB parse off the event loop; it must not re-parse."""
    loaded = await rc.preload_corpus()
    assert loaded is rc.corpus()
    assert await rc.preload_corpus() is loaded
