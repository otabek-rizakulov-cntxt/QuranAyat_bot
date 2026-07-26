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
  REDIS_HOST_URL         Redis connection URL (nav state + media file-id cache)
  DATABASE_URL           Postgres connection URL (durable per-user settings)
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
import html
from io import BytesIO
from time import time
from urllib.parse import urlencode
import httpx
import telegram
from telegram import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultAudio,
    InlineQueryResultCachedAudio,
    InlineQueryResultCachedPhoto,
    InlineQueryResultPhoto,
    InputTextMessageContent,
    ReplyKeyboardRemove,
)
from fastapi import FastAPI, Request, Response
from modules import Quran, make_index, Bot, TranslationRegistry
from lib.utils import File
from lib.user_settings import UserSettings
from config import Environment
from config.postgres import get_pool, close_pool
from locales import (
    LANGUAGES, DEFAULT_LANG, BOT_COMMANDS,
    t, button_action, normalize_lang, get_language, welcome_text,
)


# ---------------------------------------------------------------------------
# Bot logic
# ---------------------------------------------------------------------------

def _webhook_base_url() -> str | None:
    """Public HTTPS base URL this app is reachable at.

    Telegram POSTs updates here, and it is also where Telegram fetches the
    stitched range recitations from (see RANGE_AUDIO_PATH), so it is needed by
    the bot logic and not only at startup.

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


def _combined_audio_key(surah: int, start: int, end: int, performer: str) -> str:
    """Telegram file_id cache key for a stitched range, shared by the in-chat send
    that produces it and the inline result that replays it."""
    return "combined:%d:%d-%d:%s" % (surah, start, end, performer)


async def send_combined_audio(bot, surah: int, start: int, end: int, chat_id: int,
                              performer: str, reply_markup=None) -> None:
    """Send a range of ayahs as a single combined audio file, cached by Telegram file_id."""
    file = File()
    cache_key = _combined_audio_key(surah, start, end, performer)
    title = "Quran %d:%d-%d" % (surah, start, end)
    kwargs = dict(chat_id=chat_id, title=title,
                  performer=File.get_performer_name(performer),
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


# Route (on this very app) that stitches a range of recitations on demand. An
# inline audio result can only carry a file_id or a URL Telegram fetches itself —
# never an upload — so a range nobody has sent in a chat yet needs a public place
# to be fetched from, and this is it.
RANGE_AUDIO_PATH = "/media/range.mp3"


def _range_audio_url(surah: int, start: int, end: int, performer: str) -> str | None:
    """Public URL of the stitched recitation of `surah:start-end`, or None when we
    have no public base URL to serve it from (local dev without WEBHOOK_URL)."""
    base = _webhook_base_url()
    if not base or not base.startswith("https://"):
        return None
    query = urlencode({"surah": surah, "start": start, "end": end, "reciter": performer})
    return base + RANGE_AUDIO_PATH + "?" + query


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


def _reference(surah: int, ayah: int, ui_lang: str, end: int | None = None) -> str:
    """Human-readable reference in the user's UI language: "Qur'an 2:255", or
    "Qur'an 59:22-24" when `end` names a later ayah."""
    name = t("quran_name", ui_lang)
    if end is not None and end > ayah:
        return "%s %d:%d-%d" % (name, surah, ayah, end)
    return "%s %d:%d" % (name, surah, ayah)


def _ref_key(surah: int, start: int, end: int) -> str:
    """Compact ASCII form of a reference, used to build inline result ids."""
    if end > start:
        return "%d:%d-%d" % (surah, start, end)
    return "%d:%d" % (surah, start)


# Inline answers built from the caller's own settings can't use the long shared
# cache; this only has to outlive the burst of queries Telegram fires as the user
# types, and stay short enough that changing a setting is felt straight away.
INLINE_PERSONAL_CACHE_TIME = 60


def _inline_audio_result(surah: int, start: int, end: int, reciter: str,
                         ui_lang: str, file: File):
    """The recitation of an ayah — or of a whole range, stitched into one file —
    as a shareable inline result, or None if it can't be built.

    Telegram only ever takes a file_id or a URL it fetches itself here, never an
    upload. A single ayah already has a public URL on the CDN. A range does not,
    so it is served either from the file_id an in-chat send of the same range
    left in the cache, or from our own RANGE_AUDIO_PATH.
    """
    try:
        first_url = file.get_audio_filename(surah, start, reciter)
    except ValueError:
        # A saved reciter that has since left the catalog. The rest of the
        # answer is still useful, so drop the audio rather than failing.
        return None
    if not first_url.startswith(("http://", "https://")):
        # AUDIO_BASE_URL unset or pointing at a local path: neither Telegram nor
        # our own stitching route can reach it, so there is nothing to offer.
        return None

    title = _reference(surah, start, ui_lang, end)
    if end > start:
        if end - start + 1 > MAX_RANGE_AYAHS:
            return None                 # same bound the in-chat range send enforces
        # Bounded by 64 bytes — 4 + 11 + the longest subfolder in the catalog.
        result_id = "aur:%s:%s" % (_ref_key(surah, start, end), reciter)
        cached_id = file.get_file(_combined_audio_key(surah, start, end, reciter))
        if cached_id is not None:
            # Someone has already asked for this range in a chat: replay that
            # upload instead of making Telegram fetch and stitch it again.
            return InlineQueryResultCachedAudio(result_id, audio_file_id=cached_id,
                                                caption=title)
        audio_url = _range_audio_url(surah, start, end, reciter)
        if audio_url is None:
            return None                 # no public base URL to stitch it from
    else:
        # Keyed by reciter as well as ayah: the same query answered before and
        # after a reciter change must not collide in Telegram's result cache.
        result_id = "au:%s:%s" % (_ref_key(surah, start, end), reciter)
        audio_url = first_url
    return InlineQueryResultAudio(result_id, audio_url=audio_url, title=title,
                                  performer=File.get_performer_name(reciter))


# A range's Arabic images come back one result per ayah; cap them so a long range
# can neither pass Telegram's 50-results-per-answer limit nor bury the translation,
# tafsir and recitation under a wall of thumbnails.
INLINE_MAX_PHOTOS = 10


def _inline_photo_results(surah: int, start: int, end: int, ui_lang: str, file: File) -> list:
    """The rendered Arabic image of each ayah in the reference, as shareable inline
    photo results.

    Preferring the file_id an in-chat send left in the cache is not just a saved
    round-trip here: the Bot API documents an inline photo *URL* as having to be
    JPEG, and our rendered ayahs are PNG, so replaying a file Telegram already
    holds is also the more dependable of the two. The URL is the fallback for an
    ayah nobody has viewed yet, and needs PHOTO_BASE_URL to be a public URL; when
    it points at a local directory, only already-cached ayahs can be offered.
    """
    if not file.get_env("quranic_images_file_path"):
        return []                       # no images configured at all
    results = []
    for ayah in range(start, min(end, start + INLINE_MAX_PHOTOS - 1) + 1):
        result_id = "ph:%d:%d" % (surah, ayah)
        ref = _reference(surah, ayah, ui_lang)
        common = dict(title=t("btn_arabic", ui_lang), description=ref, caption=ref)
        # the same key `send_quran`'s arabic branch caches under
        source = file.get_image_filename(surah, ayah)
        cached_id = file.get_file(source)
        if cached_id is not None:
            results.append(InlineQueryResultCachedPhoto(
                result_id, photo_file_id=cached_id, **common))
        elif source.startswith(("http://", "https://")):
            results.append(InlineQueryResultPhoto(
                result_id, photo_url=source, thumbnail_url=source, **common))
    return results


def language_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard of every bundled language (native names), two per row."""
    available = TranslationRegistry.available()
    rows, row = [], []
    for lang in LANGUAGES:
        if lang.code not in available:
            continue
        label = (lang.flag + " " + lang.native) if lang.flag else lang.native
        row.append(InlineKeyboardButton(label, callback_data="setlang:" + lang.code))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


