"""The /reciter picker: paging through the whole catalog, bitrates on the buttons,
and search by name or quality.

The catalog is ~80 entries, so the picker pages rather than dumps; each button
carries the bitrate because that is what tells two recordings of the same reciter
apart and what decides how much storage a recitation costs.
"""

from unittest.mock import AsyncMock

import pytest
import telegram

import main
from lib.utils import File
from lib.user_settings import UserSettings


@pytest.fixture(scope="module")
def data():
    return main.build_data()


@pytest.fixture(scope="module")
def tg_bot():
    return telegram.Bot("123456:TEST-abcdefghijklmnopqrstuvwxyz")


@pytest.fixture
def fake_bot():
    return AsyncMock()


def _message(tg_bot, text, chat_id=558000, lang="en"):
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


def _callback(tg_bot, cb_data, chat_id=558000, update_id=2):
    payload = {
        "update_id": update_id,
        "callback_query": {
            "id": "cbq-%d" % update_id,
            "from": {"id": chat_id, "is_bot": False, "first_name": "Tester"},
            "chat_instance": "ci-1",
            "data": cb_data,
            "message": {
                "message_id": 5,
                "date": 1700000000,
                "chat": {"id": chat_id, "type": "private"},
            },
        },
    }
    return telegram.Update.de_json(payload, tg_bot)


def _reciter_buttons(markup):
    """The setreciter buttons on a picker keyboard, pager and search row excluded."""
    return [b for row in markup.inline_keyboard for b in row
            if (b.callback_data or "").startswith("setreciter:")]


def _pager_row(markup):
    return next(row for row in markup.inline_keyboard
                if any((b.callback_data or "").startswith("recpage:") for b in row))


class TestCatalogOrder:

    def test_holds_every_performer_exactly_once(self):
        catalog = main.reciter_catalog()
        subfolders = [p["subfolder"] for p in catalog]
        assert sorted(subfolders) == sorted(p["subfolder"] for p in File._load_performers())
        assert len(set(subfolders)) == len(subfolders)

    def test_shortlist_leads_so_page_one_is_the_familiar_names(self):
        catalog = main.reciter_catalog()
        assert [p["subfolder"] for p in catalog[:len(main._RECITER_SHORTLIST)]] == \
            list(main._RECITER_SHORTLIST)

    def test_page_size_matches_the_shortlist(self):
        # Page 1 being exactly the shortlist is the point of the ordering above.
        assert main.RECITER_PAGE_SIZE == len(main._RECITER_SHORTLIST)


class TestLabels:

    def test_button_shows_name_and_bitrate(self):
        label = main.reciter_label({"name": "Husary", "bitrate": "128kbps"})
        assert label == "Husary · 128kbps"

    def test_bitrate_casing_is_normalized(self):
        # performers.json mixes "64kbps" and "64Kbps"; the picker must not.
        assert main.reciter_label({"name": "Balayev", "bitrate": "64Kbps"}) == \
            "Balayev · 64kbps"

    def test_falls_back_to_the_bare_name_without_a_bitrate(self):
        assert main.reciter_label({"name": "Husary"}) == "Husary"

    def test_same_reciter_at_two_bitrates_is_distinguishable(self):
        # The motivating case: two catalog entries share the name "Abdul Basit
        # Murattal" and used to render as two identical buttons.
        labels = [b.text for b in _reciter_buttons(main.reciter_keyboard("en"))]
        murattal = [label for label in labels if label.startswith("Abdul Basit Murattal")]
        assert len(murattal) == len(set(murattal))

    def test_every_button_stays_within_telegrams_callback_data_limit(self):
        for page in range(main.reciter_page_count()):
            for button in _reciter_buttons(main.reciter_keyboard("en", page)):
                assert len(button.callback_data.encode()) <= 64


class TestPagination:

    def test_first_page_is_the_shortlist(self):
        buttons = _reciter_buttons(main.reciter_keyboard("en", 0))
        assert [b.callback_data.split(":", 1)[1] for b in buttons] == \
            list(main._RECITER_SHORTLIST)

    def test_paging_through_reaches_every_reciter(self):
        seen = []
        for page in range(main.reciter_page_count()):
            seen += [b.callback_data.split(":", 1)[1]
                     for b in _reciter_buttons(main.reciter_keyboard("en", page))]
        assert sorted(seen) == sorted(p["subfolder"] for p in main.reciter_catalog())

    def test_pager_shows_the_position_in_the_catalog(self):
        pages = main.reciter_page_count()
        assert pages > 1                                # else there is nothing to page
        indicator = _pager_row(main.reciter_keyboard("en", 2))[1]
        assert indicator.text == "3/%d" % pages

    def test_pages_wrap_so_neither_arrow_is_ever_dead(self):
        pages = main.reciter_page_count()
        first_prev, _, first_next = _pager_row(main.reciter_keyboard("en", 0))
        last_prev, _, last_next = _pager_row(main.reciter_keyboard("en", pages - 1))
        assert first_prev.callback_data == "recpage:%d" % (pages - 1)
        assert first_next.callback_data == "recpage:1"
        assert last_next.callback_data == "recpage:0"
        assert last_prev.callback_data == "recpage:%d" % (pages - 2)

    def test_out_of_range_page_wraps_instead_of_erroring(self):
        pages = main.reciter_page_count()
        assert _reciter_buttons(main.reciter_keyboard("en", pages)) == \
            _reciter_buttons(main.reciter_keyboard("en", 0))

    def test_pager_arrows_follow_reading_direction(self):
        ltr_prev, _, ltr_next = _pager_row(main.reciter_keyboard("en", 1))
        rtl_prev, _, rtl_next = _pager_row(main.reciter_keyboard("ar", 1))
        assert ltr_prev.text.startswith("‹") and ltr_next.text.endswith("›")
        assert rtl_prev.text.endswith("›") and rtl_next.text.startswith("‹")

    def test_search_button_survives_on_every_page(self):
        for page in range(main.reciter_page_count()):
            markup = main.reciter_keyboard("en", page)
            assert any(b.callback_data == "reciter_search"
                       for row in markup.inline_keyboard for b in row)


