"""Inline mode over an ayah *range*: `@bot 59:22-24` must answer with all three
ayahs, not just the first — and every representation (translation, tafsir,
recitation, Arabic image) must cover the whole range.

Same shape as test_inline_reciter_search.py: real telegram.Update objects in, an
AsyncMock bot out, so we assert on what the handler tried to answer with. The
stitching route is exercised directly (it is a plain async function) rather than
over HTTP, which would drag the app's startup hooks in.
"""

from unittest.mock import AsyncMock

import httpx
import pytest
import telegram

import main
from lib.utils import File
from lib.user_settings import UserSettings
from modules import TranslationRegistry


@pytest.fixture(scope="module")
def data():
    return main.build_data()


@pytest.fixture(scope="module")
def tg_bot():
    return telegram.Bot("123456:TEST-abcdefghijklmnopqrstuvwxyz")


@pytest.fixture
def fake_bot():
    return AsyncMock()


@pytest.fixture
def public_url(monkeypatch):
    """A public base URL, without which no range recitation can be offered."""
    monkeypatch.setenv("WEBHOOK_URL", "https://bot.test")
    return "https://bot.test"


def _inline_query(tg_bot, query, user_id=557000, lang="en"):
    payload = {
        "update_id": 1,
        "inline_query": {
            "id": "iq-%d" % user_id,
            "from": {"id": user_id, "is_bot": False, "first_name": "Tester",
                     "language_code": lang},
            "query": query,
            "offset": "",
        },
    }
    return telegram.Update.de_json(payload, tg_bot)


def _results(fake_bot):
    return fake_bot.answer_inline_query.await_args.kwargs["results"]


def _of_type(fake_bot, *types):
    return [r for r in _results(fake_bot) if isinstance(r, types)]


class TestRangeText:

    async def test_translation_covers_every_ayah_in_the_range(self, fake_bot, data, tg_bot):
        quran = TranslationRegistry.get("en")

        await main.handle_update(fake_bot, data, _inline_query(tg_bot, "59:22-24"))

        translation = _results(fake_bot)[0].input_message_content.message_text
        # the bug this test exists for: only 59:22 used to come back
        assert translation == quran.get_ayahs(59, 22, 24)
        assert translation.endswith("(59:22-24)")
        for ayah in (22, 23, 24):
            # each ayah's own words, minus the "(59:N)" reference get_ayah appends
            assert quran.get_ayah(59, ayah).rsplit(" (", 1)[0] in translation

    async def test_tafsir_covers_every_ayah_in_the_range(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "59:22-24", user_id=557001))
        tafsir = _results(fake_bot)[1].input_message_content.message_text
        for ayah in (22, 23, 24):
            assert "(59:%d)" % ayah in tafsir

    async def test_long_range_text_stays_within_telegrams_message_limit(
            self, fake_bot, data, tg_bot):
        # Surah 2's first 50 ayahs run well past 4096 characters in both views.
        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "2:1-50", user_id=557002))
        for result in _results(fake_bot)[:2]:
            assert len(result.input_message_content.message_text) <= 4096

    async def test_single_ayah_is_unchanged(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "2:255", user_id=557003))
        translation = _results(fake_bot)[0].input_message_content.message_text
        assert translation.endswith("(2:255)")


