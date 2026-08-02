"""Durable per-user settings (`lib.user_settings.UserSettings`).

Exercised against the in-process in-memory store + MemoryStore stand-ins that
conftest pins via empty DATABASE_URL / REDIS_HOST_URL, so nothing here touches a
network. The three settings — UI language, translation language and reciter —
are independent by design; that independence and the one-shot migration of the
legacy Redis `lang:<chat_id>` key are what this module protects.
"""

from lib.user_settings import (
    DEFAULT_RECITER,
    DEFAULT_TRANSLATION_LANG,
    DEFAULT_UI_LANG,
    UserSettings,
)
from lib.utils import File


def _seed_legacy_lang(chat_id: int, code: str) -> None:
    """Write the pre-Postgres language key exactly as the old `File.save_lang`
    did — that writer is gone, so tests stand in for the historical bot."""
    file = File()
    file.redis.set(file._lang_key(chat_id), code)


class TestDefaults:
    async def test_new_user_gets_documented_defaults(self):
        settings = await UserSettings().get(700001, 700001)
        assert (settings.ui_lang, settings.translation_lang, settings.reciter) == (
            "en", "en", "Husary_128kbps")

    def test_module_defaults_match_documented_values(self):
        # The literals asserted above are the contract; keep the constants honest.
        assert (DEFAULT_UI_LANG, DEFAULT_TRANSLATION_LANG, DEFAULT_RECITER) == (
            "en", "en", "Husary_128kbps")

    async def test_supplied_default_seeds_both_languages(self):
        # No legacy value: the caller-supplied default (derived from Telegram's
        # language_code on first contact) becomes both UI and translation lang.
        settings = await UserSettings().get(700002, 700002, default_ui_lang="tr")
        assert settings.ui_lang == "tr"
        assert settings.translation_lang == "tr"
        assert settings.reciter == DEFAULT_RECITER

    async def test_set_ui_lang_on_an_unseen_user_seeds_both_languages(self):
        # Row creation always couples the two languages (same rule the legacy
        # migration follows): `set_ui_lang` hands the chosen code in as the
        # creation default, so a first-ever pick seeds the translation too.
        # Unreachable from handle_update — it resolves settings, creating the
        # row, before any callback runs — but pinned so the asymmetry with
        # set_translation_lang/set_reciter below stays deliberate.
        user_settings = UserSettings()
        await user_settings.set_ui_lang(700004, 700004, "ru")
        assert (await user_settings.get(700004, 700004)).translation_lang == "ru"

    async def test_set_translation_lang_on_an_unseen_user_leaves_ui_default(self):
        user_settings = UserSettings()
        await user_settings.set_translation_lang(700005, 700005, "ru")
        settings = await user_settings.get(700005, 700005)
        assert settings.ui_lang == DEFAULT_UI_LANG
        assert settings.translation_lang == "ru"

    async def test_set_reciter_on_an_unseen_user_leaves_languages_default(self):
        user_settings = UserSettings()
        await user_settings.set_reciter(700006, 700006, "Alafasy_128kbps")
        settings = await user_settings.get(700006, 700006)
        assert (settings.ui_lang, settings.translation_lang) == (
            DEFAULT_UI_LANG, DEFAULT_TRANSLATION_LANG)
        assert settings.reciter == "Alafasy_128kbps"

    async def test_supplied_default_is_ignored_once_the_row_exists(self):
        user_settings = UserSettings()
        await user_settings.set_ui_lang(700003, 700003, "ru")
        # A later contact from a differently-configured Telegram client must not
        # silently overwrite what the user explicitly chose.
        settings = await user_settings.get(700003, 700003, default_ui_lang="fr")
        assert settings.ui_lang == "ru"


class TestRoundTrip:
    async def test_ui_lang_round_trips(self):
        user_settings = UserSettings()
        await user_settings.set_ui_lang(700010, 700010, "ru")
        assert (await user_settings.get(700010, 700010)).ui_lang == "ru"

    async def test_translation_lang_round_trips(self):
        user_settings = UserSettings()
        await user_settings.set_translation_lang(700011, 700011, "tr")
        assert (await user_settings.get(700011, 700011)).translation_lang == "tr"

    async def test_reciter_round_trips(self):
        user_settings = UserSettings()
        await user_settings.set_reciter(700012, 700012, "Alafasy_128kbps")
        assert (await user_settings.get(700012, 700012)).reciter == "Alafasy_128kbps"

    async def test_setter_overwrites_previous_value(self):
        user_settings = UserSettings()
        await user_settings.set_ui_lang(700013, 700013, "ru")
        await user_settings.set_ui_lang(700013, 700013, "fr")
        assert (await user_settings.get(700013, 700013)).ui_lang == "fr"


