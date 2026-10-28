# Plan operations (spec items D1, D4, D5): preview, save, the enqueue chain,
# today's portion, "I know this by heart" and the pause/resume/abandon
# lifecycle. Lifted out of hifz/memorize.py so the /memorize handlers and the
# Mini App's /plans, /today and /drills routes run the same code.
#
# The load-bearing properties are documented on hifz/memorize.py and tested
# there; briefly:
#
#   D1  the preview is the plan — `build_plan` is pure, so the preview and the
#       stored rows are one call over the same arguments (including the start
#       date the preview used).
#   D4  the double tap is guarded by `complete_plan_day`, a conditional write
#       taken first; the interval, session and streak follow only on the branch
#       that won it.
#   D5  a paused plan pushes nothing; `hifz.memorize.push_plan_day` re-reads the
#       plan's status, and resuming re-arms the chain through `enqueue_next`.

from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from typing import List, Optional, Sequence

from hifz.refs import KIND_JUZ, KIND_RANGE, KIND_SURAH, Ref, format_ref, juz_ref
from lib.hifz_progress import load_summary
from lib.localtime import DEFAULT_OFFSET, is_valid_offset, local_date, next_due_utc, \
    normalize_offset, to_utc
from lib.plan_builder import AUTO_PACE, Portion, advancing, build_plan, to_day_specs
from lib.scheduler import enqueue
from lib.store.plans import DAY_COMPLETED, DAY_PENDING, PLAN_ACTIVE, PLAN_COMPLETE, \
    PLAN_PAUSED
from lib.store.sessions import KIND_DRILL
from lib.streaks import record_session
from modules import Quran
from services.profile import as_time

# The scheduler kind a plan day's push is queued under. hifz/memorize.py
# registers the handler that delivers it.
SEND_KIND = "plan_day"

# Lifecycle actions.
PAUSE, RESUME, ABANDON = "pause", "resume", "abandon"

# A reminder time is required to queue a push; a plan saved without one (the
# Mini App lets the profile carry it) falls back to this.
DEFAULT_REMINDER = time(7, 0)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


# --- A plan's target -----------------------------------------------------------

def plan_ref(plan) -> Ref:
    """A stored plan's span as a `Ref`, for `build_plan` and `format_ref`.

    This is what makes "re-derive the calendar from the plan's own columns" work:
    the generator is pure, so the same target, pace, weekday set and start date
    always produce the same portions — which is how a `plan_day` row is known to
    be a consolidation day even though the table has no column for it.
    """
    kind = plan.target_kind if plan.target_kind in (KIND_SURAH, KIND_JUZ, KIND_RANGE) \
        else KIND_RANGE
    return Ref(kind, plan.start_surah, plan.start_ayah, plan.end_surah, plan.end_ayah)


def target_kind(ref: Ref) -> str:
    """`plan.target_kind` for a parsed target — the column takes three values."""
    return ref.kind if ref.kind in (KIND_SURAH, KIND_JUZ, KIND_RANGE) else KIND_RANGE


def target_label(plan) -> str:
    """What `{target}` is filled with: "Al-Mulk", "Juz 30", or "67:1-68:5"."""
    ref = plan_ref(plan)
    if plan.target_kind == KIND_SURAH and ref.is_single_surah():
        return Quran.get_surah_name(plan.start_surah)
    if plan.target_kind == KIND_JUZ:
        for n in range(1, 31):
            juz = juz_ref(n)
            if juz is not None and juz.as_tuple() == ref.as_tuple():
                return "Juz %d" % n
    return format_ref(ref)


def profile_offset(profile) -> str:
    """The profile's UTC offset, normalized, or the default when unset/invalid."""
    offset = getattr(profile, "timezone", None) or DEFAULT_OFFSET
    if not is_valid_offset(offset):
        offset = DEFAULT_OFFSET
    return normalize_offset(offset)


async def user_local_today(store, user_id: int, now: Optional[datetime] = None) -> date:
    profile = await store.profiles.get_profile(user_id)
    return local_date(now or utcnow(), profile_offset(profile))


# --- Preview and save (D1) -----------------------------------------------------

def preview(ref: Ref, pace: int, days: Sequence[int], start: date) -> List[Portion]:
    """The calendar a plan with these settings would have. Raises ValueError on
    an empty weekday set or an unusable pace — `build_plan`'s own validation."""
    return build_plan(ref, int(pace or AUTO_PACE), list(days), start)


@dataclass
class SavedPlan:
    plan: object
    portions: List[Portion]
    first_date: date          # local date of the first push


