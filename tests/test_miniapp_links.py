"""Bot → Mini App entry points (docs/MINI_APP_PLAN.md §7, P2.6 / P3.7).

Off by default: without MINIAPP_URL every keyboard is exactly what it was. With
it, verse cards, page cards and the daily drill carry a web_app button to the
matching app route, /app answers with one, and the menu button opens the app."""

from unittest.mock import AsyncMock

import pytest
import telegram

import app.lifespan as lifespan
import bot.dispatch as dispatch
import bot.keyboards.page as page_kb
import bot.keyboards.verse as verse_kb
from bot.features import memorize
from bot.miniapp import app_url, set_menu_button

APP = "https://miniapp.test"


def _web_apps(markup):
    return [b.web_app.url for row in markup.inline_keyboard for b in row if b.web_app]


@pytest.fixture
def app_on(monkeypatch):
    monkeypatch.setenv("MINIAPP_URL", APP + "/")


def test_off_by_default():
    assert app_url() is None
    assert _web_apps(verse_kb.verse_keyboard(2, 255, "translation", "en")) == []
    assert _web_apps(page_kb.page_keyboard(255, "en")) == []
    assert _web_apps(memorize._drill_keyboard(9, 67, 1, "en")) == []


def test_cards_and_drill_link_to_their_screens(app_on):
    assert _web_apps(verse_kb.verse_keyboard(2, 255, "translation", "en")) == [
        APP + "/read/2?a=255"
    ]
    assert _web_apps(page_kb.page_keyboard(255, "en")) == [APP + "/mushaf/255"]
    assert _web_apps(memorize._drill_keyboard(9, 67, 1, "ru")) == [APP + "/drill"]


def test_inline_messages_never_get_a_web_app_button(app_on):
    assert _web_apps(verse_kb.verse_keyboard(2, 255, "audio", "en", app=False)) == []


async def test_menu_button(app_on):
    bot = AsyncMock()
    assert await set_menu_button(bot) is True
    button = bot.set_chat_menu_button.call_args.kwargs["menu_button"]
    assert isinstance(button, telegram.MenuButtonWebApp) and button.web_app.url == APP + "/"


async def test_menu_button_off_without_url():
    bot = AsyncMock()
    assert await set_menu_button(bot) is False
    bot.set_chat_menu_button.assert_not_called()


def _app_command(tg_bot):
    return telegram.Update.de_json(
        {
            "update_id": 1,
            "message": {
                "message_id": 1,
                "date": 1700000000,
                "chat": {"id": 555000, "type": "private"},
                "from": {"id": 555000, "is_bot": False, "first_name": "T", "language_code": "en"},
                "text": "/app",
            },
        },
        tg_bot,
    )


@pytest.fixture(scope="module")
def data():
    return lifespan.build_data()


async def test_app_command(app_on, data):
    tg_bot = telegram.Bot("123456:TEST-abcdefghijklmnopqrstuvwxyz")
    bot = AsyncMock()
    await dispatch.handle_update(bot, data, _app_command(tg_bot))
    kwargs = bot.send_message.call_args.kwargs
    assert _web_apps(kwargs["reply_markup"]) == [APP + "/"]


async def test_app_command_without_url(data):
    tg_bot = telegram.Bot("123456:TEST-abcdefghijklmnopqrstuvwxyz")
    bot = AsyncMock()
    await dispatch.handle_update(bot, data, _app_command(tg_bot))
    assert bot.send_message.call_args.kwargs["reply_markup"] is None
