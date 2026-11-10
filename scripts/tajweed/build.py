#!/usr/bin/env python3
"""Rank example ayahs for every tajweed rule -> data/tajweed/examples.json.

    python3 scripts/tajweed/build.py

A good teaching example is short, shows the rule clearly (once or twice, not twenty
times), has few other rules tangled into the same letters, and comes from a surah a
learner already knows. Deterministic: same input, same output. Runs in seconds.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "src"))

from domain import tajweed  # noqa: E402

PER_RULE = 12
PER_SURAH = 2  # variety: at most this many examples from one surah
# Surahs most learners know by heart: al-Fatiha and Juz' 'Amma first.
FAMILIAR = {1} | set(range(78, 115))


def score(surah: int, ayah: int, rule: str) -> float:
    """Lower is better."""
    text = tajweed.text(surah, ayah)
    all_spans = tajweed.spans(surah, ayah)
    mine = [s for s in all_spans if s[0] == rule]
    others = [s for s in all_spans if s[0] != rule]
    tangled = sum(1 for _, a, b in mine for _, c, d in others if a < d and c < b)
    return (
        len(text) / 40.0  # shorter ayahs are easier to hear and read
        + 1.5 * abs(len(mine) - 1)  # one clear occurrence is best
        + 2.0 * tangled  # other rules on the same letters confuse
        - (3.0 if surah in FAMILIAR else 0.0)
    )


def main() -> None:
    tajweed._load()
    out = {}
    for rule in tajweed.RULES:
        candidates = sorted(
            (score(s, a, rule), s, a)
            for (s, a) in tajweed._spans
            if any(x[0] == rule for x in tajweed._spans[(s, a)])
        )
        picked, per_surah = [], {}
        for _, s, a in candidates:
            if per_surah.get(s, 0) >= PER_SURAH:
                continue
            picked.append([s, a])
            per_surah[s] = per_surah.get(s, 0) + 1
            if len(picked) == PER_RULE:
                break
        out[rule] = picked
    path = os.path.join(ROOT, "data", "tajweed", "examples.json")
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(out, fp, separators=(",", ":"), sort_keys=True)
        fp.write("\n")
    short = {r: len(v) for r, v in out.items() if len(v) < 3}
    print(
        "wrote %s: %d rules%s"
        % (os.path.relpath(path), len(out), ", too few: %s" % short if short else "")
    )


if __name__ == "__main__":
    main()
