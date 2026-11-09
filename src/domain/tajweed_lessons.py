"""The tajweed lessons (data/tajweed/lessons.uz.json), ready to show.

Lessons are written in Uzbek Latin; `uz-Cyrl` is generated with domain.uz_translit.
Each lesson's `content_hash` covers everything a reviewer approved (title, body,
examples), so editing a lesson after approval turns it back into a draft without
anyone having to remember to reset it (docs/TAJWEED_PLAN.md §6).
"""

import hashlib
import json
import os
from typing import Dict, List, NamedTuple, Optional, Tuple

from domain import tajweed
from domain.uz_translit import to_cyrillic

_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "tajweed",
    "lessons.uz.json",
)
AUTO_EXAMPLES = 3  # examples per lesson when the lesson says "auto"
LANGS = ("uz", "uz-Cyrl")

Example = Tuple[int, int, Tuple[str, ...]]  # (surah, ayah, rules to mark)


class Lesson(NamedTuple):
    id: str
    unit: str
    title: str
    rules: Tuple[str, ...]
    body: Tuple[str, ...]  # paragraphs, Telegram HTML subset (<b>, <i>, <u>)
    examples: Tuple[Example, ...]
    content_hash: str


class Unit(NamedTuple):
    id: str
    title: str


_cache: Dict[str, Tuple[Tuple[Unit, ...], Tuple[Lesson, ...]]] = {}


def _examples(raw, rules: Tuple[str, ...]) -> Tuple[Example, ...]:
    if raw == "auto":
        out, seen = [], set()
        # Round-robin over the lesson's rules so a two-rule lesson shows both.
        per_rule = [tajweed.examples(r, AUTO_EXAMPLES * 2) for r in rules]
        for i in range(AUTO_EXAMPLES * 2):
            for rule, exs in zip(rules, per_rule):
                if i < len(exs) and exs[i] not in seen and len(out) < AUTO_EXAMPLES:
                    seen.add(exs[i])
                    out.append((exs[i][0], exs[i][1], (rule,)))
        return tuple(out)
    return tuple((s, a, rules) for s, a in raw)


def _hash(lesson: dict, examples: Tuple[Example, ...]) -> str:
    payload = json.dumps(
        [lesson["title"], lesson["body"], [list(e[:2]) + list(e[2]) for e in examples]],
        ensure_ascii=False,
    )
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def _load(lang: str) -> Tuple[Tuple[Unit, ...], Tuple[Lesson, ...]]:
    if lang not in _cache:
        with open(_PATH, encoding="utf-8") as fp:
            raw = json.load(fp)
        tr = to_cyrillic if lang == "uz-Cyrl" else (lambda s: s)
        units = tuple(Unit(u["id"], tr(u["title"])) for u in raw["units"])
        lessons = []
        for item in raw["lessons"]:
            rules = tuple(item["rules"])
            examples = _examples(item["examples"], rules)
            lessons.append(
                Lesson(
                    id=item["id"],
                    unit=item["unit"],
                    title=tr(item["title"]),
                    rules=rules,
                    body=tuple(tr(p) for p in item["body"]),
                    examples=examples,
                    # one hash for both scripts: approval is of the Latin source
                    content_hash=_hash(item, examples),
                )
            )
        _cache[lang] = (units, tuple(lessons))
    return _cache[lang]


def units(lang: str = "uz") -> Tuple[Unit, ...]:
    return _load(lang)[0]


def lessons(lang: str = "uz") -> Tuple[Lesson, ...]:
    return _load(lang)[1]


def lesson(lesson_id: str, lang: str = "uz") -> Optional[Lesson]:
    return next((x for x in lessons(lang) if x.id == lesson_id), None)


def neighbours(lesson_id: str, ids: List[str]) -> Tuple[Optional[str], Optional[str]]:
    """Previous and next lesson ids within `ids` (the lessons this user may see)."""
    if lesson_id not in ids:
        return None, None
    i = ids.index(lesson_id)
    return (ids[i - 1] if i else None), (ids[i + 1] if i + 1 < len(ids) else None)


def reset_for_tests() -> None:
    _cache.clear()
