#!/usr/bin/env python3
"""How the bot looks on WhatsApp: its business profile, conversation starters,
`/` command list, and (once Meta allows it) its username. Also the Telegram
bot's description texts, per language, so both platforms say the same thing.

Everything here is set on Meta's side through the Graph API, not in the bot's
code, so it lives in this re-runnable script rather than at startup. Each part
first prints what is set now and what it would change; nothing changes without
`--apply`.

    python3 scripts/whatsapp_setup.py profile [--apply] [--app-id ID]
    python3 scripts/whatsapp_setup.py automation [--apply]
    python3 scripts/whatsapp_setup.py username [--apply]
    python3 scripts/whatsapp_setup.py status
    python3 scripts/whatsapp_setup.py telegram [--apply]

  profile     picture (assets/whatsapp/avatar.png), About, description, email,
              websites and category. The picture is uploaded through the app's
              resumable upload, so it needs the Meta app id (`--app-id`).
  automation  the four conversation starters shown on an empty chat and the
              command list shown when someone types `/` (bot/whatsapp.py
              routes both), plus the welcome event (`request_welcome`).
  username    claims USERNAME. Meta only grants usernames to accounts with a
              higher messaging limit, so this fails until the business is
              verified and the number is your own, not the test number.
  status      the number's display name, its review status and the username.
  telegram    the Telegram bot's description (shown on an empty chat, under the
              picture from assets/telegram/description.png) and its short
              description (profile page, shares), in English for everyone and in
              Uzbek and Russian for people whose Telegram app is in those
              languages. Through the Bot API; needs only the bot token.

The display name ("Quran Ayah Bot") is not set through this API: it is chosen
when registering your own number in WhatsApp Manager, and Meta reviews it.

Reads the same settings as the bot, from the environment or `.env`. Meta takes
one language for all of its part, for everyone; it is English. Replies to each
user stay in their own language. The Telegram picture and name are set by hand
in BotFather (Edit Description Picture, /setname); the Bot API cannot set them.
"""

import argparse
import json
import os
import sys

import httpx
from dotenv import load_dotenv

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))

from app.routes.privacy import CONTACT_EMAIL, PRIVACY_PATH  # noqa: E402
from bot.whatsapp import STARTERS  # noqa: E402
from channels.whatsapp import DEFAULT_GRAPH_VERSION, GRAPH_URL  # noqa: E402
from config.settings import Settings  # noqa: E402

DISPLAY_NAME = "Quran Ayah Bot"
USERNAME = "quranayahbot"
AVATAR = os.path.join(ROOT, "assets", "whatsapp", "avatar.png")
TELEGRAM_BOT = "https://t.me/QuranAyat_bot"

ABOUT = "📖 The Holy Qur'an on WhatsApp: ayat, translations, recitation and hifz"
DESCRIPTION = (
    "Quran Ayah Bot sends you any ayah of the Holy Qur'an: the Arabic text, a "
    "translation in your language, tafsir and audio by the reciter you choose. "
    "Get a verse of the day, open mushaf pages, and memorize with a daily hifz plan.\n\n"
    "Type menu to start, or send an ayah like 2:255. Reply STOP any time to stop "
    "daily messages. Free, no ads. Also on Telegram: @QuranAyat_bot"
)
VERTICAL = "EDU"

# The `/` list. Each name is also a word bot/whatsapp.py understands typed.
COMMANDS = [
    ("menu", "Everything the bot can do"),
    ("daily", "Verse of the day: turn on or off, pick the time"),
    ("random", "A random ayah with its translation"),
    ("index", "The 114 surahs with their numbers"),
    ("page", "A mushaf page, e.g. /page 255"),
    ("juz", "The start of a juz, e.g. /juz 30"),
    ("memorize", "Start or continue your hifz plan"),
    ("progress", "What you have memorized so far"),
    ("check", "Test yourself on what you memorized"),
    ("streak", "Your daily streak"),
    ("reciter", "Choose whose recitation you hear"),
    ("language", "The language the bot talks to you in"),
    ("translation", "The language of the Qur'an translation"),
    ("app", "Open the web app: reader, mushaf and hifz"),
    ("about", "Sources and how this bot works"),
]

