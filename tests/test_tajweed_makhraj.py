"""The 3D makhraj screens' data and who sees them (docs/MAKHRAJ_3D_PLAN.md)."""

from collections import Counter
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from bot.features import tajweed as feature
from domain import tajweed_lessons, tajweed_makhraj, tajweed_practice
from domain.uz_translit import to_latin
from infra.store import InMemoryStore
from services import tajweed as service

REVIEWER, USER = 9101, 9102
APP = "https://app.example.test"
ALPHABET = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"


@pytest.fixture(autouse=True)
def env(monkeypatch):
    monkeypatch.setenv("TAJWEED_REVIEWERS", str(REVIEWER))
    monkeypatch.setenv("TAJWEED_AUDIO_BASE_URL", "https://media.example.test/m/")
    monkeypatch.setenv("MINIAPP_URL", APP)
    monkeypatch.delenv("TAJWEED_MAKHRAJ_PUBLIC", raising=False)


# --- the data ----------------------------------------------------------------------


def test_seventeen_makhraj_in_five_regions():
    ms = tajweed_makhraj.makhraj_list()
    assert len(ms) == 17 and len({m.id for m in ms}) == 17
    assert Counter(m.region for m in ms) == {
        "jawf": 1, "throat": 3, "tongue": 10, "lips": 2, "nose": 1,
    }  # fmt: skip


def test_every_pose_is_complete_and_in_range():
    for m in tajweed_makhraj.makhraj_list():
        assert m.contact in tajweed_makhraj.CONTACTS and m.airflow in tajweed_makhraj.AIRFLOWS
        assert len(m.pose["tongue"]) == 5, m.id
        for x, y in m.pose["tongue"]:
            assert -0.6 <= x <= 0.6 and -0.6 <= y <= 0.6, m.id
        for key in tajweed_makhraj.POSE_SCALARS:
            assert 0 <= m.pose[key] <= 1, (m.id, key)
        assert m.name and m.body


def test_thirty_screens_letters_in_alphabet_order_then_madd_and_ghunna():
    screens = tajweed_makhraj.screens()
    assert [s.key for s in screens] == list(ALPHABET) + ["madd", "ghunna"]
    ids = {m.id for m in tajweed_makhraj.makhraj_list()}
    for s in screens:
        assert s.makhraj in ids and set(s.layers) <= set(tajweed_makhraj.LAYERS), s.key
        assert all(0 < v <= 1 for v in s.layers.values())
        assert tajweed_lessons.audio_lesson(s.lesson) is not None, s.key
    # every letter's lesson is the one that teaches it, with the book's title
    for s in screens[:28]:
        assert s.lesson == "ms-%03d" % (tajweed_practice.LETTERS.index(s.key) + 2)
        assert s.title and "harfi" not in s.title
    heavy = {s.key for s in screens if s.layers.get("heavy")}
    assert heavy == set("صضطظغخق")


def test_clips_are_usable_spans_of_their_lesson():
    with_clip = 0
    for s in tajweed_makhraj.screens():
        if s.clip is None:
            continue
        start, end = s.clip
        seconds = tajweed_lessons.audio_lesson(s.lesson).seconds
        assert 0 <= start < end <= seconds + 0.5, s.key
        assert tajweed_makhraj.CLIP_MIN <= end - start <= tajweed_makhraj.CLIP_MAX, s.key
        with_clip += 1
    assert with_clip >= 24  # the rest get hand-set clips while tuning (§2.1)


def test_cyrillic_screens_round_trip():
    for lat, cyr in zip(tajweed_makhraj.screens(), tajweed_makhraj.screens("uz-Cyrl")):
        assert to_latin(cyr.title) == lat.title and cyr.clip == lat.clip
    for lat, cyr in zip(tajweed_makhraj.makhraj_list(), tajweed_makhraj.makhraj_list("uz-Cyrl")):
        assert to_latin(cyr.body) == lat.body


def test_lesson_screens():
    for n in range(2, 30):
        i = tajweed_makhraj.lesson_screen("ms-%03d" % n)
        assert tajweed_makhraj.screens()[i].key == tajweed_practice.LETTERS[n - 2]
    for lesson in (
        "maxraj-kirish",
        "maxraj-bogiz",
        "maxraj-til",
        "maxraj-lab",
        "maxraj-javf-xayshum",
    ):
        assert tajweed_lessons.lesson(lesson) is not None
        assert tajweed_makhraj.lesson_screen(lesson) is not None
    assert tajweed_makhraj.lesson_screen("ms-040") is None
    assert tajweed_makhraj.lesson_screen("idgom") is None


# --- who sees it -------------------------------------------------------------------


def _ctx(user):
    return SimpleNamespace(
        user_id=user, ui_lang="uz", store=InMemoryStore(), tr=lambda key, **kw: key,
        reply=AsyncMock(), edit=AsyncMock(), answer=AsyncMock(),
        channel=SimpleNamespace(send_audio=AsyncMock()), data={},
        reciter="Husary_128kbps", translation_lang="uz",
    )  # fmt: skip


def _web_apps(ctx):
    return [c.web_app for row in ctx.edit.await_args.args[1] for c in row if c.web_app]


async def test_reviewers_only_until_released(monkeypatch):
    assert service.makhraj_visible(REVIEWER) and not service.makhraj_visible(USER)

    reviewer, user = _ctx(REVIEWER), _ctx(USER)
    await feature.on_tajweed(reviewer, "tj:l:ms-015")  # Qof
    await feature.on_tajweed(user, "tj:l:ms-015")
    assert _web_apps(reviewer) == [APP + "/learn/makhraj/20"]
    assert _web_apps(user) == []

    monkeypatch.setenv("TAJWEED_MAKHRAJ_PUBLIC", "1")
    user = _ctx(USER)
    await feature.on_tajweed(user, "tj:l:ms-015")
    assert _web_apps(user) == [APP + "/learn/makhraj/20"]
    await feature.on_tajweed(user, "tj:l:maxraj-lab")
    assert _web_apps(user) == [APP + "/learn/makhraj/1"]  # ب


async def test_no_button_without_the_app_or_on_other_lessons(monkeypatch):
    ctx = _ctx(REVIEWER)
    await feature.on_tajweed(ctx, "tj:l:ms-040")
    assert _web_apps(ctx) == []
    monkeypatch.delenv("MINIAPP_URL")
    await feature.on_tajweed(ctx, "tj:l:ms-015")
    assert _web_apps(ctx) == []
