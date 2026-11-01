"""The Telegram channel against an AsyncMock bot: each call becomes the same
python-telegram-bot request the bot code makes by hand today."""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from channels import TELEGRAM, Choice, for_platform
from channels.telegram import TelegramChannel, to_markup
from infra import media_cache


@pytest.fixture
def bot():
    bot = AsyncMock()
    bot.send_photo.return_value = SimpleNamespace(photo=[SimpleNamespace(file_id="ph-1")])
    bot.send_audio.return_value = SimpleNamespace(audio=SimpleNamespace(file_id="au-1"))
    return bot


@pytest.fixture
def cache(monkeypatch):
    store = {}
    monkeypatch.setattr(media_cache, "get", store.get)
    monkeypatch.setattr(media_cache, "save", store.__setitem__)
    return store


ROWS = [
    [Choice("A", data="a:1"), Choice("B", data="b:2")],
    [
        Choice("Site", url="https://example.org"),
        Choice("App", web_app="https://app.example.org/read/2"),
        Choice("📤", switch_inline="2:255"),
    ],
]


class TestChoice:
    def test_needs_exactly_one_action(self):
        with pytest.raises(ValueError):
            Choice("none")
        with pytest.raises(ValueError):
            Choice("two", data="x", url="https://example.org")


class TestToMarkup:
    def test_matches_a_hand_built_keyboard(self):
        expected = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("A", callback_data="a:1"),
                    InlineKeyboardButton("B", callback_data="b:2"),
                ],
                [
                    InlineKeyboardButton("Site", url="https://example.org"),
                    InlineKeyboardButton(
                        "App", web_app=WebAppInfo(url="https://app.example.org/read/2")
                    ),
                    InlineKeyboardButton("📤", switch_inline_query="2:255"),
                ],
            ]
        )
        assert to_markup(ROWS).to_dict() == expected.to_dict()

    def test_no_rows_means_no_keyboard(self):
        assert to_markup(None) is None
        assert to_markup([]) is None


class TestSendText:
    async def test_plain(self, bot):
        await TelegramChannel(bot, 42).send_text("hi")
        bot.send_message.assert_awaited_once_with(chat_id=42, text="hi")

    async def test_html_choices_and_passthrough(self, bot):
        await TelegramChannel(bot, 42).send_text(
            "<b>hi</b>", [[Choice("A", data="a")]], html=True, disable_web_page_preview=True
        )
        kwargs = bot.send_message.await_args.kwargs
        assert kwargs["parse_mode"] == "HTML"
        assert kwargs["disable_web_page_preview"] is True
        assert kwargs["reply_markup"].to_dict() == to_markup([[Choice("A", data="a")]]).to_dict()

    async def test_explicit_reply_markup_wins(self, bot):
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("X", callback_data="x")]])
        await TelegramChannel(bot, 42).send_text(
            "hi", [[Choice("A", data="a")]], reply_markup=markup
        )
        assert bot.send_message.await_args.kwargs["reply_markup"] is markup

    async def test_forum_topic(self, bot):
        await TelegramChannel(bot, -100, thread_id=7).send_text("hi")
        bot.send_message.assert_awaited_once_with(chat_id=-100, text="hi", message_thread_id=7)


class TestEditText:
    async def test_edits_in_place(self, bot):
        assert await TelegramChannel(bot, 42).edit_text(9, "new", html=True) is True
        bot.edit_message_text.assert_awaited_once_with(
            text="new", chat_id=42, message_id=9, parse_mode="HTML"
        )

    async def test_not_modified_is_not_an_error(self, bot):
        bot.edit_message_text.side_effect = telegram.error.BadRequest("Message is not modified")
        assert await TelegramChannel(bot, 42).edit_text(9, "same") is True

    async def test_other_bad_requests_raise(self, bot):
        bot.edit_message_text.side_effect = telegram.error.BadRequest("message to edit not found")
        with pytest.raises(telegram.error.BadRequest):
            await TelegramChannel(bot, 42).edit_text(9, "x")

    async def test_topic_is_not_sent_on_an_edit(self, bot):
        await TelegramChannel(bot, -100, thread_id=7).edit_text(9, "x")
        assert "message_thread_id" not in bot.edit_message_text.await_args.kwargs


