"""Mushaf page mode: stitching a page image, and sending its recitation.

everyayah.com has no full-page image, so a page is assembled from its per-ayah
PNGs. Two things make that safe to do on a small instance and they are what these
tests pin down: the result must stay inside Telegram's photo limits, and the
expensive work must happen once per page rather than once per reader.

Nothing here touches the network — images are generated in-process with Pillow.
"""

from io import BytesIO
from unittest.mock import AsyncMock

import pytest
import telegram
from PIL import Image

import main
from lib import page_image
from lib.utils import File
from modules import Quran


def _png(width: int, height: int, colour=(0, 0, 0)) -> bytes:
    """An encoded PNG standing in for one ayah's rendering."""
    buf = BytesIO()
    Image.new("RGB", (width, height), colour).save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture(scope="module")
def data():
    return main.build_data()


@pytest.fixture(scope="module")
def tg_bot():
    return telegram.Bot("123456:TEST-abcdefghijklmnopqrstuvwxyz")


@pytest.fixture
def fake_bot():
    bot = AsyncMock()
    bot.send_photo.return_value = telegram.Message(
        1, None, telegram.Chat(1, "private"),
        photo=[telegram.PhotoSize("photo-file-id", "uid", 100, 100)])
    bot.send_audio.return_value = telegram.Message(
        1, None, telegram.Chat(1, "private"),
        audio=telegram.Audio("audio-file-id", "uid", 120))
    return bot


class TestStitching:

    def test_strips_are_concatenated_top_to_bottom(self):
        out = page_image.stitch_images([_png(1500, 100), _png(1500, 250), _png(1500, 40)])
        assert Image.open(out).size == (1500, 390)

    def test_result_is_a_jpeg(self):
        # JPEG rather than PNG: these are black text on white, where JPEG is far
        # smaller, and size is the constraint that bites on a long page.
        assert Image.open(page_image.stitch_images([_png(1500, 100)])).format == "JPEG"

    def test_narrower_strips_are_centred_on_the_widest(self):
        out = page_image.stitch_images([_png(1500, 50), _png(700, 50)])
        image = Image.open(out)
        assert image.size == (1500, 100)
        # the narrow strip is centred, so both margins are white
        assert image.convert("RGB").getpixel((10, 75)) == (255, 255, 255)
        assert image.convert("RGB").getpixel((1490, 75)) == (255, 255, 255)

    def test_empty_input_is_an_error_rather_than_a_blank_page(self):
        with pytest.raises(ValueError):
            page_image.stitch_images([])

    def test_an_over_tall_page_is_downscaled_into_telegrams_limits(self):
        # 1500 x 12000 would be rejected by sendPhoto (width + height > 10000)
        out = page_image.stitch_images([_png(1500, 4000) for _ in range(3)])
        width, height = Image.open(out).size
        assert width + height <= page_image.TELEGRAM_MAX_DIMENSION_SUM

    def test_an_ordinary_page_is_left_at_full_resolution(self):
        out = page_image.stitch_images([_png(1500, 200) for _ in range(6)])
        assert Image.open(out).size == (1500, 1200)

    def test_output_stays_under_the_upload_cap(self):
        out = page_image.stitch_images([_png(1500, 900) for _ in range(5)])
        assert len(out.getvalue()) <= page_image.TELEGRAM_MAX_BYTES


