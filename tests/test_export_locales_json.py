"""Locale JSON export for the Mini App (docs/MINI_APP_PLAN.md task P0.5)."""

import importlib.util
import json
import os

from locales import DEFAULT_LANG, LOCALES, UI_LANGUAGES, WEB_LOCALES, t

_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "export_locales_json.py")
_spec = importlib.util.spec_from_file_location("export_locales_json", _SCRIPT)
exporter = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(exporter)

WEB_KEYS = sorted(k for k in LOCALES[DEFAULT_LANG] if k.startswith("web_"))


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def test_every_ui_language_is_exported_resolved_like_t(tmp_path):
    codes = exporter.export(str(tmp_path))
    assert codes == [lang.code for lang in UI_LANGUAGES]
    for code in codes:
        table = _load(tmp_path / "locales" / ("%s.json" % code))
        assert set(table) == set(LOCALES[DEFAULT_LANG]), code
        assert all(table[k] == t(k, code) for k in table), code


def test_launch_locales_have_their_own_web_strings():
    # The done-when for P0.5: zero English fallback on app screens in the launch
    # locales. ar is RTL-checked below; its web_* fall back by policy (§11.3).
    assert WEB_KEYS
    for code in WEB_LOCALES - {DEFAULT_LANG}:
        for key in WEB_KEYS:
            assert key in LOCALES[code], (code, key)
            assert LOCALES[code][key] != LOCALES[DEFAULT_LANG][key], (code, key)


def test_languages_catalogue_carries_rtl(tmp_path):
    exporter.export(str(tmp_path))
    langs = {l["code"]: l for l in _load(tmp_path / "locales" / "languages.json")}
    assert langs["ar"]["rtl"] is True and langs["uz-Cyrl"]["rtl"] is False
    assert langs["translit"]["ui"] is False
