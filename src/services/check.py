# Recall-check operations (spec items E1-E3). Used by /check (hifz/check.py) and
# the Mini App's /check routes.
#
# A question is deterministic per (user, ayah, local date) — "a retry is not a
# reroll" — so scoring rebuilds it from those three values instead of trusting
# anything the client sends back about the options.

import asyncio
from dataclasses import dataclass
from datetime import date
from typing import Optional, Tuple

from hifz.refs import KIND_RANGE, Ref, juz_ref
from lib.recall_check import RecallQuestion, build_question, pick_ayah, preload_corpus
from lib.store.sessions import KIND_RECALL_CHECK
from lib.streaks import record_session

# What a bare /check tests when the user has no plan and nothing marked. Juz 30
# is where essentially every memorizer starts, so it is the least surprising
# question to put in front of a brand new user.
DEFAULT_JUZ = 30


async def default_span(store, user_id: int, today: date) -> Tuple[Ref, bool]:
    """What a check with no reference tests, and whether we had to guess.

    In order of how well it reflects what the user is actually memorizing:
    the part of their plan they have reached, then something they have marked as
    known, then the default. Never the whole Qur'an — a random ayah out of 6236
    is not a recall check, it is a trick question.
    """
    plan = await store.plans.get_active_plan(user_id)
    if plan is not None:
        # Only as far as they have been pushed: testing next month's portion
        # would be a test of what they have not been taught yet.
        days = await store.plans.list_plan_days(plan.id, on_or_before=today)
        if days:
            reached = days[-1]
            return Ref(
                KIND_RANGE, plan.start_surah, plan.start_ayah, reached.surah, reached.end_ayah
            ), False

    intervals = await store.hifz.list_intervals(user_id)
    if intervals:
        # Cycles through what they know, one interval a day: deterministic, so
        # asking twice in a day is not a way to shop for an easier question.
        chosen = intervals[today.toordinal() % len(intervals)]
        return Ref(
            KIND_RANGE, chosen.surah, chosen.start_ayah, chosen.surah, chosen.end_ayah
        ), False

    return juz_ref(DEFAULT_JUZ), True


async def ask(user_id: int, ref: Ref, today: date) -> Optional[RecallQuestion]:
    """The question for `ref` today, or None for an empty span."""
    picked = pick_ayah(user_id, ref, today)
    if picked is None:
        return None
    await preload_corpus()  # 1.3 MB parse, once, off the loop
    return await asyncio.to_thread(build_question, user_id, picked[0], picked[1], today)


async def rebuild(user_id: int, surah: int, ayah: int, day: date) -> Optional[RecallQuestion]:
    """The question asked for (surah, ayah) on `day`, or None if it no longer
    resolves."""
    await preload_corpus()
    try:
        return await asyncio.to_thread(build_question, user_id, surah, ayah, day)
    except ValueError:
        return None


@dataclass
class Score:
    correct: bool
    correct_option: str
    logged: bool = False  # a recall_check session was written today
    milestone_key: Optional[str] = None  # streak milestone reached by this pass


async def score(user_id: int, question: RecallQuestion, choice: int) -> Score:
    """Judge `choice` and, on a pass, earn the day. E2: a pass logs a session with
    no portion, so the store dedupes every later pass today onto the same row."""
    if not question.is_correct(choice):
        return Score(False, question.correct)
    outcome = await record_session(user_id, KIND_RECALL_CHECK)
    key = (
        outcome.milestone.key if outcome.logged and outcome.milestone.reached is not None else None
    )
    return Score(True, question.correct, outcome.logged, key)
