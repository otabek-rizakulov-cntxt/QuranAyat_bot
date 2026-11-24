"""Tajweed colours in the Qur'an reader (docs/TAJWEED_NEXT_PLAN.md §3).

The reader shows the Uthmani text with each rule's spans coloured; a tap on a span
explains the rule and links to the rules-track lesson ("Qoidalar") that teaches it.
The spans index the Uthmani text (domain.tajweed), not data/translations/ar.txt, so the
reader switches to that text while the colours are on.
"""

import json
import os
from typing import Dict, List, Tuple

from domain import tajweed, tajweed_lessons
from domain.uz_translit import to_cyrillic

_HINTS = os.path.join(tajweed._DIR, "rule_hints.json")

# The order rules are numbered in the per-surah files (a span stores its rule's index).
ORDER: Tuple[str, ...] = tuple(tajweed.RULES)

# Rules no rules-track lesson lists in its `rules`, and the lesson that teaches them.
_EXTRA_LESSON = {"madd_246": "mad-oriz-lin"}

# The languages the hints are written in; every other UI language gets English.
HINT_LANGS = ("en", "uz", "uz-Cyrl")

_hints: Dict[str, dict] = {}


def rule_lesson(rule: str) -> str:
    """The rules-track lesson that teaches `rule`."""
    if rule in _EXTRA_LESSON:
        return _EXTRA_LESSON[rule]
    for lesson in tajweed_lessons.lessons("uz"):
        if rule in lesson.rules:
            return lesson.id
    return ""


def _raw_hints() -> dict:
    if not _hints:
        with open(_HINTS, encoding="utf-8") as fp:
            _hints.update(json.load(fp)["rules"])
    return _hints


def rules_doc(lang: str) -> List[dict]:
    """The rules in ORDER, with their name and hint in `lang` and their lesson."""
    source = "uz" if lang in ("uz", "uz-Cyrl") else "en"
    tr = to_cyrillic if lang == "uz-Cyrl" else (lambda s: s)
    out = []
    for rule in ORDER:
        text = _raw_hints()[rule][source]
        out.append(
            {
                "id": rule,
                "name": tr(text["name"]),
                "hint": tr(text["hint"]),
                "lesson": rule_lesson(rule),
            }
        )
    return out




def _bismillah_cut(surah: int, ayah: int, body: str) -> int:
    """Where ayah 1's text starts after the Bismillah this text prefixes to it (every
    surah but 1 and 9). The reader shows the Bismillah on its own line, as it does
    with the usual text."""
    if ayah != 1 or surah in (1, 9):
        return 0
    rahim = tajweed.text(1, 1).split(" ")[-1] + " "  # spelled exactly as in this text
    end = body.find(rahim)
    return end + len(rahim) if 0 <= end < 40 else 0


def surah_doc(surah: int) -> List[list]:
    """Each ayah as [uthmani text, [[rule index, start, end], ...]] (code points)."""
    index = {r: i for i, r in enumerate(ORDER)}
    out = []
    ayah = 1
    while True:
        try:
            body = tajweed.text(surah, ayah)
        except KeyError:
            break
        cut = _bismillah_cut(surah, ayah, body)
        spans = [
            [index[r], a - cut, b - cut]
            for r, a, b in tajweed.spans(surah, ayah)
            if r in index and a >= cut
        ]
        out.append([body[cut:], spans])
        ayah += 1
    return out
