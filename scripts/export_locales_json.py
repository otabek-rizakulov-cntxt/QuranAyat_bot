#!/usr/bin/env python3
# BismillahBot -- Explore the Holy Qur'an on Telegram
#
# Export the bot's UI string tables as JSON for the Mini App
# (docs/MINI_APP_PLAN.md §2 "i18n", task P0.5). `src/locales/*.py` stays the one
# source of truth — `scripts/check_locales.py` keeps validating it, including the
# `web_*` keys the app adds. Run from the repo root:
#
#     python3 scripts/export_locales_json.py [OUT_DIR]     # default: build/web-content
#
# Writes OUT_DIR/locales/{code}.json per interface language — already resolved
# the way `t()` resolves (the locale's own string, else English), so the app
# needs no fallback logic of its own — and OUT_DIR/locales/languages.json, the
# catalogue with each language's `rtl` flag for the app's layout direction.

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from locales import DEFAULT_LANG, LANGUAGES, LOCALES, UI_LANGUAGES  # noqa: E402

DEFAULT_OUT_DIR = os.path.join(ROOT, "build", "web-content")


def _write(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def resolved_table(code: str) -> dict:
    return {**LOCALES[DEFAULT_LANG], **LOCALES.get(code, {})}


def languages() -> list:
    return [{"code": lang.code, "native": lang.native, "english": lang.english,
             "rtl": lang.rtl, "flag": lang.flag, "ui": not lang.translation_only}
            for lang in LANGUAGES]


def export(out_dir: str = DEFAULT_OUT_DIR) -> list:
    """Write every interface language's table; return the codes written."""
    codes = [lang.code for lang in UI_LANGUAGES]
    for code in codes:
        _write(os.path.join(out_dir, "locales", "%s.json" % code), resolved_table(code))
    _write(os.path.join(out_dir, "locales", "languages.json"), languages())
    return codes


def main() -> int:
    out_dir = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT_DIR
    codes = export(out_dir)
    print("Exported %d locale tables to %s" % (len(codes), os.path.join(out_dir, "locales")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
