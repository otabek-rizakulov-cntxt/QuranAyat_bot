"""The /language and /translation pickers."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.rows import button_rows
from domain.quran import TranslationRegistry
from locales import LANGUAGES, UI_LANGUAGES


def language_picker(languages, callback_prefix: str) -> InlineKeyboardMarkup:
    """Every bundled language of `languages`, by native name, two per row; each
    button's callback is `callback_prefix` + the language code."""
    available = TranslationRegistry.available()
    return InlineKeyboardMarkup(
        button_rows(
            [
                InlineKeyboardButton(
                    (lang.flag + " " + lang.native) if lang.flag else lang.native,
                    callback_data=callback_prefix + lang.code,
                )
                for lang in languages
                if lang.code in available
            ],
            2,
        )
    )


def language_keyboard() -> InlineKeyboardMarkup:
    """The *interface* language picker.

    UI_LANGUAGES rather than LANGUAGES: the transliteration is a way to read the
    Qur'an, not a language the bot's own text exists in, so it belongs in
    /translation only.
    """
    return language_picker(UI_LANGUAGES, "setlang:")


def translation_language_keyboard() -> InlineKeyboardMarkup:
    """The Qur'an *translation* language picker, independent of the UI language."""
    return language_picker(LANGUAGES, "settranslang:")
