# BismillahBot -- Explore the Holy Qur'an on Telegram
#
# Dependency-free UI internationalization: a dict-of-dicts keyed by language code,
# with a t(key, lang) helper that falls back to English per-key. Locale tables may
# be partial — any key a locale omits is served from English, so a half-translated
# language still works everywhere.

from functools import lru_cache

from .languages import (  # re-exported for callers
    LANGUAGES, LANGUAGES_BY_CODE, DEFAULT_LANG, Language,
    get_language, is_supported, normalize_lang,
)
from . import en, ru, tr, uz, uz_cyrl, az, ar, fa, ur, tg
from . import id as _id  # avoid shadowing the builtin id()

LOCALES: dict[str, dict] = {
    "en": en.strings,
    "ru": ru.strings,
    "tr": tr.strings,
    "uz": uz.strings,
    "uz-Cyrl": uz_cyrl.strings,
    "az": az.strings,
    "id": _id.strings,
    "ar": ar.strings,
    "fa": fa.strings,
    "ur": ur.strings,
    "tg": tg.strings,
}


def t(key: str, lang: str = DEFAULT_LANG) -> str:
    """Localized UI string for `key`, falling back to English (then the key itself)."""
    table = LOCALES.get(lang)
    if table is not None and key in table:
        return table[key]
    return LOCALES[DEFAULT_LANG].get(key, key)


# --- Reply-keyboard localization -----------------------------------------------
# The reply keyboard shows localized labels, but taps arrive as plain text. We map
# each incoming label back to a canonical action so navigation stays intact whatever
# the user's language is.

# canonical action -> its button string key
ACTION_BUTTON_KEYS = {
    "arabic": "btn_arabic",
    "audio": "btn_audio",
    "translation": "btn_translation",
    "tafsir": "btn_tafsir",
    "previous": "btn_previous",
    "random": "btn_random",
    "next": "btn_next",
}


def keyboard_rows(lang: str) -> list[list[str]]:
    """The reply-keyboard layout with localized labels, in display order."""
    return [
        [t("btn_arabic", lang), t("btn_audio", lang), t("btn_translation", lang), t("btn_tafsir", lang)],
        [t("btn_previous", lang), t("btn_random", lang), t("btn_next", lang)],
    ]


@lru_cache(maxsize=None)
def _reverse_button_map(lang: str) -> dict[str, str]:
    """{lowercased label -> canonical action} for `lang`, English, and canonical words."""
    m: dict[str, str] = {}
    for action, btn_key in ACTION_BUTTON_KEYS.items():
        m[action] = action                                     # canonical word ("next")
        m[t(btn_key, DEFAULT_LANG).strip().lower()] = action   # English label
        m[t(btn_key, lang).strip().lower()] = action           # localized label
    m["english"] = "translation"  # legacy: old label and stored state value
    return m


def button_action(text: str, lang: str) -> str | None:
    """Canonical action for an incoming button tap, or None if it isn't a button."""
    return _reverse_button_map(lang).get(text.strip().lower())
