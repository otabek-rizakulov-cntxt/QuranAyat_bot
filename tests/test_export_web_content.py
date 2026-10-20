"""Static Mini App content export (docs/MINI_APP_PLAN.md task P0.4).

Exports the whole tree once per module into a temp dir, then checks the
done-when: 6236 ayahs present per language, and page boundaries in meta.json
match `Quran.page_range` for all 604 pages."""

import importlib.util
import json
import os

import pytest

from modules import Quran

_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "export_web_content.py")
_spec = importlib.util.spec_from_file_location("export_web_content", _SCRIPT)
exporter = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(exporter)


@pytest.fixture(scope="module")
def content(tmp_path_factory):
    out = tmp_path_factory.mktemp("web-content")
    meta = exporter.export(str(out))
    return out, meta


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# Ayahs the bundled tanzil files themselves leave blank. Listed so a new gap
# fails here rather than surfacing as an empty card in the app.
KNOWN_EMPTY = {("ko", 40, 81), ("ku", 108, 3)}


def _count(directory, code=None):
    total = 0
    for n in range(1, 115):
        doc = _load(os.path.join(directory, "%d.json" % n))
        assert doc["n"] == n
        assert len(doc["ayahs"]) == Quran.get_surah_length(n)
        for a, text in enumerate(doc["ayahs"], start=1):
            assert isinstance(text, str)
            assert text or (code, n, a) in KNOWN_EMPTY, (code, n, a)
        total += len(doc["ayahs"])
    return total


def test_arabic_has_every_ayah(content):
    out, _ = content
    assert _count(os.path.join(out, "ar")) == 6236


def test_every_translation_has_every_ayah(content):
    out, meta = content
    assert "en" in meta["translations"] and "translit" in meta["translations"]
    assert "ar" not in meta["translations"]          # served from ar/, not translations/
    for code in meta["translations"]:
        assert _count(os.path.join(out, "translations", code), code) == 6236, code


def test_tafsir_has_every_ayah(content):
    out, _ = content
    assert _count(os.path.join(out, "tafsir")) == 6236


def test_page_boundaries_match_the_bot(content):
    _, meta = content
    assert len(meta["pages"]) == 604
    for n, span in enumerate(meta["pages"], start=1):
        assert tuple(span) == Quran.page_range(n), n
    assert [tuple(s) for s in meta["juzs"]] == [Quran.juz_range(n) for n in range(1, 31)]


def test_meta_surahs_and_sajdas(content):
    out, meta = content
    assert _load(os.path.join(out, "meta.json")) == meta
    assert [s["ayahs"] for s in meta["surahs"]] == list(Quran.surah_lengths)
    assert meta["surahs"][1]["tname"] == "Al-Baqara"
    assert len(meta["sajdas"]) == len(Quran.sajdas)
    assert meta["total_ayahs"] == 6236


def test_basmalah_is_lifted_into_a_flag(content):
    out, _ = content
    fatiha, baqara, tawba = (_load(os.path.join(out, "ar", "%d.json" % n)) for n in (1, 2, 9))
    basmalah = fatiha["ayahs"][0]
    assert not basmalah.startswith("﻿")
    assert fatiha["bismillah"] and baqara["bismillah"] and not tawba["bismillah"]
    assert not baqara["ayahs"][0].startswith(basmalah)   # 2:1 is now just "الم"
    assert len(baqara["ayahs"][0]) < 10
