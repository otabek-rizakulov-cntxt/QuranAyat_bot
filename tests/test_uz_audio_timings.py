"""The committed Uzbek audio timing table (data/uz_audio_timings.json) is sound.

The structural half of the quality gate in docs/MULTILINGUAL_PLAN.md §8.1.9: if
any of this breaks, some ayah clip would be cut from the wrong bytes. Whether a
cut lands on the right *word* is checked by ear (scripts/uz_audio/debug.py).
"""

import os

import pytest
import ujson as json

import infra.uz_audio as uz_audio
from domain.quran import Quran

PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uz_audio_timings.json")

if not os.path.exists(PATH):
    pytest.skip("timings not generated yet (scripts/uz_audio/)", allow_module_level=True)

with open(PATH, encoding="utf-8") as fp:
    TABLE = json.load(fp)
SURAHS = sorted(int(k) for k in TABLE["surahs"])


@pytest.fixture(autouse=True)
def real_table():
    uz_audio.reset_for_tests(TABLE["surahs"])
    yield
    uz_audio.reset_for_tests()


def test_source_is_the_newbooks_mirror():
    assert TABLE["source"] == uz_audio.SOURCE_URL


@pytest.mark.parametrize("surah", SURAHS)
def test_surah_is_structurally_sound(surah):
    e = TABLE["surahs"][str(surah)]
    assert e["sample_rate"] in (32000, 44100, 48000)
    assert e["frame_bytes"] == 144 * e["kbps"] * 1000 // e["sample_rate"]
    assert e["frames"] * e["frame_bytes"] == e["size"]  # the file is whole frames, from byte 0
    assert e["status"] in ("verified", "estimated")
    ayahs = e["ayahs"]
    assert len(ayahs) == Quran.get_surah_length(surah)
    for (a0, a1, conf), nxt in zip(ayahs, ayahs[1:] + [None]):
        assert 0 <= a0 < a1 <= e["frames"]
        assert 0.0 <= conf <= 1.0
        if nxt is not None:
            assert a1 == nxt[0]  # contiguous: no gap, no overlap


@pytest.mark.parametrize("surah", SURAHS)
def test_parts_fit_telegram_and_cover_the_file(surah):
    parts = uz_audio.parts(surah)
    assert parts[0].start_byte == 0
    assert parts[-1].end_byte == uz_audio.size(surah) - 1
    for a, b in zip(parts, parts[1:]):
        assert b.start_byte == a.end_byte + 1
    assert all(p.end_byte - p.start_byte + 1 <= uz_audio.PART_LIMIT for p in parts)


def test_baqarah_matches_the_cuts_approved_by_ear():
    """2:284 and 2:284-285 were cut by hand and approved after listening (2026-11-08)."""
    if 2 not in SURAHS:
        pytest.skip("al-Baqarah not aligned yet")
    start, end = uz_audio.seconds(2, 284, 284)
    assert start == pytest.approx(9034.1, abs=0.3)
    assert end == pytest.approx(9067.4, abs=0.3)
    assert uz_audio.seconds(2, 285, 285)[1] == pytest.approx(9114.2, abs=0.3)
