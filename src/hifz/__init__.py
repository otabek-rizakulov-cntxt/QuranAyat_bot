# The hifz seam.
#
# `src/main.py` is a 1400-line module that grew one `elif command == ...` at a
# time. The memorization platform adds seven commands, a dozen callbacks and
# three wizards; bolting those onto the same chain would double the file and make
# every parallel branch a merge conflict. So features live in `src/hifz/`, one
# module per feature, and main.py gains exactly three call sites plus a scheduler
# slot.
#
# **Registration is conflict-free by construction.** A feature module declares
# itself with decorators and is discovered by walking this package's directory —
# there is no shared import list, no registry file, nothing two agents both edit.
# Adding a feature is: create `src/hifz/<feature>.py`, decorate the handlers,
# done.
#
#     from hifz import Ctx, callback, command, wizard
#
#     @command("profile")
#     async def profile(ctx: Ctx) -> None:
#         await ctx.reply(ctx.tr("profile_title"))
#
#     @callback("hp:")                        # matches any "hp:..." callback_data
#     async def on_profile_tap(ctx: Ctx, cb_data: str) -> None:
#         await ctx.answer()
#
#     @wizard("profile_name")                 # the draft's `kind`
#     async def name_step(ctx: Ctx, text: str) -> None:
#         ...
#
# Discovery is *lazy* on purpose: it runs on the first dispatch (and explicitly
# from `_initialize()` at boot), never at `import hifz` time. That means a
# feature module may `from main import send_quran` at the top of the file without
# a circular import, which is the mistake this package would otherwise invite.

import importlib
import pkgutil
import sys
import traceback
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, Optional

import telegram

from lib.wizard import Wizard
from locales import t

__all__ = [
    "Ctx", "COMMANDS", "CALLBACKS", "WIZARDS", "PREFIXES",
    "command", "callback", "wizard",
    "handles", "handles_callback", "has_wizard",
    "dispatch_command", "dispatch_callback", "dispatch_wizard",
    "load_features", "registered",
]


# --- Callback-data namespace ---------------------------------------------------
# Telegram caps callback_data at 64 bytes (see main.TYPE_BY_CODE for the same
# constraint on the reader), so prefixes are two letters and payloads are numbers.
# One prefix per feature module, allocated here so parallel work cannot collide.
# The reader owns "vc:", "vr:", "rep:", "pg:", "pga:", "recgrp:", "setlang:",
# "settranslang:", "setreciter:", "showlang" and "reciter_search"; nothing below
# may shadow those.
PREFIXES: Dict[str, str] = {
    "profile":     "hp:",   # hp:name  hp:board:on  hp:tz  hp:tz:+05:00  hp:rem
    "progress":    "hg:",   # hg:surah:67  hg:juz:30  hg:forget:...
    "memorize":    "hm:",   # hm:t:surah  hm:pace:5  hm:days:daily  hm:ok  hm:know
    "check":       "hc:",   # hc:a:<option>  hc:start
    "streak":      "hs:",   # hs:grid
    "leaderboard": "hl:",   # hl:me  hl:join
    "shared":      "hx:",   # hx:cancel  hx:back — the seam's own controls
}


# --- The handler context -------------------------------------------------------

CommandHandler = Callable[["Ctx"], Awaitable[None]]
CallbackHandler = Callable[["Ctx", str], Awaitable[None]]
WizardHandler = Callable[["Ctx", str], Awaitable[None]]


