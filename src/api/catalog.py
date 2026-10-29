# GET /catalog/reciters, GET /catalog/languages, and the reader position shared
# with the bot (GET/PUT /reader/position).

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from config.settings import get_settings
from infra import nav_state
from locales import LANGUAGES, UI_LANGUAGES
from modules import Quran, TranslationRegistry
from services.reciters import _KIND_WARNING_KEYS, RECITER_KINDS, reciter_catalog

from .auth import require_user

router = APIRouter()


class Reciter(BaseModel):
    subfolder: str
    name: str
    bitrate: str
    kind: str
    page_audio: bool
    # Locale key of the warning the bot shows when this entry is chosen (riwayah
    # and translation audio), or None for ordinary recitation.
    warning_key: Optional[str] = None


class RecitersOut(BaseModel):
    kinds: List[str]
    # Per-ayah mp3 is {audio_base_url}/{subfolder}/{SSS}{AAA}.mp3; page mp3 (when
    # page_audio) is {audio_base_url}/{subfolder}/PageMp3s/Page{PPP}.mp3.
    audio_base_url: str
    reciters: List[Reciter]


@router.get("/catalog/reciters", response_model=RecitersOut)
async def reciters(_: int = Depends(require_user)) -> RecitersOut:
    """All reciters in the bot's picker order (shortlist first)."""
    return RecitersOut(
        kinds=list(RECITER_KINDS),
        audio_base_url=(get_settings().audio_base_url or "").rstrip("/"),
        reciters=[
            Reciter(
                subfolder=p["subfolder"],
                name=p["name"],
                bitrate=p.get("bitrate", ""),
                kind=p.get("kind", RECITER_KINDS[0]),
                page_audio=bool(p.get("page_audio")),
                warning_key=_KIND_WARNING_KEYS.get(p.get("kind", RECITER_KINDS[0])),
            )
            for p in reciter_catalog()
        ],
    )


class LanguageOut(BaseModel):
    code: str
    native: str
    english: str
    rtl: bool
    flag: str


class LanguagesOut(BaseModel):
    ui: List[LanguageOut]
    translation: List[LanguageOut]


def _lang(lang) -> LanguageOut:
    return LanguageOut(
        code=lang.code, native=lang.native, english=lang.english, rtl=lang.rtl, flag=lang.flag
    )


@router.get("/catalog/languages", response_model=LanguagesOut)
async def languages(_: int = Depends(require_user)) -> LanguagesOut:
    """The /language and /translation pickers' choices, in picker order."""
    available = TranslationRegistry.available()
    return LanguagesOut(
        ui=[_lang(lang) for lang in UI_LANGUAGES],
        translation=[_lang(lang) for lang in LANGUAGES if lang.code in available],
    )


# The bot's reader views. Its next/previous buttons continue from this position.
_READER_TYPES = ("translation", "arabic", "tafsir", "audio")


class ReaderPosition(BaseModel):
    surah: int
    ayah: int
    type: str = "translation"


@router.get("/reader/position", response_model=Optional[ReaderPosition])
async def get_position(user_id: int = Depends(require_user)) -> Optional[ReaderPosition]:
    """Where the user last read — in the bot or the app. Null if they never have."""
    state = await nav_state.get(user_id)
    if not state:
        return None
    try:
        surah, ayah, kind = int(state[0]), int(state[1]), str(state[2])
    except (TypeError, ValueError, IndexError):
        return None
    if not Quran.exists(surah, ayah):
        return None
    return ReaderPosition(
        surah=surah, ayah=ayah, type=kind if kind in _READER_TYPES else "translation"
    )


@router.put("/reader/position", response_model=ReaderPosition)
async def put_position(
    body: ReaderPosition, user_id: int = Depends(require_user)
) -> ReaderPosition:
    """Save the position where the bot's next/previous read it."""
    if not Quran.exists(body.surah, body.ayah) or body.type not in _READER_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid position"
        )
    await nav_state.save(user_id, body.surah, body.ayah, body.type)
    return body
