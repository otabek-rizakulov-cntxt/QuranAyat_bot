"""GET /media/range.mp3 — a stitched recitation for Telegram to fetch."""

import logging

import httpx
from fastapi import APIRouter, Response

from bot.limits import MAX_RANGE_AYAHS
from bot.media import RANGE_AUDIO_PATH
from domain.quran import Quran
from infra import audio as cdn_audio

logger = logging.getLogger(__name__)


router = APIRouter()


@router.get(RANGE_AUDIO_PATH)
async def range_audio(surah: int, start: int, end: int, reciter: str):
    """Serve a range of ayahs as one mp3, for Telegram to fetch when someone picks
    the combined recitation from an inline answer (see `inline_audio_result`).

    Public by necessity — Telegram cannot authenticate — so every parameter is
    validated and the range is bounded, leaving nothing here but Qur'an audio the
    bot would have sent anyway.
    """
    if not (Quran.exists(surah, start) and Quran.exists(surah, end)):
        return Response(status_code=404)
    if start > end or end - start + 1 > MAX_RANGE_AYAHS:
        return Response(status_code=404)
    try:
        audio = await cdn_audio.download_combined_audio(surah, start, end, reciter)
    except ValueError:  # reciter is not in the catalog
        return Response(status_code=404)
    except httpx.HTTPError as e:  # the recitation CDN is unreachable
        logger.error("range_audio: upstream fetch failed: %s: %s", type(e).__name__, e)
        return Response(status_code=502)
    return Response(
        content=audio.getvalue(),
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": 'inline; filename="%s"' % audio.name,
            "Cache-Control": "public, max-age=86400",
        },
    )
