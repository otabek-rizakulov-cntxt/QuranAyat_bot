"""Routing one Telegram update to what handles it.

Phase 3 of docs/REFACTOR_PLAN.md replaces the hand-written chains below with
the decorator registry the hifz features already use.
"""

import logging
from time import time

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

import hifz
from bot.errors import ignore_not_modified
from bot.inline import answer_inline_query
from bot.keyboards.language import language_keyboard, translation_language_keyboard
from bot.keyboards.reciter import (
    reciter_keyboard,
    reciter_label,
    reciter_page_of,
    reciter_set_confirmation,
)
from bot.keyboards.rows import button_rows
from bot.keyboards.sajda import sajda_keyboard
from bot.keyboards.verse import TYPE_BY_CODE, verse_keyboard
from bot.limits import MAX_RANGE_AYAHS
from bot.media import (
    send_combined_audio,
    send_page,
    send_page_audio,
    send_quran,
    send_repeated_audio,
)
from bot.settings import resolve_settings
from bot.text import build_verse_text
from domain.parsing import as_int, parse_ayah_range
from lib.miniapp import app_row
from lib.user_settings import UserSettings
from lib.utils import File
from locales import button_action, get_language, normalize_lang, t, welcome_text
from modules import Quran

logger = logging.getLogger(__name__)


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
            with ignore_not_modified():  # swap the keyboard, don't post a new list
                await bot.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=cq.message.message_id,
                    reply_markup=reciter_keyboard(ui_lang, kind, int(page_s), current=reciter),
                )
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
                    # the common path: turn the page in place; re-tapping the
                    # current view yields an identical message, which is fine
                    with ignore_not_modified():
                        await bot.edit_message_text(
                            text=text,
                            chat_id=chat_id,
                            message_id=msg.message_id,
                            parse_mode="HTML",
                            reply_markup=markup,
                        )
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
        rows = button_rows(
            [
                InlineKeyboardButton(reciter_label(p), callback_data="setreciter:" + p["subfolder"])
                for p in matches
            ],
            2,
        )
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
