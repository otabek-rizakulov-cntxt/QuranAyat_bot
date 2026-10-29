"""POST /webhook/{token} — where Telegram delivers updates."""

import logging

import telegram
from fastapi import APIRouter, Request, Response

from app.state import AppState
from app.tasks import spawn
from bot.dispatch import handle_update
from config.settings import get_settings

logger = logging.getLogger(__name__)


async def _process_update(state: AppState, update: telegram.Update) -> None:
    try:
        await handle_update(state.bot, state.data, update)
    except telegram.error.Forbidden:
        pass  # user has blocked or removed the bot; nothing to do
    except Exception as e:
        logger.error("Error handling update: %s: %s", type(e).__name__, e)


router = APIRouter()


@router.post("/webhook/{token}")
async def telegram_webhook(token: str, request: Request):
    if token != get_settings().token:
        return Response(status_code=404)
    state: AppState = request.app.state.runtime
    if state.bot is None or state.data is None:
        # still initializing (corpora parsing) — ack so Telegram doesn't retry-flood
        logger.warning("Webhook hit before init finished; acking without processing")
        return {"ok": True}

    payload = await request.json()
    update = telegram.Update.de_json(payload, state.bot)
    # Ack Telegram immediately and do the (possibly slow) work in the background,
    # so downloading/uploading combined audio doesn't hold the webhook response open.
    spawn(_process_update(state, update))
    return {"ok": True}
