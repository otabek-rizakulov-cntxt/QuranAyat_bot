"""Tajweed lessons: who may see what, and marking lessons done (docs/TAJWEED_PLAN.md).

Shared by the bot (/tajvid) and the Mini App API, so both answer "can this user
open this lesson?" the same way:

- `alifbo` (the Muallimi soniy audio lessons) is open to everyone once the audio
  base URL is configured; until then the track does not exist.
- `qoidalar` (our own lessons) shows approved lessons to everyone and drafts to
  reviewers only. A lesson is approved while the stored hash equals its current
  content hash, so an edited lesson is a draft again.

Marking a lesson done counts as a `tajweed` streak session, once per lesson.
"""

from typing import Optional, Set

from config.settings import get_settings
from domain import tajweed_lessons
from domain.tajweed_lessons import TRACK_AUDIO, TRACK_RULES
from infra.store.sessions import KIND_TAJWEED
from services.streaks import SessionOutcome, record_session


def is_reviewer(user_id: int) -> bool:
    return user_id in get_settings().tajweed_reviewers


def audio_base() -> Optional[str]:
    """The R2 base URL of the lesson audio, or None while it is not configured."""
    return get_settings().tajweed_audio_base_url


async def approved_ids(store) -> Set[str]:
    """Rules lessons whose current text is the one a reviewer approved."""
    approvals = await store.tajweed.approvals()
    return {
        x.id
        for x in tajweed_lessons.lessons()
        if x.id in approvals and approvals[x.id].content_hash == x.content_hash
    }


async def can_open(store, user_id: int, lesson_id: str) -> bool:
    track = tajweed_lessons.track_of(lesson_id)
    if track == TRACK_AUDIO:
        return audio_base() is not None
    if track == TRACK_RULES:
        return is_reviewer(user_id) or lesson_id in await approved_ids(store)
    return False


async def visible_tracks(store, user_id: int) -> tuple:
    """The tracks this user has anything to open in, in display order."""
    tracks = []
    if audio_base() is not None:
        tracks.append(TRACK_AUDIO)
    if is_reviewer(user_id) or await approved_ids(store):
        tracks.append(TRACK_RULES)
    return tuple(tracks)


async def complete(store, user_id: int, lesson_id: str) -> Optional[SessionOutcome]:
    """Mark a lesson done. The first time, it logs a streak session and returns its
    outcome; marking it again returns None (one lesson counts once, so ✅ can't be
    tapped for a streak). The caller has already checked `can_open`."""
    if not await store.tajweed.mark_done(user_id, lesson_id):
        return None
    return await record_session(user_id, KIND_TAJWEED)
