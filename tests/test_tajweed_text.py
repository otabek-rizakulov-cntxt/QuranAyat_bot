"""Tajweed P2: the text of the Muallimi soniy audio lessons (docs/TAJWEED_PLAN.md).

data/tajweed/muallimi_text.txt is typed by hand; these checks catch typing slips
(a Latin letter in an Arabic row, an unknown lesson number, an empty lesson).
"""

import re

from domain import tajweed_lessons

# Arabic letters, harakat, tatweel, the dash and full stop used between word pairs.
_ARABIC_ROW = re.compile(r"^[ء-يً-ْٓ-ٰٕٱـ .–-]+$")


def _ids_with_text():
    return [x.id for x in tajweed_lessons.audio_lessons() if tajweed_lessons.audio_text(x.id)]


def test_every_lesson_in_the_text_exists():
    known = {x.id for x in tajweed_lessons.audio_lessons()}
    with open(tajweed_lessons._TEXT_PATH, encoding="utf-8") as fp:
        ids = ["ms-%03d" % int(m) for m in re.findall(r"^## (\d+)\s*$", fp.read(), re.M)]
    assert ids and set(ids) <= known
    assert len(ids) == len(set(ids)), "a lesson appears twice"
    assert all(tajweed_lessons.audio_text(i) for i in ids), "a lesson with no lines"


def test_arabic_rows_are_arabic_only():
    for lesson_id in _ids_with_text():
        for line in tajweed_lessons.audio_text(lesson_id):
            assert line.kind in ("ar", "uz")
            if line.kind == "ar":
                assert _ARABIC_ROW.match(line.text), (lesson_id, line.text)


def test_the_letter_lessons_are_typed():
    assert set(_ids_with_text()) >= {"ms-%03d" % n for n in range(1, 30)}


def test_cyrillic_leaves_arabic_alone():
    for lesson_id in _ids_with_text():
        lat = tajweed_lessons.audio_text(lesson_id, "uz")
        cyr = tajweed_lessons.audio_text(lesson_id, "uz-Cyrl")
        assert [x.text for x in lat if x.kind == "ar"] == [x.text for x in cyr if x.kind == "ar"]
