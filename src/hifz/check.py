# Workstream E — recall check (spec items E2, E3).
#
# Owns: /check and the four-option continuation quiz that lets someone
# memorizing from a physical mushaf earn a session without ever running a drill.
# Question text comes from `Quran.get_ayah_text` (no "(s:a)" suffix — that would
# leak the answer into the options).
# Callback prefix: "hc:" (see hifz.PREFIXES).
#
# Two design points carry this module:
#
#   * **The callback carries an index, never text.** `callback_data` is capped at
#     64 bytes and one vocalized Arabic word can eat 30 of them. So the button
#     carries `(surah, ayah, date, option index)` — and since a question is
#     deterministic in exactly (user, surah, ayah, date), those four values
#     regenerate it byte for byte when the tap comes back. Nothing about the
#     question is stored server-side.
#   * **A stale button scores against its own day.** Telegram never expires a
#     keyboard, so yesterday's four options can be tapped tomorrow. The date
#     travels in the callback, so the question that gets regenerated is the one
#     the user is actually looking at. Scoring today's (differently shuffled)
#     question against yesterday's button is the bug this prevents.
#
# The one-earned-session-a-day rule (E2) is not a counter: a recall-check session
# is logged with *no portion*, so (user, local_date, 'recall_check', ø, ø, ø) is
# the same row every time and `log_session` returns None for the second one. The
# store's idempotence is the guard.

import asyncio
import html
from datetime import datetime
from typing import Optional, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from hifz import Ctx, callback, command
from hifz.refs import KIND_RANGE, Ref, juz_ref, parse_reference
from lib.recall_check import (OPTION_COUNT, RecallQuestion, build_question,
                              pick_ayah, preload_corpus)
from lib.store.sessions import KIND_RECALL_CHECK
from lib.streaks import record_session, user_today
from modules import Quran

# --- callback_data shapes ------------------------------------------------------
# hc:start                              start a check from another screen (23 B max: 8)
# hc:a:<surah>:<ayah>:<YYYYMMDD>:<idx>  answer option <idx> (23 bytes at worst)
CB_START = "hc:start"
CB_ANSWER = "hc:a:"
_DATE_FORMAT = "%Y%m%d"

# What a bare /check tests when the user has no plan and nothing marked. Juz 30
# is where essentially every memorizer starts, so it is the least surprising
# question to put in front of a brand new user — and `check_usage` is appended so
# they learn they can name something else.
DEFAULT_JUZ = 30


@command("check")
async def check(ctx: Ctx) -> None:
    """`/check`, `/check 67`, `/check 67:1-8`, `/check juz 30`.

    E3: a book learner tests themselves on whatever they like, on demand. The
    argument is optional by design — the user this feature exists for may never
    have opened a plan, and "you must name a surah" is a wall in front of the one
    person the leaderboard is meant to be fair to.
    """
    await _ask(ctx, ctx.argument)


@callback("hc:")
async def on_check(ctx: Ctx, cb_data: str) -> None:
    """Every "hc:" tap: an answer, or a request for a fresh question.

    Parsed defensively — this data comes off the wire, may be years old, and may
    be neither of those two shapes.
    """
    if cb_data == CB_START:
        await ctx.answer()
        await _ask(ctx, "")
        return
    if cb_data.startswith(CB_ANSWER):
        await _score(ctx, cb_data)
        return
    await ctx.answer()                      # unknown shape: acknowledge, ignore


# --- asking --------------------------------------------------------------------

async def _ask(ctx: Ctx, argument: str) -> None:
    """Pick an ayah, build the question and send it with its four options."""
    today = await user_today(ctx.user_id)

    hint = False
    if (argument or "").strip():
        ref = parse_reference(argument)
        if ref is None:
            await ctx.reply(ctx.tr("ref_invalid"))
            return
    else:
        ref, hint = await _default_span(ctx, today)

    picked = pick_ayah(ctx.user_id, ref, today)
    if picked is None:                      # an empty span; nothing to test
        await ctx.reply(ctx.tr("ref_invalid"))
        return

    await preload_corpus()                  # 1.3 MB parse, once, off the loop
    question = await asyncio.to_thread(build_question, ctx.user_id, picked[0],
                                       picked[1], today)

    text = _question_text(ctx, question)
    if hint:
        text += "\n\n" + ctx.tr("check_usage")
    await ctx.reply(text, parse_mode="HTML", reply_markup=_options_keyboard(question, today))


