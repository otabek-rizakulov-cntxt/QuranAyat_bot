"""The reciter catalog (common/performers.json) and every CDN URL built from it."""

import os
from typing import List, Optional

import ujson as json

from config.settings import get_settings

DEFAULT_RECITER = "Husary_128kbps"
_PERFORMERS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common", "performers.json"
)
_performers: Optional[List[dict]] = None


def performers() -> List[dict]:
    """Every catalog entry, in catalog order. Parsed once per process."""
    global _performers
    if _performers is None:
        with open(_PERFORMERS_PATH, encoding="utf-8") as fp:
            _performers = json.load(fp)["performers"]
    return _performers


def find(subfolder: str) -> Optional[dict]:
    """The catalog entry for `subfolder`, or None if it isn't (or is no longer) there."""
    return next((p for p in performers() if p["subfolder"] == subfolder), None)


def performer_name(subfolder: str) -> str:
    """Display name for a performer, falling back to the default reciter's name
    when `subfolder` is unknown (e.g. a stale saved preference)."""
    entry = find(subfolder) or find(DEFAULT_RECITER)
    return entry["name"]


def search(query: str, limit: int = 8) -> List[dict]:
    """Case-insensitive search over performer names, for the reciter search flow.

    Every whitespace-separated term must appear in the name or the bitrate, so
    "sudais 192" narrows to the one entry at that quality instead of listing
    every Sudais recording. Returns up to `limit` matches, in catalog order.
    """
    terms = query.strip().lower().split()
    if not terms:
        return []
    matches = []
    for p in performers():
        haystack = (p["name"] + " " + p.get("bitrate", "")).lower()
        if all(term in haystack for term in terms):
            matches.append(p)
            if len(matches) == limit:
                break
    return matches


def has_page_audio(subfolder: str) -> bool:
    """Whether this recording has one-file-per-mushaf-page recitations.

    Recorded per entry in performers.json rather than probed at request time: a
    dozen entries in the catalog have no PageMp3s directory at all, and the page
    send needs to know *before* it picks between the single file and stitching
    the page's ayahs together.
    """
    entry = find(subfolder)
    return bool(entry and entry.get("page_audio"))


def audio_url(surah: int, ayah: int, performer: str = DEFAULT_RECITER) -> str:
    """URL of one ayah's recitation. Raises ValueError for a performer that is
    not in the catalog."""
    if find(performer) is None:
        raise ValueError(f"Unknown performer: {performer}")
    return (
        f"{get_settings().audio_base_url}/{performer}/{str(surah).zfill(3)}{str(ayah).zfill(3)}.mp3"
    )


def page_audio_url(page: int, performer: str) -> str:
    """URL of the reciter's single-file recitation of mushaf page `page`.

    Only meaningful when `has_page_audio(performer)`; callers stitch the page's
    ayah recitations together instead when it is False.
    """
    return f"{get_settings().audio_base_url}/{performer}/PageMp3s/Page{str(page).zfill(3)}.mp3"


def image_url(surah: int, ayah: int) -> str:
    """The rendered Arabic image of one ayah."""
    return "%s/%d_%d.png" % (get_settings().photo_base_url, surah, ayah)


def page_image_url(surah: int, ayah: int) -> str:
    """The per-ayah image the page stitcher tiles — same naming as `image_url`,
    but from the uniform-width set (see `Settings.page_image_base_url`)."""
    return "%s/%d_%d.png" % (get_settings().page_image_base_url, surah, ayah)
