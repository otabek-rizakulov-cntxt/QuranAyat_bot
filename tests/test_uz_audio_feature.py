"""Uzbek translation audio: byte math, parts, Range fetch, keyboard and callbacks.

Runs against a synthetic timing table whose al-Baqarah entry reproduces the
worked example in docs/MULTILINGUAL_PLAN.md §8.1.3 (2:284 = bytes
108409104-108808703, cut by ear and approved), so no network and no generated
data file is needed.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import httpx
import pytest

import bot.features.uz_audio as feature
import infra.uz_audio as uz_audio
import infra.uz_audio_delivery as delivery
from bot.keyboards.verse import verse_keyboard
from bot.limits import MAX_RANGE_AYAHS

FB = 432  # 96 kbps at 32 kHz
SIZE_2 = 110147040
FRAMES_2 = SIZE_2 // FB
A284, A285, A286 = 108409104 // FB, 108808704 // FB, 109370304 // FB


def _baqarah() -> dict:
    # 283 evenly spaced ayahs up to the measured start of 284, then the real cuts.
    starts = [1000 + (A284 - 1000) * k // 283 for k in range(283)] + [A284, A285, A286]
    ends = starts[1:] + [FRAMES_2 - 50]
    return {
        "kbps": 96,
        "sample_rate": 32000,
        "frame_bytes": FB,
        "frames": FRAMES_2,
        "size": SIZE_2,
        "status": "estimated",
        "ver": "abc123",
        "ayahs": [[s, e, 0.9] for s, e in zip(starts, ends)],
    }


def _fatiha() -> dict:
    return {
        "kbps": 320,
        "sample_rate": 32000,
        "frame_bytes": 1440,
        "frames": 2524,
        "size": 3634560,
        "status": "verified",
        "ver": "f00",
        "ayahs": [[1072 + 200 * k, 1072 + 200 * (k + 1), 1.0] for k in range(7)],
    }


@pytest.fixture(autouse=True)
def table():
    uz_audio.reset_for_tests({"1": _fatiha(), "2": _baqarah()})
    yield
    uz_audio.reset_for_tests()


# --- byte math ---------------------------------------------------------------------


def test_worked_example_ranges():
    assert uz_audio.byte_range(2, 284, 284) == (108409104, 108808703)
    assert uz_audio.byte_range(2, 284, 285) == (108409104, 109370303)


def test_seconds_match_the_approved_cuts():
    start, end = uz_audio.seconds(2, 284, 285)
    assert start == pytest.approx(9034.1, abs=0.04)
    assert end == pytest.approx(9114.2, abs=0.04)


def test_out_of_range_ayah_is_refused():
    with pytest.raises(ValueError):
        uz_audio.byte_range(2, 286, 287)


def test_parts_cover_the_file_on_ayah_boundaries():
    parts = uz_audio.parts(2)
    assert parts[0].start_byte == 0 and parts[0].first_ayah == 1
    assert parts[-1].end_byte == SIZE_2 - 1 and parts[-1].last_ayah == 286
    for a, b in zip(parts, parts[1:]):
        assert b.start_byte == a.end_byte + 1  # no gap, no overlap
        assert b.first_ayah == a.last_ayah + 1
        assert b.start_byte == uz_audio.byte_range(2, b.first_ayah, b.first_ayah)[0]
    assert all(p.end_byte - p.start_byte + 1 <= uz_audio.PART_LIMIT for p in parts)


def test_small_surah_is_one_part():
    assert len(uz_audio.parts(1)) == 1


# --- Range fetch ---------------------------------------------------------------------


def _patch_client(monkeypatch, handler):
    real = httpx.AsyncClient

    def client(**kwargs):
        return real(transport=httpx.MockTransport(handler), **kwargs)

    monkeypatch.setattr(uz_audio.httpx, "AsyncClient", client)


async def test_fetch_sends_the_range_and_returns_the_bytes(monkeypatch):
    seen = {}

    def handler(request):
        seen["range"] = request.headers["Range"]
        seen["url"] = str(request.url)
        return httpx.Response(206, content=b"\xff\xfb" + b"\0" * 98)

    _patch_client(monkeypatch, handler)
    buf = await uz_audio.fetch(2, 1000, 1099, "x.mp3")
    assert seen == {"range": "bytes=1000-1099", "url": "https://newbooks.uz/audio/t1/002.mp3"}
    assert len(buf.getvalue()) == 100 and buf.name == "x.mp3"


@pytest.mark.parametrize(
    "response",
    [
        httpx.Response(200, content=b"\xff\xfb" + b"\0" * 98),  # Range ignored
        httpx.Response(206, content=b"\xff\xfb" + b"\0" * 10),  # short
        httpx.Response(206, content=b"\0" * 100),  # not on a frame: file changed upstream
    ],
)
async def test_fetch_rejects_a_bad_response(monkeypatch, response):
    _patch_client(monkeypatch, lambda request: response)
    with pytest.raises(OSError):
        await uz_audio.fetch(2, 1000, 1099, "x.mp3")


# --- keyboard ------------------------------------------------------------------------


def _data(choices):
    return [c.data for row in choices for c in row if c.data]


@pytest.mark.parametrize("lang", ["uz", "uz-Cyrl"])
def test_uzbek_users_get_the_row(lang):
    data = _data(verse_keyboard(2, 284, "translation", lang))
    assert "uz:a:2:284" in data and "uz:s:2" in data


@pytest.mark.parametrize("lang", ["en", "ru", "tr"])
def test_other_users_do_not(lang):
    assert not any(d.startswith("uz:") for d in _data(verse_keyboard(2, 284, "translation", lang)))


def test_no_row_without_timings():
    uz_audio.reset_for_tests({})
    assert not any(d.startswith("uz:") for d in _data(verse_keyboard(2, 284, "translation", "uz")))


# --- sending -------------------------------------------------------------------------


class FakeChannel:
    """Records sends; builds the source like a cache miss would."""

    def __init__(self):
        self.sent = []

    async def send_audio(self, source, **kwargs):
        if callable(source):
            source = await source()
        self.sent.append(SimpleNamespace(source=source, **kwargs))


@pytest.fixture
def fetched(monkeypatch):
    calls = []

    async def fake_fetch(surah, start, end, name):
        calls.append((surah, start, end))
        return name

    monkeypatch.setattr(uz_audio, "fetch", fake_fetch)
    return calls


async def test_clip_fetches_its_range_and_marks_estimated(fetched):
    ch = FakeChannel()
    await delivery.send_clip(ch, 2, 284, 284, "uz")
    assert fetched == [(2, 108409104, 108808703)]
    sent = ch.sent[0]
    assert sent.cache_key == "uzt:abc123:2:284-284"
    assert "2:284" in sent.title
    assert "taxminiy" in sent.caption
    assert "uz:a:2:285" in _data(sent.choices) and "uz:a:2:283" in _data(sent.choices)


async def test_verified_surah_has_no_estimate_note(fetched):
    ch = FakeChannel()
    await delivery.send_clip(ch, 1, 1, 7, "uz")
    assert "taxminiy" not in ch.sent[0].caption
    assert ch.sent[0].choices is None  # a range gets no ◀/▶


async def test_small_surah_goes_by_url(fetched):
    ch = FakeChannel()
    await delivery.send_surah(ch, 1, "uz")
    assert fetched == []  # Telegram fetches the URL itself
    assert ch.sent[0].source == "https://newbooks.uz/audio/t1/001.mp3"
    assert ch.sent[0].cache_key == "uzt:1"


async def test_big_surah_goes_in_parts(fetched):
    ch = FakeChannel()
    await delivery.send_surah(ch, 2, "uz")
    parts = uz_audio.parts(2)
    assert len(ch.sent) == len(parts) > 1
    assert fetched == [(2, p.start_byte, p.end_byte) for p in parts]
    assert [s.cache_key for s in ch.sent] == ["uzt:abc123:2:p%d" % p.index for p in parts]
    assert "1/%d" % len(parts) in ch.sent[0].title


def test_clip_cap_matches_the_bot_range_cap():
    assert delivery.MAX_CLIP_AYAHS == MAX_RANGE_AYAHS


def test_cache_keys_follow_the_timing_version():
    before = delivery.ayah_key(2, 284, 284)
    table = _baqarah()
    table["ver"] = "def456"
    uz_audio.reset_for_tests({"2": table})
    assert delivery.ayah_key(2, 284, 284) != before


@pytest.mark.parametrize(
    "cb, want",
    [
        ("uz:a:2:284", ("a", 2, 284, 284)),
        ("uz:r:2:284:285", ("r", 2, 284, 285)),
        ("uz:s:2", ("s", 2, 1, 1)),
        ("uz:a:2:999", None),
        ("uz:r:2:285:284", None),
        ("uz:r:2:1:200", None),  # over MAX_RANGE_AYAHS
        ("uz:a:3:1", None),  # no timings for surah 3
        ("uz:x:2", None),
        ("uz:a:two:1", None),
    ],
)
def test_parse(cb, want):
    assert feature.parse(cb) == want


async def test_tap_sends_and_acknowledges(fetched):
    ch = FakeChannel()
    ctx = SimpleNamespace(ui_lang="uz", channel=ch, answer=AsyncMock(), reply=AsyncMock())
    await feature.on_uz_audio(ctx, "uz:r:2:284:285")
    ctx.answer.assert_awaited_once_with()
    assert fetched == [(2, 108409104, 109370303)]


async def test_source_failure_is_reported_not_raised(monkeypatch):
    async def broken(*args):
        raise OSError("down")

    monkeypatch.setattr(uz_audio, "fetch", broken)
    ctx = SimpleNamespace(
        ui_lang="uz", channel=FakeChannel(), answer=AsyncMock(), reply=AsyncMock()
    )
    await feature.on_uz_audio(ctx, "uz:a:2:284")
    ctx.reply.assert_awaited_once()


# --- Mini App "send to chat" -----------------------------------------------------------


async def test_api_send_runs_the_bot_feature(monkeypatch, fetched):
    import json as _json
    import time

    import main
    from api.auth import sign_init_data
    from config import get_settings

    monkeypatch.setenv("MINIAPP_JWT_SECRET", "test-jwt-secret-not-real")
    sent = []

    async def fake_send(bot, user_id, surah, first, last, ui_lang):
        sent.append((user_id, surah, first, last))

    monkeypatch.setattr("api.uz_audio.send_to_user", fake_send)
    monkeypatch.setattr(main.app.state.runtime, "bot", object(), raising=False)
    transport = httpx.ASGITransport(app=main.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        init = sign_init_data(
            {
                "auth_date": str(int(time.time())),
                "signature": "c2ln",
                "user": _json.dumps({"id": 7101, "first_name": "U", "language_code": "uz"}),
            },
            get_settings().token,
        )
        token = (await client.post("/api/v1/auth/telegram", json={"init_data": init})).json()
        h = {"Authorization": "Bearer " + token["access_token"]}
        r = await client.post(
            "/api/v1/uz-audio/send", headers=h, json={"surah": 2, "start": 284, "end": 285}
        )
        assert r.status_code == 200, r.text
        assert sent == [(7101, 2, 284, 285)]
        r = await client.post("/api/v1/uz-audio/send", headers=h, json={"surah": 3, "start": 1})
        assert r.status_code == 404  # no timings for surah 3 in this table
        r = await client.post("/api/v1/uz-audio/send", headers=h, json={"surah": 2, "start": 290})
        assert r.status_code == 422
