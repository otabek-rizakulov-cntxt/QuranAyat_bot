"""One-time sign-in links into the Mini App (MULTI_PLATFORM_PLAN P5.1).

The TestClient runs without its context manager, as in tests/test_api_auth.py.
"""

import json
import time

import httpx
import pytest
from fastapi.testclient import TestClient

import channels.whatsapp as wa
import main
from api.auth import issue_token
from bot.whatsapp import handle_message
from channels.whatsapp import GraphClient
from infra import link_token
from infra.link_token import InvalidLinkToken

SECRET = "test-jwt-secret-not-real"
APP = "https://app.example.org"
WA_USER = 2**52 + 5
client = TestClient(main.app)


@pytest.fixture(autouse=True)
def configured(monkeypatch):
    monkeypatch.setenv("MINIAPP_JWT_SECRET", SECRET)
    monkeypatch.setenv("MINIAPP_URL", APP)


def exchange(token):
    return client.post("/api/v1/auth/link", json={"token": token})


class TestToken:
    def test_off_without_a_secret(self, monkeypatch):
        monkeypatch.delenv("MINIAPP_JWT_SECRET")
        assert link_token.issue(WA_USER) is None
        with pytest.raises(InvalidLinkToken):
            link_token.redeem("x.y")

    def test_round_trip_once(self):
        token = link_token.issue(WA_USER)
        assert link_token.redeem(token) == WA_USER
        with pytest.raises(InvalidLinkToken, match="already used"):
            link_token.redeem(token)

    def test_expired(self):
        token = link_token.issue(WA_USER, now=time.time() - link_token.LINK_TTL - 1)
        with pytest.raises(InvalidLinkToken, match="expired"):
            link_token.redeem(token)

    @pytest.mark.parametrize("mangle", [lambda t: t[:-2] + "AA", lambda t: "A" + t[1:], str.upper])
    def test_tampered(self, mangle):
        with pytest.raises(InvalidLinkToken):
            link_token.redeem(mangle(link_token.issue(WA_USER)))

    def test_another_secret_cannot_mint_one(self, monkeypatch):
        monkeypatch.setenv("MINIAPP_JWT_SECRET", "another-secret")
        token = link_token.issue(WA_USER)
        monkeypatch.setenv("MINIAPP_JWT_SECRET", SECRET)
        with pytest.raises(InvalidLinkToken):
            link_token.redeem(token)

    def test_an_access_token_is_not_a_link(self):
        with pytest.raises(InvalidLinkToken):
            link_token.redeem(issue_token(WA_USER, SECRET))


class TestExchange:
    def test_a_link_signs_the_user_in(self):
        response = exchange(link_token.issue(WA_USER))
        assert response.status_code == 200
        body = response.json()
        assert body["user"]["id"] == WA_USER and body["token_type"] == "bearer"
        me = client.get("/api/v1/me", headers={"Authorization": "Bearer " + body["access_token"]})
        assert me.status_code == 200 and me.json()["user_id"] == WA_USER

    def test_a_link_works_once(self):
        token = link_token.issue(WA_USER)
        assert exchange(token).status_code == 200
        assert exchange(token).status_code == 401

    def test_garbage_and_access_tokens_are_refused(self):
        assert exchange("not-a-token").status_code == 401
        assert exchange(issue_token(WA_USER, SECRET)).status_code == 401

    def test_a_link_token_is_not_a_bearer_token(self):
        token = link_token.issue(WA_USER)
        me = client.get("/api/v1/me", headers={"Authorization": "Bearer " + token})
        assert me.status_code == 401

    def test_unconfigured(self, monkeypatch):
        monkeypatch.delenv("MINIAPP_JWT_SECRET")
        assert exchange("x.y").status_code == 503


async def test_whatsapp_app_sends_a_working_sign_in_link(monkeypatch):
    import app.lifespan as lifespan

    sent = []

    def graph(request):
        sent.append(json.loads(request.content))
        return httpx.Response(200, json={"messages": [{"id": "wamid.x"}]})

    async def no_sleep(_):
        return None

    monkeypatch.setattr(wa, "_sleep", no_sleep)
    graph_client = GraphClient("P", "T", transport=httpx.MockTransport(graph))
    data = lifespan.build_data()
    message = {"from": "998901234567", "id": "a", "type": "text", "text": {"body": "menu"}}
    await handle_message(graph_client, data, message)
    sent.clear()
    await handle_message(graph_client, data, {**message, "id": "b", "text": {"body": "ilova"}})
    (reply,) = sent
    body = reply["text"]["body"]
    assert APP + "/?t=" in body and reply["text"]["preview_url"] is True
    token = body.split("?t=", 1)[1].split()[0]
    assert exchange(token).status_code == 200
