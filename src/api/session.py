# Session, settings and profile: POST /auth/telegram, GET /me, PATCH /me/settings,
# PATCH /me/profile (docs/MINI_APP_PLAN.md §4-5).

import re
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from config.settings import get_settings
from domain.localtime import is_valid_offset, normalize_offset, offset_options
from domain.quran import TranslationRegistry
from infra import catalog
from lib.store import get_store
from lib.streaks import streak_summary
from lib.user_settings import UserSettings
from locales import is_supported, is_ui_language, normalize_lang
from services import plans as plans_service
from services import profile as profile_service

from .auth import (
    DEFAULT_TOKEN_TTL,
    InvalidInitData,
    init_data_max_age,
    issue_token,
    jwt_secret,
    require_user,
    validate_init_data,
)

router = APIRouter()

# Telegram's own limit on a `startapp` value: 1-64 chars of [A-Za-z0-9_-].
# Anything else is dropped rather than echoed back to the client.
_START_PARAM = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


class TelegramAuthIn(BaseModel):
    init_data: str


class TelegramUser(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None


class Settings(BaseModel):
    ui_lang: str
    translation_lang: str
    reciter: str


class AuthOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: TelegramUser
    settings: Settings
    start_param: Optional[str] = None


class Profile(BaseModel):
    display_name: Optional[str] = None
    leaderboard_opt_in: bool = False
    timezone: Optional[str] = None
    reminder_time: Optional[str] = None
    current_streak: int = 0
    longest_streak: int = 0


class PlanSummary(BaseModel):
    id: int
    status: str
    target: str
    day: int
    total: int


class StreakBrief(BaseModel):
    current: int
    longest: int
    active_today: bool
    at_risk: bool


class MeOut(BaseModel):
    user_id: int
    settings: Settings
    profile: Profile
    plan: Optional[PlanSummary] = None
    streak: StreakBrief
    offsets: List[str]


def _settings(row) -> Settings:
    return Settings(ui_lang=row.ui_lang, translation_lang=row.translation_lang, reciter=row.reciter)


def _profile(profile) -> Profile:
    if profile is None:
        return Profile()
    return Profile(
        display_name=profile.display_name,
        leaderboard_opt_in=profile.leaderboard_opt_in,
        timezone=profile.timezone,
        reminder_time=profile_service.format_reminder_time(
            profile_service.as_time(profile.reminder_time)
        )
        or None,
        current_streak=profile.current_streak,
        longest_streak=profile.longest_streak,
    )


@router.post("/auth/telegram", response_model=AuthOut)
async def auth_telegram(body: TelegramAuthIn) -> AuthOut:
    """Exchange the Mini App's initData for a short-lived access token."""
    secret = jwt_secret()
    bot_token = get_settings().token
    if not secret or not bot_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="mini app auth is not configured",
        )
    try:
        fields = validate_init_data(body.init_data, bot_token, max_age=init_data_max_age())
    except InvalidInitData:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid initData")

    tg_user = fields["user"]
    user_id = int(tg_user["id"])
    # The same row first contact with the bot creates: chat_id == user_id in a
    # private chat, so the legacy-Redis migration in UserSettings applies too.
    row = await UserSettings().get(
        user_id, user_id, default_ui_lang=normalize_lang(tg_user.get("language_code"))
    )

    start_param = fields.get("start_param")
    if start_param is not None and not _START_PARAM.match(start_param):
        start_param = None

    return AuthOut(
        access_token=issue_token(user_id, secret),
        expires_in=DEFAULT_TOKEN_TTL,
        user=TelegramUser(**{k: tg_user.get(k) for k in TelegramUser.model_fields}),
        settings=_settings(row),
        start_param=start_param,
    )