def translation_language_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for picking the Qur'an *translation* language, independently
    of the UI language. Same shape as language_keyboard(), different callback."""
    available = TranslationRegistry.available()
    rows, row = [], []
    for lang in LANGUAGES:
        if lang.code not in available:
            continue
        label = (lang.flag + " " + lang.native) if lang.flag else lang.native
        row.append(InlineKeyboardButton(label, callback_data="settranslang:" + lang.code))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


def _nav_labels(ui_lang: str) -> tuple[str, str]:
    """(previous, next) button labels. The arrows point in reading order, so they
    flip for right-to-left scripts."""
    prev, nxt = t("btn_previous", ui_lang), t("btn_next", ui_lang)
    if get_language(ui_lang).rtl:
        return prev + " ›", "‹ " + nxt
    return "‹ " + prev, nxt + " ›"


# A curated shortlist of well-known reciters (subfolder keys into performers.json).
# These lead the catalog, so the first page of the picker is the ten names most
# people are looking for and the pager walks through everything else.
_RECITER_SHORTLIST = (
    "Husary_128kbps",
    "Alafasy_128kbps",
    "Abdurrahmaan_As-Sudais_192kbps",
    "Abdul_Basit_Murattal_192kbps",
    "Minshawy_Murattal_128kbps",
    "Saood_ash-Shuraym_128kbps",
    "MaherAlMuaiqly128kbps",
    "Yasser_Ad-Dussary_128kbps",
    "Hudhaify_128kbps",
    "Ghamadi_40kbps",
)


# How many reciters one page of the picker shows. Equal to the shortlist length, so
# page 1 is exactly the shortlist.
RECITER_PAGE_SIZE = 10


def reciter_catalog() -> list:
    """Every reciter in src/common/performers.json, shortlist first then the rest in
    catalog order — the order the picker pages through."""
    performers = File._load_performers()
    by_subfolder = {p["subfolder"]: p for p in performers}
    # a shortlist entry the catalog no longer has is skipped, not fatal
    ordered = [by_subfolder[s] for s in _RECITER_SHORTLIST if s in by_subfolder]
    shortlisted = set(_RECITER_SHORTLIST)
    ordered.extend(p for p in performers if p["subfolder"] not in shortlisted)
    return ordered


def reciter_label(performer: dict) -> str:
    """Button label for a reciter: name plus bitrate.

    The bitrate is what tells two entries of the same reciter apart, and it is
    also how much phone storage a recitation will cost — so it belongs on the
    button, not one tap away.
    """
    bitrate = performer.get("bitrate", "").replace("Kbps", "kbps")
    if not bitrate:
        return performer["name"]
    return "%s · %s" % (performer["name"], bitrate)


def reciter_page_count() -> int:
    return max(1, -(-len(reciter_catalog()) // RECITER_PAGE_SIZE))


def reciter_page_of(subfolder: str) -> int:
    """The page holding `subfolder`, so /reciter opens where the user already is."""
    for i, p in enumerate(reciter_catalog()):
        if p["subfolder"] == subfolder:
            return i // RECITER_PAGE_SIZE
    return 0


def reciter_keyboard(ui_lang: str, page: int = 0, current: str | None = None) -> InlineKeyboardMarkup:
    """One page of the reciter catalog, two per row, under a Previous / n-of-m /
    Next pager and a search button.

    The catalog is ~80 entries, so it is paged rather than dumped in one keyboard:
    the pager walks the whole list, the search button jumps straight to a name.
    Pages wrap, so neither arrow is ever a dead button. `current` is marked with a
    dot, the same way the verse card marks the active view.
    """
    catalog = reciter_catalog()
    pages = reciter_page_count()
    page %= pages
    rows, row = [], []
    for p in catalog[page * RECITER_PAGE_SIZE:(page + 1) * RECITER_PAGE_SIZE]:
        label = reciter_label(p)
        if p["subfolder"] == current:
            label = "• " + label
        row.append(InlineKeyboardButton(label, callback_data="setreciter:" + p["subfolder"]))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    prev_label, next_label = _nav_labels(ui_lang)
    rows.append([
        InlineKeyboardButton(prev_label, callback_data="recpage:%d" % ((page - 1) % pages)),
        InlineKeyboardButton("%d/%d" % (page + 1, pages), callback_data="recpage_noop"),
        InlineKeyboardButton(next_label, callback_data="recpage:%d" % ((page + 1) % pages)),
    ])
    rows.append([InlineKeyboardButton("🔍 " + t("btn_search_reciter", ui_lang),
                                       callback_data="reciter_search")])
    return InlineKeyboardMarkup(rows)


# --- Verse reader card -------------------------------------------------------
# Every verse is delivered as a self-contained "card": the verse plus an inline
# keyboard that rides with it. Tapping a button fires a callback that edits the
# same message in place (for the text views) rather than posting a new one, so a
# reading session no longer floods the chat with near-identical bubbles.

# Short codes keep callback_data tiny (Telegram caps it at 64 bytes).
TYPE_BY_CODE = {"tr": "translation", "ar": "arabic", "tf": "tafsir", "au": "audio"}
CODE_BY_TYPE = {v: k for k, v in TYPE_BY_CODE.items()}

# Mode row, in display order. Only Audio carries an icon: it's the one entry that
# *plays* something rather than being another way to read the same verse.
_MODES = (
    ("translation", "btn_translation", ""),
    ("arabic",      "btn_arabic",      ""),
    ("tafsir",      "btn_tafsir",      ""),
    ("audio",       "btn_audio",       "🔊 "),
)


def verse_keyboard(surah: int, ayah: int, quran_type: str, ui_lang: str) -> InlineKeyboardMarkup:
    """The inline keyboard attached to a verse card — localized and RTL-aware.

    Three rows: choose a view (Translation / Arabic / Tafsir / Audio, the active
    one marked with a dot), navigate (Previous / Random / Next), and act
    (Language / Share). Every button except Random and Share is a "show ayah S:A
    as T" callback, so the handler stays uniform.

    `ui_lang` only: this keyboard's labels are bot UI text, independent of the
    user's chosen translation language.
    """
    def mode_button(mode: str, key: str, icon: str) -> InlineKeyboardButton:
        label = icon + t(key, ui_lang)
        if mode == quran_type:
            label = "• " + label            # the dot marks the view you're in now
        return InlineKeyboardButton(
            label, callback_data="vc:%s:%d:%d" % (CODE_BY_TYPE[mode], surah, ayah))

    code = CODE_BY_TYPE[quran_type]
    prev_s, prev_a = Quran.get_previous_ayah(surah, ayah)
    next_s, next_a = Quran.get_next_ayah(surah, ayah)
    rnd = t("btn_random", ui_lang)
    prev_label, next_label = _nav_labels(ui_lang)

    return InlineKeyboardMarkup([
        [mode_button(*mode) for mode in _MODES],
        [
            InlineKeyboardButton(prev_label, callback_data="vc:%s:%d:%d" % (code, prev_s, prev_a)),
            InlineKeyboardButton("🎲 " + rnd, callback_data="vr:%s" % code),
            InlineKeyboardButton(next_label, callback_data="vc:%s:%d:%d" % (code, next_s, next_a)),
        ],
        [
            InlineKeyboardButton("🌐 " + get_language(ui_lang).native, callback_data="showlang"),
            InlineKeyboardButton("📤", switch_inline_query="%d:%d" % (surah, ayah)),
        ],
    ])


async def build_verse_text(surah: int, ayah: int, quran_type: str,
                           ui_lang: str, translation_lang: str, data: dict) -> str:
    """HTML body for a text-view card: a bold surah-name header over the verse.

    Only the (untrusted) corpus text is HTML-escaped; the header is the sole tag
    and sits at the very start, so truncating an over-long tafsir at Telegram's
    4096-char limit can never split a tag.

    `ui_lang` drives the (English-only-tafsir) note text; `translation_lang`
    drives which translation corpus a "translation" view is read from — the two
    are independent settings.
    """
    if quran_type == "tafsir":
        body = data["tafsir"].get_ayah(surah, ayah)
        if ui_lang != DEFAULT_LANG:                     # tafsir is English-only; note it
            body += t("tafsir_en_note", ui_lang)
    else:
        quran = await get_translation(translation_lang)
        body = quran.get_ayah(surah, ayah)
    header = "<b>%s</b>" % html.escape(Quran.get_surah_name(surah))
    return (header + "\n\n" + html.escape(body))[:4096]


async def _resolve_settings(user_settings: UserSettings, chat_id, tg_user):
    """Return the caller's durable settings (ui_lang, translation_lang, reciter),
    detecting a UI language from Telegram on first contact.

    `chat_id` may be None for inline-query callers (no chat exists yet); in that
    case the legacy-Redis migration step inside UserSettings is simply skipped.
    """
    user_id = tg_user.id if tg_user is not None else chat_id
    default_ui_lang = normalize_lang(getattr(tg_user, "language_code", None))
    return await user_settings.get(user_id, chat_id, default_ui_lang=default_ui_lang)


async def handle_update(bot, data: dict, update: telegram.Update) -> None:
    """Process a single Telegram update pushed to the webhook."""
    file = File()
    user_settings = UserSettings()

    async def send_quran(surah: int, ayah: int, quran_type: str, chat_id: int,
                         performer: str, ui_lang: str, translation_lang: str, reply_markup=None):
        if quran_type in ("translation", "tafsir"):
            text = await build_verse_text(surah, ayah, quran_type, ui_lang, translation_lang, data)
            await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML",
                            reply_markup=reply_markup)
        elif quran_type == "arabic":
            await bot.send_chat_action(chat_id=chat_id,
                                action=telegram.constants.ChatAction.UPLOAD_PHOTO)
            image = file.get_image_filename(surah, ayah)
            await send_file(bot, image, quran_type, chat_id=chat_id,
                      caption=_reference(surah, ayah, ui_lang),
                      reply_markup=reply_markup)
        elif quran_type == "audio":
            await bot.send_chat_action(chat_id=chat_id,
                                action=telegram.constants.ChatAction.UPLOAD_VOICE)
            audio = file.get_audio_filename(surah, ayah, performer)
            await send_file(bot, audio, quran_type, chat_id=chat_id,
                      performer=File.get_performer_name(performer),
                      title=_reference(surah, ayah, ui_lang),
                      reply_markup=reply_markup)
        file.save_user(chat_id, (surah, ayah, quran_type))

    if update.inline_query:
        query_id = update.inline_query.id
        query = update.inline_query.query
        user = update.inline_query.from_user
        # inline users have no chat with us; key the preference by their user id
        settings = await _resolve_settings(user_settings, None, user)
        ui_lang, translation_lang = settings.ui_lang, settings.translation_lang
        results = []
        cache_time = 66 * (60 ** 2 * 24)
        is_personal = False
        # A range ("59:22-24") is answered as a range in every representation, the
        # same as in a chat — a single ayah is just the degenerate case start == end.
        surah, start, end = parse_ayah_range(query)
        if surah is not None and Quran.exists(surah, start) and Quran.exists(surah, end):
            ref = _ref_key(surah, start, end)
            quran = await get_translation(translation_lang)
            if end > start:
                translation = quran.get_ayahs(surah, start, end)
                tafsir = "\n\n".join(data["tafsir"].get_ayah(surah, a)
                                     for a in range(start, end + 1))
            else:
                translation = quran.get_ayah(surah, start)
                tafsir = data["tafsir"].get_ayah(surah, start)
            # Every result here is rendered from the caller's own settings —
            # translation_lang for the text, reciter for the audio — so this
            # branch is per-user too, and cannot use a long shared cache. The
            # short cache_time still absorbs the keystroke-by-keystroke repeats
            # Telegram sends while the query is being typed.
            cache_time, is_personal = INLINE_PERSONAL_CACHE_TIME, True
            results.append(InlineQueryResultArticle(
                ref + "translation", title=t("btn_translation", ui_lang),
                description=translation[:120],
                # a long range's text can outgrow Telegram's message limit
                input_message_content=InputTextMessageContent(translation[:4096]))
            )
            results.append(InlineQueryResultArticle(
                ref + "tafsir", title=t("btn_tafsir", ui_lang),
                description=tafsir[:120],
                input_message_content=InputTextMessageContent(tafsir[:4096]))
            )
            audio = _inline_audio_result(surah, start, end, settings.reciter, ui_lang, file)
            if audio is not None:
                results.append(audio)
            results.extend(_inline_photo_results(surah, start, end, ui_lang, file))
        else:
            # Not an ayah reference — try it as a reciter name, so the picker is
            # reachable from any chat without opening a DM with the bot first.
            matches = File.search_performers(query)
            if matches:
                # Unlike the immutable ayah text above, these are rendered in the
                # caller's own UI language and lead to a state change, so they must
                # not be served from a shared, long-lived cache.
                cache_time, is_personal = 0, True
                for p in matches:
                    # the subfolder keys the id: two entries can share a name (same
                    # reciter at different bitrates) and Telegram rejects duplicates
                    results.append(InlineQueryResultArticle(
                        "reciter:" + p["subfolder"], title=reciter_label(p),
                        description=t("reciter_inline_description", ui_lang),
                        input_message_content=InputTextMessageContent(
                            t("reciter_set", ui_lang).format(reciter=p["name"])),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                            t("btn_set_reciter", ui_lang),
                            callback_data="setreciter:" + p["subfolder"])]]))
                    )
            else:
                results = data["default_query_results"]
        await bot.answer_inline_query(inline_query_id=query_id, cache_time=cache_time,
                                      results=results, is_personal=is_personal)
        return

    if update.callback_query:  # a tap on an inline button (language/reciter picker or verse card)
        cq = update.callback_query
        cb_data = cq.data or ""
        # A card sent through inline mode carries an inline_message_id instead of a
        # message: there is no chat to read legacy state from, and the tapper may
        # never have opened a DM with us at all.
        from_inline = cq.message is None
        chat_id = cq.message.chat.id if cq.message else cq.from_user.id
        settings = await _resolve_settings(user_settings, None if from_inline else chat_id,
                                           cq.from_user)
        ui_lang, translation_lang, reciter = settings.ui_lang, settings.translation_lang, settings.reciter

        if cb_data.startswith("setlang:"):     # UI language picked from the /language keyboard
            code = normalize_lang(cb_data.split(":", 1)[1])
            await user_settings.set_ui_lang(cq.from_user.id, chat_id, code)
            await bot.answer_callback_query(cq.id)
            confirm = t("language_set", code).format(lang=get_language(code).native)
            # ReplyKeyboardRemove clears the persistent keyboard left over from the
            # pre-inline UI for anyone upgrading; new users never had one.
            await bot.send_message(chat_id=chat_id, text=confirm,
                            reply_markup=ReplyKeyboardRemove())
            return

        if cb_data.startswith("settranslang:"):  # translation language picked from /translation
            code = normalize_lang(cb_data.split(":", 1)[1])
            await user_settings.set_translation_lang(cq.from_user.id, chat_id, code)
            await bot.answer_callback_query(cq.id)
            confirm = t("translation_language_set", ui_lang).format(lang=get_language(code).native)
            await bot.send_message(chat_id=chat_id, text=confirm)
            return

        if cb_data.startswith("setreciter:"):  # reciter picked from the shortlist or search results
            subfolder = cb_data.split(":", 1)[1]
            await user_settings.set_reciter(cq.from_user.id, None if from_inline else chat_id,
                                            subfolder)
            confirm = t("reciter_set", ui_lang).format(reciter=File.get_performer_name(subfolder))
            if from_inline:
                # DMing someone who never started the bot raises Forbidden; the
                # callback answer reaches them wherever the card was shared instead.
                await bot.answer_callback_query(cq.id, text=confirm)
            else:
                await bot.answer_callback_query(cq.id)
                await bot.send_message(chat_id=chat_id, text=confirm)
            return

        if cb_data.startswith("recpage:"):      # the pager on the reciter picker
            page = int(cb_data.split(":", 1)[1])
            await bot.answer_callback_query(cq.id)
            if cq.message is None:
                return                          # no message of ours to turn the page in
            try:                                # swap the keyboard, don't post a new list
                await bot.edit_message_reply_markup(
                    chat_id=chat_id, message_id=cq.message.message_id,
                    reply_markup=reciter_keyboard(ui_lang, page, current=reciter))
            except telegram.error.BadRequest as err:
                if "not modified" not in str(err).lower():
                    raise
            return

        if cb_data == "reciter_search":         # the search button on the reciter picker
            file.set_awaiting_input(chat_id, "reciter_search")
            await bot.answer_callback_query(cq.id)
            await bot.send_message(chat_id=chat_id, text=t("reciter_search_prompt", ui_lang))
            return

        if cb_data == "showlang":               # the 🌐 button on a verse card
            await bot.answer_callback_query(cq.id)
            await bot.send_message(chat_id=chat_id, text=t("choose_language", ui_lang),
                            reply_markup=language_keyboard())
            return

        if cb_data.startswith("vc:") or cb_data.startswith("vr:"):  # a verse-card tap
            parts = cb_data.split(":")
            code = parts[1]
            if cb_data.startswith("vr:"):       # random ayah, same view
                surah, ayah = Quran.get_random_ayah()
            else:                               # vc:<type>:<surah>:<ayah>
                surah, ayah = int(parts[2]), int(parts[3])
            quran_type = TYPE_BY_CODE.get(code, "translation")
            if not Quran.exists(surah, ayah):
                await bot.answer_callback_query(cq.id)
                return
            markup = verse_keyboard(surah, ayah, quran_type, ui_lang)
            msg = cq.message
            on_media = bool(msg and (msg.photo or msg.audio))
            if quran_type in ("translation", "tafsir"):
                text = await build_verse_text(surah, ayah, quran_type, ui_lang, translation_lang, data)
                if on_media or msg is None:
                    # can't turn a photo/audio message into text — post a fresh card
                    await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML",
                                    reply_markup=markup)
                else:
                    try:                        # the common path: turn the page in place
                        await bot.edit_message_text(text=text, chat_id=chat_id,
                                        message_id=msg.message_id, parse_mode="HTML",
                                        reply_markup=markup)
                    except telegram.error.BadRequest as err:
                        # re-tapping the current view yields an identical message; ignore
                        if "not modified" not in str(err).lower():
                            raise
                file.save_user(chat_id, (surah, ayah, quran_type))
            else:                               # arabic/audio arrive as fresh media messages
                await send_quran(surah, ayah, quran_type, chat_id, reciter, ui_lang, translation_lang,
                                 reply_markup=markup)
            await bot.answer_callback_query(cq.id)
            return

        await bot.answer_callback_query(cq.id)  # unknown callback: acknowledge and ignore
        return

    if not update.message or not update.message.text:  # updates without text
        return

    chat_id = update.message.chat.id
    raw_message = update.message.text
    message = raw_message.lower()
    settings = await _resolve_settings(user_settings, chat_id, update.message.from_user)
    ui_lang, translation_lang, reciter = settings.ui_lang, settings.translation_lang, settings.reciter

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

    if file.pop_awaiting_input(chat_id) == "reciter_search":
        # a name typed after tapping "🔍 Search reciter" — not an ayah reference
        matches = File.search_performers(raw_message)
        if not matches:
            await bot.send_message(chat_id=chat_id, text=t("reciter_search_no_matches", ui_lang))
            file.set_awaiting_input(chat_id, "reciter_search")  # allow one retry
            return
        rows, row = [], []
        for p in matches:
            row.append(InlineKeyboardButton(reciter_label(p),
                                            callback_data="setreciter:" + p["subfolder"]))
            if len(row) == 2:
                rows.append(row)
                row = []
        if row:
            rows.append(row)
        await bot.send_message(chat_id=chat_id, text=t("reciter_search_results", ui_lang),
                        reply_markup=InlineKeyboardMarkup(rows))
        return

    if message.startswith("/"):
        command = message[1:].split("@", 1)[0]   # tolerate /help@BotName
        if command in ("start", "help"):
            # ReplyKeyboardRemove clears the old persistent keyboard for anyone
            # upgrading from the pre-inline UI; new users never see one.
            await bot.send_message(chat_id=chat_id, text=welcome_text(ui_lang),
                            parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
            return
        elif command == "about":
            await bot.send_message(chat_id=chat_id, text=t("about", ui_lang), parse_mode="HTML")
            return
        elif command == "index":
            await bot.send_message(chat_id=chat_id, text=data["index"], parse_mode="HTML")
            return
        elif command == "language":
            await bot.send_message(chat_id=chat_id, text=t("choose_language", ui_lang),
                            reply_markup=language_keyboard())
            return
        elif command == "translation":
            await bot.send_message(chat_id=chat_id, text=t("choose_translation_language", ui_lang),
                            reply_markup=translation_language_keyboard())
            return
        elif command == "reciter":
            # open on the page the current reciter is on, with it marked
            await bot.send_message(chat_id=chat_id, text=t("choose_reciter", ui_lang),
                            reply_markup=reciter_keyboard(ui_lang, reciter_page_of(reciter),
                                                          current=reciter))
            return
        elif command == "random":
            surah, ayah = Quran.get_random_ayah()
            await send_quran(surah, ayah, quran_type, chat_id, reciter, ui_lang, translation_lang,
                             reply_markup=verse_keyboard(surah, ayah, quran_type, ui_lang))
            return
        # unknown command: fall through (ignored, as before)

    action = button_action(message, ui_lang)
    if action in ("arabic", "audio", "translation", "tafsir"):
        await send_quran(surah, ayah, action, chat_id, reciter, ui_lang, translation_lang,
                         reply_markup=verse_keyboard(surah, ayah, action, ui_lang))
        return
    elif action in ("next", "previous", "random"):
        if action == "next":
            surah, ayah = Quran.get_next_ayah(surah, ayah)
        elif action == "previous":
            surah, ayah = Quran.get_previous_ayah(surah, ayah)
        else:
            surah, ayah = Quran.get_random_ayah()
        await send_quran(surah, ayah, quran_type, chat_id, reciter, ui_lang, translation_lang,
                         reply_markup=verse_keyboard(surah, ayah, quran_type, ui_lang))
        return

    surah, start, end = parse_ayah_range(message)
    if surah:
        if end > start:  # a range like "53:1-7" -> one combined audio
            if not (Quran.exists(surah, start) and Quran.exists(surah, end)):
                await bot.send_message(chat_id=chat_id, text=t("ayah_not_found", ui_lang))
            elif end - start + 1 > MAX_RANGE_AYAHS:
                await bot.send_message(
                    chat_id=chat_id,
                    text=t("range_too_large", ui_lang).format(n=MAX_RANGE_AYAHS))
            else:
                await send_combined_audio(bot, surah, start, end, chat_id, reciter,
                                          reply_markup=verse_keyboard(surah, end, "audio", ui_lang))
        elif Quran.exists(surah, start):
            await send_quran(surah, start, quran_type, chat_id, reciter, ui_lang, translation_lang,
                             reply_markup=verse_keyboard(surah, start, quran_type, ui_lang))
        else:
            await bot.send_message(chat_id=chat_id, text=t("ayah_not_found", ui_lang))


# ---------------------------------------------------------------------------
# Webhook app
# ---------------------------------------------------------------------------

app = FastAPI()
bot = None  # created during background init (guarded) so a bad/missing TOKEN can't crash import
data = None  # populated by background init after corpora finish parsing


# Telegram's per-language command menu only accepts two-letter ISO-639-1 codes,
# so script-qualified and three-letter codes ("uz-Cyrl", "ber") can't be
# registered — those users see the English default menu while the rest of their
# UI is still localized.
_COMMAND_MENU_LANGS = tuple(lang.code for lang in LANGUAGES
                            if len(lang.code) == 2 and lang.code != DEFAULT_LANG)


def _commands_for(lang: str) -> list:
    # Same source of truth as the /start message's command list (see BOT_COMMANDS).
    return [BotCommand(command, t(key, lang)) for command, key in BOT_COMMANDS]


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
        pool = await get_pool()
        schema_path = os.path.join(os.path.dirname(__file__), "common", "schema.sql")
        with open(schema_path, "r", encoding="utf-8") as fp:
            await pool.execute(fp.read())
        print("Postgres settings store ready")
    except Exception as e:
        print("INIT ERROR (postgres):", type(e).__name__, e)

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
    try:
        await close_pool()
    except Exception as e:
        print("Shutdown: close_pool failed:", type(e).__name__, e)


@app.get("/")
async def health():
    return {"status": "ok"}


@app.get(RANGE_AUDIO_PATH)
async def range_audio(surah: int, start: int, end: int, reciter: str):
    """Serve a range of ayahs as one mp3, for Telegram to fetch when someone picks
    the combined recitation from an inline answer (see `_inline_audio_result`).

    Public by necessity — Telegram cannot authenticate — so every parameter is
    validated and the range is bounded, leaving nothing here but Qur'an audio the
    bot would have sent anyway.
    """
    if not (Quran.exists(surah, start) and Quran.exists(surah, end)):
        return Response(status_code=404)
    if start > end or end - start + 1 > MAX_RANGE_AYAHS:
        return Response(status_code=404)
    try:
        audio = await _download_combined_audio(surah, start, end, reciter)
    except ValueError:                          # reciter is not in the catalog
        return Response(status_code=404)
    except httpx.HTTPError as e:                # the recitation CDN is unreachable
        print("range_audio: upstream fetch failed:", type(e).__name__, e)
        return Response(status_code=502)
    return Response(
        content=audio.getvalue(), media_type="audio/mpeg",
        headers={"Content-Disposition": 'inline; filename="%s"' % audio.name,
                 "Cache-Control": "public, max-age=86400"},
    )


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
