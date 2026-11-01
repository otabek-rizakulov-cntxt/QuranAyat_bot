"""One-time sign-in links into the Mini App, for platforms without Telegram's
initData (docs/MULTI_PLATFORM_PLAN.md P5.1).

Telegram opens the Mini App with signed `initData`; WhatsApp and a plain browser
have nothing like it. So the bot hands the user a link carrying a token that
names them, and `POST /api/v1/auth/link` exchanges it for the same access token
the Telegram flow returns. The token is:

  * **short-lived** (10 minutes): it travels in a URL, so it may sit in history;
  * **single-use**: its nonce is burned (Redis SET NX) on the first exchange;
  * **unmistakable for an access token**: signed with a key derived from the Mini
    App secret for this purpose only, in a format `decode_token` never accepts.

Format: base64url(JSON payload) "." base64url(HMAC-SHA256 signature).
"""

import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Optional

from config.settings import get_settings
from infra.redis_client import RedisSingleton

LINK_TTL = 10 * 60


class InvalidLinkToken(ValueError):
    """A link token is malformed, forged, expired or already used."""


def _key(secret: str) -> bytes:
    # A separate key per purpose: a link signature can never verify as anything else.
    return hmac.new(secret.encode(), b"miniapp-link-token", hashlib.sha256).digest()


def _b64(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def _unb64(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def _secret() -> Optional[str]:
    return get_settings().miniapp_jwt_secret or None


def issue(user_id: int, now: Optional[float] = None, ttl: int = LINK_TTL) -> Optional[str]:
    """A link token for `user_id`, or None when the Mini App API is not configured."""
    secret = _secret()
    if not secret:
        return None
    issued = int(time.time() if now is None else now)
    payload = {"sub": str(user_id), "exp": issued + ttl, "jti": secrets.token_urlsafe(16)}
    body = _b64(json.dumps(payload, separators=(",", ":")).encode())
    return body + "." + _b64(hmac.new(_key(secret), body.encode(), hashlib.sha256).digest())


def redeem(token: str, now: Optional[float] = None) -> int:
    """The user id a valid, unused token names — and burn it. Raises InvalidLinkToken."""
    secret = _secret()
    if not secret:
        raise InvalidLinkToken("not configured")
    try:
        body, signature = token.split(".")
    except (AttributeError, ValueError):
        raise InvalidLinkToken("malformed")
    expected = _b64(hmac.new(_key(secret), body.encode(), hashlib.sha256).digest())
    if not hmac.compare_digest(expected, signature):
        raise InvalidLinkToken("bad signature")
    try:
        payload = json.loads(_unb64(body))
        user_id, exp, jti = int(payload["sub"]), int(payload["exp"]), str(payload["jti"])
    except (KeyError, ValueError, TypeError):
        raise InvalidLinkToken("malformed claims")
    current = time.time() if now is None else now
    if current >= exp:
        raise InvalidLinkToken("expired")
    remaining = max(1, int(exp - current))
    if not RedisSingleton().connection.set("link:used:" + jti, "1", ex=remaining, nx=True):
        raise InvalidLinkToken("already used")
    return user_id
