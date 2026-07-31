"""Phase 1 acceptance — `docs/HIFZ_PLATFORM.md` §7, executed.

Every other test file checks one unit against its own contract. This one walks
the seven things the spec says must be true of the finished product, in the
order a real user meets them, through the same seam `main.handle_update` uses.

It is deliberately end to end and deliberately slow-ish: it is the file that
answers "is the feature actually built", and it is the one to run before a
deploy. If a refactor keeps every unit test green and breaks this, the refactor
broke the product.
"""

from datetime import date, datetime, time, timedelta, timezone
from unittest.mock import AsyncMock

import pytest

import hifz
from hifz import Ctx
from hifz import memorize as memorize_feature
from lib import scheduler
from lib.hifz_progress import summarize
from lib.leaderboard import weekly_board
from lib.store import get_store
from lib.store.sessions import KIND_DRILL, KIND_RECALL_CHECK
from lib.streaks import record_session, streak_summary
from lib.wizard import Wizard

USER = 990001
CHAT = 990001
BOOK_LEARNER = 990002        # memorizes from a physical mushaf, never runs a drill
AL_MULK = 67
OFFSET = "+05:00"


class _Settings:
    ui_lang = "en"
    translation_lang = "en"
    reciter = "Husary_128kbps"


@pytest.fixture(autouse=True)
def _isolate_registries():
    saved = (dict(hifz.COMMANDS), dict(hifz.CALLBACKS), dict(hifz.WIZARDS), hifz._loaded)
    handlers = dict(scheduler.SEND_HANDLERS)
    yield
    hifz.COMMANDS.clear()
    hifz.COMMANDS.update(saved[0])
    hifz.CALLBACKS.clear()
    hifz.CALLBACKS.update(saved[1])
    hifz.WIZARDS.clear()
    hifz.WIZARDS.update(saved[2])
    hifz._loaded = saved[3]
    scheduler.SEND_HANDLERS.clear()
    scheduler.SEND_HANDLERS.update(handlers)


class _Message:
    def __init__(self):
        self.message_id = 1
        self.photo = None
        self.audio = None


class _CallbackQuery:
    def __init__(self):
        self.id = "cq"
        self.message = _Message()


async def _ctx(bot=None, user=USER, argument="", tap=False) -> Ctx:
    from lib.utils import File
    bot = bot or AsyncMock()
    extra = {"callback_query": _CallbackQuery()} if tap else {"message": _Message()}
    return await Ctx.build(bot, {}, File(), user, user, _Settings(),
                           argument=argument, **extra)


async def _cmd(name, bot=None, user=USER, argument=""):
    bot = bot or AsyncMock()
    assert await hifz.dispatch_command(await _ctx(bot, user, argument), name) is True
    return bot


async def _tap(cb, bot=None, user=USER):
    bot = bot or AsyncMock()
    assert await hifz.dispatch_callback(await _ctx(bot, user, tap=True), cb) is True
    return bot


async def _type(text, bot=None, user=USER):
    bot = bot or AsyncMock()
    await hifz.dispatch_wizard(await _ctx(bot, user), text)
    return bot


def _texts(bot):
    """Every message body the bot sent *or edited in place*, in order.

    Wizard steps mostly edit the message the button was on rather than sending a
    new one, so a helper that only read `send_message` would quietly miss most of
    the flow — including the preview calendar.
    """
    return ([c.kwargs.get("text", "") for c in bot.send_message.await_args_list]
            + [c.kwargs.get("text", "") for c in bot.edit_message_text.await_args_list])


# --- 1. A plan is set up, and previewed before it is saved ----------------------

