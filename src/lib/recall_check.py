# Recall-check question builder.
#
# This is the part of the hifz platform that is fair to someone memorizing from a
# paper mushaf. Every other way of earning a day (running a drill, marking a
# portion) measures app usage; this one measures hifz. So it has to work for a
# user who opens the bot once, answers one question, and closes it again.
#
# The shape of a question is fixed by that goal: an *opening* the user recognizes,
# and four *continuations* one of which follows it. Nothing here formats anything
# for Telegram — `build_question` returns structured data and the handler renders
# it, because the surrounding strings are localized into 49 languages and the
# option texts are not.
#
# Two Telegram facts drive the API:
#   * `callback_data` is capped at 64 *bytes*, and one vocalized Arabic word can
#     eat 30 of them. So the callback carries `correct_index`-style integers, never
#     option text — which is why the options are an ordered tuple and the answer is
#     an index into it.
#   * Button labels have no such cap but do get truncated by the client, so options
#     are kept to a handful of words (see `MAX_OPTION_WORDS` / `MAX_OPTION_LENGTH`).
#
# The corpus is `translations/ar.txt` — the full vocalized Uthmani text, 6236
# ayahs, already bundled and reachable through the existing TranslationRegistry.
# It is parsed on the first question, never at import: it is 1.3 MB and the
# production instance has 512 MB.

import asyncio
import hashlib
import math
import random
import unicodedata
from dataclasses import dataclass
from typing import Iterable, Iterator, List, Optional, Sequence, Tuple

from modules.quran import Quran, TranslationRegistry

__all__ = [
    "RecallQuestion",
    "ARABIC", "OPTION_COUNT",
    "MODE_CONTINUATION", "MODE_NEXT_AYAH",
    "MAX_OPTION_WORDS", "MAX_OPTION_LENGTH",
    "MIN_PROMPT_WORDS", "MAX_PROMPT_WORDS", "PROMPT_SHARE", "MAX_CONTEXT_WORDS",
    "LENGTH_SLACK_RATIO", "LENGTH_SLACK_MIN",
    "build_question", "pick_ayah", "pick_ayahs",
    "display_length", "is_similar_length",
    "preload_corpus", "corpus",
]

# The recall check is always in Arabic. The user's translation language decides
# what the *chrome* around the question says, never the ayah text: a continuation
# is only a real memorization test in the language it was memorized in.
ARABIC = "ar"

OPTION_COUNT = 4

# The prompt is the opening of the ayah under test...
MODE_CONTINUATION = "continuation"
# ...unless the ayah is too short to be split (593 of the 6236 ayahs are three
# words or fewer, e.g. "الم"), in which case the prompt is the tail of the
# preceding ayah and the whole ayah is the answer.
MODE_NEXT_AYAH = "next_ayah"

# --- The two length rules ----------------------------------------------------
#
# PROMPT rule. In continuation mode the prompt is the first
#     p = clamp(ceil(PROMPT_SHARE * W), MIN_PROMPT_WORDS, MAX_PROMPT_WORDS)
# words of the ayah, where W is its word count. Two words minimum because a
# single Qur'anic word ("وَإِذَا", "قَالَ") occurs hundreds of times and cues
# nothing; six words maximum because beyond that the prompt starts to *contain*
# the phrase the answer completes, and it bloats a message that also carries four
# options. The 40% share is what keeps a five-word ayah from being handed over
# almost whole. In next-ayah mode the prompt is the last MAX_CONTEXT_WORDS words
# of the preceding ayah — a huffaz cue is the tail you are reciting *from*, and
# the preceding ayah can be 2:282.
MIN_PROMPT_WORDS = 2
MAX_PROMPT_WORDS = 6
PROMPT_SHARE = 0.4
MAX_CONTEXT_WORDS = 10

# OPTION rule. Every option in a question carries exactly the same number of
# words — the correct one is the next `c` words after the prompt, each distractor
# is the last `c` words of some other ayah — so word count can never be the tell.
# `c` is capped so an option fits a button label.
MAX_OPTION_WORDS = 8
MAX_OPTION_LENGTH = 64          # in display characters, see display_length()
MIN_OPTION_WORDS = 2            # below this the shortening stops, cap or no cap

