# Tajweed lessons in the Mini App (docs/TAJWEED_PLAN.md): GET /tajweed, POST /tajweed/done,
# POST /tajweed/review (reviewers: approve a rules lesson or an audio lesson's text tracking),
# GET /tajweed/practice/{lesson} and POST /tajweed/practice (P3 quizzes and reading drills),
# GET /tajweed/cards and POST /tajweed/cards/grade (P4 spaced repetition).
#
# The lesson texts and the audio manifest are static content (export_web_content.py
# -> public/content/tajweed/{uz,uz-Cyrl}.json); this route adds what is per user or per
# deployment: where the audio lives, which rules lessons are approved, which lessons
# this user has done, and whether they review. Marking done is services.tajweed, the
# same code as the bot's ✅ button, so the streak counts it once either way.

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from domain import tajweed, tajweed_cards, tajweed_practice
from domain.uz_translit import to_cyrillic
from infra.store import get_store
from services import tajweed as service
from services.user_settings import UserSettings

from .auth import require_user
from .common import not_found

router = APIRouter()


class TajweedOut(BaseModel):
    audio_base: Optional[str]  # None: the audio lessons are not available yet
    approved: List[str]  # rules lessons everyone may open
    done: List[str]
    reviewer: bool  # may open drafts too
    tracking: List[str]  # audio lessons whose line-by-line text is approved
    practice: Dict[str, int]  # lesson -> best practice score, percent


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
        practice={k: best for k, (_, best) in (await store.tajweed.practice(user_id)).items()},
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


class TajweedAyahOut(BaseModel):
    surah: int
    ayah: int
    html: str  # the ayah, the asked-about spans in <u><b>


class TajweedQuestionOut(BaseModel):
    kind: str  # name | find | listen | count
    rule: str
    prompt_rule: str  # the rule's Uzbek name, in the user's script
    ayahs: List[TajweedAyahOut]
    options: List[str]
    answer: int
    audio: Optional[List[int]] = None  # [surah, ayah] to play first


class TajweedDrillOut(BaseModel):
    surah: int
    ayah: int
    word: str


class PracticeOut(BaseModel):
    seed: int
    quiz: List[TajweedQuestionOut]  # empty: this lesson has no annotated rule, drills only
    drill: List[TajweedDrillOut]


@router.get("/tajweed/practice/{lesson_id}", response_model=PracticeOut)
async def practice(
    lesson_id: str, seed: int = Query(ge=1, le=10**6), user_id: int = Depends(require_user)
) -> PracticeOut:
    """The same session the bot would build for this (lesson, seed). The answers are
    included: it's self-practice, and the app checks taps without a round trip."""
    store = await get_store()
    if not await service.can_open(store, user_id, lesson_id):
        raise not_found("no such lesson")
    cyrl = (await _ui_lang(user_id)) == "uz-Cyrl"
    script = to_cyrillic if cyrl else (lambda s: s)
    return PracticeOut(
        seed=seed,
        quiz=[
            TajweedQuestionOut(
                kind=q.kind,
                rule=q.rule,
                prompt_rule=script(tajweed.RULES[q.rule].name_uz),
                ayahs=[TajweedAyahOut(surah=s, ayah=a, html=h) for s, a, h in q.ayahs],
                options=[script(o) for o in q.options],
                answer=q.answer,
                audio=list(q.audio) if q.audio else None,
            )
            for q in tajweed_practice.quiz(lesson_id, seed)
        ],
        drill=[
            TajweedDrillOut(surah=d.surah, ayah=d.ayah, word=d.word)
            for d in tajweed_practice.drill(lesson_id, seed)
        ],
    )


async def _ui_lang(user_id: int) -> str:
    return (await UserSettings().get(user_id)).ui_lang


class PracticeIn(BaseModel):
    lesson_id: str = Field(min_length=1, max_length=64)
    kind: str = Field(pattern="^(quiz|drill)$")
    correct: int = Field(ge=0, le=50)
    total: int = Field(ge=1, le=50)


class PracticeDoneOut(BaseModel):
    best_pct: int
    streak: int


@router.post("/tajweed/practice", response_model=PracticeDoneOut)
async def practice_done(body: PracticeIn, user_id: int = Depends(require_user)) -> PracticeDoneOut:
    store = await get_store()
    if not await service.can_open(store, user_id, body.lesson_id):
        raise not_found("no such lesson")
    best, outcome = await service.finish_practice(
        store, user_id, body.lesson_id, min(body.correct, body.total), body.total
    )
    return PracticeDoneOut(best_pct=best, streak=outcome.streak.current)


class TajweedCardOut(BaseModel):
    id: str
    kind: str  # letter | sign | rule | rule_back | word
    front: str  # HTML (Arabic and/or Uzbek; <u><b>, <b> only)
    back: str
    ayah: Optional[List[int]] = None  # [surah, ayah] to play


class TajweedCardsOut(BaseModel):
    card: Optional[TajweedCardOut]  # null: nothing left today
    due: int
    new: int
    unlocked: int  # cards in the user's deck (0: no lesson done yet)
    streak: Optional[int] = None  # set when this grade finished the day's cards


class GradeIn(BaseModel):
    card_id: str = Field(min_length=1, max_length=64)
    grade: int = Field(ge=0, le=2)  # Bilmadim, Qiyin, Bildim


async def _cards_out(store, user_id: int, queue, streak=None) -> TajweedCardsOut:
    script = to_cyrillic if (await _ui_lang(user_id)) == "uz-Cyrl" else (lambda s: s)
    card = tajweed_cards.card(queue.next) if queue.next else None
    return TajweedCardsOut(
        card=TajweedCardOut(
            id=card.id,
            kind=card.kind,
            front=script(card.front),
            back=script(card.back),
            ayah=list(card.ayah) if card.ayah else None,
        )
        if card
        else None,
        due=queue.due,
        new=queue.new,
        unlocked=len(tajweed_cards.unlocked(await store.tajweed.done(user_id))),
        streak=streak,
    )


@router.get("/tajweed/cards", response_model=TajweedCardsOut)
async def cards(user_id: int = Depends(require_user)) -> TajweedCardsOut:
    store = await get_store()
    return await _cards_out(store, user_id, await service.card_queue(store, user_id))


@router.post("/tajweed/cards/grade", response_model=TajweedCardsOut)
async def grade(body: GradeIn, user_id: int = Depends(require_user)) -> TajweedCardsOut:
    """Grade the card on top; 409 if it isn't the one on top any more (another
    device, a double tap), with nothing changed."""
    store = await get_store()
    result = await service.grade_card(store, user_id, body.card_id, body.grade)
    if result is None:
        raise HTTPException(status.HTTP_409_CONFLICT, "not the card on top")
    queue, outcome = result
    return await _cards_out(store, user_id, queue, outcome.streak.current if outcome else None)
