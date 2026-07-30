#!/usr/bin/env python3
# BismillahBot -- Explore the Holy Qur'an on Telegram
#
# One-off / maintenance script: download every Qur'an translation listed in
# src/locales/languages.py from the free alquran.cloud API (which serves the
# tanzil.net editions) and write each one to translations/<code>.txt in the same
# `surah|ayah|text` line format the existing parse_quran() already reads.
#
# It also:
#   * fetches the original Arabic mushaf for the "ar" entry,
#   * derives Uzbek Latin (uz) from Uzbek Cyrillic (uz-Cyrl) by transliteration,
#   * writes ATTRIBUTIONS.md with each translation's source/edition.
#
# Run from the repo root:  python3 scripts/bundle_translations.py
# Re-run any time to refresh; it verifies every file has exactly 6236 verses.

import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

# Make `from locales.languages import ...` work when run from the repo root.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from locales.languages import (  # noqa: E402
    LANGUAGES, ARABIC_ORIGINAL, TRANSLIT_UZ,
)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(REPO_ROOT, "translations")
API = "http://api.alquran.cloud/v1/quran/{edition}"
ARABIC_EDITION = "quran-simple"
TOTAL_VERSES = 6236


# --------------------------------------------------------------------------- #
# Uzbek Cyrillic -> Latin transliteration
# --------------------------------------------------------------------------- #
# The Latin values use the official Uzbek letters: oʻ / gʻ use U+02BB (ʻ) and the
# tutuq belgisi uses U+02BC (ʼ). Multi-letter Cyrillic sounds map to digraphs.
_UZ_MAP = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ё": "yo",
    "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
    "ъ": "ʼ", "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    "ў": "oʻ", "қ": "q", "ғ": "gʻ", "ҳ": "h",
}
# `е` is contextual: "ye" at the start of a word or after a vowel, "e" otherwise.
_UZ_VOWELS = set("аоуэиўеёюя")


def transliterate_uz(text: str) -> str:
    """Deterministically convert Uzbek Cyrillic text to the Latin alphabet."""
    out = []
    for i, ch in enumerate(text):
        lower = ch.lower()
        if lower == "е":
            prev = text[i - 1].lower() if i > 0 else ""
            mapped = "ye" if (prev not in _UZ_MAP or prev in _UZ_VOWELS) else "e"
        else:
            mapped = _UZ_MAP.get(lower)
        if mapped is None:
            out.append(ch)          # digits, punctuation, spaces, etc.
            continue
        if ch != lower and mapped:  # was uppercase -> capitalise the digraph
            mapped = mapped[0].upper() + mapped[1:]
        out.append(mapped)
    return "".join(out)


# --------------------------------------------------------------------------- #
# Fetch + convert
# --------------------------------------------------------------------------- #
def fetch_edition(edition: str) -> dict:
    url = API.format(edition=edition)
    with urllib.request.urlopen(url, timeout=60) as resp:
        return json.load(resp)["data"]


def to_lines(data: dict) -> str:
    """Render an alquran.cloud payload as `surah|ayah|text` lines (tanzil format)."""
    lines = []
    for surah in sorted(data["surahs"], key=lambda s: s["number"]):
        for ayah in sorted(surah["ayahs"], key=lambda a: a["numberInSurah"]):
            text = (ayah["text"] or "").replace("|", "/").replace("\r", " ").replace("\n", " ").strip()
            lines.append("%d|%d|%s" % (surah["number"], ayah["numberInSurah"], text))
    if len(lines) != TOTAL_VERSES:
        raise ValueError("expected %d verses, got %d" % (TOTAL_VERSES, len(lines)))
    return "\n".join(lines) + "\n"


def write_file(code: str, content: str) -> None:
    with open(os.path.join(OUT_DIR, code + ".txt"), "w", encoding="utf-8") as f:
        f.write(content)


