"""`/leaderboard` in DM (H2).

Driven through the seam with an `AsyncMock` bot, the way `tests/test_hifz_seam.py`
does, so a registration mistake fails here rather than in production.

The two properties that matter: an opted-out user is absent from the board
because the *query* excludes them, not because the renderer hides them; and the
caller's own rank is always shown even when they are nowhere near the top — a
board that only ever shows ten strangers is not motivating.
"""

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock

import pytest

import hifz
from hifz import Ctx
from lib.store import get_store
from lib.store.sessions import KIND_DRILL

USER_ID = 930001
CHAT_ID = 930001

# A Wednesday, so the Mon-Sun window is unambiguous.
NOW = datetime(2026, 7, 29, 12, 0, tzinfo=timezone.utc)
TODAY = date(2026, 7, 29)


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


class _Message:
    def __init__(self):
        self.message_id = 77
        self.photo = None
        self.audio = None


class _CallbackQuery:
    def __init__(self):
        self.id = "cq-1"
        self.message = _Message()


async def _ctx(bot=None, user_id=USER_ID, argument="", tap=False) -> Ctx:
    from lib.utils import File
    bot = bot or AsyncMock()
    extra = {"callback_query": _CallbackQuery()} if tap else {"message": _Message()}
    return await Ctx.build(bot, {}, File(), user_id, user_id, _Settings(),
                           argument=argument, **extra)


def _sent(bot) -> str:
    return bot.send_message.await_args.kwargs["text"]


async def _join(store, user_id: int, name: str):
    await store.profiles.ensure_profile(user_id)
    await store.profiles.set_display_name(user_id, name)
    await store.profiles.set_leaderboard_opt_in(user_id, True)


async def _earn(store, user_id: int, sessions: int, day: date = TODAY):
    """`sessions` distinct logged sessions inside the current week."""
    for n in range(sessions):
        await store.sessions.log_session(user_id, day, KIND_DRILL,
                                         surah=67, start_ayah=n + 1, end_ayah=n + 1)


class TestBoard:
    async def test_an_opted_in_user_appears(self):
        store = await get_store()
        await _join(store, USER_ID, "Otabek")
        await _earn(store, USER_ID, 3)

        bot = AsyncMock()
        await hifz.dispatch_command(await _ctx(bot), "leaderboard")
        assert bot.send_message.await_count or bot.send_photo.await_count

    async def test_an_opted_out_user_is_absent_from_the_query_not_just_the_render(self):
        """H1's done-when, asserted at the source rather than in the text."""
        from lib.leaderboard import weekly_board
        store = await get_store()
        await _join(store, USER_ID, "Otabek")
        await _earn(store, USER_ID, 3)

        board = await weekly_board(USER_ID, utc_now=NOW)
        assert any(e.user_id == USER_ID for e in board.entries)

        await store.profiles.set_leaderboard_opt_in(USER_ID, False)
        board = await weekly_board(USER_ID, utc_now=NOW)
        assert not any(e.user_id == USER_ID for e in board.entries)
        assert board.me is None
        assert board.opted_in is False

    async def test_a_user_outside_the_top_ten_still_sees_their_own_rank(self):
        """"a user ranked 400th sees rows 1-10 plus their own row"."""
        from lib.leaderboard import weekly_board
        store = await get_store()
        # twenty people ahead of the caller
        for n in range(20):
            other = 931000 + n
            await _join(store, other, "H%d" % n)
            await _earn(store, other, 10 - (n % 5) + 5)
        await _join(store, USER_ID, "Otabek")
        await _earn(store, USER_ID, 1)

        board = await weekly_board(USER_ID, utc_now=NOW, limit=10)
        assert len(board.entries) == 10
        assert board.me is not None
        assert board.me.user_id == USER_ID
        assert board.me.position > 10
        assert board.me_in_top is False

    async def test_a_user_inside_the_top_is_not_drawn_twice(self):
        from lib.leaderboard import weekly_board
        store = await get_store()
        await _join(store, USER_ID, "Otabek")
        await _earn(store, USER_ID, 9)

        board = await weekly_board(USER_ID, utc_now=NOW, limit=10)
        assert board.me_in_top is True
        assert sum(1 for e in board.entries if e.user_id == USER_ID) == 1

    async def test_the_command_renders_for_a_user_with_nothing(self):
        bot = AsyncMock()
        await hifz.dispatch_command(await _ctx(bot), "leaderboard")
        assert bot.send_message.await_count == 1
        assert _sent(bot).strip()

    async def test_an_opted_out_caller_is_offered_the_opt_in(self):
        """Rather than a board they are not on, which would just look broken."""
        store = await get_store()
        await store.profiles.ensure_profile(USER_ID)
        bot = AsyncMock()
        await hifz.dispatch_command(await _ctx(bot), "leaderboard")
        assert bot.send_message.await_count == 1
        # the offer is a button, not a dead end
        assert bot.send_message.await_args.kwargs.get("reply_markup") is not None

    async def test_the_window_is_monday_to_sunday(self):
        from lib.leaderboard import week_window
        start, end = week_window(NOW, "+00:00")
        assert start.weekday() == 0 and end.weekday() == 6
        assert (end - start).days == 6

    async def test_a_session_from_last_week_does_not_count(self):
        from lib.leaderboard import weekly_board
        store = await get_store()
        await _join(store, USER_ID, "Otabek")
        await _earn(store, USER_ID, 2, day=date(2026, 7, 20))   # previous week
        board = await weekly_board(USER_ID, utc_now=NOW)
        assert board.me is None or board.me.sessions == 0


class TestDispatch:
    def test_the_command_is_registered(self):
        hifz.load_features()
        assert hifz.handles("leaderboard") is True

    async def test_a_stale_callback_is_acknowledged_not_crashed(self):
        bot = AsyncMock()
        ctx = await _ctx(bot, tap=True)
        # garbage under the leaderboard's own prefix
        assert await hifz.dispatch_callback(ctx, "hl:nonsense:42") is True
        bot.answer_callback_query.assert_awaited()
