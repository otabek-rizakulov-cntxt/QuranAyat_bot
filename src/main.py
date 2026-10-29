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

import logging
import os

from dotenv import load_dotenv

from config.logging import setup_logging

load_dotenv()
setup_logging()

import asyncio
from time import time

import httpx
import telegram
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from telegram import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)

import hifz
from api import router as api_router
from bot.inline import answer_inline_query, get_default_query_results
from bot.keyboards.language import language_keyboard, translation_language_keyboard
from bot.keyboards.reciter import (
    reciter_keyboard,
    reciter_label,
    reciter_page_of,
    reciter_set_confirmation,
)
from bot.keyboards.sajda import sajda_keyboard
from bot.keyboards.verse import TYPE_BY_CODE, verse_keyboard
from bot.limits import MAX_RANGE_AYAHS
from bot.media import (
    RANGE_AUDIO_PATH,
    send_combined_audio,
    send_page,
    send_page_audio,
    send_quran,
    send_repeated_audio,
)
from bot.settings import resolve_settings
from bot.text import build_verse_text
from config import Environment
from config.env import webhook_base_url
from config.postgres import close_pool
from config.redis import RedisSingleton, cache_backend
from domain.parsing import as_int, parse_ayah_range
from infra import audio as cdn_audio
from lib.miniapp import app_row, set_menu_button
from lib.store import apply_schema, store_backend
from lib.user_settings import UserSettings
from lib.utils import File
from locales import (
    BOT_COMMANDS,
    DEFAULT_LANG,
    UI_LANGUAGES,
    button_action,
    get_language,
    normalize_lang,
    t,
    welcome_text,
)
from modules import Bot, Quran, TranslationRegistry, make_index
from services.reciters import (  # noqa: F401 — re-exported; tests and the picker use them here
    _KIND_WARNING_KEYS,
    _RECITER_SHORTLIST,
    DEFAULT_RECITER_KIND,
    RECITER_KINDS,
    reciter_catalog,
    reciter_group,
    reciter_kind,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Bot logic
# ---------------------------------------------------------------------------


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


async def handle_update(bot, data: dict, update: telegram.Update) -> None:
    """Process a single Telegram update pushed to the webhook."""
    file = File()
    user_settings = UserSettings()

    if update.my_chat_member:  # the bot was added to or removed from a chat
        from hifz import group as hifz_group
        from lib.store import get_store

        try:
            await hifz_group.on_my_chat_member(bot, await get_store(), update)
        except telegram.error.Forbidden:
            pass  # no permission to post in that group; nothing to do
        return

    if update.inline_query:
        await answer_inline_query(bot, data, update.inline_query)
        return

    if update.callback_query:  # a tap on an inline button (language/reciter picker or verse card)
        cq = update.callback_query
        cb_data = cq.data or ""
        # A card sent through inline mode carries an inline_message_id instead of a
        # message: there is no chat to read legacy state from, and the tapper may
        # never have opened a DM with us at all.
        from_inline = cq.message is None
        chat_id = cq.message.chat.id if cq.message else cq.from_user.id
        settings = await resolve_settings(
            user_settings, None if from_inline else chat_id, cq.from_user
        )
        ui_lang, translation_lang, reciter = (
            settings.ui_lang,
            settings.translation_lang,
            settings.reciter,
        )

        if cb_data.startswith("setlang:"):  # UI language picked from the /language keyboard
            # normalize_lang already refuses translation-only codes (there is no
            # string table to show the interface in), falling back to English.
            code = normalize_lang(cb_data.split(":", 1)[1])
            await user_settings.set_ui_lang(cq.from_user.id, chat_id, code)
            await bot.answer_callback_query(cq.id)
            confirm = t("language_set", code).format(lang=get_language(code).native)
            # ReplyKeyboardRemove clears the persistent keyboard left over from the
            # pre-inline UI for anyone upgrading; new users never had one.
            await bot.send_message(
                chat_id=chat_id, text=confirm, reply_markup=ReplyKeyboardRemove()
            )
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
            await user_settings.set_reciter(
                cq.from_user.id, None if from_inline else chat_id, subfolder
            )
            confirm = reciter_set_confirmation(subfolder, ui_lang)
            if from_inline:
                # DMing someone who never started the bot raises Forbidden; the
                # callback answer reaches them wherever the card was shared instead.
                await bot.answer_callback_query(cq.id, text=confirm)
            else:
                await bot.answer_callback_query(cq.id)
                await bot.send_message(chat_id=chat_id, text=confirm)
            return

        if cb_data.startswith("recgrp:"):  # a group tab or the pager on the picker
            _, kind, page_s = cb_data.split(":", 2)
            await bot.answer_callback_query(cq.id)
            if cq.message is None:
                return  # no message of ours to turn the page in
            try:  # swap the keyboard, don't post a new list
                await bot.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=cq.message.message_id,
                    reply_markup=reciter_keyboard(ui_lang, kind, int(page_s), current=reciter),
                )
            except telegram.error.BadRequest as err:
                if "not modified" not in str(err).lower():
                    raise
            return

        if cb_data == "reciter_search":  # the search button on the reciter picker
            file.set_awaiting_input(chat_id, "reciter_search")
            await bot.answer_callback_query(cq.id)
            await bot.send_message(chat_id=chat_id, text=t("reciter_search_prompt", ui_lang))
            return

        if cb_data.startswith("rep:"):  # "🔁 Repeat ×3" on a verse card
            _, surah_s, ayah_s = cb_data.split(":", 2)
            surah, ayah = int(surah_s), int(ayah_s)
            await bot.answer_callback_query(cq.id)
            if Quran.exists(surah, ayah):
                await send_repeated_audio(
                    bot,
                    surah,
                    ayah,
                    chat_id,
                    reciter,
                    ui_lang,
                    reply_markup=verse_keyboard(surah, ayah, "audio", ui_lang),
                )
            return

        if cb_data.startswith("pg:"):  # the mushaf pager
            page = int(cb_data.split(":", 1)[1])
            await bot.answer_callback_query(cq.id)
            if 1 <= page <= Quran.PAGE_COUNT:
                # a page arrives as an image, so it is a fresh message rather than
                # an edit of the one that was tapped
                await send_page(bot, page, chat_id, ui_lang)
            return

        if cb_data.startswith("pga:"):  # "listen to this page"
            page = int(cb_data.split(":", 1)[1])
            await bot.answer_callback_query(cq.id)
            if 1 <= page <= Quran.PAGE_COUNT:
                await send_page_audio(bot, page, chat_id, reciter, ui_lang)
            return

        if cb_data == "showlang":  # the 🌐 button on a verse card
            await bot.answer_callback_query(cq.id)
            await bot.send_message(
                chat_id=chat_id,
                text=t("choose_language", ui_lang),
                reply_markup=language_keyboard(),
            )
            return

        if cb_data.startswith("vc:") or cb_data.startswith("vr:"):  # a verse-card tap
            parts = cb_data.split(":")
            code = parts[1]
            if cb_data.startswith("vr:"):  # random ayah, same view
                surah, ayah = Quran.get_random_ayah()
            else:  # vc:<type>:<surah>:<ayah>
                surah, ayah = int(parts[2]), int(parts[3])
            quran_type = TYPE_BY_CODE.get(code, "translation")
            if not Quran.exists(surah, ayah):
                await bot.answer_callback_query(cq.id)
                return
            markup = verse_keyboard(surah, ayah, quran_type, ui_lang, app=not from_inline)
            msg = cq.message
            on_media = bool(msg and (msg.photo or msg.audio))
            if quran_type in ("translation", "tafsir"):
                text = await build_verse_text(
                    surah, ayah, quran_type, ui_lang, translation_lang, data
                )
                if on_media or msg is None:
                    # can't turn a photo/audio message into text — post a fresh card
                    await bot.send_message(
                        chat_id=chat_id, text=text, parse_mode="HTML", reply_markup=markup
                    )
                else:
                    try:  # the common path: turn the page in place
                        await bot.edit_message_text(
                            text=text,
                            chat_id=chat_id,
                            message_id=msg.message_id,
                            parse_mode="HTML",
                            reply_markup=markup,
                        )
                    except telegram.error.BadRequest as err:
                        # re-tapping the current view yields an identical message; ignore
                        if "not modified" not in str(err).lower():
                            raise
                await file.save_user(chat_id, (surah, ayah, quran_type))
            else:  # arabic/audio arrive as fresh media messages
                await send_quran(
                    bot,
                    data,
                    file,
                    surah,
                    ayah,
                    quran_type,
                    chat_id,
                    reciter,
                    ui_lang,
                    translation_lang,
                    reply_markup=markup,
                )
            await bot.answer_callback_query(cq.id)
            return

        # hifz features (src/hifz) claim their own callback prefixes — see hifz.PREFIXES.
        ctx = await hifz.Ctx.build(
            bot, data, file, chat_id, cq.from_user.id, settings, callback_query=cq
        )
        if await hifz.dispatch_callback(ctx, cb_data):
            return

        await bot.answer_callback_query(cq.id)  # unknown callback: acknowledge and ignore
        return

    if not update.message or not update.message.text:  # updates without text
        return

    chat_id = update.message.chat.id
    raw_message = update.message.text
    message = raw_message.lower()
    settings = await resolve_settings(user_settings, chat_id, update.message.from_user)
    ui_lang, translation_lang, reciter = (
        settings.ui_lang,
        settings.translation_lang,
        settings.reciter,
    )

    state = await file.get_user(chat_id)
    if state is not None:
        surah, ayah, quran_type = state
        if quran_type == "english":  # legacy stored value -> canonical name
            quran_type = "translation"
    else:
        surah, ayah, quran_type = 1, 1, "translation"

    logger.debug("%d:%.3f:%s" % (chat_id, time(), message.replace("\n", " ")))

    if chat_id < 0:
        # Group *text* is still ignored: the group cluster is driven entirely from
        # DM (admin setup, board join) and the scheduler (the daily post), never by
        # reading group chatter. Being added or removed is a my_chat_member update,
        # handled at the top of this function before we ever get here.
        return

    if message.startswith("/"):
        command = message[1:].split("@", 1)[0]  # tolerate /help@BotName
        # "/page 255" -> ("page", "255"). A bare reference like "/2:255" leaves an
        # unmatched command and falls through to the reference parser, as before.
        command, _, argument = command.partition(" ")
        argument = argument.strip()
        # A command always wins over a pending free-text prompt. The awaited-input
        # check used to run *before* this chain, so a typed /start while the bot
        # awaited a reciter name was swallowed as the name, with no way out.
        file.pop_awaiting_input(chat_id)
        if command in ("start", "help"):
            # A /start deep link (t.me/bot?start=gs_-100…) carries a group payload
            # the group feature owns — admin setup, or a member joining the board.
            if command == "start" and argument:
                from hifz import group as hifz_group

                ctx = await hifz.Ctx.build(
                    bot, data, file, chat_id, update.message.from_user.id, settings
                )
                if await hifz_group.handle_start_payload(ctx, argument):
                    return
            # ReplyKeyboardRemove clears the old persistent keyboard for anyone
            # upgrading from the pre-inline UI; new users never see one.
            await bot.send_message(
                chat_id=chat_id,
                text=welcome_text(ui_lang),
                parse_mode="HTML",
                reply_markup=ReplyKeyboardRemove(),
            )
            return
        elif command == "app":
            row = app_row("📱 " + t("web_btn_open_app", ui_lang), "/")
            await bot.send_message(
                chat_id=chat_id,
                text=t("web_app_intro" if row else "web_app_unavailable", ui_lang),
                reply_markup=InlineKeyboardMarkup(row) if row else None,
            )
            return
        elif command == "about":
            await bot.send_message(chat_id=chat_id, text=t("about", ui_lang), parse_mode="HTML")
            return
        elif command == "index":
            await bot.send_message(chat_id=chat_id, text=data["index"], parse_mode="HTML")
            return
        elif command == "language":
            await bot.send_message(
                chat_id=chat_id,
                text=t("choose_language", ui_lang),
                reply_markup=language_keyboard(),
            )
            return
        elif command == "translation":
            await bot.send_message(
                chat_id=chat_id,
                text=t("choose_translation_language", ui_lang),
                reply_markup=translation_language_keyboard(),
            )
            return
        elif command == "reciter":
            # open on the tab and page the current reciter is on, with it marked
            kind, page = reciter_page_of(reciter)
            await bot.send_message(
                chat_id=chat_id,
                text=t("choose_reciter", ui_lang),
                reply_markup=reciter_keyboard(ui_lang, kind, page, current=reciter),
            )
            return
        elif command == "page":
            # bare /page opens where the reader already is, rather than erroring
            page = Quran.page_of(surah, ayah) if not argument else as_int(argument)
            if page is None or not 1 <= page <= Quran.PAGE_COUNT:
                await bot.send_message(
                    chat_id=chat_id,
                    text=t("page_out_of_range", ui_lang).format(total=Quran.PAGE_COUNT),
                )
                return
            await send_page(bot, page, chat_id, ui_lang)
            return
        elif command == "juz":
            juz = Quran.juz_of(surah, ayah) if not argument else as_int(argument)
            if juz is None or not 1 <= juz <= Quran.JUZ_COUNT:
                await bot.send_message(
                    chat_id=chat_id,
                    text=t("juz_out_of_range", ui_lang).format(total=Quran.JUZ_COUNT),
                )
                return
            # a juz is ~20 pages of reading, so it opens the page reader at its
            # first page rather than trying to be a single message or audio file
            start_s, start_a, _, _ = Quran.juz_range(juz)
            await send_page(bot, Quran.page_of(start_s, start_a), chat_id, ui_lang)
            return
        elif command == "sajda":
            await bot.send_message(
                chat_id=chat_id,
                text=t("sajda_list_title", ui_lang),
                reply_markup=sajda_keyboard(ui_lang),
            )
            return
        elif command == "random":
            surah, ayah = Quran.get_random_ayah()
            await send_quran(
                bot,
                data,
                file,
                surah,
                ayah,
                quran_type,
                chat_id,
                reciter,
                ui_lang,
                translation_lang,
                reply_markup=verse_keyboard(surah, ayah, quran_type, ui_lang),
            )
            return
        # hifz features (src/hifz) register their own commands; they are looked up
        # here so a command escapes any wizard in progress rather than feeding it.
        if hifz.handles(command):
            ctx = await hifz.Ctx.build(
                bot,
                data,
                file,
                chat_id,
                update.message.from_user.id,
                settings,
                argument=argument,
                message=update.message,
            )
            await hifz.dispatch_command(ctx, command)
            return
        # unknown command: fall through (ignored, as before)

    if file.pop_awaiting_input(chat_id) == "reciter_search":
        # a name typed after tapping "🔍 Search reciter" — not an ayah reference
        matches = File.search_performers(raw_message)
        if not matches:
            await bot.send_message(chat_id=chat_id, text=t("reciter_search_no_matches", ui_lang))
            file.set_awaiting_input(chat_id, "reciter_search")  # allow one retry
            return
        rows, row = [], []
        for p in matches:
            row.append(
                InlineKeyboardButton(reciter_label(p), callback_data="setreciter:" + p["subfolder"])
            )
            if len(row) == 2:
                rows.append(row)
                row = []
        if row:
            rows.append(row)
        await bot.send_message(
            chat_id=chat_id,
            text=t("reciter_search_results", ui_lang),
            reply_markup=InlineKeyboardMarkup(rows),
        )
        return

    # A hifz wizard in progress consumes free text — but only after the command
    # chain above, so /cancel and every other command remain an escape hatch.
    if hifz.has_wizard(update.message.from_user.id):
        ctx = await hifz.Ctx.build(
            bot, data, file, chat_id, update.message.from_user.id, settings, message=update.message
        )
        if await hifz.dispatch_wizard(ctx, raw_message):
            return

    action = button_action(message, ui_lang)
    if action in ("arabic", "audio", "translation", "tafsir"):
        await send_quran(
            bot,
            data,
            file,
            surah,
            ayah,
            action,
            chat_id,
            reciter,
            ui_lang,
            translation_lang,
            reply_markup=verse_keyboard(surah, ayah, action, ui_lang),
        )
        return
    elif action in ("next", "previous", "random"):
        if action == "next":
            surah, ayah = Quran.get_next_ayah(surah, ayah)
        elif action == "previous":
            surah, ayah = Quran.get_previous_ayah(surah, ayah)
        else:
            surah, ayah = Quran.get_random_ayah()
        await send_quran(
            bot,
            data,
            file,
            surah,
            ayah,
            quran_type,
            chat_id,
            reciter,
            ui_lang,
            translation_lang,
            reply_markup=verse_keyboard(surah, ayah, quran_type, ui_lang),
        )
        return

    surah, start, end = parse_ayah_range(message)
    if surah:
        if end > start:  # a range like "53:1-7" -> one combined audio
            if not (Quran.exists(surah, start) and Quran.exists(surah, end)):
                await bot.send_message(chat_id=chat_id, text=t("ayah_not_found", ui_lang))
            elif end - start + 1 > MAX_RANGE_AYAHS:
                await bot.send_message(
                    chat_id=chat_id, text=t("range_too_large", ui_lang).format(n=MAX_RANGE_AYAHS)
                )
            else:
                await send_combined_audio(
                    bot,
                    surah,
                    start,
                    end,
                    chat_id,
                    reciter,
                    reply_markup=verse_keyboard(surah, end, "audio", ui_lang),
                )
        elif Quran.exists(surah, start):
            await send_quran(
                bot,
                data,
                file,
                surah,
                start,
                quran_type,
                chat_id,
                reciter,
                ui_lang,
                translation_lang,
                reply_markup=verse_keyboard(surah, start, quran_type, ui_lang),
            )
        else:
            await bot.send_message(chat_id=chat_id, text=t("ayah_not_found", ui_lang))


