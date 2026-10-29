# Memorization plans: preview, save, the active plan, its lifecycle, today's
# portion and "I know this by heart" — all through services/plans.py, the same
# code /memorize runs.

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from domain.localtime import DEFAULT_OFFSET, is_valid_offset
from domain.plan_builder import AUTO_PACE, advancing
from domain.refs import KIND_RANGE, Ref, format_ref
from lib.store import get_store
from lib.store.plans import DAY_COMPLETED
from services import plans as plans_service
from services import profile as profile_service

from .auth import require_user
from .common import RefOut, not_found, parse_ref_or_422, ref_out

router = APIRouter()

# Same bounds as the bot's typed pace (hifz/memorize.py PACE_MIN..PACE_MAX).
PACE_MAX = 50


class PlanSettingsIn(BaseModel):
    target: str = Field(description='A reference: "67", "juz 30", "67:1-10", "page 562"')
    pace: int = Field(AUTO_PACE, ge=0, le=PACE_MAX, description="Ayahs per day; 0 = automatic")
    days: List[int] = Field(min_length=1, max_length=7, description="Weekdays, 1=Mon … 7=Sun")
    start: Optional[date] = Field(None, description="First day; defaults to the user's local today")


class PortionOut(BaseModel):
    date: date
    surah: int
    start_ayah: int
    end_ayah: int
    review: bool
    label: str


class PreviewOut(BaseModel):
    target: RefOut
    start: date
    end: date
    calendar_days: int
    portions_count: int
    portions: List[PortionOut]


def _portion_out(portion) -> PortionOut:
    return PortionOut(
        date=portion.scheduled_date,
        surah=portion.surah,
        start_ayah=portion.start_ayah,
        end_ayah=portion.end_ayah,
        review=portion.is_consolidation,
        label=format_ref(portion.as_ref()),
    )


def _validated_days(days: List[int]) -> List[int]:
    cleaned = sorted(set(days))
    if not cleaned or any(d < 1 or d > 7 for d in cleaned):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="days must be weekdays 1-7"
        )
    return cleaned


async def _build(body: PlanSettingsIn, user_id: int):
    ref = parse_ref_or_422(body.target)
    days = _validated_days(body.days)
    store = await get_store()
    start = body.start or await plans_service.user_local_today(store, user_id)
    try:
        portions = plans_service.preview(ref, body.pace, days, start)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(err))
    return ref, days, start, portions


def _preview_out(ref: Ref, start: date, portions) -> PreviewOut:
    return PreviewOut(
        target=ref_out(ref),
        start=start,
        end=portions[-1].scheduled_date,
        calendar_days=len(portions),
        portions_count=len(advancing(portions)),
        portions=[_portion_out(p) for p in portions],
    )


@router.post("/plans/preview", response_model=PreviewOut)
async def preview(body: PlanSettingsIn, user_id: int = Depends(require_user)) -> PreviewOut:
    """The calendar a plan would have — nothing is written (D1). Pass the
    returned `start` back to POST /plans so the saved rows equal this preview."""
    ref, _, start, portions = await _build(body, user_id)
    return _preview_out(ref, start, portions)


class PlanCreateIn(PlanSettingsIn):
    timezone: Optional[str] = Field(
        None, description='UTC offset like "+05:00"; defaults to the profile\'s'
    )
    reminder_time: Optional[str] = Field(
        None, description='"HH:MM"; defaults to the profile\'s, else 07:00'
    )


class PlanDayOut(BaseModel):
    id: int
    date: date
    surah: int
    start_ayah: int
    end_ayah: int
    state: str
    review: bool
    label: str


class PlanOut(BaseModel):
    id: int
    status: str
    target: RefOut
    target_label: str
    pace: int
    days_of_week: List[int]
    total: int
    completed: int
    today: date
    days: List[PlanDayOut]


async def _plan_out(store, user_id: int, plan) -> PlanOut:
    rows = await store.plans.list_plan_days(plan.id)
    portions = await plans_service.portions_of(store, plan)
    days = []
    for row in rows:
        portion = plans_service.match_portion(portions, row)
        days.append(
            PlanDayOut(
                id=row.id,
                date=row.scheduled_date,
                surah=row.surah,
                start_ayah=row.start_ayah,
                end_ayah=row.end_ayah,
                state=row.state,
                review=bool(portion is not None and portion.is_consolidation),
                label=format_ref(
                    Ref(KIND_RANGE, row.surah, row.start_ayah, row.surah, row.end_ayah)
                ),
            )
        )
    return PlanOut(
        id=plan.id,
        status=plan.status,
        target=ref_out(plans_service.plan_ref(plan)),
        target_label=plans_service.target_label(plan),
        pace=plan.pace,
        days_of_week=list(plan.days_of_week),
        total=len(rows),
        completed=sum(1 for r in rows if r.state == DAY_COMPLETED),
        today=await plans_service.user_local_today(store, user_id),
        days=days,
    )


