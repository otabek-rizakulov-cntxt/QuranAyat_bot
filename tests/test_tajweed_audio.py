"""Tajweed P1: the Muallimi soniy audio track, progress (✅ Oʻqidim) and the Mini App API.

docs/TAJWEED_PLAN.md.
"""

import hashlib
import json
import os
import re
import time
from types import SimpleNamespace
from unittest.mock import AsyncMock

import httpx
import pytest

import bot.features.tajweed as feature
import main
from api.auth import sign_init_data
from config import get_settings
from domain import tajweed_lessons
from domain.uz_translit import to_latin
from infra.store import InMemoryStore, get_store
from infra.store.sessions import KIND_TAJWEED
from services import tajweed as service

REVIEWER, USER = 9001, 9002
BASE = "https://media.example.test/tajweed/muallimi-soniy/"
DOWNLOADS = os.path.join(os.path.dirname(__file__), "..", "data", "tajweed", "downloads")


# --- the manifest ----------------------------------------------------------------------


def test_manifest_covers_the_73_lessons_once_preface_first():
    lessons = tajweed_lessons.audio_lessons()
    assert sorted(x.n for x in lessons) == list(range(1, 74))
    assert len({x.id for x in lessons}) == 73
    assert lessons[0].n == 73 and lessons[1].n == 1  # Soʻz boshi, then the alphabet
    units = [u.id for u in tajweed_lessons.audio_units()]
    assert [x.unit for x in lessons] == sorted((x.unit for x in lessons), key=units.index)
    assert not {u.id for u in tajweed_lessons.units()} & set(units)  # unit ids never clash
    for x in lessons:
        assert x.file == "%03d.mp3" % x.n
        assert 0 < x.seconds < 15 * 60 and 0 < x.bytes < 20_000_000  # Telegram fetches ≤ 20 MB
        assert not re.search(r"https?://|www\.|\.(uz|com)\b", x.title)
        assert len("tj:l:" + x.id) <= 64


def test_cyrillic_titles_round_trip():
    for lat, cyr in zip(
        tajweed_lessons.audio_lessons("uz"), tajweed_lessons.audio_lessons("uz-Cyrl")
    ):
        assert lat.id == cyr.id and to_latin(cyr.title) == lat.title


@pytest.mark.skipif(not os.path.isdir(DOWNLOADS), reason="lesson audio not downloaded here")
def test_manifest_matches_the_local_files():
    names = {n[:3]: n for n in os.listdir(DOWNLOADS) if n.endswith(".mp3")}
    for x in tajweed_lessons.audio_lessons():
        with open(os.path.join(DOWNLOADS, names["%03d" % x.n]), "rb") as fp:
            data = fp.read()
        assert (len(data), hashlib.sha256(data).hexdigest()) == (x.bytes, x.sha256), x.id


# --- the bot ---------------------------------------------------------------------------


@pytest.fixture
def store():
    return InMemoryStore()


@pytest.fixture(autouse=True)
def env(monkeypatch):
    monkeypatch.setenv("TAJWEED_REVIEWERS", str(REVIEWER))
    monkeypatch.setenv("TAJWEED_AUDIO_BASE_URL", BASE)


@pytest.fixture
def sessions(monkeypatch):
    """record_session, faked: the streak service has its own tests."""
    calls = []

    async def record(user_id, kind):
        calls.append((user_id, kind))
        return SimpleNamespace(streak=SimpleNamespace(current=3))

    monkeypatch.setattr(service, "record_session", record)
    return calls


def _ctx(store, user=USER, lang="uz"):
    return SimpleNamespace(
        user_id=user,
        ui_lang=lang,
        store=store,
        tr=lambda key, **kw: key,
        reply=AsyncMock(),
        edit=AsyncMock(),
        answer=AsyncMock(),
        channel=SimpleNamespace(send_audio=AsyncMock()),
        data={},
        reciter="Husary_128kbps",
        translation_lang="uz",
    )


def _buttons(mock):
    choices = mock.await_args.args[1] if mock.await_args else None
    return [c.data for row in (choices or []) for c in row]


def _labels(mock):
    return [c.label for row in mock.await_args.args[1] for c in row]


async def test_only_the_audio_track_goes_straight_to_its_units(store):
    ctx = _ctx(store)
    await feature.tajvid(ctx)
    assert _buttons(ctx.reply)[0] == "tj:u:ms-kirish"
    assert "tj:units" not in _buttons(ctx.reply)  # nothing to go back to


