"""GET/POST /whatsapp/webhook — where Meta delivers WhatsApp messages (P2.1).

Mounted only when WhatsApp is fully configured (`Settings.whatsapp_ready`).

  * GET is Meta's one-time subscription handshake: echo `hub.challenge` when
    `hub.verify_token` matches ours.
  * POST carries messages and delivery statuses. Each is signed with the app
    secret (`X-Hub-Signature-256: sha256=<hex HMAC of the raw body>`); anything
    unsigned or mis-signed is refused before it is parsed. A valid delivery is
    acknowledged at once and processed in the background — Meta retries a slow
    webhook, and a retry must not become a second reply, so every message id is
    claimed once (Redis SET NX) before it is handled.
"""

import hashlib
import hmac
import logging

import ujson as json
from fastapi import APIRouter, Request, Response

from app.state import AppState
from app.tasks import spawn
from bot.whatsapp import handle_message
from config.settings import get_settings
from infra.redis_client import RedisSingleton

logger = logging.getLogger(__name__)

WHATSAPP_PATH = "/whatsapp/webhook"
SIGNATURE_HEADER = "X-Hub-Signature-256"
DEDUPE_TTL_SECONDS = 24 * 60 * 60

router = APIRouter()


def signature(body: bytes, secret: str) -> str:
    """The `X-Hub-Signature-256` value Meta sends for `body`."""
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def _first_delivery(message_id: str) -> bool:
    """Claim a message id; False if it was already claimed (a Meta retry)."""
    if not message_id:
        return True
    claimed = RedisSingleton().connection.set(
        "wa:seen:" + message_id, "1", ex=DEDUPE_TTL_SECONDS, nx=True
    )
    return bool(claimed)


def messages_of(payload: dict):
    """Every inbound message in a webhook payload; statuses are skipped."""
    for entry in payload.get("entry") or []:
        for change in entry.get("changes") or []:
            value = change.get("value") or {}
            yield from value.get("messages") or []


@router.get(WHATSAPP_PATH)
async def verify(request: Request):
    params = request.query_params
    expected = get_settings().whatsapp_verify_token or ""
    given = params.get("hub.verify_token", "")
    if params.get("hub.mode") == "subscribe" and expected and hmac.compare_digest(given, expected):
        return Response(content=params.get("hub.challenge", ""), media_type="text/plain")
    return Response(status_code=403)


async def _process(state: AppState, message: dict) -> None:
    try:
        await handle_message(state.whatsapp, state.data, message, bot=state.bot)
    except Exception as e:
        logger.error("Error handling WhatsApp message: %s: %s", type(e).__name__, e)


@router.post(WHATSAPP_PATH)
async def receive(request: Request):
    body = await request.body()
    secret = get_settings().whatsapp_app_secret or ""
    given = request.headers.get(SIGNATURE_HEADER, "")
    if not secret or not hmac.compare_digest(given, signature(body, secret)):
        return Response(status_code=401)

    state: AppState = request.app.state.runtime
    if state.whatsapp is None or state.data is None:
        # still initializing — ack so Meta does not retry-flood; the user can resend
        logger.warning("WhatsApp webhook hit before init finished; acking without processing")
        return {"ok": True}

    try:
        payload = json.loads(body)
    except ValueError:
        return Response(status_code=400)
    for message in messages_of(payload):
        if _first_delivery(message.get("id", "")):
            spawn(_process(state, message))
    return {"ok": True}
