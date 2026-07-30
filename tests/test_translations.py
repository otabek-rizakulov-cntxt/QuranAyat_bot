"""TranslationRegistry: lazy loading, caching, and graceful fallback.

Also covers the transliteration, which is catalogued as a *translation-only*
entry: it is a way to read the Qur'an rather than a language the interface exists
in, so it must appear under /translation and nowhere else.
"""

import main
from modules import TranslationRegistry
from locales import (
    DEFAULT_LANG, LANGUAGES, UI_LANGUAGES, get_language, is_supported,
    is_ui_language, normalize_lang,
)


class TestAvailable:
    def test_lists_bundled_languages(self):
        available = TranslationRegistry.available()
        assert {"en", "ru", "ar", "uz", "uz-Cyrl"} <= available

    def test_has_many_languages(self):
        assert len(TranslationRegistry.available()) >= 40


class TestCaching:
    def test_get_caches_instance(self):
        first = TranslationRegistry.get("ru")
        assert TranslationRegistry.is_cached("ru")
        assert TranslationRegistry.get("ru") is first

    def test_preload_returns_cached_instance(self):
        preloaded = TranslationRegistry.preload("en")
        assert TranslationRegistry.get("en") is preloaded


class TestFallback:
    def test_missing_language_falls_back_to_default(self):
        # "zz" has no bundled file, so the registry serves the default language.
        assert TranslationRegistry.get("zz") is TranslationRegistry.get(DEFAULT_LANG)


class TestTransliteration:

    def test_it_is_bundled_like_any_other_translation(self):
        assert "translit" in TranslationRegistry.available()
        text = TranslationRegistry.get("translit").get_ayah(1, 1)
        assert text.startswith("Bismillaahir Rahmaanir Raheem")

    def test_it_is_latin_script_not_arabic(self):
        # the whole point: readable by someone who cannot read the Arabic script
        text = TranslationRegistry.get("translit").get_ayah(2, 255)
        assert text.isascii()

    def test_it_covers_the_whole_quran(self):
        quran = TranslationRegistry.get("translit")
        assert quran.get_ayah(114, 6).startswith("Minal jinnati wan naas")

    def test_it_is_catalogued_but_not_an_interface_language(self):
        assert is_supported("translit")
        assert not is_ui_language("translit")
        assert "translit" in [l.code for l in LANGUAGES]
        assert "translit" not in [l.code for l in UI_LANGUAGES]

    def test_it_needs_no_string_table_of_its_own(self):
        from locales import missing_locales
        assert missing_locales() == []

    def test_it_is_offered_as_a_translation(self):
        codes = [b.callback_data.split(":", 1)[1]
                 for row in main.translation_language_keyboard().inline_keyboard
                 for b in row]
        assert "translit" in codes

    def test_it_is_not_offered_as_an_interface_language(self):
        codes = [b.callback_data.split(":", 1)[1]
                 for row in main.language_keyboard().inline_keyboard for b in row]
        assert "translit" not in codes

    def test_it_can_never_become_the_ui_language(self):
        # a stale or hand-crafted callback must not leave the user with an
        # interface that has no strings
        assert normalize_lang("translit") == DEFAULT_LANG

    def test_it_is_excluded_from_telegrams_command_menu(self):
        assert "translit" not in main._COMMAND_MENU_LANGS

    def test_get_language_still_resolves_it_for_display(self):
        assert get_language("translit").native == "Transliteration"