# ---------------------------------------------------------------------------
# Webhook app
# ---------------------------------------------------------------------------

app = FastAPI()
app.include_router(api_router)

# The Mini App is served from its own origin (docs/MINI_APP_PLAN.md §4.3), so the
# browser needs CORS to reach /api/v1. Allow-list only, bearer header only — no
# cookies. With no origins configured the middleware is not installed at all.
_miniapp_origins = [
    o.strip() for o in (Environment.get_env("miniapp_origins") or "").split(",") if o.strip()
]
if _miniapp_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_miniapp_origins,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
        allow_credentials=False,
        max_age=600,
    )
bot = None  # created during background init (guarded) so a bad/missing TOKEN can't crash import
data = None  # populated by background init after corpora finish parsing


# Telegram's per-language command menu only accepts two-letter ISO-639-1 codes,
# so script-qualified and three-letter codes ("uz-Cyrl", "ber") can't be
# registered — those users see the English default menu while the rest of their
# UI is still localized.
_COMMAND_MENU_LANGS = tuple(
    lang.code for lang in UI_LANGUAGES if len(lang.code) == 2 and lang.code != DEFAULT_LANG
)


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
        logger.error("INIT ERROR (set_my_commands, default): %s: %s", type(e).__name__, e)
        return  # the API is unhappy; skip the per-language pass
    registered, rejected = 1, []
    for code in _COMMAND_MENU_LANGS:
        try:
            await bot.set_my_commands(_commands_for(code), language_code=code)
            registered += 1
        except Exception as e:
            rejected.append("%s (%s)" % (code, type(e).__name__))
    logger.info("Command menu registered for %d languages" % registered)
    if rejected:
        logger.warning("Command menu not accepted for: %s", ", ".join(rejected))


