# Tajweed lessons in the Mini App (docs/TAJWEED_PLAN.md): GET /tajweed, POST /tajweed/done,
# POST /tajweed/review (reviewers: approve a rules lesson or an audio lesson's text tracking).
#
# The lesson texts and the audio manifest are static content (export_web_content.py
# -> public/content/tajweed/{uz,uz-Cyrl}.json); this route adds what is per user or per
# deployment: where the audio lives, which rules lessons are approved, which lessons
# this user has done, and whether they review. Marking done is services.tajweed, the
# same code as the bot's ✅ button, so the streak counts it once either way.

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from infra.store import get_store
from services import tajweed as service

from .auth import require_user
from .common import not_found

router = APIRouter()


class TajweedOut(BaseModel):
    audio_base: Optional[str]  # None: the audio lessons are not available yet
    approved: List[str]  # rules lessons everyone may open
    done: List[str]
    reviewer: bool  # may open drafts too
    tracking: List[str]  # audio lessons whose line-by-line text is approved


class DoneIn(BaseModel):
    lesson_id: str = Field(min_length=1, max_length=64)


class DoneOut(BaseModel):
    done: bool
    first_time: bool  # False: it was done already, so no new streak session
    streak: Optional[int] = None  # the current streak after a first-time completion


@router.get("/tajweed", response_model=TajweedOut)
async def state(user_id: int = Depends(require_user)) -> TajweedOut:
    store = await get_store()
    return TajweedOut(
        audio_base=service.audio_base(),
        approved=sorted(await service.approved_ids(store)),
        done=sorted(await store.tajweed.done(user_id)),
        reviewer=service.is_reviewer(user_id),
        tracking=sorted(await service.tracking_ids(store)),
    )


@router.post("/tajweed/done", response_model=DoneOut)
async def done(body: DoneIn, user_id: int = Depends(require_user)) -> DoneOut:
    store = await get_store()
    if not await service.can_open(store, user_id, body.lesson_id):
        raise not_found("no such lesson")
    outcome = await service.complete(store, user_id, body.lesson_id)
    if outcome is None:
        return DoneOut(done=True, first_time=False)
    return DoneOut(done=True, first_time=True, streak=outcome.streak.current)


class ReviewIn(BaseModel):
    lesson_id: str = Field(min_length=1, max_length=64)
    approve: bool


class ReviewOut(BaseModel):
    approved: bool


@router.post("/tajweed/review", response_model=ReviewOut)
async def review(body: ReviewIn, user_id: int = Depends(require_user)) -> ReviewOut:
    if not service.is_reviewer(user_id):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "reviewers only")
    store = await get_store()
    if not await service.review(store, user_id, body.lesson_id, body.approve):
        raise not_found("nothing to review for this lesson")
    return ReviewOut(approved=body.approve)
