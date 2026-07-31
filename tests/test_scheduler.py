"""The due-queue scheduler (`src/lib/scheduler.py`) — workstream F.

The acceptance criterion this file exists for is §7's:

    At their local reminder time the next day the bot pushes that day's portion
    unprompted — verified by restarting the app between scheduling and firing,
    with no duplicate send.

So the tests are about *exactly once across a restart*, not about polling. Every
one of them drives `tick()` directly with an injected `now` and an injected
store: nothing here sleeps, and `asyncio.sleep` is never monkeypatched. A restart
is simulated the way it actually behaves — the rows survive, the process does
not — by rebuilding the store around one persistent `MemoryState`.
"""

import asyncio
from datetime import datetime, time, timedelta, timezone
from unittest.mock import AsyncMock

import pytest
import telegram

from lib import scheduler
from lib.scheduler import SendCtx, TickResult
from lib.store import InMemoryStore
from lib.store._state import MemoryState

UTC = timezone.utc


def _at(hour, minute=0, day=1):
    return datetime(2026, 8, day, hour, minute, tzinfo=UTC)


@pytest.fixture(autouse=True)
def _isolate_handlers():
    """Snapshot and restore the process-wide handler registry.

    It is module state, so a test registering a dummy kind would otherwise leak
    into every later test — and into the real boot path.
    """
    saved = dict(scheduler.SEND_HANDLERS)
    yield
    scheduler.SEND_HANDLERS.clear()
    scheduler.SEND_HANDLERS.update(saved)


@pytest.fixture
def state():
    """The rows. Survives a simulated restart; the store around it does not."""
    return MemoryState()


@pytest.fixture
def store(state):
    return InMemoryStore(state)


@pytest.fixture
def bot():
    return AsyncMock()


def _claimed_at(store, when):
    """Restate every claimed row's `claimed_at` on the tests' fabricated timeline.

    The store stamps it from the wall clock (correctly — in production the clock
    and `now` are the same one), so a test injecting a `now` in 2026 has to say
    when the claim happened in that same frame or the comparison is meaningless.
    """
    for row in store.state.scheduled_send.values():
        if row.claimed_at is not None:
            row.claimed_at = when


def _record(kind="drill"):
    """Register a handler for `kind` that records the contexts it was called with."""
    seen = []

    @scheduler.send_handler(kind)
    async def handler(ctx: SendCtx) -> None:
        seen.append(ctx)

    return seen


# --- F2: idempotent enqueue ----------------------------------------------------

