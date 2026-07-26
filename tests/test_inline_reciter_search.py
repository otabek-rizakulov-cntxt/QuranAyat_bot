"""Inline-mode reciter search: `@bot <name>` offers reciters, `@bot 2:255` still
offers the ayah.

Same shape as test_handle_update.py: real telegram.Update objects in, an
AsyncMock bot out, so we assert on what the handler *tried to answer* with.
"""

from unittest.mock import AsyncMock

import pytest
import telegram

import main
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


def _inline_query(tg_bot, query, user_id=556000, lang="en"):
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


def _inline_callback(tg_bot, cb_data, user_id=556100):
    """A tap on a card that was sent through inline mode: no `message`, only an
    inline_message_id."""
    payload = {
        "update_id": 2,
        "callback_query": {
            "id": "cbq-%d" % user_id,
            "from": {"id": user_id, "is_bot": False, "first_name": "Tester"},
            "chat_instance": "ci-inline",
            "inline_message_id": "AgAAAO0zAAA",
            "data": cb_data,
        },
    }
    return telegram.Update.de_json(payload, tg_bot)


async def test_ayah_query_still_returns_translation_and_tafsir(fake_bot, data, tg_bot):
    await main.handle_update(fake_bot, data, _inline_query(tg_bot, "2:255", user_id=556001))
    kwargs = fake_bot.answer_inline_query.await_args.kwargs
    assert [r.title for r in kwargs["results"]] == [main.t("btn_translation", "en"),
                                                    main.t("btn_tafsir", "en")]
    # immutable text: the aggressive shared cache must survive this change
    assert kwargs["cache_time"] == 66 * (60 ** 2 * 24)
    assert kwargs["is_personal"] is False


async def test_reciter_query_returns_setreciter_articles(fake_bot, data, tg_bot):
    await main.handle_update(fake_bot, data, _inline_query(tg_bot, "sudais", user_id=556002))
    results = fake_bot.answer_inline_query.await_args.kwargs["results"]
    assert results and all(isinstance(r, telegram.InlineQueryResultArticle) for r in results)
    for r in results:
        assert "Sudais" in r.title
        assert r.description == main.t("reciter_inline_description", "en")
        button = r.reply_markup.inline_keyboard[0][0]
        assert button.text == main.t("btn_set_reciter", "en")
        assert button.callback_data.startswith("setreciter:")
    assert len({r.id for r in results}) == len(results)  # Telegram rejects duplicate ids


async def test_reciter_query_is_personal_and_uncached(fake_bot, data, tg_bot):
    # Results are in the caller's language and mutate a setting, so they may not be
    # served from the long-lived shared cache the ayah branch uses.
    await main.handle_update(fake_bot, data, _inline_query(tg_bot, "husary", user_id=556003))
    kwargs = fake_bot.answer_inline_query.await_args.kwargs
    assert kwargs["cache_time"] == 0
    assert kwargs["is_personal"] is True


async def test_reciter_results_are_localized(fake_bot, data, tg_bot):
    await main.handle_update(fake_bot, data,
                             _inline_query(tg_bot, "sudais", user_id=556004, lang="ru"))
    result = fake_bot.answer_inline_query.await_args.kwargs["results"][0]
    assert result.description == main.t("reciter_inline_description", "ru")
    assert result.reply_markup.inline_keyboard[0][0].text == main.t("btn_set_reciter", "ru")


async def test_no_match_falls_back_to_defaults(fake_bot, data, tg_bot):
    await main.handle_update(fake_bot, data, _inline_query(tg_bot, "zzqqxx", user_id=556005))
    kwargs = fake_bot.answer_inline_query.await_args.kwargs
    assert kwargs["results"] is data["default_query_results"]
    assert kwargs["cache_time"] == 66 * (60 ** 2 * 24)


async def test_empty_query_falls_back_to_defaults(fake_bot, data, tg_bot):
    await main.handle_update(fake_bot, data, _inline_query(tg_bot, "", user_id=556006))
    kwargs = fake_bot.answer_inline_query.await_args.kwargs
    assert kwargs["results"] is data["default_query_results"]


async def test_setreciter_from_inline_message_persists(fake_bot, data, tg_bot):
    update = _inline_callback(tg_bot, "setreciter:Ghamadi_40kbps", user_id=556007)
    assert update.callback_query.message is None  # the case this test exists for

    await main.handle_update(fake_bot, data, update)

    assert (await UserSettings().get(556007)).reciter == "Ghamadi_40kbps"


async def test_setreciter_from_inline_message_confirms_without_dm(fake_bot, data, tg_bot):
    # No chat exists, so a DM could be rejected with Forbidden: confirm in the
    # callback answer itself instead.
    await main.handle_update(fake_bot, data,
                             _inline_callback(tg_bot, "setreciter:Ghamadi_40kbps", user_id=556008))
    fake_bot.send_message.assert_not_awaited()
    kwargs = fake_bot.answer_callback_query.await_args.kwargs
    assert kwargs["text"] == main.t("reciter_set", "en").format(reciter="Ghamadi")


async def test_setreciter_in_chat_still_sends_confirmation(fake_bot, data, tg_bot):
    payload = {
        "update_id": 3,
        "callback_query": {
            "id": "cbq-chat",
            "from": {"id": 556009, "is_bot": False, "first_name": "Tester"},
            "chat_instance": "ci-1",
            "data": "setreciter:Alafasy_128kbps",
            "message": {
                "message_id": 5,
                "date": 1700000000,
                "chat": {"id": 556009, "type": "private"},
            },
        },
    }
    await main.handle_update(fake_bot, data, telegram.Update.de_json(payload, tg_bot))
    assert fake_bot.send_message.await_args.kwargs["text"] == \
        main.t("reciter_set", "en").format(reciter="Alafasy")
    assert (await UserSettings().get(556009)).reciter == "Alafasy_128kbps"
