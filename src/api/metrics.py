# POST /metrics/audio: one "tap -> sound" timing from the Mini App's player, and
# GET /metrics/audio: p50/p95 per host for reviewers (docs/MAKHRAJ_3D_PLAN.md §9).

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from services import audio_metrics
from services import tajweed as tajweed_service

from .auth import require_user

router = APIRouter()


class AudioSampleIn(BaseModel):
    host: str = Field(min_length=1, max_length=64, pattern=r"^[a-z0-9.-]+$")
    kind: str = Field(pattern="^(%s)$" % "|".join(audio_metrics.KINDS))
    ms: int = Field(ge=0, le=60_000)
    cached: bool = False
    net: str = Field(default="", max_length=8, pattern=r"^[a-z0-9-]*$")
    platform: str = Field(default="", max_length=16, pattern=r"^[a-z0-9_-]*$")


class AudioRowOut(BaseModel):
    host: str
    kind: str
    cached: bool
    n: int
    p50: int
    p95: int


@router.post("/metrics/audio", status_code=status.HTTP_204_NO_CONTENT)
async def audio_sample(body: AudioSampleIn, user_id: int = Depends(require_user)) -> None:
    audio_metrics.record(audio_metrics.Sample(**body.model_dump()))


@router.get("/metrics/audio", response_model=List[AudioRowOut])
async def audio_summary(user_id: int = Depends(require_user)) -> List[AudioRowOut]:
    if not tajweed_service.is_reviewer(user_id):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "reviewers only")
    return [AudioRowOut(**row) for row in audio_metrics.summary()]
