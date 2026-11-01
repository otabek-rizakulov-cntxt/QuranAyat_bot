"""Keeps the channel seam honest (MULTI_PLATFORM_PLAN P3.5).

Every feature that serves WhatsApp sends through `ctx.channel`. What may still
speak Telegram directly is a short, named list — Telegram-only by design — and
this test fails the moment anything else starts to.
"""

import os
import re

SRC = os.path.join(os.path.dirname(__file__), "..", "src", "bot")

# Modules allowed to import python-telegram-bot, and why.
TELEGRAM_MODULES = {
    "dispatch.py": "parses Telegram updates into Incoming",
    "inline.py": "inline mode exists only on Telegram",
    "features/group.py": "hifz groups live in Telegram supergroups (forum topics, members)",
    "keyboards/time_pickers.py": "offset_keyboard: the Telegram wrapper the group setup uses",
    "miniapp.py": "the chat menu button",
    "router.py": "exception types only",
    "handlers/settings.py": "ReplyKeyboardRemove for pre-inline Telegram users",
    "handlers/info.py": "ReplyKeyboardRemove for pre-inline Telegram users",
}
# Modules allowed to read the Telegram client off the context.
CTX_BOT_MODULES = {"features/group.py"}


def _modules():
    for dirpath, _, names in os.walk(SRC):
        for name in names:
            if name.endswith(".py"):
                path = os.path.join(dirpath, name)
                rel = os.path.relpath(path, SRC).replace(os.sep, "/")
                with open(path, encoding="utf-8") as f:
                    yield rel, f.read()


def test_only_telegram_only_modules_import_telegram():
    importing = {
        rel
        for rel, source in _modules()
        if re.search(r"^(from telegram\b|import telegram\b)", source, re.M)
    }
    assert importing <= set(TELEGRAM_MODULES), sorted(importing - set(TELEGRAM_MODULES))


def test_only_group_code_reads_the_telegram_client():
    reading = {rel for rel, source in _modules() if re.search(r"\bctx\.bot\b", source)}
    assert reading <= CTX_BOT_MODULES, sorted(reading - CTX_BOT_MODULES)


def test_nothing_builds_telegram_markup_by_hand_outside_those_modules():
    building = {
        rel for rel, source in _modules() if re.search(r"InlineKeyboard(Markup|Button)\(", source)
    }
    assert building <= set(TELEGRAM_MODULES), sorted(building - set(TELEGRAM_MODULES))
