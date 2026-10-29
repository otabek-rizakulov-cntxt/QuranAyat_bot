"""Mini App auth (docs/MINI_APP_PLAN.md §4, task P0.2).

initData validation vectors (valid / tampered / wrong token / expired), the
HS256 access token, and the two routes that exist so far: POST
/api/v1/auth/telegram and GET /api/v1/me. The TestClient is used without its
context manager so the startup lifespan never runs (see test_webhook.py)."""

import base64
import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

import pytest
from fastapi.testclient import TestClient

import main
from api.auth import (
    InvalidInitData,
    InvalidToken,
    decode_token,
    issue_token,
    sign_init_data,
    validate_init_data,
)
from config import Environment

BOT_TOKEN = Environment.get_env("token")
SECRET = "test-jwt-secret-not-real"
USER = {"id": 424242, "first_name": "Amina", "language_code": "ru"}

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def _jwt_secret(monkeypatch):
    monkeypatch.setenv("MINIAPP_JWT_SECRET", SECRET)


def _fields(**overrides) -> dict:
    # `signature` is the Ed25519 third-party signature Telegram has sent since
    # Bot API 8.0; we don't verify it, but it is part of the HMAC'd string.
    fields = {
        "auth_date": str(int(time.time())),
        "query_id": "AAH-test",
        "signature": "dGVzdC1zaWduYXR1cmU",
        "user": json.dumps(USER, separators=(",", ":")),
    }
    fields.update(overrides)
    return fields


# ---------------------------------------------------------------------------
# validate_init_data
# ---------------------------------------------------------------------------


def test_known_good_vector_computed_independently():
    # Spell out Telegram's algorithm here rather than reuse sign_init_data, so a
    # bug shared by the signer and the validator cannot hide itself.
    fields = _fields()
    dcs = "\n".join("%s=%s" % (k, fields[k]) for k in sorted(fields))
    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    digest = hmac.new(secret_key, dcs.encode(), hashlib.sha256).hexdigest()
    init_data = urlencode({**fields, "hash": digest})

    out = validate_init_data(init_data, BOT_TOKEN)
    assert out["user"]["id"] == USER["id"]
    assert out["query_id"] == "AAH-test"
    assert "hash" not in out


def test_tampered_field_is_rejected():
    init_data = sign_init_data(_fields(), BOT_TOKEN)
    forged = init_data.replace("424242", "424243")
    with pytest.raises(InvalidInitData):
        validate_init_data(forged, BOT_TOKEN)


def test_added_field_is_rejected():
    init_data = sign_init_data(_fields(), BOT_TOKEN) + "&start_param=page_1"
    with pytest.raises(InvalidInitData):
        validate_init_data(init_data, BOT_TOKEN)


def test_wrong_bot_token_is_rejected():
    init_data = sign_init_data(_fields(), "999999:SOME-OTHER-BOT")
    with pytest.raises(InvalidInitData):
        validate_init_data(init_data, BOT_TOKEN)


def test_expired_auth_date_is_rejected():
    stale = str(int(time.time()) - 24 * 3600 - 5)
    init_data = sign_init_data(_fields(auth_date=stale), BOT_TOKEN)
    with pytest.raises(InvalidInitData):
        validate_init_data(init_data, BOT_TOKEN)


@pytest.mark.parametrize("init_data", ["", "user=%7B%7D", "auth_date=1&hash=abc"])
def test_garbage_is_rejected(init_data):
    with pytest.raises(InvalidInitData):
        validate_init_data(init_data, BOT_TOKEN)


def test_duplicate_field_is_rejected():
    init_data = sign_init_data(_fields(), BOT_TOKEN) + "&auth_date=1"
    with pytest.raises(InvalidInitData):
        validate_init_data(init_data, BOT_TOKEN)


# ---------------------------------------------------------------------------
# Access token
# ---------------------------------------------------------------------------


def test_token_round_trip():
    assert decode_token(issue_token(7, SECRET), SECRET) == 7


def test_expired_token_is_rejected():
    token = issue_token(7, SECRET, ttl=60, now=time.time() - 120)
    with pytest.raises(InvalidToken):
        decode_token(token, SECRET)


def test_token_signed_with_other_secret_is_rejected():
    with pytest.raises(InvalidToken):
        decode_token(issue_token(7, "another-secret"), SECRET)


def test_token_with_swapped_subject_is_rejected():
    header, payload, sig = issue_token(7, SECRET).split(".")
    claims = json.loads(base64.urlsafe_b64decode(payload + "=="))
    claims["sub"] = "8"
    forged = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b"=").decode()
    with pytest.raises(InvalidToken):
        decode_token("%s.%s.%s" % (header, forged, sig), SECRET)


def test_unsigned_alg_none_token_is_rejected():
    def seg(obj):
        return base64.urlsafe_b64encode(json.dumps(obj).encode()).rstrip(b"=").decode()

    token = "%s.%s." % (
        seg({"alg": "none", "typ": "JWT"}),
        seg({"sub": "7", "exp": int(time.time()) + 60}),
    )
    with pytest.raises(InvalidToken):
        decode_token(token, SECRET)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


def _auth(**overrides):
    return client.post(
        "/api/v1/auth/telegram", json={"init_data": sign_init_data(_fields(**overrides), BOT_TOKEN)}
    )


def test_auth_issues_token_and_seeds_settings_from_language_code():
    response = _auth(start_param="drill_17")
    assert response.status_code == 200
    body = response.json()
    assert body["user"]["id"] == USER["id"]
    assert body["settings"]["ui_lang"] == "ru"
    assert body["settings"]["translation_lang"] == "ru"
    assert body["start_param"] == "drill_17"
    assert body["expires_in"] == 3600
    assert decode_token(body["access_token"], SECRET) == USER["id"]


def test_auth_keeps_existing_settings():
    # A user who already picked a language in the bot keeps it on first app open.
    first = _auth().json()
    second = _auth(user=json.dumps({**USER, "language_code": "ar"})).json()
    assert second["settings"] == first["settings"]


def test_auth_drops_malformed_start_param():
    response = _auth(start_param="../../etc/passwd")
    assert response.status_code == 200
    assert response.json()["start_param"] is None


def test_auth_rejects_tampered_init_data():
    init_data = sign_init_data(_fields(), BOT_TOKEN).replace("Amina", "Bilal")
    response = client.post("/api/v1/auth/telegram", json={"init_data": init_data})
    assert response.status_code == 401


def test_auth_rejects_expired_init_data():
    response = _auth(auth_date=str(int(time.time()) - 3 * 24 * 3600))
    assert response.status_code == 401


def test_auth_unconfigured_answers_503(monkeypatch):
    monkeypatch.delenv("MINIAPP_JWT_SECRET")
    assert _auth().status_code == 503


def test_me_without_token_is_401():
    response = client.get("/api/v1/me")
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_me_with_bad_token_is_401():
    response = client.get("/api/v1/me", headers={"Authorization": "Bearer not.a.token"})
    assert response.status_code == 401


def test_me_with_token_returns_the_tokens_user():
    token = _auth().json()["access_token"]
    response = client.get("/api/v1/me", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == USER["id"]
    assert body["settings"]["ui_lang"] == "ru"
    assert body["profile"]["leaderboard_opt_in"] is False
