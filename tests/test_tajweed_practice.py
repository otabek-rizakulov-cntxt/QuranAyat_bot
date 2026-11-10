"""Tajweed P3: quizzes and reading drills (domain.tajweed_practice, bot, API)."""

import json
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
from domain import tajweed, tajweed_lessons, tajweed_practice
from infra.store import InMemoryStore
from services import tajweed as service

REVIEWER, USER = 9001, 9002
BASE = "https://media.example.test/tajweed/muallimi-soniy/"
ALL = [x.id for x in tajweed_lessons.audio_lessons()] + [x.id for x in tajweed_lessons.lessons()]


# --- the generator ---------------------------------------------------------------------


@pytest.mark.parametrize("lesson_id", ALL)
def test_every_lesson_has_a_full_drill_and_rule_lessons_a_full_quiz(lesson_id):
    drill = tajweed_practice.drill(lesson_id, 1)
    assert len(drill) == tajweed_practice.N
    assert len({d.word for d in drill}) == len(drill)
    for d in drill:
        assert d.word in tajweed.text(d.surah, d.ayah).split(" ")
    quiz = tajweed_practice.quiz(lesson_id, 1)
    assert len(quiz) == (tajweed_practice.N if tajweed_practice.rules_for(lesson_id) else 0)


@pytest.mark.parametrize("lesson_id", [x for x in ALL if tajweed_practice.rules_for(x)])
@pytest.mark.parametrize("seed", [1, 42, 99999])
def test_every_answer_is_right_and_every_distractor_wrong(lesson_id, seed):
    for q in tajweed_practice.quiz(lesson_id, seed):
        assert 0 <= q.answer < len(q.options)
        assert len(set(q.options)) == len(q.options)
        if q.kind in ("name", "listen"):
            ((s, a, marked),) = q.ayahs
            assert q.options[q.answer] == tajweed.RULES[q.rule].name_uz
            # the rule occurs once there, and no offered wrong answer is also
            # annotated on those letters (it would be right too)
            ((_, x, y),) = tajweed.spans(s, a, [q.rule])
            names = {tajweed.RULES[r].name_uz: r for r in tajweed.RULES}
            wrong = {names[o] for i, o in enumerate(q.options) if i != q.answer}
            assert not any(r in wrong and p < y and x < e for r, p, e in tajweed.spans(s, a))
        elif q.kind == "find":
            has = [bool(tajweed.spans(s, a, [q.rule])) for s, a, _ in q.ayahs]
            assert has.count(True) == 1 and has.index(True) == q.answer
        else:  # count
            ((s, a, marked),) = q.ayahs
            n = len(tajweed.spans(s, a, [q.rule]))
            assert q.options[q.answer] == str(n) and marked.count("<u><b>") == n
        if q.kind == "listen":
            assert q.audio == q.ayahs[0][:2]


def test_sessions_are_deterministic_per_seed():
    assert tajweed_practice.quiz("ms-056", 7) == tajweed_practice.quiz("ms-056", 7)
    assert tajweed_practice.drill("ms-004", 7) == tajweed_practice.drill("ms-004", 7)
    assert tajweed_practice.drill("ms-004", 7) != tajweed_practice.drill("ms-004", 8)


def test_letter_drills_use_the_lessons_letter():
    for d in tajweed_practice.drill("ms-004", 3):  # Za
        assert "ز" in d.word


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
    calls = []

    async def record(user_id, kind):
        calls.append((user_id, kind))
        return SimpleNamespace(streak=SimpleNamespace(current=2))

    monkeypatch.setattr(service, "record_session", record)
    return calls


