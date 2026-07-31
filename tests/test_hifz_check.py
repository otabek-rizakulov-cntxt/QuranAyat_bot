"""The recall check (`src/hifz/check.py`) — spec items E2 and E3.

This is the feature that makes the leaderboard fair to someone memorizing from a
paper mushaf: it measures hifz, not app usage. So the tests that matter most are
the ones about a user who has *nothing* — no plan, no profile, no marked
intervals — being able to answer one question and earn the day.

The other half is the callback. `callback_data` is capped at 64 bytes and Arabic
is not, so the button carries an option *index* plus the four values a question
is deterministic in — (user, surah, ayah, date). Everything below about stale
buttons follows from that: a keyboard from yesterday regenerates yesterday's
question, because Telegram never expires a keyboard and the shuffle differs by
day.
"""

from datetime import timedelta
from unittest.mock import AsyncMock

import pytest
import telegram

import hifz
from hifz import Ctx
from hifz.check import CB_ANSWER, CB_START, _parse_answer
from lib.recall_check import OPTION_COUNT, build_question
from lib.store import get_store
from lib.store.sessions import KIND_RECALL_CHECK
from lib.streaks import streak_summary, user_today
from locales import t

USER = 900_501


class _Settings:
    ui_lang = "en"
    translation_lang = "en"
    reciter = "Husary_128kbps"


@pytest.fixture(autouse=True)
def _isolate_registries():
    """Snapshot and restore the process-wide registries (see tests/test_hifz_seam)."""
    saved = (dict(hifz.COMMANDS), dict(hifz.CALLBACKS), dict(hifz.WIZARDS), hifz._loaded)
    yield
    hifz.COMMANDS.clear()
    hifz.COMMANDS.update(saved[0])
    hifz.CALLBACKS.clear()
    hifz.CALLBACKS.update(saved[1])
    hifz.WIZARDS.clear()
    hifz.WIZARDS.update(saved[2])
    hifz._loaded = saved[3]


def _callback_query(message_id: int = 11):
    message = type("M", (), {"message_id": message_id, "photo": None, "audio": None})()
    return type("CQ", (), {"id": "cq-1", "message": message})()


async def _ctx(bot=None, **kwargs) -> Ctx:
    from lib.utils import File
    return await Ctx.build(bot or AsyncMock(), {}, File(), USER, USER,
                           _Settings(), **kwargs)


async def _ask(argument: str = "", bot=None):
    """Run `/check <argument>` and return (bot, text, keyboard)."""
    bot = bot or AsyncMock()
    ctx = await _ctx(bot=bot, argument=argument)
    assert await hifz.dispatch_command(ctx, "check") is True
    kwargs = bot.send_message.await_args.kwargs
    return bot, kwargs["text"], kwargs.get("reply_markup")


def _buttons(markup):
    return [row[0] for row in markup.inline_keyboard]


def _asked(markup):
    """(surah, ayah, date) the keyboard's buttons all point at."""
    parsed = [_parse_answer(button.callback_data) for button in _buttons(markup)]
    assert all(p is not None for p in parsed), "every button must parse"
    assert len({p[:3] for p in parsed}) == 1, "one question per keyboard"
    return parsed[0][:3]


def _answer_data(surah, ayah, day, index) -> str:
    return "%s%d:%d:%s:%d" % (CB_ANSWER, surah, ayah, day.strftime("%Y%m%d"), index)


async def _tap(cb_data: str, bot=None):
    """Tap an answer button and return (bot, the text the message was edited to)."""
    bot = bot or AsyncMock()
    ctx = await _ctx(bot=bot, callback_query=_callback_query())
    assert await hifz.dispatch_callback(ctx, cb_data) is True
    if bot.edit_message_text.await_args is not None:
        return bot, bot.edit_message_text.await_args.kwargs["text"]
    if bot.send_message.await_args is not None:        # media fallback path
        return bot, bot.send_message.await_args.kwargs["text"]
    return bot, None


async def _sessions():
    store = await get_store()
    return await store.sessions.list_sessions(USER)


# --- E3: the entry point -------------------------------------------------------

