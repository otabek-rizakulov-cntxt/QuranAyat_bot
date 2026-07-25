"""Reference parsing: `parse_ayah` and `parse_ayah_range` in main.py."""

import main


class TestParseAyah:
    def test_colon_separator(self):
        assert main.parse_ayah("2:255") == (2, 255)

    def test_space_separator(self):
        assert main.parse_ayah("2 255") == (2, 255)

    def test_all_accepted_separators(self):
        for sep in (":", " ", "-", ";", ".", ","):
            assert main.parse_ayah("2%s255" % sep) == (2, 255), sep

    def test_surah_only_defaults_to_ayah_1(self):
        assert main.parse_ayah("2") == (2, 1)

    def test_leading_slash_tolerated(self):
        assert main.parse_ayah("/2:255") == (2, 255)

    def test_non_numeric_returns_none(self):
        assert main.parse_ayah("hello") == (None, None)

    def test_empty_returns_none(self):
        assert main.parse_ayah("") == (None, None)


class TestParseAyahRange:
    def test_single_ayah_collapses_to_point_range(self):
        assert main.parse_ayah_range("2:255") == (2, 255, 255)

    def test_hyphen_range(self):
        assert main.parse_ayah_range("53:1-7") == (53, 1, 7)

    def test_en_dash_range(self):
        assert main.parse_ayah_range("53:1–7") == (53, 1, 7)

    def test_reversed_range_is_sorted(self):
        assert main.parse_ayah_range("53:7-1") == (53, 1, 7)

    def test_spaces_around_dash(self):
        assert main.parse_ayah_range("53:1 - 7") == (53, 1, 7)

    def test_surah_only(self):
        assert main.parse_ayah_range("2") == (2, 1, 1)

    def test_invalid_returns_none_triple(self):
        assert main.parse_ayah_range("hello") == (None, None, None)
