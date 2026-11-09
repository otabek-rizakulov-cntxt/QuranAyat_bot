"""Tajweed rules over the Qur'an text (docs/TAJWEED_PLAN.md §2, §4).

Reads `data/tajweed/`: the Tanzil Uthmani text and cpfair's per-ayah rule annotations
(code-point ranges into that exact text), plus the generated `examples.json`. This text
is separate from `data/translations/ar.txt`, which uses another spelling and whose
offsets would not match.

Everything loads lazily on first use and stays in memory (~10 MB).
"""

import html
import json
import os
from typing import Dict, Iterable, List, NamedTuple, Optional, Tuple

_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "tajweed"
)


class Rule(NamedTuple):
    id: str  # cpfair's rule id
    name_uz: str  # Uzbek (Latin) name, as the lessons use it
    group: str  # lesson unit it belongs to


# Every rule id that appears in the annotations, with its Uzbek name.
RULES: Dict[str, Rule] = {
    r.id: r
    for r in (
        Rule("madd_2", "Tabiiy mad", "mad"),
        Rule("madd_muttasil", "Muttasil mad", "mad"),
        Rule("madd_munfasil", "Munfasil mad", "mad"),
        Rule("madd_6", "Lozim mad", "mad"),
        Rule("madd_246", "Oriz va lin mad", "mad"),
        Rule("ikhfa", "Ixfo", "nun"),
        Rule("idghaam_ghunnah", "Gʻunnali idgʻom", "nun"),
        Rule("idghaam_no_ghunnah", "Gʻunnasiz idgʻom", "nun"),
        Rule("iqlab", "Iqlob", "nun"),
        Rule("ikhfa_shafawi", "Shafaviy ixfo", "mim"),
        Rule("idghaam_shafawi", "Shafaviy idgʻom", "mim"),
        Rule("ghunnah", "Gʻunna", "other"),
        Rule("qalqalah", "Qalqala", "other"),
        Rule("lam_shamsiyyah", "Shamsiy lom", "other"),
        Rule("hamzat_wasl", "Hamzai vasl", "other"),
        Rule("silent", "Oʻqilmaydigan harf", "other"),
        Rule("idghaam_mutajanisayn", "Mutajonis idgʻom", "other"),
        Rule("idghaam_mutaqaribayn", "Mutaqorib idgʻom", "other"),
    )
}

Span = Tuple[str, int, int]  # (rule id, start, end) — code points, end exclusive

_text: Optional[Dict[Tuple[int, int], str]] = None
_spans: Optional[Dict[Tuple[int, int], List[Span]]] = None
_examples: Optional[Dict[str, List[Tuple[int, int]]]] = None


def _load() -> None:
    global _text, _spans
    if _text is not None:
        return
    text = {}
    with open(os.path.join(_DIR, "quran-uthmani.txt"), encoding="utf-8") as fp:
        for line in fp:
            parts = line.rstrip("\n").split("|", 2)
            if len(parts) == 3 and parts[0].isdigit():
                text[(int(parts[0]), int(parts[1]))] = parts[2]
    with open(os.path.join(_DIR, "tajweed.json"), encoding="utf-8") as fp:
        raw = json.load(fp)
    spans = {
        (e["surah"], e["ayah"]): sorted((a["rule"], a["start"], a["end"]) for a in e["annotations"])
        for e in raw
    }
    _text, _spans = text, spans


def text(surah: int, ayah: int) -> str:
    """The Uthmani text of an ayah, exactly as the annotations index it."""
    _load()
    return _text[(surah, ayah)]


def spans(surah: int, ayah: int, rules: Optional[Iterable[str]] = None) -> List[Span]:
    """Rule spans in an ayah, optionally only those of `rules`, by start offset."""
    _load()
    out = _spans.get((surah, ayah), [])
    if rules is not None:
        wanted = set(rules)
        out = [s for s in out if s[0] in wanted]
    return sorted(out, key=lambda s: (s[1], s[2]))


def examples(rule: str, limit: int = 6) -> List[Tuple[int, int]]:
    """The best example ayahs for a rule, as ranked by scripts/tajweed/build.py."""
    global _examples
    if _examples is None:
        with open(os.path.join(_DIR, "examples.json"), encoding="utf-8") as fp:
            _examples = {k: [tuple(x) for x in v] for k, v in json.load(fp).items()}
    return _examples.get(rule, [])[:limit]


def marked_html(surah: int, ayah: int, rules: Iterable[str]) -> str:
    """The ayah as Telegram HTML with the spans of `rules` underlined and bold.

    Telegram can't colour text, so underline + bold is the bot's marker; the Mini
    App colours by rule instead. Overlapping spans are merged."""
    body = text(surah, ayah)
    ranges = sorted((a, b) for _, a, b in spans(surah, ayah, rules))
    merged: List[List[int]] = []
    for a, b in ranges:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    out, pos = [], 0
    for a, b in merged:
        out.append(html.escape(body[pos:a]))
        out.append("<u><b>%s</b></u>" % html.escape(body[a:b]))
        pos = b
    out.append(html.escape(body[pos:]))
    return "".join(out)


def reset_for_tests() -> None:
    global _text, _spans, _examples
    _text = _spans = _examples = None
