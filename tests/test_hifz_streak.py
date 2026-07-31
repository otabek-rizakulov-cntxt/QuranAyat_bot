"""`/streak` (`src/hifz/streak.py`) — spec items G2 and G3.

Two properties are load-bearing:

* **The 12-week grid is a rendered PNG.** §4 G2 and assumption 1 asked for an
  emoji grid; that was overridden with approval. `lib/streak_image.py` renders
  the card and this module sends it, caching the Telegram `file_id` per
  (user, local date) so a user hammering /streak pays for one render a day.
* **No percentile line is ever rendered.** G3 holds "top X% of users" dark until
  ≥200 users have a streak. `streak_summary` takes a `population` argument; this
  module must never pass one, and there is no string in the table to render the
  claim with even if it did.
"""

from datetime import timedelta
from io import BytesIO
from unittest.mock import AsyncMock

import pytest
import telegram

import hifz
from hifz import Ctx
from hifz.streak import CB_GRID
from lib.store import get_store
from lib.store.sessions import KIND_DRILL, KIND_RECALL_CHECK
from lib.streak_image import cache_key
from lib.streaks import refresh_streaks, user_today
from locales import t

USER = 900_601
MILESTONES = ("streak_milestone_7", "streak_milestone_30",
              "streak_milestone_100", "streak_milestone_365")


class _Settings:
    ui_lang = "en"
    translation_lang = "en"
    reciter = "Husary_128kbps"


@pytest.fixture(autouse=True)
def _isolate_registries():
    saved = (dict(hifz.COMMANDS), dict(hifz.CALLBACKS), dict(hifz.WIZARDS), hifz._loaded)
    yield
    hifz.COMMANDS.clear()
    hifz.COMMANDS.update(saved[0])
    hifz.CALLBACKS.clear()
    hifz.CALLBACKS.update(saved[1])
    hifz.WIZARDS.clear()
    hifz.WIZARDS.update(saved[2])
    hifz._loaded = saved[3]


def _photo_message(file_id: str = "FILEID"):
    """What `send_photo` returns: sizes ascending, largest last."""
    size = type("PhotoSize", (), {"file_id": file_id})()
    return type("Message", (), {"message_id": 3, "photo": [size]})()


async def _ctx(bot=None, **kwargs) -> Ctx:
    from lib.utils import File
    bot = bot or AsyncMock()
    bot.send_photo.return_value = _photo_message()
    return await Ctx.build(bot, {}, File(), USER, USER, _Settings(), **kwargs)


async def _streak(bot=None):
    bot = bot or AsyncMock()
    bot.send_photo.return_value = _photo_message()
    ctx = await _ctx(bot=bot)
    assert await hifz.dispatch_command(ctx, "streak") is True
    return bot


async def _earn(days_back=(0,), kind=KIND_DRILL):
    """Log one session on each of the given days-ago and refresh the counters."""
    store = await get_store()
    today = await user_today(USER)
    for back in days_back:
        await store.sessions.log_session(USER, today - timedelta(days=back), kind)
    await refresh_streaks(USER, today=today)
    return today


def _caption(bot) -> str:
    return bot.send_photo.await_args.kwargs["caption"]


# --- The card ------------------------------------------------------------------

class TestStreakCard:
    async def test_a_user_with_no_sessions_gets_the_invitation_not_a_graph(self):
        bot = await _streak()
        text = bot.send_message.await_args.kwargs["text"]
        assert t("streak_title", "en") in text
        assert t("streak_none", "en") in text
        bot.send_photo.assert_not_awaited()          # nothing to render yet

    async def test_the_invitation_offers_a_way_to_earn_today(self):
        bot = await _streak()
        markup = bot.send_message.await_args.kwargs["reply_markup"]
        button = markup.inline_keyboard[0][0]
        assert button.text == t("btn_check_start", "en")
        assert button.callback_data == "hc:start"    # hifz.PREFIXES: the check module

    async def test_a_streak_sends_the_graph_with_both_counters(self):
        await _earn((2, 1, 0))
        bot = await _streak()
        bot.send_photo.assert_awaited_once()
        assert isinstance(bot.send_photo.await_args.kwargs["photo"], BytesIO)
        caption = _caption(bot)
        assert t("streak_title", "en") in caption
        assert t("streak_current", "en").format(n=3) in caption
        assert t("streak_longest", "en").format(n=3) in caption
        assert t("streak_graph_caption", "en") in caption

    async def test_a_day_already_earned_carries_no_call_to_action(self):
        await _earn((0,))
        bot = await _streak()
        assert bot.send_photo.await_args.kwargs["reply_markup"] is None

    async def test_a_streak_at_risk_still_offers_the_check(self):
        await _earn((1,))                            # yesterday, not today
        bot = await _streak()
        markup = bot.send_photo.await_args.kwargs["reply_markup"]
        assert markup.inline_keyboard[0][0].callback_data == "hc:start"

    async def test_a_broken_streak_still_shows_the_lifetime_best(self):
        await _earn((9, 8, 7))                       # long over
        bot = await _streak()
        caption = _caption(bot)
        assert t("streak_current", "en").format(n=0) in caption
        assert t("streak_longest", "en").format(n=3) in caption


# --- G3: milestones, and the percentile that never appears ----------------------

