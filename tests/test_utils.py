"""File helper: media URL construction and the Redis-backed state store
(exercised here against the in-memory fallback)."""

import pytest

from lib.utils import File


class TestAudioFilename:
    def test_known_performer_zero_padded(self):
        url = File().get_audio_filename(1, 1, "Husary_128kbps")
        assert url.endswith("/Husary_128kbps/001001.mp3")

    def test_three_digit_padding(self):
        url = File().get_audio_filename(2, 255, "Husary_128kbps")
        assert url.endswith("/002255.mp3")

    def test_unknown_performer_raises(self):
        with pytest.raises(ValueError):
            File().get_audio_filename(1, 1, "NoSuchReciter")


class TestImageFilename:
    def test_image_path(self):
        assert File().get_image_filename(2, 255).endswith("/2_255.png")


class TestStateStore:
    def test_user_state_round_trips(self):
        File().save_user(900001, (2, 255, "translation"))
        # JSON round-trip turns the stored tuple into a list.
        assert File().get_user(900001) == [2, 255, "translation"]

    def test_missing_user_state_is_none(self):
        assert File().get_user(900002) is None

    def test_file_id_cache_round_trips(self):
        File().save_file("media/x.png", "FILEID-123")
        assert File().get_file("media/x.png") == "FILEID-123"

    def test_empty_file_id_is_not_cached(self):
        File().save_file("media/y.png", "")
        assert File().get_file("media/y.png") is None


class TestLegacyLanguageKey:
    """Language preferences now live in Postgres (see tests/test_user_settings.py);
    `File.save_lang` is gone. What survives here is the migration-on-read half of
    the old key: read whatever an older bot version wrote, then drop it once
    `UserSettings` has absorbed it."""

    def test_legacy_language_is_readable_then_deletable(self):
        file = File()
        file.redis.set(file._lang_key(900003), "ru")   # as the retired save_lang wrote it
        assert file.get_lang(900003) == "ru"
        file.delete_lang(900003)
        assert file.get_lang(900003) is None

    def test_missing_language_is_none(self):
        assert File().get_lang(900004) is None

    def test_deleting_an_absent_language_is_a_no_op(self):
        File().delete_lang(900005)   # migration runs unconditionally; must not raise
        assert File().get_lang(900005) is None
