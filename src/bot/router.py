"""The bot's router: commands, callback prefixes and wizard steps, registered
with decorators and dispatched from one place.

A feature module declares itself and is discovered by walking its package —
there is no shared import list, so two features never edit the same line:

    from hifz import Ctx, callback, command, wizard

    @command("profile")
    async def profile(ctx: Ctx) -> None:
        await ctx.reply(ctx.tr("profile_title"))

    @callback("hp:")                        # any callback_data starting "hp:"
    async def on_profile_tap(ctx: Ctx, cb_data: str) -> None:
        await ctx.answer()

    @wizard("profile_name")                 # the wizard draft's `kind`
    async def name_step(ctx: Ctx, text: str) -> None:
        ...

Discovery is lazy: it runs on the first dispatch (and explicitly at boot),
never at import time.
"""

import importlib
import logging
import pkgutil
import sys
from typing import Awaitable, Callable, Dict, Optional

import telegram

from bot.context import Ctx
from lib.wizard import Wizard

logger = logging.getLogger(__name__)

# Packages whose modules register handlers. Discovery imports every module in
# each one whose name does not start with "_".
FEATURE_PACKAGES = ("bot.handlers", "hifz")


CommandHandler = Callable[["Ctx"], Awaitable[None]]


CallbackHandler = Callable[["Ctx", str], Awaitable[None]]


WizardHandler = Callable[["Ctx", str], Awaitable[None]]


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
    return getattr(a, "__module__", None) == getattr(b, "__module__", None) and getattr(
        a, "__qualname__", None
    ) == getattr(b, "__qualname__", None)


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
            if (
                existing is not None
                and existing is not handler
                and not _same_origin(existing, handler)
            ):
                raise ValueError(
                    "command /%s is already registered by %s"
                    % (key, getattr(existing, "__module__", "?"))
                )
            COMMANDS[key] = handler
        return handler

    return decorate


def callback(*prefixes: str):
    """Register an inline-button handler for every callback_data with `prefix`.

    Use the prefix allocated to your module in `hifz.PREFIXES` — `@callback("hm:")`.
    The handler receives the full callback_data, prefix included, and must parse
    it defensively: callback_data comes off the wire and can be stale, truncated
    or forged.

    A prefix may not overlap one another *module* owns ("p" would take every
    "pg:" tap no longer prefix claims). Within one module it may: "hm:day:" can be
    split out of "hm:", and the longer one wins (see `_match_callback`).
    """

    def decorate(handler: CallbackHandler) -> CallbackHandler:
        for prefix in prefixes:
            existing = CALLBACKS.get(prefix)
            if (
                existing is not None
                and existing is not handler
                and not _same_origin(existing, handler)
            ):
                raise ValueError(
                    "callback prefix %r is already registered by %s"
                    % (prefix, getattr(existing, "__module__", "?"))
                )
            module = getattr(handler, "__module__", None)
            for other, owner in CALLBACKS.items():
                overlaps = other != prefix and (
                    other.startswith(prefix) or prefix.startswith(other)
                )
                if overlaps and getattr(owner, "__module__", None) != module:
                    raise ValueError(
                        "callback prefix %r overlaps %r, registered by %s"
                        % (prefix, other, getattr(owner, "__module__", "?"))
                    )
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
            if (
                existing is not None
                and existing is not handler
                and not _same_origin(existing, handler)
            ):
                raise ValueError(
                    "wizard kind %r is already registered by %s"
                    % (kind, getattr(existing, "__module__", "?"))
                )
            WIZARDS[kind] = handler
        return handler

    return decorate


_loaded = False


_snapshot = None  # the first successful discovery, replayed after a test clears


def load_features(force: bool = False) -> Dict[str, int]:
    """Import every module of every feature package, registering its handlers.

    Walks each of FEATURE_PACKAGES rather than reading an import list, so two agents
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

    command("cancel")(_cancel)  # the seam's own command (see below)
    for package_name in FEATURE_PACKAGES:
        package = importlib.import_module(package_name)
        for info in sorted(pkgutil.iter_modules(package.__path__), key=lambda m: m.name):
            if info.name.startswith("_"):
                continue
            name = "%s.%s" % (package_name, info.name)
            try:
                existing = sys.modules.get(name)
                if existing is not None:
                    importlib.reload(existing)
                else:
                    importlib.import_module(name)
            except Exception as e:
                logger.exception(
                    "Router: feature %r failed to load: %s: %s" % (name, type(e).__name__, e)
                )
    _snapshot = (dict(COMMANDS), dict(CALLBACKS), dict(WIZARDS))
    counts = registered()
    logger.info(
        "Router: %d commands, %d callback prefixes, %d wizards registered"
        % (counts["commands"], counts["callbacks"], counts["wizards"])
    )
    return counts


def registered() -> Dict[str, int]:
    """How much is registered — for the boot log and for tests."""
    return {"commands": len(COMMANDS), "callbacks": len(CALLBACKS), "wizards": len(WIZARDS)}


def reset_for_tests() -> None:
    """Forget every registration and re-run discovery on next dispatch."""
    global _loaded, _snapshot
    COMMANDS.clear()
    CALLBACKS.clear()
    WIZARDS.clear()
    _loaded = False
    _snapshot = None


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
        raise  # user blocked the bot; the webhook handles it
    except Exception as e:
        logger.exception("Router: callback %r failed: %s: %s" % (cb_data, type(e).__name__, e))
        try:
            await ctx.answer()
        except Exception:
            pass
    return True


async def dispatch_wizard(ctx: Ctx, raw_message: str) -> bool:
    """Feed free text to the wizard the user is in. True if it was consumed.

    `/cancel` is handled here rather than by each feature, so every wizard has
    the same escape hatch. Other commands escape by being dispatched *before*
    this slot in bot.dispatch — the wizard never sees them.
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
        logger.warning(
            "Router: no handler for wizard kind %r; dropping the draft" % (draft["kind"],)
        )
        ctx.wiz.clear(ctx.user_id)
        return False
    try:
        await handler(ctx, raw_message)
    except telegram.error.Forbidden:
        raise
    except Exception as e:
        logger.exception("Router: wizard %r failed: %s: %s" % (draft["kind"], type(e).__name__, e))
        ctx.wiz.clear(ctx.user_id)
        await ctx.reply(ctx.tr("wizard_invalid_input"))
    return True


async def _cancel(ctx: Ctx) -> None:
    """End whatever wizard is in flight."""
    if ctx.wiz.cancel(ctx.user_id):
        await ctx.reply(ctx.tr("wizard_cancelled"))
    else:
        await ctx.reply(ctx.tr("wizard_nothing_to_cancel"))
