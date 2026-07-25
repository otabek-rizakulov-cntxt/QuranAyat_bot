"""FastAPI webhook endpoint: health check and token-gated routing.

The TestClient is used WITHOUT its context manager on purpose, so the startup
lifespan (which would kick off bot creation / webhook registration) never runs.
`main.bot` and `main.data` therefore stay None, letting us assert the
"still initializing" acknowledgement path without any network."""

from fastapi.testclient import TestClient

import main
from config import Environment

client = TestClient(main.app)


def test_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_webhook_rejects_wrong_token():
    response = client.post("/webhook/not-the-real-token", json={"update_id": 1})
    assert response.status_code == 404


def test_webhook_acks_before_initialization():
    token = Environment.get_env("token")
    response = client.post("/webhook/%s" % token, json={"update_id": 1})
    assert response.status_code == 200
    assert response.json() == {"ok": True}
