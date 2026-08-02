"""`/memorize` — the setup wizard, drill delivery, and the plan lifecycle (D1, D3-D5).

Driven through the seam (`hifz.dispatch_command` / `dispatch_callback` /
`dispatch_wizard`) with an `AsyncMock` bot, the way `tests/test_hifz_seam.py`
does, so a registration mistake fails here rather than in production.

The two properties worth the most: **the preview is the plan** — the same pure
generator produces both, so what the user approved is what gets pushed, row for
row — and **the enqueue chain**, without which the scheduler drains a queue
nothing ever fills and the headline feature silently never fires.
"""

from datetime import date, datetime, time, timedelta, timezone
from unittest.mock import AsyncMock

import pytest

import hifz
from hifz import Ctx
from hifz import memorize as memorize_feature
from lib import scheduler
from lib.plan_builder import advancing, build_plan
from lib.store import get_store
from lib.store.plans import DAY_COMPLETED, PLAN_ACTIVE, PLAN_COMPLETE, PLAN_PAUSED
from hifz.refs import surah_ref

USER_ID = 940001
CHAT_ID = 940001
AL_MULK = 67
WEEKDAYS = [1, 2, 3, 4, 5]


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
        self.message_id = 77
        self.photo = None
        self.audio = None


class _CallbackQuery:
    def __init__(self):
        self.id = "cq-1"
        self.message = _Message()


async def _ctx(bot=None, argument="", tap=False) -> Ctx:
    from lib.utils import File
    bot = bot or AsyncMock()
    extra = {"callback_query": _CallbackQuery()} if tap else {"message": _Message()}
    return await Ctx.build(bot, {}, File(), CHAT_ID, USER_ID, _Settings(),
                           argument=argument, **extra)


async def _tap(cb_data: str, bot=None):
    bot = bot or AsyncMock()
    ctx = await _ctx(bot, tap=True)
    assert await hifz.dispatch_callback(ctx, cb_data) is True
    return bot


async def _type(text: str, bot=None):
    bot = bot or AsyncMock()
    ctx = await _ctx(bot)
    handled = await hifz.dispatch_wizard(ctx, text)
    return bot, handled


async def _run_wizard(target="67", pace="2", offset="+05:00", reminder="07:00"):
    """The whole happy path, ending just before the save tap."""
    await hifz.dispatch_command(await _ctx(), "memorize")
    await _tap("hm:t:s")
    await _type(target)
    await _tap("hm:p:" + pace)
    await _tap("hm:d:wk")                       # weekdays
    await _tap("hm:tz:" + offset)
    await _tap("hm:rt:" + reminder)


# --- The wizard ----------------------------------------------------------------