async def _initialize():
    """Heavy init (bot, corpora parsing, webhook registration) done OFF the startup path.

    Parsing the Quran translation + tafsir is CPU-bound and slow on small free instances;
    if it ran inside the startup event, uvicorn wouldn't accept connections until it finished
    and the platform's health check would fail the deploy. So we return from startup immediately
    and do this in the background — the server listens right away and answers `/`.
    """
    global data, bot

    if not os.getenv("PAGE_IMAGE_BASE_URL"):
        # The page stitcher tiles per-ayah images edge to edge, which only works if
        # every image is the same width. Falling back to PHOTO_BASE_URL is fine when
        # that points at a uniform set (everyayah's `quranpngs`) and produces ragged
        # pages when it does not (`images_png` varies 115-700px), so say so rather
        # than let /page quietly look broken.
        logger.warning(
            "PAGE_IMAGE_BASE_URL is not set — /page will tile "
            "PHOTO_BASE_URL's images, which must be a uniform-width set "
            "(e.g. everyayah.com/data/quranpngs) or pages will render ragged."
        )

    try:
        bot = Bot.get_instance()
    except Exception as e:
        logger.error("INIT ERROR (bot — check TOKEN): %s: %s", type(e).__name__, e)

    try:
        # Through the repository layer: it owns the schema file and knows that the
        # in-memory store has no schema to apply. Reaching for the pool directly
        # here raised AttributeError on every boot without DATABASE_URL, because
        # get_pool() answers None in that case.
        await apply_schema()
        logger.info("Settings store ready")
    except Exception as e:
        logger.error("INIT ERROR (postgres): %s: %s", type(e).__name__, e)

    try:
        # Connect now rather than on the first update, so a missing or
        # unreachable Redis shows on the health check straight after boot. In a
        # worker thread: the client is synchronous and a connect can block.
        await asyncio.to_thread(RedisSingleton)
        logger.info("Cache ready (%s)" % cache_backend())
    except Exception as e:
        logger.error("INIT ERROR (redis): %s: %s", type(e).__name__, e)

    try:
        # run the blocking parse in a worker thread so the event loop stays responsive
        data = await asyncio.to_thread(build_data)
        logger.info("Corpora loaded; bot is ready")
    except Exception as e:
        logger.error("INIT ERROR (build_data — check corpus files): %s: %s", type(e).__name__, e)

    webhook_base = webhook_base_url()
    if bot and webhook_base:
        try:
            token = Environment.get_env("token")
            await bot.set_webhook(url=f"{webhook_base}/webhook/{token}")
            logger.info("Webhook registered at %s", webhook_base)
        except Exception as e:
            logger.error("INIT ERROR (set_webhook): %s: %s", type(e).__name__, e)
    else:
        logger.warning("Webhook NOT registered (bot=%s, base=%s)" % (bool(bot), webhook_base))

    if bot:
        await _set_bot_commands(bot)
        try:
            if await set_menu_button(bot):
                logger.info("Menu button opens the Mini App")
        except Exception as e:
            logger.error("INIT ERROR (set_chat_menu_button): %s: %s", type(e).__name__, e)

    # Register the hifz features (src/hifz/*.py) — imported here, once the rest of
    # main is loaded, so a feature module may import from main without a cycle.
    try:
        hifz.load_features()
    except Exception as e:
        logger.error("INIT ERROR (hifz features): %s: %s", type(e).__name__, e)

    # --- SCHEDULER SLOT (Wave 1D) ---------------------------------------------
    # The due-queue loop. It goes last because it needs `bot` and `data`
    # populated and the schema applied — and after hifz.load_features(), because
    # that import is what registers the per-kind send handlers it dispatches to.
    #
    # The loop owns its own error handling (a failing tick is logged and the loop
    # continues), so the only thing that can land here is a failure to *start* it.
    # It is stopped by cancellation when uvicorn tears the event loop down.
    try:
        from lib.scheduler import run_scheduler

        task = asyncio.create_task(run_scheduler(bot, data))
        _background_tasks.add(task)  # strong ref: tasks are GC'd otherwise
        task.add_done_callback(_background_tasks.discard)
    except Exception as e:
        logger.error("INIT ERROR (scheduler): %s: %s", type(e).__name__, e)


