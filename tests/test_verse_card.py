"""The inline verse-card reader: keyboard shape, text rendering, and callbacks.

The card replaces the old persistent reply keyboard: every verse now carries an
inline keyboard, and tapping it fires a `vc:`/`vr:` callback that edits the same
message in place (for the text views) instead of posting a new one. These tests
drive real telegram.Update objects through `handle_update` against an AsyncMock
bot, so we assert on what the handler *tried to send/edit* with no network.
"""

from unittest.mock import AsyncMock

import pytest
import telegram

import main
from locales import LANGUAGES, get_language


def _button(markup, predicate):
    """The one button on `markup` matching `predicate`.

    Found by what a button *does* rather than by its position, so adding a button
    to a row cannot silently repoint these assertions at a different one.
    """
    return next(b for row in markup.inline_keyboard for b in row if predicate(b))


@pytest.fixture(scope="module")
def data():
    return main.build_data()


@pytest.fixture(scope="module")
def tg_bot():
    return telegram.Bot("123456:TEST-abcdefghijklmnopqrstuvwxyz")


@pytest.fixture
def fake_bot():
    return AsyncMock()


def _callback(tg_bot, data_str, chat_id=556000, message_kind="text"):
    """A callback_query update whose source message is either text or a photo."""
    message = {
        "message_id": 10,
        "date": 1700000000,
        "chat": {"id": chat_id, "type": "private"},
        "from": {"id": 42, "is_bot": True, "first_name": "Bot"},
    }
    if message_kind == "text":
        message["text"] = "placeholder"
    elif message_kind == "photo":
        message["photo"] = [
            {"file_id": "f", "file_unique_id": "u", "width": 100, "height": 100}
        ]
    payload = {
        "update_id": 1,
        "callback_query": {
            "id": "cbq-1",
            "from": {"id": chat_id, "is_bot": False, "first_name": "Tester", "language_code": "en"},
            "chat_instance": "ci-1",
            "data": data_str,
            "message": message,
        },
    }
    return telegram.Update.de_json(payload, tg_bot)


# --- Keyboard shape ---------------------------------------------------------

class TestVerseKeyboard:
    def test_active_view_is_marked_with_a_dot(self):
        rows = main.verse_keyboard(2, 255, "tafsir", "en").inline_keyboard
        labels = [b.text for b in rows[0]]
        assert any(label.startswith("• ") and "Tafsir" in label for label in labels)

    def test_only_audio_carries_an_icon(self):
        labels = [b.text for b in main.verse_keyboard(1, 1, "translation", "en").inline_keyboard[0]]
        assert "🔊 Audio" in labels
        # The scripture views stay clean — no icon decorates translation/arabic/tafsir.
        assert "Translation" in [label.lstrip("• ") for label in labels]

    def test_nav_callbacks_point_at_neighbouring_ayat(self):
        nav = main.verse_keyboard(2, 255, "translation", "en").inline_keyboard[1]
        assert nav[0].callback_data == "vc:tr:2:254"   # previous
        assert nav[1].callback_data == "vr:tr"         # random keeps the view
        assert nav[2].callback_data == "vc:tr:2:256"   # next

    def test_arrows_flip_for_rtl(self):
        ltr = main.verse_keyboard(2, 255, "translation", "en").inline_keyboard[1]
        rtl = main.verse_keyboard(2, 255, "translation", "ar").inline_keyboard[1]
        assert ltr[0].text.startswith("‹")   # LTR: previous points left
        assert rtl[0].text.endswith("›")      # RTL: mirrored so "next" reads forward

    def test_share_uses_inline_mode(self):
        share = _button(main.verse_keyboard(2, 255, "translation", "en"),
                        lambda b: b.switch_inline_query is not None)
        assert share.switch_inline_query == "2:255"

    def test_language_button_shows_current_language(self):
        util = _button(main.verse_keyboard(2, 255, "translation", "uz"),
                       lambda b: b.callback_data == "showlang")
        assert get_language("uz").native in util.text

    def test_repeat_button_replays_this_ayah(self):
        repeat = _button(main.verse_keyboard(2, 255, "audio", "en"),
                         lambda b: (b.callback_data or "").startswith("rep:"))
        assert repeat.callback_data == "rep:2:255"
        assert "×%d" % main.REPEAT_COUNT in repeat.text

    def test_repeat_label_is_localized(self):
        repeat = _button(main.verse_keyboard(2, 255, "audio", "ru"),
                         lambda b: (b.callback_data or "").startswith("rep:"))
        assert "Повтор" in repeat.text


# --- Text rendering ---------------------------------------------------------

class TestVerseText:
    async def test_has_bold_header_and_reference(self, data):
        text = await main.build_verse_text(2, 255, "translation", "en", "en", data)
        assert text.startswith("<b>")
        assert "(2:255)" in text

    async def test_tafsir_note_follows_ui_language_not_translation_language(self, data):
        # The tafsir corpus is English-only, so the note is bot UI text: it must
        # follow ui_lang even for a reader whose translations are in English.
        text = await main.build_verse_text(1, 1, "tafsir", "ru", "en", data)
        assert main.t("tafsir_en_note", "ru") in text

    async def test_translation_body_follows_translation_language(self, data):
        # The whole point of splitting the settings: a Russian UI can render an
        # English translation, and the body must come from translation_lang.
        ru = await main.build_verse_text(1, 2, "translation", "ru", "ru", data)
        en = await main.build_verse_text(1, 2, "translation", "ru", "en", data)
        assert ru != en


# --- Callback dispatch ------------------------------------------------------

class TestVerseCallbacks:
    async def test_text_view_edits_message_in_place(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data, _callback(tg_bot, "vc:tr:2:255"))
        kwargs = fake_bot.edit_message_text.await_args.kwargs
        assert "(2:255)" in kwargs["text"]
        assert kwargs["message_id"] == 10
        assert kwargs["parse_mode"] == "HTML"
        fake_bot.answer_callback_query.assert_awaited()
        fake_bot.send_message.assert_not_awaited()   # no new bubble — the page turned

    async def test_switching_from_media_posts_a_fresh_card(self, fake_bot, data, tg_bot):
        # A photo message can't be edited into text, so we send a new text card.
        await main.handle_update(fake_bot, data, _callback(tg_bot, "vc:tf:1:1", message_kind="photo"))
        fake_bot.send_message.assert_awaited()
        fake_bot.edit_message_text.assert_not_awaited()

    async def test_random_callback_turns_the_page(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data, _callback(tg_bot, "vr:tr"))
        fake_bot.edit_message_text.assert_awaited()
        fake_bot.answer_callback_query.assert_awaited()

    async def test_showlang_opens_the_picker(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data, _callback(tg_bot, "showlang"))
        markup = fake_bot.send_message.await_args.kwargs["reply_markup"]
        assert isinstance(markup, telegram.InlineKeyboardMarkup)

    async def test_nonexistent_ayah_only_acknowledges(self, fake_bot, data, tg_bot):
        await main.handle_update(fake_bot, data, _callback(tg_bot, "vc:tr:2:999"))
        fake_bot.answer_callback_query.assert_awaited()
        fake_bot.edit_message_text.assert_not_awaited()
        fake_bot.send_message.assert_not_awaited()


# --- Language flags ---------------------------------------------------------

class TestLanguageFlags:
    def test_every_catalogued_language_has_a_flag(self):
        missing = [lang.code for lang in LANGUAGES if not lang.flag]
        assert missing == []

    def test_picker_prefixes_the_flag(self):
        first = main.language_keyboard().inline_keyboard[0][0].text
        english = get_language("en")
        assert english.flag in first and english.native in first