async def _me(user_id: int) -> MeOut:
    row = await UserSettings().get(user_id, user_id)
    store = await get_store()
    profile = await store.profiles.get_profile(user_id)

    plan_out = None
    plan = await plans_service.current_plan(store, user_id)
    if plan is not None:
        total = await store.plans.count_plan_days(plan.id)
        done = await store.plans.count_plan_days(plan.id, "completed")
        plan_out = PlanSummary(
            id=plan.id,
            status=plan.status,
            target=plans_service.target_label(plan),
            day=min(done + 1, total) if total else 0,
            total=total,
        )

    streak = await streak_summary(user_id)
    return MeOut(
        user_id=user_id,
        settings=_settings(row),
        profile=_profile(profile),
        plan=plan_out,
        streak=StreakBrief(
            current=streak.current,
            longest=streak.longest,
            active_today=streak.active_today,
            at_risk=streak.at_risk,
        ),
        offsets=offset_options(),
    )


@router.get("/me", response_model=MeOut)
async def me(user_id: int = Depends(require_user)) -> MeOut:
    """The caller's settings, hifz profile, current plan and streak. Read-only:
    a profile that does not exist yet is reported as defaults, not created."""
    return await _me(user_id)


class SettingsPatch(BaseModel):
    ui_lang: Optional[str] = None
    translation_lang: Optional[str] = None
    reciter: Optional[str] = None


def _unprocessable(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


@router.patch("/me/settings", response_model=Settings)
async def patch_settings(body: SettingsPatch, user_id: int = Depends(require_user)) -> Settings:
    """Change UI language, translation language and/or reciter — the same three
    independent settings /language, /translation and /reciter write. Changing
    the UI language never changes the reciter (the README guarantee)."""
    settings = UserSettings()
    if body.ui_lang is not None:
        if not is_ui_language(body.ui_lang):
            raise _unprocessable("unknown ui_lang")
        await settings.set_ui_lang(user_id, user_id, body.ui_lang)
    if body.translation_lang is not None:
        if (
            not is_supported(body.translation_lang)
            or body.translation_lang not in TranslationRegistry.available()
        ):
            raise _unprocessable("unknown translation_lang")
        await settings.set_translation_lang(user_id, user_id, body.translation_lang)
    if body.reciter is not None:
        if not any(p["subfolder"] == body.reciter for p in catalog.performers()):
            raise _unprocessable("unknown reciter")
        await settings.set_reciter(user_id, user_id, body.reciter)
    return _settings(await settings.get(user_id, user_id))


class ProfilePatch(BaseModel):
    """Every field optional; send `null` to clear a reminder time."""

    display_name: Optional[str] = None
    leaderboard_opt_in: Optional[bool] = None
    timezone: Optional[str] = None
    reminder_time: Optional[str] = None


@router.patch("/me/profile", response_model=MeOut)
async def patch_profile(body: ProfilePatch, user_id: int = Depends(require_user)) -> MeOut:
    """The /profile card's four settings. Joining the leaderboard needs a display
    name — the same rule as the bot: nobody is shown under a blank label — so
    opting in without one answers 409 `name_required`."""
    store = await get_store()
    fields = body.model_fields_set

    if "display_name" in fields:
        name = profile_service.valid_display_name(body.display_name or "")
        if name is None:
            raise _unprocessable(
                "display_name must be %d-%d characters"
                % (profile_service.NAME_MIN, profile_service.NAME_MAX)
            )
        await profile_service.set_display_name(store, user_id, name)

    if "timezone" in fields:
        if not body.timezone or not is_valid_offset(body.timezone):
            raise _unprocessable("invalid timezone offset")
        await profile_service.save_timezone(store, user_id, normalize_offset(body.timezone))

    if "reminder_time" in fields:
        value = None
        if body.reminder_time:
            value = profile_service.parse_reminder_time(body.reminder_time)
            if value is None:
                raise _unprocessable("invalid reminder_time")
        await profile_service.save_reminder_time(store, user_id, value)

    if "leaderboard_opt_in" in fields and body.leaderboard_opt_in is not None:
        if body.leaderboard_opt_in:
            if not await profile_service.join_leaderboard(store, user_id, None):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="name_required")
        else:
            await profile_service.leave_leaderboard(store, user_id)

    return await _me(user_id)
