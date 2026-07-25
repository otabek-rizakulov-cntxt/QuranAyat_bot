"""TranslationRegistry: lazy loading, caching, and graceful fallback."""

from modules import TranslationRegistry
from locales import DEFAULT_LANG


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