@app.on_event("startup")
async def on_startup():
    # Kick off heavy init in the background and return immediately so the HTTP server
    # starts listening and passes health checks without waiting on corpora parsing.
    task = asyncio.create_task(_initialize())
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)
    logger.info("Startup event returned — HTTP server is listening")


@app.on_event("shutdown")
async def on_shutdown():
    if bot is not None:
        try:
            await bot.delete_webhook()
        except Exception as e:
            logger.error("Shutdown: delete_webhook failed: %s: %s", type(e).__name__, e)
    try:
        await close_pool()
    except Exception as e:
        logger.error("Shutdown: close_pool failed: %s: %s", type(e).__name__, e)


@app.get("/")
async def health(response: Response):
    """Liveness plus where state lives: `store` for user settings, `cache` for
    Redis. 503 when either could not be reached or isn't configured, so a
    deployment missing its database or Redis fails its health check instead of
    serving a bot that forgets every user on the next restart. "pending" (still
    booting) stays 200, so a slow start isn't mistaken for an outage."""
    store, cache = store_backend(), cache_backend()
    healthy = "unavailable" not in (store, cache)
    if not healthy:
        response.status_code = 503
    return {"status": "ok" if healthy else "unavailable", "store": store, "cache": cache}


@app.get(RANGE_AUDIO_PATH)
async def range_audio(surah: int, start: int, end: int, reciter: str):
    """Serve a range of ayahs as one mp3, for Telegram to fetch when someone picks
    the combined recitation from an inline answer (see `inline_audio_result`).

    Public by necessity — Telegram cannot authenticate — so every parameter is
    validated and the range is bounded, leaving nothing here but Qur'an audio the
    bot would have sent anyway.
    """
    if not (Quran.exists(surah, start) and Quran.exists(surah, end)):
        return Response(status_code=404)
    if start > end or end - start + 1 > MAX_RANGE_AYAHS:
        return Response(status_code=404)
    try:
        audio = await cdn_audio.download_combined_audio(surah, start, end, reciter)
    except ValueError:  # reciter is not in the catalog
        return Response(status_code=404)
    except httpx.HTTPError as e:  # the recitation CDN is unreachable
        logger.error("range_audio: upstream fetch failed: %s: %s", type(e).__name__, e)
        return Response(status_code=502)
    return Response(
        content=audio.getvalue(),
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": 'inline; filename="%s"' % audio.name,
            "Cache-Control": "public, max-age=86400",
        },
    )


