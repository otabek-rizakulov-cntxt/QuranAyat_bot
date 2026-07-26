"""UI internationalization: catalogue completeness and the t()/button helpers.

The per-locale integrity block mirrors scripts/check_locales.py, but as granular
pytest cases so a single bad language points straight at the failing check.
"""

import re

import pytest

from locales import (
    ACTION_BUTTON_KEYS,
    BOT_COMMANDS,
    DEFAULT_LANG,
    LANGUAGES,
    LOCALES,
    button_action,
    get_language,
    is_supported,
    keyboard_rows,
    missing_keys,
    missing_locales,
    normalize_lang,
    t,
    welcome_text,
)

_PLACEHOLDER = re.compile(r"\{(\w+)\}")
_CODES = [lang.code for lang in LANGUAGES]
_REQUIRED_KEYS = sorted(LOCALES[DEFAULT_LANG])


def _placeholders(text):
    return set(_PLACEHOLDER.findall(text))


class TestCatalogue:
    def test_every_language_has_a_locale_table(self):
        assert missing_locales() == []


@pytest.mark.parametrize("code", _CODES)
class TestLocaleIntegrity:
    def test_no_missing_keys(self, code):
        assert missing_keys(code) == []

    def test_placeholders_match_english(self, code):
        table = LOCALES[code]
        for key in _REQUIRED_KEYS:
            if key not in table:
                continue
            assert _placeholders(table[key]) == _placeholders(LOCALES[DEFAULT_LANG][key]), key

    def test_no_empty_values(self, code):
        table = LOCALES[code]
        for key in _REQUIRED_KEYS:
            if key in table:
                assert table[key].strip() != "", key

    def test_button_labels_round_trip(self, code):
        # A localized label must resolve back to the exact action that produced it,
        # otherwise a tap silently sends the user to the wrong action.
        for action, btn_key in ACTION_BUTTON_KEYS.items():
            assert button_action(t(btn_key, code), code) == action, (code, action)

    def test_keyboard_labels_are_unique(self, code):
        labels = [label for row in keyboard_rows(code) for label in row]
        assert len(labels) == len(set(labels)), labels

    def test_html_tags_balanced(self, code):
        table = LOCALES[code]
        for key in ("welcome_intro", "welcome_inline", "about"):
            value = table.get(key, "")
            assert value.count("<b>") == value.count("</b>"), key

    def test_start_advertises_every_command(self, code):
        message = welcome_text(code)
        for command, key in BOT_COMMANDS:
            assert "/%s — %s" % (command, t(key, code)) in message, command


class TestWelcomeText:
    def test_command_list_is_localized(self):
        assert t("cmd_index", "ru") in welcome_text("ru")

    def test_unknown_language_falls_back_to_english(self):
        assert welcome_text("zz") == welcome_text("en")


class TestTranslate:
    def test_returns_localized_string(self):
        assert t("welcome_intro", "en")

    def test_falls_back_to_english_for_unknown_language(self):
        assert t("welcome_intro", "zz") == t("welcome_intro", "en")

    def test_unknown_key_returns_the_key_itself(self):
        assert t("no_such_key_xyz", "en") == "no_such_key_xyz"


class TestNormalizeLang:
    def test_supported_code_passthrough(self):
        assert normalize_lang("ru") == "ru"

    def test_primary_subtag_extracted(self):
        assert normalize_lang("en-US") == "en"

    def test_uz_latin_primary_subtag(self):
        assert normalize_lang("uz-Latn") == "uz"

    def test_uz_cyrillic_full_tag_honoured(self):
        assert normalize_lang("uz-Cyrl") == "uz-Cyrl"

    def test_unsupported_defaults_to_english(self):
        assert normalize_lang("xx") == "en"

    def test_none_defaults_to_english(self):
        assert normalize_lang(None) == "en"


class TestButtonAction:
    def test_canonical_word(self):
        assert button_action("next", "en") == "next"

    def test_english_label(self):
        assert button_action(t("btn_translation", "en"), "en") == "translation"

    def test_legacy_english_label(self):
        assert button_action("english", "en") == "translation"

    def test_localized_label(self):
        assert button_action(t("btn_audio", "ru"), "ru") == "audio"

    def test_case_and_whitespace_insensitive(self):
        assert button_action("  NEXT  ", "en") == "next"

    def test_non_button_returns_none(self):
        assert button_action("some random text 123", "en") is None


class TestLanguageLookup:
    def test_known_language(self):
        assert get_language("ru").english == "Russian"

    def test_unknown_language_defaults_to_english(self):
        assert get_language("zz").code == DEFAULT_LANG

    def test_is_supported(self):
        assert is_supported("uz-Cyrl")
        assert not is_supported("zz")