class TestRangeAudio:

    async def test_offers_one_combined_recitation_of_the_whole_range(
            self, fake_bot, data, tg_bot, public_url):
        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "59:22-24", user_id=557010))

        audio = _of_type(fake_bot, telegram.InlineQueryResultAudio)
        assert len(audio) == 1                  # one file for 22-24, not one per ayah
        assert audio[0].audio_url == (
            public_url + "/media/range.mp3"
            "?surah=59&start=22&end=24&reciter=Husary_128kbps")
        assert audio[0].title == main._reference(59, 22, "en", 24)
        assert len(audio[0].id.encode()) <= 64  # Telegram's hard limit on result ids

    async def test_recitation_follows_the_callers_reciter(self, fake_bot, data, tg_bot,
                                                          public_url):
        await UserSettings().set_reciter(557011, None, "Alafasy_128kbps")

        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "59:22-24", user_id=557011))

        audio = _of_type(fake_bot, telegram.InlineQueryResultAudio)[0]
        assert "reciter=Alafasy_128kbps" in audio.audio_url

    async def test_replays_the_file_id_an_in_chat_send_left_behind(
            self, fake_bot, data, tg_bot, public_url):
        # Telegram already holds this stitched file; re-fetching and re-stitching it
        # would be pure waste, so the cached id wins over the URL.
        File().save_file("combined:59:22-24:Husary_128kbps", "CACHED-FILE-ID")

        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "59:22-24", user_id=557012))

        cached = _of_type(fake_bot, telegram.InlineQueryResultCachedAudio)
        assert len(cached) == 1
        assert cached[0].audio_file_id == "CACHED-FILE-ID"
        assert cached[0].caption == main._reference(59, 22, "en", 24)
        assert not _of_type(fake_bot, telegram.InlineQueryResultAudio)

    async def test_dropped_without_a_public_base_url(self, fake_bot, data, tg_bot):
        # WEBHOOK_URL is unset here: there is nowhere for Telegram to fetch the
        # stitched file from, so the answer drops the audio instead of offering a
        # link that would 404.
        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "59:22-24", user_id=557013))
        assert not _of_type(fake_bot, telegram.InlineQueryResultAudio,
                            telegram.InlineQueryResultCachedAudio)
        assert _results(fake_bot)                # the rest of the answer survives

    async def test_dropped_when_the_range_exceeds_the_stitching_cap(
            self, fake_bot, data, tg_bot, public_url):
        too_many = main.MAX_RANGE_AYAHS + 1
        await main.handle_update(
            fake_bot, data,
            _inline_query(tg_bot, "2:1-%d" % too_many, user_id=557014))
        assert not _of_type(fake_bot, telegram.InlineQueryResultAudio,
                            telegram.InlineQueryResultCachedAudio)

    async def test_single_ayah_still_comes_straight_from_the_cdn(self, fake_bot, data,
                                                                 tg_bot, public_url):
        # No stitching needed for one ayah, so it must not be routed through us.
        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "2:255", user_id=557015))
        audio = _of_type(fake_bot, telegram.InlineQueryResultAudio)[0]
        assert audio.audio_url == "https://cdn.test/audio/Husary_128kbps/002255.mp3"


class TestInlineArabicImage:

    async def test_single_ayah_offers_its_rendered_image(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "2:255", user_id=557020))
        photos = _of_type(fake_bot, telegram.InlineQueryResultPhoto)
        assert len(photos) == 1
        assert photos[0].photo_url == "https://cdn.test/images/2_255.png"
        assert photos[0].thumbnail_url == photos[0].photo_url
        assert photos[0].title == main.t("btn_arabic", "en")
        assert photos[0].caption == main._reference(2, 255, "en")

    async def test_range_offers_one_image_per_ayah(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "59:22-24", user_id=557021))
        photos = _of_type(fake_bot, telegram.InlineQueryResultPhoto)
        assert [p.photo_url for p in photos] == [
            "https://cdn.test/images/59_%d.png" % a for a in (22, 23, 24)]
        assert len({p.id for p in photos}) == len(photos)  # Telegram rejects duplicate ids

    async def test_long_range_caps_the_images(self, fake_bot, data, tg_bot, public_url):
        # Telegram accepts at most 50 results per answer, and a wall of thumbnails
        # would bury the text and audio results anyway.
        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "2:1-40", user_id=557022))
        photos = _of_type(fake_bot, telegram.InlineQueryResultPhoto)
        assert len(photos) == main.INLINE_MAX_PHOTOS
        assert len(_results(fake_bot)) <= 50

    async def test_localized_title(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "2:255", user_id=557023, lang="ru"))
        photo = _of_type(fake_bot, telegram.InlineQueryResultPhoto)[0]
        assert photo.title == main.t("btn_arabic", "ru")

    async def test_replays_the_file_id_an_in_chat_send_left_behind(self, fake_bot, data,
                                                                   tg_bot):
        # Our ayah renders are PNG and the Bot API wants a JPEG behind photo_url, so
        # a file Telegram already holds is both cheaper and more dependable.
        File().save_file("https://cdn.test/images/2_255.png", "CACHED-PHOTO-ID")

        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "2:255", user_id=557025))

        cached = _of_type(fake_bot, telegram.InlineQueryResultCachedPhoto)
        assert len(cached) == 1
        assert cached[0].photo_file_id == "CACHED-PHOTO-ID"
        assert cached[0].caption == main._reference(2, 255, "en")
        assert not _of_type(fake_bot, telegram.InlineQueryResultPhoto)

    async def test_local_images_are_offered_only_once_cached(self, fake_bot, data, tg_bot,
                                                             monkeypatch):
        # Telegram fetches photo_url itself; a path on our disk is unreachable to it,
        # so an uncached ayah has nothing to offer while a cached one still does.
        monkeypatch.setenv("PHOTO_BASE_URL", "/srv/quranic_images")
        File().save_file("/srv/quranic_images/2_255.png", "CACHED-PHOTO-ID")

        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "2:254", user_id=557026))
        assert not _of_type(fake_bot, telegram.InlineQueryResultPhoto,
                            telegram.InlineQueryResultCachedPhoto)
        assert _results(fake_bot)                # the rest of the answer survives

        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "2:255", user_id=557026))
        assert _of_type(fake_bot, telegram.InlineQueryResultCachedPhoto)

    async def test_dropped_when_no_images_are_configured(self, fake_bot, data, tg_bot,
                                                         monkeypatch):
        monkeypatch.delenv("PHOTO_BASE_URL")

        await main.handle_update(fake_bot, data,
                                 _inline_query(tg_bot, "2:255", user_id=557027))

        assert not _of_type(fake_bot, telegram.InlineQueryResultPhoto,
                            telegram.InlineQueryResultCachedPhoto)
        assert _results(fake_bot)                # the rest of the answer survives


