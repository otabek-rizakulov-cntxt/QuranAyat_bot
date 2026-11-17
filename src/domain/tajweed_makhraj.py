"""Makhraj (articulation points) for the 3D letter screens (docs/MAKHRAJ_3D_PLAN.md).

data/tajweed/makhraj.json holds the 17 makhraj, each with a pose for the Mini App's
3D figure (the tongue's midline as 5 points, tip to root, plus the jaw, lips, soft
palate and throat), and the 28 letters, each pointing at its makhraj with optional
layers (`heavy`, `round`, `nasal`). Two extra screens follow the letters: the madd
letters (jawf) and ghunna (khayshum). That's 30 screens, shown one at a time.

Each screen's sound is a span of its Muallimi soniy lesson: a letter lesson opens
with the letter and its three vowels, so by default the clip is that lesson's first
Arabic row (P2 timings), when it is timed and 1.5-12 s long. `clip` [start, end] in
the JSON overrides it; a screen with no usable clip just has no sound.
"""

import json
import os
from typing import Dict, List, NamedTuple, Optional, Tuple

from domain import tajweed_lessons, tajweed_practice
from domain.uz_translit import to_cyrillic

_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "tajweed", "makhraj.json")

REGIONS = ("jawf", "throat", "tongue", "lips", "nose")
CONTACTS = (
    "cavity",
    "glottis",
    "pharynx-mid",
    "uvula",
    "velum-back",
    "velum-front",
    "palate-mid",
    "molars-side",
    "alveolar-wide",
    "alveolar",
    "alveolar-back",
    "incisor-root",
    "incisor-gap",
    "incisor-edge",
    "lip-teeth",
    "lips",
    "nasal",
)
AIRFLOWS = ("oral", "nasal", "hiss", "none")
POSE_SCALARS = (
    "tongue_side",
    "jaw",
    "lips_close",
    "lips_round",
    "lip_to_teeth",
    "velum",
    "pharynx",
)
LAYERS = ("heavy", "round", "nasal")
CLIP_MIN, CLIP_MAX = 1.5, 12.0

# Which screen a rules-track makhraj lesson opens.
_LESSON_SCREENS = {
    "maxraj-kirish": "ا",
    "maxraj-bogiz": "ا",
    "maxraj-til": "ت",
    "maxraj-lab": "ب",
    "maxraj-javf-xayshum": "madd",
}


class Makhraj(NamedTuple):
    id: str
    region: str
    name: str
    body: str
    contact: str
    airflow: str
    pose: dict


class Screen(NamedTuple):
    key: str  # the letter, or "madd" / "ghunna"
    glyph: str
    title: str  # the letter's name (Qof) or the screen's title
    makhraj: str
    layers: Dict[str, float]
    lesson: str  # the Muallimi lesson it comes from (ms-NNN)
    clip: Optional[Tuple[float, float]]  # seconds in that lesson's mp3
    note: Optional[str]


_raw: Optional[dict] = None


def _data() -> dict:
    global _raw
    if _raw is None:
        with open(_PATH, encoding="utf-8") as fp:
            _raw = json.load(fp)
    return _raw


def _script(lang: str):
    return to_cyrillic if lang == "uz-Cyrl" else (lambda s: s)


def makhraj_list(lang: str = "uz") -> List[Makhraj]:
    tr = _script(lang)
    return [
        Makhraj(
            m["id"],
            m["region"],
            tr(m["name_uz"]),
            tr(m["body_uz"]),
            m["contact"],
            m["airflow"],
            m["pose"],
        )
        for m in _data()["makhraj"]
    ]


def letter_lesson(letter: str) -> Optional[str]:
    """The Muallimi lesson that teaches this letter (lessons 2-29, in the book's order)."""
    i = tajweed_practice.LETTERS.find(letter)
    return "ms-%03d" % (i + 2) if i >= 0 else None


def default_clip(lesson_id: str) -> Optional[Tuple[float, float]]:
    """The lesson's first Arabic row, if it is timed and of a usable length."""
    for line in tajweed_lessons.audio_timings(lesson_id):
        if line.kind != "ar":
            continue
        if line.start is None or line.end is None:
            return None
        return (line.start, line.end) if CLIP_MIN <= line.end - line.start <= CLIP_MAX else None
    return None


def _letter_names(lang: str) -> Dict[str, str]:
    names = {}
    for x in tajweed_lessons.audio_lessons(lang):
        if 2 <= x.n <= 29:
            name = x.title
            for suffix in (" harfi", " ҳарфи"):
                name = name.replace(suffix, "")
            names[tajweed_practice.LETTERS[x.n - 2]] = name
    return names


def screens(lang: str = "uz") -> List[Screen]:
    """The 30 screens in order: the 28 letters (alphabet order), madd, ghunna."""
    tr, names, out = _script(lang), _letter_names(lang), []
    for x in _data()["letters"]:
        lesson = letter_lesson(x["letter"])
        clip = tuple(x["clip"]) if x.get("clip") else default_clip(lesson)
        out.append(
            Screen(
                x["letter"],
                x["letter"],
                names.get(x["letter"], x["letter"]),
                x["makhraj"],
                x.get("layers", {}),
                lesson,
                clip,
                tr(x["note_uz"]) if x.get("note_uz") else None,
            )
        )
    for x in _data()["extra"]:
        clip = tuple(x["clip"]) if x.get("clip") else default_clip(x["lesson"])
        out.append(
            Screen(
                x["id"],
                x["glyph"],
                tr(x["title_uz"]),
                x["makhraj"],
                x.get("layers", {}),
                x["lesson"],
                clip,
                tr(x["note_uz"]) if x.get("note_uz") else None,
            )
        )
    return out


def screen_index(key: str) -> Optional[int]:
    for i, s in enumerate(screens()):
        if s.key == key:
            return i
    return None


def lesson_screen(lesson_id: str) -> Optional[int]:
    """The screen a lesson's 🦷 button opens: its letter (lessons 2-29), or the start
    of its region for the rules-track makhraj lessons; None for other lessons."""
    if lesson_id in _LESSON_SCREENS:
        return screen_index(_LESSON_SCREENS[lesson_id])
    for i, s in enumerate(screens()):
        if s.lesson == lesson_id and len(s.key) == 1:
            return i
    return None


def reset_for_tests() -> None:
    global _raw
    _raw = None
