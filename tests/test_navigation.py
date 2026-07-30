"""Structural navigation: mushaf pages, juzs and the sajda list.

All of this comes from quran-data.xml, which the bot already shipped and parsed
only the surah names out of. The invariant worth protecting is that the divisions
*tile* the Qur'an: every ayah belongs to exactly one page and exactly one juz, with
no gap between one division's end and the next one's start.
"""

from unittest.mock import AsyncMock

import pytest
import telegram

import main
from modules import Quran


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
        photo=[telegram.PhotoSize("fid", "uid", 100, 100)])
    return bot


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    """Page sends stitch real images off a CDN; the navigation tests only care
    which page was chosen, so the stitch is stubbed out here."""
    async def fake_stitch(urls, name="page.jpg"):
        from io import BytesIO
        buf = BytesIO(b"jpegbytes")
        buf.name = name
        return buf
    monkeypatch.setattr(main, "fetch_and_stitch", fake_stitch)


def _message(tg_bot, text, chat_id=771000, lang="en"):
    payload = {
        "update_id": 1,
        "message": {
            "message_id": 1,
            "date": 1700000000,
            "chat": {"id": chat_id, "type": "private"},
            "from": {"id": chat_id, "is_bot": False, "first_name": "Tester",
                     "language_code": lang},
            "text": text,
        },
    }
    return telegram.Update.de_json(payload, tg_bot)


class TestDivisionsTileTheQuran:

    def test_there_are_the_expected_number_of_each(self):
        assert (Quran.PAGE_COUNT, Quran.JUZ_COUNT) == (604, 30)
        assert (len(Quran.hizbs), len(Quran.manzils), len(Quran.rukus)) == (240, 7, 556)
        assert len(Quran.sajdas) == 15

    @pytest.mark.parametrize("marks_name,count,ranger", [
        ("pages", 604, Quran.page_range),
        ("juzs", 30, Quran.juz_range),
    ])
    def test_divisions_cover_every_ayah_exactly_once(self, marks_name, count, ranger):
        total, previous_end = 0, None
        for n in range(1, count + 1):
            start_s, start_a, end_s, end_a = ranger(n)
            if previous_end is not None:
                # gapless: each division starts on the ayah after the last one ended
                assert Quran.get_next_ayah(*previous_end) == (start_s, start_a)
            previous_end = (end_s, end_a)
            total += len(Quran.ayahs_between((start_s, start_a), (end_s, end_a)))
        assert total == 6236
        assert previous_end == (114, 6)         # ...and the last one ends the Qur'an

    def test_first_and_last_page(self):
        assert Quran.page_range(1) == (1, 1, 1, 7)
        assert Quran.page_range(604) == (112, 1, 114, 6)

    def test_a_page_that_crosses_a_surah_boundary(self):
        # 96 of the 604 pages do this; page 255 runs from the end of Ar-Ra'd into
        # the start of Ibrahim, which is why page media works in (surah, ayah) pairs.
        assert Quran.page_range(255) == (13, 43, 14, 5)
        assert Quran.ayahs_between((13, 43), (14, 5)) == \
            [(13, 43), (14, 1), (14, 2), (14, 3), (14, 4), (14, 5)]

    def test_out_of_range_divisions_return_none(self):
        assert Quran.page_range(0) is None
        assert Quran.page_range(605) is None
        assert Quran.juz_range(0) is None
        assert Quran.juz_range(31) is None

    def test_lookup_is_the_inverse_of_the_range(self):
        for n in (1, 2, 255, 400, 603, 604):
            start_s, start_a, end_s, end_a = Quran.page_range(n)
            assert Quran.page_of(start_s, start_a) == n
            assert Quran.page_of(end_s, end_a) == n

    def test_juz_lookup(self):
        assert Quran.juz_of(1, 1) == 1
        assert Quran.juz_of(78, 1) == 30        # juz 'Amma starts at An-Naba
        assert Quran.juz_range(30) == (78, 1, 114, 6)

    def test_ayahs_between_rejects_a_reversed_span(self):
        assert Quran.ayahs_between((2, 10), (2, 5)) == []

    def test_no_page_exceeds_the_stitching_cap(self):
        # A page with no upstream Page<NNN>.mp3 is assembled from its ayah files,
        # which is only safe while every page stays inside MAX_RANGE_AYAHS.
        longest = max(len(Quran.ayahs_between(Quran.page_range(n)[:2],
                                              Quran.page_range(n)[2:]))
                      for n in range(1, Quran.PAGE_COUNT + 1))
        assert longest <= main.MAX_RANGE_AYAHS


class TestPageCommand:

    async def test_page_number_sends_that_page(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data, _message(tg_bot, "/page 255"))
        caption = fake_bot.send_photo.await_args.kwargs["caption"]
        assert "255" in caption and "13:43" in caption and "14:5" in caption

    async def test_bare_page_opens_where_the_reader_already_is(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data, _message(tg_bot, "2:255", chat_id=771001))
        fake_bot.reset_mock()
        await main.handle_update(fake_bot, data, _message(tg_bot, "/page", chat_id=771001))
        caption = fake_bot.send_photo.await_args.kwargs["caption"]
        assert str(Quran.page_of(2, 255)) in caption

    @pytest.mark.parametrize("text", ["/page 0", "/page 605", "/page abc"])
    async def test_out_of_range_page_explains_the_range(self, fake_bot, data, tg_bot, text):
        await main.handle_update(fake_bot, data, _message(tg_bot, text))
        fake_bot.send_photo.assert_not_awaited()
        assert "604" in fake_bot.send_message.await_args.kwargs["text"]


class TestJuzCommand:

    async def test_juz_opens_its_first_page(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data, _message(tg_bot, "/juz 30"))
        caption = fake_bot.send_photo.await_args.kwargs["caption"]
        assert str(Quran.page_of(78, 1)) in caption

    @pytest.mark.parametrize("text", ["/juz 0", "/juz 31", "/juz abc"])
    async def test_out_of_range_juz_explains_the_range(self, fake_bot, data, tg_bot, text):
        await main.handle_update(fake_bot, data, _message(tg_bot, text))
        fake_bot.send_photo.assert_not_awaited()
        assert "30" in fake_bot.send_message.await_args.kwargs["text"]


class TestSajdaCommand:

    async def test_lists_all_fifteen_as_verse_links(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data, _message(tg_bot, "/sajda"))
        markup = fake_bot.send_message.await_args.kwargs["reply_markup"]
        buttons = [b for row in markup.inline_keyboard for b in row]
        assert len(buttons) == 15
        # every one opens the verse card for its ayah
        for button, (surah, ayah, _kind) in zip(buttons, Quran.sajdas):
            assert button.callback_data == "vc:tr:%d:%d" % (surah, ayah)

    def test_every_sajda_is_a_real_ayah(self):
        for surah, ayah, kind in Quran.sajdas:
            assert Quran.exists(surah, ayah)
            assert kind in ("obligatory", "recommended")


class TestCommandArguments:

    def test_a_bare_reference_is_not_swallowed_as_a_command(self):
        # "/2:255" must still parse as an ayah reference, not a "2:255" command
        assert main.parse_ayah_range("/2:255") == (2, 255, 255)

    def test_non_numeric_argument_is_rejected_rather_than_raising(self):
        assert main._as_int("abc") is None
        assert main._as_int("255") == 255
