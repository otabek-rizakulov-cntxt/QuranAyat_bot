"""Practice for a tajweed lesson: quizzes and reading drills (docs/TAJWEED_PLAN.md P3).

Everything is built from real ayahs and the rule annotations (domain.tajweed), and
is deterministic for a (lesson, seed): the bot rebuilds the same session from its
callback data on every tap, and the Mini App gets the same questions from the API.

Quiz kinds, for lessons that teach an annotated rule:
    name    an ayah with one span marked: which rule is it?
    find    four short ayahs: which one has the rule?
    listen  as `name`, but the ayah is played first (the user's reciter)
    count   an ayah with the rule marked 1-4 times: how many?

Reading drills work for every lesson: a word, with its harakat, from a short ayah,
chosen to show what the lesson teaches (its letter, a shadda, a tanwin, the rule).
"""

import html
import random
from typing import Callable, Dict, List, NamedTuple, Optional, Tuple

from domain import tajweed, tajweed_lessons

N = 5  # questions or words per session
FAMILIAR = [1] + list(range(78, 115))  # al-Fatiha and Juz' 'Amma first
SHORT = 70  # characters: an ayah short enough to read in a quiz


class Question(NamedTuple):
    kind: str  # name | find | listen | count
    rule: str  # the rule asked about
    ayahs: Tuple[Tuple[int, int, str], ...]  # (surah, ayah, marked html) shown
    options: Tuple[str, ...]  # button labels
    answer: int  # index into options
    audio: Optional[Tuple[int, int]]  # an ayah to play first (listen)


class DrillItem(NamedTuple):
    surah: int
    ayah: int
    word: str


# Audio lessons (Muallimi soniy numbers) that teach an annotated rule.
AUDIO_RULES: Dict[int, Tuple[str, ...]] = {
    41: ("silent",),
    42: ("lam_shamsiyyah",),
    44: ("hamzat_wasl",),
    47: ("madd_2",),
    48: ("madd_muttasil",),
    49: ("madd_munfasil",),
    50: ("madd_6",),
    51: ("madd_246",),
    52: ("madd_246",),
    53: ("madd_246",),
    55: ("iqlab",),
    56: ("idghaam_ghunnah",),
    57: ("idghaam_no_ghunnah",),
    58: ("ikhfa",),
}

# Letter lessons 2-29 in the book's order.
LETTERS = "ارزمتنيبكلوهفقشسثصطجخحغعدضذظ"

_HARAKAT_CHECKS: Dict[int, Callable[[str], bool]] = {
    30: lambda w: any(x in w for x in ("َا", "ُو", "ِي", "ٰ")),  # madd letters
    31: lambda w: "ّ" in w,  # shadda
    32: lambda w: any(c in w for c in "ًٌٍ"),  # tanwin
    33: lambda w: "ّ" in w and any(c in w for c in "ًٌٍ"),
    34: lambda w: any(c in w for c in "ءأؤئإ"),  # hamza
    35: lambda w: "ة" in w,  # ta marbuta
    36: lambda w: "ٰ" in w,  # read but not written
    37: lambda w: "ۦ" in w,  # the small ya
    38: lambda w: "ۥ" in w,  # the small waw
    39: lambda w: w.endswith("ىٰ") or w.endswith("ى"),
    40: lambda w: "وٰ" in w,
}


def rules_for(lesson_id: str) -> Tuple[str, ...]:
    """The annotated rules a lesson's quiz can ask about (empty: drills only)."""
    audio = tajweed_lessons.audio_lesson(lesson_id)
    if audio is not None:
        return AUDIO_RULES.get(audio.n, ())
    lesson = tajweed_lessons.lesson(lesson_id)
    return tuple(r for r in lesson.rules if r in tajweed.RULES) if lesson else ()


# --- the ayah pool ----------------------------------------------------------------

_pool: Optional[List[Tuple[int, int]]] = None


def _ayahs() -> List[Tuple[int, int]]:
    """Short ayahs, familiar surahs first: what quiz and drill items are drawn from."""
    global _pool
    if _pool is None:
        tajweed._load()
        keys = sorted(tajweed._text)
        familiar = [k for k in keys if k[0] in FAMILIAR and len(tajweed.text(*k)) <= SHORT]
        rest = [k for k in keys if k[0] not in FAMILIAR and len(tajweed.text(*k)) <= SHORT]
        _pool = familiar + rest
    return _pool


def _with(rule: str, times: Tuple[int, int] = (1, 1)) -> List[Tuple[int, int]]:
    lo, hi = times
    return [k for k in _ayahs() if lo <= len(tajweed.spans(*k, [rule])) <= hi]


def _mark(surah: int, ayah: int, ranges) -> str:
    body = tajweed.text(surah, ayah)
    out, pos = [], 0
    for a, b in sorted(ranges):
        out.append(html.escape(body[pos:a]))
        out.append("<u><b>%s</b></u>" % html.escape(body[a:b]))
        pos = b
    out.append(html.escape(body[pos:]))
    return "".join(out)


