"""Mini App API feature routes (docs/MINI_APP_PLAN.md Phases 2-3).

Each test drives the real FastAPI app in-process (httpx + ASGITransport, so the
in-memory store shares the test's event loop) and checks a plan done-when
against the same store the bot reads — the routes are adapters over
services/*, so "the app and the bot agree" is asserted on shared rows."""

import json
import time
from datetime import date
from datetime import time as dtime

import httpx
import pytest

import main
from api.auth import sign_init_data
from config import get_settings
from infra.file_facade import File
from infra.store import get_store
from infra.store.plans import DAY_COMPLETED
from infra.store.sessions import KIND_DRILL
from services import plans as plans_service
from services.user_settings import UserSettings

SECRET = "test-jwt-secret-not-real"
ALICE, BOB = 7001, 7002


@pytest.fixture(autouse=True)
def _jwt_secret(monkeypatch):
    monkeypatch.setenv("MINIAPP_JWT_SECRET", SECRET)


@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=main.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


async def _login(client, user_id=ALICE, lang="en", name="Amina"):
    init = sign_init_data(
        {
            "auth_date": str(int(time.time())),
            "signature": "c2ln",
            "user": json.dumps({"id": user_id, "first_name": name, "language_code": lang}),
        },
        get_settings().token,
    )
    r = await client.post("/api/v1/auth/telegram", json={"init_data": init})
    assert r.status_code == 200, r.text
    return {"Authorization": "Bearer " + r.json()["access_token"]}


# --- settings & catalog ---------------------------------------------------------


async def test_reciter_set_in_app_is_the_bots_reciter_and_language_never_changes_it(client):
    h = await _login(client)
    r = await client.patch("/api/v1/me/settings", headers=h, json={"reciter": "Alafasy_128kbps"})
    assert r.status_code == 200 and r.json()["reciter"] == "Alafasy_128kbps"
    assert (await UserSettings().get(ALICE)).reciter == "Alafasy_128kbps"

    r = await client.patch("/api/v1/me/settings", headers=h, json={"ui_lang": "ru"})
    assert r.json() == {"ui_lang": "ru", "translation_lang": "en", "reciter": "Alafasy_128kbps"}


async def test_settings_reject_unknown_values(client):
    h = await _login(client)
    for body in ({"ui_lang": "xx"}, {"translation_lang": "xx"}, {"reciter": "nobody"}):
        assert (await client.patch("/api/v1/me/settings", headers=h, json=body)).status_code == 422


async def test_catalogs(client):
    h = await _login(client)
    reciters = (await client.get("/api/v1/catalog/reciters", headers=h)).json()
    assert reciters["reciters"][0]["subfolder"] == "Husary_128kbps"  # shortlist first
    assert len(reciters["reciters"]) == len(File._load_performers())
    assert {r["warning_key"] for r in reciters["reciters"] if r["kind"] == "riwayah"} == {
        "riwayah_warning"
    }
    langs = (await client.get("/api/v1/catalog/languages", headers=h)).json()
    assert any(l["code"] == "translit" for l in langs["translation"])
    assert not any(l["code"] == "translit" for l in langs["ui"])


async def test_every_feature_route_needs_a_token(client):
    for method, path in (
        ("GET", "/me"),
        ("GET", "/today"),
        ("GET", "/progress"),
        ("GET", "/streak"),
        ("GET", "/leaderboard"),
        ("GET", "/check/question"),
        ("GET", "/plans/active"),
        ("GET", "/catalog/reciters"),
        ("GET", "/reader/position"),
    ):
        assert (await client.request(method, "/api/v1" + path)).status_code == 401, path


# --- reader position --------------------------------------------------------------


async def test_reader_position_is_the_bots_position(client):
    h = await _login(client)
    assert (await client.get("/api/v1/reader/position", headers=h)).json() is None
    r = await client.put(
        "/api/v1/reader/position", headers=h, json={"surah": 2, "ayah": 255, "type": "arabic"}
    )
    assert r.status_code == 200
    assert await File().get_user(ALICE) == [2, 255, "arabic"]  # what next/prev read

    await File().save_user(ALICE, (18, 10, "translation"))  # the bot moved on
    assert (await client.get("/api/v1/reader/position", headers=h)).json() == {
        "surah": 18,
        "ayah": 10,
        "type": "translation",
    }
    assert (
        await client.put("/api/v1/reader/position", headers=h, json={"surah": 1, "ayah": 9})
    ).status_code == 422


# --- profile ------------------------------------------------------------------------