# An ayah needs two words of prompt and two of continuation before splitting it
# tests anything; below that the question changes shape (see MODE_NEXT_AYAH).
MIN_SPLITTABLE_WORDS = MIN_PROMPT_WORDS + MIN_OPTION_WORDS

# LENGTH tolerance. An option is "similar length" to the correct one when
#     |len(option) - len(correct)| <= max(LENGTH_SLACK_MIN, LENGTH_SLACK_RATIO * len(correct))
# measured in display characters. 25% is roughly the point below which two Arabic
# fragments on adjacent buttons read as the same size; the absolute floor of four
# characters is for the muqatta'at ("الم" is three characters, and a 25% band
# around it would admit nothing at all).
LENGTH_SLACK_RATIO = 0.25
LENGTH_SLACK_MIN = 4

# How far the distractor search widens when the surah cannot supply three
# similar-length options. In mushaf order, so it crosses surah boundaries — which
# is exactly what "falling back to neighbouring ayahs" means for Al-Kawthar.
NEIGHBOUR_RADIUS = 48
WIDE_RADIUS = 400

_BOM = "﻿"
_TATWEEL = "ـ"


@dataclass(frozen=True)
class RecallQuestion:
    """One four-option recall check, ready to be rendered and keyboarded.

    Everything here is raw corpus text: unescaped, un-prefixed, no reference
    suffix. The caller escapes it for HTML and wraps it in localized copy. The
    answer travels as `correct_index` because `callback_data` is 64 bytes and
    Arabic is not.
    """

    surah: int
    ayah: int
    prompt: str
    options: Tuple[str, ...]
    correct_index: int
    mode: str
    prompt_surah: int
    prompt_ayah: int
    prompt_truncated: bool

    @property
    def correct(self) -> str:
        """The option that actually follows the prompt."""
        return self.options[self.correct_index]

    @property
    def ref(self) -> Tuple[int, int]:
        return self.surah, self.ayah

    @property
    def prompt_ref(self) -> Tuple[int, int]:
        """Where the prompt text came from — the ayah itself, or the one before it."""
        return self.prompt_surah, self.prompt_ayah

    def is_correct(self, index: int) -> bool:
        """Whether the option the user tapped is the right one."""
        return index == self.correct_index


# --- corpus access -----------------------------------------------------------

def corpus() -> Quran:
    """The vocalized Arabic text, parsed on first use and cached thereafter.

    TranslationRegistry caches at class level for the life of the process, so the
    1.3 MB parse happens once. Deliberately *not* done at import time: importing
    this module must stay free, because main.py imports everything at boot.
    """
    return TranslationRegistry.get(ARABIC)


async def preload_corpus() -> Quran:
    """Warm the Arabic corpus without blocking the event loop.

    Same trick as `main.get_translation`: the first parse is ~1.3 MB of file I/O
    and string work, which is long enough to stall a webhook if it happens inline.
    Once cached this is a dict lookup and never touches a thread.
    """
    if TranslationRegistry.is_cached(ARABIC):
        return corpus()
    return await asyncio.to_thread(corpus)


_basmala: Optional[str] = None


def _basmala_prefix() -> str:
    """The basmala exactly as the corpus spells it.

    Tanzil's text prepends it to ayah 1 of every surah except At-Tawbah, where in
    the mushaf it is a heading above the page rather than part of the verse. It
    has to come off before a question is built: leaving it on would make every
    "first ayah of a surah" option start with the same 38 characters, which is
    both a giveaway and a length distortion. Surah 1 is the exception to the
    exception — there the basmala *is* ayah 1.
    """
    global _basmala
    if _basmala is None:
        _basmala = _clean(corpus().get_ayah_text(1, 1))
    return _basmala


def _clean(text: str) -> str:
    """Corpus text with the file's BOM and stray whitespace removed."""
    return " ".join(text.replace(_BOM, "").split())


