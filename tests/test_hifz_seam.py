"""The hifz seam (`src/hifz/__init__.py`).

`src/main.py` grew one `elif command == ...` at a time; the memorization platform
adds seven commands, a dozen callbacks and three wizards. Rather than double that
file, features live in `src/hifz/` and register themselves, and main.py gains
three call sites.

These tests pin the contract every feature module is written against — the
registration API, the dispatch rules, and above all the property that makes
parallel work possible: **registration is conflict-free**, because discovery
walks the package directory instead of reading a shared import list.
"""

import os
from unittest.mock import AsyncMock

import pytest
import telegram

import hifz
from hifz import Ctx


class _Settings:
    ui_lang = "en"
    translation_lang = "en"
    reciter = "Husary_128kbps"


@pytest.fixture(autouse=True)
def _isolate_registries():
    """Snapshot and restore the module-level registries.

    They are process-wide, so a test that registers a dummy command would
    otherwise leak it into every later test — and into the real boot path.
    """
    saved = (dict(hifz.COMMANDS), dict(hifz.CALLBACKS), dict(hifz.WIZARDS), hifz._loaded)
    yield
    hifz.COMMANDS.clear()
    hifz.COMMANDS.update(saved[0])
    hifz.CALLBACKS.clear()
    hifz.CALLBACKS.update(saved[1])
    hifz.WIZARDS.clear()
    hifz.WIZARDS.update(saved[2])
    hifz._loaded = saved[3]


async def _ctx(**kwargs) -> Ctx:
    bot = kwargs.pop("bot", None) or AsyncMock()
    from lib.utils import File
    return await Ctx.build(bot, {}, File(), 900001, 900001, _Settings(), **kwargs)


# --- Registration --------------------------------------------------------------

class TestRegistration:
    async def test_command_decorator_claims_a_slash_command(self):
        calls = []

        @hifz.command("dummycmd")
        async def handler(ctx):
            calls.append(ctx)

        assert hifz.handles("dummycmd") is True
        assert hifz.handles("/dummycmd") is True      # leading slash tolerated
        assert hifz.handles("DUMMYCMD") is True       # main.py lowercases anyway
        assert await hifz.dispatch_command(await _ctx(), "dummycmd") is True
        assert len(calls) == 1

    async def test_a_command_can_have_aliases(self):
        @hifz.command("aliasone", "aliastwo")
        async def handler(ctx):
            pass

        assert hifz.handles("aliasone") and hifz.handles("aliastwo")

    def test_registering_a_command_twice_raises_at_import_time(self):
        @hifz.command("clash")
        async def first(ctx):
            pass

        with pytest.raises(ValueError, match="already registered"):
            @hifz.command("clash")
            async def second(ctx):
                pass

    def test_re_registering_the_same_handler_is_not_a_clash(self):
        # module reloaded under test; the same function is not a collision
        async def handler(ctx):
            pass

        hifz.command("idempotent")(handler)
        hifz.command("idempotent")(handler)
        assert hifz.COMMANDS["idempotent"] is handler

    def test_registering_a_callback_prefix_twice_raises(self):
        @hifz.callback("zz:")
        async def first(ctx, cb):
            pass

        with pytest.raises(ValueError, match="already registered"):
            @hifz.callback("zz:")
            async def second(ctx, cb):
                pass

    def test_registering_a_wizard_kind_twice_raises(self):
        @hifz.wizard("zzkind")
        async def first(ctx, text):
            pass

        with pytest.raises(ValueError, match="already registered"):
            @hifz.wizard("zzkind")
            async def second(ctx, text):
                pass

    def test_unregistered_things_are_not_claimed(self):
        assert hifz.handles("definitely-not-a-command") is False
        assert hifz.handles_callback("nope:1") is False