class TestIdempotentEnqueue:
    async def test_the_same_key_twice_inserts_one_row_and_raises_nothing(self, store):
        first = await scheduler.enqueue(store, "drill", 501, _at(7), local_day="2026-08-01")
        second = await scheduler.enqueue(store, "drill", 501, _at(7), local_day="2026-08-01")

        assert first is not None
        assert second is None                       # not an exception — a None
        assert len(store.state.scheduled_send) == 1

    async def test_the_key_is_kind_target_local_date(self, store):
        row = await scheduler.enqueue(store, "plan_day", 42, _at(7),
                                      local_day=_at(7).date())
        assert row.idempotency_key == "plan_day:42:2026-08-01"

    async def test_different_days_are_different_rows(self, store):
        await scheduler.enqueue(store, "drill", 501, _at(7, day=1), local_day="2026-08-01")
        await scheduler.enqueue(store, "drill", 501, _at(7, day=2), local_day="2026-08-02")
        assert len(store.state.scheduled_send) == 2

    async def test_different_recipients_are_different_rows(self, store):
        await scheduler.enqueue(store, "drill", 501, _at(7), local_day="2026-08-01")
        await scheduler.enqueue(store, "drill", 502, _at(7), local_day="2026-08-01")
        assert len(store.state.scheduled_send) == 2

    async def test_enqueue_without_a_day_or_key_is_a_programming_error(self, store):
        with pytest.raises(ValueError):
            await scheduler.enqueue(store, "drill", 501, _at(7))

    async def test_schedule_daily_uses_the_recipients_local_clock(self, store):
        # 07:00 local at UTC+05:00 is 02:00 UTC.
        row = await scheduler.schedule_daily(store, "plan_day", 501, time(7, 0),
                                             "+05:00", now=_at(0))
        assert row.due_at == _at(2)
        assert row.idempotency_key == "plan_day:501:2026-08-01"
        assert row.payload["offset"] == "+05:00"    # so staleness knows the local day

    async def test_schedule_daily_twice_in_one_local_day_queues_once(self, store):
        first = await scheduler.schedule_daily(store, "plan_day", 501, time(7, 0),
                                               "+05:00", now=_at(0))
        again = await scheduler.schedule_daily(store, "plan_day", 501, time(7, 0),
                                               "+05:00", now=_at(1))
        assert first is not None and again is None
        assert len(store.state.scheduled_send) == 1

    async def test_schedule_daily_after_firing_queues_tomorrow(self, store):
        await scheduler.schedule_daily(store, "plan_day", 501, time(7, 0), "+05:00",
                                       now=_at(0))
        # Re-scheduling from the moment it fired must advance a day, never re-fire
        # the same instant (next_due_utc is strictly-after for this reason).
        tomorrow = await scheduler.schedule_daily(store, "plan_day", 501, time(7, 0),
                                                  "+05:00", now=_at(2))
        assert tomorrow is not None
        assert tomorrow.due_at == _at(2, day=2)
        assert tomorrow.idempotency_key == "plan_day:501:2026-08-02"


# --- F1: the loop --------------------------------------------------------------

class TestTick:
    async def test_a_due_row_is_delivered_and_marked_sent(self, store, bot):
        seen = _record()
        row = await scheduler.enqueue(store, "drill", 501, _at(7), local_day="2026-08-01",
                                      payload={"surah": 67})

        result = await scheduler.tick(bot, {}, now=_at(7), store=store)

        assert (result.claimed, result.sent, result.failed) == (1, 1, 0)
        assert len(seen) == 1
        assert seen[0].chat_id == 501 and seen[0].payload["surah"] == 67
        assert (await store.schedule.get(row.id)).state == "sent"

    async def test_a_row_due_in_the_future_is_not_claimed_early(self, store, bot):
        seen = _record()
        row = await scheduler.enqueue(store, "drill", 501, _at(7), local_day="2026-08-01")

        result = await scheduler.tick(bot, {}, now=_at(6, 59), store=store)

        assert result == TickResult()               # nothing happened at all
        assert seen == []
        assert (await store.schedule.get(row.id)).state == "pending"

    async def test_a_claimed_row_is_never_claimed_twice(self, store, bot):
        seen = _record()
        await scheduler.enqueue(store, "drill", 501, _at(7), local_day="2026-08-01")

        first = await scheduler.tick(bot, {}, now=_at(7), store=store)
        second = await scheduler.tick(bot, {}, now=_at(7, 1), store=store)

        assert first.sent == 1
        assert second.claimed == 0
        assert len(seen) == 1

    async def test_the_context_carries_the_row_and_the_store(self, store, bot):
        seen = _record()
        await scheduler.enqueue(store, "drill", 501, _at(7), local_day="2026-08-01",
                                thread_id=77)

        await scheduler.tick(bot, {"index": "x"}, now=_at(7), store=store)

        ctx = seen[0]
        assert ctx.kind == "drill" and ctx.thread_id == 77
        assert ctx.store is store
        assert ctx.data == {"index": "x"}
        assert ctx.bot is bot

    async def test_claiming_is_bounded_and_oldest_first(self, store, bot):
        seen = _record()
        await scheduler.enqueue(store, "drill", 502, _at(8), local_day="b")
        await scheduler.enqueue(store, "drill", 501, _at(7), local_day="a")

        result = await scheduler.tick(bot, {}, now=_at(9), store=store, limit=1)

        assert result.claimed == 1
        assert seen[0].chat_id == 501               # the older due row went first