def _ayah_text(surah: int, ayah: int) -> str:
    """The ayah as a single-spaced string, basmala heading stripped.

    Kept string-shaped rather than tokenized because the distractor search touches
    thousands of ayahs per question and only ever wants a handful of words off the
    end of each: splitting every one of them whole was the profile's hot spot.
    """
    text = corpus().get_ayah_text(surah, ayah).replace(_BOM, "").strip()
    if ayah == 1 and surah != 1:
        prefix = _basmala_prefix()
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    return text


def _words(surah: int, ayah: int) -> List[str]:
    """The ayah as a word list — only the ayah under test needs this."""
    return _ayah_text(surah, ayah).split()


# --- length -------------------------------------------------------------------

# Every combining mark in the Arabic blocks, mapped away in one C-level pass.
# Built by asking unicodedata once at import rather than hard-coding ranges, so a
# Unicode update cannot leave a stray mark being counted as width. This is a few
# hundred category lookups; the alternative is thirty-odd million of them per
# corpus-wide distractor search, which is what profiling showed.
_MARKS = {code: None
          for block in (range(0x0600, 0x0700), range(0x0750, 0x0780),
                        range(0x08A0, 0x0900), range(0xFB50, 0xFE00),
                        range(0xFE70, 0xFF00))
          for code in block
          if unicodedata.category(chr(code)) == "Mn"}
_MARKS[ord(_TATWEEL)] = None
_MARKS_AND_SPACE = dict(_MARKS)
_MARKS_AND_SPACE[ord(" ")] = None


def display_length(text: str) -> int:
    """Length as the eye sees it: combining marks and tatweel do not count.

    Vocalized Uthmani text carries two to three harakat per letter, so raw
    `len()` measures vowelling density as much as it measures width — "الم" is 3
    characters and a fully-pointed three-word ayah can be 40. Buttons are laid out
    by rendered width, so the length filter has to be too.

    Deliberately not NFD-normalized first: آ is one glyph on a button whether or
    not Unicode is willing to decompose it into two code points.
    """
    return len(" ".join(text.split()).translate(_MARKS))


def is_similar_length(length: int, target: int) -> bool:
    """Whether an option of `length` is close enough to `target` to hide in a set."""
    return abs(length - target) <= max(LENGTH_SLACK_MIN,
                                       int(round(LENGTH_SLACK_RATIO * target)))


def _key(text: str) -> str:
    """Duplicate-detection key: same letters, ignoring vowelling and spacing.

    Two options that differ only in harakat would read as the same button to the
    user, and offering the correct text twice makes the question unanswerable.
    """
    return text.translate(_MARKS_AND_SPACE)


# --- determinism --------------------------------------------------------------

def _rng(*parts) -> random.Random:
    """A private RNG seeded from the given parts.

    Never the module-level `random`: that is process-wide shared state, so a
    question built between two other calls to it would come out differently, and
    another test seeding it would silently reroll ours. Seeding from
    (user, ayah, date) is what makes a retry show the same question rather than a
    fresh one — otherwise a wrong answer could be re-rolled until it was easy.
    """
    raw = "\x1f".join(str(p) for p in parts).encode("utf-8")
    return random.Random(int.from_bytes(hashlib.sha256(raw).digest(), "big"))


def _date_key(local_date) -> str:
    """A `datetime.date`, or anything already string-shaped, as a stable key."""
    isoformat = getattr(local_date, "isoformat", None)
    return isoformat() if callable(isoformat) else str(local_date)


# --- candidate pools ----------------------------------------------------------

def _same_surah(surah: int, ayah: int) -> Iterator[Tuple[int, int]]:
    """Every other ayah of the same surah — the preferred distractor source.

    Same surah means same subject matter, similar cadence and often a shared
    rhyme, so a distractor from here is a real test rather than a giveaway.
    """
    for a in range(1, Quran.get_surah_length(surah) + 1):
        if a != ayah:
            yield surah, a


