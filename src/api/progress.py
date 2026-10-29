# Progress: GET /progress, GET /progress/surah/{n}, POST /progress/forget.
# Everything is derived by domain.hifz_progress from the interval store — the same
# numbers /progress shows in chat.

from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from domain.hifz_progress import surah_progress
from domain.quran import Quran
from infra.store import get_store
from services import progress as progress_service
from services.progress import load_summary

from .auth import require_user
from .common import RefOut, not_found, parse_ref_or_422, ref_out

router = APIRouter()


class Ratio(BaseModel):
    done: int
    total: int
    percent: float
    percent_text: str


class SurahRatio(Ratio):
    surah: int
    name: str


class JuzRatio(Ratio):
    juz: int


class ProgressOut(BaseModel):
    is_empty: bool
    quran: Ratio
    quran_pages_percent_text: Optional[str] = None
    focus: Optional[SurahRatio] = None
    focus_juz: Optional[JuzRatio] = None
    focus_juz_pages_percent_text: Optional[str] = None
    surahs: List[SurahRatio]
    juzs: List[JuzRatio]


def _ratio(r) -> dict:
    return dict(done=r.done, total=r.total, percent=r.percent, percent_text=r.percent_text)


def _surah(r) -> SurahRatio:
    return SurahRatio(surah=r.surah, name=Quran.get_surah_name(r.surah), **_ratio(r))


def _juz(r) -> JuzRatio:
    return JuzRatio(juz=r.juz, **_ratio(r))


async def _summary(user_id: int, focus: Optional[int] = None) -> ProgressOut:
    s = await load_summary(await get_store(), user_id, focus)
    return ProgressOut(
        is_empty=s.is_empty,
        quran=Ratio(**_ratio(s.quran)),
        quran_pages_percent_text=s.quran_pages.percent_text if s.quran_pages else None,
        focus=_surah(s.focus) if s.focus is not None else None,
        focus_juz=_juz(s.focus_juz) if s.focus_juz is not None else None,
        focus_juz_pages_percent_text=s.focus_juz_pages.percent_text if s.focus_juz_pages else None,
        surahs=[_surah(r) for r in s.surahs],
        juzs=[_juz(r) for r in s.juzs],
    )


@router.get("/progress", response_model=ProgressOut)
async def progress(
    focus: Optional[int] = None, user_id: int = Depends(require_user)
) -> ProgressOut:
    """The /progress summary; `focus` picks the headline surah (default: the
    most recently marked one)."""
    if focus is not None and not 1 <= focus <= 114:
        raise not_found("no such surah")
    return await _summary(user_id, focus)


class Span(BaseModel):
    start_ayah: int
    end_ayah: int


class SurahDetailOut(SurahRatio):
    memorized: List[Span]


@router.get("/progress/surah/{n}", response_model=SurahDetailOut)
async def surah_detail(n: int, user_id: int = Depends(require_user)) -> SurahDetailOut:
    """One surah: its percentage and exactly which ayahs are marked."""
    if not 1 <= n <= 114:
        raise not_found("no such surah")
    store = await get_store()
    intervals = await store.hifz.list_intervals(user_id, n)
    r = surah_progress(intervals, n)
    return SurahDetailOut(
        surah=n,
        name=Quran.get_surah_name(n),
        **_ratio(r),
        memorized=[
            Span(start_ayah=i.start_ayah, end_ayah=i.end_ayah)
            for i in sorted(intervals, key=lambda i: i.start_ayah)
        ],
    )


class ForgetIn(BaseModel):
    ref: str


class ForgetOut(BaseModel):
    removed: bool
    ref: RefOut
    progress: ProgressOut


@router.post("/progress/forget", response_model=ForgetOut)
async def forget(body: ForgetIn, user_id: int = Depends(require_user)) -> ForgetOut:
    """/forgot: unmark a range, splitting stored intervals as needed. Answers the
    updated numbers, since this is the one moment a percentage goes down."""
    ref = parse_ref_or_422(body.ref)
    removed = await progress_service.unmark(await get_store(), user_id, ref)
    return ForgetOut(
        removed=removed, ref=ref_out(ref), progress=await _summary(user_id, ref.start_surah)
    )
