"""The order in which a text message is offered to the bot's handlers.

    command  >  pending reciter search  >  wizard in flight  >  button label  >  ayah reference

The order is load-bearing: a command must always escape a wizard or a pending
prompt (a /start typed while the bot awaited a reciter name used to be
swallowed as the name), and a wizard must see its user's free text before the
reference parser does. These tests pin it end to end through handle_update, so
the router rewrite (refactor Phase 3) has to keep it.
"""

from unittest.mock import AsyncMock

import pytest
import telegram

import app.lifespan as lifespan
import bot.dispatch as dispatch
import hifz
import locales
from lib.utils import File
from lib.wizard import Wizard

PROBE = "zz_order_probe"


@pytest.fixture(scope="module")
def data():
    return lifespan.build_data()


@pytest.fixture(scope="module")
def tg_bot():
    return telegram.Bot("123456:TEST-abcdefghijklmnopqrstuvwxyz")


@pytest.fixture
def fake_bot():
    return AsyncMock()


@pytest.fixture
def probe(monkeypatch):
    """A wizard kind that records the text it was fed."""
    hifz.load_features()
    seen = []

    async def step(ctx, text):
        seen.append(text)

    monkeypatch.setitem(hifz.WIZARDS, PROBE, step)
    return seen


def _message(tg_bot, text, chat_id):
    return telegram.Update.de_json(
        {
            "update_id": 1,
            "message": {
                "message_id": 1,
                "date": 1700000000,
                "chat": {"id": chat_id, "type": "private"},
                "from": {"id": chat_id, "is_bot": False, "first_name": "T", "language_code": "en"},
                "text": text,
            },
        },
        tg_bot,
    )


def _callback(tg_bot, cb_data, chat_id):
    return telegram.Update.de_json(
        {
            "update_id": 2,
            "callback_query": {
                "id": "cbq",
                "from": {"id": chat_id, "is_bot": False, "first_name": "T"},
                "chat_instance": "ci",
                "data": cb_data,
                "message": {
                    "message_id": 5,
                    "date": 1700000000,
                    "chat": {"id": chat_id, "type": "private"},
                },
            },
        },
        tg_bot,
    )


def _texts(fake_bot):
    return [c.kwargs.get("text") for c in fake_bot.send_message.await_args_list]


def _sent_a_verse(fake_bot):
    return any(c.kwargs.get("parse_mode") == "HTML" and "<b>" in (c.kwargs.get("text") or "")
               for c in fake_bot.send_message.await_args_list)  # fmt: skip


async def test_a_command_beats_a_pending_reciter_search(fake_bot, data, tg_bot):
    chat = 610001
    File().set_awaiting_input(chat, "reciter_search")
    await dispatch.handle_update(fake_bot, data, _message(tg_bot, "/about", chat))
    assert _texts(fake_bot) == [locales.t("about", "en")]
    assert File().pop_awaiting_input(chat) is None, "a command clears the pending prompt"


async def test_an_unknown_command_clears_the_prompt_then_reads_as_a_reference(
    fake_bot, data, tg_bot
):
    chat = 610002
    File().set_awaiting_input(chat, "reciter_search")
    await dispatch.handle_update(fake_bot, data, _message(tg_bot, "/2:255", chat))
    assert _sent_a_verse(fake_bot), "/2:255 is a reference, not a reciter search"
    assert locales.t("reciter_search_results", "en") not in _texts(fake_bot)


async def test_a_pending_reciter_search_beats_a_wizard(fake_bot, data, tg_bot, probe):
    chat = 610003
    Wizard().start(chat, PROBE)
    File().set_awaiting_input(chat, "reciter_search")
    await dispatch.handle_update(fake_bot, data, _message(tg_bot, "husary", chat))
    assert locales.t("reciter_search_results", "en") in _texts(fake_bot)
    assert probe == []


async def test_a_wizard_beats_the_reference_parser(fake_bot, data, tg_bot, probe):
    chat = 610004
    Wizard().start(chat, PROBE)
    await dispatch.handle_update(fake_bot, data, _message(tg_bot, "2:255", chat))
    assert probe == ["2:255"]
    assert not _sent_a_verse(fake_bot)


async def test_a_wizard_gets_the_text_as_typed(fake_bot, data, tg_bot, probe):
    chat = 610005
    Wizard().start(chat, PROBE)
    await dispatch.handle_update(fake_bot, data, _message(tg_bot, "Al-Mulk Daily", chat))
    assert probe == ["Al-Mulk Daily"], "not lowercased"


async def test_a_command_escapes_a_wizard_without_ending_it(fake_bot, data, tg_bot, probe):
    chat = 610006
    Wizard().start(chat, PROBE)
    await dispatch.handle_update(fake_bot, data, _message(tg_bot, "/about", chat))
    assert _texts(fake_bot) == [locales.t("about", "en")]
    assert probe == []
    assert Wizard().is_active(chat), "only /cancel ends a wizard"


async def test_cancel_ends_a_wizard(fake_bot, data, tg_bot, probe):
    chat = 610007
    Wizard().start(chat, PROBE)
    await dispatch.handle_update(fake_bot, data, _message(tg_bot, "/cancel", chat))
    assert _texts(fake_bot) == [locales.t("wizard_cancelled", "en")]
    assert not Wizard().is_active(chat)


async def test_with_nothing_in_flight_a_reference_is_read(fake_bot, data, tg_bot):
    await dispatch.handle_update(fake_bot, data, _message(tg_bot, "2:255", 610008))
    assert _sent_a_verse(fake_bot)


async def test_an_unknown_callback_is_only_acknowledged(fake_bot, data, tg_bot):
    await dispatch.handle_update(fake_bot, data, _callback(tg_bot, "zz:nothing", 610009))
    fake_bot.answer_callback_query.assert_awaited_once_with("cbq")
    fake_bot.send_message.assert_not_awaited()
    fake_bot.edit_message_text.assert_not_awaited()
