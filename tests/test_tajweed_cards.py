"""Tajweed P4: spaced-repetition cards (domain.tajweed_cards, services.tajweed, bot)."""

from datetime import date, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

import bot.features.tajweed as feature
from domain import tajweed, tajweed_cards
from infra.store import InMemoryStore
from infra.store.tajweed import CardRow
from services import tajweed as service

USER = 9002
DAY = date(2026, 11, 10)


# --- the deck --------------------------------------------------------------------------


def test_the_deck_covers_every_letter_sign_rule_and_has_words():
    deck = tajweed_cards.deck()
    kinds = {c.kind for c in deck.values()}
    assert kinds == {"letter", "sign", "rule", "rule_back", "word"}
    assert {c.id[2:] for c in deck.values() if c.kind == "letter"} == set(
        "ارزمتنيبكلوهفقشسثصطجخحغعدضذظ"
    )
    for c in deck.values():
        assert c.lessons and c.front and c.back
        assert len(("tj:sg:%s:2" % c.id).encode()) <= 64  # fits Telegram callback_data
        if c.kind == "word":
            s, a = c.ayah
            assert c.front in tajweed.text(s, a).split(" ")


def test_a_letter_unlocks_from_either_track():
    za = tajweed_cards.card("L:ز")
    assert za.lessons == {"ms-004", "maxraj-til"}
    assert za in tajweed_cards.unlocked({"maxraj-til"})
    assert not tajweed_cards.unlocked(set())


# --- the schedule ----------------------------------------------------------------------


@pytest.mark.parametrize("grade, days", [(0, 0), (1, 1), (2, 3)])
def test_a_new_card(grade, days):
    row = service.schedule(None, "L:ز", grade, DAY)
    assert (row.interval_days, row.due, row.first_seen, row.last_seen) == (
        days,
        DAY + timedelta(days),
        DAY,
        DAY,
    )


@pytest.mark.parametrize("grade, days, lapses", [(0, 1, 1), (1, 12, 0), (2, 25, 0)])
def test_a_seen_card(grade, days, lapses):
    row = CardRow("L:ز", 10, DAY, DAY - timedelta(10), DAY - timedelta(30), 3, 0)
    nxt = service.schedule(row, "L:ز", grade, DAY)
    assert (nxt.interval_days, nxt.due, nxt.lapses, nxt.reps) == (
        days,
        DAY + timedelta(days),
        lapses,
        4,
    )


def test_intervals_are_capped():
    row = CardRow("L:ز", 300, DAY, DAY, DAY)
    assert service.schedule(row, "L:ز", 2, DAY).interval_days == service.MAX_INTERVAL


# --- the daily queue -------------------------------------------------------------------


@pytest.fixture
def store():
    return InMemoryStore()


@pytest.fixture
def sessions(monkeypatch):
    calls = []

    async def record(user_id, kind):
        calls.append((user_id, kind))
        return SimpleNamespace(streak=SimpleNamespace(current=4))

    monkeypatch.setattr(service, "record_session", record)
    return calls


@pytest.fixture(autouse=True)
def today(monkeypatch):
    async def fixed(user_id):
        return DAY

    monkeypatch.setattr(service, "user_today", fixed)


async def test_nothing_until_a_lesson_is_done(store):
    assert (await service.card_queue(store, USER)).next is None
    await store.tajweed.mark_done(USER, "ms-004")
    q = await service.card_queue(store, USER)
    assert q.next == "L:ز" and q.due == 0 and q.new >= 1


async def test_new_cards_are_limited_per_day_and_finishing_counts_once(store, sessions):
    for lesson in ("ms-004", "ms-005", "ms-006"):  # more than NEW_PER_DAY cards
        await store.tajweed.mark_done(USER, lesson)
    graded = []
    while (q := await service.card_queue(store, USER)).next is not None:
        graded.append(q.next)
        assert await service.grade_card(store, USER, q.next, 2) is not None
    assert len(graded) == service.NEW_PER_DAY
    assert sessions == [(USER, "tajweed")]  # the last card of the day


async def test_due_cards_come_back_and_a_miss_is_not_shown_twice_a_day(store, sessions):
    await store.tajweed.mark_done(USER, "ms-004")
    yesterday = DAY - timedelta(1)
    await store.tajweed.save_card(USER, CardRow("L:ز", 1, DAY, yesterday, yesterday, 1, 0))
    q = await service.card_queue(store, USER)
    assert q.next == "L:ز" and q.due == 1  # due before any new card
    await service.grade_card(store, USER, "L:ز", 0)
    assert (await service.card_queue(store, USER)).next != "L:ز"