def _neighbours(surah: int, ayah: int, radius: int) -> Iterator[Tuple[int, int]]:
    """Ayahs within `radius` positions in mushaf order, both directions.

    Crosses surah boundaries, which is the whole point: Al-Kawthar has three
    ayahs, so "the same surah" can never supply three distractors and the
    neighbourhood has to. `Quran.get_next_ayah` / `get_previous_ayah` wrap around
    the ends of the Qur'an, so 1:1 and 114:6 get a full-sized neighbourhood too
    instead of a truncated one.
    """
    back = forward = (surah, ayah)
    for _ in range(radius):
        back = Quran.get_previous_ayah(*back)
        forward = Quran.get_next_ayah(*forward)
        yield back
        yield forward


def _everything() -> Iterator[Tuple[int, int]]:
    """The whole Qur'an, last resort.

    Reached when neither the surah nor the neighbourhood holds three fragments of
    the right length — the muqatta'at are the standard case, since the only good
    distractors for "الم" are the other opening letters, scattered across twenty
    surahs.
    """
    for s in range(1, 115):
        for a in range(1, Quran.get_surah_length(s) + 1):
            yield s, a


def _option_from(surah: int, ayah: int, word_count: int) -> Optional[str]:
    """A distractor of exactly `word_count` words taken from the end of an ayah.

    The tail, not the head: an ayah's closing words are a grammatically complete
    phrase and read like something that could follow a prompt, whereas its opening
    words often read like something that could only start one. Returns None when
    the ayah is too short to give that many words — a shorter option would make
    word count the tell.
    """
    # rsplit stops after `word_count` cuts, so a 129-word ayah costs the same as a
    # five-word one. It returns word_count + 1 parts when there is text left over
    # in front, and exactly word_count when the ayah is precisely that long.
    parts = _ayah_text(surah, ayah).rsplit(" ", word_count)
    if len(parts) == word_count + 1:
        return " ".join(parts[1:])
    if len(parts) == word_count:
        return " ".join(parts)
    return None


def _whole_ayah_option(surah: int, ayah: int) -> Optional[str]:
    """The whole ayah as an option, for next-ayah mode."""
    return _ayah_text(surah, ayah) or None


def _gather(stages: Sequence[Iterable[Tuple[int, int]]], make_option, exclude_keys,
            target_length: int, rng: random.Random) -> List[str]:
    """Three distinct distractors, widening the search only as far as needed.

    Stages are tried in order and *accumulate*: once a stage brings the pool to
    three similar-length candidates we sample from everything gathered so far, so
    a surah that can supply two good distractors still contributes them. If even
    the last stage cannot fill the length band — which the corpus never actually
    does, but a caller could construct — we take the three nearest by length, so
    the question is always answerable and the outlier is as small as possible.
    """
    pool: dict = {}
    for stage in stages:
        for ref in stage:
            if ref in pool:
                continue
            text = make_option(*ref)
            if text is not None:
                pool[ref] = (text, display_length(text))
        near = _distinct(pool, exclude_keys,
                         lambda length: is_similar_length(length, target_length))
        if len(near) >= OPTION_COUNT - 1:
            return [near[key][0] for key in rng.sample(sorted(near), OPTION_COUNT - 1)]

    everything = _distinct(pool, exclude_keys, lambda length: True)
    nearest = sorted(everything,
                     key=lambda key: (abs(everything[key][1] - target_length), key))
    return [everything[key][0] for key in nearest[:OPTION_COUNT - 1]]


def _distinct(pool: dict, exclude_keys, keep) -> dict:
    """The pool reduced to one entry per distinguishable text, `keep` applied first.

    Keyed by the vowelling-insensitive form so two candidates that would render as
    the same button collapse into one, and so an option identical to the answer is
    dropped rather than offered twice. Cheap because it runs over the pool, not
    over each candidate as it arrives: the corpus-wide stage looks at 6236 ayahs
    and normalizing every one of them was measurably the slowest thing here.
    """
    chosen: dict = {}
    for text, length in pool.values():
        if not keep(length):
            continue
        key = _key(text)
        if key not in exclude_keys and key not in chosen:
            chosen[key] = (text, length)
    return chosen