# Keep strong references to in-flight background tasks so they aren't garbage-collected.
_background_tasks: set = set()


async def _process_update(update: telegram.Update) -> None:
    try:
        await handle_update(bot, data, update)
    except telegram.error.Forbidden:
        pass  # user has blocked or removed the bot; nothing to do
    except Exception as e:
        logger.error("Error handling update: %s: %s", type(e).__name__, e)


@app.post("/webhook/{token}")
async def telegram_webhook(token: str, request: Request):
    if token != Environment.get_env("token"):
        return Response(status_code=404)
    if bot is None or data is None:
        # still initializing (corpora parsing) — ack so Telegram doesn't retry-flood
        logger.warning("Webhook hit before init finished; acking without processing")
        return {"ok": True}

    payload = await request.json()
    update = telegram.Update.de_json(payload, bot)
    # Ack Telegram immediately and do the (possibly slow) work in the background,
    # so downloading/uploading combined audio doesn't hold the webhook response open.
    task = asyncio.create_task(_process_update(update))
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)
    return {"ok": True}


# --- Compatibility re-exports (refactor step 1.6 removes this block) ----------
# Tests still reach these through `main`; they move to the new module paths in
# one mechanical commit once every slice is out of this file.
from bot.inline import INLINE_MAX_PHOTOS, INLINE_PERSONAL_CACHE_TIME  # noqa: E402, F401
from bot.keyboards.page import page_keyboard  # noqa: E402, F401
from bot.keyboards.reciter import RECITER_PAGE_SIZE, reciter_page_count  # noqa: E402, F401
from bot.limits import REPEAT_COUNT  # noqa: E402, F401
from bot.text import reference as _reference  # noqa: E402, F401
from domain.parsing import as_int as _as_int  # noqa: E402, F401
from domain.parsing import parse_ayah  # noqa: E402, F401
from infra.audio import download_combined_audio as _download_combined_audio  # noqa: E402, F401
