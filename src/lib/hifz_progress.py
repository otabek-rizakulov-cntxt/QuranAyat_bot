# Hifz percentages, derived from the interval store and nothing else (spec C2).
#
# There is no `memorized_count` column anywhere and there never will be. Every
# number `/progress` shows is recomputed from `hifz_interval` against the corpus
# the reader already ships (`Quran.surah_lengths`, `Quran.juz_range`). A stored
# counter would need to be kept in step with three writers — marking a drill
# done, `/forgot`, and the merge that silently absorbs a neighbour — and the
# first time one of them missed, the user's percentage would be wrong forever
# with nothing to reconcile it against. Arithmetic over the rows cannot drift:
# the rows *are* the truth.
#
# The counting is cheap enough to do on every read. A user who has memorized the
# whole Qur'an has at most 114 intervals; 30 juz intersections over 114 spans is
# a few thousand integer comparisons.
#
# Everything here returns numbers in dataclasses, never sentences. `/progress`
# renders "Al-Mulk 8/30 · 27% · juz 29 4% · Qur'an 0.4%" from the string table,
# where the surah name, the separators and the "%" itself are all translatable —
# a percent sign formatted in here would be a hard-coded English typographic
# convention baked into a module that has no business knowing the user's locale.

import math
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

from hifz.refs import Ref, contains, juz_ref, surah_ref
from modules import Quran

__all__ = [
    "TOTAL_AYAHS", "Progress", "SurahProgress", "JuzProgress", "ProgressSummary",
    "round_percent", "format_percent",
    "surah_progress", "juz_progress", "quran_progress",
    "started_surahs", "started_juzs", "summarize", "load_summary",
]

# 6236. Summed from the corpus rather than written down, so it can never disagree
# with the surah lengths the per-surah percentages are computed against.
TOTAL_AYAHS = sum(Quran.surah_lengths)


# --- The rounding rule ---------------------------------------------------------
#
# Three properties matter more than decimal places, because this number is the
# thing that makes someone open the bot again tomorrow:
#
#   1. **Whole percents by default.** "27%" is what the spec asks for (8/30 =
#      26.67) and what a person can hold in their head. Half rounds up, so 26.5
#      is 27 — Python's built-in `round` is banker's rounding and would say 26.
#   2. **Non-zero progress is never shown as 0%.** Ten ayahs is 0.16% of the
#      Qur'an; reporting "0%" to someone who has genuinely memorized something is
#      the single most demotivating thing this module could do. Below 1% we fall
#      to one decimal and floor at 0.1.
#   3. **100% means finished.** 430 of a 431-ayah juz is 99.77%, and rounding
#      that to "100%" would tell a user they had completed a juz they have not.
#      Anything short of complete is capped at 99.
#
# Symmetric at both ends, then: the only way to see 0 is to have memorized
# nothing, and the only way to see 100 is to have memorized all of it.

def round_percent(fraction: float) -> float:
    """`fraction` (0.0-1.0) as a percentage, rounded per the rule above.

    Returns a float that is whole (27.0) except in the sub-1% band (0.4). Use
    `format_percent` to get the token that goes into a `{pct}` placeholder.
    """
    if fraction <= 0:
        return 0.0
    if fraction >= 1:
        return 100.0
    percent = fraction * 100.0
    if percent < 1:
        return max(0.1, round(percent, 1))
    return float(min(99, max(1, math.floor(percent + 0.5))))


def format_percent(fraction: float) -> str:
    """The rounded percentage as a bare token — "27", "0.4", "100".

    No percent sign: `/progress` gets that from `progress_surah_line` and friends
    so a locale that writes "٪" first, or spaces it, can.
    """
    percent = round_percent(fraction)
    return "%g" % percent


class _Ratio:
    """Derived-percentage behaviour shared by every progress dataclass.

    Not a dataclass itself and it declares no fields: it exists so `surah`, `juz`
    and the whole-Qur'an total can each keep the field order that reads best at
    their call sites while `done`/`total` mean exactly one thing everywhere.
    """

    done: int
    total: int

    @property
    def fraction(self) -> float:
        """Memorized share as an exact 0.0-1.0 ratio, unrounded.

        The honest number. Sort and compare on this; show `percent`.
        """
        return (self.done / self.total) if self.total else 0.0

    @property
    def percent(self) -> float:
        """`fraction` put through `round_percent` — what the user is told."""
        return round_percent(self.fraction)

    @property
    def percent_text(self) -> str:
        """`percent` as the bare token for a `{pct}` placeholder."""
        return format_percent(self.fraction)

    @property
    def is_started(self) -> bool:
        return self.done > 0

    @property
    def is_complete(self) -> bool:
        return self.total > 0 and self.done >= self.total

    @property
    def remaining(self) -> int:
        """Ayahs still to memorize — what a "keep going" line counts down."""
        return max(0, self.total - self.done)


