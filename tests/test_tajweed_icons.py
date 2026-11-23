import unicodedata

from domain import tajweed_icons, tajweed_lessons


def _all_ids():
    return [x.id for x in tajweed_lessons.audio_lessons("uz")] + [
        x.id for x in tajweed_lessons.lessons("uz")
    ]


def test_every_lesson_has_an_icon():
    missing = [i for i in _all_ids() if not tajweed_icons.icon(i)]
    assert missing == []


def test_no_icons_for_lessons_that_do_not_exist():
    assert set(tajweed_icons.ICONS) - set(_all_ids()) == set()


def test_icons_are_short_arabic_text():
    for lesson_id, glyph in tajweed_icons.ICONS.items():
        chars = [c for c in glyph if c not in " ◌"]
        letters = [c for c in chars if not unicodedata.combining(c)]
        assert chars and len(letters) <= 5, lesson_id
        assert all("ARABIC" in unicodedata.name(c, "") for c in chars), lesson_id


def test_unknown_lesson_has_no_icon():
    assert tajweed_icons.icon("nope") == ""