def _name(rule: str) -> str:
    return tajweed.RULES[rule].name_uz


def _distractors(rng: random.Random, rule: str, avoid: set) -> List[str]:
    """Three other rules, from the same family first (the madd rules for a madd)."""
    group = tajweed.RULES[rule].group
    same = [
        r for r in tajweed.RULES if r != rule and r not in avoid and tajweed.RULES[r].group == group
    ]
    other = [r for r in tajweed.RULES if r != rule and r not in avoid and r not in same]
    rng.shuffle(same)
    rng.shuffle(other)
    return (same + other)[:3]


def _q_name(rng, rule, kind) -> Optional[Question]:
    pool = _with(rule)
    if not pool:
        return None
    s, a = pool[rng.randrange(min(len(pool), 40))]
    _, x, y = tajweed.spans(s, a, [rule])[0]
    # rules annotated on the same letters would also be a right answer: never offer them
    overlap = {r for r, p, q in tajweed.spans(s, a) if p < y and x < q}
    options = [rule] + _distractors(rng, rule, overlap)
    rng.shuffle(options)
    return Question(
        kind,
        rule,
        ((s, a, _mark(s, a, [(x, y)])),),
        tuple(_name(r) for r in options),
        options.index(rule),
        (s, a) if kind == "listen" else None,
    )


def _q_find(rng, rule) -> Optional[Question]:
    yes = _with(rule, (1, 3))
    no = [k for k in _ayahs() if not tajweed.spans(*k, [rule])]
    if not yes or len(no) < 3:
        return None
    right = yes[rng.randrange(min(len(yes), 40))]
    wrong = rng.sample(no[:200], 3)
    shown = [right] + wrong
    rng.shuffle(shown)
    return Question(
        "find",
        rule,
        tuple((s, a, html.escape(tajweed.text(s, a))) for s, a in shown),
        ("1", "2", "3", "4"),
        shown.index(right),
        None,
    )


def _q_count(rng, rule) -> Optional[Question]:
    pool = _with(rule, (1, 4))
    if not pool:
        return None
    s, a = pool[rng.randrange(min(len(pool), 60))]
    found = tajweed.spans(s, a, [rule])
    return Question(
        "count",
        rule,
        ((s, a, _mark(s, a, [(x, y) for _, x, y in found])),),
        ("1", "2", "3", "4"),
        len(found) - 1,
        None,
    )


KINDS = ("name", "find", "listen", "count")


def quiz(lesson_id: str, seed: int, n: int = N) -> List[Question]:
    """`n` questions on the lesson's rules, kinds in rotation; [] when it has none."""
    rules = rules_for(lesson_id)
    if not rules:
        return []
    rng = random.Random("%s:%d" % (lesson_id, seed))
    out: List[Question] = []
    for i in range(n * 3):  # a kind can come up empty for a rare rule; try the next
        if len(out) == n:
            break
        rule, kind = rules[i % len(rules)], KINDS[i % len(KINDS)]
        if kind == "find":
            q = _q_find(rng, rule)
        elif kind == "count":
            q = _q_count(rng, rule)
        else:
            q = _q_name(rng, rule, kind)
        if q is not None and all(q.ayahs != p.ayahs for p in out):
            out.append(q)
    return out


# --- reading drills ---------------------------------------------------------------


def _word_check(lesson_id: str) -> Optional[Callable[[str], bool]]:
    audio = tajweed_lessons.audio_lesson(lesson_id)
    if audio is not None:
        if 2 <= audio.n <= 29:
            letter = LETTERS[audio.n - 2]
            return lambda w: letter in w
        return _HARAKAT_CHECKS.get(audio.n)
    return None


def drill(lesson_id: str, seed: int, n: int = N) -> List[DrillItem]:
    """`n` words to read aloud, each from a short ayah that can be played."""
    rng = random.Random("drill:%s:%d" % (lesson_id, seed))
    rules = rules_for(lesson_id)
    check = _word_check(lesson_id)
    candidates: List[DrillItem] = []
    tajweed._load()
    # short familiar ayahs first; the whole Qur'an only for a rare spelling (lesson 40)
    for s, a in _ayahs() + sorted(set(tajweed._text) - set(_ayahs())):
        if len(candidates) >= 80:
            break
        body = tajweed.text(s, a)
        if rules:
            for _, x, _y in tajweed.spans(s, a, rules):
                start = body.rfind(" ", 0, x) + 1
                end = body.find(" ", x)
                candidates.append(DrillItem(s, a, body[start : end if end != -1 else len(body)]))
        else:
            for w in body.split(" "):
                if len(w) >= 3 and (check is None or check(w)):
                    candidates.append(DrillItem(s, a, w))
    seen, out = set(), []
    rng.shuffle(candidates)
    for item in candidates:
        if item.word not in seen:
            seen.add(item.word)
            out.append(item)
        if len(out) == n:
            break
    return out


def reset_for_tests() -> None:
    global _pool
    _pool = None