class TestTheLoopSurvivesABadRow:
    async def test_an_exception_in_one_send_does_not_block_the_next_row(self, store, bot):
        delivered = []

        @scheduler.send_handler("poison")
        async def poisoned(ctx):
            raise KeyError("plan_day_id")

        @scheduler.send_handler("drill")
        async def good(ctx):
            delivered.append(ctx.chat_id)

        bad = await scheduler.enqueue(store, "poison", 501, _at(7), local_day="a")
        ok = await scheduler.enqueue(store, "drill", 502, _at(7, 30), local_day="b")

        result = await scheduler.tick(bot, {}, now=_at(8), store=store)

        assert (result.claimed, result.sent, result.failed) == (2, 1, 1)
        assert delivered == [502]                   # the queue kept moving
        assert (await store.schedule.get(bad.id)).state == "failed"
        assert (await store.schedule.get(ok.id)).state == "sent"
        assert isinstance(result.errors[0][1], KeyError)

    async def test_a_failed_row_is_terminal_and_never_retried(self, store, bot):
        calls = []

        @scheduler.send_handler("poison")
        async def poisoned(ctx):
            calls.append(ctx)
            raise RuntimeError("boom")

        await scheduler.enqueue(store, "poison", 501, _at(7), local_day="a")

        await scheduler.tick(bot, {}, now=_at(7), store=store)
        await scheduler.tick(bot, {}, now=_at(7, 1), store=store)

        assert len(calls) == 1                      # 'failed' is not claimable

    async def test_a_blocked_user_is_terminal_not_retried_forever(self, store, bot):
        calls = []

        @scheduler.send_handler("drill")
        async def blocked(ctx):
            calls.append(ctx)
            raise telegram.error.Forbidden("bot was blocked by the user")

        row = await scheduler.enqueue(store, "drill", 501, _at(7), local_day="a")

        result = await scheduler.tick(bot, {}, now=_at(7), store=store)

        assert result.failed == 1
        assert (await store.schedule.get(row.id)).state == "failed"
        await scheduler.tick(bot, {}, now=_at(7, 1), store=store)
        assert len(calls) == 1

    async def test_an_unregistered_kind_fails_its_row_without_stopping_the_batch(
            self, store, bot):
        delivered = _record("drill")
        orphan = await scheduler.enqueue(store, "not_a_kind", 501, _at(7), local_day="a")
        await scheduler.enqueue(store, "drill", 502, _at(7, 30), local_day="b")

        result = await scheduler.tick(bot, {}, now=_at(8), store=store)

        assert (result.sent, result.failed) == (1, 1)
        assert (await store.schedule.get(orphan.id)).state == "failed"
        assert len(delivered) == 1

    async def test_a_traceback_is_printed_when_a_send_fails(self, store, bot, capsys):
        @scheduler.send_handler("poison")
        async def poisoned(ctx):
            raise ValueError("bad payload")

        await scheduler.enqueue(store, "poison", 501, _at(7), local_day="a")
        await scheduler.tick(bot, {}, now=_at(7), store=store)

        captured = capsys.readouterr()
        combined = captured.out + captured.err
        assert "ValueError: bad payload" in combined
        assert "Traceback" in combined              # not just the type and message
        assert "test_scheduler.py" in combined      # with the frame that raised


# --- F3: catch-up and staleness ------------------------------------------------

