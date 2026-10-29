"""Shared by the /memorize modules: the wizard's knobs, draft conversions, and
the plan operations under the names the handlers use. Not a feature module (the
leading underscore keeps router discovery away)."""

from typing import Optional

import services.plans as plans_service
from bot.features import Ctx
from bot.limits import MAX_RANGE_AYAHS
from domain.refs import Ref
from services.profile import as_time

# The plan operations live in services/plans.py, shared with the Mini App API;
# these names are what the handlers below (and the tests) know them by.
_as_time = as_time


_plan_ref = plans_service.plan_ref


_target_kind = plans_service.target_kind


_target_label = plans_service.target_label


_utcnow = plans_service.utcnow


_enqueue_next = plans_service.enqueue_next


_portion_for = plans_service.portion_for


_day_position = plans_service.day_position


# The one draft kind this feature owns. One kind rather than one per question:
# the seam routes free text on `kind`, but the *step* is what decides how to read
# a message, and keeping both in the draft means a step can be skipped (the
# timezone, when the profile already has one) without renaming anything.
WIZARD_KIND = "plan_setup"


STEP_TARGET = "target"  # which kind of target (buttons)


STEP_TARGET_TEXT = "target_text"  # the surah / juz / range itself (typed)


STEP_PACE = "pace"  # auto, a preset, or "type one"


STEP_PACE_TEXT = "pace_text"


STEP_DAYS = "days"


STEP_DAYS_CUSTOM = "days_custom"


STEP_TIMEZONE = "timezone"


STEP_REMINDER = "reminder"


STEP_PREVIEW = "preview"


# An explicit pace is bounded by what a single stitched recitation may carry —
# above `MAX_RANGE_AYAHS` a portion could not be sent as one audio file, which is
# D3's acceptance criterion.
PACE_MIN = 1


PACE_MAX = MAX_RANGE_AYAHS


# Preset paces. The labels are the numbers themselves, which need no translation.
PACE_CHOICES = (1, 2, 3, 5, 10)


# Preset reminder times, likewise label-free.
REMINDER_CHOICES = ("05:00", "07:00", "09:00", "12:00", "18:00", "21:00")


DAILY = (1, 2, 3, 4, 5, 6, 7)


WEEKDAYS = (1, 2, 3, 4, 5)


_DAY_KEYS = ("day_mon", "day_tue", "day_wed", "day_thu", "day_fri", "day_sat", "day_sun")


# A juz plan is ~100 rows and Telegram caps a message at 4096 characters, so the
# preview shows the first `PREVIEW_MAX_ROWS` and then says how many it withheld.
PREVIEW_MAX_ROWS = 30


# How a consolidation day is marked in the calendar and in the drill header, so a
# review day never reads as padding. Deliberately an emoji rather than a word:
# every string in this module comes from the frozen manifest, and the manifest
# has no key for "review day" (see docs/HIFZ_STRINGS_GAPS.md).
REVIEW_MARK = "🔁 "


def _ref_to_draft(ref: Ref) -> list:
    """A `Ref` as JSON the draft can hold (ujson has no dataclasses)."""
    return [ref.kind, ref.start_surah, ref.start_ayah, ref.end_surah, ref.end_ayah, ref.n]


def _ref_from_draft(data: dict) -> Optional[Ref]:
    """The draft's target back as a `Ref`, or None if it is missing or malformed."""
    raw = (data or {}).get("ref")
    try:
        kind, s1, a1, s2, a2, n = raw
        return Ref(str(kind), int(s1), int(a1), int(s2), int(a2), None if n is None else int(n))
    except (TypeError, ValueError):
        return None


async def _expired(ctx: Ctx) -> None:
    """The draft went away between two taps — say so instead of half-working.

    `Wizard.update` answers None when the 30-minute TTL has passed, and every
    call site has to handle it: the alternative is a wizard that appears to
    accept an answer and then previews nothing.
    """
    await ctx.answer()
    await ctx.reply(ctx.tr("wizard_cancelled"))
    ctx.wiz.clear(ctx.user_id)
