"""The Telegram file_id cache keys every media sender reads and writes.

These strings are persistent state: Redis holds a file_id under each one, so a
key that changes shape silently throws away every cached upload and makes the
bot re-download and re-upload everything. Each case sends once (a miss: built,
uploaded, cached under the exact key) and again (a hit: replayed from that key,
nothing rebuilt).
"""

from io import BytesIO
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

import bot.media as bot_media
import infra.audio as cdn_audio
from lib.utils import File

RECITER = "Husary_128kbps"  # has single-file page audio upstream
STITCHED_RECITER = "Ibrahim_Akhdar_64kbps"  # page audio is stitched from ayahs


def _bot():
    """A bot whose uploads return a distinct file_id per call."""
    counter = {"n": 0}

    def _next_id():
        counter["n"] += 1
        return "FID%d" % counter["n"]

    async def send_photo(**kwargs):
        return SimpleNamespace(photo=[SimpleNamespace(file_id=_next_id())])

    async def send_audio(**kwargs):
        return SimpleNamespace(audio=SimpleNamespace(file_id=_next_id()))

    return SimpleNamespace(
        send_photo=AsyncMock(side_effect=send_photo),
        send_audio=AsyncMock(side_effect=send_audio),
        send_chat_action=AsyncMock(),
        send_message=AsyncMock(),
    )


@pytest.fixture(autouse=True)
def no_cdn(monkeypatch):
    builds = []

    async def stitched_audio(ayahs, performer, name):
        builds.append(("audio", name))
        buf = BytesIO(b"MP3")
        buf.name = name
        return buf

    async def stitched_image(urls, name):
        builds.append(("image", name))
        buf = BytesIO(b"JPG")
        buf.name = name
        return buf

    monkeypatch.setattr(cdn_audio, "download_stitched_audio", stitched_audio)
    monkeypatch.setattr(bot_media, "fetch_and_stitch", stitched_image)
    return builds


def _source(call):
    kwargs = call.kwargs
    return kwargs.get("photo", kwargs.get("audio"))


CASES = [
    (
        "combined range",
        lambda b: bot_media.send_combined_audio(b, 59, 22, 24, 7, RECITER),
        "combined:59:22-24:%s" % RECITER,
        "send_audio",
    ),
    (
        "mushaf page image",
        lambda b: bot_media.send_page(b, 255, 7, "en"),
        "page:255",
        "send_photo",
    ),
    (
        "page audio, single upstream file",
        lambda b: bot_media.send_page_audio(b, 255, 7, RECITER, "en"),
        "pageaudio:255:%s" % RECITER,
        "send_audio",
    ),
    (
        "page audio, stitched",
        lambda b: bot_media.send_page_audio(b, 255, 7, STITCHED_RECITER, "en"),
        "pageaudio:255:%s" % STITCHED_RECITER,
        "send_audio",
    ),
    (
        "repeated ayah",
        lambda b: bot_media.send_repeated_audio(b, 2, 255, 7, RECITER, "en"),
        "repeat:3:2:255:%s" % RECITER,
        "send_audio",
    ),
    (
        "single ayah audio (keyed by its URL)",
        lambda b: bot_media.send_quran(b, {}, 2, 255, "audio", 7, RECITER, "en", "en"),
        "https://cdn.test/audio/%s/002255.mp3" % RECITER,
        "send_audio",
    ),
    (
        "single ayah image (keyed by its URL)",
        lambda b: bot_media.send_quran(b, {}, 2, 255, "arabic", 7, RECITER, "en", "en"),
        "https://cdn.test/images/2_255.png",
        "send_photo",
    ),
]


@pytest.mark.parametrize("name, send, key, method", CASES, ids=[c[0] for c in CASES])
async def test_a_miss_caches_under_the_key_and_a_hit_replays_it(no_cdn, name, send, key, method):
    if name == "page audio, stitched":
        assert not File.has_page_audio(STITCHED_RECITER), "pick a reciter without page audio"
    bot = _bot()
    await send(bot)
    sent = getattr(bot, method)
    assert File().get_file(key) == "FID1", "the upload must be cached under exactly %r" % key
    builds_after_miss = len(no_cdn)

    await send(bot)
    assert _source(sent.await_args_list[-1]) == "FID1", "the second send must replay the cache"
    assert len(no_cdn) == builds_after_miss, "a cache hit must not rebuild anything"


async def test_a_rejected_cached_id_is_rebuilt_and_recached():
    import telegram

    key = "page:255"
    File().save_file(key, "STALE")
    bot = _bot()
    real = bot.send_photo.side_effect

    async def reject_stale(**kwargs):
        if kwargs.get("photo") == "STALE":
            raise telegram.error.BadRequest("wrong file identifier")
        return await real(**kwargs)

    bot.send_photo.side_effect = reject_stale
    await bot_media.send_page(bot, 255, 7, "en")
    assert File().get_file(key) == "FID1"
