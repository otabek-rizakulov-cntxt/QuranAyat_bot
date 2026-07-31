# BismillahBot -- Explore the Holy Qur'an on Telegram
# Copyright (C) 1436-1438 AH  Rahiel Kasim
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import re
import xml.etree.ElementTree as ET
from bisect import bisect_right
from random import randint
from typing import Tuple

from locales.languages import DEFAULT_LANG

# translations/ lives at the repo root (next to en.ahmedraza, quran-data.xml).
# Resolve it absolutely from this file so it works regardless of the process cwd.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRANSLATIONS_DIR = os.path.join(_REPO_ROOT, "translations")

# tanzil's quran-data.xml, parsed once at import. Resolved absolutely for the same
# reason TRANSLATIONS_DIR is: the corpus must load whatever the process cwd is.
_QURAN_DATA = ET.parse(os.path.join(_REPO_ROOT, "quran-data.xml")).getroot()


def _division_marks(tag: str) -> tuple:
    """Start position of every division of one kind, in mushaf order.

    Returns ((sura, aya), ...) — e.g. `_division_marks("pages")` has 604 entries,
    the first ayah of each page. A division runs from its own mark to the ayah
    before the next one's, which is what `Quran._division_range` reconstructs.

    (sura, aya) tuples sort in mushaf order, so these are also directly bisectable
    to answer "which division is this ayah in?".
    """
    return tuple((int(e.attrib["sura"]), int(e.attrib["aya"]))
                 for e in _QURAN_DATA.find(tag))


def parse_quran(filename: str):
    """Parse Quran text files (with ayah numbers) from http://tanzil.net."""
    quran = []
    surah = []
    s = 1

    def process_verse(verse: str):
        """Add verse and replace for Arabic ligatures (salawat)"""
        return (verse.strip()
                .replace("– peace and blessings be upon him", "ﷺ‎"))

    with open(filename, "r") as f:
        for line in f.readlines():
            if line == "\n":
                continue
            if line.startswith("#"):
                break
            verse = line.split("|")
            assert len(verse) == 3
            if int(verse[0]) == s:
                surah.append(process_verse(verse[2]))
            else:
                quran.append(surah)
                surah = [process_verse(verse[2])]
                s += 1
    quran.append(surah)
    assert sum([len(s) for s in quran]) == 6236, "Missing verses!"
    return quran


def parse_quran_tafsir(filename: str = "Al_Jalalain_Eng.txt"):
    """Parse tafsir al-Jalalayn from http://www.altafsir.com/Al-Jalalayn.asp, after
    that PDF was processed with `pdftotext -nopgbrk Al_Jalalain_Eng.pdf`.
    """
    quran = []
    surah = []
    s, v = 1, 1
    in_verse = False
    verse = []

    def add_verse(verse, surah):
        surah.append(" ".join(verse))

    def add_line(line, verse):
        """Add line and replace for Arabic ligatures (salawat)"""
        verse.append(line.strip().replace("(s)", "ﷺ‎"))

    with open(filename, "r") as f:
        for line in f.readlines():
            if line == "\n": continue
            if re.match(r"\d+\w*", line): continue
            elif line.startswith("[%d:%d]" % (s, v)):
                in_verse = True
            elif line.startswith("[%d:%d]" % (s, v + 1)):
                add_verse(verse, surah)
                verse = []
                v += 1
                in_verse = True
            elif line.startswith("[%d:1]" % (s + 1)):
                add_verse(verse, surah)
                verse = []
                quran.append(surah)
                surah = []
                s += 1
                v = 1
                in_verse = True
            elif (line.startswith("Medinese") or line.startswith("Meccan") or
                  line.startswith("[Consists") or  # [Consists end surah 5
                  line.startswith("Mecca, consisting") or  # end surah 73
                  line.startswith("This was revealed")):
                if s == 26 and v == 200:
                    # only line starting with "Meccan" that is part of a verse
                    add_line(line, verse)
                else:
                    in_verse = False
            elif in_verse:
                add_line(line, verse)
    add_verse(verse, surah)
    quran.append(surah)
    assert sum([len(s) for s in quran]) == 6236, "Missing verses!"
    return quran


