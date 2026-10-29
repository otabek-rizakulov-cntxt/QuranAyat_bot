# The hifz feature package: one module per memorization feature (profile,
# progress, memorize, check, streak, leaderboard, group).
#
# Adding a feature is: create `src/bot/features/<feature>.py` and decorate its handlers.
# The router (bot/router.py) discovers every module here by walking the
# directory, so there is no shared import list and two features never edit the
# same line:
#
#     from hifz import Ctx, callback, command, wizard
#
# This module re-exports the router's API under the names the features and
# tests have always used, and owns the callback-prefix table below. Feature
# modules take what they send from `bot.media` and friends — never from `main`,
# which tests/test_layering.py enforces.
from typing import Dict

from bot.context import Ctx
from bot.router import (
    CALLBACKS,
    COMMANDS,
    WIZARDS,
    callback,
    command,
    dispatch_callback,
    dispatch_command,
    dispatch_wizard,
    handles,
    handles_callback,
    has_wizard,
    load_features,
    registered,
    reset_for_tests,
    wizard,
)

__all__ = [
    "Ctx",
    "COMMANDS",
    "CALLBACKS",
    "WIZARDS",
    "PREFIXES",
    "command",
    "callback",
    "wizard",
    "handles",
    "handles_callback",
    "has_wizard",
    "dispatch_command",
    "dispatch_callback",
    "dispatch_wizard",
    "load_features",
    "registered",
    "reset_for_tests",
]


# --- Callback-data namespace ---------------------------------------------------
# Telegram caps callback_data at 64 bytes (see bot.keyboards.verse.TYPE_BY_CODE
# for the same constraint on the reader), so prefixes are two letters and payloads are numbers.
# One prefix per feature module, allocated here so parallel work cannot collide.
# The reader's own prefixes are whatever bot/handlers/ registers; the router
# refuses any prefix that overlaps one another module owns, so nothing below can
# shadow them.
PREFIXES: Dict[str, str] = {
    "profile": "hp:",  # hp:name  hp:board:on  hp:tz  hp:tz:+05:00  hp:rem
    "progress": "hg:",  # hg:surah:67  hg:juz:30  hg:forget:...
    "memorize": "hm:",  # hm:t:surah  hm:pace:5  hm:days:daily  hm:ok  hm:know
    "check": "hc:",  # hc:a:<option>  hc:start
    "streak": "hs:",  # hs:grid
    "leaderboard": "hl:",  # hl:me  hl:join
    "group": "gr:",  # gr:tl:ru  gr:rc:...  gr:ok — Phase 2 group setup
    "shared": "hx:",  # hx:cancel  hx:back — the seam's own controls
}


# --- The handler context -------------------------------------------------------


# --- The registries ------------------------------------------------------------
# Populated by the decorators as feature modules are imported by load_features().


# --- Feature discovery ---------------------------------------------------------


# --- Cheap gates ---------------------------------------------------------------
# main.py asks these before building a Ctx, so an update that has nothing to do
# with hifz never touches the store.


# --- Dispatch ------------------------------------------------------------------


# --- The shared /cancel --------------------------------------------------------
# Registered by load_features(), not by a decorator here, so that clearing the
# registries in a test and re-discovering brings it back. It lives in the seam
# rather than in a feature module because every wizard needs the same way out,
# and a feature that owned it would make itself a dependency of the others.