class TestIndependence:
    """The point of the feature: three settings, no coupling between them."""

    async def test_setting_ui_lang_leaves_the_others_alone(self):
        user_settings = UserSettings()
        await user_settings.get(700020, 700020)      # existing user, English defaults
        await user_settings.set_ui_lang(700020, 700020, "ru")
        settings = await user_settings.get(700020, 700020)
        assert settings.translation_lang == DEFAULT_TRANSLATION_LANG
        assert settings.reciter == DEFAULT_RECITER

    async def test_setting_translation_lang_leaves_the_others_alone(self):
        user_settings = UserSettings()
        await user_settings.set_ui_lang(700021, 700021, "ru")
        await user_settings.set_translation_lang(700021, 700021, "tr")
        settings = await user_settings.get(700021, 700021)
        assert settings.ui_lang == "ru"
        assert settings.reciter == DEFAULT_RECITER

    async def test_setting_reciter_leaves_the_languages_alone(self):
        user_settings = UserSettings()
        await user_settings.set_ui_lang(700022, 700022, "ru")
        await user_settings.set_translation_lang(700022, 700022, "tr")
        await user_settings.set_reciter(700022, 700022, "Alafasy_128kbps")
        settings = await user_settings.get(700022, 700022)
        assert settings.ui_lang == "ru"
        assert settings.translation_lang == "tr"

    async def test_uzbek_cyrillic_ui_with_english_translation(self):
        # The motivating requirement: read the bot in Uzbek Cyrillic while
        # keeping the English translation of the Qur'an.
        user_settings = UserSettings()
        await user_settings.set_ui_lang(700023, 700023, "uz-Cyrl")
        await user_settings.set_translation_lang(700023, 700023, "en")
        settings = await user_settings.get(700023, 700023)
        assert settings.ui_lang == "uz-Cyrl"
        assert settings.translation_lang == "en"

    async def test_all_three_can_differ_at_once(self):
        user_settings = UserSettings()
        await user_settings.set_ui_lang(700024, 700024, "uz-Cyrl")
        await user_settings.set_translation_lang(700024, 700024, "ru")
        await user_settings.set_reciter(700024, 700024, "Alafasy_128kbps")
        settings = await user_settings.get(700024, 700024)
        assert (settings.ui_lang, settings.translation_lang, settings.reciter) == (
            "uz-Cyrl", "ru", "Alafasy_128kbps")


class TestLegacyMigration:
    async def test_legacy_language_seeds_both_languages(self):
        _seed_legacy_lang(700030, "ru")
        settings = await UserSettings().get(700030, 700030)
        # Pre-migration the single Redis key drove both, so preserve that on the
        # first post-migration read rather than resetting anyone to English.
        assert settings.ui_lang == "ru"
        assert settings.translation_lang == "ru"
        assert settings.reciter == DEFAULT_RECITER

    async def test_legacy_language_beats_the_supplied_default(self):
        _seed_legacy_lang(700031, "ru")
        settings = await UserSettings().get(700031, 700031, default_ui_lang="fr")
        assert settings.ui_lang == "ru"

    async def test_legacy_key_is_deleted_after_migration(self):
        _seed_legacy_lang(700032, "ru")
        await UserSettings().get(700032, 700032)
        assert File().get_lang(700032) is None

    async def test_migrated_row_is_authoritative_on_the_second_read(self):
        user_settings = UserSettings()
        _seed_legacy_lang(700033, "ru")
        await user_settings.get(700033, 700033)
        # The legacy key is gone by now; the Postgres row must still answer.
        settings = await user_settings.get(700033, 700033)
        assert settings.ui_lang == "ru"
        assert settings.translation_lang == "ru"

    async def test_post_migration_edits_survive_the_vanished_legacy_key(self):
        user_settings = UserSettings()
        _seed_legacy_lang(700034, "ru")
        await user_settings.get(700034, 700034)
        await user_settings.set_translation_lang(700034, 700034, "en")
        settings = await user_settings.get(700034, 700034)
        assert settings.ui_lang == "ru"
        assert settings.translation_lang == "en"


class TestInlineCaller:
    """Inline queries have a user but no chat, so they pass chat_id=None."""

    async def test_get_without_chat_id_returns_defaults(self):
        settings = await UserSettings().get(700040, None)
        assert (settings.ui_lang, settings.translation_lang, settings.reciter) == (
            DEFAULT_UI_LANG, DEFAULT_TRANSLATION_LANG, DEFAULT_RECITER)

    async def test_get_without_chat_id_skips_the_legacy_lookup(self):
        # A legacy key exists under an unrelated chat id; with no chat id to key
        # on there is nothing to migrate, and it must not be picked up.
        _seed_legacy_lang(700041, "ru")
        settings = await UserSettings().get(700042, None)
        assert settings.ui_lang == DEFAULT_UI_LANG
        assert settings.translation_lang == DEFAULT_TRANSLATION_LANG
        assert File().get_lang(700041) == "ru"   # left untouched

    async def test_inline_setter_without_chat_id_persists(self):
        user_settings = UserSettings()
        await user_settings.set_ui_lang(700043, None, "ru")
        assert (await user_settings.get(700043, None)).ui_lang == "ru"


class TestKeyedByUserId:
    async def test_same_user_sees_the_same_settings_from_any_chat(self):
        user_settings = UserSettings()
        await user_settings.set_ui_lang(700050, 700050, "ru")
        # Same Telegram user reaching us through a different chat id.
        settings = await user_settings.get(700050, 999050)
        assert settings.ui_lang == "ru"

    async def test_different_users_do_not_share_settings(self):
        user_settings = UserSettings()
        await user_settings.set_ui_lang(700051, 700051, "ru")
        assert (await user_settings.get(700052, 700052)).ui_lang == DEFAULT_UI_LANG

    async def test_legacy_key_of_another_chat_is_not_migrated(self):
        _seed_legacy_lang(999053, "ru")
        settings = await UserSettings().get(700053, 700053)
        assert settings.ui_lang == DEFAULT_UI_LANG
        assert File().get_lang(999053) == "ru"