async def _default_span(ctx: Ctx, today) -> Tuple[Ref, bool]:
    """What a bare `/check` tests, and whether we had to guess.

    In order of how well it reflects what the user is actually memorizing:
    the part of their plan they have reached, then something they have marked as
    known, then the default. Never the whole Qur'an — a random ayah out of 6236
    is not a recall check, it is a trick question.
    """
    plan = await ctx.store.plans.get_active_plan(ctx.user_id)
    if plan is not None:
        # Only as far as they have been pushed: testing next month's portion
        # would be a test of what they have not been taught yet.
        days = await ctx.store.plans.list_plan_days(plan.id, on_or_before=today)
        if days:
            reached = days[-1]
            return Ref(KIND_RANGE, plan.start_surah, plan.start_ayah,
                       reached.surah, reached.end_ayah), False

    intervals = await ctx.store.hifz.list_intervals(ctx.user_id)
    if intervals:
        # Cycles through what they know, one interval a day: deterministic, so
        # asking twice in a day is not a way to shop for an easier question.
        chosen = intervals[today.toordinal() % len(intervals)]
        return Ref(KIND_RANGE, chosen.surah, chosen.start_ayah,
                   chosen.surah, chosen.end_ayah), False

    return juz_ref(DEFAULT_JUZ), True


def _question_text(ctx: Ctx, question: RecallQuestion) -> str:
    """The prompt, HTML-escaped and set off from the localized question line.

    The corpus holds no `<`, `>` or `&` — the escape is belt-and-braces, and it
    is the same belt `main.build_verse_text` wears.
    """
    return "%s\n\n<b>%s</b> …" % (ctx.tr("check_question"), html.escape(question.prompt))


def _options_keyboard(question: RecallQuestion, today) -> InlineKeyboardMarkup:
    """One option per row — an Arabic fragment does not share a row legibly."""
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(option, callback_data=_answer_data(question, today, index))]
         for index, option in enumerate(question.options)])


def _answer_data(question: RecallQuestion, today, index: int) -> str:
    """"hc:a:67:12:20260731:2" — 23 bytes at the very worst (2:282, option 3)."""
    return "%s%d:%d:%s:%d" % (CB_ANSWER, question.surah, question.ayah,
                              today.strftime(_DATE_FORMAT), index)


# --- scoring -------------------------------------------------------------------

async def _score(ctx: Ctx, cb_data: str) -> None:
    """Regenerate the tapped question, judge the answer, and earn the day."""
    parsed = _parse_answer(cb_data)
    if parsed is None:
        await ctx.answer()
        return
    surah, ayah, day, index = parsed

    await preload_corpus()
    try:
        question = await asyncio.to_thread(build_question, ctx.user_id, surah, ayah, day)
    except ValueError:                      # an ayah that no longer resolves
        await ctx.answer()
        return

    if question.is_correct(index):
        # E2: a pass logs a recall_check session with no portion, so the store
        # dedupes every later pass today onto the same row.
        outcome = await record_session(ctx.user_id, KIND_RECALL_CHECK)
        result = ctx.tr("check_correct")
        if not outcome.logged:
            result += "\n" + ctx.tr("check_already_today")
        elif outcome.milestone.reached is not None:
            result += "\n" + ctx.tr(outcome.milestone.key)
    else:
        result = ctx.tr("check_wrong", correct=html.escape(question.correct))

    await ctx.answer()
    # Editing without a reply_markup drops the keyboard, so the same question
    # cannot be answered twice from the same message.
    await ctx.edit(_question_text(ctx, question) + "\n\n" + result, parse_mode="HTML")


def _parse_answer(cb_data: str) -> Optional[Tuple[int, int, object, int]]:
    """"hc:a:67:12:20260731:2" -> (67, 12, date(2026, 7, 31), 2), or None.

    Everything is checked: the shape, every integer, the date, the option index
    and whether the ayah exists. A tap that fails any of them is acknowledged and
    dropped rather than raising — a keyboard from an older release of this bot is
    a normal thing to receive, not an error.
    """
    parts = cb_data.split(":")
    if len(parts) != 6:
        return None
    try:
        surah, ayah, index = int(parts[2]), int(parts[3]), int(parts[5])
        day = datetime.strptime(parts[4], _DATE_FORMAT).date()
    except (ValueError, TypeError):
        return None
    if not 0 <= index < OPTION_COUNT:
        return None
    if not Quran.exists(surah, ayah):
        return None
    return surah, ayah, day, index
