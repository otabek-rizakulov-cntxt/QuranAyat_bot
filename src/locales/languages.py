# BismillahBot -- Explore the Holy Qur'an on Telegram
#
# Language catalogue: the single source of truth for which languages the bot
# offers, how their names are shown in the /language picker, whether they render
# right-to-left, and (for the offline bundler) which tanzil/alquran.cloud edition
# supplies the Qur'an translation text.
#
# The running bot only reads `code`, `native`, `english`, `rtl`, `flag`. The
# `edition` field is consumed exclusively by scripts/bundle_translations.py when it
# fetches and converts the translation files into translations/<code>.txt — the app
# never touches the network.

from dataclasses import dataclass


# Sentinel editions handled specially by the bundler:
#   __arabic__      -> fetch the original Arabic mushaf (quran-simple)
#   __translit_uz__ -> derive Uzbek Latin from the bundled Uzbek Cyrillic file
ARABIC_ORIGINAL = "__arabic__"
TRANSLIT_UZ = "__translit_uz__"


@dataclass(frozen=True)
class Language:
    code: str          # our internal code (usually ISO 639-1, plus uz-Cyrl)
    native: str        # endonym shown on the /language keyboard
    english: str       # English name (for logs, attribution, fallback labels)
    rtl: bool          # right-to-left script (Telegram renders it correctly on its own)
    edition: str       # alquran.cloud edition id, or a sentinel above
    flag: str = ""     # representative flag emoji for the /language picker (see note below)
    # True for entries that are a way to *read the Qur'an* rather than a language
    # the interface can be shown in — currently the Latin transliteration. They
    # appear in /translation only: they have no UI string table (and are not
    # expected to have one), no Telegram command menu, and cannot be set as a UI
    # language. See UI_LANGUAGES below.
    translation_only: bool = False


