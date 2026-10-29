"""FastAPI webhook endpoint: health check and secret-header-gated routing.

The TestClient is used WITHOUT its context manager on purpose, so the startup
lifespan (which would kick off bot creation / webhook registration) never runs.
`app.state.runtime.bot` and `.data` therefore stay None, letting us assert the
"still initializing" acknowledgement path without any network."""

from fastapi.testclient import TestClient

import main
from app.routes.webhook import SECRET_HEADER, WEBHOOK_PATH, webhook_secret
from config import get_settings

client = TestClient(main.app)


def test_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    # "pending" until first use; tests run on the in-memory stores after that.
    assert body["store"] in ("pending", "memory")
    assert body["cache"] in ("pending", "memory")


def test_webhook_rejects_a_missing_secret():
    response = client.post(WEBHOOK_PATH, json={"update_id": 1})
    assert response.status_code == 401


def test_webhook_rejects_a_wrong_secret():
    response = client.post(WEBHOOK_PATH, json={"update_id": 1}, headers={SECRET_HEADER: "nope"})
    assert response.status_code == 401


def test_the_old_token_in_the_path_route_is_gone():
    token = get_settings().token
    response = client.post("/webhook/%s" % token, json={"update_id": 1})
    assert response.status_code == 404


def test_webhook_acks_before_initialization():
    headers = {SECRET_HEADER: webhook_secret()}
    response = client.post(WEBHOOK_PATH, json={"update_id": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_the_secret_does_not_reveal_the_token():
    secret, token = webhook_secret(), get_settings().token
    assert secret and token not in secret and token.split(":")[1] not in secret
    assert len(secret) <= 256 and all(c.isalnum() or c in "_-" for c in secret)
    assert secret == webhook_secret()  # stable across calls, so registration and check agree


async def test_startup_registers_the_webhook_without_the_token(monkeypatch):
    from unittest.mock import AsyncMock

    import app.lifespan as lifespan
    from app.state import AppState

    bot = AsyncMock()
    monkeypatch.setenv("WEBHOOK_URL", "https://bot.example")
    monkeypatch.setattr(lifespan, "create_bot", lambda settings: bot)
    monkeypatch.setattr(lifespan, "build_data", lambda: {})
    monkeypatch.setattr(lifespan.hifz, "load_features", lambda: None)
    monkeypatch.setattr(lifespan, "spawn", lambda coro: coro.close())
    await lifespan.initialize(AppState())

    kwargs = bot.set_webhook.await_args.kwargs
    assert kwargs["url"] == "https://bot.example/webhook"
    assert kwargs["secret_token"] == webhook_secret()
    assert get_settings().token not in kwargs["url"]
