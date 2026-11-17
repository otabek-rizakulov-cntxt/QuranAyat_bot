"""Audio start-time samples from the Mini App (docs/MAKHRAJ_3D_PLAN.md §9)."""

import json
import time

import httpx
import pytest

import main
from api.auth import sign_init_data
from config import get_settings
from services import audio_metrics

SECRET = "test-jwt-secret-not-real"
REVIEWER, USER = 7101, 7102


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setenv("MINIAPP_JWT_SECRET", SECRET)
    monkeypatch.setenv("TAJWEED_REVIEWERS", str(REVIEWER))
    audio_metrics.reset_for_tests()
    yield
    audio_metrics.reset_for_tests()


@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=main.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


async def _login(client, user_id):
    init = sign_init_data(
        {
            "auth_date": str(int(time.time())),
            "signature": "c2ln",
            "user": json.dumps({"id": user_id, "first_name": "A", "language_code": "uz"}),
        },
        get_settings().token,
    )
    r = await client.post("/api/v1/auth/telegram", json={"init_data": init})
    return {"Authorization": "Bearer " + r.json()["access_token"]}


def _sample(**kw):
    body = {
        "host": "media.example.test",
        "kind": "lesson",
        "ms": 900,
        "cached": False,
        "net": "4g",
        "platform": "ios",
    }
    body.update(kw)
    return body


async def test_samples_are_summarised_per_host_for_reviewers_only(client):
    assert (await client.post("/api/v1/metrics/audio", json=_sample())).status_code == 401
    user = await _login(client, USER)
    for ms in (100, 200, 300, 400, 5000):
        r = await client.post("/api/v1/metrics/audio", headers=user, json=_sample(ms=ms))
        assert r.status_code == 204
    await client.post("/api/v1/metrics/audio", headers=user, json=_sample(host="cdn.test", ms=50))

    assert (await client.get("/api/v1/metrics/audio", headers=user)).status_code == 403
    rows = (
        await client.get("/api/v1/metrics/audio", headers=await _login(client, REVIEWER))
    ).json()
    assert rows[0] == {
        "host": "media.example.test",
        "kind": "lesson",
        "cached": False,
        "n": 5,
        "p50": 300,
        "p95": 5000,
    }  # the slowest first
    assert rows[1]["host"] == "cdn.test"


@pytest.mark.parametrize(
    "bad",
    [
        {"host": "https://x.test/a"},
        {"host": "A B"},
        {"kind": "video"},
        {"ms": -1},
        {"ms": 60_001},
        {"net": "x" * 9},
        {"platform": "<script>"},
    ],
)
async def test_bad_samples_are_rejected(client, bad):
    user = await _login(client, USER)
    r = await client.post("/api/v1/metrics/audio", headers=user, json=_sample(**bad))
    assert r.status_code == 422
    assert audio_metrics.summary() == []
