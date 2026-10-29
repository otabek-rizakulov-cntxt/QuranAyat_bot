"""Recitation audio from the CDN: fetch ayah mp3s and join them into one file."""

import asyncio
from io import BytesIO

import httpx

from infra import catalog

# Cap simultaneous CDN connections: fast, but polite enough to avoid rate-limiting/blocks.
_DOWNLOAD_CONCURRENCY = 4


async def download_stitched_audio(ayahs: list, performer: str, name: str) -> BytesIO:
    """Fetch each ayah's mp3 from the CDN (with bounded concurrency) and concatenate.

    Takes an explicit list of (surah, ayah) pairs rather than one surah's range,
    because a mushaf page is also assembled this way and 96 of the 604 pages cross
    a surah boundary.
    """
    urls = [catalog.audio_url(surah, ayah, performer) for surah, ayah in ayahs]
    semaphore = asyncio.Semaphore(_DOWNLOAD_CONCURRENCY)

    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:

        async def fetch(url):
            async with semaphore:
                response = await client.get(url)
                response.raise_for_status()
                return response.content

        chunks = await asyncio.gather(*(fetch(url) for url in urls))

    buf = BytesIO()
    for chunk in chunks:  # gather preserves order, so ayahs stay in sequence
        buf.write(chunk)
    buf.seek(0)
    buf.name = name
    return buf


async def download_combined_audio(surah: int, start: int, end: int, performer: str) -> BytesIO:
    """One surah's ayah range, stitched into a single mp3."""
    return await download_stitched_audio(
        [(surah, ayah) for ayah in range(start, end + 1)],
        performer,
        "quran_%d_%d-%d.mp3" % (surah, start, end),
    )
