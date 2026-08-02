# Cross-surah reference parsing for hifz targets.
#
# `main.parse_ayah_range` is single-surah by construction — "67:1-8" -> (67, 1, 8)
# — which is the right shape for the reader, where a range is one combined audio
# and one keyboard. It is the wrong shape here: a plan target of kind `range` may
# span surahs ("67:1-68:5"), and *every* juz target does (juz 30 runs 78:1-114:6).
# So this module parses into (start_surah, start_ayah, end_surah, end_ayah).
#
# `parse_ayah_range` is deliberately left alone: it is pinned by
# tests/test_parsing.py and by every reader path in main.py.

import re
from dataclasses import dataclass
from typing import Optional, Tuple

from modules import Quran

__all__ = [
    "Ref", "parse_reference", "parse_range", "surah_ref", "juz_ref", "page_ref",
    "ayah_count", "format_ref", "contains", "clamp_to_quran",
]

# Kinds mirror `plan.target_kind` in the data model, plus "page" for the drill
# unit the plan generator widens to.
KIND_SURAH = "surah"
KIND_JUZ = "juz"
KIND_PAGE = "page"
KIND_RANGE = "range"


@dataclass(frozen=True)
class Ref:
    """A validated, normalized span of the Qur'an.

    `start` never follows `end` in mushaf order, and both ends are real ayahs.
    `kind` records how it was expressed so a plan can say "Juz 30" rather than
    "78:1-114:6"; `n` carries the juz/page number for those kinds.
    """
    kind: str
    start_surah: int
    start_ayah: int
    end_surah: int
    end_ayah: int
    n: Optional[int] = None

    @property
    def start(self) -> Tuple[int, int]:
        return self.start_surah, self.start_ayah

    @property
    def end(self) -> Tuple[int, int]:
        return self.end_surah, self.end_ayah

    def as_tuple(self) -> Tuple[int, int, int, int]:
        """(start_surah, start_ayah, end_surah, end_ayah) — the storage shape."""
        return self.start_surah, self.start_ayah, self.end_surah, self.end_ayah

    def count(self) -> int:
        """How many ayahs the span covers."""
        return ayah_count(*self.as_tuple())

    def is_single_surah(self) -> bool:
        return self.start_surah == self.end_surah


# "67:1-68:5" / "67.1 - 68.5" — two surah:ayah pairs joined by a dash.
_CROSS = re.compile(
    r"^/?(\d{1,3})\s*[:.;,]\s*(\d{1,3})\s*[-–—]\s*(\d{1,3})\s*[:.;,]\s*(\d{1,3})$")
# "67:1-8" — one surah, two ayah numbers.
_WITHIN = re.compile(r"^/?(\d{1,3})\s*[:.;, ]\s*(\d{1,3})\s*[-–—]\s*(\d{1,3})$")
# "67:5" — a single ayah.
_SINGLE = re.compile(r"^/?(\d{1,3})\s*[:.;, ]\s*(\d{1,3})$")
# "67" — a whole surah.
_SURAH = re.compile(r"^/?(\d{1,3})$")
# "juz 30", "juz30", "j30", "30 juz"
_JUZ = re.compile(r"^/?(?:juz|j)\s*(\d{1,2})$|^(\d{1,2})\s*juz$", re.IGNORECASE)
# "page 604", "p604", "604 page"
_PAGE = re.compile(r"^/?(?:page|pg|p)\s*(\d{1,3})$|^(\d{1,3})\s*page$", re.IGNORECASE)


def _clean(text: str) -> str:
    return (text or "").strip()


def surah_ref(surah: int) -> Optional[Ref]:
    """The whole of surah `surah`, or None if there is no such surah."""
    if not 1 <= surah <= 114:
        return None
    return Ref(KIND_SURAH, surah, 1, surah, Quran.get_surah_length(surah), n=surah)


def juz_ref(n: int) -> Optional[Ref]:
    """The span of juz `n` (1-30), or None if out of range."""
    span = Quran.juz_range(n)
    if span is None:
        return None
    return Ref(KIND_JUZ, *span, n=n)