class Quran:
    """Interface to get ayahs from the Quran."""
    surah_lengths = (7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99, 128, 111, 110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88, 69, 60, 34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37, 35, 38, 29, 18, 45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11, 18, 12, 12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42, 29, 19, 36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11, 11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6)

    surah_names = [s.attrib["tname"] for s in _QURAN_DATA.find("suras")]

    # The mushaf's structural divisions, all from the same quran-data.xml the surah
    # names come from. `pages` and `juzs` back /page and /juz; the other three are
    # exposed for callers that want them but have no command of their own yet.
    pages = _division_marks("pages")        # 604
    juzs = _division_marks("juzs")          # 30
    hizbs = _division_marks("hizbs")        # 240
    manzils = _division_marks("manzils")    # 7
    rukus = _division_marks("rukus")        # 556

    # Ayahs of prostration: (sura, aya, "obligatory" | "recommended").
    sajdas = tuple((int(s.attrib["sura"]), int(s.attrib["aya"]), s.attrib["type"])
                   for s in _QURAN_DATA.find("sajdas"))

    def __init__(self, text: list) -> None:
        """`text` is a list of surahs, each a list of ayah strings (see parse_quran)."""
        self.text = text

    @classmethod
    def from_file(cls, path: str) -> "Quran":
        """Build a Quran from a tanzil-format `surah|ayah|text` file."""
        return cls(parse_quran(path))

    @classmethod
    def from_tafsir(cls, path: str = "Al_Jalalain_Eng.txt") -> "Quran":
        return cls(parse_quran_tafsir(path))

    def get_ayah(self, surah: int, ayah: int) -> str:
        """Get verse by surah and ayah numbers."""
        return self.text[surah - 1][ayah - 1] + " (%d:%d)" % (surah, ayah)

    def get_ayahs(self, surah: int, a: int, b: int) -> str:
        """Get range of Ayahs."""
        return " ".join(self.text[surah - 1][a - 1:b]) + " (%d:%d-%d)" % (surah, a, b)

    def get_ayah_text(self, surah: int, ayah: int) -> str:
        """The ayah alone, with no "(surah:ayah)" suffix.

        `get_ayah` appends the reference because a verse card is read on its own
        and needs to say where it came from. The recall check must not: it shows
        an opening and four continuations, and a reference on the correct one
        would be the answer written next to the question.
        """
        return self.text[surah - 1][ayah - 1]

    def get_ayahs_text(self, surah: int, a: int, b: int) -> str:
        """A range of ayahs joined, with no reference suffix — see get_ayah_text."""
        return " ".join(self.text[surah - 1][a - 1:b])

    @staticmethod
    def get_random_ayah() -> Tuple[int, int]:
        surah = randint(1, 114)
        ayah = randint(1, Quran.get_surah_length(surah))
        return surah, ayah

    @staticmethod
    def get_next_ayah(s: int, a: int) -> Tuple[int, int]:
        length = Quran.get_surah_length(s)
        if a == length:
            s = s + 1 if s < 114 else 1
            a = 1
        else:
            a += 1
        return s, a

    @staticmethod
    def get_previous_ayah(s: int, a: int) -> Tuple[int, int]:
        if a == 1:
            s = s - 1 if s > 1 else 114
            a = Quran.get_surah_length(s)
        else:
            a -= 1
        return s, a

    @staticmethod
    def exists(s: int, a: int) -> bool:
        return 0 < s < 115 and 0 < a <= Quran.get_surah_length(s)

    @staticmethod
    def get_surah_length(surah: int) -> int:
        return Quran.surah_lengths[surah - 1]

    @staticmethod
    def get_surah_name(surah: int) -> str:
        return Quran.surah_names[surah - 1]

    # --- Structural divisions ---------------------------------------------------
    # A page or juz is a *range* of ayahs that routinely crosses a surah boundary
    # (96 of the 604 pages do), so everything here works in (surah, ayah) pairs
    # rather than the single-surah (surah, start, end) shape the rest of the bot
    # uses for ayah ranges.

    PAGE_COUNT = len(pages)
    JUZ_COUNT = len(juzs)

    @staticmethod
    def _division_range(marks: tuple, n: int):
        """(start_surah, start_ayah, end_surah, end_ayah) of the n-th division.

        Divisions are contiguous and gapless, so one ends where the next begins:
        the end is the ayah just before the next mark. The final division has no
        next mark and runs to the last ayah of the Qur'an. Returns None if `n` is
        out of range.
        """
        if not 1 <= n <= len(marks):
            return None
        start_s, start_a = marks[n - 1]
        if n == len(marks):
            end_s = 114
            end_a = Quran.get_surah_length(114)
        else:
            # get_previous_ayah wraps 1:1 -> 114:6, but no mark after the first is
            # ever 1:1, so the step back can never wrap here.
            end_s, end_a = Quran.get_previous_ayah(*marks[n])
        return start_s, start_a, end_s, end_a

    @staticmethod
    def page_range(n: int):
        """The ayah span of mushaf page `n` (1-604), or None if out of range."""
        return Quran._division_range(Quran.pages, n)

    @staticmethod
    def juz_range(n: int):
        """The ayah span of juz `n` (1-30), or None if out of range."""
        return Quran._division_range(Quran.juzs, n)

    @staticmethod
    def _division_of(marks: tuple, s: int, a: int) -> int:
        """1-based index of the division containing ayah s:a.

        (surah, ayah) tuples sort in mushaf order, so the containing division is
        simply the last mark at or before this ayah.
        """
        return bisect_right(marks, (s, a))

    @staticmethod
    def page_of(s: int, a: int) -> int:
        """The mushaf page ayah s:a is on."""
        return Quran._division_of(Quran.pages, s, a)

    @staticmethod
    def juz_of(s: int, a: int) -> int:
        """The juz ayah s:a is in."""
        return Quran._division_of(Quran.juzs, s, a)

    @staticmethod
    def ayahs_between(start: tuple, end: tuple) -> list:
        """Every (surah, ayah) from `start` to `end` inclusive, in mushaf order.

        This is what turns a page or juz into the list of per-ayah media files it
        is made of. Returns [] if `end` precedes `start`.
        """
        if tuple(end) < tuple(start):
            return []
        s, a = start
        last = tuple(end)
        ayahs = []
        while True:
            ayahs.append((s, a))
            if (s, a) == last:
                return ayahs
            s, a = Quran.get_next_ayah(s, a)


