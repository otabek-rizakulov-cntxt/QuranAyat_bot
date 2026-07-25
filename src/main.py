# BismillahBot -- Explore the Holy Qur'an on Telegram
# Copyright (C) 1436-1438 AH  Rahiel Kasim
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Webhook entrypoint: Telegram pushes updates to us; we never poll.

Run with: uvicorn main:app --host 0.0.0.0 --port 8000

Required env vars (see .env.example):
  TOKEN                  Telegram bot token
  REDIS_HOST_URL         Redis connection URL (user state + media file-id cache)
  AUDIO_BASE_URL         base URL for recitation mp3s
  PHOTO_BASE_URL         base URL/path for Arabic ayah images
  WEBHOOK_URL            public HTTPS base URL Telegram should POST updates to;
                         the webhook is registered as WEBHOOK_URL + "/webhook/" + TOKEN
"""
import os
import re
"""Webhook entrypoint: Telegram pushes updates to us; we never poll.

Run with: uvicorn main:app --host 0.0.0.0 --port 8000

Required env vars (see .env.example):
  TOKEN                  Telegram bot token
  REDIS_HOST_URL         Redis connection URL (user state + media file-id cache)
  AUDIO_BASE_URL         base URL for recitation mp3s
  PHOTO_BASE_URL         base URL/path for Arabic ayah images
  WEBHOOK_URL            public HTTPS base URL Telegram should POST updates to;
                         the webhook is registered as WEBHOOK_URL + "/webhook/" + TOKEN
"""
import os
import re
from dotenv import load_dotenv
load_dotenv()

import asyncio
from io import BytesIO
from time import time
import httpx
import telegram
from telegram import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    ReplyKeyboardMarkup,
)
from fastapi import FastAPI, Request, Response
from modules import Quran, make_index, Bot, TranslationRegistry
from lib.utils import File
from config import Environment
from locales import (
    LANGUAGES, DEFAULT_LANG,
    t, keyboard_rows, button_action, normalize_lang, get_language,
)


# ---------------------------------------------------------------------------
# Bot logic
# ---------------------------------------------------------------------------

async def send_file(bot, filename, quran_type, **kwargs):
    """Send a media file, preferring Telegram's cached file_id over a fresh upload.

    On a cache miss (or if the cached file_id is rejected) we upload from the
    filename/URL and persist the returned file_id in Redis for next time.
    """
    file = File()

    async def send(source):
        """`source` is either a cached file_id string or a filename/URL to upload."""
        if quran_type == "arabic":
            result = await bot.send_photo(photo=source, **kwargs)
            return result.photo[-1].file_id
        elif quran_type == "audio":
            result = await bot.send_audio(audio=source, **kwargs)
            return result.audio.file_id
        return None

    cached_id = file.get_file(filename)
    if cached_id is not None:
        try:
            return await send(cached_id)
        except telegram.error.TelegramError:
            # cached file_id was rejected (e.g. expired); fall back to a fresh upload
            pass

    new_id = await send(filename)
    file.save_file(filename, new_id)
    return new_id


# Cap how many ayahs a single combined-audio request may stitch together, to bound
# download time and stay well under Telegram's 50 MB bot upload limit.
MAX_RANGE_AYAHS = 50


# Cap simultaneous CDN connections: fast, but polite enough to avoid rate-limiting/blocks.
_DOWNLOAD_CONCURRENCY = 4


async def _download_combined_audio(surah: int, start: int, end: int, performer: str) -> BytesIO:
    """Fetch each ayah's mp3 from the CDN (with bounded concurrency) and concatenate."""
    file = File()
    urls = [file.get_audio_filename(surah, ayah, performer) for ayah in range(start, end + 1)]
    semaphore = asyncio.Semaphore(_DOWNLOAD_CONCURRENCY)

    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        async def fetch(url):
            async with semaphore:
                response = await client.get(url)
                response.raise_for_status()
                return response.content

        chunks = await asyncio.gather(*(fetch(url) for url in urls))

    buf = BytesIO()
    for chunk in chunks:  # gather preserves order, so ayahs stay in sequence
        buf.write(chunk)
    buf.seek(0)
    buf.name = "quran_%d_%d-%d.mp3" % (surah, start, end)
    return buf