async def test_only_the_card_on_top_can_be_graded(store, sessions):
    await store.tajweed.mark_done(USER, "ms-004")
    top = (await service.card_queue(store, USER)).next
    others = [c.id for c in tajweed_cards.unlocked({"ms-004"}) if c.id != top]
    assert await service.grade_card(store, USER, others[0], 2) is None  # no skipping ahead
    assert await service.grade_card(store, USER, top, 7) is None  # no such grade
    assert await service.grade_card(store, USER, top, 2) is not None
    assert await service.grade_card(store, USER, top, 2) is None  # no replay


# --- the bot ---------------------------------------------------------------------------


def _ctx(store):
    return SimpleNamespace(
        user_id=USER,
        ui_lang="uz",
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
    return [c.data for row in mock.await_args.args[1] for c in row]


async def test_review_in_the_bot(store, sessions, monkeypatch):
    played = AsyncMock()
    monkeypatch.setattr(feature, "deliver_quran", played)
    ctx = _ctx(store)
    await feature.on_tajweed(ctx, "tj:s")
    assert ctx.edit.await_args.args[0] == "tj_srs_empty"

    await store.tajweed.mark_done(USER, "ms-004")
    await feature.on_tajweed(ctx, "tj:s")
    assert "tj:sv:L:ز" in _buttons(ctx.edit)  # the front first
    await feature.on_tajweed(ctx, "tj:sv:L:ز")
    assert [b for b in _buttons(ctx.edit) if b.startswith("tj:sg:")] == [
        "tj:sg:L:ز:0",
        "tj:sg:L:ز:1",
        "tj:sg:L:ز:2",
    ]
    assert "Za" in ctx.edit.await_args.args[0]
    for _ in range(service.NEW_PER_DAY):
        top = (await service.card_queue(store, USER)).next
        if top is None:
            break
        await feature.on_tajweed(ctx, "tj:sv:" + top)
        if any(b.startswith("tj:sp:") for b in _buttons(ctx.edit)):
            await feature.on_tajweed(ctx, "tj:sp:" + top)
            assert played.await_args.args[2:4] == tajweed_cards.card(top).ayah
        await feature.on_tajweed(ctx, "tj:sg:%s:2" % top)
    assert "tj_srs_done" in ctx.edit.await_args.args[0]
    assert sessions == [(USER, "tajweed")]


@pytest.mark.parametrize(
    "cb", ["tj:sg:L:ز:9", "tj:sg:L:ز:x", "tj:sg:nope:2", "tj:sp:nope", "tj:sp:L:ز"]
)
async def test_bad_card_taps_change_nothing(store, sessions, cb):
    ctx = _ctx(store)
    await feature.on_tajweed(ctx, cb)
    assert await store.tajweed.cards(USER) == {}
    assert sessions == []


# --- the API ---------------------------------------------------------------------------


async def test_api_cards(monkeypatch):
    import json
    import time

    import httpx

    import main
    from api.auth import sign_init_data
    from config import get_settings
    from infra.store import get_store

    monkeypatch.setenv("MINIAPP_JWT_SECRET", "test-jwt-secret-not-real")
    monkeypatch.setenv("TAJWEED_AUDIO_BASE_URL", "https://media.example.test/m/")
    transport = httpx.ASGITransport(app=main.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        init = sign_init_data(
            {
                "auth_date": str(int(time.time())),
                "signature": "c2ln",
                "user": json.dumps({"id": 7311, "first_name": "A", "language_code": "uz"}),
            },
            get_settings().token,
        )
        token = (await client.post("/api/v1/auth/telegram", json={"init_data": init})).json()
        h = {"Authorization": "Bearer " + token["access_token"]}

        empty = (await client.get("/api/v1/tajweed/cards", headers=h)).json()
        assert empty["card"] is None and empty["unlocked"] == 0

        await (await get_store()).tajweed.mark_done(7311, "ms-004")
        first = (await client.get("/api/v1/tajweed/cards", headers=h)).json()
        assert first["card"]["id"] == "L:ز" and first["unlocked"] > 0

        r = await client.post(
            "/api/v1/tajweed/cards/grade", headers=h, json={"card_id": "L:ز", "grade": 2}
        )
        assert r.status_code == 200 and r.json()["card"]["id"] != "L:ز"
        again = await client.post(
            "/api/v1/tajweed/cards/grade", headers=h, json={"card_id": "L:ز", "grade": 2}
        )
        assert again.status_code == 409