class TestConflictFreeByConstruction:
    """The property the whole parallel-agent plan rests on."""

    def test_the_package_has_no_shared_import_list(self):
        # If __init__.py named the feature modules, every agent adding a feature
        # would edit the same line — the merge point this design exists to avoid.
        source = open(os.path.join(os.path.dirname(hifz.__file__), "__init__.py"),
                      encoding="utf-8").read()
        for feature in ("profile", "progress", "memorize", "check", "streak",
                        "leaderboard"):
            assert "import %s" % feature not in source, feature
            assert "from .%s" % feature not in source, feature

    def test_discovery_walks_the_directory(self):
        hifz.reset_for_tests()
        counts = hifz.load_features()
        assert counts["commands"] >= 1          # at least the seam's own /cancel
        assert hifz.handles("cancel") is True

    def test_load_features_is_idempotent(self):
        hifz.reset_for_tests()
        first = hifz.load_features()
        second = hifz.load_features()
        assert first == second

    def test_a_broken_feature_does_not_take_the_bot_down(self, capsys):
        # One feature failing to import must be reported and skipped, not fatal —
        # otherwise a typo in one module costs the whole bot. The probe is named
        # without a leading underscore so discovery actually imports it.
        broken = os.path.join(os.path.dirname(hifz.__file__), "zz_broken_probe.py")
        try:
            with open(broken, "w", encoding="utf-8") as fp:
                fp.write("raise RuntimeError('boom')\n")
            hifz.reset_for_tests()
            hifz.load_features()                    # must not raise
            assert "zz_broken_probe" in capsys.readouterr().out
            assert hifz.handles("cancel") is True   # the healthy ones still loaded
        finally:
            os.remove(broken)

    def test_private_modules_are_skipped_by_discovery(self):
        # a leading underscore marks a helper, not a feature
        probe = os.path.join(os.path.dirname(hifz.__file__), "_zz_private_probe.py")
        try:
            with open(probe, "w", encoding="utf-8") as fp:
                fp.write("raise RuntimeError('discovery must not import this')\n")
            hifz.reset_for_tests()
            hifz.load_features()                    # must not raise
        finally:
            os.remove(probe)


# --- Dispatch ------------------------------------------------------------------

class TestDispatchCommand:
    async def test_unclaimed_command_returns_false(self):
        assert await hifz.dispatch_command(await _ctx(), "nosuchcommand") is False

    async def test_the_argument_reaches_the_handler(self):
        seen = {}

        @hifz.command("witharg")
        async def handler(ctx):
            seen["argument"] = ctx.argument

        await hifz.dispatch_command(await _ctx(argument="67"), "witharg")
        assert seen["argument"] == "67"


class TestDispatchCallback:
    async def test_prefix_match_dispatches(self):
        seen = {}

        @hifz.callback("zz:")
        async def handler(ctx, cb_data):
            seen["cb"] = cb_data

        assert await hifz.dispatch_callback(await _ctx(), "zz:board:on") is True
        assert seen["cb"] == "zz:board:on"      # full data, prefix included

    async def test_unclaimed_callback_returns_false(self):
        assert await hifz.dispatch_callback(await _ctx(), "unclaimed:1") is False

    async def test_empty_callback_data_is_not_claimed(self):
        assert await hifz.dispatch_callback(await _ctx(), "") is False

    async def test_longest_prefix_wins(self):
        # so "hm:day:" can be split out of "hm:" later without "hm:" swallowing it
        hit = []

        @hifz.callback("zz:")
        async def broad(ctx, cb_data):
            hit.append("broad")

        @hifz.callback("zz:day:")
        async def narrow(ctx, cb_data):
            hit.append("narrow")

        await hifz.dispatch_callback(await _ctx(), "zz:day:3")
        assert hit == ["narrow"]

    async def test_a_raising_handler_still_answers_the_tap(self):
        # An unanswered callback leaves a spinner on the user's screen forever.
        @hifz.callback("zz:")
        async def handler(ctx, cb_data):
            raise ValueError("malformed callback data")

        bot = AsyncMock()
        cq = type("CQ", (), {"id": "cq1", "message": None})()
        ctx = await _ctx(bot=bot, callback_query=cq)
        assert await hifz.dispatch_callback(ctx, "zz:garbage") is True
        bot.answer_callback_query.assert_awaited()

    async def test_forbidden_propagates_for_main_to_handle(self):
        # main._process_update swallows Forbidden (user blocked the bot); the seam
        # must not turn it into a generic logged error.
        @hifz.callback("zz:")
        async def handler(ctx, cb_data):
            raise telegram.error.Forbidden("bot was blocked by the user")

        with pytest.raises(telegram.error.Forbidden):
            await hifz.dispatch_callback(await _ctx(), "zz:x")


