# Workstream E — recall check (spec items E2, E3).
#
# Owns: /check and the four-option continuation quiz that lets someone
# memorizing from a physical mushaf earn a session without ever running a drill.
# Question text comes from `Quran.get_ayah_text` (no "(s:a)" suffix — that would
# leak the answer into the options).
# Callback prefix: "hc:" (see bot.features.PREFIXES).
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

import html
from datetime import datetime
from typing import Optional, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import services.check as check_service
from bot.features import Ctx, callback, command
from domain.quran import Quran
from domain.recall_check import OPTION_COUNT, RecallQuestion
from domain.refs import parse_reference
from services.check import DEFAULT_JUZ  # noqa: F401 — re-exported
from services.streaks import user_today

# --- callback_data shapes ------------------------------------------------------
# hc:start                              start a check from another screen (23 B max: 8)
# hc:a:<surah>:<ayah>:<YYYYMMDD>:<idx>  answer option <idx> (23 bytes at worst)
CB_START = "hc:start"
CB_ANSWER = "hc:a:"
_DATE_FORMAT = "%Y%m%d"


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
    await ctx.answer()  # unknown shape: acknowledge, ignore


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
        ref, hint = await check_service.default_span(ctx.store, ctx.user_id, today)

    question = await check_service.ask(ctx.user_id, ref, today)
    if question is None:  # an empty span; nothing to test
        await ctx.reply(ctx.tr("ref_invalid"))
        return

    text = _question_text(ctx, question)
    if hint:
        text += "\n\n" + ctx.tr("check_usage")
    await ctx.reply(text, parse_mode="HTML", reply_markup=_options_keyboard(question, today))


def _question_text(ctx: Ctx, question: RecallQuestion) -> str:
    """The prompt, HTML-escaped and set off from the localized question line.

    The corpus holds no `<`, `>` or `&` — the escape is belt-and-braces, and it
    is the same belt `main.build_verse_text` wears.
    """
    return "%s\n\n<b>%s</b> …" % (ctx.tr("check_question"), html.escape(question.prompt))


def _options_keyboard(question: RecallQuestion, today) -> InlineKeyboardMarkup:
    """One option per row — an Arabic fragment does not share a row legibly."""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(option, callback_data=_answer_data(question, today, index))]
            for index, option in enumerate(question.options)
        ]
    )


def _answer_data(question: RecallQuestion, today, index: int) -> str:
    """ "hc:a:67:12:20260731:2" — 23 bytes at the very worst (2:282, option 3)."""
    return "%s%d:%d:%s:%d" % (
        CB_ANSWER,
        question.surah,
        question.ayah,
        today.strftime(_DATE_FORMAT),
        index,
    )


# --- scoring -------------------------------------------------------------------


async def _score(ctx: Ctx, cb_data: str) -> None:
    """Regenerate the tapped question, judge the answer, and earn the day."""
    parsed = _parse_answer(cb_data)
    if parsed is None:
        await ctx.answer()
        return
    surah, ayah, day, index = parsed

    question = await check_service.rebuild(ctx.user_id, surah, ayah, day)
    if question is None:  # an ayah that no longer resolves
        await ctx.answer()
        return

    scored = await check_service.score(ctx.user_id, question, index)
    if scored.correct:
        result = ctx.tr("check_correct")
        if not scored.logged:
            result += "\n" + ctx.tr("check_already_today")
        elif scored.milestone_key is not None:
            result += "\n" + ctx.tr(scored.milestone_key)
    else:
        result = ctx.tr("check_wrong", correct=html.escape(scored.correct_option))

    await ctx.answer()
    # Editing without a reply_markup drops the keyboard, so the same question
    # cannot be answered twice from the same message.
    await ctx.edit(_question_text(ctx, question) + "\n\n" + result, parse_mode="HTML")


def _parse_answer(cb_data: str) -> Optional[Tuple[int, int, object, int]]:
    """ "hc:a:67:12:20260731:2" -> (67, 12, date(2026, 7, 31), 2), or None.

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