class TestPageCard:

    async def test_sends_the_stitched_image_with_a_pager(self, fake_bot, monkeypatch):
        monkeypatch.setattr(main, "fetch_and_stitch", _stub_stitch())
        await main.send_page(fake_bot, 255, 4001, "en")

        kwargs = fake_bot.send_photo.await_args.kwargs
        assert "255" in kwargs["caption"]
        rows = kwargs["reply_markup"].inline_keyboard
        assert rows[0][1].text == "255/604"

    async def test_caption_names_both_surahs_when_the_page_crosses(self, fake_bot,
                                                                   monkeypatch):
        monkeypatch.setattr(main, "fetch_and_stitch", _stub_stitch())
        await main.send_page(fake_bot, 255, 4002, "en")
        caption = fake_bot.send_photo.await_args.kwargs["caption"]
        assert "13:43" in caption and "14:5" in caption

    async def test_it_asks_for_exactly_the_pages_ayah_images(self, fake_bot, monkeypatch):
        seen = {}

        async def capture(urls, name="page.jpg"):
            seen["urls"] = urls
            return _buffer()

        monkeypatch.setattr(main, "fetch_and_stitch", capture)
        await main.send_page(fake_bot, 255, 4003, "en")
        assert len(seen["urls"]) == 6           # 13:43 plus 14:1-14:5
        assert seen["urls"][0].endswith("/13_43.png")
        assert seen["urls"][-1].endswith("/14_5.png")

    async def test_the_page_is_stitched_once_and_then_replayed_from_cache(
            self, fake_bot, monkeypatch):
        calls = []

        async def counting(urls, name="page.jpg"):
            calls.append(name)
            return _buffer()

        monkeypatch.setattr(main, "fetch_and_stitch", counting)
        await main.send_page(fake_bot, 100, 4004, "en")
        await main.send_page(fake_bot, 100, 4005, "en")

        assert len(calls) == 1                  # second reader pays nothing
        assert fake_bot.send_photo.await_count == 2
        assert fake_bot.send_photo.await_args.kwargs["photo"] == "photo-file-id"

    async def test_a_rejected_cached_file_id_is_rebuilt(self, fake_bot, monkeypatch):
        monkeypatch.setattr(main, "fetch_and_stitch", _stub_stitch())
        File().save_file("page:7", "stale-file-id")
        fake_bot.send_photo.side_effect = [
            telegram.error.BadRequest("wrong file identifier"),
            telegram.Message(1, None, telegram.Chat(1, "private"),
                             photo=[telegram.PhotoSize("fresh", "uid", 10, 10)]),
        ]
        await main.send_page(fake_bot, 7, 4006, "en")
        assert fake_bot.send_photo.await_count == 2


class TestPageKeyboard:

    def test_pages_wrap_at_both_ends(self):
        first = main.page_keyboard(1, "en").inline_keyboard[0]
        last = main.page_keyboard(604, "en").inline_keyboard[0]
        assert first[0].callback_data == "pg:604"
        assert first[2].callback_data == "pg:2"
        assert last[2].callback_data == "pg:1"

    def test_ayah_view_button_opens_the_pages_first_ayah(self):
        rows = main.page_keyboard(255, "en").inline_keyboard
        ayah_view = rows[1][1]
        assert ayah_view.callback_data == "vc:tr:13:43"

    def test_audio_is_a_button_not_an_attachment(self):
        # a page of recitation is ~1 MB nobody asked for if they only wanted to read
        rows = main.page_keyboard(255, "en").inline_keyboard
        assert rows[1][0].callback_data == "pga:255"

    def test_every_button_stays_within_telegrams_callback_data_limit(self):
        for page in (1, 255, 604):
            for row in main.page_keyboard(page, "en").inline_keyboard:
                for button in row:
                    if button.callback_data:
                        assert len(button.callback_data.encode()) <= 64


class TestPageAudio:

    async def test_uses_the_single_page_file_when_the_reciter_has_one(self, fake_bot):
        assert File.has_page_audio("Husary_128kbps")
        await main.send_page_audio(fake_bot, 255, 4007, "Husary_128kbps", "en")
        source = fake_bot.send_audio.await_args.kwargs["audio"]
        assert source.endswith("/Husary_128kbps/PageMp3s/Page255.mp3")

    async def test_falls_back_to_stitching_when_the_reciter_has_none(self, fake_bot,
                                                                     monkeypatch):
        reciter = "Nasser_Alqatami_128kbps"
        assert not File.has_page_audio(reciter)
        seen = {}

        async def capture(ayahs, performer, name):
            seen["ayahs"] = ayahs
            buf = BytesIO(b"mp3")
            buf.name = name
            return buf

        monkeypatch.setattr(main, "_download_stitched_audio", capture)
        await main.send_page_audio(fake_bot, 255, 4008, reciter, "en")

        # the fallback has to cross the surah boundary this page sits on
        assert seen["ayahs"] == [(13, 43), (14, 1), (14, 2), (14, 3), (14, 4), (14, 5)]

    async def test_page_audio_is_cached_per_reciter(self, fake_bot):
        await main.send_page_audio(fake_bot, 300, 4009, "Husary_128kbps", "en")
        await main.send_page_audio(fake_bot, 300, 4010, "Husary_128kbps", "en")
        assert fake_bot.send_audio.await_args.kwargs["audio"] == "audio-file-id"

        # a different reciter must not be served the first one's recording
        fake_bot.reset_mock()
        fake_bot.send_audio.return_value = telegram.Message(
            1, None, telegram.Chat(1, "private"), audio=telegram.Audio("other", "u", 1))
        await main.send_page_audio(fake_bot, 300, 4011, "Alafasy_128kbps", "en")
        assert fake_bot.send_audio.await_args.kwargs["audio"] != "audio-file-id"


