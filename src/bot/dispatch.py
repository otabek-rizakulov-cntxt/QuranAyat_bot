"""Routing one incoming event to what handles it.

A Telegram update is normalized to a `channels.Incoming` and routed by
`handle_incoming`, the path every platform shares (docs/MULTI_PLATFORM_PLAN.md
P1.3); group membership changes and inline queries stay Telegram-only.

Commands, callback prefixes and wizard steps are registered with the router
(bot/router.py) by the core reader (bot/handlers/) and the hifz features alike;
this module only decides, per update type, which of them gets a turn. For a
text message the order is load-bearing (tests/test_dispatch_order.py):

    command  >  pending reciter search  >  wizard in flight  >  button label / reference
"""

import logging
from time import time

import telegram

from bot import router
from bot.context import Ctx
from bot.features import group as hifz_group
from bot.handlers.reader import read_text
from bot.inline import answer_inline_query
from bot.keyboards.reciter import reciter_search_keyboard
from bot.settings import resolve_settings
from channels import TELEGRAM, Incoming
from channels.telegram import TelegramChannel
from infra import catalog, pending_input
from infra.file_facade import File
from infra.store import get_store
from locales import t
from services.user_settings import UserSettings

logger = logging.getLogger(__name__)


async def handle_update(bot, data: dict, update: telegram.Update) -> None:
    """Process a single Telegram update pushed to the webhook."""
    if update.my_chat_member:  # the bot was added to or removed from a chat
        try:
            await hifz_group.on_my_chat_member(bot, await get_store(), update)
        except telegram.error.Forbidden:
            pass  # no permission to post in that group; nothing to do
        return

    if update.inline_query:
        await answer_inline_query(bot, data, update.inline_query)
        return

    incoming = await _incoming(update)
    if incoming is not None:
        await handle_incoming(TelegramChannel(bot, incoming.chat_id), data, incoming, bot=bot)


async def _incoming(update: telegram.Update):
    """A tap or a text message as a platform-neutral `Incoming`; None for anything else."""
    store = await get_store()
    cq = update.callback_query
    if cq:
        # A card sent through inline mode carries an inline_message_id instead of a
        # message: there is no chat to read legacy state from, and the tapper may
        # never have opened a DM with us at all.
        inline = cq.message is None
        sender = cq.from_user
        return Incoming(
            platform=TELEGRAM,
            external_id=str(sender.id),
            user_id=await store.identity.resolve(TELEGRAM, str(sender.id)),
            chat_id=sender.id if inline else cq.message.chat.id,
            callback_data=cq.data or "",
            callback_id=cq.id,
            message_id=None if inline else cq.message.message_id,
            lang_hint=sender.language_code,
            inline=inline,
            raw=cq,
        )
    message = update.message
    if message and message.text:
        sender = message.from_user
        # a sender-less message (a channel post) is keyed by its chat, as before
        sender_id = sender.id if sender is not None else message.chat.id
        return Incoming(
            platform=TELEGRAM,
            external_id=str(sender_id),
            user_id=await store.identity.resolve(TELEGRAM, str(sender_id)),
            chat_id=message.chat.id,
            text=message.text,
            message_id=message.message_id,
            lang_hint=getattr(sender, "language_code", None),
            raw=message,
        )
    return None


async def handle_incoming(channel, data: dict, incoming: Incoming, bot=None) -> None:
    """Route one normalized event: a tap to its callback handler, text to commands,
    prompts, wizards and the reader. Shared by every platform; `bot` is the
    Telegram client the not-yet-converted hifz handlers still read off `Ctx`."""
    settings = await resolve_settings(
        UserSettings(),
        None if incoming.inline else incoming.chat_id,
        incoming.user_id,
        incoming.lang_hint,
    )
    if incoming.callback_data is not None:
        await _on_callback(channel, bot, data, incoming, settings)
    elif incoming.text:
        await _on_text(channel, bot, data, incoming, settings)


async def _on_callback(channel, bot, data: dict, incoming: Incoming, settings) -> None:
    """A tap on an inline button, routed by its callback_data prefix."""
    ctx = await Ctx.build(
        bot,
        data,
        File(),
        incoming.chat_id,
        incoming.user_id,
        settings,
        callback_query=incoming.raw,
        channel=channel,
        platform=incoming.platform,
    )
    if not await router.dispatch_callback(ctx, incoming.callback_data):
        await channel.answer(incoming.callback_id)  # unknown callback: acknowledge and ignore


async def _on_text(channel, bot, data: dict, incoming: Incoming, settings) -> None:
    chat_id = incoming.chat_id
    raw = incoming.text
    text = raw.lower()
    file = File()
    logger.debug("%d:%.3f:%s" % (chat_id, time(), text.replace("\n", " ")))

    if chat_id < 0:
        # Group *text* is ignored: the group cluster is driven entirely from DM
        # (admin setup, board join) and the scheduler (the daily post), never by
        # reading group chatter. Being added or removed is a my_chat_member update.
        return

    async def ctx(**kwargs) -> Ctx:
        return await Ctx.build(
            bot,
            data,
            file,
            chat_id,
            incoming.user_id,
            settings,
            message=incoming.raw,
            channel=channel,
            platform=incoming.platform,
            **kwargs,
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
        await _search_reciters(channel, raw, settings.ui_lang)
        return

    # A wizard in progress consumes free text — but only after commands, so
    # /cancel and every other command remain an escape hatch.
    if router.has_wizard(incoming.user_id) and await router.dispatch_wizard(await ctx(), raw):
        return

    await read_text(await ctx(), text)


async def _search_reciters(channel, query: str, ui_lang: str) -> None:
    """A name typed after tapping "🔍 Search reciter" — not an ayah reference."""
    matches = catalog.search(query)
    if not matches:
        await channel.send_text(t("reciter_search_no_matches", ui_lang))
        pending_input.expect(channel.chat_id, "reciter_search")  # allow one retry
        return
    await channel.send_text(t("reciter_search_results", ui_lang), reciter_search_keyboard(matches))
