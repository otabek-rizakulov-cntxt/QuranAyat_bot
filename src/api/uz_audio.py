# POST /uz-audio/send — the Mini App's "send to chat" for the Uzbek translation
# audio (docs/MULTILINGUAL_PLAN.md §8.1). The app plays ayahs straight from
# newbooks.uz; to *keep* one, it asks the bot to post the clip into the user's
# private chat, where Telegram lets them save or forward it. Same code path as
# the bot's own buttons (infra.uz_audio_delivery).

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from infra import uz_audio
from infra.store.identity import NON_TELEGRAM_ID_START
from infra.uz_audio_delivery import send_to_user, valid_clip
from services.user_settings import UserSettings

from .auth import require_user

router = APIRouter()


class SendIn(BaseModel):
    surah: int = Field(ge=1, le=114)
    # Both omitted: the whole surah. Otherwise ayahs start..end (end defaults to start).
    start: int | None = Field(default=None, ge=1)
    end: int | None = Field(default=None, ge=1)


class SendOut(BaseModel):
    sent: bool


@router.post("/uz-audio/send", response_model=SendOut)
async def send(body: SendIn, request: Request, user_id: int = Depends(require_user)) -> SendOut:
    if not uz_audio.available(body.surah):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "no Uzbek audio for this surah")
    if user_id >= NON_TELEGRAM_ID_START:  # a WhatsApp-only account has no Telegram chat
        raise HTTPException(status.HTTP_409_CONFLICT, "only a Telegram chat can receive audio")
    bot = getattr(request.app.state.runtime, "bot", None)
    if bot is None:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "bot not running")

    ui_lang = (await UserSettings().get(user_id)).ui_lang
    end = body.end or body.start
    if body.start is not None and not valid_clip(body.surah, body.start, end):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "bad ayah range")
    try:
        await send_to_user(bot, user_id, body.surah, body.start, end, ui_lang)
    except (OSError, httpx.HTTPError) as err:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "audio source unavailable") from err
    return SendOut(sent=True)