@dataclass(frozen=True)
class Ctx:
    """Everything a hifz handler needs, assembled once by the seam.

    Frozen: a handler reads its context and writes through `store`, never by
    mutating what it was handed.
    """

    bot: Any                        # telegram.Bot (an AsyncMock under test)
    data: dict                      # the shared corpora dict built by main.build_data
    file: Any                       # lib.utils.File — media cache + nav state
    store: Any                      # lib.store.Store — profiles/hifz/plans/sessions/schedule
    chat_id: int
    user_id: int
    ui_lang: str
    translation_lang: str
    reciter: str
    argument: str = ""              # text after the command: "/check 67" -> "67"
    callback_query: Any = None      # telegram.CallbackQuery, on a callback dispatch
    message: Any = None             # telegram.Message, on a message dispatch

    # --- construction ---------------------------------------------------------

    @classmethod
    async def build(cls, bot, data, file, chat_id: int, user_id: int, settings,
                    **kwargs) -> "Ctx":
        """Build a Ctx from main.py's per-update locals.

        `settings` is the UserSettingsRow-shaped object `_resolve_settings`
        returns. The store is fetched here so no call site has to know that
        storage is a coroutine-guarded singleton.
        """
        from lib.store import get_store
        return cls(bot=bot, data=data, file=file, store=await get_store(),
                   chat_id=chat_id, user_id=user_id,
                   ui_lang=settings.ui_lang,
                   translation_lang=settings.translation_lang,
                   reciter=settings.reciter, **kwargs)

    # --- conveniences ---------------------------------------------------------

    @property
    def wiz(self) -> Wizard:
        """The user's wizard-draft store (see lib/wizard.py)."""
        return Wizard()

    def tr(self, key: str, **fmt: Any) -> str:
        """A localized string in the caller's UI language, formatted.

        `ctx.tr("plan_saved", first_date="2026-08-01")` — placeholders are named,
        and every one is multiplied by 47 translators, so keep them few.
        """
        text = t(key, self.ui_lang)
        return text.format(**fmt) if fmt else text

    async def reply(self, text: str, **kwargs) -> Any:
        """Send a message to the caller's chat."""
        return await self.bot.send_message(chat_id=self.chat_id, text=text, **kwargs)

    async def answer(self, text: str = None, show_alert: bool = False) -> None:
        """Acknowledge the tap, so the client stops spinning. No-op off a callback."""
        if self.callback_query is None:
            return
        if text is None:
            await self.bot.answer_callback_query(self.callback_query.id)
        else:
            await self.bot.answer_callback_query(self.callback_query.id, text=text,
                                                 show_alert=show_alert)

    async def edit(self, text: str, **kwargs) -> bool:
        """Edit the tapped message in place; send a fresh one if that isn't possible.

        Returns True if the message was edited. Re-tapping the view you are
        already in produces an identical message, and Telegram answers "message
        is not modified" — that is a no-op, not an error (same idiom as the verse
        card in main.py).
        """
        msg = getattr(self.callback_query, "message", None)
        if msg is None or msg.photo or msg.audio:
            await self.reply(text, **kwargs)
            return False
        try:
            await self.bot.edit_message_text(text=text, chat_id=self.chat_id,
                                             message_id=msg.message_id, **kwargs)
        except telegram.error.BadRequest as err:
            if "not modified" not in str(err).lower():
                raise
        return True


# --- The registries ------------------------------------------------------------
# Populated by the decorators as feature modules are imported by load_features().

COMMANDS: Dict[str, CommandHandler] = {}
CALLBACKS: Dict[str, CallbackHandler] = {}
WIZARDS: Dict[str, WizardHandler] = {}


def _same_origin(a, b) -> bool:
    """Whether two functions are the same declaration, across a module reload.

    Identity is the obvious test and the wrong one: `importlib.reload` re-executes
    the module body, producing a *new* function object for the same `def`. Under
    identity that reads as a second module claiming the name and raises, which
    would make rediscovery impossible. Module plus qualified name is stable across
    a reload and still distinct between two different features, which is the case
    the guard actually exists to catch.
    """
    return (getattr(a, "__module__", None) == getattr(b, "__module__", None)
            and getattr(a, "__qualname__", None) == getattr(b, "__qualname__", None))


def command(*names: str):
    """Register a slash command. `@command("progress")` claims `/progress`.

    Several names may be given for aliases. Registering a name twice is a
    programming error and raises at import time rather than silently letting one
    module shadow another's command.
    """
    def decorate(handler: CommandHandler) -> CommandHandler:
        for name in names:
            key = name.lstrip("/").lower()
            existing = COMMANDS.get(key)
            if existing is not None and existing is not handler \
                    and not _same_origin(existing, handler):
                raise ValueError("command /%s is already registered by %s"
                                 % (key, getattr(existing, "__module__", "?")))
            COMMANDS[key] = handler
        return handler
    return decorate