async def test_without_the_audio_base_url_there_is_nothing_yet(store, monkeypatch):
    monkeypatch.delenv("TAJWEED_AUDIO_BASE_URL")
    ctx = _ctx(store)
    await feature.tajvid(ctx)
    assert ctx.reply.await_args.args[0] == "tj_soon"
    await feature.on_tajweed(ctx, "tj:l:ms-073")
    ctx.edit.assert_not_awaited()
    await feature.on_tajweed(ctx, "tj:a:ms-073")
    ctx.channel.send_audio.assert_not_awaited()


async def test_reviewer_picks_between_both_tracks(store):
    ctx = _ctx(store, REVIEWER)
    await feature.tajvid(ctx)
    assert _buttons(ctx.reply) == ["tj:t:alifbo", "tj:t:qoidalar", "tj:s"]
    await feature.on_tajweed(ctx, "tj:t:qoidalar")
    assert "tj:units" in _buttons(ctx.edit)


async def test_unit_lists_lessons_with_ticks(store):
    await store.tajweed.mark_done(USER, "ms-002")
    ctx = _ctx(store)
    await feature.on_tajweed(ctx, "tj:u:ms-harflar")
    data = _buttons(ctx.edit)
    assert data[:2] == ["tj:l:ms-002", "tj:l:ms-003"]  # two per row for the 28 letters
    assert data[-1] == "tj:t:alifbo"
    assert _labels(ctx.edit)[0].startswith("✓ ")
    assert not _labels(ctx.edit)[1].startswith("✓ ")


async def test_audio_card_listen_and_done(store, sessions):
    ctx = _ctx(store)
    await feature.on_tajweed(ctx, "tj:l:ms-073")
    assert {"tj:a:ms-073", "tj:d:ms-073"} <= set(_buttons(ctx.edit))
    assert any(b.startswith("tj:r:ms-073:") for b in _buttons(ctx.edit))  # reading practice
    assert "tj:l:ms-001" in _buttons(ctx.edit)  # ▶ to the alphabet

    await feature.on_tajweed(ctx, "tj:a:ms-073")
    lesson = tajweed_lessons.audio_lesson("ms-073")
    call = ctx.channel.send_audio.await_args
    assert call.args[0] == BASE + "073.mp3"
    assert call.kwargs["cache_key"] == "tjm:" + lesson.sha256[:12]
    assert call.kwargs["caption"] == "🎧 " + lesson.title  # no source line

    await feature.on_tajweed(ctx, "tj:d:ms-073")
    assert sessions == [(USER, KIND_TAJWEED)]
    assert await store.tajweed.done(USER) == {"ms-073"}
    assert "tj_done_already" in _labels(ctx.edit)  # the card re-renders with ✓

    await feature.on_tajweed(ctx, "tj:d:ms-073")  # again: no second session
    assert sessions == [(USER, KIND_TAJWEED)]
    ctx.answer.assert_awaited_with("tj_done_already")


async def test_rules_lessons_can_be_marked_done_once_published(store, sessions):
    lesson = tajweed_lessons.lessons()[0]
    ctx = _ctx(store)
    await feature.on_tajweed(ctx, "tj:d:" + lesson.id)  # a draft: not for users
    assert sessions == []
    await store.tajweed.approve(lesson.id, lesson.content_hash, REVIEWER)
    await feature.on_tajweed(ctx, "tj:l:" + lesson.id)
    assert "tj:d:" + lesson.id in _buttons(ctx.edit)
    await feature.on_tajweed(ctx, "tj:d:" + lesson.id)
    assert sessions == [(USER, KIND_TAJWEED)]


@pytest.mark.parametrize(
    "cb", ["tj:a:nope", "tj:d:nope", "tj:t:nope", "tj:a:", "tj:d:ms-073:x", "tj:units:x"]
)
async def test_bad_callbacks_are_only_acknowledged(store, sessions, cb):
    ctx = _ctx(store)
    await feature.on_tajweed(ctx, cb)
    ctx.channel.send_audio.assert_not_awaited()
    ctx.answer.assert_awaited()
    assert sessions == []


# --- the Mini App API ------------------------------------------------------------------

SECRET = "test-jwt-secret-not-real"