def page_ref(n: int) -> Optional[Ref]:
    """The span of mushaf page `n` (1-604), or None if out of range."""
    span = Quran.page_range(n)
    if span is None:
        return None
    return Ref(KIND_PAGE, *span, n=n)


def parse_reference(text: str) -> Optional[Ref]:
    """Parse a hifz target reference, or None if it doesn't parse or doesn't exist.

    Understood forms::

        67          whole surah          -> 67:1-67:30
        67:1-8      within one surah     -> 67:1-67:8
        67:1-68:5   across surahs        -> 67:1-68:5
        67:5        a single ayah        -> 67:5-67:5
        juz 30 / j30 / 30 juz
        page 604 / p604 / 604 page

    Every result is validated against `Quran.exists`, and a reversed range is
    swapped rather than rejected — someone typing "68:5-67:1" meant the span.
    """
    text = _clean(text)
    if not text:
        return None

    match = _JUZ.match(text)
    if match is not None:
        return juz_ref(int(match.group(1) or match.group(2)))

    match = _PAGE.match(text)
    if match is not None:
        return page_ref(int(match.group(1) or match.group(2)))

    match = _CROSS.match(text)
    if match is not None:
        s1, a1, s2, a2 = (int(g) for g in match.groups())
        return _validated(KIND_RANGE, s1, a1, s2, a2)

    match = _WITHIN.match(text)
    if match is not None:
        surah, start, end = (int(g) for g in match.groups())
        if end < start:
            start, end = end, start
        return _validated(KIND_RANGE, surah, start, surah, end)

    match = _SINGLE.match(text)
    if match is not None:
        surah, ayah = int(match.group(1)), int(match.group(2))
        return _validated(KIND_RANGE, surah, ayah, surah, ayah)

    match = _SURAH.match(text)
    if match is not None:
        return surah_ref(int(match.group(1)))

    return None


def parse_range(text: str) -> Optional[Tuple[int, int, int, int]]:
    """`parse_reference` reduced to the normalized 4-tuple, or None."""
    ref = parse_reference(text)
    return ref.as_tuple() if ref is not None else None


def _validated(kind: str, s1: int, a1: int, s2: int, a2: int) -> Optional[Ref]:
    """Build a Ref after checking both ends exist, ordering them if reversed."""
    if not (Quran.exists(s1, a1) and Quran.exists(s2, a2)):
        return None
    if (s2, a2) < (s1, a1):
        s1, a1, s2, a2 = s2, a2, s1, a1
    return Ref(kind, s1, a1, s2, a2)


def ayah_count(start_surah: int, start_ayah: int,
               end_surah: int, end_ayah: int) -> int:
    """Ayahs in an inclusive cross-surah span; 0 if the span is inverted.

    Counted from the surah lengths rather than by walking, so a juz costs the
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


def contains(ref: Ref, surah: int, ayah: int) -> bool:
    """Whether ayah `surah:ayah` falls inside `ref`."""
    return ref.start <= (surah, ayah) <= ref.end


def clamp_to_quran(surah: int, ayah: int) -> Tuple[int, int]:
    """Nearest real ayah to `surah:ayah`, for arithmetic that ran off an end."""
    surah = max(1, min(114, surah))
    return surah, max(1, min(Quran.get_surah_length(surah), ayah))


def format_ref(ref: Ref) -> str:
    """Compact ASCII form: "67:1-8", "67:1-68:5", "67:5".

    Deliberately un-localized — it is the machine-ish half of a message whose
    prose comes from the string table, and it is what `{ref}` placeholders are
    filled with.
    """
    if ref.start == ref.end:
        return "%d:%d" % ref.start
    if ref.is_single_surah():
        return "%d:%d-%d" % (ref.start_surah, ref.start_ayah, ref.end_ayah)
    return "%d:%d-%d:%d" % ref.as_tuple()