# Ordered for the /language picker: English first, then the Central-Asia-focused
# core (the bot's primary audience), then the rest grouped roughly by region.
#
# `flag` is a representative flag emoji shown before the endonym in the picker.
# A language is not a country, so a few are judgment calls: Arabic uses a pan-Arab
# stand-in (🇸🇦), and stateless languages with no flag emoji of their own (Kurdish,
# Uyghur, Tatar, Chechen, Berber) use the flag of the country with the most
# speakers purely as a geographic marker. Any of these is a one-line change here.
LANGUAGES: list[Language] = [
    Language("en",      "English",           "English",             False, "en.ahmedraza",    "🇬🇧"),
    Language("ar",      "العربية",            "Arabic",              True,  ARABIC_ORIGINAL,   "🇸🇦"),
    # Not a language: the Arabic sounded out in Latin letters, for the many readers
    # who can follow the recitation but cannot read the script. Offered under
    # /translation only — see `translation_only` above.
    Language("translit", "Transliteration",  "Transliteration (Latin)", False,
             "en.transliteration", "🔤", translation_only=True),
    Language("ru",      "Русский",           "Russian",             False, "ru.kuliev",       "🇷🇺"),
    Language("uz-Cyrl", "Ўзбекча (Кирилл)",  "Uzbek (Cyrillic)",    False, "uz.sodik",        "🇺🇿"),
    Language("uz",      "Oʻzbekcha (Lotin)", "Uzbek (Latin)",       False, TRANSLIT_UZ,       "🇺🇿"),
    Language("tr",      "Türkçe",            "Turkish",             False, "tr.diyanet",      "🇹🇷"),
    Language("ur",      "اردو",               "Urdu",                True,  "ur.jalandhry",    "🇵🇰"),
    Language("fa",      "فارسی",              "Persian",             True,  "fa.makarem",      "🇮🇷"),
    Language("tg",      "Тоҷикӣ",            "Tajik",               False, "tg.ayati",        "🇹🇯"),
    Language("az",      "Azərbaycan",        "Azerbaijani",         False, "az.musayev",      "🇦🇿"),
    Language("id",      "Bahasa Indonesia",  "Indonesian",          False, "id.indonesian",   "🇮🇩"),
    Language("ms",      "Bahasa Melayu",     "Malay",               False, "ms.basmeih",      "🇲🇾"),
    Language("fr",      "Français",          "French",              False, "fr.hamidullah",   "🇫🇷"),
    Language("de",      "Deutsch",           "German",              False, "de.bubenheim",    "🇩🇪"),
    Language("es",      "Español",           "Spanish",             False, "es.cortes",       "🇪🇸"),
    Language("pt",      "Português",         "Portuguese",          False, "pt.elhayek",      "🇵🇹"),
    Language("it",      "Italiano",          "Italian",             False, "it.piccardo",     "🇮🇹"),
    Language("nl",      "Nederlands",        "Dutch",               False, "nl.siregar",      "🇳🇱"),
    Language("bs",      "Bosanski",          "Bosnian",             False, "bs.korkut",       "🇧🇦"),
    Language("sq",      "Shqip",             "Albanian",            False, "sq.nahi",         "🇦🇱"),
    Language("bg",      "Български",          "Bulgarian",           False, "bg.theophanov",   "🇧🇬"),
    Language("cs",      "Čeština",           "Czech",               False, "cs.hrbek",        "🇨🇿"),
    Language("pl",      "Polski",            "Polish",              False, "pl.bielawskiego", "🇵🇱"),
    Language("ro",      "Română",            "Romanian",            False, "ro.grigore",      "🇷🇴"),
    Language("sv",      "Svenska",           "Swedish",             False, "sv.bernstrom",    "🇸🇪"),
    Language("no",      "Norsk",             "Norwegian",           False, "no.berg",         "🇳🇴"),
    Language("bn",      "বাংলা",              "Bengali",             False, "bn.bengali",      "🇧🇩"),
    Language("hi",      "हिन्दी",              "Hindi",               False, "hi.farooq",       "🇮🇳"),
    Language("ta",      "தமிழ்",              "Tamil",               False, "ta.tamil",        "🇮🇳"),
    Language("ml",      "മലയാളം",            "Malayalam",           False, "ml.abdulhameed",  "🇮🇳"),
    Language("th",      "ไทย",                "Thai",                False, "th.thai",         "🇹🇭"),
    Language("zh",      "中文",               "Chinese",             False, "zh.majian",       "🇨🇳"),
    Language("ja",      "日本語",              "Japanese",            False, "ja.japanese",     "🇯🇵"),
    Language("ko",      "한국어",              "Korean",              False, "ko.korean",       "🇰🇷"),
    # ku.asan is Sorani in Arabic script, so this entry is RTL and its endonym
    # is written in that script (not the Latin/Kurmanji "Kurdî").
    Language("ku",      "کوردی",              "Kurdish (Sorani)",    True,  "ku.asan",         "🇮🇶"),
    Language("ha",      "Hausa",             "Hausa",               False, "ha.gumi",         "🇳🇬"),
    Language("so",      "Soomaali",          "Somali",              False, "so.abduh",        "🇸🇴"),
    Language("sw",      "Kiswahili",         "Swahili",             False, "sw.barwani",      "🇹🇿"),
    Language("am",      "አማርኛ",              "Amharic",             False, "am.sadiq",        "🇪🇹"),
    Language("sd",      "سنڌي",               "Sindhi",              True,  "sd.amroti",       "🇵🇰"),
    Language("ug",      "ئۇيغۇرچە",           "Uyghur",              True,  "ug.saleh",        "🇨🇳"),
    Language("ps",      "پښتو",               "Pashto",              True,  "ps.abdulwali",    "🇦🇫"),
    Language("dv",      "ދިވެހި",              "Divehi",              True,  "dv.divehi",       "🇲🇻"),
    Language("si",      "සිංහල",              "Sinhala",             False, "si.naseemismail", "🇱🇰"),
    Language("my",      "မြန်မာ",              "Burmese",             False, "my.ghazi",        "🇲🇲"),
    Language("tt",      "Татарча",           "Tatar",               False, "tt.nugman",       "🇷🇺"),
    Language("ce",      "Нохчийн",           "Chechen",             False, "ce.magomedov",    "🇷🇺"),
    Language("ber",     "Tamaziɣt",          "Berber",              False, "ber.mensur",      "🇩🇿"),
]

# code -> Language, and the default the whole bot falls back to.
LANGUAGES_BY_CODE: dict[str, Language] = {lang.code: lang for lang in LANGUAGES}
DEFAULT_LANG = "en"

# Languages the *interface* can be shown in — everything except the reading aids.
# This is the list that must have a complete locale table, and the one /language
# offers; /translation offers all of LANGUAGES.
UI_LANGUAGES: list[Language] = [lang for lang in LANGUAGES if not lang.translation_only]


def get_language(code: str) -> Language:
    """Return the Language for `code`, or the English default if unknown."""
    return LANGUAGES_BY_CODE.get(code, LANGUAGES_BY_CODE[DEFAULT_LANG])


def is_supported(code: str) -> bool:
    return code in LANGUAGES_BY_CODE


def is_ui_language(code: str) -> bool:
    """Whether `code` may be used as an interface language (i.e. has a string
    table). False for reading aids like the transliteration, which are offered
    as a translation but can never be the UI."""
    lang = LANGUAGES_BY_CODE.get(code)
    return lang is not None and not lang.translation_only


def normalize_lang(code: str | None) -> str:
    """Map an arbitrary Telegram language_code to a supported code.

    Telegram sends tags like "tr", "en-US", "uz-Latn"; we take the primary
    subtag and use it if supported, else fall back to English. The special
    "uz-Cyrl" full tag is honoured when sent verbatim.
    """
    if not code:
        return DEFAULT_LANG
    if is_ui_language(code):
        return code
    primary = code.split("-", 1)[0].lower()
    return primary if is_ui_language(primary) else DEFAULT_LANG
