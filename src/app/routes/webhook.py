"""POST /webhook — where Telegram delivers updates.

Telegram proves each delivery is genuine with the secret we gave it in
set_webhook, sent back in the X-Telegram-Bot-Api-Secret-Token header. The bot
token used to sit in the URL path instead (/webhook/<token>), which put it in
every access-log line.
"""

import hashlib
import hmac
import logging
from typing import Optional

import telegram
from fastapi import APIRouter, Request, Response

from app.state import AppState
from app.tasks import spawn
from bot.dispatch import handle_update
from config import Environment

logger = logging.getLogger(__name__)


async def _process_update(state: AppState, update: telegram.Update) -> None:
    try:
        await handle_update(state.bot, state.data, update)
    except telegram.error.Forbidden:
        pass  # user has blocked or removed the bot; nothing to do
    except Exception as e:
        logger.error("Error handling update: %s: %s", type(e).__name__, e)


WEBHOOK_PATH = "/webhook"
SECRET_HEADER = "X-Telegram-Bot-Api-Secret-Token"


def webhook_secret() -> Optional[str]:
    """The secret Telegram sends with every update, derived from the bot token.

    Derived rather than configured, so there is no extra secret to provision; a
    one-way hash, so it reveals nothing about the token. 64 hex characters, well
    inside Telegram's 1-256 [A-Za-z0-9_-] limit. None when no token is set.
    """
    token = Environment.get_env("token")
    if not token:
        return None
    return hashlib.sha256(("telegram-webhook:" + token).encode()).hexdigest()


router = APIRouter()


@router.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    expected = webhook_secret()
    given = request.headers.get(SECRET_HEADER, "")
    if not expected or not hmac.compare_digest(given, expected):
        return Response(status_code=401)
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
