"""The UTC-offset picker, shared by /profile, the /memorize wizard and group setup."""

from typing import Optional

from telegram import InlineKeyboardMarkup

from bot.keyboards.rows import button_rows
from channels import Choice, Choices
from channels.telegram import to_markup
from domain.localtime import offset_options
from locales import t


def offset_keyboard(
    ui_lang: str,
    prefix: str,
    columns: int = 4,
    cancel_data: Optional[str] = None,
    label_prefix: str = "",
) -> InlineKeyboardMarkup:
    """`offset_choices` as Telegram markup, for the hifz features not yet on a channel."""
    return to_markup(offset_choices(ui_lang, prefix, columns, cancel_data, label_prefix))


def offset_choices(
    ui_lang: str,
    prefix: str,
    columns: int = 4,
    cancel_data: Optional[str] = None,
    label_prefix: str = "",
) -> Choices:
    """Every offset the picker offers (see domain/localtime.py), `columns` per row.

    The labels *are* the offsets ("+05:00", or "UTC+05:00" with
    `label_prefix="UTC"`), so this keyboard needs no translation — half the
    reason the fixed-offset model was chosen over IANA zone names. Each button's
    callback_data is `prefix` + the offset, so every feature keeps routing its
    own taps. `cancel_data` adds a trailing Cancel row when given.
    """
    buttons = [Choice(label_prefix + offset, data=prefix + offset) for offset in offset_options()]
    rows = button_rows(buttons, columns)
    if cancel_data:
        rows.append([Choice(t("btn_cancel", ui_lang), data=cancel_data)])
    return rows
