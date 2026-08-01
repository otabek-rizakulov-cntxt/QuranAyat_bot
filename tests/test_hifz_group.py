"""The group cluster's onboarding, topic creation and board join (J1-J3, J6 entry).

Driven with an AsyncMock bot. The bot's group-facing calls — get_me,
create_forum_topic, get_chat_member — are stubbed per test, because that is where
the interesting branches are: is the caller an admin, is the group a forum, is the
tapper actually a member.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
import telegram

import hifz
from hifz import Ctx
from hifz import group as G
from lib.store import get_store

ADMIN = 500
CHAT = -100200300


class _Settings:
    ui_lang = "en"
    translation_lang = "en"
    reciter = "Husary_128kbps"


@pytest.fixture(autouse=True)
def _isolate_registries():
    saved = (dict(hifz.COMMANDS), dict(hifz.CALLBACKS), dict(hifz.WIZARDS), hifz._loaded)
    G._bot_username = None
    yield
    hifz.COMMANDS.clear(); hifz.COMMANDS.update(saved[0])
    hifz.CALLBACKS.clear(); hifz.CALLBACKS.update(saved[1])
    hifz.WIZARDS.clear(); hifz.WIZARDS.update(saved[2])
    hifz._loaded = saved[3]
    G._bot_username = None


def _bot(**kw):
    bot = AsyncMock()
    bot.get_me.return_value = SimpleNamespace(username="BismillahBot")
    for k, v in kw.items():
        getattr(bot, k).return_value = v
    return bot


async def _ctx(bot, user=ADMIN, chat=ADMIN):
    from lib.utils import File
    return await Ctx.build(bot, {}, File(), chat, user, _Settings())


def _member(status):
    return SimpleNamespace(status=status)


def _added_update(status="member", adder=ADMIN, chat_type="supergroup"):
    return SimpleNamespace(my_chat_member=SimpleNamespace(
        chat=SimpleNamespace(id=CHAT, type=chat_type),
        from_user=SimpleNamespace(id=adder),
        new_chat_member=SimpleNamespace(status=status)))


# --- J2: the bot is added ------------------------------------------------------

class TestAdded:
    async def test_adding_creates_config_and_posts_a_setup_link(self):
        store = await get_store()
        bot = _bot()
        await G.on_my_chat_member(bot, store, _added_update())

        config = await store.groups.get_config(CHAT)
        assert config is not None and config.admin_user_id == ADMIN
        assert config.status == "setup"
        bot.send_message.assert_awaited_once()
        markup = bot.send_message.await_args.kwargs["reply_markup"]
        url = markup.inline_keyboard[0][0].url
        assert url.endswith("?start=gs_%d" % CHAT)

    async def test_a_private_chat_is_ignored(self):
        store = await get_store()
        bot = _bot()
        await G.on_my_chat_member(bot, store, _added_update(chat_type="private"))
        assert await store.groups.get_config(CHAT) is None
        bot.send_message.assert_not_awaited()

    async def test_removal_pauses_the_config_but_keeps_it(self):
        store = await get_store()
        await store.groups.ensure_config(CHAT, admin_user_id=ADMIN)
        await store.groups.update_config(CHAT, status="active")
        await G.on_my_chat_member(_bot(), store, _added_update(status="kicked"))
        config = await store.groups.get_config(CHAT)
        assert config is not None and config.status == "paused"


# --- J2/J3: admin setup --------------------------------------------------------

class TestSetup:
    async def test_non_admin_is_refused(self):
        store = await get_store()
        await store.groups.ensure_config(CHAT, admin_user_id=ADMIN)
        bot = _bot(get_chat_member=_member("member"))
        ctx = await _ctx(bot, user=999)
        assert await G.handle_start_payload(ctx, "gs_%d" % CHAT) is True
        assert G.WIZARD_KIND not in [ctx.wiz.kind(999) or ""]
        assert bot.send_message.await_args.kwargs["text"]  # a refusal message

    async def test_unknown_group_is_refused(self):
        bot = _bot(get_chat_member=_member("administrator"))
        ctx = await _ctx(bot)
        assert await G.handle_start_payload(ctx, "gs_-999") is True
        assert ctx.wiz.is_active(ADMIN) is False

    async def test_admin_enters_the_topic_step(self):
        store = await get_store()
        await store.groups.ensure_config(CHAT, admin_user_id=ADMIN)
        bot = _bot(get_chat_member=_member("creator"))
        ctx = await _ctx(bot)
        await G.handle_start_payload(ctx, "gs_%d" % CHAT)
        assert ctx.wiz.kind(ADMIN) == G.WIZARD_KIND
        assert ctx.wiz.get(ADMIN)["data"]["chat_id"] == CHAT

    async def test_topic_name_creates_a_forum_topic(self):
        store = await get_store()
        await store.groups.ensure_config(CHAT, admin_user_id=ADMIN)
        bot = _bot(get_chat_member=_member("administrator"),
                   create_forum_topic=SimpleNamespace(message_thread_id=77))
        ctx = await _ctx(bot)
        await G.handle_start_payload(ctx, "gs_%d" % CHAT)
        await hifz.dispatch_wizard(await _ctx(bot), "Daily Hifz")

        assert (await store.groups.get_config(CHAT)).thread_id == 77
        bot.create_forum_topic.assert_awaited_once()

    async def test_a_non_forum_group_falls_back_to_no_topic(self):
        store = await get_store()
        await store.groups.ensure_config(CHAT, admin_user_id=ADMIN)
        bot = _bot(get_chat_member=_member("administrator"))
        bot.create_forum_topic.side_effect = telegram.error.BadRequest(
            "the group is not a forum")
        ctx = await _ctx(bot)
        await G.handle_start_payload(ctx, "gs_%d" % CHAT)
        await hifz.dispatch_wizard(await _ctx(bot), "Daily Hifz")

        assert (await store.groups.get_config(CHAT)).thread_id is None  # fallback

    async def test_choosing_a_language_activates_the_group(self):
        store = await get_store()
        await store.groups.ensure_config(CHAT, admin_user_id=ADMIN)
        bot = _bot(get_chat_member=_member("administrator"),
                   create_forum_topic=SimpleNamespace(message_thread_id=77))
        await G.handle_start_payload(await _ctx(bot), "gs_%d" % CHAT)
        await hifz.dispatch_wizard(await _ctx(bot), "Daily Hifz")

        # the language pick is a gr: callback
        ctx = await _ctx(bot)
        ctx = await Ctx.build(bot, {}, ctx.file, ADMIN, ADMIN, _Settings(),
                              callback_query=SimpleNamespace(id="cq", message=None))
        await hifz.dispatch_callback(ctx, "gr:tl:ru")

        config = await store.groups.get_config(CHAT)
        assert config.translation_lang == "ru"
        assert config.status == "active"
        assert ctx.wiz.is_active(ADMIN) is False


# --- J6 entry: a member joins the board ----------------------------------------

class TestBoardJoin:
    async def test_a_member_is_linked(self):
        store = await get_store()
        await store.groups.ensure_config(CHAT, admin_user_id=ADMIN)
        bot = _bot(get_chat_member=_member("member"))
        ctx = await _ctx(bot, user=42)
        assert await G.handle_start_payload(ctx, "gb_%d" % CHAT) is True
        assert await store.groups.is_linked(42, CHAT) is True

    async def test_a_non_member_is_refused(self):
        store = await get_store()
        await store.groups.ensure_config(CHAT, admin_user_id=ADMIN)
        bot = _bot(get_chat_member=_member("left"))
        ctx = await _ctx(bot, user=42)
        await G.handle_start_payload(ctx, "gb_%d" % CHAT)
        assert await store.groups.is_linked(42, CHAT) is False

    async def test_get_chat_member_error_is_treated_as_not_a_member(self):
        store = await get_store()
        await store.groups.ensure_config(CHAT, admin_user_id=ADMIN)
        bot = _bot()
        bot.get_chat_member.side_effect = telegram.error.BadRequest("user not found")
        ctx = await _ctx(bot, user=42)
        await G.handle_start_payload(ctx, "gb_%d" % CHAT)
        assert await store.groups.is_linked(42, CHAT) is False

    async def test_a_non_group_payload_is_not_claimed(self):
        ctx = await _ctx(_bot())
        assert await G.handle_start_payload(ctx, "somethingelse") is False


class TestRegistration:
    def test_group_prefix_is_allocated_and_distinct(self):
        assert hifz.PREFIXES["group"] == "gr:"
        vals = list(hifz.PREFIXES.values())
        assert len(set(vals)) == len(vals)

    def test_the_callback_and_wizard_register(self):
        hifz.load_features()
        assert "gr:" in hifz.CALLBACKS
        assert G.WIZARD_KIND in hifz.WIZARDS
