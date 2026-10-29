"""Routing one Telegram update to what handles it.

Commands, callback prefixes and wizard steps are registered with the router
(bot/router.py) by the core reader (bot/handlers/) and the hifz features alike;
this module only decides, per update type, which of them gets a turn. For a
text message the order is load-bearing (tests/test_dispatch_order.py):

    command  >  pending reciter search  >  wizard in flight  >  button label / reference
"""

import logging
from time import time

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot import router
from bot.context import Ctx
from bot.handlers.reader import read_text
from bot.inline import answer_inline_query
from bot.keyboards.reciter import reciter_label
from bot.keyboards.rows import button_rows
from bot.settings import resolve_settings
from infra import catalog, pending_input
from lib.user_settings import UserSettings
from lib.utils import File
from locales import t

logger = logging.getLogger(__name__)


async def handle_update(bot, data: dict, update: telegram.Update) -> None:
    """Process a single Telegram update pushed to the webhook."""
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

    if update.callback_query:
        await _on_callback(bot, data, update.callback_query)
        return

    if update.message and update.message.text:
        await _on_text(bot, data, update.message)


async def _on_callback(bot, data: dict, cq) -> None:
    """A tap on an inline button, routed by its callback_data prefix."""
    # A card sent through inline mode carries an inline_message_id instead of a
    # message: there is no chat to read legacy state from, and the tapper may
    # never have opened a DM with us at all.
    from_inline = cq.message is None
    chat_id = cq.from_user.id if from_inline else cq.message.chat.id
    settings = await resolve_settings(
        UserSettings(), None if from_inline else chat_id, cq.from_user
    )
    ctx = await Ctx.build(bot, data, File(), chat_id, cq.from_user.id, settings, callback_query=cq)
    if not await router.dispatch_callback(ctx, cq.data or ""):
        await bot.answer_callback_query(cq.id)  # unknown callback: acknowledge and ignore


async def _on_text(bot, data: dict, message) -> None:
    chat_id = message.chat.id
    raw = message.text
    text = raw.lower()
    file = File()
    settings = await resolve_settings(UserSettings(), chat_id, message.from_user)
    logger.debug("%d:%.3f:%s" % (chat_id, time(), text.replace("\n", " ")))

    if chat_id < 0:
        # Group *text* is ignored: the group cluster is driven entirely from DM
        # (admin setup, board join) and the scheduler (the daily post), never by
        # reading group chatter. Being added or removed is a my_chat_member update.
        return

    async def ctx(**kwargs) -> Ctx:
        return await Ctx.build(
            bot, data, file, chat_id, message.from_user.id, settings, message=message, **kwargs
        )

    if text.startswith("/"):
        # "/page 255" -> ("page", "255"); "/help@BotName" -> "help". A bare
        # reference like "/2:255" matches no command and falls through to the
        # reference parser below.
        name, _, argument = text[1:].split("@", 1)[0].partition(" ")
        # A command always wins over a pending free-text prompt: a /start typed
        # while the bot awaited a reciter name used to be swallowed as the name.
        pending_input.take(chat_id)
        if router.handles(name):
            await router.dispatch_command(await ctx(argument=argument.strip()), name)
            return

    if pending_input.take(chat_id) == "reciter_search":
        await _search_reciters(bot, file, chat_id, raw, settings.ui_lang)
        return

    # A wizard in progress consumes free text — but only after commands, so
    # /cancel and every other command remain an escape hatch.
    if router.has_wizard(message.from_user.id) and await router.dispatch_wizard(await ctx(), raw):
        return

    await read_text(await ctx(), text)


async def _search_reciters(bot, file, chat_id: int, query: str, ui_lang: str) -> None:
    """A name typed after tapping "🔍 Search reciter" — not an ayah reference."""
    matches = catalog.search(query)
    if not matches:
        await bot.send_message(chat_id=chat_id, text=t("reciter_search_no_matches", ui_lang))
        pending_input.expect(chat_id, "reciter_search")  # allow one retry
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
