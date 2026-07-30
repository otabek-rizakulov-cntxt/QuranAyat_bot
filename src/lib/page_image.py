# BismillahBot -- Explore the Holy Qur'an on Telegram
#
# Assembling a mushaf page out of its per-ayah images.
#
# everyayah.com serves no full-page mushaf image — only per-ayah renderings — so a
# "page" is built here by concatenating each ayah's PNG vertically. The `quranpngs`
# set is the one used: every image in it is exactly 1500px wide, so the strips tile
# without padding. (`images_png` varies 115-700px wide and cannot be tiled.)
#
# The result is not a facsimile of a printed mushaf — the strips are rendered
# separately, so inter-ayah margins are uneven. What it is: one screen per page,
# which is what makes reading through the Qur'an possible at all.

import asyncio
from io import BytesIO

import httpx

# Telegram's sendPhoto limits. The width+height cap is the binding one here: at a
# 1500px width it holds the height under 8500, which also keeps the aspect ratio
# far inside the separate 20:1 limit, so only this one needs enforcing.
TELEGRAM_MAX_DIMENSION_SUM = 10000
# The documented upload cap is 10 MB; leave headroom rather than sit on the line.
TELEGRAM_MAX_BYTES = 8 * 1024 * 1024

JPEG_QUALITY = 88

# Same bound (and reasoning) as main._DOWNLOAD_CONCURRENCY: fast, but polite enough
# to the CDN not to get rate-limited.
_DOWNLOAD_CONCURRENCY = 4

# A stitch holds the whole decoded page in memory (~36 MB for a long one), so on a
# 512 MB instance they must not stack. Two at a time keeps a burst of /page requests
# from being the thing that runs the process out of memory.
_STITCH_CONCURRENCY = 2

# asyncio primitives bind to the first event loop they are awaited in, so a plain
# module-level semaphore would break the moment a second loop appeared (production
# has one loop for the process lifetime, but each test gets its own). Rebuild it
# whenever the running loop changes — see the same concern in config/postgres.py.
_stitch_semaphore = None
_stitch_semaphore_loop = None


def _semaphore() -> asyncio.Semaphore:
    global _stitch_semaphore, _stitch_semaphore_loop
    loop = asyncio.get_running_loop()
    if _stitch_semaphore is None or _stitch_semaphore_loop is not loop:
        _stitch_semaphore = asyncio.Semaphore(_STITCH_CONCURRENCY)
        _stitch_semaphore_loop = loop
    return _stitch_semaphore


def _fit_for_telegram(image):
    """Downscale `image` until Telegram will accept its dimensions."""
    width, height = image.size
    if width + height <= TELEGRAM_MAX_DIMENSION_SUM:
        return image
    from PIL import Image

    scale = TELEGRAM_MAX_DIMENSION_SUM / float(width + height)
    return image.resize((max(1, int(width * scale)), max(1, int(height * scale))),
                        Image.LANCZOS)


def stitch_images(blobs: list) -> BytesIO:
    """Concatenate encoded images vertically into one JPEG, top to bottom.

    Synchronous and free of I/O so it can be unit-tested directly and handed to a
    worker thread by `fetch_and_stitch`. JPEG rather than PNG: the sources are black
    text on white, where JPEG is several times smaller for no visible loss, and the
    size cap is the constraint that actually bites on a long page.

    Strips narrower than the widest are centred rather than left-aligned, so a
    short final ayah does not sit off to one side.
    """
    from PIL import Image

    if not blobs:
        raise ValueError("no images to stitch")

    images = [Image.open(BytesIO(b)) for b in blobs]
    width = max(im.width for im in images)
    canvas = Image.new("RGB", (width, sum(im.height for im in images)), "white")
    y = 0
    for im in images:
        rgba = im.convert("RGBA")           # sources are palette/RGBA with alpha
        canvas.paste(rgba, ((width - im.width) // 2, y), rgba)
        y += im.height

    canvas = _fit_for_telegram(canvas)

    # Re-encode at a lower quality if the page is still too heavy. Two steps is
    # plenty: a full page of text lands well under the cap even at quality 60.
    for quality in (JPEG_QUALITY, 70, 55):
        out = BytesIO()
        canvas.save(out, format="JPEG", quality=quality, optimize=True)
        if out.tell() <= TELEGRAM_MAX_BYTES:
            break
    out.seek(0)
    return out


async def fetch_and_stitch(urls: list, name: str = "page.jpg") -> BytesIO:
    """Download every ayah image of a page and stitch them into one upload.

    The Pillow work runs in a worker thread: it is CPU-bound and would otherwise
    stall the event loop (and every other user's update) for the duration.
    """
    async with _semaphore():
        limit = asyncio.Semaphore(_DOWNLOAD_CONCURRENCY)
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            async def fetch(url):
                async with limit:
                    response = await client.get(url)
                    response.raise_for_status()
                    return response.content

            blobs = await asyncio.gather(*(fetch(url) for url in urls))

        buf = await asyncio.to_thread(stitch_images, list(blobs))
    buf.name = name
    return buf
