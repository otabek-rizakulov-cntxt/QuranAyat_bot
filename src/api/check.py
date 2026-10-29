# Recall check: GET /check/question, POST /check/answer.
#
# Integrity (docs/MINI_APP_PLAN.md §5): the question response never contains the
# correct index. `question_token` is an HMAC-signed (user, surah, ayah, date);
# the answer route verifies it and rebuilds the question — deterministic per
# (user, ayah, date) — to score the choice. A token cannot be forged to pick an
# easier ayah, replayed by another user, or used to reroll the day's question.

import base64
import hashlib
import hmac
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from lib.store import get_store
from lib.streaks import user_today
from services import check as check_service

from .auth import jwt_secret, require_user
from .common import RefOut, parse_ref_or_422, ref_out

router = APIRouter()


def _sign(payload: str, secret: str) -> str:
    return (
        base64.urlsafe_b64encode(
            hmac.new(secret.encode(), ("check:" + payload).encode(), hashlib.sha256).digest()[:18]
        )
        .decode()
        .rstrip("=")
    )


def make_token(user_id: int, surah: int, ayah: int, day: date, secret: str) -> str:
    payload = "%d.%d.%d.%s" % (user_id, surah, ayah, day.strftime("%Y%m%d"))
    return payload + "." + _sign(payload, secret)


def read_token(token: str, user_id: int, secret: str):
    """(surah, ayah, date) from a token this user was issued, else None."""
    try:
        uid, surah, ayah, day, sig = token.split(".")
        payload = "%s.%s.%s.%s" % (uid, surah, ayah, day)
        if not hmac.compare_digest(_sign(payload, secret), sig) or int(uid) != user_id:
            return None
        return int(surah), int(ayah), date(int(day[:4]), int(day[4:6]), int(day[6:8]))
    except (ValueError, AttributeError):
        return None


def _secret() -> str:
    secret = jwt_secret()
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="mini app auth is not configured",
        )
    return secret


class QuestionOut(BaseModel):
    question_token: str
    prompt: str
    options: List[str]
    span: RefOut
    guessed_span: bool = Field(
        description="No reference given and nothing memorized: fell back to juz 30"
    )


@router.get("/check/question", response_model=QuestionOut)
async def question(
    ref: Optional[str] = Query(None, description='"67", "juz 30", "67:1-8"'),
    user_id: int = Depends(require_user),
) -> QuestionOut:
    """Today's question for `ref`, or — with no `ref` — for what the user is
    memorizing (the part of their plan they have reached, else something marked
    known, else juz 30). Asking again today returns the same question."""
    today = await user_today(user_id)
    if ref:
        span, guessed = parse_ref_or_422(ref), False
    else:
        span, guessed = await check_service.default_span(await get_store(), user_id, today)
    q = await check_service.ask(user_id, span, today)
    if q is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="nothing to test in that span"
        )
    return QuestionOut(
        question_token=make_token(user_id, q.surah, q.ayah, today, _secret()),
        prompt=q.prompt,
        options=list(q.options),
        span=ref_out(span),
        guessed_span=guessed,
    )


class AnswerIn(BaseModel):
    question_token: str
    choice: int = Field(ge=0)


class AnswerOut(BaseModel):
    correct: bool
    correct_index: int
    correct_option: str
    surah: int
    ayah: int
    already_today: bool = Field(description="A pass, but today was already earned")
    milestone_key: Optional[str] = Field(
        None, description="Locale key of a streak milestone reached"
    )


@router.post("/check/answer", response_model=AnswerOut)
async def answer(body: AnswerIn, user_id: int = Depends(require_user)) -> AnswerOut:
    """Score an answer. A pass logs today's recall-check session (once a day,
    shared with /check in chat) and may reach a streak milestone."""
    parsed = read_token(body.question_token, user_id, _secret())
    if parsed is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid question_token"
        )
    surah, ayah, day = parsed
    q = await check_service.rebuild(user_id, surah, ayah, day)
    if q is None or body.choice >= len(q.options):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid choice"
        )
    scored = await check_service.score(user_id, q, body.choice)
    return AnswerOut(
        correct=scored.correct,
        correct_index=q.correct_index,
        correct_option=scored.correct_option,
        surah=surah,
        ayah=ayah,
        already_today=scored.correct and not scored.logged,
        milestone_key=scored.milestone_key,
    )
