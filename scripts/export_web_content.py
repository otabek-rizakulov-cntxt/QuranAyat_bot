#!/usr/bin/env python3
# BismillahBot -- Explore the Holy Qur'an on Telegram
#
# Export the bot's Qur'an corpora as static JSON for the Mini App
# (docs/MINI_APP_PLAN.md §2 "Quran content delivery", task P0.4). Content never
# changes, so the Mini App serves these files from its CDN and the API never
# sees a request for Qur'an text. Run from the repo root:
#
#     python3 scripts/export_web_content.py [OUT_DIR]      # default: build/web-content
#
# Layout (all UTF-8, compact):
#
#   meta.json                       surahs, page/juz spans, sajdas, translation codes
#   ar/{surah}.json                 Uthmani text; the basmalah prefix tanzil puts on
#                                   ayah 1 is lifted into `"bismillah": true`
#   translations/{code}/{surah}.json   every bundled translation (+ `translit`)
#   tafsir/{surah}.json             Tafsir al-Jalalayn (English)
#
# Everything is read through `modules.Quran`, the same parser the bot uses, so
# the app and the bot can never disagree on an ayah boundary.

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from modules import Quran, TranslationRegistry  # noqa: E402
from modules.quran import _QURAN_DATA  # noqa: E402

DEFAULT_OUT_DIR = os.path.join(ROOT, "build", "web-content")
ARABIC = "ar"


def _write(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


def _spans(count: int, range_of) -> list:
    return [list(range_of(n)) for n in range(1, count + 1)]


def build_meta(translation_codes: list) -> dict:
    surahs = [
        {
            "n": int(s.attrib["index"]),
            "ayahs": int(s.attrib["ayas"]),
            "name": s.attrib["name"],
            "tname": s.attrib["tname"],
            "ename": s.attrib["ename"],
            "type": s.attrib["type"],
            "order": int(s.attrib["order"]),
        }
        for s in _QURAN_DATA.find("suras")
    ]
    return {
        "surahs": surahs,
        # [start_surah, start_ayah, end_surah, end_ayah] per page / juz, 1-based
        # by position — the same spans Quran.page_range / juz_range return.
        "pages": _spans(Quran.PAGE_COUNT, Quran.page_range),
        "juzs": _spans(Quran.JUZ_COUNT, Quran.juz_range),
        "sajdas": [{"surah": s, "ayah": a, "type": kind} for s, a, kind in Quran.sajdas],
        "translations": translation_codes,
        "total_ayahs": sum(Quran.surah_lengths),
    }


def split_basmalah(text: list) -> list:
    """Per surah: (ayahs, has_bismillah). Tanzil prefixes the basmalah onto ayah 1
    of every surah except al-Fatiha (where it *is* ayah 1) and at-Tawba (which has
    none); the reader shows it as a header instead, so it is lifted out here."""
    basmalah = text[0][0].lstrip("﻿")
    out = []
    for n, ayahs in enumerate(text, start=1):
        ayahs = list(ayahs)
        ayahs[0] = ayahs[0].lstrip("﻿")
        has = n != 1 and ayahs[0].startswith(basmalah + " ")
        if has:
            ayahs[0] = ayahs[0][len(basmalah) + 1 :]
        out.append((ayahs, n == 1 or has))
    return out


def export(out_dir: str = DEFAULT_OUT_DIR) -> dict:
    """Write the full content tree under `out_dir`; return meta.json's content."""
    codes = sorted(c for c in TranslationRegistry.available() if c != ARABIC)

    arabic = Quran.from_file(os.path.join(ROOT, "translations", "ar.txt")).text
    for n, (ayahs, bismillah) in enumerate(split_basmalah(arabic), start=1):
        _write(
            os.path.join(out_dir, ARABIC, "%d.json" % n),
            {"n": n, "bismillah": bismillah, "ayahs": ayahs},
        )

    for code in codes:
        quran = Quran.from_file(os.path.join(ROOT, "translations", "%s.txt" % code))
        for n, ayahs in enumerate(quran.text, start=1):
            _write(
                os.path.join(out_dir, "translations", code, "%d.json" % n), {"n": n, "ayahs": ayahs}
            )

    tafsir = Quran.from_tafsir(os.path.join(ROOT, "Al_Jalalain_Eng.txt"))
    for n, ayahs in enumerate(tafsir.text, start=1):
        _write(os.path.join(out_dir, "tafsir", "%d.json" % n), {"n": n, "ayahs": ayahs})

    meta = build_meta(codes)
    _write(os.path.join(out_dir, "meta.json"), meta)
    return meta


def main() -> int:
    out_dir = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT_DIR
    meta = export(out_dir)
    print(
        "Exported %d surahs, Arabic + %d translations + tafsir to %s"
        % (len(meta["surahs"]), len(meta["translations"]), out_dir)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
