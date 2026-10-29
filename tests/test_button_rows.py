"""bot.keyboards.rows.button_rows — the one row-packing helper."""

from bot.keyboards.rows import button_rows


def test_packs_in_order_with_a_short_last_row():
    assert button_rows([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_an_exact_fit_has_no_empty_trailing_row():
    assert button_rows([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_nothing_in_nothing_out():
    assert button_rows([], 3) == []


def test_a_non_positive_width_is_one_per_row():
    assert button_rows([1, 2], 0) == [[1], [2]]