# Telegram's texts by the language code of the reader's Telegram app; "" is the
# default, shown to everyone else. (description, short description)
TELEGRAM_TEXTS = {
    "": (
        "Assalamu alaykum 👋\n\n"
        "Send an ayah like 2:255, a range like 59:22-24, or a surah name, and get the "
        "Arabic text, a translation in your language, tafsir and audio by the reciter "
        "you choose.\n\n"
        "🌅 A verse of the day at a time you pick\n"
        "📄 Mushaf pages and juz\n"
        "🧠 Memorize with a daily hifz plan, recall checks and streaks\n"
        "📱 A Mini App with the reader, mushaf and hifz\n\n"
        "Free, no ads.",
        "📖 The Holy Qur'an on Telegram: ayat, translations, recitation, verse of the day "
        "and hifz.",
    ),
    "uz": (
        "Assalomu alaykum 👋\n\n"
        "Oyatni 2:255 kabi, oraliqni 59:22-24 kabi yoki sura nomini yuboring: arabcha "
        "matn, oʻz tilingizdagi tarjima, tafsir va siz tanlagan qorining qiroatini "
        "olasiz.\n\n"
        "🌅 Siz tanlagan vaqtda kun oyati\n"
        "📄 Mushaf sahifalari va poralar\n"
        "🧠 Kunlik hifz rejasi, takrorlash va ketma-ketlik bilan yodlash\n"
        "📱 Mini ilova: oʻqish, mushaf va hifz\n\n"
        "Bepul, reklamasiz.",
        "📖 Qurʼoni Karim Telegram'da: oyatlar, tarjimalar, qiroat, kun oyati va hifz.",
    ),
    "ru": (
        "Ассаляму алейкум 👋\n\n"
        "Отправьте аят, например 2:255, диапазон 59:22-24 или название суры, и получите "
        "арабский текст, перевод на вашем языке, тафсир и чтение выбранного вами "
        "чтеца.\n\n"
        "🌅 Аят дня в удобное вам время\n"
        "📄 Страницы мусхафа и джузы\n"
        "🧠 Заучивание по ежедневному плану, с проверками и серией дней\n"
        "📱 Мини-приложение: чтение, мусхаф и хифз\n\n"
        "Бесплатно, без рекламы.",
        "📖 Священный Коран в Telegram: аяты, переводы, чтение, аят дня и хифз.",
    ),
}
TELEGRAM_DESCRIPTION_MAX, TELEGRAM_SHORT_MAX = 512, 120

# Meta's limits, checked before anything is sent.
ABOUT_MAX, DESCRIPTION_MAX, PROMPT_MAX, PROMPTS_MAX = 139, 512, 80, 4
COMMAND_MAX, COMMAND_HINT_MAX, COMMANDS_MAX = 32, 256, 30


class Graph:
    def __init__(self, settings: Settings):
        if not (settings.whatsapp_phone_number_id and settings.whatsapp_access_token):
            sys.exit(
                "The WhatsApp phone number id and access token must be set (see .env.example)."
            )
        self.phone = settings.whatsapp_phone_number_id
        self.token = settings.whatsapp_access_token
        self.http = httpx.Client(
            base_url="%s/%s/" % (GRAPH_URL, DEFAULT_GRAPH_VERSION),
            headers={"Authorization": "Bearer " + self.token},
            timeout=60,
        )

    def call(self, method: str, path: str, **kwargs) -> dict:
        response = self.http.request(method, path, **kwargs)
        body = response.json() if response.content else {}
        if response.status_code >= 400:
            error = body.get("error", {})
            sys.exit(
                "Meta refused %s %s: %s (code %s)"
                % (method, path, error.get("message", response.text), error.get("code"))
            )
        return body

    def upload_picture(self, app_id: str, path: str) -> str:
        """Meta's resumable upload: open a session on the app, send the bytes,
        get back the handle the profile takes."""
        with open(path, "rb") as f:
            content = f.read()
        session = self.call(
            "POST",
            "%s/uploads" % app_id,
            params={"file_length": len(content), "file_type": "image/png"},
        )["id"]
        # This one endpoint wants "OAuth", not "Bearer".
        response = self.http.post(
            session,
            content=content,
            headers={"Authorization": "OAuth " + self.token, "file_offset": "0"},
        )
        if response.status_code >= 400:
            sys.exit("Meta refused the picture upload: %s" % response.text)
        return response.json()["h"]


def _show(title: str, current, wanted) -> bool:
    """Print one setting; True when it would change."""
    changes = current != wanted
    print("%s %s" % ("~" if changes else "=", title))
    if changes:
        print("    now:  %s" % json.dumps(current, ensure_ascii=False))
        print("    want: %s" % json.dumps(wanted, ensure_ascii=False))
    return changes


def websites(settings: Settings) -> list:
    base = settings.webhook_base_url
    first = settings.miniapp_url or (base + PRIVACY_PATH if base else None)
    return [site for site in (first, TELEGRAM_BOT) if site]


