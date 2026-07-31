# Local time for the hifz platform, expressed as a **fixed UTC offset** and
# nothing else.
#
# The streak day boundary, the daily push and the weekly leaderboard window all
# have to be local to the user (a UTC+5 audience would otherwise see their streak
# roll over at 05:00). The approved model is a fixed offset stored as TEXT on
# `user_profile.timezone` — e.g. "+05:00" — never an IANA zone name:
#
#   * no `tzdata` dependency and no per-platform zone database to ship,
#   * no DST branches, so "what date is it for this user" is one addition,
#   * a picker with ~30 entries is a single inline keyboard, where a zone list is
#     a search UI nobody asked for.
#
# The cost is that a user in a DST-observing country drifts by an hour twice a
# year and has to re-pick. That is a deliberate trade: an hour of drift moves a
# reminder, it never loses a streak day (the boundary moves with the offset, and
# both the session write and the day computation read the same stored offset).

import re
from datetime import date, datetime, time, timedelta, timezone
from typing import List, Tuple

__all__ = [
    "MIN_OFFSET_MINUTES", "MAX_OFFSET_MINUTES", "DEFAULT_OFFSET", "OFFSET_CHOICES",
    "parse_offset", "format_offset", "normalize_offset", "is_valid_offset",
    "local_now", "local_date", "local_time", "to_utc", "next_due_utc",
    "week_bounds", "offset_options",
]

# The real world runs from UTC-12:00 (Baker Island) to UTC+14:00 (Line Islands).
MIN_OFFSET_MINUTES = -12 * 60
MAX_OFFSET_MINUTES = 14 * 60

DEFAULT_OFFSET = "+00:00"

# Accepts "+05:00", "-03:30", "+0530", "+5", "UTC+5", "GMT-3:30", "Z", "UTC".
_OFFSET_RE = re.compile(
    r"""^\s*
        (?:(?:UTC|GMT)\s*)?          # optional prefix
        (?P<sign>[+\-−])?       # ASCII hyphen or Unicode minus
        (?P<hours>\d{1,2})
        (?:\s*:\s*|\s*)?             # ":" separator, or none for "+0530"
        (?P<minutes>\d{2})?
        \s*$""",
    re.IGNORECASE | re.VERBOSE,
)


def parse_offset(s: str) -> timedelta:
    """A stored/typed UTC offset as a timedelta.

    Accepts "+05:00", "-03:30", "+0530", "UTC+5", "Z"/"UTC" (zero). Raises
    ValueError on anything else, including offsets outside UTC-12:00..UTC+14:00
    and minute values that are not a real fraction of an hour.
    """
    if s is None:
        raise ValueError("offset is None")
    text = str(s).strip()
    if text.upper() in ("Z", "UTC", "GMT"):
        return timedelta(0)
    match = _OFFSET_RE.match(text)
    if match is None:
        raise ValueError("not a UTC offset: %r" % (s,))
    hours = int(match.group("hours"))
    minutes = int(match.group("minutes") or 0)
    if minutes >= 60:
        raise ValueError("minutes out of range in offset: %r" % (s,))
    total = hours * 60 + minutes
    if match.group("sign") in ("-", "−"):
        total = -total
    if not MIN_OFFSET_MINUTES <= total <= MAX_OFFSET_MINUTES:
        raise ValueError("offset out of range (-12:00..+14:00): %r" % (s,))
    return timedelta(minutes=total)