async def send_combined_audio(bot, surah: int, start: int, end: int, chat_id: int,
                              performer: str, reply_markup=None) -> None:
    """Send a range of ayahs as a single combined audio file, cached by Telegram file_id."""
    file = File()
    cache_key = "combined:%d:%d-%d:%s" % (surah, start, end, performer)
    title = "Quran %d:%d-%d" % (surah, start, end)
    kwargs = dict(chat_id=chat_id, title=title,
                  performer="Shaykh Mahmoud Khalil al-Husary",
                  reply_markup=reply_markup)

    cached_id = file.get_file(cache_key)
    if cached_id is not None:
        try:
            await bot.send_audio(audio=cached_id, **kwargs)
            file.save_user(chat_id, (surah, end, "audio"))
            return
        except telegram.error.TelegramError:
            pass  # cached file_id rejected; rebuild below

    await bot.send_chat_action(chat_id=chat_id,
                        action=telegram.constants.ChatAction.UPLOAD_VOICE)
    audio = await _download_combined_audio(surah, start, end, performer)
    result = await bot.send_audio(audio=audio, **kwargs)
    file.save_file(cache_key, result.audio.file_id)
    file.save_user(chat_id, (surah, end, "audio"))


def get_default_query_results(quran: Quran):
    results = []
    ayat = [
        (13, 28), (33, 56), (2, 62), (10, 31), (17, 36), (5, 32), (39, 9), (17, 44), (28, 88), (17, 84), (33, 6),
        (7, 57), (3, 7), (2, 255), (63, 9), (57, 20), (49, 12), (16, 125), (24, 35), (73, 8), (4, 103)
    ]
    for s, a in ayat:
        ayah = "%d:%d" % (s, a)
        english = quran.get_ayah(s, a)
        results.append(InlineQueryResultArticle(
            ayah + "def", title=ayah,
            description=english[:120],
            input_message_content=InputTextMessageContent(english))
        )
    return results


def parse_ayah(message: str):
    match = re.match(r"/?(\d+)[ :\-;.,]*(\d*)", message)
    if match is not None:
        surah = int(match.group(1))
        ayah = int(match.group(2)) if match.group(2) else 1
        return surah, ayah
    else:
        return None, None


def parse_ayah_range(message: str):
    """Parse a reference into (surah, start, end).

    A range like "53:1-7" -> (53, 1, 7). A single ayah like "2:255" -> (2, 255, 255).
    Returns (None, None, None) when nothing parses.
    """
    # surah <sep> start <dash> end  (three numbers, second separator is a dash)
    match = re.match(r"/?(\d+)[ :.;,]+(\d+)\s*[-–]\s*(\d+)", message)
    if match is not None:
        surah, start, end = (int(match.group(i)) for i in (1, 2, 3))
        if end < start:
            start, end = end, start
        return surah, start, end
    surah, ayah = parse_ayah(message)
    if surah is None:
        return None, None, None
    return surah, ayah, ayah


def build_data() -> dict:
    """Build the shared, read-mostly application state: corpora and inline defaults.

    Built once at process startup and reused for every update. Only the default
    language's translation is preloaded; other languages are parsed lazily by the
    TranslationRegistry on first use. The reply keyboard is now built per-update
    (its labels are localized), so it is no longer part of this shared state.
    """
    TranslationRegistry.preload(DEFAULT_LANG)  # English ready immediately
    data = {
        "tafsir": Quran.from_tafsir(),
        "index": make_index(),
    }
    data["default_query_results"] = get_default_query_results(TranslationRegistry.get(DEFAULT_LANG))
    return data


async def get_translation(lang: str) -> Quran:
    """Return the Qur'an translation for `lang`, parsing off the event loop on first use."""
    if TranslationRegistry.is_cached(lang):
        return TranslationRegistry.get(lang)
    return await asyncio.to_thread(TranslationRegistry.get, lang)


def _reference(surah: int, ayah: int, lang: str) -> str:
    """Human-readable ayah reference ("Qur'an 2:255") in the user's language."""
    return "%s %d:%d" % (t("quran_name", lang), surah, ayah)


