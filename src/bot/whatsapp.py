"""Routing a WhatsApp message into the shared dispatcher (MULTI_PLATFORM_PLAN P2.4).

WhatsApp has no slash-command menu, so people type words: `menu`, `reciter`,
`page 255` (in English, Uzbek or Russian) become the commands Telegram users
type, a tapped reply button or list row carries the same `callback_data` a
Telegram button does, and a number answers the last numbered menu. Everything
then goes through `bot.dispatch.handle_incoming`, exactly like a Telegram update.

Only features converted to the channel seam are reachable here: the reader,
the verse of the day and, since Phase 3, the hifz platform (plans, drills,
checks, progress, streak, leaderboard, profile). Hifz *groups* and inline mode
stay Telegram-only and answer "not available on WhatsApp yet".
"""

import logging
from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Optional

from bot.dispatch import handle_incoming
from bot.keyboards.language import language_keyboard
from bot.settings import resolve_settings
from channels import WHATSAPP, Incoming
from channels.whatsapp import WhatsAppChannel
from infra import choice_memory
from infra.store import get_store
from locales import t, welcome_text
from services.user_settings import UserSettings

logger = logging.getLogger(__name__)

# Commands and callback prefixes whose handlers speak through `ctx.channel`.
# Extend these as features are converted (Phase 3 adds the hifz set).
COMMANDS = {
    "start",
    "help",
    "about",
    "index",
    "language",
    "translation",
    "reciter",
    "page",
    "juz",
    "sajda",
    "random",
    "daily",
    # hifz (Phase 3)
    "memorize",
    "progress",
    "check",
    "forgot",
    "streak",
    "leaderboard",
    "profile",
    "cancel",
}
CALLBACK_PREFIXES = (
    "vc:",
    "vr:",
    "rep:",
    "showlang",
    "setlang:",
    "settranslang:",
    "pg:",
    "pgnoop",
    "pga:",
    "recgrp:",
    "recpage_noop",
    "reciter_search",
    "setreciter:",
    "hd:",  # verse of the day
    # hifz (Phase 3): plan wizard, profile, progress, check, streak, leaderboard, shared
    "hm:",
    "hp:",
    "hg:",
    "hc:",
    "hs:",
    "hl:",
    "hx:",
)

# A typed word -> the command it stands for, in English, Uzbek (both scripts)
# and Russian — the languages the WhatsApp strings ship in.
KEYWORDS = {
    "help": ("menu", "help", "start", "menyu", "меню", "yordam", "ёрдам", "помощь"),
    "language": ("language", "til", "тил", "язык"),
    "translation": ("translation", "tarjima", "таржима", "перевод"),
    "reciter": ("reciter", "qori", "қори", "чтец"),
    "page": ("page", "sahifa", "саҳифа", "страница"),
    "juz": ("juz", "pora", "пора", "джуз"),
    "sajda": ("sajda", "сажда", "саджда"),
    "random": ("random", "tasodifiy", "тасодифий", "случайный"),
    "about": ("about",),
    "index": ("index", "suralar", "суралар", "суры"),
    "daily": ("daily", "kunlik", "кунлик", "ежедневно"),
    "memorize": ("memorize", "yodlash", "ёдлаш", "заучивать"),
    "progress": ("progress", "natija", "натижа", "прогресс"),
    "check": ("check", "tekshirish", "текшириш", "проверка"),
    "streak": ("streak", "ketma-ketlik", "кетма-кетлик", "серия"),
    "leaderboard": ("leaderboard", "reyting", "рейтинг"),
    "profile": ("profile", "profil", "профил", "профиль"),
    "cancel": ("cancel", "bekor", "бекор", "отмена"),
}
_COMMAND_BY_WORD = {word: name for name, words in KEYWORDS.items() for word in words}

STOP_WORDS = {"stop", "unsubscribe", "стоп", "отписаться", "toʻxtat", "to'xtat", "тўхтат"}

# Calling code -> interface language, for the very first reply (the user can
# change it with `language`). Longest prefix wins; anything else is English.
_LANG_BY_PREFIX = {
    "998": "uz",
    "992": "tg",
    "994": "az",
    "7": "ru",
    "90": "tr",
    "92": "ur",
    "98": "fa",
    "880": "bn",
    "91": "hi",
    "62": "id",
    "60": "ms",
    "20": "ar",
    "212": "ar",
    "962": "ar",
    "963": "ar",
    "964": "ar",
    "965": "ar",
    "966": "ar",
    "968": "ar",
    "971": "ar",
    "973": "ar",
    "974": "ar",
}