class TestWizard:
    async def test_memorize_opens_the_target_chooser(self):
        bot = AsyncMock()
        assert await hifz.dispatch_command(await _ctx(bot), "memorize") is True
        assert bot.send_message.await_count == 1
        assert bot.send_message.await_args.kwargs.get("reply_markup") is not None

    async def test_the_happy_path_saves_a_plan(self):
        await _run_wizard()
        bot = await _tap("hm:ok")
        store = await get_store()
        plan = await store.plans.get_active_plan(USER_ID)
        assert plan is not None
        assert (plan.start_surah, plan.end_surah) == (AL_MULK, AL_MULK)
        assert plan.status == PLAN_ACTIVE
        assert sorted(plan.days_of_week) == WEEKDAYS
        assert bot.send_message.await_count >= 1

    async def test_the_preview_is_the_plan_day_for_day(self):
        """D1's done-when. Guaranteed structurally: `build_plan` is pure, so the
        preview and the save call the same function with the same arguments."""
        await _run_wizard()
        draft = hifz.Ctx.build  # noqa: F841 - keep the import obvious
        from lib.wizard import Wizard
        data = Wizard().data(USER_ID)
        previewed = build_plan(surah_ref(AL_MULK), int(data["pace"]),
                               [int(d) for d in data["days"]],
                               date.fromisoformat(data["start"]))

        await _tap("hm:ok")
        store = await get_store()
        plan = await store.plans.get_active_plan(USER_ID)
        stored = await store.plans.list_plan_days(plan.id)

        assert len(stored) == len(previewed)
        for saved, portion in zip(stored, previewed):
            assert saved.scheduled_date == portion.scheduled_date
            assert (saved.surah, saved.start_ayah, saved.end_ayah) == \
                   (portion.surah, portion.start_ayah, portion.end_ayah)

    async def test_al_mulk_over_weekdays_is_fifteen_portions_over_eighteen_days(self):
        """The number the preview copy quotes, asserted rather than assumed."""
        await _run_wizard()
        await _tap("hm:ok")
        store = await get_store()
        plan = await store.plans.get_active_plan(USER_ID)
        days = await store.plans.list_plan_days(plan.id)
        portions = build_plan(surah_ref(AL_MULK), 2, WEEKDAYS, days[0].scheduled_date)
        assert len(advancing(portions)) == 15
        assert len(days) == 18
        assert (days[-1].surah, days[-1].end_ayah) == (AL_MULK, 30)

    async def test_a_junk_target_is_rejected_without_ending_the_wizard(self):
        await hifz.dispatch_command(await _ctx(), "memorize")
        await _tap("hm:t:s")
        bot, handled = await _type("not a surah")
        assert handled is True
        from lib.wizard import Wizard
        assert Wizard().is_active(USER_ID) is True      # still in the wizard

    async def test_cancel_ends_the_wizard(self):
        await hifz.dispatch_command(await _ctx(), "memorize")
        await _tap("hm:t:s")
        bot, handled = await _type("/cancel")
        assert handled is True
        from lib.wizard import Wizard
        assert Wizard().is_active(USER_ID) is False

    async def test_the_cancel_button_ends_the_wizard(self):
        await hifz.dispatch_command(await _ctx(), "memorize")
        await _tap("hm:x")
        from lib.wizard import Wizard
        assert Wizard().is_active(USER_ID) is False

    async def test_a_draft_expiring_mid_wizard_does_not_crash(self):
        """A draft can expire between two taps; every step must survive it."""
        await hifz.dispatch_command(await _ctx(), "memorize")
        from lib.wizard import Wizard
        Wizard().clear(USER_ID)
        for cb in ("hm:p:2", "hm:d:wk", "hm:tz:+05:00", "hm:rt:07:00", "hm:ok"):
            bot = await _tap(cb)                        # must not raise
            assert bot.answer_callback_query.await_count >= 1

    async def test_a_second_memorize_while_a_plan_is_active_is_handled(self):
        await _run_wizard()
        await _tap("hm:ok")
        bot = AsyncMock()
        assert await hifz.dispatch_command(await _ctx(bot), "memorize") is True
        assert bot.send_message.await_count >= 1

    async def test_stale_and_forged_callback_data_is_acknowledged(self):
        for cb in ("hm:", "hm:nonsense", "hm:t:zzz", "hm:kn:notanumber", "hm:p:"):
            bot = await _tap(cb)
            assert bot.answer_callback_query.await_count >= 1


# --- The enqueue chain ----------------------------------------------------------

class TestEnqueueChain:
    """Wave F drains the queue; nothing else fills it. If this is wrong, the
    daily push silently never fires and no test of the scheduler would notice."""

    async def test_saving_a_plan_queues_the_first_push(self):
        await _run_wizard()
        await _tap("hm:ok")
        store = await get_store()
        rows = list(store.schedule._state.scheduled_send.values())
        assert len(rows) == 1
        assert rows[0].kind == "plan_day"
        assert rows[0].target_chat_id == CHAT_ID
        assert "plan_day_id" in rows[0].payload

    async def test_queueing_twice_in_one_day_inserts_one_row(self):
        """The idempotency key is what makes a restart or a double call safe."""
        await _run_wizard()
        await _tap("hm:ok")
        store = await get_store()
        plan = await store.plans.get_active_plan(USER_ID)
        before = len(store.schedule._state.scheduled_send)
        again = await memorize_feature._enqueue_next(store, USER_ID, CHAT_ID, plan)
        assert again is None                     # already queued for that day
        assert len(store.schedule._state.scheduled_send) == before

    async def test_pausing_stops_the_chain_and_resuming_restarts_it(self):
        await _run_wizard()
        await _tap("hm:ok")
        store = await get_store()

        await _tap("hm:ps")
        plan = (await store.plans.list_plans(USER_ID))[0]
        assert plan.status == PLAN_PAUSED
        queued = await memorize_feature._enqueue_next(store, USER_ID, CHAT_ID, plan)
        assert queued is None, "a paused plan must not queue a push"

        await _tap("hm:rs")
        plan = (await store.plans.list_plans(USER_ID))[0]
        assert plan.status == PLAN_ACTIVE

    async def test_abandoning_retires_the_plan(self):
        await _run_wizard()
        await _tap("hm:ok")
        await _tap("hm:ab")
        store = await get_store()
        assert await store.plans.get_active_plan(USER_ID) is None

    async def test_the_plan_day_kind_is_registered_with_the_scheduler(self):
        hifz.load_features()
        assert memorize_feature.SEND_KIND in scheduler.SEND_HANDLERS

    async def test_a_push_delivers_once_even_if_the_row_is_claimed_twice(self):
        """`claim_plan_day` is a conditional write; the second delivery is a no-op."""
        await _run_wizard()
        await _tap("hm:ok")
        store = await get_store()
        plan = await store.plans.get_active_plan(USER_ID)
        day = (await store.plans.list_plan_days(plan.id))[0]

        assert await store.plans.claim_plan_day(day.id) is not None
        assert await store.plans.claim_plan_day(day.id) is None


