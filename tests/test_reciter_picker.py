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
    """The Previous / n-of-m / Next row — the one carrying the page indicator, which
    is what tells it apart from the group-tab row (both use `recgrp:`)."""
    return next(row for row in markup.inline_keyboard
                if any((b.callback_data or "") == "recpage_noop" for b in row))


def _tab_row(markup):
    """The group-tab row: Reciters / Riwayah / Meaning, always first."""
    return markup.inline_keyboard[0]


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

    def test_paging_through_every_group_reaches_every_reciter(self):
        seen = []
        for kind in main.RECITER_KINDS:
            for page in range(main.reciter_page_count(kind)):
                seen += [b.callback_data.split(":", 1)[1]
                         for b in _reciter_buttons(main.reciter_keyboard("en", kind, page))]
        assert sorted(seen) == sorted(p["subfolder"] for p in main.reciter_catalog())

    def test_pager_shows_the_position_in_the_group(self):
        pages = main.reciter_page_count("recitation")
        assert pages > 1                                # else there is nothing to page
        indicator = _pager_row(main.reciter_keyboard("en", "recitation", 2))[1]
        assert indicator.text == "3/%d" % pages

    def test_pages_wrap_so_neither_arrow_is_ever_dead(self):
        pages = main.reciter_page_count("recitation")
        first_prev, _, first_next = _pager_row(main.reciter_keyboard("en", "recitation", 0))
        last_prev, _, last_next = _pager_row(
            main.reciter_keyboard("en", "recitation", pages - 1))
        assert first_prev.callback_data == "recgrp:recitation:%d" % (pages - 1)
        assert first_next.callback_data == "recgrp:recitation:1"
        assert last_next.callback_data == "recgrp:recitation:0"
        assert last_prev.callback_data == "recgrp:recitation:%d" % (pages - 2)

    def test_out_of_range_page_wraps_instead_of_erroring(self):
        pages = main.reciter_page_count("recitation")
        assert _reciter_buttons(main.reciter_keyboard("en", "recitation", pages)) == \
            _reciter_buttons(main.reciter_keyboard("en", "recitation", 0))

    def test_pager_arrows_follow_reading_direction(self):
        ltr_prev, _, ltr_next = _pager_row(main.reciter_keyboard("en", "recitation", 1))
        rtl_prev, _, rtl_next = _pager_row(main.reciter_keyboard("ar", "recitation", 1))
        assert ltr_prev.text.startswith("‹") and ltr_next.text.endswith("›")
        assert rtl_prev.text.endswith("›") and rtl_next.text.startswith("‹")

    def test_search_button_survives_on_every_page(self):
        for kind in main.RECITER_KINDS:
            for page in range(main.reciter_page_count(kind)):
                markup = main.reciter_keyboard("en", kind, page)
                assert any(b.callback_data == "reciter_search"
                           for row in markup.inline_keyboard for b in row)


class TestCurrentReciter:

    def test_active_reciter_is_marked(self):
        buttons = _reciter_buttons(main.reciter_keyboard("en", 0, current="Husary_128kbps"))
        marked = [b.text for b in buttons if b.text.startswith("• ")]
        assert marked == ["• " + main.reciter_label(main.reciter_catalog()[0])]

    def test_page_of_finds_the_reciters_group_and_page(self):
        recitation = main.reciter_group("recitation")
        assert main.reciter_page_of(recitation[0]["subfolder"]) == ("recitation", 0)
        target = recitation[main.RECITER_PAGE_SIZE * 2 + 1]["subfolder"]
        assert main.reciter_page_of(target) == ("recitation", 2)

    def test_page_of_finds_an_entry_on_a_non_default_tab(self):
        warsh = main.reciter_group("riwayah")[0]["subfolder"]
        assert main.reciter_page_of(warsh) == ("riwayah", 0)

    def test_page_of_falls_back_to_the_first_page_for_a_stale_preference(self):
        assert main.reciter_page_of("Retired_Reciter_64kbps") == ("recitation", 0)


class TestPickerFlow:

    async def test_reciter_command_opens_on_the_current_reciters_page(self, fake_bot, data,
                                                                     tg_bot):
        recitation = main.reciter_group("recitation")
        on_page_three = recitation[main.RECITER_PAGE_SIZE * 2]["subfolder"]
        await UserSettings().set_reciter(558001, 558001, on_page_three)

        await main.handle_update(fake_bot, data,
                                 _message(tg_bot, "/reciter", chat_id=558001))

        markup = fake_bot.send_message.await_args.kwargs["reply_markup"]
        assert _pager_row(markup)[1].text.startswith("3/")
        assert any(b.text.startswith("• ") for b in _reciter_buttons(markup))

    async def test_reciter_command_opens_on_the_tab_the_reciter_lives_on(self, fake_bot,
                                                                        data, tg_bot):
        warsh = main.reciter_group("riwayah")[0]["subfolder"]
        await UserSettings().set_reciter(558011, 558011, warsh)

        await main.handle_update(fake_bot, data,
                                 _message(tg_bot, "/reciter", chat_id=558011))

        markup = fake_bot.send_message.await_args.kwargs["reply_markup"]
        active = [b for b in _tab_row(markup) if b.text.startswith("• ")]
        assert [b.callback_data for b in active] == ["recgrp:riwayah:0"]

    async def test_pager_tap_swaps_the_keyboard_in_place(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data,
                                 _callback(tg_bot, "recgrp:recitation:1", chat_id=558002))

        fake_bot.send_message.assert_not_awaited()      # no new list posted
        kwargs = fake_bot.edit_message_reply_markup.await_args.kwargs
        assert kwargs["message_id"] == 5
        assert _pager_row(kwargs["reply_markup"])[1].text.startswith("2/")
        fake_bot.answer_callback_query.assert_awaited()

    async def test_tab_tap_switches_group_in_place(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data,
                                 _callback(tg_bot, "recgrp:translation:0", chat_id=558012))

        fake_bot.send_message.assert_not_awaited()
        markup = fake_bot.edit_message_reply_markup.await_args.kwargs["reply_markup"]
        shown = {b.callback_data.split(":", 1)[1] for b in _reciter_buttons(markup)}
        assert shown == {p["subfolder"] for p in main.reciter_group("translation")}

    async def test_pager_tap_keeps_marking_the_current_reciter(self, fake_bot, data, tg_bot):
        recitation = main.reciter_group("recitation")
        on_page_two = recitation[main.RECITER_PAGE_SIZE]["subfolder"]
        await UserSettings().set_reciter(558003, 558003, on_page_two)

        await main.handle_update(fake_bot, data,
                                 _callback(tg_bot, "recgrp:recitation:1", chat_id=558003))

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


