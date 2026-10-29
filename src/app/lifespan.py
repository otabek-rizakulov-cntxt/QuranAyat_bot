"""Startup and shutdown.

Startup returns at once and does the heavy work (corpora parsing, store and
cache connections, webhook and menu registration, the scheduler) in a
background task, so the server answers health checks straight away.
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager

from telegram import BotCommand

from app.routes.webhook import WEBHOOK_PATH, webhook_secret
from app.state import AppState
from app.tasks import spawn
from bot import features
from bot.inline import get_default_query_results
from bot.miniapp import set_menu_button
from config.settings import get_settings
from domain.quran import Quran, TranslationRegistry, make_index
from infra.postgres import close_pool
from infra.redis_client import RedisSingleton, cache_backend
from infra.store import apply_schema
from infra.telegram import create_bot
from locales import BOT_COMMANDS, DEFAULT_LANG, UI_LANGUAGES, t

logger = logging.getLogger(__name__)


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


async def initialize(state: AppState) -> None:
    """Heavy init (bot, corpora parsing, webhook registration) done OFF the startup path.

    Parsing the Quran translation + tafsir is CPU-bound and slow on small free instances;
    if it ran inside the startup event, uvicorn wouldn't accept connections until it finished
    and the platform's health check would fail the deploy. So we return from startup immediately
    and do this in the background — the server listens right away and answers `/`.
    """
    bot = data = None

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
        state.bot = bot = create_bot(get_settings())
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
        state.data = data = await asyncio.to_thread(build_data)
        logger.info("Corpora loaded; bot is ready")
    except Exception as e:
        logger.error("INIT ERROR (build_data — check corpus files): %s: %s", type(e).__name__, e)

    webhook_base = get_settings().webhook_base_url
    if bot and webhook_base:
        try:
            await bot.set_webhook(url=webhook_base + WEBHOOK_PATH, secret_token=webhook_secret())
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

    # Register the hifz features (src/bot/features/*.py). Discovery is lazy, so this is
    # where they load at boot rather than on the first update.
    try:
        features.load_features()
    except Exception as e:
        logger.error("INIT ERROR (hifz features): %s: %s", type(e).__name__, e)

    # --- SCHEDULER SLOT (Wave 1D) ---------------------------------------------
    # The due-queue loop. It goes last because it needs `bot` and `data`
    # populated and the schema applied — and after features.load_features(), because
    # that import is what registers the per-kind send handlers it dispatches to.
    #
    # The loop owns its own error handling (a failing tick is logged and the loop
    # continues), so the only thing that can land here is a failure to *start* it.
    # It is stopped by cancellation when uvicorn tears the event loop down.
    try:
        from infra.scheduler import run_scheduler

        spawn(run_scheduler(bot, data))
    except Exception as e:
        logger.error("INIT ERROR (scheduler): %s: %s", type(e).__name__, e)


@asynccontextmanager
async def lifespan(app):
    """Kick off the heavy startup in the background and return immediately, so
    the HTTP server starts listening and passes health checks without waiting
    on corpora parsing; on the way out, unregister the webhook and close the pool."""
    state: AppState = app.state.runtime
    spawn(initialize(state))
    logger.info("Startup returned — HTTP server is listening")
    yield
    if state.bot is not None:
        try:
            await state.bot.delete_webhook()
        except Exception as e:
            logger.error("Shutdown: delete_webhook failed: %s: %s", type(e).__name__, e)
    try:
        await close_pool()
    except Exception as e:
        logger.error("Shutdown: close_pool failed: %s: %s", type(e).__name__, e)
