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
from dotenv import load_dotenv
load_dotenv()

import asyncio
from io import BytesIO
from time import time
import httpx
import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup
from fastapi import FastAPI, Request, Response
from modules import Quran, make_index, Bot
from lib.utils import File
from config import Environment


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
    """Build the shared, read-mostly application state: corpora, keyboard, inline defaults.

    Built once at process startup and reused for every update.
    """
    interface = ReplyKeyboardMarkup(
        [["Arabic", "Audio", "English", "Tafsir"],
         ["Previous", "Random", "Next"]],
        resize_keyboard=True)

    data = {
        "english": Quran("translation"),
        "tafsir": Quran("tafsir"),
        "index": make_index(),
        "interface": interface,
    }
    data["default_query_results"] = get_default_query_results(data["english"])
    return data


async def handle_update(bot, data: dict, update: telegram.Update) -> None:
    """Process a single Telegram update pushed to the webhook."""
    file = File()

    async def send_quran(surah: int, ayah: int, quran_type: str, chat_id: int, performer: str, reply_markup=None):
        if quran_type in ("english", "tafsir"):
            text = data[quran_type].get_ayah(surah, ayah)
            await bot.send_message(chat_id=chat_id, text=text[:4096],
                            reply_markup=reply_markup)
        elif quran_type == "arabic":
            await bot.send_chat_action(chat_id=chat_id,
                                action=telegram.constants.ChatAction.UPLOAD_PHOTO)
            image = file.get_image_filename(surah, ayah)
            await send_file(bot, image, quran_type, chat_id=chat_id,
                      caption="Quran %d:%d" % (surah, ayah),
                      reply_markup=reply_markup)
        elif quran_type == "audio":
            await bot.send_chat_action(chat_id=chat_id,
                                action=telegram.constants.ChatAction.UPLOAD_VOICE)
            audio = file.get_audio_filename(surah, ayah, performer)
            await send_file(bot, audio, quran_type, chat_id=chat_id,
                      performer="Shaykh Mahmoud Khalil al-Husary",
                      title="Quran %d:%d" % (surah, ayah),
                      reply_markup=reply_markup)
        file.save_user(chat_id, (surah, ayah, quran_type))

    if update.inline_query:
        query_id = update.inline_query.id
        query = update.inline_query.query
        results = []
        cache_time = 66 * (60 ** 2 * 24)
        surah, ayah = parse_ayah(query)
        if surah is not None and Quran.exists(surah, ayah):
            ref = "%d:%d" % (surah, ayah)
            english = data["english"].get_ayah(surah, ayah)
            tafsir = data["tafsir"].get_ayah(surah, ayah)
            results.append(InlineQueryResultArticle(
                ref + "english", title="English",
                description=english[:120],
                input_message_content=InputTextMessageContent(english))
            )
            results.append(InlineQueryResultArticle(
                ref + "tafsir", title="Tafsir",
                description=tafsir[:120],
                input_message_content=InputTextMessageContent(tafsir))
            )
        else:
            results = data["default_query_results"]
        await bot.answer_inline_query(inline_query_id=query_id, cache_time=cache_time, results=results)
        return

    if not update.message or not update.message.text:  # updates without text
        return

    chat_id = update.message.chat.id
    message = update.message.text.lower()
    state = file.get_user(chat_id)
    if state is not None:
        surah, ayah, quran_type = state
    else:
        surah, ayah, quran_type = 1, 1, "english"

    print("%d:%.3f:%s" % (chat_id, time(), message.replace("\n", " ")))

    if chat_id < 0:
        return              # bot should not be in a group

    if message.startswith("/"):
        command = message[1:]
        if command in ("start", "help"):
            text = ("Send me the numbers of a surah and ayah, for example:"
                    " <b>2:255</b>. Then I respond with that ayah from the Holy "
                    "Quran. Type /index to see all Surahs or try /random. "
                    "I'm available in any chat on Telegram, just type: <b>@BismillahBot</b>\n\n"
                    "For audio tracks of complete Surahs, talk to @AudioQuranBot.")
        elif command == "about":
            text = ("The English translation is by Imam Ahmed Raza from "
                    "tanzil.net/trans/. The audio is a recitation by "
                    "Shaykh Mahmoud Khalil al-Husary from everyayah.com. "
                    "The tafsir is Tafsir al-Jalalayn from altafsir.com."
                    "The source code of BismillahBot is available at: "
                    "https://github.com/rahiel/BismillahBot.")
        elif command == "index":
            text = data["index"]
        else:
            text = None  # "Invalid command"

        if text:
            await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
            return

    if message in ("english", "tafsir", "audio", "arabic"):
        await send_quran(surah, ayah, message, chat_id, "Husary_128kbps")
        return
    elif message in ("next", "previous", "random", "/random"):
        if message == "next":
            surah, ayah = Quran.get_next_ayah(surah, ayah)
        elif message == "previous":
            surah, ayah = Quran.get_previous_ayah(surah, ayah)
        elif message in ("random", "/random"):
            surah, ayah = Quran.get_random_ayah()
        await send_quran(surah, ayah, quran_type, chat_id, "Husary_128kbps")
        return

    surah, start, end = parse_ayah_range(message)
    if surah:
        if end > start:  # a range like "53:1-7" -> one combined audio
            if not (Quran.exists(surah, start) and Quran.exists(surah, end)):
                await bot.send_message(chat_id=chat_id, text="Ayah does not exist!")
            elif end - start + 1 > MAX_RANGE_AYAHS:
                await bot.send_message(
                    chat_id=chat_id,
                    text="Range too large, please request at most %d ayahs at a time." % MAX_RANGE_AYAHS)
            else:
                await send_combined_audio(bot, surah, start, end, chat_id, "Husary_128kbps",
                                          reply_markup=data["interface"])
        elif Quran.exists(surah, start):
            await send_quran(surah, start, quran_type, chat_id, "Husary_128kbps", reply_markup=data["interface"])
        else:
            await bot.send_message(chat_id=chat_id, text="Ayah does not exist!")


# ---------------------------------------------------------------------------
# Webhook app
# ---------------------------------------------------------------------------

app = FastAPI()
bot = Bot.get_instance()
data = None  # populated on startup


@app.on_event("startup")
async def on_startup():
    global data
    data = build_data()

    webhook_base = os.getenv("WEBHOOK_URL")
    if webhook_base:
        token = Environment.get_env("token")
        await bot.set_webhook(url=f"{webhook_base.rstrip('/')}/webhook/{token}")
    print("Webhook server has been started")


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()


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

    payload = await request.json()
    update = telegram.Update.de_json(payload, bot)
    # Ack Telegram immediately and do the (possibly slow) work in the background,
    # so downloading/uploading combined audio doesn't hold the webhook response open.
    task = asyncio.create_task(_process_update(update))
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)
    return {"ok": True}
