"""The /language and /translation pickers."""

from bot.keyboards.rows import button_rows
from channels import Choice, Choices
from domain.quran import TranslationRegistry
from locales import LANGUAGES, UI_LANGUAGES


def language_picker(languages, callback_prefix: str) -> Choices:
    """Every bundled language of `languages`, by native name, two per row; each
    button's callback is `callback_prefix` + the language code."""
    available = TranslationRegistry.available()
    return button_rows(
        [
            Choice(
                (lang.flag + " " + lang.native) if lang.flag else lang.native,
                data=callback_prefix + lang.code,
            )
            for lang in languages
            if lang.code in available
        ],
        2,
    )


def language_keyboard() -> Choices:
    """The *interface* language picker.

    UI_LANGUAGES rather than LANGUAGES: the transliteration is a way to read the
    Qur'an, not a language the bot's own text exists in, so it belongs in
    /translation only.
    """
    return language_picker(UI_LANGUAGES, "setlang:")


def translation_language_keyboard() -> Choices:
    """The Qur'an *translation* language picker, independent of the UI language."""
    return language_picker(LANGUAGES, "settranslang:")


SHORTLIST = 9  # + "More languages" = a 10-row WhatsApp list


def language_shortlist(more_label: str, more_data: str) -> Choices:
    """The first interface languages (UI_LANGUAGES is ordered by audience), one
    per row, then a row that opens the full picker."""
    flat = [choice for row in language_keyboard() for choice in row][:SHORTLIST]
    return [[choice] for choice in flat] + [[Choice("🌍 " + more_label, data=more_data)]]
