# BismillahBot -- Explore the Holy Qur'an on Telegram
#
# Dependency-free UI internationalization: a dict-of-dicts keyed by language code,
# with a t(key, lang) helper that falls back to English per-key. Locale tables may
# be partial — any key a locale omits is served from English, so a half-translated
# language still works everywhere.

from functools import lru_cache
from importlib import import_module

from .languages import (  # re-exported for callers
    LANGUAGES, LANGUAGES_BY_CODE, UI_LANGUAGES, DEFAULT_LANG, Language,
    get_language, is_supported, is_ui_language, normalize_lang,
)


def _module_name(code: str) -> str:
    """Locale module basename for a language code: "uz-Cyrl" -> "uz_cyrl"."""
    return code.replace("-", "_").lower()


def _load_locales() -> dict[str, dict]:
    """Import one string table per catalogued language, keyed by language code.

    Driven by UI_LANGUAGES rather than a hand-written import list, so adding a
    language to the catalogue is enough. A language whose module is missing is
    skipped with a warning instead of breaking startup — `t()` then serves it
    from English. `missing_locales()` reports the gap (the test suite asserts
    it is empty).

    Translation-only entries (the transliteration) are skipped: they are a way to
    read the Qur'an, not a language the interface exists in, so having no string
    table is correct rather than a gap.
    """
    tables: dict[str, dict] = {}
    for lang in UI_LANGUAGES:
        try:
            module = import_module("." + _module_name(lang.code), __name__)
        except ImportError:
            print("LOCALE MISSING: %s (%s) falls back to English"
                  % (lang.code, lang.english))
            continue
        tables[lang.code] = module.strings
    return tables


LOCALES: dict[str, dict] = _load_locales()


def missing_locales() -> list[str]:
    """Interface languages with no locale table of their own."""
    return [lang.code for lang in UI_LANGUAGES if lang.code not in LOCALES]


# Phase 2 (docs/HIFZ_PLATFORM.md §5): group-cluster UI strings (`group_*`) are
# translated for these locales only, by deliberate scope decision — every other
# UI locale is *expected* to be missing them and falls back to English through
# t(). `missing_keys` below treats that as the intended shape, not a gap to
# report, so the 44-locale group_* absence does not fail `check_locales.py` or
# `tests/test_locales.py`. (Coincides with, but is independent of, the
# `_GROUP_LANGS` translation-language picker in `hifz/group.py` — same policy,
# different concern, and importing across that boundary would invert the
# dependency direction between `locales` and `hifz`.)
GROUP_LOCALES = frozenset({"en", "ru", "uz", "uz-Cyrl"})


def missing_keys(lang: str) -> list[str]:
    """English keys a locale does not define (each falls back to English).

    Excludes `group_*` keys for locales outside `GROUP_LOCALES` — those are
    supposed to be absent there, not a translation gap.
    """
    table = LOCALES.get(lang, {})
    gaps = [key for key in LOCALES[DEFAULT_LANG] if key not in table]
    if lang not in GROUP_LOCALES:
        gaps = [key for key in gaps if not key.startswith("group_")]
    return gaps


def t(key: str, lang: str = DEFAULT_LANG) -> str:
    """Localized UI string for `key`, falling back to English (then the key itself)."""
    table = LOCALES.get(lang)
    if table is not None and key in table:
        return table[key]
    return LOCALES[DEFAULT_LANG].get(key, key)


# --- Commands ------------------------------------------------------------------
# The bot's slash commands in menu order, each paired with its description key.
# Both the Telegram command menu and the /start message are generated from this
# one list, so a command added here shows up in every language at once — locales
# only translate the descriptions, never the list itself.

BOT_COMMANDS = (
    # Reading the Qur'an
    ("index", "cmd_index"),
    ("page", "cmd_page"),
    ("juz", "cmd_juz"),
    ("sajda", "cmd_sajda"),
    ("random", "cmd_random"),
    # Memorizing it — the hifz platform, in the order a user meets them:
    # commit to a plan, see how far you are, test yourself, correct a mistake,
    # then the two motivation surfaces.
    ("memorize", "cmd_memorize"),
    ("progress", "cmd_progress"),
    ("check", "cmd_check"),
    ("forgot", "cmd_forgot"),
    ("streak", "cmd_streak"),
    ("leaderboard", "cmd_leaderboard"),
    # Settings
    ("profile", "cmd_profile"),
    ("language", "cmd_language"),
    ("translation", "cmd_translation"),
    ("reciter", "cmd_reciter"),
    ("about", "cmd_about"),
)


def command_lines(lang: str) -> str:
    """The "/command — description" block, one line per registered command."""
    return "\n".join("/%s — %s" % (command, t(key, lang))
                     for command, key in BOT_COMMANDS)


def welcome_text(lang: str) -> str:
    """The /start message: localized prose around a generated command list."""
    return "\n\n".join((
        t("welcome_intro", lang),
        t("welcome_commands_header", lang) + "\n" + command_lines(lang),
        t("welcome_inline", lang),
    ))


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