def lang_hint(wa_id: str) -> Optional[str]:
    for size in (3, 2, 1):
        lang = _LANG_BY_PREFIX.get(wa_id[:size])
        if lang:
            return lang
    return None


def as_command(text: str) -> str:
    """`page 255` -> `/page 255` for a known keyword; anything else unchanged."""
    word, _, rest = text.strip().partition(" ")
    name = _COMMAND_BY_WORD.get(word.lower())
    if name is None:
        return text
    return "/" + name + (" " + rest.strip() if rest.strip() else "")


def _allowed_command(text: str) -> bool:
    name = text[1:].split("@", 1)[0].partition(" ")[0].lower()
    return name in COMMANDS


def _tap(message: dict) -> Optional[str]:
    """The `callback_data` behind a tapped reply button, list row or template button."""
    kind = message.get("type")
    if kind == "interactive":
        interactive = message.get("interactive") or {}
        reply = interactive.get("button_reply") or interactive.get("list_reply") or {}
        return reply.get("id")
    if kind == "button":
        return (message.get("button") or {}).get("payload")
    return None


def _now() -> datetime:
    return datetime.now(timezone.utc)


async def handle_message(client, data: dict, message: dict, bot=None, now=None) -> None:
    """Process one inbound WhatsApp message (one entry of a webhook's `messages`)."""
    store = await get_store()
    wa_id = str(message["from"])
    first_contact = await store.identity.get(WHATSAPP, wa_id) is None
    user_id = await store.identity.resolve(WHATSAPP, wa_id)
    await store.identity.touch_inbound(user_id, WHATSAPP, now or _now())
    channel = WhatsAppChannel(client, wa_id, user_id)
    hint = lang_hint(wa_id)
    settings = await resolve_settings(UserSettings(), user_id, user_id, hint)
    ui_lang = settings.ui_lang

    if first_contact:
        await channel.send_text(welcome_text(ui_lang), html=True)
        await channel.send_text(t("wa_welcome_hint", ui_lang), html=True)
        await channel.send_text(t("choose_language", ui_lang), language_keyboard())

    tapped = _tap(message)
    text = (message.get("text") or {}).get("body") if message.get("type") == "text" else None

    if tapped is None and text is not None:
        tapped = choice_memory.pick(user_id, text)

    if tapped is not None:
        if not tapped.startswith(CALLBACK_PREFIXES):
            await channel.send_text(t("wa_not_here", ui_lang))
            return
        incoming = Incoming(
            platform=WHATSAPP,
            external_id=wa_id,
            user_id=user_id,
            chat_id=user_id,
            callback_data=tapped,
            callback_id=message.get("id"),
            message_id=message.get("id"),
            lang_hint=hint,
            # Ctx reads the tapped message off the callback; WhatsApp cannot edit
            # it, so the channel's caps (not this stub) decide that edits resend.
            raw=SimpleNamespace(
                id=message.get("id"),
                data=tapped,
                message=SimpleNamespace(
                    message_id=(message.get("context") or {}).get("id"), photo=None, audio=None
                ),
            ),
        )
        await handle_incoming(channel, data, incoming, bot=bot)
        return

    if text is None:
        if message.get("type") not in ("reaction", "unsupported", "system"):
            await channel.send_text(t("wa_unsupported", ui_lang))
        return

    if text.strip().lower() in STOP_WORDS:
        await opt_out(store, user_id, ui_lang, channel, now or _now())
        return

    command = as_command(text)
    if command.lower().startswith("/start "):
        # A /start payload is a Telegram deep link (group setup, board join).
        command = "/start"
    if first_contact and command.startswith("/help"):
        return  # the welcome above already answered it
    if command.startswith("/") and not _allowed_command(command):
        await channel.send_text(t("wa_not_here", ui_lang))
        return

    incoming = Incoming(
        platform=WHATSAPP,
        external_id=wa_id,
        user_id=user_id,
        chat_id=user_id,
        text=command,
        message_id=message.get("id"),
        lang_hint=hint,
        raw=message,
    )
    await handle_incoming(channel, data, incoming, bot=bot)


async def opt_out(store, user_id: int, ui_lang: str, channel, at: datetime) -> None:
    """STOP: withdraw consent to scheduled pushes, at once (WhatsApp policy)."""
    await store.identity.opt_out(user_id, WHATSAPP, at)
    await store.daily.set_enabled(user_id, False)
    await channel.send_text(t("wa_stopped", ui_lang))