# --- the builder ---------------------------------------------------------------

def _split_point(word_count: int) -> int:
    """How many opening words the prompt shows — the PROMPT rule, in code."""
    share = math.ceil(PROMPT_SHARE * word_count)
    return max(MIN_PROMPT_WORDS, min(MAX_PROMPT_WORDS, share))


def _option_words(available: int) -> int:
    """How many words each option carries — the OPTION rule, in code."""
    return max(1, min(available, MAX_OPTION_WORDS))


def _shorten_to_button(words: List[str], count: int) -> int:
    """Trim an option until it fits a button, never below MIN_OPTION_WORDS.

    A long ayah's continuation would otherwise run to hundreds of characters and
    be truncated by the client mid-word — which, applied to only one of the four
    options, would itself be a tell.
    """
    while count > MIN_OPTION_WORDS and display_length(" ".join(words[:count])) > MAX_OPTION_LENGTH:
        count -= 1
    return count


def build_question(user_id: int, surah: int, ayah: int, local_date) -> RecallQuestion:
    """Build the recall check for `surah:ayah` as this user sees it on this date.

    Deterministic in (user_id, surah, ayah, local_date): the same four options in
    the same order every time, so re-opening the message or retrying after a
    network blip shows the question again rather than rerolling it into an easier
    one. A different date is a different question on the same ayah.

    Raises ValueError if the ayah does not exist.
    """
    if not Quran.exists(surah, ayah):
        raise ValueError("no such ayah: %s:%s" % (surah, ayah))

    words = _words(surah, ayah)
    rng = _rng(user_id, surah, ayah, _date_key(local_date))

    # 1:1 has no preceding ayah to take a cue from, so it is always split — which
    # is safe, because the basmala is four words.
    if len(words) >= MIN_SPLITTABLE_WORDS or (surah, ayah) == (1, 1):
        question = _continuation_question(rng, surah, ayah, words)
    else:
        question = _next_ayah_question(rng, surah, ayah, words)
    return question


def _continuation_question(rng: random.Random, surah: int, ayah: int,
                           words: List[str]) -> RecallQuestion:
    """Opening of the ayah, then the words that continue it."""
    prompt_words = min(_split_point(len(words)), len(words) - 1)
    count = _option_words(len(words) - prompt_words)
    count = _shorten_to_button(words[prompt_words:], count)

    correct = " ".join(words[prompt_words:prompt_words + count])
    target = display_length(correct)
    distractors = _gather(
        [_same_surah(surah, ayah),
         _neighbours(surah, ayah, NEIGHBOUR_RADIUS),
         _neighbours(surah, ayah, WIDE_RADIUS),
         _everything()],
        lambda s, a: _option_from(s, a, count),
        {_key(correct)},
        target,
        rng,
    )
    return _assemble(rng, surah, ayah, " ".join(words[:prompt_words]), correct,
                     distractors, MODE_CONTINUATION, surah, ayah,
                     prompt_truncated=False)


def _next_ayah_question(rng: random.Random, surah: int, ayah: int,
                        words: List[str]) -> RecallQuestion:
    """Tail of the preceding ayah, then the whole (short) ayah under test.

    For an ayah of three words or fewer there is no honest place to cut: "الم"
    split at a word boundary is either nothing or everything. So the cue moves
    back one ayah, which is how these are actually joined in recitation anyway.
    Ayah 1 of a surah takes its cue from the last ayah of the previous surah,
    which is mushaf order and is what a hafiz reciting continuously hears.
    """
    previous = Quran.get_previous_ayah(surah, ayah)
    context = _words(*previous)
    truncated = len(context) > MAX_CONTEXT_WORDS
    prompt = " ".join(context[len(context) - MAX_CONTEXT_WORDS:] if truncated else context)

    correct = " ".join(words)
    target = display_length(correct)
    distractors = _gather(
        [_same_surah(surah, ayah),
         _neighbours(surah, ayah, NEIGHBOUR_RADIUS),
         _neighbours(surah, ayah, WIDE_RADIUS),
         _everything()],
        _whole_ayah_option,
        {_key(correct), _key(prompt)},
        target,
        rng,
    )
    return _assemble(rng, surah, ayah, prompt, correct, distractors,
                     MODE_NEXT_AYAH, previous[0], previous[1],
                     prompt_truncated=truncated)