class TestOneSetUpAPlan:
    """"A user runs /memorize, picks Al-Mulk, a pace and a reminder time, and
    sees a day-by-day preview before saving.\""""

    async def test_the_preview_comes_before_anything_is_stored(self):
        store = await get_store()
        await _cmd("memorize")
        await _tap("hm:t:s")
        await _type("67")
        await _tap("hm:p:2")
        await _tap("hm:d:wk")
        await _tap("hm:tz:" + OFFSET)
        preview_bot = await _tap("hm:rt:07:00")

        # The preview has been shown...
        assert any(t.strip() for t in _texts(preview_bot))
        # ...and nothing is in the database yet.
        assert await store.plans.get_active_plan(USER) is None
        assert Wizard().is_active(USER) is True

        await _tap("hm:ok")
        plan = await store.plans.get_active_plan(USER)
        assert plan is not None
        assert (plan.start_surah, plan.end_surah) == (AL_MULK, AL_MULK)

    async def test_the_preview_shows_every_day_of_the_plan(self):
        store = await get_store()
        await _run_wizard()
        preview = await _tap("hm:rt:07:00")
        shown = "\n".join(_texts(preview))
        await _tap("hm:ok")
        plan = await store.plans.get_active_plan(USER)
        days = await store.plans.list_plan_days(plan.id)
        assert len(days) == 18                      # 15 portions + 3 consolidation
        # the calendar the user approved names its first and last day
        assert days[0].scheduled_date.isoformat() in shown
        assert days[-1].scheduled_date.isoformat() in shown


async def _run_wizard(user=USER):
    await _cmd("memorize", user=user)
    await _tap("hm:t:s", user=user)
    await _type("67", user=user)
    await _tap("hm:p:2", user=user)
    await _tap("hm:d:wk", user=user)
    await _tap("hm:tz:" + OFFSET, user=user)


async def _save_plan(user=USER):
    await _run_wizard(user)
    await _tap("hm:rt:07:00", user=user)
    await _tap("hm:ok", user=user)
    store = await get_store()
    return await store.plans.get_active_plan(user)


# --- 2. The push fires unprompted, exactly once, across a restart ---------------

class TestTwoTheDailyPush:
    """"At their local reminder time the next day the bot pushes that day's
    portion unprompted — verified by restarting the app between scheduling and
    firing, with no duplicate send.\""""

    async def test_saving_a_plan_queues_a_push_at_the_local_reminder_time(self):
        store = await get_store()
        await _save_plan()
        rows = list(store.schedule._state.scheduled_send.values())
        assert len(rows) == 1
        row = rows[0]
        assert row.kind == memorize_feature.SEND_KIND
        assert row.target_chat_id == CHAT
        # 07:00 local at +05:00 is 02:00 UTC
        assert row.due_at.astimezone(timezone.utc).hour == 2

    async def test_a_restart_between_scheduling_and_firing_delivers_exactly_once(self):
        """The spec's sharpest criterion, and the reason the queue exists."""
        store = await get_store()
        await _save_plan()
        row = list(store.schedule._state.scheduled_send.values())[0]

        delivered = []

        async def counting(ctx):
            delivered.append(ctx.payload["plan_day_id"])

        scheduler.SEND_HANDLERS[memorize_feature.SEND_KIND] = counting

        # The process dies before the row is due, and boots again.
        after_boot = row.due_at - timedelta(minutes=5)
        await scheduler.catch_up(AsyncMock(), {}, now=after_boot, store=store)
        assert delivered == [], "nothing is due yet"

        # Now it comes due, and every subsequent tick must be a no-op.
        await scheduler.tick(AsyncMock(), {}, now=row.due_at, store=store)
        await scheduler.tick(AsyncMock(), {}, now=row.due_at + timedelta(minutes=1),
                             store=store)
        await scheduler.tick(AsyncMock(), {}, now=row.due_at + timedelta(minutes=2),
                             store=store)
        assert len(delivered) == 1, "exactly once, across a restart"

    async def test_the_push_queues_the_following_day(self, monkeypatch):
        """Otherwise the chain stops after one push and the feature dies quietly.

        The real handler runs — only the two senders are stubbed, since they
        would otherwise reach for the audio CDN. What is under test is the
        handler's own decision to queue tomorrow, so it must not be stubbed out.
        """
        async def no_network(*args, **kwargs):
            pass

        monkeypatch.setattr(memorize_feature, "send_combined_audio", no_network)
        monkeypatch.setattr(memorize_feature, "send_quran", no_network)

        store = await get_store()
        await _save_plan()
        row = list(store.schedule._state.scheduled_send.values())[0]

        await scheduler.tick(AsyncMock(), {}, now=row.due_at, store=store)

        queued = [r for r in store.schedule._state.scheduled_send.values()
                  if r.state == "pending"]
        assert queued, "the next portion should already be queued"
        assert queued[0].due_at > row.due_at