def format_offset(td: timedelta) -> str:
    """Canonical text form of an offset: "+05:00", "-03:30", "+00:00"."""
    total = int(round(td.total_seconds() / 60))
    if not MIN_OFFSET_MINUTES <= total <= MAX_OFFSET_MINUTES:
        raise ValueError("offset out of range (-12:00..+14:00): %r" % (td,))
    sign = "-" if total < 0 else "+"
    total = abs(total)
    return "%s%02d:%02d" % (sign, total // 60, total % 60)


def normalize_offset(s: str) -> str:
    """Round-trip an offset through parsing so storage only ever sees "+05:00"."""
    return format_offset(parse_offset(s))


def is_valid_offset(s: str) -> bool:
    """Whether `s` parses as a UTC offset — for validating typed input."""
    try:
        parse_offset(s)
    except (ValueError, TypeError):
        return False
    return True


def _as_utc(dt: datetime) -> datetime:
    """`dt` as an aware UTC datetime; a naive datetime is assumed to be UTC.

    The repository layer hands out aware UTC datetimes, but callers building a
    time by hand routinely produce naive ones, and mixing the two raises.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def local_now(utc_now: datetime, offset: str) -> datetime:
    """`utc_now` as a naive local wall-clock datetime for a user at `offset`."""
    return (_as_utc(utc_now) + parse_offset(offset)).replace(tzinfo=None)


def local_date(utc_now: datetime, offset: str) -> date:
    """The user's local calendar date at instant `utc_now`.

    This is the streak's unit: 23:59 and 00:01 local are two different dates even
    though they are two minutes apart (see G1's acceptance criterion).
    """
    return local_now(utc_now, offset).date()


def local_time(utc_now: datetime, offset: str) -> time:
    """The user's local wall-clock time at instant `utc_now`."""
    return local_now(utc_now, offset).time()


def to_utc(local_dt: datetime, offset: str) -> datetime:
    """A local wall-clock datetime as an aware UTC instant."""
    naive = local_dt.replace(tzinfo=None) if local_dt.tzinfo is not None else local_dt
    return (naive - parse_offset(offset)).replace(tzinfo=timezone.utc)


def next_due_utc(reminder_time: time, offset: str, after: datetime) -> datetime:
    """The first UTC instant strictly after `after` at which the user's local
    wall clock reads `reminder_time`.

    Strictly after, so re-scheduling immediately upon firing advances a day
    instead of re-firing the same instant forever.
    """
    delta = parse_offset(offset)
    after_utc = _as_utc(after)
    local = (after_utc + delta).replace(tzinfo=None)
    candidate = datetime.combine(local.date(), reminder_time)
    if candidate <= local:
        candidate = datetime.combine(local.date() + timedelta(days=1), reminder_time)
    return (candidate - delta).replace(tzinfo=timezone.utc)


def week_bounds(d: date) -> Tuple[date, date]:
    """The Monday→Sunday week containing `d`, inclusive on both ends.

    H1 defines the leaderboard window as Mon 00:00 → Sun 23:59 in the user's own
    timezone, so the window is computed from a *local* date and compared against
    `session_log.local_date` — no instants involved.
    """
    monday = d - timedelta(days=d.weekday())
    return monday, monday + timedelta(days=6)


# The offset picker. Not every quarter-hour offset in the world (Chatham's
# +12:45 and Nepal's +05:45 exist), but the spread people actually live at, kept
# short enough for one inline keyboard. Anyone outside it can still be stored at
# an exact offset — `parse_offset` accepts far more than this list offers.
_PICKER_MINUTES = (
    -12 * 60, -11 * 60, -10 * 60, -9 * 60, -8 * 60, -7 * 60, -6 * 60, -5 * 60,
    -4 * 60, -3 * 60 - 30, -3 * 60, -2 * 60, -1 * 60, 0,
    60, 2 * 60, 3 * 60, 3 * 60 + 30, 4 * 60, 4 * 60 + 30, 5 * 60, 5 * 60 + 30,
    5 * 60 + 45, 6 * 60, 6 * 60 + 30, 7 * 60, 8 * 60, 9 * 60, 9 * 60 + 30,
    10 * 60, 11 * 60, 12 * 60, 13 * 60, 14 * 60,
)

OFFSET_CHOICES: Tuple[str, ...] = tuple(
    format_offset(timedelta(minutes=m)) for m in _PICKER_MINUTES)


def offset_options() -> List[str]:
    """The UTC offsets the picker offers, ascending. Labels are the offsets
    themselves — they need no translation, which is half the reason for this
    model."""
    return list(OFFSET_CHOICES)
