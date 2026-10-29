"""Putting a send in the queue, at most once per target and local day (F2)."""

from datetime import date, datetime, time
from typing import Any, Dict, Optional

from domain.localtime import local_date, next_due_utc
from infra.scheduler.tick import _utcnow
from infra.store.schedule import ScheduledSend


def idempotency_key(kind: str, target_chat_id: int, local_day) -> str:
    """The canonical `(kind, target, local_date)` key, e.g. `plan_day:42:2026-08-01`.

    The uniqueness of this string is the entire duplicate-send defence, so it is
    built in one place rather than formatted at each call site. `local_day` may
    be a `date` or an ISO string.
    """
    day = local_day.isoformat() if isinstance(local_day, date) else str(local_day)
    return "%s:%d:%s" % (kind, target_chat_id, day)


async def enqueue(
    store,
    kind: str,
    target_chat_id: int,
    due_at: datetime,
    local_day=None,
    payload: Optional[Dict[str, Any]] = None,
    thread_id: Optional[int] = None,
    key: Optional[str] = None,
) -> Optional[ScheduledSend]:
    """Queue one send. Returns the row, or None if that key is already queued.

    Enqueueing the same key twice inserts one row and raises nothing — that is
    F2, and it is what makes a double boot or a re-run of the day's scheduling
    pass harmless. Pass either `local_day` (the key is derived) or an explicit
    `key`.
    """
    if key is None:
        if local_day is None:
            raise ValueError("enqueue needs either local_day or an explicit key")
        key = idempotency_key(kind, target_chat_id, local_day)
    return await store.schedule.enqueue(
        kind, target_chat_id, due_at, key, payload=payload, thread_id=thread_id
    )


async def schedule_daily(
    store,
    kind: str,
    target_chat_id: int,
    reminder_time: time,
    offset: str,
    now: Optional[datetime] = None,
    payload: Optional[Dict[str, Any]] = None,
    thread_id: Optional[int] = None,
) -> Optional[ScheduledSend]:
    """Queue the next occurrence of a daily push at the user's local `reminder_time`.

    `offset` is a fixed UTC offset (`"+05:00"`); all the arithmetic goes through
    `domain.localtime`, never through hand-rolled timedeltas. The due instant is the
    first one strictly after `now` at which the recipient's wall clock reads
    `reminder_time`, and the key is keyed on the *local* date of that instant —
    so scheduling twice in the same local day is a no-op, and the row for
    tomorrow can be queued the moment today's fires.

    The recipient's offset is copied into the payload (unless the caller already
    put one there) because staleness is a local-day question: see `_is_stale`.
    """
    now = _utcnow(now)
    due_at = next_due_utc(reminder_time, offset, now)
    day = local_date(due_at, offset)
    body = dict(payload or {})
    body.setdefault("offset", offset)
    return await enqueue(
        store, kind, target_chat_id, due_at, local_day=day, payload=body, thread_id=thread_id
    )
