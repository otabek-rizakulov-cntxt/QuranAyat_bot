"""The tajweed data the lessons rest on (docs/TAJWEED_PLAN.md §2, §4, §11)."""

import json
import os

import pytest

from domain import tajweed
from domain.quran import Quran

DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "tajweed")


def test_text_covers_every_ayah():
    for s in range(1, 115):
        for a in range(1, Quran.get_surah_length(s) + 1):
            assert tajweed.text(s, a)


def test_every_annotation_is_a_known_rule_inside_its_ayah():
    with open(os.path.join(DIR, "tajweed.json"), encoding="utf-8") as fp:
        raw = json.load(fp)
    assert len(raw) == 6236
    for entry in raw:
        length = len(tajweed.text(entry["surah"], entry["ayah"]))
        for ann in entry["annotations"]:
            assert ann["rule"] in tajweed.RULES, ann
            assert 0 <= ann["start"] < ann["end"] <= length, (entry["surah"], entry["ayah"], ann)


@pytest.mark.parametrize("rule", sorted(tajweed.RULES))
def test_every_rule_has_real_examples(rule):
    ex = tajweed.examples(rule, 12)
    assert len(ex) >= 3
    for s, a in ex:
        assert tajweed.spans(s, a, [rule]), (rule, s, a)


def test_marked_html_marks_the_rule_and_escapes_nothing_else():
    # 112:2 "as-Samad": the classic qalqala on the final dal
    out = tajweed.marked_html(112, 2, ["qalqalah"])
    assert out.count("<u><b>") == 1 and "د" in out.split("<u><b>")[1].split("</b></u>")[0]
    assert out.replace("<u><b>", "").replace("</b></u>", "") == tajweed.text(112, 2)


def test_marked_html_merges_overlapping_spans():
    s, a = tajweed.examples("madd_6", 1)[0]
    rules = [r for r, _, _ in tajweed.spans(s, a)]  # every rule: spans overlap
    out = tajweed.marked_html(s, a, rules)
    depth = 0
    for token in out.replace("<u><b>", "\x00").replace("</b></u>", "\x01"):
        depth += {"\x00": 1, "\x01": -1}.get(token, 0)
        assert depth in (0, 1)  # never nested, never closed twice
    assert depth == 0
    assert out.replace("<u><b>", "").replace("</b></u>", "") == tajweed.text(s, a)