class TestCatchUp:
    async def test_a_window_missed_during_a_restart_still_fires(self, store, bot):
        seen = _record()
        await scheduler.enqueue(store, "drill", 501, _at(7), local_day="2026-08-01")

        # The instance was down at 07:00 and came back at 07:20.
        result = await scheduler.catch_up(bot, {}, now=_at(7, 20), store=store)

        assert result.sent == 1
        assert len(seen) == 1

    async def test_a_window_missed_overnight_is_dropped_not_delivered_at_3am(
            self, store, bot):
        seen = _record()
        row = await scheduler.enqueue(store, "drill", 501, _at(7), local_day="2026-08-01")

        result = await scheduler.catch_up(bot, {}, now=_at(2, 0, day=2), store=store)

        assert seen == []                           # nobody is woken at 03:00
        assert result.dropped == 1 and result.sent == 0
        assert await store.schedule.get(row.id) is None     # pruned, not left to rot

    async def test_a_row_past_the_recipients_local_midnight_is_not_delivered(
            self, store, bot):
        seen = _record()
        # 23:30 local at UTC+05:00 is 18:30 UTC.
        row = await scheduler.enqueue(store, "drill", 501, _at(18, 30),
                                      local_day="2026-08-01",
                                      payload={"offset": "+05:00"})

        # 40 minutes late — inside the 6 h window, but it is now 00:10 tomorrow
        # for the recipient, and yesterday's portion is not today's.
        result = await scheduler.tick(bot, {}, now=_at(19, 10), store=store)

        assert seen == []
        assert result.dropped == 1
        assert (await store.schedule.get(row.id)).state == "failed"

    async def test_a_row_still_inside_the_local_day_is_delivered(self, store, bot):
        seen = _record()
        await scheduler.enqueue(store, "drill", 501, _at(18, 30), local_day="2026-08-01",
                                payload={"offset": "+05:00"})

        result = await scheduler.tick(bot, {}, now=_at(18, 50), store=store)

        assert result.sent == 1 and len(seen) == 1

    async def test_boot_releases_a_claim_stranded_by_a_crash(self, store, bot):
        seen = _record()
        row = await scheduler.enqueue(store, "drill", 501, _at(7), local_day="a")
        # The predecessor claimed it and died before sending.
        await store.schedule.claim_due(_at(7))
        assert (await store.schedule.get(row.id)).state == "claimed"

        result = await scheduler.catch_up(bot, {}, now=_at(7, 1), store=store)

        assert result.released == 1
        assert result.sent == 1 and len(seen) == 1

    async def test_a_fresh_claim_is_not_released_out_from_under_a_live_send(
            self, store, bot):
        """A slow send must not be released and re-claimed by the next tick —
        that would be the one way this design double-sends while running."""
        seen = _record()
        await scheduler.enqueue(store, "drill", 501, _at(7), local_day="a")
        await store.schedule.claim_due(_at(7))
        # The store stamps claimed_at from the wall clock; these tests inject a
        # `now`, so restate the stamp on the same (fabricated) timeline.
        _claimed_at(store, _at(7))                  # in flight, one minute ago

        # A routine tick (not a boot) only releases claims older than CLAIM_TIMEOUT.
        result = await scheduler.tick(bot, {}, now=_at(7, 1), store=store)

        assert result.released == 0 and seen == []

    async def test_a_claim_older_than_the_timeout_is_released_by_a_routine_tick(
            self, store, bot):
        seen = _record()
        await scheduler.enqueue(store, "drill", 501, _at(7), local_day="a")
        await store.schedule.claim_due(_at(7))
        _claimed_at(store, _at(7, 30) - scheduler.CLAIM_TIMEOUT - timedelta(minutes=1))

        result = await scheduler.tick(bot, {}, now=_at(7, 30), store=store)

        assert result.released == 1
        assert result.sent == 1 and len(seen) == 1