# --- 3. A completed drill and a passed check tick the streak once ---------------

class TestThreeTheStreak:
    """"Completing that drill and passing the recall check ticks the streak
    once; /streak shows 1.\""""

    async def test_two_sessions_in_one_local_day_tick_the_streak_once(self):
        store = await get_store()
        await store.profiles.ensure_profile(USER)
        await store.profiles.set_timezone(USER, OFFSET)
        now = datetime(2026, 8, 3, 6, 0, tzinfo=timezone.utc)   # 11:00 local

        drill = await record_session(USER, KIND_DRILL, utc_now=now,
                                     surah=AL_MULK, start_ayah=1, end_ayah=2)
        check = await record_session(USER, KIND_RECALL_CHECK, utc_now=now,
                                     surah=AL_MULK, start_ayah=1, end_ayah=2)
        assert drill.logged and check.logged            # both are real sessions
        assert drill.local_date == check.local_date

        summary = await streak_summary(USER, utc_now=now)
        assert summary.current == 1, "one day, however many sessions"
        assert summary.longest == 1

    async def test_streak_renders_for_that_user(self):
        store = await get_store()
        await store.profiles.ensure_profile(USER)
        await store.profiles.set_timezone(USER, OFFSET)
        await record_session(USER, KIND_DRILL,
                             utc_now=datetime(2026, 8, 3, 6, 0, tzinfo=timezone.utc))
        bot = AsyncMock()
        bot.send_photo.return_value = type("M", (), {"photo": [type("P", (), {
            "file_id": "FID"})()]})()
        await _cmd("streak", bot)
        assert bot.send_photo.await_count == 1, "the contribution graph"

    async def test_no_percentile_claim_is_ever_rendered(self):
        """Assumption 2: not until >=200 users have a streak."""
        store = await get_store()
        await store.profiles.ensure_profile(USER)
        await record_session(USER, KIND_DRILL,
                             utc_now=datetime(2026, 8, 3, 6, 0, tzinfo=timezone.utc))
        summary = await streak_summary(USER)
        assert summary.percentile is None


# --- 4. Percentages are derived, and merging is visible in them -----------------

class TestFourProgress:
    """"Marking 67:1-8 memorized makes /progress report Al-Mulk 27%; re-marking
    67:5-10 reports 33%." And "/forgot 67:5-6 splits 67:1-10 into 67:1-4 and
    67:7-10.\""""

    async def test_twenty_seven_then_thirty_three(self):
        store = await get_store()
        await store.hifz.add_interval(USER, AL_MULK, 1, 8)
        summary = summarize(await store.hifz.list_intervals(USER), AL_MULK)
        assert (summary.focus.done, summary.focus.total) == (8, 30)
        assert summary.focus.percent_text == "27"

        await store.hifz.add_interval(USER, AL_MULK, 5, 10)
        summary = summarize(await store.hifz.list_intervals(USER), AL_MULK)
        assert (summary.focus.done, summary.focus.total) == (10, 30)
        assert summary.focus.percent_text == "33", "47% would mean the merge failed"

    async def test_forgot_splits_an_interval_in_two(self):
        store = await get_store()
        await store.hifz.add_interval(USER, AL_MULK, 1, 10)
        await _cmd("forgot", argument="67:5-6")
        spans = [(i.start_ayah, i.end_ayah)
                 for i in await store.hifz.list_intervals(USER, AL_MULK)]
        assert spans == [(1, 4), (7, 10)]

    async def test_progress_reports_the_juz_in_pages_and_the_surah_in_ayahs(self):
        store = await get_store()
        await store.hifz.add_interval(USER, AL_MULK, 1, 8)
        summary = summarize(await store.hifz.list_intervals(USER), AL_MULK)
        assert summary.focus.total == 30                      # ayahs
        assert summary.focus_juz_pages.total_pages == 20.0    # pages, juz 29
        assert summary.quran_pages.total_pages == 604.0

    async def test_the_command_renders(self):
        store = await get_store()
        await store.hifz.add_interval(USER, AL_MULK, 1, 8)
        bot = await _cmd("progress")
        assert bot.send_message.await_count == 1
        assert "27" in _texts(bot)[0]