async def save_plan(store, user_id: int, chat_id: int, ref: Ref, pace: int,
                    days: Sequence[int], start: date, offset: str,
                    reminder: Optional[time]) -> SavedPlan:
    """Write a plan (retiring any earlier one) and queue its first push.

    The portions are rebuilt from the arguments rather than passed in: same
    target, same pace, same weekdays, same start date, same pure function — so
    what is stored is what was previewed, row for row. The offset and reminder
    are written to the profile, since the push chain reads them from there.
    """
    pace = int(pace or AUTO_PACE)
    portions = preview(ref, pace, days, start)
    offset = normalize_offset(offset or DEFAULT_OFFSET)
    reminder = reminder or DEFAULT_REMINDER

    # "One active plan per user" is a convention, so the old one is retired here
    # rather than by a constraint that would make pause-then-create a crash.
    for plan in await store.plans.list_plans(user_id):
        if plan.status != PLAN_COMPLETE:
            await store.plans.set_plan_status(plan.id, PLAN_COMPLETE)

    plan = await store.plans.create_plan(
        user_id, target_kind(ref), ref.start_surah, ref.start_ayah,
        ref.end_surah, ref.end_ayah, pace, list(days), to_day_specs(portions))

    await store.profiles.set_timezone(user_id, offset)
    await store.profiles.set_reminder_time(user_id, reminder)

    queued = await enqueue_next(store, user_id, chat_id, plan)
    first = local_date(queued.due_at, offset) if queued is not None \
        else portions[0].scheduled_date
    print("HIFZ: plan #%d saved for %d — %d portion(s) over %d day(s), first push %s"
          % (plan.id, user_id, len(advancing(portions)), len(portions), first))
    return SavedPlan(plan, portions, first)


# --- The enqueue chain -----------------------------------------------------------

async def enqueue_next(store, user_id: int, chat_id: int, plan,
                       now: Optional[datetime] = None):
    """Queue the push for the plan's next pending portion. None if there is none.

    Called when a plan is saved, when a push fires, when a plan is resumed, and
    (harmlessly) when a portion is marked known. `enqueue` answers None on a key
    clash rather than raising, so calling it more often than strictly necessary
    is a no-op — which is what makes the chain self-healing instead of a single
    point of failure.

    The due instant is the portion's own `scheduled_date` at the user's local
    reminder time; a portion whose date has already passed (the plan was paused
    for a week, or set up after today's reminder) is pushed at the next reminder
    instead, so a backlog is delivered one portion a day rather than dropped by
    the scheduler's staleness window.
    """
    if plan is None or plan.status != PLAN_ACTIVE:
        return None

    profile = await store.profiles.get_profile(user_id)
    reminder = as_time(profile.reminder_time) if profile is not None else None
    if reminder is None:
        print("HIFZ: plan #%d has no reminder time; nothing queued" % plan.id)
        return None
    offset = profile_offset(profile)

    pending = await store.plans.list_plan_days(plan.id, state=DAY_PENDING)
    if not pending:
        return None
    day = pending[0]

    now = now or utcnow()
    due_at = to_utc(datetime.combine(day.scheduled_date, reminder), offset)
    if due_at <= now:
        due_at = next_due_utc(reminder, offset, now)

    return await enqueue(store, SEND_KIND, chat_id, due_at,
                         local_day=local_date(due_at, offset),
                         payload={"plan_day_id": day.id, "plan_id": plan.id,
                                  "user_id": user_id, "offset": offset})


# --- Reading a plan ------------------------------------------------------------

async def current_plan(store, user_id: int):
    """The user's active plan, else their (most recent) paused one, else None."""
    plan = await store.plans.get_active_plan(user_id)
    if plan is not None:
        return plan
    paused = await store.plans.list_plans(user_id, PLAN_PAUSED)
    return paused[0] if paused else None


async def portions_of(store, plan) -> List[Portion]:
    """The generated calendar a stored plan came from (empty if it cannot be
    re-derived). Same call as the preview, over the plan's own columns."""
    days = await store.plans.list_plan_days(plan.id)
    if not days:
        return []
    try:
        return build_plan(plan_ref(plan), plan.pace, plan.days_of_week,
                          days[0].scheduled_date)
    except ValueError as err:                   # a plan with no weekdays cannot exist
        print("HIFZ: cannot re-derive plan #%d: %s" % (plan.id, err))
        return []


def match_portion(portions: Sequence[Portion], day) -> Optional[Portion]:
    for portion in portions:
        if (portion.scheduled_date, portion.surah, portion.start_ayah, portion.end_ayah) \
                == (day.scheduled_date, day.surah, day.start_ayah, day.end_ayah):
            return portion
    return None