def bundle_one(lang) -> tuple[str, dict]:
    """Fetch/convert one language (skips the derived Uzbek Latin). Returns (code, edition-meta)."""
    edition = ARABIC_EDITION if lang.edition == ARABIC_ORIGINAL else lang.edition
    data = fetch_edition(edition)
    write_file(lang.code, to_lines(data))
    return lang.code, data.get("edition", {})


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    # Optional subset: `bundle_translations.py translit ru` refreshes only those.
    # Handy for adding one edition without re-downloading (and re-writing) all 48.
    only = set(sys.argv[1:])
    if only:
        unknown = only - {l.code for l in LANGUAGES}
        if unknown:
            sys.exit("unknown language code(s): %s" % ", ".join(sorted(unknown)))

    to_fetch = [l for l in LANGUAGES
                if l.edition != TRANSLIT_UZ and (not only or l.code in only)]
    meta: dict[str, dict] = {}
    failures: dict[str, str] = {}

    print("Downloading %d translations into %s ..." % (len(to_fetch), OUT_DIR))
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(bundle_one, l): l for l in to_fetch}
        for fut in as_completed(futures):
            lang = futures[fut]
            try:
                code, edmeta = fut.result()
                meta[code] = edmeta
                print("  ok  %-8s %s" % (code, lang.english))
            except Exception as e:
                failures[lang.code] = "%s: %s" % (type(e).__name__, e)
                print("  FAIL %-8s %s -> %s" % (lang.code, lang.english, failures[lang.code]))

    # Derive Uzbek Latin from the bundled Uzbek Cyrillic.
    uz_cyrl_path = os.path.join(OUT_DIR, "uz-Cyrl.txt")
    if only and "uz" not in only:
        pass                                    # not part of this subset
    elif os.path.exists(uz_cyrl_path):
        with open(uz_cyrl_path, encoding="utf-8") as f:
            cyr = f.read()
        write_file("uz", transliterate_uz(cyr))
        print("  ok  %-8s %s (transliterated from uz-Cyrl)" % ("uz", "Uzbek (Latin)"))
    else:
        failures["uz"] = "uz-Cyrl.txt missing; cannot transliterate"
        print("  FAIL uz -> uz-Cyrl.txt missing; cannot transliterate")

    if only:
        # A subset run only knows the editions it fetched, so rewriting the table
        # would blank every other row. The full run regenerates it correctly.
        print("\n(subset run: ATTRIBUTIONS.md left alone — "
              "re-run without arguments to regenerate it)")
    else:
        write_attributions(meta)

    print("\nDone. %d ok, %d failed." % (len(to_fetch) - len(failures), len(failures)))
    if failures:
        print("Failed:", ", ".join(sorted(failures)))
        sys.exit(1)


def write_attributions(meta: dict) -> None:
    """Record each bundled translation's edition/source for /about and licensing review."""
    lines = [
        "# Translation attributions",
        "",
        "Qur'an translations bundled in `translations/` are sourced from the",
        "[tanzil.net](https://tanzil.net) project via the free",
        "[alquran.cloud](https://alquran.cloud) API. Each translation carries its",
        "own copyright and licence held by its translator/publisher; the editions",
        "used are listed below. **Review each translation's licence before public",
        "distribution.**",
        "",
        "The Uzbek Latin text (`uz`) is produced by automatic transliteration of the",
        "Uzbek Cyrillic edition (`uz-Cyrl`, Muhammad Sodiq Muhammad Yusuf).",
        "",
        "| Code | Language | Edition | Translator |",
        "|------|----------|---------|------------|",
    ]
    for lang in LANGUAGES:
        ed = meta.get(lang.code, {})
        if lang.edition == TRANSLIT_UZ:
            edition_id, translator = "(derived from uz-Cyrl)", "Automatic transliteration"
        elif lang.edition == ARABIC_ORIGINAL:
            edition_id, translator = ARABIC_EDITION, ed.get("englishName", "Original Arabic (Tanzil)")
        else:
            edition_id = lang.edition
            translator = ed.get("englishName") or ed.get("name") or "—"
        lines.append("| `%s` | %s | `%s` | %s |" % (lang.code, lang.english, edition_id, translator))
    lines.append("")
    with open(os.path.join(REPO_ROOT, "ATTRIBUTIONS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
