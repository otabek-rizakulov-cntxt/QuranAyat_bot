# Profile operations (spec items B1-B3): display name, leaderboard opt-in,
# timezone (a fixed UTC offset) and the daily reminder time. Used by /profile
# (hifz/profile.py), the plan wizard and the Mini App's PATCH /me/profile.

import re
from datetime import datetime, time, timezone
from typing import Optional

from domain.localtime import is_valid_offset, next_due_utc, normalize_offset
from domain.quran import Quran
from domain.refs import KIND_RANGE, Ref, format_ref
from lib.store.plans import DAY_COMPLETED

NAME_MIN = 2
NAME_MAX = 32


# --- Display names -------------------------------------------------------------


def valid_display_name(text: str) -> Optional[str]:
    """The cleaned display name, or None if it is not 2-32 characters.

    Whitespace is collapsed rather than rejected: someone typing "Abu   Bakr" or
    pasting a name with a trailing newline meant the name, not an error. What is
    stored is the *raw* text — escaping happens at render time, because storing
    escaped text would double-escape it the next time it is shown.
    """
    name = " ".join((text or "").split())
    if not NAME_MIN <= len(name) <= NAME_MAX:
        return None
    return name


async def set_display_name(store, user_id: int, name: str):
    return await store.profiles.set_display_name(user_id, name)


async def join_leaderboard(store, user_id: int, fallback_name: Optional[str]) -> bool:
    """Opt in, naming the user `fallback_name` (their @username) if they have no
    display name yet. False — and nothing written — when there is no name to
    show: nobody is put on a public board under a blank label."""
    profile = await store.profiles.ensure_profile(user_id)
    name = profile.display_name or fallback_name
    if not name:
        return False
    if not profile.display_name:
        await store.profiles.set_display_name(user_id, name)
    await store.profiles.set_leaderboard_opt_in(user_id, True)
    return True


async def leave_leaderboard(store, user_id: int):
    return await store.profiles.set_leaderboard_opt_in(user_id, False)


# --- Timezone (B3) -------------------------------------------------------------


async def save_timezone(store, user_id: int, offset: str):
    """Store the user's fixed UTC offset, normalized to "+05:00" form.

    Returns the updated `ProfileRow` (created if this is their first write).
    Raises ValueError if `offset` is not a UTC offset — validate a tap with
    `hifz.profile.offset_from_callback` and typed text with
    `domain.localtime.is_valid_offset`.
    """
    return await store.profiles.set_timezone(user_id, normalize_offset(offset))


# --- Reminder time (B3) --------------------------------------------------------

# "07:30", "7:30", "0730", "730", "7", "7.30", "7h30". 12-hour input is not
# accepted: `reminder_prompt` asks for 24-hour form in all 48 languages, and
# guessing at an unqualified "7" being the evening is worse than a re-prompt.
_TIME_RE = re.compile(
    r"^(?P<h>\d{1,2})\s*(?:[:.,;h\-]\s*(?P<m>\d{1,2})|(?P<m2>\d{2}))?$", re.IGNORECASE
)


def parse_reminder_time(text: str) -> Optional[time]:
    """A typed 24-hour time as a `datetime.time`, or None if it does not parse."""
    cleaned = (text or "").strip()
    if not cleaned:
        return None
    match = _TIME_RE.match(cleaned)
    if match is None:
        return None
    hour = int(match.group("h"))
    minute = int(match.group("m") or match.group("m2") or 0)
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    return time(hour=hour, minute=minute)


def format_reminder_time(value: Optional[time]) -> str:
    """A stored reminder time as the "07:30" token a `{time}` placeholder wants."""
    if value is None:
        return ""
    return "%02d:%02d" % (value.hour, value.minute)


def as_time(value) -> Optional[time]:
    """A stored reminder time as a `datetime.time`, whatever shape it arrived in.

    Postgres hands back a `time`; a wizard draft carries the same value as
    "07:30" text, because a draft is JSON.
    """
    if value is None or isinstance(value, time):
        return value
    return parse_reminder_time(str(value))


async def save_reminder_time(store, user_id: int, value: Optional[time]):
    """Store (or clear, with None) the local time of day for the daily push."""
    return await store.profiles.set_reminder_time(user_id, value)


def next_push_utc(profile, now: Optional[datetime] = None) -> Optional[datetime]:
    """When this profile's next daily push is due, in UTC — or None if it has no
    reminder time.

    The scheduler queues each day's push from the profile as it stands, so this
    is the falsifiable half of B3: change the timezone and the instant moves by
    exactly the difference between the two offsets, with no row to migrate.
    """
    reminder = getattr(profile, "reminder_time", None)
    if reminder is None:
        return None
    offset = getattr(profile, "timezone", None) or "+00:00"
    if not is_valid_offset(offset):
        offset = "+00:00"
    return next_due_utc(reminder, offset, now or datetime.now(timezone.utc))


# --- The active plan, as the profile card shows it ------------------------------


def plan_target(plan) -> str:
    """What to call the plan's target: a surah name when it is a whole surah,
    otherwise the compact reference. Both are un-localized by design — a surah
    name is a proper noun and `format_ref` is machine text."""
    whole_surah = (
        plan.start_surah == plan.end_surah
        and plan.start_ayah == 1
        and plan.end_ayah == Quran.get_surah_length(plan.start_surah)
    )
    if plan.target_kind == "surah" or whole_surah:
        return Quran.get_surah_name(plan.start_surah)
    return format_ref(
        Ref(KIND_RANGE, plan.start_surah, plan.start_ayah, plan.end_surah, plan.end_ayah)
    )


async def active_plan_progress(store, user_id: int):
    """(plan, day, total) for the user's active plan, or None. `day` is the
    portion they are on: one past the completed count, capped at the total."""
    plan = await store.plans.get_active_plan(user_id)
    if plan is None:
        return None
    total = await store.plans.count_plan_days(plan.id)
    done = await store.plans.count_plan_days(plan.id, DAY_COMPLETED)
    day = min(done + 1, total) if total else 0
    return plan, day, total