@dataclass(frozen=True)
class Progress(_Ratio):
    """Memorized-vs-total for a span the caller already knows the identity of."""

    done: int
    total: int


@dataclass(frozen=True)
class SurahProgress(_Ratio):
    """One surah's share. `{name}` is resolved by the renderer, not here."""

    surah: int
    done: int
    total: int


@dataclass(frozen=True)
class JuzProgress(_Ratio):
    """One juz's share. Juz spans cross surahs, so `done` is an intersection."""

    juz: int
    done: int
    total: int


@dataclass(frozen=True)
class ProgressSummary:
    """Everything `/progress` needs in one read of the interval store.

    `focus` and `focus_juz` are the one-liner ("Al-Mulk 8/30 · 27% · juz 29 4% ·
    Qur'an 0.4%"); `surahs` and `juzs` are the breakdown beneath it, restricted to
    what the user has actually started so a fresh user does not scroll past 114
    zeroes. `quran` is always present, and is 0/6236 for a user with nothing.
    """

    quran: Progress
    surahs: Tuple[SurahProgress, ...]
    juzs: Tuple[JuzProgress, ...]
    focus: Optional[SurahProgress] = None
    focus_juz: Optional[JuzProgress] = None

    @property
    def is_empty(self) -> bool:
        """Nothing marked at all — `/progress` shows `progress_empty` instead."""
        return self.quran.done == 0


# --- Intersecting intervals with a span ----------------------------------------

def _spans(intervals: Iterable) -> List[Tuple[int, int, int]]:
    """Normalize whatever the caller passed into (surah, start, end) triples.

    `HifzInterval` rows are the everyday input, but plain tuples are accepted so
    a test — or a preview of a plan day that has not been written yet — can ask
    "what would this look like" without minting rows.
    """
    out = []
    for interval in intervals or ():
        if isinstance(interval, (tuple, list)):
            surah, start, end = interval[0], interval[1], interval[2]
        else:
            surah, start, end = (interval.surah, interval.start_ayah,
                                 interval.end_ayah)
        if start > end:
            start, end = end, start
        out.append((int(surah), int(start), int(end)))
    return out


def _surah_of(interval) -> int:
    """The surah number of one interval, whichever shape it arrived in."""
    return int(interval[0] if isinstance(interval, (tuple, list)) else interval.surah)


def _clip(ref: Ref, surah: int, start: int, end: int) -> Optional[Tuple[int, int]]:
    """[start, end] of `surah` narrowed to the part lying inside `ref`, or None.

    This is the only piece of real geometry in the module, and it is here because
    a juz is a cross-surah span while an interval is per-surah: juz 1 runs
    1:1-2:141, so the user's single 2:1-286 row contributes 141 ayahs to juz 1 and
    the rest to juz 2 and 3. Membership is asked of `hifz.refs.contains` rather
    than re-derived, so mushaf ordering is defined in exactly one place.

    Clipping through here also makes the module robust to a row that runs past the
    end of its surah: `surah_ref` stops at the real last ayah, so a bad 67:1-999
    row can inflate `count_ayahs` but can never push a percentage over 100.
    """
    if not (ref.start_surah <= surah <= ref.end_surah):
        return None
    low, high = start, end
    if not contains(ref, surah, low):
        # The interval opens before the ref does. That can only still overlap if
        # the ref itself opens inside this surah, at a later ayah.
        if surah != ref.start_surah or (surah, low) > ref.start:
            return None
        low = ref.start_ayah
    if not contains(ref, surah, high):
        # Mirror image: the interval runs past the ref's close.
        if surah != ref.end_surah or (surah, high) < ref.end:
            return None
        high = ref.end_ayah
    return (low, high) if low <= high else None


def _covered(ref: Ref, spans: Sequence[Tuple[int, int, int]]) -> int:
    """How many ayahs of `ref` the (non-overlapping) `spans` cover.

    A plain sum is only correct because the store guarantees the intervals are
    disjoint — that invariant is what lets every percentage here be one pass of
    addition instead of a union.
    """
    total = 0
    for surah, start, end in spans:
        clipped = _clip(ref, surah, start, end)
        if clipped is not None:
            total += clipped[1] - clipped[0] + 1
    return total


# --- The public readings -------------------------------------------------------

def surah_progress(intervals: Iterable, surah: int) -> SurahProgress:
    """How much of `surah` the intervals cover. 0/0 for a surah that isn't real."""
    ref = surah_ref(surah)
    if ref is None:
        return SurahProgress(surah=surah, done=0, total=0)
    return SurahProgress(surah=surah, done=_covered(ref, _spans(intervals)),
                         total=ref.count())


def juz_progress(intervals: Iterable, juz: int) -> JuzProgress:
    """How much of juz `juz` (1-30) the intervals cover, across surah boundaries."""
    ref = juz_ref(juz)
    if ref is None:
        return JuzProgress(juz=juz, done=0, total=0)
    return JuzProgress(juz=juz, done=_covered(ref, _spans(intervals)),
                       total=ref.count())


