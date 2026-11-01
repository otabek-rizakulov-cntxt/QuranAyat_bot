"""POST/GET /whatsapp/webhook against recorded payloads (MULTI_PLATFORM_PLAN P2.1).

Like tests/test_webhook.py, the TestClient runs without its context manager, so
startup never runs; the runtime state is filled in by hand, and the background
`spawn` is replaced by a list so the test sees exactly what would be processed.
"""

import json
import os

import pytest
from fastapi.testclient import TestClient

import app.routes.whatsapp as route
from app.factory import create_app
from app.routes.whatsapp import SIGNATURE_HEADER, WHATSAPP_PATH, signature

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures", "whatsapp")
SECRET = "app-secret"
ENV = {
    "WHATSAPP_ENABLED": "1",
    "WHATSAPP_PHONE_NUMBER_ID": "PHONE",
    "WHATSAPP_ACCESS_TOKEN": "TOKEN",
    "WHATSAPP_APP_SECRET": SECRET,
    "WHATSAPP_VERIFY_TOKEN": "verify-me",
}


def fixture(name) -> bytes:
    with open(os.path.join(FIXTURES, name + ".json"), "rb") as f:
        return f.read()


@pytest.fixture
def handled(monkeypatch):
    """Messages that reached the router, in order."""
    seen = []

    async def fake_handle(client, data, message, bot=None):
        seen.append(message)

    monkeypatch.setattr(route, "handle_message", fake_handle)

    def run_now(coro):
        # drive the background task to completion inline
        try:
            coro.send(None)
        except StopIteration:
            pass

    monkeypatch.setattr(route, "spawn", run_now)
    return seen


@pytest.fixture
def client(monkeypatch, handled):
    for name, value in ENV.items():
        monkeypatch.setenv(name, value)
    app = create_app()
    app.state.runtime.whatsapp = object()
    app.state.runtime.data = {}
    return TestClient(app)


def post(client, body: bytes, sign=True, secret=SECRET):
    headers = {"Content-Type": "application/json"}
    if sign:
        headers[SIGNATURE_HEADER] = signature(body, secret)
    return client.post(WHATSAPP_PATH, content=body, headers=headers)


class TestHandshake:
    def test_echoes_the_challenge(self, client):
        response = client.get(
            WHATSAPP_PATH,
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "verify-me",
                "hub.challenge": "42",
            },
        )
        assert response.status_code == 200 and response.text == "42"

    @pytest.mark.parametrize(
        "params",
        [
            {"hub.mode": "subscribe", "hub.verify_token": "wrong", "hub.challenge": "42"},
            {"hub.mode": "unsubscribe", "hub.verify_token": "verify-me", "hub.challenge": "42"},
            {},
        ],
    )
    def test_refuses_anything_else(self, client, params):
        assert client.get(WHATSAPP_PATH, params=params).status_code == 403


class TestSignature:
    def test_unsigned_is_refused(self, client, handled):
        assert post(client, fixture("text"), sign=False).status_code == 401
        assert handled == []

    def test_forged_is_refused(self, client, handled):
        assert post(client, fixture("text"), secret="not-the-secret").status_code == 401
        assert handled == []

    def test_a_signed_body_altered_in_transit_is_refused(self, client, handled):
        body = fixture("text")
        headers = {SIGNATURE_HEADER: signature(body, SECRET)}
        tampered = body.replace(b"2:255", b"9:999")
        assert client.post(WHATSAPP_PATH, content=tampered, headers=headers).status_code == 401
        assert handled == []


class TestDelivery:
    def test_a_message_reaches_the_router(self, client, handled):
        response = post(client, fixture("text"))
        assert response.status_code == 200 and response.json() == {"ok": True}
        assert [m["text"]["body"] for m in handled] == ["2:255"]

    def test_a_retry_is_processed_once(self, client, handled):
        post(client, fixture("text"))
        post(client, fixture("text"))
        assert len(handled) == 1

    def test_statuses_are_ignored(self, client, handled):
        assert post(client, fixture("status")).status_code == 200
        assert handled == []

    def test_every_message_in_a_batch(self, client, handled):
        post(client, fixture("two_messages"))
        assert [m["id"] for m in handled] == ["wamid.A", "wamid.B"]

    def test_acks_before_initialization(self, client, handled):
        client.app.state.runtime.data = None
        assert post(client, fixture("text")).status_code == 200
        assert handled == []

    def test_malformed_json(self, client):
        assert post(client, b"{not json").status_code == 400

    @pytest.mark.parametrize("name", ["text", "button_reply", "list_reply", "image", "status"])
    def test_fixtures_are_valid_payloads(self, name):
        payload = json.loads(fixture(name))
        assert payload["object"] == "whatsapp_business_account"


def test_not_mounted_unless_configured(monkeypatch):
    for name in ENV:
        monkeypatch.delenv(name, raising=False)
    plain = TestClient(create_app())
    assert plain.get(WHATSAPP_PATH).status_code == 404
    assert plain.post(WHATSAPP_PATH, content=b"{}").status_code == 404