def language_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard of every bundled language (native names), two per row."""
    available = TranslationRegistry.available()
    rows, row = [], []
    for lang in LANGUAGES:
        if lang.code not in available:
            continue
        row.append(InlineKeyboardButton(lang.native, callback_data="setlang:" + lang.code))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


def _resolve_lang(file: File, chat_id: int, tg_user) -> str:
    """Return the user's saved language, detecting from Telegram on first contact.

    On first contact we take the user's Telegram `language_code`, map it to a
    supported language (else English), and persist it so the choice is stable.
    """
    lang = file.get_lang(chat_id)
    if lang is None:
        lang = normalize_lang(getattr(tg_user, "language_code", None))
        file.save_lang(chat_id, lang)
    return lang


async def handle_update(bot, data: dict, update: telegram.Update) -> None:
    """Process a single Telegram update pushed to the webhook."""
    file = File()

    async def send_quran(surah: int, ayah: int, quran_type: str, chat_id: int,
                         performer: str, lang: str, reply_markup=None):
        if quran_type == "translation":
            quran = await get_translation(lang)
            text = quran.get_ayah(surah, ayah)
            await bot.send_message(chat_id=chat_id, text=text[:4096],
                            reply_markup=reply_markup)
        elif quran_type == "tafsir":
            text = data["tafsir"].get_ayah(surah, ayah)
            if lang != DEFAULT_LANG:               # tafsir is English-only; note it
                text = text + t("tafsir_en_note", lang)
            await bot.send_message(chat_id=chat_id, text=text[:4096],
                            reply_markup=reply_markup)
        elif quran_type == "arabic":
            await bot.send_chat_action(chat_id=chat_id,
                                action=telegram.constants.ChatAction.UPLOAD_PHOTO)
            image = file.get_image_filename(surah, ayah)
            await send_file(bot, image, quran_type, chat_id=chat_id,
                      caption=_reference(surah, ayah, lang),
                      reply_markup=reply_markup)
        elif quran_type == "audio":
            await bot.send_chat_action(chat_id=chat_id,
                                action=telegram.constants.ChatAction.UPLOAD_VOICE)
            audio = file.get_audio_filename(surah, ayah, performer)
            await send_file(bot, audio, quran_type, chat_id=chat_id,
                      performer="Shaykh Mahmoud Khalil al-Husary",
                      title=_reference(surah, ayah, lang),
                      reply_markup=reply_markup)
        file.save_user(chat_id, (surah, ayah, quran_type))

    if update.inline_query:
        query_id = update.inline_query.id
        query = update.inline_query.query
        user = update.inline_query.from_user
        # inline users have no chat with us; key the preference by their user id
        lang = file.get_lang(user.id) if user else None
        if lang is None:
            lang = normalize_lang(getattr(user, "language_code", None))
        results = []
        cache_time = 66 * (60 ** 2 * 24)
        surah, ayah = parse_ayah(query)
        if surah is not None and Quran.exists(surah, ayah):
            ref = "%d:%d" % (surah, ayah)
            quran = await get_translation(lang)
            translation = quran.get_ayah(surah, ayah)
            tafsir = data["tafsir"].get_ayah(surah, ayah)
            results.append(InlineQueryResultArticle(
                ref + "translation", title=t("btn_translation", lang),
                description=translation[:120],
                input_message_content=InputTextMessageContent(translation))
            )
            results.append(InlineQueryResultArticle(
                ref + "tafsir", title=t("btn_tafsir", lang),
                description=tafsir[:120],
                input_message_content=InputTextMessageContent(tafsir))
            )
        else:
            results = data["default_query_results"]
        await bot.answer_inline_query(inline_query_id=query_id, cache_time=cache_time, results=results)
        return

    if update.callback_query:  # language selection from the /language keyboard
        cq = update.callback_query
        cb_data = cq.data or ""
        chat_id = cq.message.chat.id if cq.message else cq.from_user.id
        await bot.answer_callback_query(cq.id)
        if cb_data.startswith("setlang:"):
            code = normalize_lang(cb_data.split(":", 1)[1])
            file.save_lang(chat_id, code)
            interface = ReplyKeyboardMarkup(keyboard_rows(code), resize_keyboard=True)
            confirm = t("language_set", code).format(lang=get_language(code).native)
            await bot.send_message(chat_id=chat_id, text=confirm, reply_markup=interface)
        return

    if not update.message or not update.message.text:  # updates without text
        return

    chat_id = update.message.chat.id
    message = update.message.text.lower()
    lang = _resolve_lang(file, chat_id, update.message.from_user)

    state = file.get_user(chat_id)
    if state is not None:
        surah, ayah, quran_type = state
        if quran_type == "english":   # legacy stored value -> canonical name
            quran_type = "translation"
    else:
        surah, ayah, quran_type = 1, 1, "translation"

    print("%d:%.3f:%s" % (chat_id, time(), message.replace("\n", " ")))

    if chat_id < 0:
        return              # bot should not be in a group

    interface = ReplyKeyboardMarkup(keyboard_rows(lang), resize_keyboard=True)

    if message.startswith("/"):
        command = message[1:].split("@", 1)[0]   # tolerate /help@BotName
        if command in ("start", "help"):
            await bot.send_message(chat_id=chat_id, text=t("welcome", lang),
                            parse_mode="HTML", reply_markup=interface)
            return
        elif command == "about":
            await bot.send_message(chat_id=chat_id, text=t("about", lang), parse_mode="HTML")
            return
        elif command == "index":
            await bot.send_message(chat_id=chat_id, text=data["index"], parse_mode="HTML")
            return
        elif command == "language":
            await bot.send_message(chat_id=chat_id, text=t("choose_language", lang),
                            reply_markup=language_keyboard())
            return
        elif command == "random":
            surah, ayah = Quran.get_random_ayah()
            await send_quran(surah, ayah, quran_type, chat_id, "Husary_128kbps", lang,
                             reply_markup=interface)
            return
        # unknown command: fall through (ignored, as before)

    action = button_action(message, lang)
    if action in ("arabic", "audio", "translation", "tafsir"):
        await send_quran(surah, ayah, action, chat_id, "Husary_128kbps", lang)
        return
    elif action in ("next", "previous", "random"):
        if action == "next":
            surah, ayah = Quran.get_next_ayah(surah, ayah)
        elif action == "previous":
            surah, ayah = Quran.get_previous_ayah(surah, ayah)
        else:
            surah, ayah = Quran.get_random_ayah()
        await send_quran(surah, ayah, quran_type, chat_id, "Husary_128kbps", lang)
        return

    surah, start, end = parse_ayah_range(message)
    if surah:
        if end > start:  # a range like "53:1-7" -> one combined audio
            if not (Quran.exists(surah, start) and Quran.exists(surah, end)):
                await bot.send_message(chat_id=chat_id, text=t("ayah_not_found", lang))
            elif end - start + 1 > MAX_RANGE_AYAHS:
                await bot.send_message(
                    chat_id=chat_id,
                    text=t("range_too_large", lang).format(n=MAX_RANGE_AYAHS))
            else:
                await send_combined_audio(bot, surah, start, end, chat_id, "Husary_128kbps",
                                          reply_markup=interface)
        elif Quran.exists(surah, start):
            await send_quran(surah, start, quran_type, chat_id, "Husary_128kbps", lang,
                             reply_markup=interface)
        else:
            await bot.send_message(chat_id=chat_id, text=t("ayah_not_found", lang))


# ---------------------------------------------------------------------------
# Webhook app
# ---------------------------------------------------------------------------

app = FastAPI()
bot = None  # created during background init (guarded) so a bad/missing TOKEN can't crash import
data = None  # populated by background init after corpora finish parsing


def _webhook_base_url() -> str | None:
    """Public HTTPS base URL for the webhook.

    Prefer an explicit WEBHOOK_URL; otherwise fall back to Railway's auto-injected
    RAILWAY_PUBLIC_DOMAIN (host only, so we prepend https://).
    """
    explicit = os.getenv("WEBHOOK_URL")
    if explicit:
        return explicit.rstrip("/")
    railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    if railway_domain:
        return "https://" + railway_domain.rstrip("/")
    return None


# Telegram's per-language command menu only accepts two-letter ISO-639-1 codes,
# so script-qualified and three-letter codes ("uz-Cyrl", "ber") can't be
# registered — those users see the English default menu while the rest of their
# UI is still localized.
_COMMAND_MENU_LANGS = tuple(lang.code for lang in LANGUAGES
                            if len(lang.code) == 2 and lang.code != DEFAULT_LANG)


def _commands_for(lang: str) -> list:
    return [
        BotCommand("index", t("cmd_index", lang)),
        BotCommand("random", t("cmd_random", lang)),
        BotCommand("language", t("cmd_language", lang)),
        BotCommand("about", t("cmd_about", lang)),
    ]


async def _set_bot_commands(bot) -> None:
    """Register the slash-command menu: English default + localized per language.

    Each language is registered independently: Telegram rejects language codes it
    doesn't recognise, and one rejection must not cost the other 45 their menu.
    """
    try:
        await bot.set_my_commands(_commands_for(DEFAULT_LANG))
    except Exception as e:
        print("INIT ERROR (set_my_commands, default):", type(e).__name__, e)
        return                      # the API is unhappy; skip the per-language pass
    registered, rejected = 1, []
    for code in _COMMAND_MENU_LANGS:
        try:
            await bot.set_my_commands(_commands_for(code), language_code=code)
            registered += 1
        except Exception as e:
            rejected.append("%s (%s)" % (code, type(e).__name__))
    print("Command menu registered for %d languages" % registered)
    if rejected:
        print("Command menu not accepted for:", ", ".join(rejected))


async def _initialize():
    """Heavy init (bot, corpora parsing, webhook registration) done OFF the startup path.

    Parsing the Quran translation + tafsir is CPU-bound and slow on small free instances;
    if it ran inside the startup event, uvicorn wouldn't accept connections until it finished
    and the platform's health check would fail the deploy. So we return from startup immediately
    and do this in the background — the server listens right away and answers `/`.
    """
    global data, bot

    try:
        bot = Bot.get_instance()
    except Exception as e:
        print("INIT ERROR (bot — check TOKEN):", type(e).__name__, e)

    try:
        # run the blocking parse in a worker thread so the event loop stays responsive
        data = await asyncio.to_thread(build_data)
        print("Corpora loaded; bot is ready")
    except Exception as e:
        print("INIT ERROR (build_data — check corpus files):", type(e).__name__, e)

    webhook_base = _webhook_base_url()
    if bot and webhook_base:
        try:
            token = Environment.get_env("token")
            await bot.set_webhook(url=f"{webhook_base}/webhook/{token}")
            print("Webhook registered at", webhook_base)
        except Exception as e:
            print("INIT ERROR (set_webhook):", type(e).__name__, e)
    else:
        print("Webhook NOT registered (bot=%s, base=%s)" % (bool(bot), webhook_base))

    if bot:
        await _set_bot_commands(bot)


@app.on_event("startup")
async def on_startup():
    # Kick off heavy init in the background and return immediately so the HTTP server
    # starts listening and passes health checks without waiting on corpora parsing.
    task = asyncio.create_task(_initialize())
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)
    print("Startup event returned — HTTP server is listening")


@app.on_event("shutdown")
async def on_shutdown():
    if bot is not None:
        try:
            await bot.delete_webhook()
        except Exception as e:
            print("Shutdown: delete_webhook failed:", type(e).__name__, e)


@app.get("/")
async def health():
    return {"status": "ok"}


# Keep strong references to in-flight background tasks so they aren't garbage-collected.
_background_tasks: set = set()


async def _process_update(update: telegram.Update) -> None:
    try:
        await handle_update(bot, data, update)
    except telegram.error.Forbidden:
        pass  # user has blocked or removed the bot; nothing to do
    except Exception as e:
        print("Error handling update:", type(e).__name__, e)


@app.post("/webhook/{token}")
async def telegram_webhook(token: str, request: Request):
    if token != Environment.get_env("token"):
        return Response(status_code=404)
    if bot is None or data is None:
        # still initializing (corpora parsing) — ack so Telegram doesn't retry-flood
        print("Webhook hit before init finished; acking without processing")
        return {"ok": True}

    payload = await request.json()
    update = telegram.Update.de_json(payload, bot)
    # Ack Telegram immediately and do the (possibly slow) work in the background,
    # so downloading/uploading combined audio doesn't hold the webhook response open.
    task = asyncio.create_task(_process_update(update))
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)
    return {"ok": True}