# --- 5 & 6. The board, and the user who never runs a drill ----------------------

class TestFiveAndSixTheBoard:
    """"An opted-in user appears in /leaderboard; opting out removes them within
    one command." And "a user who never runs a drill but passes a recall check
    still earns the session and appears on the board.\""""

    async def test_opting_in_puts_you_on_the_board_and_opting_out_removes_you(self):
        store = await get_store()
        await store.profiles.ensure_profile(USER)
        await store.profiles.set_display_name(USER, "Otabek")
        await store.profiles.set_leaderboard_opt_in(USER, True)
        await record_session(USER, KIND_DRILL,
                             utc_now=datetime(2026, 8, 3, 6, 0, tzinfo=timezone.utc))

        board = await weekly_board(USER, utc_now=datetime(2026, 8, 3, 6, 0,
                                                          tzinfo=timezone.utc))
        assert any(e.user_id == USER for e in board.entries)

        await _tap("hp:board:off")               # one command
        board = await weekly_board(USER, utc_now=datetime(2026, 8, 3, 6, 0,
                                                          tzinfo=timezone.utc))
        assert not any(e.user_id == USER for e in board.entries)
        assert board.me is None

    async def test_the_book_learner_earns_the_day_without_ever_running_a_drill(self):
        """The whole reason the recall check exists: it tests hifz, not app use."""
        store = await get_store()
        await store.profiles.ensure_profile(BOOK_LEARNER)
        await store.profiles.set_display_name(BOOK_LEARNER, "Hafiz")
        await store.profiles.set_leaderboard_opt_in(BOOK_LEARNER, True)
        now = datetime(2026, 8, 3, 6, 0, tzinfo=timezone.utc)

        assert await store.plans.get_active_plan(BOOK_LEARNER) is None

        outcome = await record_session(BOOK_LEARNER, KIND_RECALL_CHECK, utc_now=now,
                                       surah=AL_MULK, start_ayah=1, end_ayah=1)
        assert outcome.logged is True
        assert outcome.streak.current == 1

        board = await weekly_board(BOOK_LEARNER, utc_now=now)
        assert any(e.user_id == BOOK_LEARNER for e in board.entries), \
            "someone memorizing from a physical mushaf is a first-class citizen"

    async def test_a_recall_check_earns_at_most_one_session_a_day(self):
        store = await get_store()
        await store.profiles.ensure_profile(BOOK_LEARNER)
        now = datetime(2026, 8, 3, 6, 0, tzinfo=timezone.utc)
        first = await record_session(BOOK_LEARNER, KIND_RECALL_CHECK, utc_now=now,
                                     surah=AL_MULK, start_ayah=1, end_ayah=1)
        again = await record_session(BOOK_LEARNER, KIND_RECALL_CHECK, utc_now=now,
                                     surah=AL_MULK, start_ayah=1, end_ayah=1)
        assert first.logged is True
        assert again.logged is False, "the same portion twice is not two sessions"


# --- 7. Everything is reachable -------------------------------------------------

class TestSevenTheCommandsExist:
    def test_every_new_command_is_registered_and_advertised(self):
        from locales import BOT_COMMANDS, welcome_text
        hifz.load_features()
        welcome = welcome_text("en")
        for name in ("memorize", "progress", "streak", "leaderboard", "profile",
                     "check", "forgot"):
            assert hifz.handles(name), "%s has no handler" % name
            assert name in {c for c, _ in BOT_COMMANDS}, "%s is not in the menu" % name
            assert "/%s " % name in welcome, "%s is not in /start" % name

    def test_the_scheduler_starts_at_boot(self):
        """A loop nobody starts is a feature nobody gets."""
        source = open("src/main.py", encoding="utf-8").read()
        assert "run_scheduler" in source
        assert "hifz.load_features()" in source
        assert source.index("hifz.load_features()") < source.index("run_scheduler"), \
            "handlers must be registered before the loop that dispatches to them"