def quran_progress(intervals: Iterable) -> Progress:
    """How much of the whole Qur'an the intervals cover, out of 6236.

    Summed per surah rather than straight off the rows so the same clipping that
    protects the surah percentages protects this one.
    """
    done = 0
    for surah, start, end in _spans(intervals):
        ref = surah_ref(surah)
        if ref is None:
            continue
        clipped = _clip(ref, surah, start, end)
        if clipped is not None:
            done += clipped[1] - clipped[0] + 1
    return Progress(done=done, total=TOTAL_AYAHS)


def started_surahs(intervals: Iterable) -> List[SurahProgress]:
    """Every surah with at least one memorized ayah, in mushaf order.

    Only started surahs: a breakdown that listed all 114 would bury the three the
    user cares about under a hundred zeroes.
    """
    spans = _spans(intervals)
    surahs = sorted({surah for surah, _, _ in spans if surah_ref(surah) is not None})
    return [surah_progress(spans, surah) for surah in surahs]


def started_juzs(intervals: Iterable) -> List[JuzProgress]:
    """Every juz with at least one memorized ayah, ascending.

    All 30 are tested because there is no cheap way to go from a per-surah
    interval to "which juz did that land in" for a span that straddles a boundary
    — and 30 intersections is nothing.
    """
    spans = _spans(intervals)
    found = []
    for n in range(1, Quran.JUZ_COUNT + 1):
        progress = juz_progress(spans, n)
        if progress.is_started:
            found.append(progress)
    return found


def _recency_key(interval):
    """Sort key for "which interval did the user touch last".

    `marked_at` first, but it cannot be the only term: the clock is only good to a
    microsecond and two writes inside one handler routinely land on the identical
    timestamp, which would make the focus of `/progress` depend on how busy the
    machine was. The row id breaks those ties and is exactly the right thing to
    break them with — it comes from a monotonic sequence in both store legs, and a
    merge or a split always inserts a *new* row, so the highest id in a surah is
    always the most recently written one there.

    The leading flag keeps a timestamped row ahead of an untimestamped one and
    stops a datetime ever being compared against None. Raw tuples have neither
    field and fall back to mushaf order, which is at least stable.
    """
    if isinstance(interval, (tuple, list)):
        return (False, None, -int(interval[0]))
    marked_at = getattr(interval, "marked_at", None)
    row_id = getattr(interval, "id", None)
    return (marked_at is not None, marked_at, row_id if row_id is not None else 0)


def _focus_surah(intervals: Iterable) -> Optional[int]:
    """Which surah the one-line summary should name.

    The most recently marked one — the line is a reaction to work the user just
    did, so it should be about the thing they just did. `marked_at` survives a
    split and is refreshed by a merge, so "most recent" tracks activity rather
    than the original learning date.
    """
    candidates = [interval for interval in (intervals or ())
                  if surah_ref(_surah_of(interval)) is not None]
    if not candidates:
        return None
    return _surah_of(max(candidates, key=_recency_key))


def summarize(intervals: Iterable,
              focus_surah: Optional[int] = None) -> ProgressSummary:
    """Everything `/progress` renders, from one list of intervals.

    Pass `focus_surah` when there is an obvious subject — the surah of the drill
    just completed, or the target of the active plan — and the summary will lead
    with it even if the user last touched something else. Left out, it picks the
    most recently marked surah.
    """
    spans = _spans(intervals)
    surahs = started_surahs(spans)
    juzs = started_juzs(spans)
    quran = quran_progress(spans)

    if focus_surah is None:
        focus_surah = _focus_surah(intervals)
    focus = None
    focus_juz = None
    if focus_surah is not None and surah_ref(focus_surah) is not None:
        focus = surah_progress(spans, focus_surah)
        # The juz of the *last* ayah marked in that surah: the one the user is
        # working through now, not the one they started in a month ago.
        marked = [(start, end) for surah, start, end in spans if surah == focus_surah]
        if marked:
            last_ayah = min(max(end for _, end in marked),
                            Quran.get_surah_length(focus_surah))
            focus_juz = juz_progress(spans, Quran.juz_of(focus_surah, last_ayah))

    return ProgressSummary(quran=quran, surahs=tuple(surahs), juzs=tuple(juzs),
                           focus=focus, focus_juz=focus_juz)


async def load_summary(store, user_id: int,
                       focus_surah: Optional[int] = None) -> ProgressSummary:
    """`summarize` over everything `user_id` has marked. One store round trip.

    The whole interval set is read even when only one surah is being shown,
    because the summary always carries the whole-Qur'an line and a per-surah query
    could not produce it.
    """
    return summarize(await store.hifz.list_intervals(user_id), focus_surah)