class TestRestartDeliversExactlyOnce:
    """§7's acceptance criterion, spelled out.

    A restart is: the rows survive (one `MemoryState`), the process does not (a
    new `InMemoryStore`, a new handler registration, a fresh boot pass).
    """

    async def test_enqueue_restart_then_fire_delivers_exactly_once(self, state, bot):
        # --- boot 1: the wizard schedules tomorrow's portion, then the app dies.
        store = InMemoryStore(state)
        row = await scheduler.schedule_daily(store, "plan_day", 501, time(7, 0),
                                             "+05:00", now=_at(20, day=1),
                                             payload={"plan_day_id": 9})
        assert row.due_at == _at(2, day=2)          # 07:00 local next day

        # --- boot 2: a brand new process, same rows.
        delivered = []
        store = InMemoryStore(state)

        @scheduler.send_handler("plan_day")
        async def push(ctx):
            delivered.append(ctx.payload["plan_day_id"])

        booted = await scheduler.catch_up(bot, {}, now=_at(1, 55, day=2), store=store)
        assert booted.claimed == 0                  # not yet due; nothing fires early

        fired = await scheduler.tick(bot, {}, now=_at(2, day=2), store=store)
        assert (fired.sent, delivered) == (1, [9])

        # --- boot 3: it restarts again, right after firing.
        store = InMemoryStore(state)
        after = await scheduler.catch_up(bot, {}, now=_at(2, 1, day=2), store=store)

        assert after.claimed == 0
        assert delivered == [9]                     # exactly once, across two restarts

    async def test_rescheduling_after_a_restart_cannot_double_queue(self, state, bot):
        """A double boot re-runs whatever schedules the day's push. F2 is what
        makes that a no-op rather than two reminders."""
        store = InMemoryStore(state)
        first = await scheduler.schedule_daily(store, "plan_day", 501, time(7, 0),
                                               "+05:00", now=_at(20, day=1))

        store = InMemoryStore(state)                # restart, same rows
        second = await scheduler.schedule_daily(store, "plan_day", 501, time(7, 0),
                                                 "+05:00", now=_at(21, day=1))

        assert first is not None and second is None
        assert len(state.scheduled_send) == 1

    async def test_a_crash_between_send_and_mark_sent_is_the_known_window(
            self, state, bot):
        """Honest test of the one duplicate this design allows.

        The process dies after Telegram accepted the message but before
        `mark_sent` committed. The row is still 'claimed', so boot recovery
        re-queues it and it is delivered twice — which is why handlers are asked
        to be idempotent (`claim_plan_day` is a conditional write for exactly
        this reason). The test asserts the *bound*: it can only ever re-send
        today's row, never a backlog.
        """
        store = InMemoryStore(state)
        await scheduler.enqueue(store, "plan_day", 501, _at(7), local_day="a",
                                payload={"plan_day_id": 9})
        await store.schedule.claim_due(_at(7))      # claimed... sent... then crash

        deliveries = []
        store = InMemoryStore(state)

        @scheduler.send_handler("plan_day")
        async def push(ctx):
            # A real handler guards itself; this one records every attempt so the
            # window is visible rather than hidden.
            deliveries.append(ctx.payload["plan_day_id"])

        await scheduler.catch_up(bot, {}, now=_at(7, 1), store=store)
        assert deliveries == [9]                    # re-sent: the documented window

        # ... but the same crash a day later delivers nothing at all.
        store = InMemoryStore(state)
        await scheduler.enqueue(store, "plan_day", 502, _at(7), local_day="b",
                                payload={"plan_day_id": 10})
        await store.schedule.claim_due(_at(7))
        store = InMemoryStore(state)
        result = await scheduler.catch_up(bot, {}, now=_at(9, day=2), store=store)

        assert deliveries == [9]
        assert result.dropped == 1


# --- run_scheduler -------------------------------------------------------------