def profile(graph: Graph, settings: Settings, apply: bool, app_id) -> None:
    wanted = {
        "about": ABOUT,
        "description": DESCRIPTION,
        "email": CONTACT_EMAIL,
        "websites": websites(settings),
        "vertical": VERTICAL,
    }
    assert len(ABOUT) <= ABOUT_MAX and len(DESCRIPTION) <= DESCRIPTION_MAX
    fields = ",".join(list(wanted) + ["profile_picture_url"])
    (current,) = graph.call(
        "GET", "%s/whatsapp_business_profile" % graph.phone, params={"fields": fields}
    )["data"]
    changed = {
        name: value for name, value in wanted.items() if _show(name, current.get(name), value)
    }
    has_picture = bool(current.get("profile_picture_url"))
    print("%s picture (%s)" % ("=" if has_picture else "~", "set" if has_picture else "none"))
    if not apply:
        print(
            "\nDry run. Re-run with --apply to change this%s."
            % ("" if app_id else " (add --app-id to upload the picture)")
        )
        return
    body = {"messaging_product": "whatsapp", **changed}
    if app_id:
        body["profile_picture_handle"] = graph.upload_picture(app_id, AVATAR)
    if len(body) == 1:
        print("\nNothing to change.")
        return
    graph.call("POST", "%s/whatsapp_business_profile" % graph.phone, json=body)
    print("\nProfile updated.")


def automation(graph: Graph, apply: bool) -> None:
    prompts = list(STARTERS)
    commands = [{"command_name": n, "command_description": d} for n, d in COMMANDS]
    assert len(prompts) <= PROMPTS_MAX and all(len(p) <= PROMPT_MAX for p in prompts)
    assert len(commands) <= COMMANDS_MAX
    assert all(len(n) <= COMMAND_MAX and len(d) <= COMMAND_HINT_MAX for n, d in COMMANDS)
    current = graph.call("GET", graph.phone, params={"fields": "conversational_automation"})
    current = current.get("conversational_automation", {})
    _show("prompts", current.get("prompts"), prompts)
    _show("commands", current.get("commands"), commands)
    _show("welcome message", current.get("enable_welcome_message"), True)
    if not apply:
        print("\nDry run. Re-run with --apply to change this.")
        return
    graph.call(
        "POST",
        "%s/conversational_automation" % graph.phone,
        json={"enable_welcome_message": True, "prompts": prompts, "commands": commands},
    )
    print("\nStarters, commands and the welcome event are set.")


def username(graph: Graph, apply: bool) -> None:
    current = graph.call("GET", "%s/username" % graph.phone)
    print("now: %s" % json.dumps(current, ensure_ascii=False))
    if not apply:
        print("Dry run. Re-run with --apply to claim @%s." % USERNAME)
        return
    result = graph.call("POST", "%s/username" % graph.phone, json={"username": USERNAME})
    print("@%s: %s" % (USERNAME, result.get("status", result)))


def status(graph: Graph) -> None:
    fields = "display_phone_number,verified_name,name_status,new_name_status,quality_rating"
    print(json.dumps(graph.call("GET", graph.phone, params={"fields": fields}), indent=2))
    print(
        "Wanted display name: %s (set in WhatsApp Manager when registering your number)"
        % DISPLAY_NAME
    )


def _bot_api(token: str, method: str, **params) -> dict:
    """One Bot API call. The token is part of the URL, so errors never print it."""
    response = httpx.post("https://api.telegram.org/bot%s/%s" % (token, method), json=params)
    body = response.json()
    if not body.get("ok"):
        sys.exit(
            "Telegram refused %s: %s" % (method, body.get("description", response.status_code))
        )
    return body["result"]


def telegram(settings: Settings, apply: bool) -> None:
    if not settings.token:
        sys.exit("The Telegram bot token must be set (see .env.example).")
    for lang, (description, short) in TELEGRAM_TEXTS.items():
        assert len(description) <= TELEGRAM_DESCRIPTION_MAX, lang
        assert len(short) <= TELEGRAM_SHORT_MAX, lang
        name = lang or "default"
        now = _bot_api(settings.token, "getMyDescription", language_code=lang)
        now_short = _bot_api(settings.token, "getMyShortDescription", language_code=lang)
        changes = _show("%s description" % name, now.get("description") or None, description)
        changes_short = _show(
            "%s short description" % name, now_short.get("short_description") or None, short
        )
        if apply and changes:
            _bot_api(
                settings.token, "setMyDescription", description=description, language_code=lang
            )
        if apply and changes_short:
            _bot_api(
                settings.token, "setMyShortDescription", short_description=short, language_code=lang
            )
    print(
        "\nTelegram texts updated." if apply else "\nDry run. Re-run with --apply to change this."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("part", choices=("profile", "automation", "username", "status", "telegram"))
    parser.add_argument("--apply", action="store_true", help="change it (default: dry run)")
    parser.add_argument("--app-id", help="the Meta app id, to upload the profile picture")
    args = parser.parse_args()
    load_dotenv(os.path.join(ROOT, ".env"))
    settings = Settings.from_env()
    if args.part == "telegram":
        telegram(settings, args.apply)
        return
    graph = Graph(settings)
    if args.part == "profile":
        profile(graph, settings, args.apply, args.app_id)
    elif args.part == "automation":
        automation(graph, args.apply)
    elif args.part == "username":
        username(graph, args.apply)
    else:
        status(graph)


if __name__ == "__main__":
    main()