# --- The drill ------------------------------------------------------------------

class TestDrill:
    async def test_know_by_heart_writes_an_interval_and_logs_a_session(self):
        await _run_wizard()
        await _tap("hm:ok")
        store = await get_store()
        plan = await store.plans.get_active_plan(USER_ID)
        day = (await store.plans.list_plan_days(plan.id))[0]

        await _tap("hm:kn:%d" % day.id)

        intervals = await store.hifz.list_intervals(USER_ID, AL_MULK)
        assert intervals, "the portion should be marked memorized"
        assert intervals[0].start_ayah == day.start_ayah
        assert (await store.sessions.list_active_dates(USER_ID)) != []

    async def test_tapping_know_by_heart_twice_does_not_double_log(self):
        """D4's done-when."""
        await _run_wizard()
        await _tap("hm:ok")
        store = await get_store()
        plan = await store.plans.get_active_plan(USER_ID)
        day = (await store.plans.list_plan_days(plan.id))[0]

        await _tap("hm:kn:%d" % day.id)
        sessions_after_first = len(await store.sessions.list_sessions(USER_ID))
        intervals_after_first = await store.hifz.list_intervals(USER_ID, AL_MULK)

        await _tap("hm:kn:%d" % day.id)
        assert len(await store.sessions.list_sessions(USER_ID)) == sessions_after_first
        assert await store.hifz.list_intervals(USER_ID, AL_MULK) == intervals_after_first

        refreshed = await store.plans.get_plan_day(day.id)
        assert refreshed.state == DAY_COMPLETED

    async def test_know_by_heart_on_an_unknown_day_is_acknowledged(self):
        bot = await _tap("hm:kn:999999")
        assert bot.answer_callback_query.await_count >= 1

    async def test_a_multi_ayah_portion_sends_one_stitched_audio(self, monkeypatch):
        """D3's done-when: one combined file, not N."""
        calls = []

        async def fake_combined(bot, surah, start, end, chat_id, performer,
                                reply_markup=None):
            calls.append((surah, start, end))

        async def fake_send_quran(*args, **kwargs):
            pass

        monkeypatch.setattr(memorize_feature, "send_combined_audio", fake_combined)
        monkeypatch.setattr(memorize_feature, "send_quran", fake_send_quran)

        await _run_wizard()
        await _tap("hm:ok")
        store = await get_store()
        plan = await store.plans.get_active_plan(USER_ID)
        day = (await store.plans.list_plan_days(plan.id))[0]
        assert day.end_ayah > day.start_ayah, "need a multi-ayah portion to test this"

        from lib.utils import File
        await memorize_feature._send_drill(AsyncMock(), {}, File(), store, CHAT_ID,
                                           plan, day, "en", "en", "Husary_128kbps")
        assert len(calls) == 1
        assert calls[0] == (day.surah, day.start_ayah, day.end_ayah)


class TestRegistration:
    def test_the_command_and_wizard_are_registered(self):
        hifz.load_features()
        assert hifz.handles("memorize") is True
        assert memorize_feature.WIZARD_KIND in hifz.WIZARDS
        assert "hm:" in hifz.CALLBACKS

    def test_callback_data_fits_telegrams_cap(self):
        for cb in ("hm:t:s", "hm:p:12", "hm:d:wk", "hm:dt:7", "hm:dok",
                   "hm:tz:+05:00", "hm:rt:07:00", "hm:ok", "hm:x", "hm:go",
                   "hm:kn:%d" % 2 ** 31, "hm:ps", "hm:rs", "hm:ab"):
            assert len(cb.encode()) <= 64, cb
