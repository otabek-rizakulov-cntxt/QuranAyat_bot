"""Tajweed P2: the line aligner (scripts/tajweed/align_text.py) on a made-up transcript.

The real transcripts come from Colab; this fixture imitates one: Uzbek talk, then
the rows read aloud as Whisper spells them, with pauses between.
"""

import pytest

from scripts.tajweed import align_text as at

ROWS = [
    "زَ زِ زُ",
    "اَزْ اِزْ اُزْ زَرْ زِرْ زُرْ",
    "اَزْرُ اِزْرُ اُزْرُ اُرْزُ",
]


def _words(spec):
    """[(text, gap_before_s)] -> Whisper-style [[start, end, text]], 0.4 s a word."""
    out, t = [], 0.0
    for text, gap in spec:
        t += gap
        out.append([round(t, 2), round(t + 0.4, 2), text])
        t += 0.4
    return out


SPEC = [
    ("Endi", 0.0),
    ("za", 0.05),
    ("harfini", 0.05),
    ("oʻrganamiz.", 0.05),
    ("Za,", 1.2),
    ("zi,", 0.1),
    ("zu.", 0.1),
    ("Az,", 1.0),
    ("iz,", 0.1),
    ("uz,", 0.1),
    ("zar,", 0.1),
    ("zir,", 0.1),
    ("zur.", 0.1),
    ("Yaxshilab", 1.5),
    ("takrorlang.", 0.05),
    ("Azru,", 1.0),
    ("izru,", 0.1),
    ("uzru,", 0.1),
    ("urzu.", 0.1),
]


@pytest.mark.parametrize(
    "row, sound",
    [
        ("زَ زِ زُ", "za zi zu"),
        ("مَرْمَرْ رَمْرَمْ", "marmar ramram"),
        ("بٰا بِى بُو", "ba bi bu"),
        ("ا ب ت", "alif ba ta"),
        ("الٓمٓ", "alif lam mim"),
        ("حَبًّا", "haban"),
        ("لٰٓا اِلٰهَ", "la ilaha"),
    ],
)
def test_romanize(row, sound):
    assert at.romanize(row) == sound


def test_fold_reads_latin_cyrillic_and_arabic_alike():
    assert at.fold("Zar, zir, zur.") == "zar zir zur"
    assert at.fold("Зар зир зур") == "zar zir zur"
    assert at.fold("Qalb") == at.fold("kalb")


def test_rows_land_on_their_words_and_talk_becomes_uzbek_lines():
    lines = at.align(ROWS, _words(SPEC))
    kinds = [x["kind"] for x in lines]
    assert kinds == ["uz", "ar", "ar", "uz", "ar"]
    ar = [x for x in lines if x["kind"] == "ar"]
    assert [x["row"] for x in ar] == [0, 1, 2]
    assert all(x["conf"] > 0.8 for x in ar)
    assert lines[0]["text"] == "Endi za harfini oʻrganamiz."
    assert lines[3]["text"] == "Yaxshilab takrorlang."
    starts = [x["start"] for x in lines]
    assert starts == sorted(starts)
    assert all(a["end"] <= b["start"] + 1e-9 for a, b in zip(lines, lines[1:]))


def test_boundaries_move_into_the_quietest_moment():
    words = _words(SPEC)
    energy = [-20.0] * int(words[-1][1] / at.HOP_S + 10)
    quiet = int(2.6 / at.HOP_S)  # silence inside the 1.2 s gap before "Za"
    energy[quiet] = -80.0
    lines = at.align(ROWS, words, energy)
    assert lines[0]["end"] == lines[1]["start"] == round(quiet * at.HOP_S + at.HOP_S / 2, 2)


def test_a_row_the_narrator_skips_is_kept_unmatched():
    rows = ROWS[:2] + ["مَرْمَرْ رَمْرَمْ زَمْزَمْ"] + ROWS[2:]
    lines = at.align(rows, _words(SPEC))
    skipped = next(x for x in lines if x.get("row") == 2)
    assert skipped["start"] is None and skipped["conf"] == 0.0
    assert [x["row"] for x in lines if x["kind"] == "ar"] == [0, 1, 2, 3]


def test_a_pin_overrides_the_guess():
    words = _words(SPEC)
    pin = {"start": words[13][0], "end": words[18][1]}  # "Yaxshilab ... urzu."
    lines = at.align(ROWS, words, pins={2: pin})
    row2 = next(x for x in lines if x.get("row") == 2)
    assert (row2["start"], row2["end"], row2["conf"]) == (pin["start"], pin["end"], 1.0)
    timed = [x for x in lines if x["start"] is not None]
    assert all(a["end"] <= b["start"] for a, b in zip(timed, timed[1:]))  # neighbours fit


def test_words_of_flattens_segments():
    t = {
        "segments": [
            {"start": 0, "end": 1, "text": "a b", "words": [[0, 0.5, " a"], [0.5, 1, "b "]]}
        ]
    }
    assert at.words_of(t) == [[0.0, 0.5, "a"], [0.5, 1.0, "b"]]
