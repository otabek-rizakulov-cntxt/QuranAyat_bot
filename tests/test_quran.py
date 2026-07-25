"""Quran corpus model: bounds, navigation wraparound, and corpus integrity."""

from modules import Quran, TranslationRegistry


class TestStructure:
    def test_114_surahs(self):
        assert len(Quran.surah_lengths) == 114
        assert len(Quran.surah_names) == 114

    def test_total_ayah_count_is_6236(self):
        assert sum(Quran.surah_lengths) == 6236


class TestExists:
    def test_valid_references(self):
        assert Quran.exists(1, 1)
        assert Quran.exists(2, 255)
        assert Quran.exists(114, 6)

    def test_surah_out_of_range(self):
        assert not Quran.exists(0, 1)
        assert not Quran.exists(115, 1)

    def test_ayah_out_of_range(self):
        assert not Quran.exists(1, 0)
        assert not Quran.exists(1, 8)     # Al-Faatiha has 7 ayahs
        assert not Quran.exists(2, 287)   # Al-Baqara has 286 ayahs


class TestNavigation:
    def test_next_within_surah(self):
        assert Quran.get_next_ayah(2, 1) == (2, 2)

    def test_next_wraps_to_following_surah(self):
        assert Quran.get_next_ayah(1, 7) == (2, 1)

    def test_next_wraps_around_end_of_quran(self):
        assert Quran.get_next_ayah(114, 6) == (1, 1)

    def test_previous_within_surah(self):
        assert Quran.get_previous_ayah(2, 2) == (2, 1)

    def test_previous_wraps_to_preceding_surah(self):
        assert Quran.get_previous_ayah(2, 1) == (1, 7)

    def test_previous_wraps_around_start_of_quran(self):
        assert Quran.get_previous_ayah(1, 1) == (114, 6)

    def test_next_then_previous_is_identity(self):
        for s, a in [(1, 1), (1, 7), (2, 286), (9, 127), (114, 6)]:
            ns, na = Quran.get_next_ayah(s, a)
            assert Quran.get_previous_ayah(ns, na) == (s, a)


class TestRandom:
    def test_random_ayah_always_in_bounds(self):
        for _ in range(300):
            s, a = Quran.get_random_ayah()
            assert Quran.exists(s, a), (s, a)


class TestSurahMeta:
    def test_surah_length(self):
        assert Quran.get_surah_length(1) == 7
        assert Quran.get_surah_length(2) == 286

    def test_surah_name(self):
        assert Quran.get_surah_name(1) == "Al-Faatiha"


class TestCorpusIntegrity:
    """These load the real bundled corpora, so they double as data-integrity checks."""

    def test_english_translation_parses_completely(self):
        quran = TranslationRegistry.get("en")
        assert sum(len(surah) for surah in quran.text) == 6236

    def test_get_ayah_appends_reference(self):
        quran = TranslationRegistry.get("en")
        text = quran.get_ayah(1, 1)
        assert text.endswith("(1:1)")

    def test_get_ayahs_range_appends_reference(self):
        quran = TranslationRegistry.get("en")
        assert quran.get_ayahs(1, 1, 3).endswith("(1:1-3)")

    def test_tafsir_parses_completely(self):
        tafsir = Quran.from_tafsir()
        assert sum(len(surah) for surah in tafsir.text) == 6236
        assert tafsir.get_ayah(1, 1).endswith("(1:1)")
