"""End-to-end dispatch of Telegram updates through `handle_update`.

Updates are built as real telegram.Update objects; the outgoing bot is an
AsyncMock so we assert on what the handler *tried to send* without any network.
Only text/translation/tafsir/navigation branches are exercised — the media
branches would require a real upload round-trip and are out of scope here.
"""

from unittest.mock import AsyncMock

import pytest
import telegram

import main
from lib.utils import File


@pytest.fixture(scope="module")
def data():
    # Parses the real corpora once for the whole module (tafsir + index + inline defaults).
    return main.build_data()


@pytest.fixture(scope="module")
def tg_bot():
    # Constructing a Bot does no network in python-telegram-bot; it only needs a
    # token-shaped string so Update.de_json can attach a bot reference.
    return telegram.Bot("123456:TEST-abcdefghijklmnopqrstuvwxyz")


@pytest.fixture
def fake_bot():
    return AsyncMock()


def _message(tg_bot, text, chat_id=555000, lang="en"):
    payload = {
        "update_id": 1,
        "message": {
            "message_id": 1,
            "date": 1700000000,
            "chat": {"id": chat_id, "type": "private" if chat_id > 0 else "supergroup"},
            "from": {"id": chat_id, "is_bot": False, "first_name": "Tester", "language_code": lang},
            "text": text,
        },
    }
    return telegram.Update.de_json(payload, tg_bot)


async def test_start_sends_welcome(fake_bot, data, tg_bot):
    await main.handle_update(fake_bot, data, _message(tg_bot, "/start", chat_id=555001))
    fake_bot.send_message.assert_awaited()
    assert fake_bot.send_message.await_args.kwargs["text"] == main.t("welcome", "en")


async def test_about_uses_html(fake_bot, data, tg_bot):
    await main.handle_update(fake_bot, data, _message(tg_bot, "/about", chat_id=555002))
    kwargs = fake_bot.send_message.await_args.kwargs
    assert kwargs["parse_mode"] == "HTML"
    assert kwargs["text"] == main.t("about", "en")


async def test_index_sends_surah_index(fake_bot, data, tg_bot):
    await main.handle_update(fake_bot, data, _message(tg_bot, "/index", chat_id=555003))
    assert fake_bot.send_message.await_args.kwargs["text"] == data["index"]


async def test_language_shows_inline_keyboard(fake_bot, data, tg_bot):
    await main.handle_update(fake_bot, data, _message(tg_bot, "/language", chat_id=555004))
    markup = fake_bot.send_message.await_args.kwargs["reply_markup"]
    assert isinstance(markup, telegram.InlineKeyboardMarkup)


async def test_group_chats_are_ignored(fake_bot, data, tg_bot):
    await main.handle_update(fake_bot, data, _message(tg_bot, "/start", chat_id=-100200300))
    fake_bot.send_message.assert_not_awaited()


async def test_translation_button_sends_ayah(fake_bot, data, tg_bot):
    # Default navigation state is (1, 1, "translation"); the canonical action word
    # resolves to the translation action in any language.
    await main.handle_update(fake_bot, data, _message(tg_bot, "translation", chat_id=555005))
    assert "(1:1)" in fake_bot.send_message.await_args.kwargs["text"]


async def test_tafsir_appends_english_note_for_non_english(fake_bot, data, tg_bot):
    await main.handle_update(fake_bot, data, _message(tg_bot, "tafsir", chat_id=555006, lang="ru"))
    assert main.t("tafsir_en_note", "ru") in fake_bot.send_message.await_args.kwargs["text"]


async def test_next_navigates_forward(fake_bot, data, tg_bot):
    # From default (1, 1) "next" advances to 1:2 and sends the translation.
    await main.handle_update(fake_bot, data, _message(tg_bot, "next", chat_id=555007))
    assert "(1:2)" in fake_bot.send_message.await_args.kwargs["text"]


async def test_setlang_callback_persists_language(fake_bot, data, tg_bot):
    payload = {
        "update_id": 2,
        "callback_query": {
            "id": "cbq-1",
            "from": {"id": 555008, "is_bot": False, "first_name": "Tester"},
            "chat_instance": "ci-1",
            "data": "setlang:ru",
            "message": {
                "message_id": 5,
                "date": 1700000000,
                "chat": {"id": 555008, "type": "private"},
            },
        },
    }
    await main.handle_update(fake_bot, data, telegram.Update.de_json(payload, tg_bot))
    fake_bot.answer_callback_query.assert_awaited()
    assert File().get_lang(555008) == "ru"


async def test_inline_query_valid_ayah_returns_two_results(fake_bot, data, tg_bot):
    payload = {
        "update_id": 3,
        "inline_query": {
            "id": "iq-1",
            "from": {"id": 555009, "is_bot": False, "first_name": "Tester", "language_code": "en"},
            "query": "2:255",
            "offset": "",
        },
    }
    await main.handle_update(fake_bot, data, telegram.Update.de_json(payload, tg_bot))
    fake_bot.answer_inline_query.assert_awaited()
    # A valid ayah yields exactly a translation result and a tafsir result.
    assert len(fake_bot.answer_inline_query.await_args.kwargs["results"]) == 2


async def test_textless_message_is_ignored(fake_bot, data, tg_bot):
    payload = {
        "update_id": 4,
        "message": {
            "message_id": 9,
            "date": 1700000000,
            "chat": {"id": 555010, "type": "private"},
            "from": {"id": 555010, "is_bot": False, "first_name": "Tester"},
        },
    }
    await main.handle_update(fake_bot, data, telegram.Update.de_json(payload, tg_bot))
    fake_bot.send_message.assert_not_awaited()
