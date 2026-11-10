"""Tajweed lessons: content checks, transliteration, review flow and the bot feature.

docs/TAJWEED_PLAN.md §5, §6, §8, §11.
"""

import re
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

import bot.features.tajweed as feature
from domain import tajweed, tajweed_lessons
from domain.uz_translit import to_cyrillic, to_latin
from infra.store import InMemoryStore

REVIEWER, USER = 9001, 9002


# --- lessons ---------------------------------------------------------------------------


def test_every_lesson_is_well_formed():
    units = {u.id for u in tajweed_lessons.units()}
    lessons = tajweed_lessons.lessons()
    assert len(lessons) >= 20
    assert len({x.id for x in lessons}) == len(lessons)
    for x in lessons:
        assert x.unit in units, x.id
        assert x.title and x.body
        assert all(r in tajweed.RULES for r in x.rules), x.id
        assert len("tj:p:%s:9" % x.id) <= 64  # fits Telegram callback_data
        for s, a, rules in x.examples:
            assert tajweed.text(s, a)
            if rules:
                assert tajweed.spans(s, a, rules), (x.id, s, a)


def test_lessons_name_no_external_site():
    for x in tajweed_lessons.lessons():
        for text in (x.title, *x.body):
            assert not re.search(r"https?://|www\.|\b[\w-]+\.(uz|com|org|net|ru)\b", text), x.id


def test_cyrillic_is_real_cyrillic_and_round_trips():
    for lat, cyr in zip(tajweed_lessons.lessons("uz"), tajweed_lessons.lessons("uz-Cyrl")):
        assert lat.content_hash == cyr.content_hash  # approval is of the Latin source
        for p, q in zip((lat.title, *lat.body), (cyr.title, *cyr.body)):
            assert to_latin(q) == p
            assert not re.search(r"[a-z]{2,}", re.sub(r"<[^>]*>|&\w+;|/\w+", "", q)), q[:80]
            assert re.findall(r"<[^>]*>", q) == re.findall(r"<[^>]*>", p)  # tags untouched


@pytest.mark.parametrize(
    "lat, cyr",
    [
        ("Oʻzbekcha", "Ўзбекча"),
        ("yoʻqoladi", "йўқолади"),
        ("Yer yuzi", "Ер юзи"),
        ("ekin", "экин"),
        ("Isʼhoq", "Исъҳоқ"),
        ("OʻQISH", "ЎҚИШ"),
        ("<b>gʻunna</b> /language", "<b>ғунна</b> /language"),
        ("Seriya: {days} kun", "Серия: {days} кун"),
    ],
)
def test_transliteration_cases(lat, cyr):
    assert to_cyrillic(lat) == cyr
    assert to_latin(cyr) == lat


# --- bot -------------------------------------------------------------------------------


@pytest.fixture
def store():
    return InMemoryStore()


@pytest.fixture(autouse=True)
def reviewers(monkeypatch):
    monkeypatch.setenv("TAJWEED_REVIEWERS", str(REVIEWER))
    monkeypatch.delenv("TAJWEED_AUDIO_BASE_URL", raising=False)  # rules track only here


def _ctx(store, user=USER, lang="uz"):
    return SimpleNamespace(
        user_id=user,
        ui_lang=lang,
        store=store,
        tr=lambda key, **kw: key,
        reply=AsyncMock(),
        edit=AsyncMock(),
        answer=AsyncMock(),
        channel=object(),
        data={},
        reciter="Husary_128kbps",
        translation_lang="uz",
    )


def _buttons(mock):
    """callback_data of every button in the mock's last call (args: text, choices)."""
    choices = mock.await_args.args[1] if mock.await_args else None
    return [c.data for row in (choices or []) for c in row]


async def test_nothing_published_means_coming_soon(store):
    ctx = _ctx(store)
    await feature.tajvid(ctx)
    assert ctx.reply.await_args.args[0] == "tj_soon"


async def test_reviewer_sees_drafts_and_approves(store):
    first = tajweed_lessons.lessons()[0]
    rev = _ctx(store, REVIEWER)
    await feature.tajvid(rev)
    assert "tj:u:" + first.unit in _buttons(rev.reply)

    await feature.on_tajweed(rev, "tj:l:" + first.id)
    assert "tj:ok:" + first.id in _buttons(rev.edit)
    assert "tj_status_draft" in rev.edit.await_args.args[0]

    await feature.on_tajweed(rev, "tj:ok:" + first.id)
    assert (await store.tajweed.approvals())[first.id].approved_by == REVIEWER

    user = _ctx(store)
    await feature.on_tajweed(user, "tj:l:" + first.id)
    assert user.edit.await_args is not None  # now visible to everyone
    assert "tj:ok:" + first.id not in _buttons(user.edit)  # but no review buttons


async def test_users_cannot_open_or_approve_drafts(store):
    first = tajweed_lessons.lessons()[0]
    user = _ctx(store)
    await feature.on_tajweed(user, "tj:l:" + first.id)
    user.edit.assert_not_awaited()
    user.answer.assert_awaited_with("tj_unavailable")
    await feature.on_tajweed(user, "tj:ok:" + first.id)
    assert await store.tajweed.approvals() == {}


async def test_editing_a_lesson_sends_it_back_to_draft(store):
    first = tajweed_lessons.lessons()[0]
    await store.tajweed.approve(first.id, "an-older-text", REVIEWER)  # approved, then edited
    user = _ctx(store)
    await feature.on_tajweed(user, "tj:l:" + first.id)
    user.edit.assert_not_awaited()


async def test_example_button_plays_the_ayah_in_the_users_reciter(store, monkeypatch):
    lesson = next(x for x in tajweed_lessons.lessons() if x.examples)
    await store.tajweed.approve(lesson.id, lesson.content_hash, REVIEWER)
    played = AsyncMock()
    monkeypatch.setattr(feature, "deliver_quran", played)
    ctx = _ctx(store)
    await feature.on_tajweed(ctx, "tj:p:%s:1" % lesson.id)
    s, a, _ = lesson.examples[0]
    assert played.await_args.args[2:6] == (s, a, "audio", "Husary_128kbps")


@pytest.mark.parametrize(
    "cb", ["tj:p:nope:1", "tj:p:%s:99", "tj:p:%s:x", "tj:l:", "tj:zz", "tj:u:nope:extra"]
)
async def test_bad_callbacks_are_only_acknowledged(store, cb, monkeypatch):
    lesson = next(x for x in tajweed_lessons.lessons() if x.examples)
    await store.tajweed.approve(lesson.id, lesson.content_hash, REVIEWER)
    played = AsyncMock()
    monkeypatch.setattr(feature, "deliver_quran", played)
    ctx = _ctx(store)
    await feature.on_tajweed(ctx, cb.replace("%s", lesson.id))
    played.assert_not_awaited()
    ctx.answer.assert_awaited()


async def test_non_uzbek_users_are_pointed_to_language(store):
    ctx = _ctx(store, lang="en")
    await feature.tajvid(ctx)
    assert ctx.reply.await_args.args[0] == "tj_uzbek_only"


def test_command_is_in_the_uzbek_menu_only():
    from app.lifespan import _commands_for

    assert "tajvid" in [c.command for c in _commands_for("uz")]
    assert "tajvid" not in [c.command for c in _commands_for("en")]
    assert "tajvid" not in [c.command for c in _commands_for("ru")]
