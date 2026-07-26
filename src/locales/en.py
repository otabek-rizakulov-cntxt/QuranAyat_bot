# English — the canonical UI strings. Every other locale falls back to these
# per-key, so this table must define every key the bot uses.

strings = {
    "welcome_intro": (
        "Send me a surah and ayah number, for example <b>2:255</b>, and I'll reply with "
        "that verse of the Holy Qur'an.\n\n"
        "You can also send a range like <b>59:22-24</b> for a combined audio recitation."
    ),
    "welcome_commands_header": "Commands:",
    "welcome_inline": (
        "You can use me inline in any chat: type <b>@QuranAyat_bot</b> followed by a "
        "reference."
    ),
    "about": (
        "This bot lets you explore the Holy Qur'an on Telegram in many languages.\n\n"
        "Translations are sourced from tanzil.net (see ATTRIBUTIONS.md for each "
        "translation's edition and translator). Audio recitations are sourced from "
        "everyayah.com — pick your reciter any time with /reciter. The tafsir is "
        "Tafsir al-Jalalayn (altafsir.com), available in English.\n\n"
        "Change your UI language with /language, and your translation language "
        "separately with /translation."
    ),
    "ayah_not_found": "Ayah does not exist!",
    "range_too_large": "Range too large, please request at most {n} ayahs at a time.",
    "choose_language": "Choose your language:",
    "language_set": "Language set to {lang}.",
    "choose_translation_language": "Choose your translation language:",
    "translation_language_set": "Translation language set to {lang}.",
    "choose_reciter": "Choose a reciter:",
    "reciter_set": "Reciter set to {reciter}.",
    "btn_search_reciter": "Search by name",
    "reciter_search_prompt": "Type a reciter's name to search (e.g. \"Sudais\", \"Basit\").",
    "reciter_search_no_matches": "No reciters matched that name — try again.",
    "reciter_search_results": "Search results:",
    "btn_set_reciter": "Set as my reciter",
    "reciter_inline_description": "Tap to set as your reciter",
    "tafsir_en_note": "\n\n(Tafsir is available in English only.)",
    "btn_translation": "Translation",
    "btn_tafsir": "Tafsir",
    "btn_arabic": "Arabic",
    "btn_audio": "Audio",
    "btn_previous": "Previous",
    "btn_random": "Random",
    "btn_next": "Next",
    "cmd_index": "List all surahs",
    "cmd_random": "A random verse",
    "cmd_language": "Change UI language",
    "cmd_translation": "Change translation language",
    "cmd_reciter": "Change reciter",
    "cmd_about": "Sources & credits",
    "quran_name": "Qur'an",
}
