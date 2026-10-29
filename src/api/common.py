# Shapes and helpers shared by the /api/v1 route modules.

from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel

from hifz.refs import Ref, format_ref, parse_reference
from modules import Quran


class RefOut(BaseModel):
    """A span of the Qur'an, as both numbers and the compact label ("67:1-12")."""
    kind: str
    start_surah: int
    start_ayah: int
    end_surah: int
    end_ayah: int
    n: Optional[int] = None
    label: str


def ref_out(ref: Ref) -> RefOut:
    return RefOut(kind=ref.kind, start_surah=ref.start_surah, start_ayah=ref.start_ayah,
                  end_surah=ref.end_surah, end_ayah=ref.end_ayah, n=ref.n,
                  label=format_ref(ref))


def parse_ref_or_422(text: str) -> Ref:
    """A reference the bot would accept ("67", "juz 30", "67:1-10", "page 562"),
    or a 422 — the same parser as /memorize, /check and /forgot."""
    ref = parse_reference(text or "")
    if ref is None or ref.count() <= 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid reference")
    return ref


def not_found(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def surah_name(n: int) -> str:
    return Quran.get_surah_name(n)