class TestDispatchWizard:
    async def test_no_draft_means_not_consumed(self):
        ctx = await _ctx()
        ctx.wiz.clear(ctx.user_id)
        assert await hifz.dispatch_wizard(ctx, "67:1-8") is False

    async def test_free_text_reaches_the_registered_kind(self):
        seen = {}

        @hifz.wizard("zzflow")
        async def handler(ctx, text):
            seen["text"] = text

        ctx = await _ctx()
        ctx.wiz.start(ctx.user_id, "zzflow")
        assert await hifz.dispatch_wizard(ctx, "Abu Bakr") is True
        assert seen["text"] == "Abu Bakr"       # raw, not lowercased

    async def test_cancel_ends_any_wizard_without_the_feature_handling_it(self):
        @hifz.wizard("zzflow")
        async def handler(ctx, text):
            raise AssertionError("cancel must not reach the feature handler")

        bot = AsyncMock()
        ctx = await _ctx(bot=bot)
        ctx.wiz.start(ctx.user_id, "zzflow")
        assert await hifz.dispatch_wizard(ctx, "/cancel") is True
        assert ctx.wiz.is_active(ctx.user_id) is False
        bot.send_message.assert_awaited()

    async def test_a_draft_whose_feature_vanished_is_dropped_not_trapped(self):
        ctx = await _ctx()
        ctx.wiz.start(ctx.user_id, "kind-nothing-handles")
        assert await hifz.dispatch_wizard(ctx, "hello") is False
        assert ctx.wiz.is_active(ctx.user_id) is False

    async def test_a_raising_step_clears_the_draft_and_tells_the_user(self):
        @hifz.wizard("zzflow")
        async def handler(ctx, text):
            raise ValueError("bad input")

        bot = AsyncMock()
        ctx = await _ctx(bot=bot)
        ctx.wiz.start(ctx.user_id, "zzflow")
        assert await hifz.dispatch_wizard(ctx, "garbage") is True
        assert ctx.wiz.is_active(ctx.user_id) is False   # not stuck forever
        bot.send_message.assert_awaited()

    async def test_has_wizard_gates_the_slot(self):
        ctx = await _ctx()
        ctx.wiz.clear(ctx.user_id)
        assert hifz.has_wizard(ctx.user_id) is False
        ctx.wiz.start(ctx.user_id, "zzflow")
        assert hifz.has_wizard(ctx.user_id) is True


# --- Ctx -----------------------------------------------------------------------