class TestCatalogKinds:
    """The catalog holds three different kinds of recording and must say so."""

    def test_every_entry_declares_a_kind(self):
        assert all(p.get("kind") in main.RECITER_KINDS for p in File._load_performers())

    def test_the_groups_partition_the_catalog(self):
        grouped = [p["subfolder"] for kind in main.RECITER_KINDS
                   for p in main.reciter_group(kind)]
        assert sorted(grouped) == sorted(p["subfolder"] for p in File._load_performers())

    def test_warsh_is_riwayah_not_an_ordinary_reciter(self):
        # a different reading of the text, so the audio stops matching the Arabic
        assert main.reciter_kind("warsh/warsh_Abdul_Basit_128kbps") == "riwayah"

    def test_recited_translations_are_not_filed_as_recitation(self):
        for subfolder in ("English/Sahih_Intnl_Ibrahim_Walk_192kbps",
                          "translations/urdu_farhat_hashmi",
                          "MultiLanguage/Basfar_Walk_192kbps"):
            assert main.reciter_kind(subfolder) == "translation"

    def test_an_unknown_reciter_is_treated_as_plain_recitation(self):
        assert main.reciter_kind("Retired_Reciter_64kbps") == "recitation"

    def test_the_default_reciter_is_ordinary_recitation(self):
        from lib.user_settings import DEFAULT_RECITER
        assert main.reciter_kind(DEFAULT_RECITER) == "recitation"


class TestKindWarnings:
    """Choosing something that is not Arabic recitation has to say so, at the moment
    of choosing — that is the whole point of the split."""

    def test_plain_reciter_gets_no_warning(self):
        text = main.reciter_set_confirmation("Husary_128kbps", "en")
        assert text == "Reciter set to Husary."

    def test_translation_audio_says_it_is_not_recitation(self):
        text = main.reciter_set_confirmation("translations/urdu_farhat_hashmi", "en")
        assert "not Qur'an recitation" in text

    def test_riwayah_gets_its_own_warning_not_the_translation_one(self):
        # Warsh *is* recitation, just a different reading — the two warnings
        # must not be interchanged.
        text = main.reciter_set_confirmation("warsh/warsh_Abdul_Basit_128kbps", "en")
        assert "Warsh" in text
        assert "not Qur'an recitation" not in text

    def test_warnings_are_localized(self):
        text = main.reciter_set_confirmation("translations/urdu_farhat_hashmi", "ru")
        assert "не чтение Корана" in text


class TestAudioNeverFollowsLanguage:
    """The audio a user hears is decided by their reciter and nothing else.

    Changing the UI or translation language must never silently switch the Qur'an
    recitation to a reading of the translated meaning.
    """

    async def test_changing_ui_language_leaves_the_audio_url_identical(self, fake_bot,
                                                                      data, tg_bot):
        file = File()
        before = file.get_audio_filename(2, 255, "Husary_128kbps")

        for code in ("ru", "ur", "fa", "en"):
            await main.handle_update(fake_bot, data,
                                     _callback(tg_bot, "setlang:" + code, chat_id=558100))

        settings = await UserSettings().get(558100, 558100)
        assert settings.reciter == "Husary_128kbps"
        assert file.get_audio_filename(2, 255, settings.reciter) == before

    async def test_changing_translation_language_leaves_the_reciter_alone(self, fake_bot,
                                                                         data, tg_bot):
        await UserSettings().set_reciter(558101, 558101, "Alafasy_128kbps")
        await main.handle_update(fake_bot, data,
                                 _callback(tg_bot, "settranslang:ur", chat_id=558101))

        settings = await UserSettings().get(558101, 558101)
        assert settings.reciter == "Alafasy_128kbps"

    async def test_an_urdu_speaker_still_gets_arabic_recitation_by_default(self, fake_bot,
                                                                          data, tg_bot):
        await main.handle_update(fake_bot, data,
                                 _message(tg_bot, "/start", chat_id=558102, lang="ur"))
        settings = await UserSettings().get(558102, 558102)
        assert settings.ui_lang == "ur"
        assert main.reciter_kind(settings.reciter) == "recitation"


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