class TestMilestones:
    @pytest.mark.parametrize("days,key", [(7, "streak_milestone_7"),
                                          (30, "streak_milestone_30"),
                                          (100, "streak_milestone_100"),
                                          (365, "streak_milestone_365")])
    async def test_the_milestone_copy_fires_at_the_exact_day(self, days, key):
        await _earn(range(days))
        bot = await _streak()
        caption = _caption(bot)
        assert t(key, "en") in caption
        for other in MILESTONES:
            if other != key:
                assert t(other, "en") not in caption

    async def test_a_day_past_a_milestone_stops_congratulating(self):
        await _earn(range(8))
        bot = await _streak()
        caption = _caption(bot)
        assert all(t(key, "en") not in caption for key in MILESTONES)

    async def test_no_percentile_claim_is_ever_rendered(self):
        # Assumption 2: with a small user base the line stays dark. There is no
        # string for it, so the only way one could appear is a hand-built line.
        for days in (1, 7, 30, 100, 365):
            await _earn(range(days))
            caption = _caption(await _streak())
            assert "%" not in caption
            assert "top" not in caption.lower()

    def test_no_hifz_module_can_reach_the_percentile_machinery(self):
        """`percentile_band` returns None unless a real >=200-user population is
        passed, and `streak_summary(population=...)` is the only way to pass one.
        No handler reaches either — a structural guarantee, not a rendering one.

        Asserted over the parsed AST rather than the source text, so a comment
        *explaining* why we pass no population does not trip the guard that
        enforces it. Grepping the raw file cannot tell code from prose.
        """
        import ast
        import os

        directory = os.path.dirname(hifz.__file__)
        for name in sorted(os.listdir(directory)):
            if not name.endswith(".py"):
                continue
            tree = ast.parse(open(os.path.join(directory, name), encoding="utf-8").read())
            identifiers = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    identifiers.add(node.id)
                elif isinstance(node, ast.Attribute):
                    identifiers.add(node.attr)
                elif isinstance(node, ast.arg):
                    identifiers.add(node.arg)
                elif isinstance(node, ast.keyword) and node.arg:
                    identifiers.add(node.arg)
                elif isinstance(node, ast.alias):
                    identifiers.add(node.asname or node.name)
            assert "population" not in identifiers, name
            assert "percentile" not in identifiers, name
            assert "percentile_band" not in identifiers, name


# --- The file_id cache ---------------------------------------------------------

class TestGraphCache:
    async def test_the_graph_is_rendered_once_a_day_and_re_sent_from_the_file_id(
            self, monkeypatch):
        from lib.utils import File
        import hifz.streak as streak_module

        renders = []
        original = streak_module.render_streak_graph

        async def counting(*args, **kwargs):
            renders.append(kwargs.get("today"))
            return await original(*args, **kwargs)

        monkeypatch.setattr(streak_module, "render_streak_graph", counting)

        today = await _earn((0,))
        first = await _streak()
        assert len(renders) == 1
        assert File().get_file(cache_key(USER, today)) == "FILEID"

        second = await _streak()
        assert len(renders) == 1, "a second /streak the same day must not re-render"
        assert second.send_photo.await_args.kwargs["photo"] == "FILEID"

    async def test_the_cache_is_keyed_per_user_and_per_local_day(self):
        from lib.utils import File
        today = await _earn((0,))
        await _streak()
        assert File().get_file(cache_key(USER, today)) == "FILEID"
        # tomorrow's key is a different key, so the graph is rebuilt then
        assert File().get_file(cache_key(USER, today + timedelta(days=1))) is None
        assert File().get_file(cache_key(USER + 1, today)) is None

    async def test_a_rejected_file_id_falls_back_to_a_fresh_upload(self):
        from lib.utils import File
        today = await _earn((0,))
        File().save_file(cache_key(USER, today), "STALE")

        bot = AsyncMock()
        bot.send_photo.side_effect = [telegram.error.BadRequest("wrong file identifier"),
                                      _photo_message("FRESH")]
        await _streak(bot=bot)

        assert bot.send_photo.await_count == 2
        assert bot.send_photo.await_args_list[0].kwargs["photo"] == "STALE"
        assert isinstance(bot.send_photo.await_args_list[1].kwargs["photo"], BytesIO)
        assert File().get_file(cache_key(USER, today)) == "FRESH"


# --- The callback --------------------------------------------------------------

class TestCallback:
    async def test_the_grid_tap_re_sends_the_card(self):
        await _earn((0,))
        bot = AsyncMock()
        bot.send_photo.return_value = _photo_message()
        cq = type("CQ", (), {"id": "cq-1", "message": None})()
        ctx = await _ctx(bot=bot, callback_query=cq)
        assert await hifz.dispatch_callback(ctx, CB_GRID) is True
        bot.answer_callback_query.assert_awaited()
        bot.send_photo.assert_awaited_once()

    @pytest.mark.parametrize("cb_data", ["hs:", "hs:grid:extra", "hs:garbage"])
    async def test_an_unknown_shape_is_acknowledged_and_ignored(self, cb_data):
        from hifz.streak import on_streak
        bot = AsyncMock()
        cq = type("CQ", (), {"id": "cq-1", "message": None})()
        ctx = await _ctx(bot=bot, callback_query=cq)
        await on_streak(ctx, cb_data)
        bot.answer_callback_query.assert_awaited()
        bot.send_photo.assert_not_awaited()
        bot.send_message.assert_not_awaited()

    def test_every_callback_shape_fits_inside_the_64_byte_cap(self):
        assert len(CB_GRID.encode()) <= 64


# --- What a session is ---------------------------------------------------------

class TestWhatTicksADay:
    async def test_a_recall_check_ticks_the_day_just_like_a_drill(self):
        # The book learner's whole path to a streak.
        await _earn((0,), kind=KIND_RECALL_CHECK)
        bot = await _streak()
        assert t("streak_current", "en").format(n=1) in _caption(bot)