async def portion_for(store, plan, day) -> Optional[Portion]:
    """The generated `Portion` a stored `plan_day` row came from, or None.

    `plan_day` has no column for `drill` or `unit`, and it does not need one:
    the generator is pure, so re-running it over the plan's own columns and its
    own first date reproduces the identical calendar, and the row is matched by
    (date, surah, span).
    """
    return match_portion(await portions_of(store, plan), day)


async def day_position(store, plan, day) -> tuple:
    """(which day this is, how many days the plan has)."""
    days = await store.plans.list_plan_days(plan.id)
    for index, row in enumerate(days, start=1):
        if row.id == day.id:
            return index, len(days)
    return 1, len(days) or 1


async def due_days(store, user_id: int, plan, now: Optional[datetime] = None) -> list:
    """The plan's portions not yet completed and due today or earlier (local)."""
    today = await user_local_today(store, user_id, now)
    return [d for d in await store.plans.list_plan_days(plan.id, on_or_before=today)
            if d.state != DAY_COMPLETED]


async def owned_day(store, user_id: int, plan_day_id: int):
    """(day, plan) when `plan_day_id` is one of `user_id`'s portions, else (None, None)."""
    day = await store.plans.get_plan_day(plan_day_id)
    if day is None:
        return None, None
    plan = await store.plans.get_plan(day.plan_id)
    if plan is None or plan.user_id != user_id:
        return None, None
    return day, plan


# --- "I know this by heart" (D4) ----------------------------------------------

DONE, ALREADY, MISSING = "completed", "already", "missing"


@dataclass
class DrillResult:
    status: str                       # DONE | ALREADY | MISSING
    day: object = None
    plan: object = None
    percent_text: Optional[str] = None
    plan_completed: bool = False


async def complete_day(store, user_id: int, chat_id: int, plan_day_id: int) -> DrillResult:
    """End a drill: mark the day done, write the interval, log the session.

    The order is the correctness argument. `complete_plan_day` is a conditional
    write, so it is taken **first** and everything after it runs only on the tap
    that won: a second tap on the same portion — in chat or in the app — gets
    None and stops, which is why a streak can never tick twice off one portion.
    `record_session` is itself idempotent on (user, local date, kind, portion), so
    even a lost update between the two writes cannot double-log.
    """
    day, plan = await owned_day(store, user_id, plan_day_id)
    if day is None:
        return DrillResult(MISSING)

    completed = await store.plans.complete_plan_day(plan_day_id)
    if completed is None:
        return DrillResult(ALREADY, day, plan)

    await store.hifz.add_interval(user_id, day.surah, day.start_ayah, day.end_ayah)
    await record_session(user_id, KIND_DRILL, surah=day.surah,
                         start_ayah=day.start_ayah, end_ayah=day.end_ayah)

    summary = await load_summary(store, user_id, focus_surah=day.surah)
    pct = summary.focus.percent_text if summary.focus is not None \
        else summary.quran.percent_text

    remaining = await store.plans.count_plan_days(plan.id) \
        - await store.plans.count_plan_days(plan.id, DAY_COMPLETED)
    if remaining <= 0:
        await store.plans.set_plan_status(plan.id, PLAN_COMPLETE)
        return DrillResult(DONE, day, plan, pct, plan_completed=True)
    # Belt and braces: the push that delivered this portion already queued the
    # next one, so this is normally a key clash answering None.
    await enqueue_next(store, user_id, chat_id, plan)
    return DrillResult(DONE, day, plan, pct)


# --- Lifecycle (D5) -------------------------------------------------------------

async def change_status(store, user_id: int, chat_id: int, action: str):
    """Pause, resume or abandon the user's current plan. Returns the updated plan,
    or None when there is no plan to act on.

    Pausing deletes nothing queued: `push_plan_day` re-reads the status and
    declines to deliver, so the chain lapses; resuming re-arms it. Abandoning
    moves the plan to 'complete' — the column's "no longer running" value — and
    keeps its rows, so what was memorized is still counted.
    """
    plan = await current_plan(store, user_id)
    if plan is None:
        return None
    if action == PAUSE:
        return await store.plans.set_plan_status(plan.id, PLAN_PAUSED) or plan
    if action == RESUME:
        updated = await store.plans.set_plan_status(plan.id, PLAN_ACTIVE) or plan
        await enqueue_next(store, user_id, chat_id, updated)
        return updated
    if action == ABANDON:
        return await store.plans.set_plan_status(plan.id, PLAN_COMPLETE) or plan
    raise ValueError("unknown plan action %r" % action)
