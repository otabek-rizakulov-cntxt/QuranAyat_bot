# The Mini App's HTTP API, mounted on the bot's FastAPI app at /api/v1
# (docs/MINI_APP_PLAN.md §5).
#
# Routes here are thin adapters: they authenticate, validate shapes and call
# into `lib/*` (and, from Phase 1, `services/*`). No SQL lives in this package —
# persistence goes through `lib.store`, the same as the bot handlers.

import re
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from config import Environment
from lib.store import get_store
from lib.user_settings import UserSettings
from locales import normalize_lang

from .auth import (DEFAULT_TOKEN_TTL, InvalidInitData, init_data_max_age, issue_token,
                   jwt_secret, require_user, validate_init_data)

__all__ = ["router", "require_user"]

router = APIRouter(prefix="/api/v1")

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


class MeOut(BaseModel):
    user_id: int
    settings: Settings
    profile: Profile


@router.post("/auth/telegram", response_model=AuthOut)
async def auth_telegram(body: TelegramAuthIn) -> AuthOut:
    """Exchange the Mini App's initData for a short-lived access token."""
    secret = jwt_secret()
    bot_token = Environment.get_env("token")
    if not secret or not bot_token:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="mini app auth is not configured")
    try:
        fields = validate_init_data(body.init_data, bot_token, max_age=init_data_max_age())
    except InvalidInitData:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="invalid initData")

    tg_user = fields["user"]
    user_id = int(tg_user["id"])
    # The same row first contact with the bot creates: chat_id == user_id in a
    # private chat, so the legacy-Redis migration in UserSettings applies too.
    row = await UserSettings().get(user_id, user_id,
                                   default_ui_lang=normalize_lang(tg_user.get("language_code")))

    start_param = fields.get("start_param")
    if start_param is not None and not _START_PARAM.match(start_param):
        start_param = None

    return AuthOut(
        access_token=issue_token(user_id, secret),
        expires_in=DEFAULT_TOKEN_TTL,
        user=TelegramUser(**{k: tg_user.get(k) for k in TelegramUser.model_fields}),
        settings=Settings(ui_lang=row.ui_lang, translation_lang=row.translation_lang,
                          reciter=row.reciter),
        start_param=start_param,
    )


@router.get("/me", response_model=MeOut)
async def me(user_id: int = Depends(require_user)) -> MeOut:
    """The caller's settings and hifz profile. Read-only: a profile that does
    not exist yet is reported as defaults, not created."""
    row = await UserSettings().get(user_id, user_id)
    store = await get_store()
    profile = await store.profiles.get_profile(user_id)
    return MeOut(
        user_id=user_id,
        settings=Settings(ui_lang=row.ui_lang, translation_lang=row.translation_lang,
                          reciter=row.reciter),
        profile=Profile() if profile is None else Profile(
            display_name=profile.display_name,
            leaderboard_opt_in=profile.leaderboard_opt_in,
            timezone=profile.timezone,
            reminder_time=(profile.reminder_time.strftime("%H:%M")
                           if profile.reminder_time else None),
            current_streak=profile.current_streak,
            longest_streak=profile.longest_streak,
        ),
    )
