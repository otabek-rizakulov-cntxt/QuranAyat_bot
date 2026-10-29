"""bot.keyboards.time_pickers.offset_keyboard — the one UTC-offset picker that
/profile, the /memorize wizard and group setup share."""

from bot.keyboards.time_pickers import offset_keyboard
from domain.localtime import offset_options


def _grid(markup):
    return [[(b.text, b.callback_data) for b in row] for row in markup.inline_keyboard]


def test_every_offset_is_offered_in_order_under_the_callers_prefix():
    flat = [cell for row in _grid(offset_keyboard("en", "gr:tz:")) for cell in row]
    assert flat == [(o, "gr:tz:" + o) for o in offset_options()]


def test_rows_are_columns_wide():
    rows = _grid(offset_keyboard("en", "hp:tz:", columns=4))
    assert all(len(r) == 4 for r in rows[:-1]) and 1 <= len(rows[-1]) <= 4


def test_a_label_prefix_changes_only_the_label():
    first = _grid(offset_keyboard("en", "hm:tz:", label_prefix="UTC"))[0][0]
    assert first == ("UTC" + offset_options()[0], "hm:tz:" + offset_options()[0])


def test_cancel_data_adds_a_localized_cancel_row():
    last = _grid(offset_keyboard("ru", "hm:tz:", cancel_data="hm:x"))[-1]
    assert last == [("Отмена", "hm:x")]


def test_no_cancel_row_unless_asked():
    rows = _grid(offset_keyboard("en", "gr:tz:"))
    assert all(cb.startswith("gr:tz:") for row in rows for _, cb in row)