class TestCurrentReciter:

    def test_active_reciter_is_marked(self):
        buttons = _reciter_buttons(main.reciter_keyboard("en", 0, current="Husary_128kbps"))
        marked = [b.text for b in buttons if b.text.startswith("• ")]
        assert marked == ["• " + main.reciter_label(main.reciter_catalog()[0])]

    def test_page_of_finds_the_reciters_page(self):
        catalog = main.reciter_catalog()
        assert main.reciter_page_of(catalog[0]["subfolder"]) == 0
        target = catalog[main.RECITER_PAGE_SIZE * 2 + 1]["subfolder"]
        assert main.reciter_page_of(target) == 2

    def test_page_of_falls_back_to_the_first_page_for_a_stale_preference(self):
        assert main.reciter_page_of("Retired_Reciter_64kbps") == 0


class TestPickerFlow:

    async def test_reciter_command_opens_on_the_current_reciters_page(self, fake_bot, data,
                                                                     tg_bot):
        catalog = main.reciter_catalog()
        on_page_three = catalog[main.RECITER_PAGE_SIZE * 2]["subfolder"]
        await UserSettings().set_reciter(558001, 558001, on_page_three)

        await main.handle_update(fake_bot, data,
                                 _message(tg_bot, "/reciter", chat_id=558001))

        markup = fake_bot.send_message.await_args.kwargs["reply_markup"]
        assert _pager_row(markup)[1].text.startswith("3/")
        assert any(b.text.startswith("• ") for b in _reciter_buttons(markup))

    async def test_pager_tap_swaps_the_keyboard_in_place(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data,
                                 _callback(tg_bot, "recpage:1", chat_id=558002))

        fake_bot.send_message.assert_not_awaited()      # no new list posted
        kwargs = fake_bot.edit_message_reply_markup.await_args.kwargs
        assert kwargs["message_id"] == 5
        assert _pager_row(kwargs["reply_markup"])[1].text.startswith("2/")
        fake_bot.answer_callback_query.assert_awaited()

    async def test_pager_tap_keeps_marking_the_current_reciter(self, fake_bot, data, tg_bot):
        catalog = main.reciter_catalog()
        on_page_two = catalog[main.RECITER_PAGE_SIZE]["subfolder"]
        await UserSettings().set_reciter(558003, 558003, on_page_two)

        await main.handle_update(fake_bot, data,
                                 _callback(tg_bot, "recpage:1", chat_id=558003))

        markup = fake_bot.edit_message_reply_markup.await_args.kwargs["reply_markup"]
        assert any(b.text.startswith("• ") for b in _reciter_buttons(markup))

    async def test_page_indicator_tap_is_a_no_op(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data,
                                 _callback(tg_bot, "recpage_noop", chat_id=558004))
        fake_bot.answer_callback_query.assert_awaited()
        fake_bot.edit_message_reply_markup.assert_not_awaited()
        fake_bot.send_message.assert_not_awaited()

    async def test_pager_tap_on_a_shared_inline_card_is_ignored(self, fake_bot, data, tg_bot):
        # No message of ours exists there, so there is no keyboard to swap.
        payload = {
            "update_id": 3,
            "callback_query": {
                "id": "cbq-inline",
                "from": {"id": 558005, "is_bot": False, "first_name": "Tester"},
                "chat_instance": "ci-inline",
                "inline_message_id": "AgAAAO0zAAA",
                "data": "recpage:1",
            },
        }
        await main.handle_update(fake_bot, data, telegram.Update.de_json(payload, tg_bot))
        fake_bot.edit_message_reply_markup.assert_not_awaited()
        fake_bot.answer_callback_query.assert_awaited()

    async def test_search_results_carry_the_bitrate(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data,
                                 _callback(tg_bot, "reciter_search", chat_id=558006))
        await main.handle_update(fake_bot, data, _message(tg_bot, "basit", chat_id=558006))

        markup = fake_bot.send_message.await_args.kwargs["reply_markup"]
        buttons = _reciter_buttons(markup)
        assert buttons
        for button in buttons:
            assert "kbps" in button.text


class TestSearch:

    def test_matches_on_name(self):
        assert all("Sudais" in p["name"] for p in File.search_performers("sudais"))

    def test_bitrate_narrows_the_match(self):
        matches = File.search_performers("sudais 192")
        assert [p["subfolder"] for p in matches] == ["Abdurrahmaan_As-Sudais_192kbps"]

    def test_terms_may_arrive_in_any_order(self):
        assert File.search_performers("192 sudais") == File.search_performers("sudais 192")

    def test_unmatched_term_rejects_the_whole_query(self):
        assert File.search_performers("sudais 999") == []

    def test_blank_query_matches_nothing(self):
        assert File.search_performers("   ") == []

    def test_respects_the_limit(self):
        assert len(File.search_performers("a", limit=3)) == 3