class TestRangeAudioRoute:
    """The public endpoint Telegram fetches a stitched range from."""

    @staticmethod
    def _stub_download(monkeypatch, content=b"MP3"):
        calls = []

        async def fake_download(surah, start, end, performer):
            calls.append((surah, start, end, performer))
            buf = main.BytesIO(content)
            buf.name = "quran_%d_%d-%d.mp3" % (surah, start, end)
            return buf

        monkeypatch.setattr(main, "_download_combined_audio", fake_download)
        return calls

    async def test_serves_the_stitched_mp3(self, monkeypatch):
        calls = self._stub_download(monkeypatch, b"AYAH22AYAH23AYAH24")

        response = await main.range_audio(59, 22, 24, "Husary_128kbps")

        assert calls == [(59, 22, 24, "Husary_128kbps")]
        assert response.status_code == 200
        assert response.body == b"AYAH22AYAH23AYAH24"
        assert response.media_type == "audio/mpeg"
        assert "quran_59_22-24.mp3" in response.headers["content-disposition"]

    @pytest.mark.parametrize("surah, start, end", [
        (0, 1, 2),                                   # no such surah
        (115, 1, 2),                                 # ditto
        (59, 22, 25),                                # surah 59 ends at 24
        (59, 24, 22),                                # inverted range
        (2, 1, 2 + main.MAX_RANGE_AYAHS),            # past the stitching cap
    ])
    async def test_rejects_references_the_bot_would_never_send(self, monkeypatch,
                                                               surah, start, end):
        calls = self._stub_download(monkeypatch)
        response = await main.range_audio(surah, start, end, "Husary_128kbps")
        assert response.status_code == 404
        assert calls == []                      # rejected before any upstream fetch

    async def test_rejects_a_reciter_outside_the_catalog(self, monkeypatch):
        response = await main.range_audio(59, 22, 24, "Not_A_Reciter_128kbps")
        assert response.status_code == 404

    async def test_reports_an_unreachable_recitation_cdn_as_a_bad_gateway(self, monkeypatch):
        async def boom(*args):
            raise httpx.ConnectError("cdn down")

        monkeypatch.setattr(main, "_download_combined_audio", boom)

        response = await main.range_audio(59, 22, 24, "Husary_128kbps")
        assert response.status_code == 502


class TestStitching:

    async def test_concatenates_the_ayahs_in_order(self, monkeypatch):
        """The stitched file must play 22, 23, 24 in that order even though the
        downloads run concurrently and can finish out of order."""
        bodies = {"022": b"<22>", "023": b"<23>", "024": b"<24>"}

        class FakeResponse:
            def __init__(self, content):
                self.content = content

            def raise_for_status(self):
                pass

        class FakeClient:
            def __init__(self, *args, **kwargs):
                pass

            async def __aenter__(self):
                return self

            async def __aexit__(self, *exc):
                return False

            async def get(self, url):
                return FakeResponse(bodies[url[-7:-4]])

        monkeypatch.setattr(main.httpx, "AsyncClient", FakeClient)

        buf = await main._download_combined_audio(59, 22, 24, "Husary_128kbps")

        assert buf.getvalue() == b"<22><23><24>"
        assert buf.name == "quran_59_22-24.mp3"