class TestRunScheduler:
    async def test_it_ticks_and_stops_on_max_ticks(self, store, bot):
        seen = _record()
        await scheduler.enqueue(store, "drill", 501, _at(7) - timedelta(days=400),
                                local_day="a")
        await scheduler.enqueue(store, "drill", 502, datetime.now(UTC), local_day="b")

        await scheduler.run_scheduler(bot, {}, interval=0, store=store, max_ticks=1)

        assert [c.chat_id for c in seen] == [502]   # the 400-day-old row was dropped

    async def test_a_tick_that_raises_does_not_kill_the_loop(self, store, bot):
        calls = {"n": 0}
        real_claim = store.schedule.claim_due

        async def flaky(now, limit=20):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RuntimeError("database went away")
            return await real_claim(now, limit=limit)

        store.schedule.claim_due = flaky
        seen = _record()
        await scheduler.enqueue(store, "drill", 501, datetime.now(UTC), local_day="a")

        await scheduler.run_scheduler(bot, {}, interval=0, store=store, max_ticks=2)

        assert calls["n"] == 2                      # it came back for a second pass
        assert len(seen) == 1

    async def test_a_stop_event_ends_the_loop_without_waiting_out_the_interval(
            self, store, bot):
        stop = asyncio.Event()
        stop.set()

        # interval is a minute; if the event were not honoured this would hang.
        await scheduler.run_scheduler(bot, {}, interval=60, store=store,
                                      stop_event=stop, max_ticks=None)

    async def test_cancellation_propagates(self, store, bot):
        task = asyncio.create_task(
            scheduler.run_scheduler(bot, {}, interval=60, store=store))
        await asyncio.sleep(0)                      # let it reach the first wait
        await asyncio.sleep(0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task


# --- The registry and the built-in kind ----------------------------------------

class TestRegistry:
    def test_registering_a_kind_twice_raises_at_import_time(self):
        @scheduler.send_handler("dup")
        async def first(ctx):
            pass

        with pytest.raises(ValueError):
            @scheduler.send_handler("dup")
            async def second(ctx):
                pass

    def test_re_registering_the_same_function_is_harmless(self):
        async def handler(ctx):
            pass

        scheduler.register_send_handler("same", handler)
        scheduler.register_send_handler("same", handler)
        assert scheduler.SEND_HANDLERS["same"] is handler

    def test_registered_kinds_names_the_defining_module(self):
        assert scheduler.registered_kinds()["message"] == "lib.scheduler"

    async def test_the_builtin_message_kind_delivers_text(self, store, bot):
        await scheduler.enqueue(store, "message", 501, _at(7), local_day="a",
                                payload={"text": "Assalamu alaykum"})

        result = await scheduler.tick(bot, {}, now=_at(7), store=store)

        assert result.sent == 1
        bot.send_message.assert_awaited_once_with(chat_id=501, text="Assalamu alaykum",
                                                  parse_mode="HTML")

    async def test_the_builtin_message_kind_posts_into_a_thread_when_bound(
            self, store, bot):
        await scheduler.enqueue(store, "message", -100123, _at(7), local_day="a",
                                payload={"text": "hi", "parse_mode": None},
                                thread_id=17)

        await scheduler.tick(bot, {}, now=_at(7), store=store)

        bot.send_message.assert_awaited_once_with(chat_id=-100123, text="hi",
                                                  message_thread_id=17)

    async def test_a_message_with_no_text_fails_its_row(self, store, bot):
        row = await scheduler.enqueue(store, "message", 501, _at(7), local_day="a",
                                      payload={})

        result = await scheduler.tick(bot, {}, now=_at(7), store=store)

        assert result.failed == 1
        assert (await store.schedule.get(row.id)).state == "failed"
        bot.send_message.assert_not_awaited()


class TestTransientFailuresAreRetried:
    """A thirty-second network blip at the reminder instant must not cost the user
    their day's push — and, with no attempts column, must not retry forever either."""

    async def test_a_timeout_puts_the_row_back_on_the_queue(self, store, bot):
        attempts = []

        @scheduler.send_handler("drill")
        async def flaky(ctx):
            attempts.append(ctx.chat_id)
            if len(attempts) == 1:
                raise telegram.error.TimedOut()

        row = await scheduler.enqueue(store, "drill", 501, _at(7), local_day="a")

        first = await scheduler.tick(bot, {}, now=_at(7), store=store)
        assert (first.sent, first.failed, first.deferred) == (0, 0, 1)
        assert (await store.schedule.get(row.id)).state == "pending"

        second = await scheduler.tick(bot, {}, now=_at(7, 1), store=store)
        assert (second.sent, second.deferred) == (1, 0)
        assert (await store.schedule.get(row.id)).state == "sent"
        assert len(attempts) == 2          # delivered on the retry, exactly once

    async def test_rate_limiting_is_transient_too(self, store, bot):
        @scheduler.send_handler("drill")
        async def limited(ctx):
            raise telegram.error.RetryAfter(30)

        row = await scheduler.enqueue(store, "drill", 501, _at(7), local_day="a")
        result = await scheduler.tick(bot, {}, now=_at(7), store=store)
        assert result.deferred == 1
        assert (await store.schedule.get(row.id)).state == "pending"

    async def test_a_released_row_clears_its_claim(self, store, bot):
        """Otherwise release_stale_claims would release an already-pending row."""
        @scheduler.send_handler("drill")
        async def flaky(ctx):
            raise telegram.error.NetworkError("connection reset")

        row = await scheduler.enqueue(store, "drill", 501, _at(7), local_day="a")
        await scheduler.tick(bot, {}, now=_at(7), store=store)
        stored = await store.schedule.get(row.id)
        assert stored.state == "pending"
        assert stored.claimed_at is None

    async def test_a_bad_request_is_permanent_despite_subclassing_network_error(
            self, store, bot):
        """The trap this ordering exists to avoid.

        `telegram.error.BadRequest` subclasses `NetworkError` in PTB, so the
        obvious `except NetworkError: retry` would retry a malformed request every
        60 s until drop_stale buried it — burning six hours of ticks on a request
        that can never succeed.
        """
        assert issubclass(telegram.error.BadRequest, telegram.error.NetworkError)

        calls = []

        @scheduler.send_handler("drill")
        async def rejected(ctx):
            calls.append(ctx)
            raise telegram.error.BadRequest("chat not found")

        row = await scheduler.enqueue(store, "drill", 501, _at(7), local_day="a")
        result = await scheduler.tick(bot, {}, now=_at(7), store=store)

        assert (result.failed, result.deferred) == (1, 0)
        assert (await store.schedule.get(row.id)).state == "failed"

        await scheduler.tick(bot, {}, now=_at(7, 1), store=store)
        assert len(calls) == 1              # terminal: never attempted again

    async def test_a_blocked_user_is_still_terminal(self, store, bot):
        @scheduler.send_handler("drill")
        async def blocked(ctx):
            raise telegram.error.Forbidden("bot was blocked by the user")

        row = await scheduler.enqueue(store, "drill", 501, _at(7), local_day="a")
        result = await scheduler.tick(bot, {}, now=_at(7), store=store)
        assert (result.failed, result.deferred) == (1, 0)
        assert (await store.schedule.get(row.id)).state == "failed"

    async def test_retrying_is_bounded_by_the_stale_drop_not_by_luck(self, store, bot):
        """With no attempts column, time is what stops the loop.

        The row is released each tick, so what must be true is that it eventually
        stops being retried rather than churning forever.
        """
        @scheduler.send_handler("drill")
        async def never_works(ctx):
            raise telegram.error.TimedOut()

        row = await scheduler.enqueue(store, "drill", 501, _at(7), local_day="a")
        for minute in range(1, 4):
            await scheduler.tick(bot, {}, now=_at(7, minute), store=store)
        assert (await store.schedule.get(row.id)).state == "pending"

        # once it is no longer same-day-relevant, it is dropped unsent
        late = _at(7) + scheduler.CATCH_UP_WINDOW + timedelta(minutes=1)
        await scheduler.tick(bot, {}, now=late, store=store)
        stored = await store.schedule.get(row.id)
        assert stored is None or stored.state == "failed"