def callback(*prefixes: str):
    """Register an inline-button handler for every callback_data with `prefix`.

    Use the prefix allocated to your module in `PREFIXES` — `@callback("hm:")`.
    The handler receives the full callback_data, prefix included, and must parse
    it defensively: callback_data comes off the wire and can be stale, truncated
    or forged.
    """
    def decorate(handler: CallbackHandler) -> CallbackHandler:
        for prefix in prefixes:
            existing = CALLBACKS.get(prefix)
            if existing is not None and existing is not handler \
                    and not _same_origin(existing, handler):
                raise ValueError("callback prefix %r is already registered by %s"
                                 % (prefix, getattr(existing, "__module__", "?")))
            CALLBACKS[prefix] = handler
        return handler
    return decorate


def wizard(*kinds: str):
    """Register the free-text step handler for a wizard `kind`.

    The kind is the one stored in the draft (`ctx.wiz.start(user_id, "plan_pace")`),
    so a module owns its own kinds and never sees another's messages. The handler
    receives the raw (un-lowercased) message text.
    """
    def decorate(handler: WizardHandler) -> WizardHandler:
        for kind in kinds:
            existing = WIZARDS.get(kind)
            if existing is not None and existing is not handler \
                    and not _same_origin(existing, handler):
                raise ValueError("wizard kind %r is already registered by %s"
                                 % (kind, getattr(existing, "__module__", "?")))
            WIZARDS[kind] = handler
        return handler
    return decorate


# --- Feature discovery ---------------------------------------------------------

_loaded = False
_snapshot = None     # the first successful discovery, replayed after a test clears


def load_features(force: bool = False) -> Dict[str, int]:
    """Import every feature module in this package, registering its handlers.

    Walks the package directory rather than reading an import list, so two agents
    adding two features never touch the same line. A module that fails to import
    is reported and skipped: one broken feature must not take the bot down with
    it, and the traceback in the boot log says exactly which one.
    """
    global _loaded, _snapshot
    if _loaded and not force:
        return registered()
    _loaded = True

    # Registration lives in decorators, which run at *import* time, and
    # `import_module` is a no-op for a module already in sys.modules. So once the
    # registries have been cleared — which only a test does — re-running discovery
    # would find every feature already imported and register nothing, silently
    # emptying the bot. Replaying the first load's result fixes that without
    # re-executing anything: reloading would also throw away any monkeypatch a
    # test had applied to a feature module, and handlers resolve their module
    # globals at call time, so the recorded functions see patches just fine.
    if _snapshot is not None and not force:
        COMMANDS.update(_snapshot[0])
        CALLBACKS.update(_snapshot[1])
        WIZARDS.update(_snapshot[2])
        return registered()

    command("cancel")(_cancel)          # the seam's own command (see below)
    for info in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
        if info.name.startswith("_"):
            continue
        try:
            existing = sys.modules.get("%s.%s" % (__name__, info.name))
            if existing is not None:
                importlib.reload(existing)
            else:
                importlib.import_module("." + info.name, __name__)
        except Exception as e:
            print("HIFZ: feature %r failed to load: %s: %s"
                  % (info.name, type(e).__name__, e))
            traceback.print_exc()
    _snapshot = (dict(COMMANDS), dict(CALLBACKS), dict(WIZARDS))
    counts = registered()
    print("HIFZ: %d commands, %d callback prefixes, %d wizards registered"
          % (counts["commands"], counts["callbacks"], counts["wizards"]))
    return counts


def registered() -> Dict[str, int]:
    """How much is registered — for the boot log and for tests."""
    return {"commands": len(COMMANDS), "callbacks": len(CALLBACKS),
            "wizards": len(WIZARDS)}


def reset_for_tests() -> None:
    """Forget every registration and re-run discovery on next dispatch."""
    global _loaded, _snapshot
    COMMANDS.clear()
    CALLBACKS.clear()
    WIZARDS.clear()
    _loaded = False
    _snapshot = None


# --- Cheap gates ---------------------------------------------------------------
# main.py asks these before building a Ctx, so an update that has nothing to do
# with hifz never touches the store.