async def test_profile_patch_and_name_rule(client):
    h = await _login(client)
    r = await client.patch("/api/v1/me/profile", headers=h, json={"leaderboard_opt_in": True})
    assert r.status_code == 409 and r.json()["detail"] == "name_required"

    r = await client.patch(
        "/api/v1/me/profile",
        headers=h,
        json={
            "display_name": "  Abu   Bakr ",
            "leaderboard_opt_in": True,
            "timezone": "+5",
            "reminder_time": "6:30",
        },
    )
    assert r.status_code == 200, r.text
    profile = r.json()["profile"]
    assert profile == {
        **profile,
        "display_name": "Abu Bakr",
        "leaderboard_opt_in": True,
        "timezone": "+05:00",
        "reminder_time": "06:30",
    }

    r = await client.patch("/api/v1/me/profile", headers=h, json={"reminder_time": None})
    assert r.json()["profile"]["reminder_time"] is None
    for bad in ({"display_name": "A"}, {"timezone": "Mars"}, {"reminder_time": "25:00"}):
        assert (await client.patch("/api/v1/me/profile", headers=h, json=bad)).status_code == 422


# --- plans ----------------------------------------------------------------------------

PLAN = {"target": "67", "pace": 2, "days": [1, 2, 3, 4, 5], "start": "2026-10-19"}


async def test_preview_equals_saved_plan_day_for_day(client):
    h = await _login(client)
    preview = (await client.post("/api/v1/plans/preview", headers=h, json=PLAN)).json()
    assert preview["target"]["label"] == "67:1-30"
    assert preview["start"] == "2026-10-19"

    r = await client.post(
        "/api/v1/plans", headers=h, json={**PLAN, "timezone": "+05:00", "reminder_time": "07:00"}
    )
    assert r.status_code == 201, r.text
    saved = r.json()
    assert [
        (d["date"], d["surah"], d["start_ayah"], d["end_ayah"], d["review"]) for d in saved["days"]
    ] == [
        (p["date"], p["surah"], p["start_ayah"], p["end_ayah"], p["review"])
        for p in preview["portions"]
    ]

    # ...and the bot pushes it: the first portion is queued for the daily push.
    store = await get_store()
    plan = await store.plans.get_active_plan(ALICE)
    assert plan.id == saved["id"]
    queued = await plans_service.enqueue_next(store, ALICE, ALICE, plan)
    assert queued is None  # already queued by the save: a key clash


async def test_preview_rejects_bad_input(client):
    h = await _login(client)
    for body in (
        {**PLAN, "target": "nonsense"},
        {**PLAN, "days": [0]},
        {**PLAN, "days": []},
        {**PLAN, "pace": 500},
    ):
        assert (
            await client.post("/api/v1/plans/preview", headers=h, json=body)
        ).status_code == 422, body


async def test_lifecycle_and_today(client):
    h = await _login(client)
    assert (await client.get("/api/v1/today", headers=h)).json()["status"] == "none"
    await client.post(
        "/api/v1/plans", headers=h, json={**PLAN, "start": None, "days": [1, 2, 3, 4, 5, 6, 7]}
    )
    today = (await client.get("/api/v1/today", headers=h)).json()
    assert today["status"] == "due" and today["position"] == 1
    assert today["day"]["label"] == "67:1-2"

    paused = (await client.post("/api/v1/plans/active/pause", headers=h)).json()
    assert paused["status"] == "paused"
    assert (await client.get("/api/v1/today", headers=h)).json()["status"] == "paused"
    assert (await client.post("/api/v1/plans/active/resume", headers=h)).json()[
        "status"
    ] == "active"
    assert (await client.post("/api/v1/plans/active/abandon", headers=h)).json() is None
    assert (await client.get("/api/v1/plans/active", headers=h)).json() is None
    assert (await client.post("/api/v1/plans/active/pause", headers=h)).status_code == 404


async def test_drill_in_app_and_chat_logs_one_session(client):
    h = await _login(client)
    saved = (
        await client.post(
            "/api/v1/plans", headers=h, json={**PLAN, "start": None, "days": [1, 2, 3, 4, 5, 6, 7]}
        )
    ).json()
    day_id = saved["days"][0]["id"]

    first = (await client.post("/api/v1/drills/%d/complete" % day_id, headers=h)).json()
    assert first["status"] == "completed" and first["label"] == "67:1-2"
    again = (await client.post("/api/v1/drills/%d/complete" % day_id, headers=h)).json()
    assert again["status"] == "already"

    # The chat button for the same portion runs the same service: nothing new.
    store = await get_store()
    chat = await plans_service.complete_day(store, ALICE, ALICE, day_id)
    assert chat.status == plans_service.ALREADY
    sessions = await store.sessions.list_sessions(ALICE)
    assert [s.kind for s in sessions] == [KIND_DRILL]
    assert (await store.plans.get_plan_day(day_id)).state == DAY_COMPLETED


async def test_cannot_complete_someone_elses_portion(client):
    h_alice = await _login(client, ALICE)
    h_bob = await _login(client, BOB)
    saved = (await client.post("/api/v1/plans", headers=h_alice, json=PLAN)).json()
    r = await client.post("/api/v1/drills/%d/complete" % saved["days"][0]["id"], headers=h_bob)
    assert r.status_code == 404


# --- recall check -----------------------------------------------------------------


