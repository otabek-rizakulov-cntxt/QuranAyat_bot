"""Tajweed lessons: who may see what, and marking lessons done (docs/TAJWEED_PLAN.md).

Shared by the bot (/tajvid) and the Mini App API, so both answer "can this user
open this lesson?" the same way:

- `alifbo` (the Muallimi soniy audio lessons) is open to everyone once the audio
  base URL is configured; until then the track does not exist.
- `qoidalar` (our own lessons) shows approved lessons to everyone and drafts to
  reviewers only. A lesson is approved while the stored hash equals its current
  content hash, so an edited lesson is a draft again.

Marking a lesson done counts as a `tajweed` streak session, once per lesson.

Cards (P4): spaced repetition over domain.tajweed_cards. A card joins the user's deck
when a lesson that teaches it is done. Grades are 0 Bilmadim, 1 Qiyin, 2 Bildim.
Per day: every due card (not yet seen today) and up to NEW_PER_DAY new ones, at most
SESSION_MAX in all; finishing the day's cards counts a `tajweed` streak day.

Text tracking (P2): an audio lesson's lines and times are shown to everyone once a
reviewer approved them; the approval row (same table, id `ms-NNN`) holds the hash
of the timings, so re-aligning a lesson puts it back to draft.
"""

from dataclasses import replace
from datetime import date, timedelta
from typing import NamedTuple, Optional, Set

from config.settings import get_settings
from domain import tajweed_cards, tajweed_lessons
from domain.tajweed_lessons import TRACK_AUDIO, TRACK_RULES
from infra.store.sessions import KIND_TAJWEED
from infra.store.tajweed import CardRow
from services.streaks import SessionOutcome, record_session, user_today


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


async def tracking_ids(store) -> Set[str]:
    """Audio lessons whose current text tracking is the one a reviewer approved."""
    approvals = await store.tajweed.approvals()
    out = set()
    for x in tajweed_lessons.audio_lessons():
        row = approvals.get(x.id)
        if row is not None and row.content_hash == tajweed_lessons.timings_hash(x.id):
            out.add(x.id)
    return out


def review_hash(lesson_id: str) -> Optional[str]:
    """What approving this lesson pins: the timings of an audio lesson, the text of
    a rules lesson; None when there is nothing to review yet."""
    if tajweed_lessons.track_of(lesson_id) == TRACK_AUDIO:
        return tajweed_lessons.timings_hash(lesson_id)
    lesson = tajweed_lessons.lesson(lesson_id)
    return lesson.content_hash if lesson is not None else None


async def review(store, user_id: int, lesson_id: str, approve: bool) -> bool:
    """A reviewer approves (or withdraws) a lesson. False when not allowed or there
    is nothing to review."""
    content_hash = review_hash(lesson_id)
    if not is_reviewer(user_id) or content_hash is None:
        return False
    if approve:
        await store.tajweed.approve(lesson_id, content_hash, user_id)
    else:
        await store.tajweed.revoke(lesson_id)
    return True


async def finish_practice(store, user_id: int, lesson_id: str, correct: int, total: int):
    """A finished quiz or reading drill: keep the score, log a `tajweed` streak session.
    Returns (best_pct, outcome). The caller has already checked `can_open`."""
    total = max(1, total)
    pct = round(100 * max(0, min(correct, total)) / total)
    _, best = await store.tajweed.record_practice(user_id, lesson_id, pct)
    return best, await record_session(user_id, KIND_TAJWEED)


# --- spaced repetition (P4) ---------------------------------------------------------

NEW_PER_DAY = 5
SESSION_MAX = 25
MAX_INTERVAL = 365
GRADES = (0, 1, 2)  # Bilmadim, Qiyin, Bildim


class CardQueue(NamedTuple):
    next: Optional[str]  # the card to show now, or None: done for today
    due: int  # cards still due today (including `next`)
    new: int  # new cards still allowed today
    seen_today: int


def schedule(row: Optional[CardRow], card_id: str, grade: int, today: date) -> CardRow:
    """The card's next state after a grade. New: 0 -> again tomorrow's session (due
    today, but not shown twice a day), 1 -> 1 day, 2 -> 3 days. Seen before: 0 -> 1
    day (a lapse), 1 -> ×1.2, 2 -> ×2.5, at least one day more."""
    if row is None:
        interval = (0, 1, 3)[grade]
        return CardRow(card_id, interval, today + timedelta(interval), today, today, 1, 0)
    i = row.interval_days
    if grade == 0:
        interval, lapses = 1, row.lapses + 1
    elif grade == 1:
        interval, lapses = max(1, round(i * 1.2)), row.lapses
    else:
        interval, lapses = max(i + 1, round(i * 2.5)), row.lapses
    interval = min(interval, MAX_INTERVAL)
    return replace(
        row,
        interval_days=interval,
        due=today + timedelta(interval),
        last_seen=today,
        reps=row.reps + 1,
        lapses=lapses,
    )


async def card_queue(store, user_id: int, today: Optional[date] = None) -> CardQueue:
    today = today or await user_today(user_id)
    rows = await store.tajweed.cards(user_id)
    seen_today = sum(1 for r in rows.values() if r.last_seen == today)
    new_today = sum(1 for r in rows.values() if r.first_seen == today)
    room = max(0, SESSION_MAX - seen_today)
    due = sorted(
        (r for r in rows.values() if r.due <= today and r.last_seen < today),
        key=lambda r: (r.due, r.card_id),
    )
    unlocked = tajweed_cards.unlocked(await store.tajweed.done(user_id))
    fresh = [c.id for c in unlocked if c.id not in rows]
    new_left = min(max(0, NEW_PER_DAY - new_today), len(fresh), max(0, room - len(due)))
    queue = [r.card_id for r in due][:room] + fresh[:new_left]
    return CardQueue(queue[0] if queue else None, min(len(due), room), new_left, seen_today)


async def grade_card(store, user_id: int, card_id: str, grade: int, today: Optional[date] = None):
    """Grade one card. Returns (queue after it, streak outcome when that finished the
    day's cards, else None), or None if this card can't be graded now."""
    today = today or await user_today(user_id)
    if grade not in GRADES:
        return None
    queue = await card_queue(store, user_id, today)
    if queue.next != card_id:  # only the card on screen: no skipping ahead, no replays
        return None
    row = (await store.tajweed.cards(user_id)).get(card_id)
    await store.tajweed.save_card(user_id, schedule(row, card_id, grade, today))
    after = await card_queue(store, user_id, today)
    outcome = await record_session(user_id, KIND_TAJWEED) if after.next is None else None
    return after, outcome