class TranslationRegistry:
    """Lazily loads and caches Qur'an translations, one per language.

    Only the default language is preloaded at startup (see preload()); every other
    language is parsed from translations/<code>.txt on first request and then kept
    in memory. This keeps startup fast and memory proportional to the languages
    actually used — important on the 512 MB free instance.
    """
    _cache: dict[str, Quran] = {}

    @classmethod
    def _path(cls, code: str) -> str:
        return os.path.join(TRANSLATIONS_DIR, code + ".txt")

    @classmethod
    def available(cls) -> set[str]:
        """Language codes that have a bundled translation file on disk."""
        try:
            return {f[:-4] for f in os.listdir(TRANSLATIONS_DIR) if f.endswith(".txt")}
        except OSError:
            return set()

    @classmethod
    def is_cached(cls, code: str) -> bool:
        return code in cls._cache

    @classmethod
    def preload(cls, code: str) -> Quran:
        """Parse and cache a language now (called at startup for the default)."""
        cls._cache[code] = Quran.from_file(cls._path(code))
        return cls._cache[code]

    @classmethod
    def get(cls, code: str) -> Quran:
        """Return the translation for `code`, parsing on first use.

        Falls back to the default language if the requested file is missing, so a
        trimmed/partial bundle degrades gracefully instead of erroring.
        """
        cached = cls._cache.get(code)
        if cached is not None:
            return cached
        path = cls._path(code)
        if not os.path.exists(path):
            if code != DEFAULT_LANG:
                return cls.get(DEFAULT_LANG)
            raise FileNotFoundError("Missing default translation: " + path)
        cls._cache[code] = Quran.from_file(path)
        return cls._cache[code]


def make_index():
    """An index of the Surahs in the Quran, formatted to send over Telegram."""
    chapters = Quran.surah_names[:]
    # padding...
    for i in range(9):
        chapters[i] = " " + chapters[i] + " " * (14 - len(chapters[i]))
    for i in range(9, 58):
        chapters[i] += " " * (14 - len(chapters[i]))

    index = []
    left = range(1, 58)
    right = range(58, 115)
    for i, j in zip(left, right):
        index.append("/{} <code>{}</code>/{} {}"
                     .format(i, chapters[i - 1], j, chapters[j - 1]))
    return "\n".join(index)