class TestCtx:
    async def test_carries_the_resolved_settings(self):
        ctx = await _ctx()
        assert ctx.ui_lang == "en"
        assert ctx.translation_lang == "en"
        assert ctx.reciter == "Husary_128kbps"

    async def test_store_is_attached(self):
        ctx = await _ctx()
        for aggregate in ("profiles", "hifz", "plans", "sessions", "schedule"):
            assert hasattr(ctx.store, aggregate), aggregate

    async def test_is_frozen(self):
        ctx = await _ctx()
        with pytest.raises(Exception):
            ctx.ui_lang = "fr"

    async def test_tr_localizes_and_formats(self):
        ctx = await _ctx()
        assert ctx.tr("btn_translation") == "Translation"
        # a key with a placeholder round-trips through str.format
        assert "{n}" not in ctx.tr("range_too_large", n=50)
        assert "50" in ctx.tr("range_too_large", n=50)

    async def test_reply_sends_to_the_callers_chat(self):
        bot = AsyncMock()
        ctx = await _ctx(bot=bot)
        await ctx.reply("hello")
        bot.send_message.assert_awaited_once()
        assert bot.send_message.await_args.kwargs["chat_id"] == ctx.chat_id

    async def test_answer_is_a_noop_off_a_callback(self):
        bot = AsyncMock()
        ctx = await _ctx(bot=bot)
        await ctx.answer()
        bot.answer_callback_query.assert_not_awaited()

    async def test_edit_treats_not_modified_as_success(self):
        # re-tapping the view you are already in is a no-op, not an error
        bot = AsyncMock()
        bot.edit_message_text.side_effect = telegram.error.BadRequest(
            "Message is not modified")
        msg = type("M", (), {"message_id": 7, "photo": None, "audio": None})()
        cq = type("CQ", (), {"id": "cq1", "message": msg})()
        ctx = await _ctx(bot=bot, callback_query=cq)
        assert await ctx.edit("same text") is True

    async def test_edit_reraises_a_real_bad_request(self):
        bot = AsyncMock()
        bot.edit_message_text.side_effect = telegram.error.BadRequest("chat not found")
        msg = type("M", (), {"message_id": 7, "photo": None, "audio": None})()
        cq = type("CQ", (), {"id": "cq1", "message": msg})()
        ctx = await _ctx(bot=bot, callback_query=cq)
        with pytest.raises(telegram.error.BadRequest):
            await ctx.edit("new text")

    async def test_edit_falls_back_to_a_fresh_message_for_media(self):
        # a photo/audio message has no text to edit
        bot = AsyncMock()
        msg = type("M", (), {"message_id": 7, "photo": True, "audio": None})()
        cq = type("CQ", (), {"id": "cq1", "message": msg})()
        ctx = await _ctx(bot=bot, callback_query=cq)
        assert await ctx.edit("text") is False
        bot.send_message.assert_awaited_once()


# --- The callback-data namespace -----------------------------------------------

READER_PREFIXES = ("vc:", "vr:", "rep:", "pg:", "pga:", "recgrp:", "setlang:",
                   "settranslang:", "setreciter:", "showlang", "reciter_search",
                   "recpage_noop", "pgnoop")


class TestPrefixNamespace:
    def test_every_feature_has_a_prefix(self):
        for feature in ("profile", "progress", "memorize", "check", "streak",
                        "leaderboard"):
            assert feature in hifz.PREFIXES, feature

    def test_prefixes_are_unique(self):
        values = list(hifz.PREFIXES.values())
        assert len(set(values)) == len(values)

    def test_no_hifz_prefix_collides_with_the_reader(self):
        # main.py's chain runs first for its own prefixes; a shadow would make a
        # verse-card tap silently reach a hifz handler or vice versa.
        for feature, prefix in hifz.PREFIXES.items():
            for reader in READER_PREFIXES:
                assert not prefix.startswith(reader), (feature, prefix, reader)
                assert not reader.startswith(prefix), (feature, prefix, reader)

    def test_prefixes_leave_room_inside_telegrams_64_byte_cap(self):
        for feature, prefix in hifz.PREFIXES.items():
            assert len(prefix.encode()) <= 4, (feature, prefix)


# --- The _initialize() schema path ---------------------------------------------

class TestSchemaApplication:
    """Regression: Wave 0a made get_pool() return None when DATABASE_URL is unset,
    while main.py still called pool.execute() on it. The AttributeError was
    swallowed by the surrounding try/except, so boot logged an INIT ERROR instead
    of applying the schema — and no test caught it, because nothing drove
    _initialize()."""

    async def test_apply_schema_survives_an_unset_database_url(self):
        from lib.store import apply_schema
        assert os.environ.get("DATABASE_URL") == ""
        await apply_schema()          # must not raise

    def test_main_no_longer_dereferences_the_pool_for_the_schema(self):
        source = open(os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "src", "main.py"), encoding="utf-8").read()
        assert "pool.execute" not in source
        assert "apply_schema" in source

    async def test_schema_application_is_idempotent(self):
        from lib.store import apply_schema
        await apply_schema()
        await apply_schema()          # a restart re-applies it; must stay clean