@pytest.fixture
async def client(monkeypatch):
    monkeypatch.setenv("MINIAPP_JWT_SECRET", SECRET)
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
    assert r.status_code == 200, r.text
    return {"Authorization": "Bearer " + r.json()["access_token"]}


async def test_api_state_and_done(client):
    h = await _login(client, USER)
    r = await client.get("/api/v1/tajweed", headers=h)
    assert r.json() == {
        "audio_base": BASE,
        "approved": [],
        "done": [],
        "reviewer": False,
        "tracking": [],
        "practice": {},
    }

    r = await client.post("/api/v1/tajweed/done", headers=h, json={"lesson_id": "ms-001"})
    assert r.status_code == 200
    assert r.json()["first_time"] is True and r.json()["streak"] >= 1
    r = await client.post("/api/v1/tajweed/done", headers=h, json={"lesson_id": "ms-001"})
    assert r.json() == {"done": True, "first_time": False, "streak": None}

    assert (await client.get("/api/v1/tajweed", headers=h)).json()["done"] == ["ms-001"]
    sessions = await (await get_store()).sessions.list_active_dates(USER)
    assert len(sessions) == 1


async def test_api_refuses_unknown_and_draft_lessons(client):
    h = await _login(client, USER)
    draft = tajweed_lessons.lessons()[0].id
    for lesson_id in ("nope", draft):
        r = await client.post("/api/v1/tajweed/done", headers=h, json={"lesson_id": lesson_id})
        assert r.status_code == 404
    r = await client.get("/api/v1/tajweed", headers=await _login(client, REVIEWER))
    assert r.json()["reviewer"] is True


# --- text tracking (P2) ----------------------------------------------------------------

LINES = (
    tajweed_lessons.TimedLine("uz", "Endi za harfini oʻrganamiz.", 0.5, 2.7),
    tajweed_lessons.TimedLine("ar", "زَ زِ زُ", 2.7, 5.1),
)


@pytest.fixture
def timed(monkeypatch):
    """Lesson 4 aligned (the real timings come from Colab + align_text)."""
    table = {"ms-004": LINES}
    monkeypatch.setattr(
        tajweed_lessons, "audio_timings", lambda lesson_id, lang="uz": table.get(lesson_id, ())
    )
    return table


async def test_text_tracking_is_shown_once_a_reviewer_approves_it(store, timed):
    user = _ctx(store)
    await feature.on_tajweed(user, "tj:l:ms-004")
    assert "tj:m:ms-004" not in _buttons(user.edit)  # a draft: hidden from users
    await feature.on_tajweed(user, "tj:m:ms-004")
    user.reply.assert_not_awaited()

    rev = _ctx(store, REVIEWER)
    await feature.on_tajweed(rev, "tj:l:ms-004")
    assert {"tj:m:ms-004", "tj:ok:ms-004"} <= set(_buttons(rev.edit))
    await feature.on_tajweed(rev, "tj:ok:ms-004")
    assert await service.tracking_ids(store) == {"ms-004"}

    await feature.on_tajweed(user, "tj:m:ms-004")
    sent = user.reply.await_args.args[0]
    assert "زَ زِ زُ" in sent and "<i>Endi za harfini oʻrganamiz.</i>" in sent

    timed["ms-004"] = LINES[:1]  # re-aligned: the approval no longer matches
    assert await service.tracking_ids(store) == set()


async def test_lessons_without_timings_have_nothing_to_review(store, timed):
    rev = _ctx(store, REVIEWER)
    await feature.on_tajweed(rev, "tj:l:ms-005")
    assert not {"tj:m:ms-005", "tj:ok:ms-005"} & set(_buttons(rev.edit))
    assert await service.review(store, REVIEWER, "ms-005", True) is False


async def test_api_review(client, timed):
    user = await _login(client, USER)
    body = {"lesson_id": "ms-004", "approve": True}
    assert (await client.post("/api/v1/tajweed/review", headers=user, json=body)).status_code == 403

    rev = await _login(client, REVIEWER)
    r = await client.post("/api/v1/tajweed/review", headers=rev, json=body)
    assert r.status_code == 200
    assert (await client.get("/api/v1/tajweed", headers=user)).json()["tracking"] == ["ms-004"]
    missing = {"lesson_id": "ms-005", "approve": True}
    assert (
        await client.post("/api/v1/tajweed/review", headers=rev, json=missing)
    ).status_code == 404