def handles(command_name: str) -> bool:
    """Whether a hifz feature claims `/command_name`."""
    load_features()
    return command_name.lstrip("/").lower() in COMMANDS


def handles_callback(cb_data: str) -> bool:
    """Whether a hifz feature claims this callback_data."""
    load_features()
    return _match_callback(cb_data) is not None


def has_wizard(user_id: int) -> bool:
    """Whether the user has a draft in flight (so free text may be for it)."""
    return Wizard().is_active(user_id)


def _match_callback(cb_data: str) -> Optional[CallbackHandler]:
    """Longest registered prefix matching `cb_data`, or None.

    Longest-first so "hm:day:" can be split out of "hm:" later without the
    shorter prefix swallowing it.
    """
    if not cb_data:
        return None
    for prefix in sorted(CALLBACKS, key=len, reverse=True):
        if cb_data.startswith(prefix):
            return CALLBACKS[prefix]
    return None


# --- Dispatch ------------------------------------------------------------------

async def dispatch_command(ctx: Ctx, command_name: str) -> bool:
    """Run the handler for `/command_name`. True if a feature handled it."""
    load_features()
    handler = COMMANDS.get(command_name.lstrip("/").lower())
    if handler is None:
        return False
    await handler(ctx)
    return True


async def dispatch_callback(ctx: Ctx, cb_data: str) -> bool:
    """Run the handler whose prefix matches `cb_data`. True if handled.

    Defensive by design: callback_data arrives from the client, may be years old
    (Telegram never expires a keyboard) and may be malformed. A handler that
    raises is logged and the tap is acknowledged anyway, because an unanswered
    callback leaves a spinner on the user's screen forever.
    """
    load_features()
    handler = _match_callback(cb_data)
    if handler is None:
        return False
    try:
        await handler(ctx, cb_data)
    except telegram.error.Forbidden:
        raise                               # user blocked the bot; main.py handles it
    except Exception as e:
        print("HIFZ: callback %r failed: %s: %s" % (cb_data, type(e).__name__, e))
        traceback.print_exc()
        try:
            await ctx.answer()
        except Exception:
            pass
    return True


async def dispatch_wizard(ctx: Ctx, raw_message: str) -> bool:
    """Feed free text to the wizard the user is in. True if it was consumed.

    `/cancel` is handled here rather than by each feature, so every wizard has
    the same escape hatch. Other commands escape by being dispatched *before*
    this slot in main.py — the wizard never sees them.
    """
    load_features()
    draft = ctx.wiz.get(ctx.user_id)
    if draft is None:
        return False
    if Wizard.is_cancel(raw_message):
        ctx.wiz.clear(ctx.user_id)
        await ctx.reply(ctx.tr("wizard_cancelled"))
        return True
    handler = WIZARDS.get(draft["kind"])
    if handler is None:
        # a draft whose feature is gone (renamed kind, failed import): drop it
        # rather than trapping the user in a wizard nothing answers.
        print("HIFZ: no handler for wizard kind %r; dropping the draft" % (draft["kind"],))
        ctx.wiz.clear(ctx.user_id)
        return False
    try:
        await handler(ctx, raw_message)
    except telegram.error.Forbidden:
        raise
    except Exception as e:
        print("HIFZ: wizard %r failed: %s: %s" % (draft["kind"], type(e).__name__, e))
        traceback.print_exc()
        ctx.wiz.clear(ctx.user_id)
        await ctx.reply(ctx.tr("wizard_invalid_input"))
    return True


# --- The shared /cancel --------------------------------------------------------
# Registered by load_features(), not by a decorator here, so that clearing the
# registries in a test and re-discovering brings it back. It lives in the seam
# rather than in a feature module because every wizard needs the same way out,
# and a feature that owned it would make itself a dependency of the others.

async def _cancel(ctx: Ctx) -> None:
    """End whatever wizard is in flight."""
    if ctx.wiz.cancel(ctx.user_id):
        await ctx.reply(ctx.tr("wizard_cancelled"))
    else:
        await ctx.reply(ctx.tr("wizard_nothing_to_cancel"))