def _ctx(store, lang="uz"):
    return SimpleNamespace(
        user_id=USER,
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
    return [c.data for row in mock.await_args.args[1] for c in row]


async def test_a_quiz_end_to_end(store, sessions):
    ctx = _ctx(store)
    seed, lesson = 5, "ms-056"
    questions = tajweed_practice.quiz(lesson, seed)
    score, i = 0, 0
    await feature.on_tajweed(ctx, "tj:q:%s:%d:0:0" % (lesson, seed))
    for i, q in enumerate(questions):
        pick = q.answer if i % 2 == 0 else (q.answer + 1) % len(q.options)  # right, wrong, ...
        assert "tj:qa:%s:%d:%d:%d:%d" % (lesson, seed, i, score, pick) in _buttons(ctx.edit)
        await feature.on_tajweed(ctx, "tj:qa:%s:%d:%d:%d:%d" % (lesson, seed, i, score, pick))
        verdict = ctx.edit.await_args.args[0]
        assert ("tj_right" in verdict) == (i % 2 == 0)
        score += i % 2 == 0
        nxt = "tj:q:%s:%d:%d:%d" % (lesson, seed, i + 1, score)
        assert nxt in _buttons(ctx.edit)
        await feature.on_tajweed(ctx, nxt)
    assert sessions == [(USER, "tajweed")]
    assert await store.tajweed.practice(USER) == {lesson: (1, 60)}  # 3 of 5


async def test_a_reading_drill_end_to_end(store, sessions, monkeypatch):
    played = AsyncMock()
    monkeypatch.setattr(feature, "deliver_quran", played)
    ctx = _ctx(store)
    await feature.on_tajweed(ctx, "tj:r:ms-004:3:0:0")
    for i in range(tajweed_practice.N):
        assert "tj:rp:ms-004:3:%d" % i in _buttons(ctx.edit)
        await feature.on_tajweed(ctx, "tj:ra:ms-004:3:%d:%d:k" % (i, i))
    assert await store.tajweed.practice(USER) == {"ms-004": (1, 100)}
    await feature.on_tajweed(ctx, "tj:rp:ms-004:3:0")  # 🔊 plays that word's ayah
    first = tajweed_practice.drill("ms-004", 3)[0]
    assert played.await_args.args[2:4] == (first.surah, first.ayah)


@pytest.mark.parametrize(
    "cb",
    [
        "tj:q:ms-056:5:9:0",  # past the end
        "tj:q:ms-056:5:1:5",  # a score above the question number
        "tj:qa:ms-056:5:0:0",  # missing choice
        "tj:q:ms-056:x:0:0",
        "tj:r:ms-004:3:0:0:extra",
        "tj:ra:ms-004:3:0:0:maybe",
        "tj:q:nope:5:0:0",
        "tj:qp:ms-056:5:99",
    ],
)
async def test_bad_practice_callbacks_are_only_acknowledged(store, sessions, cb):
    ctx = _ctx(store)
    await feature.on_tajweed(ctx, cb)
    ctx.edit.assert_not_awaited()
    ctx.answer.assert_awaited()
    assert sessions == []


async def test_cyrillic_ui_gets_cyrillic_rule_names(store):
    ctx = _ctx(store, "uz-Cyrl")
    await feature.on_tajweed(ctx, "tj:q:ms-056:5:0:0")
    labels = [c.label for row in ctx.edit.await_args.args[1] for c in row]
    assert not any(re.search(r"[a-z]{3}", lbl) for lbl in labels if not lbl.startswith("tj_"))


# --- the API ---------------------------------------------------------------------------


@pytest.fixture
async def client(monkeypatch):
    monkeypatch.setenv("MINIAPP_JWT_SECRET", "test-jwt-secret-not-real")
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


async def test_api_practice(client):
    h = await _login(client, USER)
    r = await client.get("/api/v1/tajweed/practice/ms-056?seed=5", headers=h)
    assert r.status_code == 200
    body = r.json()
    assert len(body["quiz"]) == 5 and len(body["drill"]) == 5
    assert body["quiz"][0]["options"][body["quiz"][0]["answer"]]

    r = await client.post(
        "/api/v1/tajweed/practice",
        headers=h,
        json={"lesson_id": "ms-056", "kind": "quiz", "correct": 4, "total": 5},
    )
    assert r.status_code == 200 and r.json()["best_pct"] == 80 and r.json()["streak"] >= 1
    assert (await client.get("/api/v1/tajweed", headers=h)).json()["practice"] == {"ms-056": 80}

    assert (await client.get("/api/v1/tajweed/practice/nope?seed=1", headers=h)).status_code == 404
    draft = tajweed_lessons.lessons()[0].id  # not approved: not for users
    assert (
        await client.get("/api/v1/tajweed/practice/%s?seed=1" % draft, headers=h)
    ).status_code == 404