class TestEditChoices:
    async def test_swaps_the_keyboard(self, bot):
        rows = [[Choice("A", data="a")]]
        assert await TelegramChannel(bot, 42).edit_choices(9, rows) is True
        kwargs = bot.edit_message_reply_markup.await_args.kwargs
        assert (kwargs["chat_id"], kwargs["message_id"]) == (42, 9)
        assert kwargs["reply_markup"].to_dict() == to_markup(rows).to_dict()

    async def test_not_modified_is_not_an_error(self, bot):
        bot.edit_message_reply_markup.side_effect = telegram.error.BadRequest("not modified")
        assert await TelegramChannel(bot, 42).edit_choices(9, []) is True


class TestMedia:
    async def test_image_by_url_without_cache(self, bot):
        await TelegramChannel(bot, 42).send_image(
            "https://img/1.png", caption="2:255", choices=[[Choice("A", data="a")]]
        )
        bot.send_chat_action.assert_awaited_once_with(
            chat_id=42, action=telegram.constants.ChatAction.UPLOAD_PHOTO
        )
        kwargs = bot.send_photo.await_args.kwargs
        assert kwargs["chat_id"] == 42 and kwargs["photo"] == "https://img/1.png"
        assert kwargs["caption"] == "2:255" and "reply_markup" in kwargs

    async def test_audio_builder_is_called(self, bot):
        async def build():
            return b"mp3"

        await TelegramChannel(bot, 42).send_audio(
            build, title="2:255", performer="Husary", upload_action=False
        )
        bot.send_chat_action.assert_not_awaited()
        bot.send_audio.assert_awaited_once_with(
            chat_id=42, audio=b"mp3", title="2:255", performer="Husary"
        )

    async def test_cache_miss_uploads_and_caches(self, bot, cache):
        await TelegramChannel(bot, 42).send_image("https://img/1.png", cache_key="k1")
        assert bot.send_photo.await_args.kwargs["photo"] == "https://img/1.png"
        assert cache["k1"] == "ph-1"

    async def test_cache_hit_replays_the_file_id(self, bot, cache):
        cache["k2"] = "au-old"
        built = AsyncMock(return_value=b"never")
        await TelegramChannel(bot, 42).send_audio(built, cache_key="k2")
        assert bot.send_audio.await_args.kwargs["audio"] == "au-old"
        built.assert_not_awaited()
        bot.send_chat_action.assert_not_awaited()


class TestAnswerAndTyping:
    async def test_answer_without_text(self, bot):
        await TelegramChannel(bot, 42).answer("cb-1")
        bot.answer_callback_query.assert_awaited_once_with("cb-1")

    async def test_answer_with_alert(self, bot):
        await TelegramChannel(bot, 42).answer("cb-1", "done", alert=True)
        bot.answer_callback_query.assert_awaited_once_with("cb-1", text="done", show_alert=True)

    async def test_answer_without_a_tap_is_a_no_op(self, bot):
        await TelegramChannel(bot, 42).answer(None, "x")
        bot.answer_callback_query.assert_not_awaited()

    async def test_typing(self, bot):
        await TelegramChannel(bot, 42).typing()
        bot.send_chat_action.assert_awaited_once_with(
            chat_id=42, action=telegram.constants.ChatAction.TYPING
        )

    async def test_no_templates(self, bot):
        with pytest.raises(NotImplementedError):
            await TelegramChannel(bot, 42).send_template("daily_ayah", "en", [])


class TestForPlatform:
    def test_telegram(self, bot):
        channel = for_platform(TELEGRAM, bot=bot, external_id="42", thread_id=3)
        assert isinstance(channel, TelegramChannel)
        assert (channel.chat_id, channel.thread_id, channel.platform) == (42, 3, TELEGRAM)

    def test_unknown_platform(self, bot):
        with pytest.raises(ValueError):
            for_platform("carrier-pigeon", bot=bot, external_id="1")