@router.post("/plans", response_model=PlanOut, status_code=status.HTTP_201_CREATED)
async def create(body: PlanCreateIn, user_id: int = Depends(require_user)) -> PlanOut:
    """Save a plan (retiring any earlier one, as /memorize does) and queue its
    first push. The bot delivers the daily drills from here on."""
    ref, days, start, _ = await _build(body, user_id)
    store = await get_store()
    profile = await store.profiles.get_profile(user_id)

    offset = body.timezone or getattr(profile, "timezone", None) or DEFAULT_OFFSET
    if not is_valid_offset(offset):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid timezone offset"
        )
    if body.reminder_time:
        reminder = profile_service.parse_reminder_time(body.reminder_time)
        if reminder is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid reminder_time"
            )
    else:
        reminder = profile_service.as_time(getattr(profile, "reminder_time", None))

    saved = await plans_service.save_plan(
        store, user_id, user_id, ref, body.pace, days, start, offset, reminder
    )
    return await _plan_out(store, user_id, saved.plan)


@router.get("/plans/active", response_model=Optional[PlanOut])
async def active(user_id: int = Depends(require_user)) -> Optional[PlanOut]:
    """The running (or paused) plan with every day's state; null when none."""
    store = await get_store()
    plan = await plans_service.current_plan(store, user_id)
    return None if plan is None else await _plan_out(store, user_id, plan)


_ACTIONS = {
    "pause": plans_service.PAUSE,
    "resume": plans_service.RESUME,
    "abandon": plans_service.ABANDON,
}


@router.post("/plans/active/{action}", response_model=Optional[PlanOut])
async def lifecycle(action: str, user_id: int = Depends(require_user)) -> Optional[PlanOut]:
    """pause | resume | abandon. A paused plan is pushed nothing; resuming re-arms
    the daily push. Abandoning answers null (there is no current plan after it)."""
    if action not in _ACTIONS:
        raise not_found("unknown action")
    store = await get_store()
    plan = await plans_service.change_status(store, user_id, user_id, _ACTIONS[action])
    if plan is None:
        raise not_found("no plan")
    current = await plans_service.current_plan(store, user_id)
    return None if current is None else await _plan_out(store, user_id, current)


class TodayOut(BaseModel):
    status: str = Field(description="none | paused | due | done")
    today: date
    plan_id: Optional[int] = None
    target_label: Optional[str] = None
    day: Optional[PlanDayOut] = None  # the portion to drill now
    position: Optional[int] = None  # which day of the plan it is
    total: Optional[int] = None
    next_date: Optional[date] = None  # when status is "done": the next portion's date


@router.get("/today", response_model=TodayOut)
async def today(user_id: int = Depends(require_user)) -> TodayOut:
    """Today's portion: the earliest one not yet completed and due today or
    earlier — the same pick as the bot's "Start today's portion"."""
    store = await get_store()
    local_today = await plans_service.user_local_today(store, user_id)
    plan = await plans_service.current_plan(store, user_id)
    if plan is None:
        return TodayOut(status="none", today=local_today)
    if plan.status != plans_service.PLAN_ACTIVE:
        return TodayOut(
            status="paused",
            today=local_today,
            plan_id=plan.id,
            target_label=plans_service.target_label(plan),
        )

    out = await _plan_out(store, user_id, plan)
    due = await plans_service.due_days(store, user_id, plan)
    if not due:
        upcoming = [d for d in out.days if d.state != DAY_COMPLETED and d.date > local_today]
        return TodayOut(
            status="done",
            today=local_today,
            plan_id=plan.id,
            target_label=out.target_label,
            total=out.total,
            next_date=upcoming[0].date if upcoming else None,
        )
    first = next(d for d in out.days if d.id == due[0].id)
    position = [d.id for d in out.days].index(first.id) + 1
    return TodayOut(
        status="due",
        today=local_today,
        plan_id=plan.id,
        target_label=out.target_label,
        day=first,
        position=position,
        total=out.total,
    )


class DrillOut(BaseModel):
    status: str = Field(description="completed | already")
    label: str
    percent: Optional[str] = None
    plan_completed: bool = False
    target_label: Optional[str] = None


@router.post("/drills/{plan_day_id}/complete", response_model=DrillOut)
async def complete(plan_day_id: int, user_id: int = Depends(require_user)) -> DrillOut:
    """ "I know this by heart". Idempotent across the app and the chat button: the
    second tap for the same portion answers `already` and logs nothing (D4)."""
    store = await get_store()
    result = await plans_service.complete_day(store, user_id, user_id, plan_day_id)
    if result.status == plans_service.MISSING:
        raise not_found("no such portion")
    day = result.day
    label = format_ref(Ref(KIND_RANGE, day.surah, day.start_ayah, day.surah, day.end_ayah))
    return DrillOut(
        status=result.status,
        label=label,
        percent=result.percent_text,
        plan_completed=result.plan_completed,
        target_label=plans_service.target_label(result.plan) if result.plan_completed else None,
    )