async def test_question_hides_the_answer_and_a_pass_ticks_the_streak_once(client):
    h = await _login(client)
    q = (await client.get("/api/v1/check/question?ref=67", headers=h)).json()
    assert set(q) == {"question_token", "prompt", "options", "span", "guessed_span"}
    assert len(q["options"]) == 4

    # Find the right option by trying each one — wrong answers log nothing.
    results = []
    for i in range(4):
        r = await client.post(
            "/api/v1/check/answer",
            headers=h,
            json={"question_token": q["question_token"], "choice": i},
        )
        results.append(r.json())
    right = [r for r in results if r["correct"]]
    assert len(right) == 1 and right[0]["already_today"] is False
    assert all(r["correct_index"] == right[0]["correct_index"] for r in results)

    again = (
        await client.post(
            "/api/v1/check/answer",
            headers=h,
            json={"question_token": q["question_token"], "choice": right[0]["correct_index"]},
        )
    ).json()
    assert again["correct"] and again["already_today"]
    store = await get_store()
    assert len(await store.sessions.list_sessions(ALICE)) == 1
    assert (await client.get("/api/v1/streak", headers=h)).json()["current"] == 1


async def test_question_token_is_bound_to_user_and_untamperable(client):
    h_alice = await _login(client, ALICE)
    h_bob = await _login(client, BOB)
    q = (await client.get("/api/v1/check/question?ref=67", headers=h_alice)).json()
    r = await client.post(
        "/api/v1/check/answer",
        headers=h_bob,
        json={"question_token": q["question_token"], "choice": 0},
    )
    assert r.status_code == 422
    uid, surah, ayah, day, sig = q["question_token"].split(".")
    forged = ".".join((uid, surah, "1", day, sig))
    r = await client.post(
        "/api/v1/check/answer", headers=h_alice, json={"question_token": forged, "choice": 0}
    )
    assert r.status_code == 422


async def test_bare_check_falls_back_to_juz_30(client):
    h = await _login(client)
    q = (await client.get("/api/v1/check/question", headers=h)).json()
    assert q["guessed_span"] is True and q["span"]["start_surah"] == 78


# --- progress -----------------------------------------------------------------------


async def test_progress_numbers_match_the_spec_and_forget_lowers_them(client):
    h = await _login(client)
    store = await get_store()
    await store.hifz.add_interval(ALICE, 67, 1, 8)
    p = (await client.get("/api/v1/progress", headers=h)).json()
    assert p["focus"]["surah"] == 67 and p["focus"]["percent_text"] == "27"

    await store.hifz.add_interval(ALICE, 67, 5, 10)
    p = (await client.get("/api/v1/progress", headers=h)).json()
    assert p["focus"]["percent_text"] == "33"

    detail = (await client.get("/api/v1/progress/surah/67", headers=h)).json()
    assert detail["memorized"] == [{"start_ayah": 1, "end_ayah": 10}]

    r = (await client.post("/api/v1/progress/forget", headers=h, json={"ref": "67:9-10"})).json()
    assert r["removed"] is True and r["progress"]["focus"]["done"] == 8
    r = (await client.post("/api/v1/progress/forget", headers=h, json={"ref": "2:1-5"})).json()
    assert r["removed"] is False


# --- leaderboard -------------------------------------------------------------------


async def test_opted_out_user_is_absent_from_the_board(client):
    from services.streaks import record_session

    h_alice = await _login(client, ALICE)
    await _login(client, BOB)
    await client.patch(
        "/api/v1/me/profile",
        headers=h_alice,
        json={"display_name": "Alice", "leaderboard_opt_in": True},
    )
    await record_session(ALICE, KIND_DRILL, surah=67, start_ayah=1, end_ayah=2)
    await record_session(BOB, KIND_DRILL, surah=67, start_ayah=1, end_ayah=2)

    board = (await client.get("/api/v1/leaderboard", headers=h_alice)).json()
    assert [(e["display_name"], e["is_me"]) for e in board["entries"]] == [("Alice", True)]
    assert "user_id" not in json.dumps(board)
    assert board["opted_in"] and board["me_in_top"]


async def test_streak_shape(client):
    h = await _login(client)
    s = (await client.get("/api/v1/streak", headers=h)).json()
    assert s["current"] == 0 and s["activity"] == []
    assert date.fromisoformat(s["window_start"]).weekday() == 0
    assert (date.fromisoformat(s["today"]) - date.fromisoformat(s["window_start"])).days < 84


async def test_me_carries_plan_and_streak(client):
    h = await _login(client)
    await client.post("/api/v1/plans", headers=h, json={**PLAN, "reminder_time": "05:00"})
    me = (await client.get("/api/v1/me", headers=h)).json()
    assert me["plan"]["target"] == "Al-Mulk" and me["plan"]["day"] == 1
    assert me["profile"]["reminder_time"] == "05:00"
    assert "+05:00" in me["offsets"]
    assert dtime(5, 0) == (await (await get_store()).profiles.get_profile(ALICE)).reminder_time
