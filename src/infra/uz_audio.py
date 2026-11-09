"""Uzbek translation audio: surah mp3s on newbooks.uz, cut into ayahs by HTTP Range.

docs/MULTILINGUAL_PLAN.md §8.1. Every file is constant-bitrate MPEG audio, so
frame `f` starts at byte `f * frame_bytes`. `data/uz_audio_timings.json`
(generated offline by scripts/uz_audio/) holds each ayah as
`[start_frame, end_frame)`, and a clip is one Range request. Audio is never
written anywhere: a fetched slice lives in a BytesIO until Telegram has it, and
from then on the bot replays Telegram's file_id.
"""

import asyncio
import os
from io import BytesIO
from typing import List, NamedTuple, Optional

import httpx
import ujson as json

_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "uz_audio_timings.json",
)
SOURCE_URL = "https://newbooks.uz/audio/t1/%03d.mp3"

# Telegram fetches a URL itself only up to 20 MB; bigger surahs go out in parts
# that we upload. Parts stay a little under so a part never trips the limit.
URL_SEND_LIMIT = 20_000_000
PART_LIMIT = 19_500_000

_FETCH_CONCURRENCY = 2  # slices pass through RAM; keep the 512 MB instance safe
_semaphore: Optional[asyncio.Semaphore] = None
_table: Optional[dict] = None


class Part(NamedTuple):
    index: int  # 1-based
    first_ayah: int
    last_ayah: int
    start_byte: int
    end_byte: int  # inclusive, as in a Range header


def _surahs() -> dict:
    global _table
    if _table is None:
        if os.path.exists(_PATH):
            with open(_PATH, encoding="utf-8") as fp:
                _table = json.load(fp)["surahs"]
        else:
            _table = {}
    return _table


def reset_for_tests(table: Optional[dict] = None) -> None:
    """Drop the cached table (or install `table`, the JSON's "surahs" object)."""
    global _table, _semaphore
    _table = table
    _semaphore = None


def entry(surah: int) -> Optional[dict]:
    return _surahs().get(str(surah))


def available(surah: int) -> bool:
    return entry(surah) is not None


def estimated(surah: int) -> bool:
    """Whether this surah's ayah cuts are automatic and not yet checked by ear."""
    e = entry(surah)
    return e is None or e.get("status") != "verified"


def version(surah: int) -> str:
    """Changes whenever this surah's timings change, so cached clips go stale with it."""
    e = entry(surah)
    return e.get("ver", "0") if e else "0"


def url(surah: int) -> str:
    return SOURCE_URL % surah


def size(surah: int) -> int:
    return entry(surah)["size"]


def byte_range(surah: int, first: int, last: int) -> tuple:
    """`(start, end_inclusive)` bytes of ayahs first..last in the surah's mp3."""
    e = entry(surah)
    ayahs = e["ayahs"]
    if not 1 <= first <= last <= len(ayahs):
        raise ValueError("ayahs %d-%d outside surah %d" % (first, last, surah))
    fb = e["frame_bytes"]
    return ayahs[first - 1][0] * fb, ayahs[last - 1][1] * fb - 1


def seconds(surah: int, first: int, last: int) -> tuple:
    """`(start, end)` seconds of ayahs first..last, as the Mini App seeks them."""
    e = entry(surah)
    frame_s = 1152 / e["sample_rate"]
    return e["ayahs"][first - 1][0] * frame_s, e["ayahs"][last - 1][1] * frame_s


def parts(surah: int) -> List[Part]:
    """The whole surah as Telegram-sized pieces that start and end on ayah boundaries.

    Part 1 starts at byte 0 (it keeps the spoken intro) and the last part runs to
    the end of the file, so the parts together are exactly the file."""
    e = entry(surah)
    fb, ayahs = e["frame_bytes"], e["ayahs"]
    out: List[Part] = []
    first, start = 1, 0
    for a in range(1, len(ayahs) + 1):
        end = e["size"] if a == len(ayahs) else ayahs[a - 1][1] * fb
        if end - start > PART_LIMIT and a > first:
            cut = ayahs[a - 2][1] * fb
            out.append(Part(len(out) + 1, first, a - 1, start, cut - 1))
            first, start = a, cut
    out.append(Part(len(out) + 1, first, len(ayahs), start, e["size"] - 1))
    return out


async def fetch(surah: int, start: int, end: int, name: str) -> BytesIO:
    """Bytes start..end (inclusive) of the surah's mp3, checked, in memory."""
    global _semaphore
    if _semaphore is None:
        _semaphore = asyncio.Semaphore(_FETCH_CONCURRENCY)
    async with _semaphore:
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
            response = await client.get(url(surah), headers={"Range": "bytes=%d-%d" % (start, end)})
    data = response.content
    if response.status_code != 206:
        raise OSError("newbooks.uz answered %d to a Range request" % response.status_code)
    if len(data) != end - start + 1:
        raise OSError("short Range response: %d of %d bytes" % (len(data), end - start + 1))
    if data[0] != 0xFF or (data[1] & 0xE0) != 0xE0:
        # the file changed upstream (re-encoded?) and our frame math no longer holds
        raise OSError("no MPEG frame at byte %d of surah %d" % (start, surah))
    buf = BytesIO(data)
    buf.name = name
    return buf