class TestCheckEntryPoint:
    async def test_check_67_produces_a_question_from_al_mulk(self):
        _, text, markup = await _ask("67")
        surah, ayah, _ = _asked(markup)
        assert surah == 67
        assert 1 <= ayah <= 30                       # Al-Mulk has 30 ayahs
        assert t("check_question", "en") in text
        assert len(_buttons(markup)) == OPTION_COUNT

    async def test_a_range_and_a_juz_are_understood(self):
        _, _, markup = await _ask("67:1-8")
        surah, ayah, _ = _asked(markup)
        assert (surah, ayah) >= (67, 1) and (surah, ayah) <= (67, 8)

        _, _, markup = await _ask("juz 30")
        surah, _, _ = _asked(markup)
        assert 78 <= surah <= 114

    async def test_a_reference_that_does_not_parse_is_rejected(self):
        _, text, markup = await _ask("not a surah")
        assert text == t("ref_invalid", "en")
        assert markup is None

    async def test_bare_check_works_with_no_argument_and_no_plan(self):
        # The book learner: no plan, no profile, nothing marked. A bare /check
        # must still put a question in front of them.
        _, text, markup = await _ask("")
        surah, ayah, _ = _asked(markup)
        assert 78 <= surah <= 114                    # the juz 30 default
        assert len(_buttons(markup)) == OPTION_COUNT
        # ...and it tells them they can name something else.
        assert t("check_usage", "en") in text

    async def test_bare_check_prefers_the_plan_portion_already_reached(self):
        from lib.store.plans import PlanDaySpec
        store = await get_store()
        today = await user_today(USER)
        await store.plans.create_plan(
            USER, "surah", 67, 1, 67, 30, 5, [1, 2, 3, 4, 5, 6, 7],
            [PlanDaySpec(today - timedelta(days=1), 67, 1, 5),
             PlanDaySpec(today, 67, 6, 10),
             PlanDaySpec(today + timedelta(days=1), 67, 11, 15)])

        _, text, markup = await _ask("")
        surah, ayah, _ = _asked(markup)
        assert surah == 67
        assert 1 <= ayah <= 10, "must not test a portion that has not been pushed"
        assert t("check_usage", "en") not in text     # we did not have to guess

    async def test_bare_check_falls_back_to_something_marked_as_known(self):
        store = await get_store()
        await store.hifz.add_interval(USER, 112, 1, 4)
        _, _, markup = await _ask("")
        surah, ayah, _ = _asked(markup)
        assert surah == 112 and 1 <= ayah <= 4

    async def test_the_start_button_asks_a_question(self):
        bot = AsyncMock()
        ctx = await _ctx(bot=bot, callback_query=_callback_query())
        assert await hifz.dispatch_callback(ctx, CB_START) is True
        bot.answer_callback_query.assert_awaited()
        assert t("check_question", "en") in bot.send_message.await_args.kwargs["text"]


# --- E2: scoring ---------------------------------------------------------------

class TestScoring:
    async def test_a_correct_answer_is_told_so_and_logs_a_session(self):
        _, _, markup = await _ask("67")
        surah, ayah, day = _asked(markup)
        question = build_question(USER, surah, ayah, day)

        _, text = await _tap(_answer_data(surah, ayah, day, question.correct_index))
        assert t("check_correct", "en") in text

        rows = await _sessions()
        assert len(rows) == 1
        assert rows[0].kind == KIND_RECALL_CHECK
        assert rows[0].local_date == day
        # No portion: that is what makes the store dedupe every later pass today.
        assert (rows[0].surah, rows[0].start_ayah, rows[0].end_ayah) == (None, None, None)

    async def test_a_wrong_answer_logs_nothing_and_shows_the_continuation(self):
        _, _, markup = await _ask("67")
        surah, ayah, day = _asked(markup)
        question = build_question(USER, surah, ayah, day)
        wrong = (question.correct_index + 1) % OPTION_COUNT

        _, text = await _tap(_answer_data(surah, ayah, day, wrong))
        assert t("check_correct", "en") not in text
        assert question.correct in text                  # "It continues: ..."
        assert await _sessions() == []

    async def test_a_user_with_no_plan_at_all_earns_the_day(self):
        # The acceptance criterion for E2, and the reason this feature exists.
        store = await get_store()
        assert await store.plans.get_active_plan(USER) is None
        assert await store.profiles.get_profile(USER) is None

        _, _, markup = await _ask("67")
        surah, ayah, day = _asked(markup)
        question = build_question(USER, surah, ayah, day)
        await _tap(_answer_data(surah, ayah, day, question.correct_index))

        summary = await streak_summary(USER)
        assert summary.current == 1
        assert summary.active_today is True

    async def test_only_one_session_is_earned_a_day_however_many_checks_pass(self):
        first, second = [], []
        for argument, sink in (("67", first), ("36", second)):
            _, _, markup = await _ask(argument)
            surah, ayah, day = _asked(markup)
            question = build_question(USER, surah, ayah, day)
            _, text = await _tap(_answer_data(surah, ayah, day, question.correct_index))
            sink.append(text)

        assert t("check_already_today", "en") not in first[0]
        assert t("check_correct", "en") in second[0]
        assert t("check_already_today", "en") in second[0]
        assert len(await _sessions()) == 1
        assert (await streak_summary(USER)).current == 1

    async def test_the_milestone_line_fires_on_the_day_it_is_reached(self):
        store = await get_store()
        today = await user_today(USER)
        for back in range(1, 7):                          # six days already earned
            await store.sessions.log_session(USER, today - timedelta(days=back),
                                             KIND_RECALL_CHECK)

        _, _, markup = await _ask("67")
        surah, ayah, day = _asked(markup)
        question = build_question(USER, surah, ayah, day)
        _, text = await _tap(_answer_data(surah, ayah, day, question.correct_index))

        assert t("streak_milestone_7", "en") in text       # day seven, exactly

    async def test_answering_removes_the_keyboard(self):
        # Editing without a reply_markup drops it, so one message cannot be
        # answered twice.
        _, _, markup = await _ask("67")
        surah, ayah, day = _asked(markup)
        bot, _ = await _tap(_answer_data(surah, ayah, day, 0))
        assert "reply_markup" not in bot.edit_message_text.await_args.kwargs