def _assemble(rng: random.Random, surah: int, ayah: int, prompt: str, correct: str,
              distractors: Sequence[str], mode: str, prompt_surah: int,
              prompt_ayah: int, prompt_truncated: bool) -> RecallQuestion:
    """Shuffle the correct option in among the distractors and record where it landed."""
    options = [correct] + list(distractors)
    rng.shuffle(options)
    return RecallQuestion(
        surah=surah,
        ayah=ayah,
        prompt=prompt,
        options=tuple(options),
        correct_index=options.index(correct),
        mode=mode,
        prompt_surah=prompt_surah,
        prompt_ayah=prompt_ayah,
        prompt_truncated=prompt_truncated,
    )


# --- which ayah to test --------------------------------------------------------

def _span_tuple(span) -> Tuple[int, int, int, int]:
    """Accept either a 4-tuple or anything with `as_tuple()` — i.e. a hifz Ref.

    Duck-typed on purpose: `hifz.refs.Ref` is the natural argument from a plan
    portion or from `/check 67`, but this module has no reason to import it and
    every reason not to grow a dependency on the hifz package.
    """
    as_tuple = getattr(span, "as_tuple", None)
    values = as_tuple() if callable(as_tuple) else tuple(span)
    if len(values) != 4:
        raise ValueError("span must be (start_surah, start_ayah, end_surah, end_ayah)")
    return tuple(int(v) for v in values)  # type: ignore[return-value]


def _span_length(start_surah: int, start_ayah: int,
                 end_surah: int, end_ayah: int) -> int:
    """Ayahs in an inclusive cross-surah span; 0 if inverted.

    Counted from the surah lengths rather than walked, so a whole juz costs the
    same as a single ayah.
    """
    if (end_surah, end_ayah) < (start_surah, start_ayah):
        return 0
    if start_surah == end_surah:
        return end_ayah - start_ayah + 1
    total = Quran.get_surah_length(start_surah) - start_ayah + 1
    for surah in range(start_surah + 1, end_surah):
        total += Quran.get_surah_length(surah)
    return total + end_ayah


def _at_offset(start_surah: int, start_ayah: int, offset: int) -> Tuple[int, int]:
    """The ayah `offset` positions after start, by arithmetic rather than walking."""
    surah, ayah = start_surah, start_ayah
    while True:
        remaining = Quran.get_surah_length(surah) - ayah + 1
        if offset < remaining:
            return surah, ayah + offset
        offset -= remaining
        surah, ayah = surah + 1, 1


def pick_ayahs(user_id: int, span, local_date, count: int = 1) -> List[Tuple[int, int]]:
    """Which ayahs to test out of `span`, in mushaf order, without repeats.

    `span` is a plan portion or whatever the user named — `/check 67` is the whole
    of Al-Mulk. Deterministic in (user, span, date) for the same reason a question
    is: a session interrupted halfway must resume on the same ayahs, and asking
    again should not be a way to shop for an easy one. Returns fewer than `count`
    only when the span itself is smaller, and [] for an empty or inverted span.
    """
    start_surah, start_ayah, end_surah, end_ayah = _span_tuple(span)
    total = _span_length(start_surah, start_ayah, end_surah, end_ayah)
    if total <= 0 or count <= 0:
        return []
    rng = _rng(user_id, start_surah, start_ayah, end_surah, end_ayah,
               _date_key(local_date))
    offsets = sorted(rng.sample(range(total), min(count, total)))
    return [_at_offset(start_surah, start_ayah, offset) for offset in offsets]


def pick_ayah(user_id: int, span, local_date) -> Optional[Tuple[int, int]]:
    """The single ayah to test out of `span`, or None if the span holds none."""
    picked = pick_ayahs(user_id, span, local_date, 1)
    return picked[0] if picked else None
