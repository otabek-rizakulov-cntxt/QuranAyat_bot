# Mini App authentication (docs/MINI_APP_PLAN.md §4).
#
# Two primitives and one dependency:
#
#   * `validate_init_data` — checks the `Telegram.WebApp.initData` query string
#     the Mini App was opened with, using the bot token we already hold
#     (HMAC-SHA256 with key HMAC("WebAppData", token)). This is the only place
#     a user id enters the API.
#   * `issue_token` / `decode_token` — a minimal HS256 JWT. Hand-rolled rather
#     than a new dependency: we only ever produce and accept one fixed header,
#     so the general-purpose parts of a JWT library (alg negotiation, key sets)
#     are attack surface we would never use.
#   * `require_user` — the FastAPI dependency every `/me/*` route takes. The
#     user id comes from the verified token's `sub` and nowhere else.
#
# No refresh tokens: re-exchanging the still-valid initData *is* the refresh.

import base64
import hashlib
import hmac
import json
import os
import time
from typing import Optional
from urllib.parse import parse_qsl, urlencode

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import Environment

DEFAULT_INIT_DATA_MAX_AGE = 24 * 3600  # seconds an initData stays exchangeable
DEFAULT_TOKEN_TTL = 3600  # seconds an access token lives

_JWT_HEADER = {"alg": "HS256", "typ": "JWT"}


class InvalidInitData(ValueError):
    """initData failed validation. The message is safe to log, never to echo
    back with the payload — it names the check that failed, nothing more."""


class InvalidToken(ValueError):
    """An access token is malformed, forged or expired."""


# ---------------------------------------------------------------------------
# initData
# ---------------------------------------------------------------------------


def _init_data_secret(bot_token: str) -> bytes:
    return hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()


def sign_init_data(fields: dict, bot_token: str) -> str:
    """Build a signed initData query string from `fields` — what Telegram does
    when it opens the Mini App. Production never calls this; tests and local
    tooling use it to produce known-good vectors."""
    data_check_string = "\n".join("%s=%s" % (k, fields[k]) for k in sorted(fields))
    digest = hmac.new(
        _init_data_secret(bot_token), data_check_string.encode(), hashlib.sha256
    ).hexdigest()
    return urlencode({**fields, "hash": digest})


def validate_init_data(
    init_data: str,
    bot_token: str,
    max_age: int = DEFAULT_INIT_DATA_MAX_AGE,
    now: Optional[float] = None,
) -> dict:
    """Verify `init_data` and return its fields, with `user` decoded from JSON.

    Raises InvalidInitData on a missing/forged hash, a missing or stale
    `auth_date`, or a missing `user`. The comparison is constant-time.
    """
    if not init_data or not bot_token:
        raise InvalidInitData("empty initData or bot token")

    # keep_blank_values: an empty field is still part of the signed string.
    pairs = parse_qsl(init_data, keep_blank_values=True, strict_parsing=False)
    fields = {}
    for key, value in pairs:
        if key in fields:
            raise InvalidInitData("duplicate field")
        fields[key] = value

    received_hash = fields.pop("hash", None)
    if not received_hash:
        raise InvalidInitData("missing hash")

    data_check_string = "\n".join("%s=%s" % (k, fields[k]) for k in sorted(fields))
    expected = hmac.new(
        _init_data_secret(bot_token), data_check_string.encode(), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected, received_hash):
        raise InvalidInitData("hash mismatch")

    try:
        auth_date = int(fields["auth_date"])
    except (KeyError, ValueError):
        raise InvalidInitData("missing or malformed auth_date")
    current = time.time() if now is None else now
    if current - auth_date > max_age:
        raise InvalidInitData("initData expired")

    try:
        user = json.loads(fields["user"])
        int(user["id"])
    except (KeyError, ValueError, TypeError):
        raise InvalidInitData("missing or malformed user")

    fields["user"] = user
    fields["auth_date"] = auth_date
    return fields


# ---------------------------------------------------------------------------
# Access token (HS256 JWT)
# ---------------------------------------------------------------------------


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def _b64url_decode(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def _sign(signing_input: str, secret: str) -> str:
    return _b64url(hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest())


def issue_token(
    user_id: int, secret: str, ttl: int = DEFAULT_TOKEN_TTL, now: Optional[float] = None
) -> str:
    issued = int(time.time() if now is None else now)
    payload = {"sub": str(user_id), "iat": issued, "exp": issued + ttl}
    signing_input = "%s.%s" % (
        _b64url(json.dumps(_JWT_HEADER, separators=(",", ":")).encode()),
        _b64url(json.dumps(payload, separators=(",", ":")).encode()),
    )
    return "%s.%s" % (signing_input, _sign(signing_input, secret))


def decode_token(token: str, secret: str, now: Optional[float] = None) -> int:
    """Return the user id in a valid token; raise InvalidToken otherwise."""
    try:
        header_b64, payload_b64, signature = token.split(".")
    except (AttributeError, ValueError):
        raise InvalidToken("malformed token")

    # Signature first, then parse: nothing from an unverified token is trusted,
    # including its claim about which algorithm signed it.
    if not hmac.compare_digest(_sign("%s.%s" % (header_b64, payload_b64), secret), signature):
        raise InvalidToken("bad signature")
    try:
        header = json.loads(_b64url_decode(header_b64))
        payload = json.loads(_b64url_decode(payload_b64))
        user_id = int(payload["sub"])
        exp = int(payload["exp"])
    except (KeyError, ValueError, TypeError):
        raise InvalidToken("malformed claims")
    if header != _JWT_HEADER:
        raise InvalidToken("unexpected header")
    if (time.time() if now is None else now) >= exp:
        raise InvalidToken("token expired")
    return user_id


# ---------------------------------------------------------------------------
# Configuration + FastAPI dependency
# ---------------------------------------------------------------------------


def jwt_secret() -> Optional[str]:
    return Environment.get_env("miniapp_jwt_secret") or None


def init_data_max_age() -> int:
    raw = os.getenv("MINIAPP_INIT_DATA_MAX_AGE")
    try:
        return int(raw) if raw else DEFAULT_INIT_DATA_MAX_AGE
    except ValueError:
        return DEFAULT_INIT_DATA_MAX_AGE


_bearer = HTTPBearer(auto_error=False)


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def require_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
) -> int:
    """The authenticated Telegram user id, from the bearer token only."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized("missing bearer token")
    secret = jwt_secret()
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="mini app auth is not configured",
        )
    try:
        return decode_token(credentials.credentials, secret)
    except InvalidToken:
        raise _unauthorized("invalid or expired token")