# --- Stale keyboards -----------------------------------------------------------

class TestStaleButtons:
    """Telegram never expires a keyboard: yesterday's buttons are tappable today."""

    @staticmethod
    def _diverging_ayah(today, yesterday):
        """An ayah of Al-Mulk whose shuffle differs between the two days."""
        for ayah in range(1, 31):
            old = build_question(USER, 67, ayah, yesterday)
            new = build_question(USER, 67, ayah, today)
            if old.correct_index != new.correct_index:
                return ayah, old, new
        raise AssertionError("no ayah shuffles differently between the two days")

    async def test_a_stale_button_is_scored_against_its_own_day(self):
        today = await user_today(USER)
        yesterday = today - timedelta(days=1)
        ayah, old, new = self._diverging_ayah(today, yesterday)

        # Yesterday's correct option, tapped today, is correct — even though it
        # sits at a different index in today's shuffle of the same ayah.
        assert old.correct_index != new.correct_index
        _, text = await _tap(_answer_data(67, ayah, yesterday, old.correct_index))
        assert t("check_correct", "en") in text
        assert len(await _sessions()) == 1

    async def test_a_stale_button_does_not_mis_score_todays_question(self):
        today = await user_today(USER)
        yesterday = today - timedelta(days=1)
        ayah, old, new = self._diverging_ayah(today, yesterday)

        # Today's correct index, on yesterday's keyboard, is the wrong option —
        # and the feedback quotes *yesterday's* correct continuation.
        _, text = await _tap(_answer_data(67, ayah, yesterday, new.correct_index))
        assert t("check_correct", "en") not in text
        assert old.correct in text
        assert await _sessions() == []


# --- Defensive parsing ---------------------------------------------------------

class TestCallbackDataDiscipline:
    async def test_no_option_text_ever_travels_in_the_callback(self):
        _, _, markup = await _ask("2")
        for button in _buttons(markup):
            assert button.callback_data.startswith(CB_ANSWER)
            assert button.text not in button.callback_data

    async def test_every_callback_stays_inside_telegrams_64_byte_cap(self):
        for argument in ("2", "67", "112", "juz 30", ""):
            _, _, markup = await _ask(argument)
            for button in _buttons(markup):
                assert len(button.callback_data.encode()) <= 64, button.callback_data
        # the worst shape the format can produce: three-digit surah, three-digit
        # ayah, a four-digit year and the last option index
        assert len(_answer_data(114, 286, _AnyDay(), 3).encode()) <= 64

    @pytest.mark.parametrize("cb_data", [
        "hc:",                          # bare prefix
        "hc:a:",                        # no payload
        "hc:a:67:1:20260731",           # truncated
        "hc:a:67:1:20260731:0:9",       # over-long
        "hc:a:sixtyseven:1:20260731:0",  # non-numeric surah
        "hc:a:67:1:not-a-date:0",       # unparseable date
        "hc:a:67:1:20261332:0",         # impossible date
        "hc:a:67:99:20260731:0",        # no such ayah
        "hc:a:0:0:20260731:0",          # no such surah
        "hc:a:67:1:20260731:9",         # option index out of range
        "hc:a:67:1:20260731:-1",        # negative index
        "hc:whatever",                  # an unknown shape entirely
    ])
    async def test_garbage_is_acknowledged_and_dropped(self, cb_data):
        # Called directly rather than through dispatch_callback, which would
        # swallow an exception and make a crash look like a clean drop.
        from hifz.check import on_check
        bot = AsyncMock()
        ctx = await _ctx(bot=bot, callback_query=_callback_query())
        await on_check(ctx, cb_data)
        bot.answer_callback_query.assert_awaited()
        bot.edit_message_text.assert_not_awaited()
        assert await _sessions() == []

    def test_the_parser_round_trips_a_well_formed_tap(self):
        from datetime import date
        parsed = _parse_answer("hc:a:67:12:20260731:2")
        assert parsed == (67, 12, date(2026, 7, 31), 2)

    async def test_a_failing_edit_still_answers_the_tap(self):
        # The seam guarantees it, but a spinner left on screen forever is the
        # worst failure this module can have, so it is asserted here too.
        _, _, markup = await _ask("67")
        bot = AsyncMock()
        bot.edit_message_text.side_effect = telegram.error.BadRequest("chat not found")
        ctx = await _ctx(bot=bot, callback_query=_callback_query())
        await hifz.dispatch_callback(ctx, _buttons(markup)[0].callback_data)
        bot.answer_callback_query.assert_awaited()


class _AnyDay:
    """A stand-in for the widest date the format can carry."""

    def strftime(self, fmt):
        return "29991231"
