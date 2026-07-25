# English — the canonical UI strings. Every other locale falls back to these
# per-key, so this table must define every key the bot uses.

strings = {
    "welcome": (
        "Send me a surah and ayah number, for example <b>2:255</b>, and I'll "
        "reply with that verse of the Holy Qur'an.\n\n"
        "You can also send a range like <b>59:22-24</b> for a combined audio recitation.\n\n"
        "Commands:\n"
        "/index — list all surahs\n"
        "/random — a random verse\n"
        "/language — change language\n"
        "/about — sources & credits\n\n"
        "You can use me inline in any chat: type <b>@QuranAyat_bot</b> followed by a reference."
    ),
    "about": (
        "This bot lets you explore the Holy Qur'an on Telegram in many languages.\n\n"
        "Translations are sourced from tanzil.net (see ATTRIBUTIONS.md for each "
        "translation's edition and translator). The audio is a recitation by "
        "Shaykh Mahmoud Khalil al-Husary (everyayah.com). The tafsir is "
        "Tafsir al-Jalalayn (altafsir.com), available in English.\n\n"
        "Change language any time with /language.\n"
        "Source code: https://github.com/rahiel/BismillahBot"
    ),
    "ayah_not_found": "Ayah does not exist!",
    "range_too_large": "Range too large, please request at most {n} ayahs at a time.",
    "choose_language": "Choose your language:",
    "language_set": "Language set to {lang}.",
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
    "cmd_language": "Change language",
    "cmd_about": "Sources & credits",
}
