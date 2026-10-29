"""The /language and /translation pickers."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from locales import LANGUAGES, UI_LANGUAGES
from modules import TranslationRegistry


def language_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard of every bundled *interface* language (native names), two
    per row.

    UI_LANGUAGES rather than LANGUAGES: the transliteration is a way to read the
    Qur'an, not a language the bot's own text exists in, so it belongs in
    /translation only.
    """
    available = TranslationRegistry.available()
    rows, row = [], []
    for lang in UI_LANGUAGES:
        if lang.code not in available:
            continue
        label = (lang.flag + " " + lang.native) if lang.flag else lang.native
        row.append(InlineKeyboardButton(label, callback_data="setlang:" + lang.code))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


def translation_language_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for picking the Qur'an *translation* language, independently
    of the UI language. Same shape as language_keyboard(), different callback."""
    available = TranslationRegistry.available()
    rows, row = [], []
    for lang in LANGUAGES:
        if lang.code not in available:
            continue
        label = (lang.flag + " " + lang.native) if lang.flag else lang.native
        row.append(InlineKeyboardButton(label, callback_data="settranslang:" + lang.code))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)