class TestRepeatForMemorization:
    """Repeating an ayah is the same concatenation a range uses, with the ayah
    listed more than once — so it needs no timing data and works for every
    reciter in the catalog, not only the ones upstream published timings for."""

    async def test_it_sends_the_ayah_the_configured_number_of_times(self, fake_bot,
                                                                    monkeypatch):
        seen = {}

        async def capture(ayahs, performer, name):
            seen.update(ayahs=ayahs, name=name, performer=performer)
            return BytesIO(b"mp3")

        monkeypatch.setattr(main, "_download_stitched_audio", capture)
        await main.send_repeated_audio(fake_bot, 2, 255, 5001, "Husary_128kbps", "en")

        assert seen["ayahs"] == [(2, 255)] * main.REPEAT_COUNT
        assert seen["performer"] == "Husary_128kbps"

    async def test_the_title_says_how_many_times(self, fake_bot, monkeypatch):
        monkeypatch.setattr(main, "_download_stitched_audio", _stub_audio())
        await main.send_repeated_audio(fake_bot, 2, 255, 5002, "Husary_128kbps", "en")
        title = fake_bot.send_audio.await_args.kwargs["title"]
        assert title == "Qur'an 2:255 ×%d" % main.REPEAT_COUNT

    async def test_it_is_built_once_and_then_replayed_from_cache(self, fake_bot,
                                                                 monkeypatch):
        calls = []

        async def counting(ayahs, performer, name):
            calls.append(name)
            return BytesIO(b"mp3")

        monkeypatch.setattr(main, "_download_stitched_audio", counting)
        await main.send_repeated_audio(fake_bot, 2, 255, 5003, "Husary_128kbps", "en")
        await main.send_repeated_audio(fake_bot, 2, 255, 5004, "Husary_128kbps", "en")

        assert len(calls) == 1
        assert fake_bot.send_audio.await_args.kwargs["audio"] == "audio-file-id"

    async def test_a_different_reciter_gets_its_own_recording(self, fake_bot,
                                                              monkeypatch):
        monkeypatch.setattr(main, "_download_stitched_audio", _stub_audio())
        await main.send_repeated_audio(fake_bot, 2, 255, 5005, "Husary_128kbps", "en")
        fake_bot.reset_mock()
        fake_bot.send_audio.return_value = telegram.Message(
            1, None, telegram.Chat(1, "private"), audio=telegram.Audio("other", "u", 1))
        await main.send_repeated_audio(fake_bot, 2, 255, 5006, "Alafasy_128kbps", "en")
        assert fake_bot.send_audio.await_args.kwargs["audio"] != "audio-file-id"

    async def test_it_works_for_a_reciter_with_no_upstream_timings(self, fake_bot,
                                                                   monkeypatch):
        # the point of dropping the timings files: coverage is the whole catalog
        monkeypatch.setattr(main, "_download_stitched_audio", _stub_audio())
        await main.send_repeated_audio(fake_bot, 36, 1, 5007, "Yaser_Salamah_128kbps", "en")
        fake_bot.send_audio.assert_awaited()


class TestStitchedAudioAcrossSurahs:

    async def test_a_range_within_one_surah_keeps_its_filename(self, monkeypatch):
        captured = {}

        async def fake_download(ayahs, performer, name):
            captured.update(ayahs=ayahs, name=name)
            return BytesIO(b"")

        monkeypatch.setattr(main, "_download_stitched_audio", fake_download)
        await main._download_combined_audio(59, 22, 24, "Husary_128kbps")
        assert captured["ayahs"] == [(59, 22), (59, 23), (59, 24)]
        assert captured["name"] == "quran_59_22-24.mp3"


def _buffer(name="page.jpg"):
    buf = BytesIO(b"jpeg-bytes")
    buf.name = name
    return buf


def _stub_stitch():
    async def stub(urls, name="page.jpg"):
        return _buffer(name)
    return stub


def _stub_audio():
    async def stub(ayahs, performer, name):
        buf = BytesIO(b"mp3")
        buf.name = name
        return buf
    return stub
