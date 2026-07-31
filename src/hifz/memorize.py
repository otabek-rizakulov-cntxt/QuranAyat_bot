# Workstream D — plans & drills (spec items D1, D3-D5).
#
# Owns: /memorize (the setup wizard: target -> pace -> days -> preview ->
# confirm), drill delivery, the "I know this by heart" button, and the plan
# lifecycle (pause / resume / abandon / complete).
# Callback prefix: "hm:" (see hifz.PREFIXES). Wizard kinds: prefix them "plan_".
#
# Drill delivery reuses `main.send_quran` (module level since Wave 0b, so the
# scheduler can call it too) and `main.send_combined_audio`.
#
# Four properties are load-bearing here, and each has a test named after it:
#
#   D1  **the preview is the plan.** `lib.plan_builder.build_plan` is pure, so
#       the preview calendar and the rows written by `create_plan` are the same
#       function call over the same arguments — the start date the preview used
#       is stashed in the draft so confirming ten minutes later still reproduces
#       it date for date, rather than "today" having quietly moved on.
#   D3  **one stitched audio per portion**, never one file per ayah:
#       `send_combined_audio` for a range, `send_quran` for a single ayah.
#   D4  **the double tap is guarded by a conditional write.**
#       `complete_plan_day` returns the row once and None afterwards, so it is
#       taken *first* and everything else — the interval, the session, the
#       streak — happens only on the branch that won it.
#   D5  **a paused plan pushes nothing.** There is no "cancel a queued send" in
#       the schedule repository (by design: a queued row is keyed on a local
#       day, not on a plan), so the pause is enforced where it cannot be missed:
#       `push_plan_day` re-reads the plan and returns without delivering unless
#       it is still active. Returning rather than raising marks the row 'sent',
#       and the chain simply stops until the user resumes.
#
# **The enqueue chain.** The scheduler (workstream F) only drains the queue;
# nothing in it ever fills the queue, which is this module's job. Exactly three
# things put a row in it, and all three go through `_enqueue_next`:
#
#     saving a plan            -> the first portion's push
#     a push firing            -> the following portion's push
#     resuming a paused plan   -> the next pending portion's push
#
# plus a belt-and-braces call after a portion is marked known, which is a no-op
# whenever the push that fired already queued the same day (`enqueue` answers
# None on a key clash instead of raising — that is the whole point of F2).
#
# The key is `plan_day:<chat_id>:<local date the push is due>`, so two portions
# can never collide on one day and a restart between enqueue and due time
# re-delivers nothing: the row is already there, and `claim_plan_day` is a
# conditional write on top of that.

import html
from datetime import date, datetime, time, timezone
from typing import Optional, Sequence

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from hifz import Ctx, callback, command, wizard
from hifz.profile import format_reminder_time, offset_from_callback, offset_keyboard, \
    parse_reminder_time, reminder_keyboard, save_reminder_time, save_timezone
from hifz.refs import KIND_JUZ, KIND_RANGE, KIND_SURAH, Ref, format_ref, juz_ref, \
    parse_reference, surah_ref
from lib.hifz_progress import load_summary
from lib.localtime import DEFAULT_OFFSET, OFFSET_CHOICES, is_valid_offset, \
    local_date, next_due_utc, normalize_offset, to_utc
from lib.plan_builder import AUTO_PACE, Portion, advancing, build_plan, to_day_specs
from lib.scheduler import SendCtx, enqueue, send_handler
from lib.store.plans import DAY_COMPLETED, DAY_PENDING, PLAN_ACTIVE, PLAN_COMPLETE, \
    PLAN_PAUSED
from lib.store.sessions import KIND_DRILL
from lib.streaks import record_session
from lib.user_settings import DEFAULT_RECITER, DEFAULT_TRANSLATION_LANG, DEFAULT_UI_LANG
from locales import t
from main import MAX_RANGE_AYAHS, REPEAT_COUNT, get_translation, send_combined_audio, \
    send_quran
from modules import Quran

__all__ = ["memorize", "on_tap", "plan_step", "push_plan_day", "SEND_KIND", "WIZARD_KIND"]


# --- Knobs ---------------------------------------------------------------------

# The one draft kind this feature owns. One kind rather than one per question:
# the seam routes free text on `kind`, but the *step* is what decides how to read
# a message, and keeping both in the draft means a step can be skipped (the
# timezone, when the profile already has one) without renaming anything.
WIZARD_KIND = "plan_setup"

# The scheduled-send kind. `lib.scheduler` dispatches on it; nothing else uses it.
SEND_KIND = "plan_day"

STEP_TARGET = "target"          # which kind of target (buttons)
STEP_TARGET_TEXT = "target_text"  # the surah / juz / range itself (typed)
STEP_PACE = "pace"              # auto, a preset, or "type one"
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


# --- Small conversions ---------------------------------------------------------

def _as_time(value) -> Optional[time]:
    """A stored reminder time as a `datetime.time`, whatever shape it arrived in.

    Postgres hands back a `time`; the draft carries the same value as "07:30"
    text, because a draft is JSON.
    """
    if value is None or isinstance(value, time):
        return value
    return parse_reminder_time(str(value))


def _ref_to_draft(ref: Ref) -> list:
    """A `Ref` as JSON the draft can hold (ujson has no dataclasses)."""
    return [ref.kind, ref.start_surah, ref.start_ayah, ref.end_surah, ref.end_ayah, ref.n]


def _ref_from_draft(data: dict) -> Optional[Ref]:
    """The draft's target back as a `Ref`, or None if it is missing or malformed."""
    raw = (data or {}).get("ref")
    try:
        kind, s1, a1, s2, a2, n = raw
        return Ref(str(kind), int(s1), int(a1), int(s2), int(a2),
                   None if n is None else int(n))
    except (TypeError, ValueError):
        return None


def _plan_ref(plan) -> Ref:
    """A stored plan's span as a `Ref`, for `build_plan` and `format_ref`.

    This is what makes "re-derive the calendar from the plan's own columns" work:
    the generator is pure, so the same target, pace, weekday set and start date
    always produce the same portions — which is how a `plan_day` row is known to
    be a consolidation day even though the table has no column for it.
    """
    kind = plan.target_kind if plan.target_kind in (KIND_SURAH, KIND_JUZ, KIND_RANGE) \
        else KIND_RANGE
    return Ref(kind, plan.start_surah, plan.start_ayah, plan.end_surah, plan.end_ayah)


def _target_kind(ref: Ref) -> str:
    """`plan.target_kind` for a parsed target — the column takes three values."""
    return ref.kind if ref.kind in (KIND_SURAH, KIND_JUZ, KIND_RANGE) else KIND_RANGE


def _target_label(plan) -> str:
    """What `{target}` is filled with: "Al-Mulk", "Juz 30", or "67:1-68:5"."""
    ref = _plan_ref(plan)
    if plan.target_kind == KIND_SURAH and ref.is_single_surah():
        return Quran.get_surah_name(plan.start_surah)
    if plan.target_kind == KIND_JUZ:
        for n in range(1, 31):
            juz = juz_ref(n)
            if juz is not None and juz.as_tuple() == ref.as_tuple():
                return "Juz %d" % n
    return format_ref(ref)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# --- Keyboards -----------------------------------------------------------------
# Every callback_data here is `hm:` plus a two-letter selector plus, at most, a
# number or an offset — the longest is `hm:kn:<plan_day_id>`, comfortably inside
# Telegram's 64-byte cap. Nothing about the wizard's state travels in a button:
# it all lives in the draft, because callback_data is neither private nor
# reliably fresh.

def _cancel_row(ui_lang: str) -> list:
    return [InlineKeyboardButton(t("btn_cancel", ui_lang), callback_data="hm:x")]


def _target_keyboard(ui_lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_target_surah", ui_lang), callback_data="hm:t:s")],
        [InlineKeyboardButton(t("btn_target_juz", ui_lang), callback_data="hm:t:j")],
        [InlineKeyboardButton(t("btn_target_range", ui_lang), callback_data="hm:t:r")],
        _cancel_row(ui_lang),
    ])


def _pace_keyboard(ui_lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_pace_auto", ui_lang), callback_data="hm:p:0")],
        [InlineKeyboardButton(str(n), callback_data="hm:p:%d" % n) for n in PACE_CHOICES],
        # No `btn_pace_custom` exists in the frozen manifest, so the "type your
        # own" affordance is a pencil rather than an invented word.
        [InlineKeyboardButton("✏️", callback_data="hm:p:c")],
        _cancel_row(ui_lang),
    ])


def _days_keyboard(ui_lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_days_daily", ui_lang), callback_data="hm:d:all")],
        [InlineKeyboardButton(t("btn_days_weekdays", ui_lang), callback_data="hm:d:wk")],
        [InlineKeyboardButton(t("btn_days_custom", ui_lang), callback_data="hm:d:pick")],
        _cancel_row(ui_lang),
    ])


def _custom_days_keyboard(selected: Sequence[int], ui_lang: str) -> InlineKeyboardMarkup:
    chosen = set(int(d) for d in selected or ())
    row = []
    for index, key in enumerate(_DAY_KEYS, start=1):
        label = t(key, ui_lang)
        row.append(InlineKeyboardButton(("✅ " if index in chosen else "") + label,
                                        callback_data="hm:dt:%d" % index))
    return InlineKeyboardMarkup([
        row[:4], row[4:],
        [InlineKeyboardButton(t("btn_confirm", ui_lang), callback_data="hm:dok")],
        _cancel_row(ui_lang),
    ])


# --- INTEGRATION NOTE (Wave 2A) ------------------------------------------------
# B3 says the timezone and reminder time are captured once, during first plan
# setup, and `/profile` edits them later. Wave 2A owns `/profile` and is building
# the offset picker and the reminder-time capture in parallel; at the time this
# module was written `src/hifz/profile.py` was still a stub exporting nothing, so
# the two keyboards below are the minimum needed to finish the wizard. They are
# deliberately kept together, use only frozen manifest keys, and carry this
# module's own callback prefix — when Wave 2A lands its public helpers, delete
# `_offset_keyboard` / `_reminder_keyboard` and call theirs with an `hm:` prefix.

def _offset_keyboard(ui_lang: str) -> InlineKeyboardMarkup:
    """The UTC-offset picker. Labels are the offsets, which need no translation."""
    buttons = [InlineKeyboardButton("UTC" + offset, callback_data="hm:tz:" + offset)
               for offset in OFFSET_CHOICES]
    rows = [buttons[i:i + 4] for i in range(0, len(buttons), 4)]
    rows.append(_cancel_row(ui_lang))
    return InlineKeyboardMarkup(rows)


def _reminder_keyboard(ui_lang: str) -> InlineKeyboardMarkup:
    """Preset reminder times, with free text as the escape for anything else."""
    buttons = [InlineKeyboardButton(choice, callback_data="hm:rt:" + choice)
               for choice in REMINDER_CHOICES]
    rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
    rows.append(_cancel_row(ui_lang))
    return InlineKeyboardMarkup(rows)

# --- end of the Wave 2A duplication -------------------------------------------


def _preview_keyboard(ui_lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_confirm_plan", ui_lang), callback_data="hm:ok")],
        _cancel_row(ui_lang),
    ])


def _plan_keyboard(plan, ui_lang: str) -> InlineKeyboardMarkup:
    """The lifecycle controls for a plan the user already has (D5)."""
    rows = []
    if plan.status == PLAN_ACTIVE:
        rows.append([InlineKeyboardButton(t("btn_start_drill", ui_lang),
                                          callback_data="hm:go")])
        rows.append([InlineKeyboardButton(t("btn_pause_plan", ui_lang),
                                          callback_data="hm:ps")])
    elif plan.status == PLAN_PAUSED:
        rows.append([InlineKeyboardButton(t("btn_resume_plan", ui_lang),
                                          callback_data="hm:rs")])
    rows.append([InlineKeyboardButton(t("btn_abandon_plan", ui_lang),
                                      callback_data="hm:ab")])
    return InlineKeyboardMarkup(rows)


def _drill_keyboard(plan_day_id: int, surah: int, ayah: int,
                    ui_lang: str) -> InlineKeyboardMarkup:
    """The drill controls: mark it known, hear it again, or stop the plan.

    The repeat button carries the reader's own `rep:` callback_data on purpose —
    "🔁 Repeat ×3" already exists in `main.verse_keyboard` and is handled by
    main.py's chain, so the drill reuses the behaviour instead of copying it.
    """
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_know_by_heart", ui_lang),
                              callback_data="hm:kn:%d" % plan_day_id)],
        [InlineKeyboardButton("🔁 %s ×%d" % (t("btn_repeat", ui_lang), REPEAT_COUNT),
                              callback_data="rep:%d:%d" % (surah, ayah))],
        [InlineKeyboardButton(t("btn_pause_plan", ui_lang), callback_data="hm:ps")],
    ])


# --- The wizard ----------------------------------------------------------------

@command("memorize")
async def memorize(ctx: Ctx) -> None:
    """`/memorize` — start the setup wizard, or manage the plan already running.

    "One active plan per user" is a convention, not a constraint (a partial
    unique index would turn pause-then-create into a user-visible violation), so
    the rule is enforced here: an active plan is offered its controls instead of
    a second wizard, and a paused plan has to be resumed or abandoned before a
    new one can start.
    """
    active = await ctx.store.plans.get_active_plan(ctx.user_id)
    if active is not None:
        await ctx.reply(ctx.tr("plan_exists"), reply_markup=_plan_keyboard(active, ctx.ui_lang))
        return

    paused = await ctx.store.plans.list_plans(ctx.user_id, PLAN_PAUSED)
    if paused:
        await ctx.reply(ctx.tr("plan_paused"),
                        reply_markup=_plan_keyboard(paused[0], ctx.ui_lang))
        return

    ctx.wiz.start(ctx.user_id, WIZARD_KIND, step=STEP_TARGET)

    # "/memorize 67" skips the first question — the argument is a reference the
    # same parser reads at the typed step, so nothing is special-cased.
    ref = parse_reference(ctx.argument) if ctx.argument else None
    if ref is not None and ref.count() > 0:
        ctx.wiz.update(ctx.user_id, step=STEP_PACE, ref=_ref_to_draft(ref))
        await _ask_pace(ctx)
        return

    await ctx.reply(ctx.tr("memorize_choose_target"),
                    reply_markup=_target_keyboard(ctx.ui_lang))


async def _ask_pace(ctx: Ctx) -> None:
    await ctx.edit(ctx.tr("memorize_choose_pace"), reply_markup=_pace_keyboard(ctx.ui_lang))


async def _ask_days(ctx: Ctx) -> None:
    await ctx.edit(ctx.tr("memorize_choose_days"), reply_markup=_days_keyboard(ctx.ui_lang))


async def _expired(ctx: Ctx) -> None:
    """The draft went away between two taps — say so instead of half-working.

    `Wizard.update` answers None when the 30-minute TTL has passed, and every
    call site has to handle it: the alternative is a wizard that appears to
    accept an answer and then previews nothing.
    """
    await ctx.answer()
    await ctx.reply(ctx.tr("wizard_cancelled"))
    ctx.wiz.clear(ctx.user_id)


async def _after_days(ctx: Ctx) -> None:
    """Days are chosen: ask for whatever the profile is still missing, then preview.

    B3's "asked once" lives here — a user whose profile already carries an offset
    and a reminder time goes straight from the day picker to the calendar.
    """
    profile = await ctx.store.profiles.get_profile(ctx.user_id)
    draft = ctx.wiz.data(ctx.user_id)

    offset = draft.get("offset") or (profile.timezone if profile is not None else None)
    if not offset or not is_valid_offset(offset):
        if ctx.wiz.set_step(ctx.user_id, STEP_TIMEZONE) is None:
            await _expired(ctx)
            return
        await ctx.edit(ctx.tr("timezone_prompt"), reply_markup=_offset_keyboard(ctx.ui_lang))
        return

    reminder = draft.get("time") or (_as_time(profile.reminder_time)
                                     if profile is not None else None)
    if not reminder:
        if ctx.wiz.update(ctx.user_id, step=STEP_REMINDER,
                          offset=normalize_offset(offset)) is None:
            await _expired(ctx)
            return
        await ctx.edit(ctx.tr("reminder_prompt"),
                       reply_markup=_reminder_keyboard(ctx.ui_lang))
        return

    if ctx.wiz.update(ctx.user_id, step=STEP_PREVIEW, offset=normalize_offset(offset),
                      time=reminder if isinstance(reminder, str)
                      else format_reminder_time(reminder)) is None:
        await _expired(ctx)
        return
    await _show_preview(ctx)


async def _show_preview(ctx: Ctx) -> None:
    """The calendar the user approves before anything is written (D1).

    The start date is written into the draft here and read back by `_save_plan`,
    so confirming later reproduces exactly these dates: `build_plan` is pure, and
    the only impure input it has is the day it was asked about.
    """
    data = ctx.wiz.data(ctx.user_id)
    ref = _ref_from_draft(data)
    days = [int(d) for d in data.get("days") or ()]
    if ref is None or not days:
        await _expired(ctx)
        return

    offset = data.get("offset") or DEFAULT_OFFSET
    start = data.get("start")
    start_date = date.fromisoformat(start) if start else local_date(_utcnow(), offset)
    if ctx.wiz.update(ctx.user_id, step=STEP_PREVIEW, start=start_date.isoformat()) is None:
        await _expired(ctx)
        return

    portions = build_plan(ref, int(data.get("pace") or AUTO_PACE), days, start_date)
    await ctx.edit(_preview_text(portions, ctx.ui_lang),
                   reply_markup=_preview_keyboard(ctx.ui_lang))


def _preview_text(portions: Sequence[Portion], ui_lang: str) -> str:
    """The preview calendar: one row per date, review days marked.

    `{days}` is filled with the number of **calendar dates**, not with the number
    of advancing portions — Al-Mulk over weekdays is 15 portions spread over 18
    days, and calling that "15 days" would misstate when the plan ends. The
    manifest has no key that can say both numbers in one sentence; see
    docs/HIFZ_STRINGS_GAPS.md.
    """
    header = t("memorize_preview_title", ui_lang).format(
        days=len(portions), start=portions[0].scheduled_date.isoformat(),
        end=portions[-1].scheduled_date.isoformat())
    row = t("memorize_preview_row", ui_lang)
    lines = [header]
    for portion in portions[:PREVIEW_MAX_ROWS]:
        lines.append(row.format(date=portion.scheduled_date.isoformat(),
                                ref=_portion_label(portion)))
    hidden = len(portions) - PREVIEW_MAX_ROWS
    if hidden > 0:
        lines.append("… +%d" % hidden)
    return "\n".join(lines)


def _portion_label(portion: Portion) -> str:
    """"67:1-2", or "🔁 67:1-12" when the day consolidates ground already covered."""
    label = format_ref(portion.as_ref())
    return (REVIEW_MARK + label) if portion.is_consolidation else label


@wizard(WIZARD_KIND)
async def plan_step(ctx: Ctx, text: str) -> None:
    """Free text, routed by the draft's step.

    One handler rather than one per kind: the seam dispatches on `kind`, and a
    step that can be skipped (the timezone) must not need a kind rename to be
    skipped.
    """
    draft = ctx.wiz.get(ctx.user_id)
    if draft is None:
        return
    step = draft.get("step")

    if step == STEP_TARGET_TEXT:
        await _read_target(ctx, text, draft["data"].get("tk"))
    elif step == STEP_PACE_TEXT:
        await _read_pace(ctx, text)
    elif step == STEP_REMINDER:
        await _read_reminder(ctx, text)
    else:
        # Free text at a buttons-only step: repeat the question rather than
        # dropping the draft, which the seam would do if this raised.
        await ctx.reply(ctx.tr("wizard_invalid_input"))


async def _read_target(ctx: Ctx, text: str, target_kind: Optional[str]) -> None:
    """A typed surah number / juz number / range."""
    raw = (text or "").strip()
    if target_kind == "s":
        ref = surah_ref(int(raw)) if raw.isdigit() else parse_reference(raw)
    elif target_kind == "j":
        ref = juz_ref(int(raw)) if raw.isdigit() else parse_reference(raw)
    else:
        ref = parse_reference(raw)

    if ref is None or ref.count() <= 0:
        await ctx.reply(ctx.tr("ref_invalid"))
        return
    if ctx.wiz.update(ctx.user_id, step=STEP_PACE, ref=_ref_to_draft(ref)) is None:
        await _expired(ctx)
        return
    await _ask_pace(ctx)


async def _read_pace(ctx: Ctx, text: str) -> None:
    """A typed ayahs-per-day, bounded by what one stitched audio can carry."""
    raw = (text or "").strip()
    pace = int(raw) if raw.isdigit() else 0
    if not PACE_MIN <= pace <= PACE_MAX:
        await ctx.reply(ctx.tr("memorize_pace_invalid").format(min=PACE_MIN, max=PACE_MAX))
        return
    if ctx.wiz.update(ctx.user_id, step=STEP_DAYS, pace=pace) is None:
        await _expired(ctx)
        return
    await _ask_days(ctx)


async def _read_reminder(ctx: Ctx, text: str) -> None:
    """A typed reminder time. The preset buttons take the same path."""
    value = parse_reminder_time(text)
    if value is None:
        await ctx.reply(ctx.tr("reminder_invalid"))
        return
    if ctx.wiz.update(ctx.user_id, step=STEP_PREVIEW, time=format_reminder_time(value)) is None:
        await _expired(ctx)
        return
    await ctx.reply(ctx.tr("reminder_saved").format(time=format_reminder_time(value)))
    await _show_preview(ctx)


# --- Taps ----------------------------------------------------------------------

@callback("hm:")
async def on_tap(ctx: Ctx, cb_data: str) -> None:
    """Every `hm:` button. Parsed defensively — callback_data comes off the wire.

    Shapes (all far inside Telegram's 64-byte cap):
        hm:t:s|j|r      target kind          hm:tz:+05:00   utc offset
        hm:p:<n>|c      pace preset / typed  hm:rt:07:00    reminder preset
        hm:d:all|wk|pick day set             hm:ok          save the plan
        hm:dt:<1-7>     toggle one day       hm:x           cancel the wizard
        hm:dok          confirm custom days  hm:go          start today's portion
        hm:kn:<id>      "I know this by heart"
        hm:ps hm:rs hm:ab                    pause / resume / abandon
    """
    action, _, arg = cb_data[len("hm:"):].partition(":")

    if action == "x":
        ctx.wiz.clear(ctx.user_id)
        await ctx.answer()
        await ctx.edit(ctx.tr("wizard_cancelled"))
    elif action == "t":
        await _tap_target(ctx, arg)
    elif action == "p":
        await _tap_pace(ctx, arg)
    elif action == "d":
        await _tap_days(ctx, arg)
    elif action == "dt":
        await _tap_day_toggle(ctx, arg)
    elif action == "dok":
        await _tap_days_confirm(ctx)
    elif action == "tz":
        await _tap_timezone(ctx, arg)
    elif action == "rt":
        await _tap_reminder(ctx, arg)
    elif action == "ok":
        await _save_plan(ctx)
    elif action == "go":
        await _start_drill(ctx)
    elif action == "kn":
        await _know_by_heart(ctx, arg)
    elif action in ("ps", "rs", "ab"):
        await _lifecycle(ctx, action)
    else:
        await ctx.answer()          # stale or forged: acknowledge, do nothing


async def _tap_target(ctx: Ctx, arg: str) -> None:
    prompts = {"s": "memorize_surah_prompt", "j": "memorize_juz_prompt",
               "r": "memorize_range_prompt"}
    if arg not in prompts:
        await ctx.answer()
        return
    await ctx.answer()
    if ctx.wiz.update(ctx.user_id, step=STEP_TARGET_TEXT, tk=arg) is None:
        await _expired(ctx)
        return
    await ctx.edit(ctx.tr(prompts[arg]),
                   reply_markup=InlineKeyboardMarkup([_cancel_row(ctx.ui_lang)]))


async def _tap_pace(ctx: Ctx, arg: str) -> None:
    await ctx.answer()
    if arg == "c":
        if ctx.wiz.set_step(ctx.user_id, STEP_PACE_TEXT) is None:
            await _expired(ctx)
            return
        await ctx.edit(ctx.tr("memorize_pace_prompt"),
                       reply_markup=InlineKeyboardMarkup([_cancel_row(ctx.ui_lang)]))
        return
    pace = int(arg) if arg.isdigit() else AUTO_PACE
    if pace and not PACE_MIN <= pace <= PACE_MAX:
        pace = AUTO_PACE
    if ctx.wiz.update(ctx.user_id, step=STEP_DAYS, pace=pace) is None:
        await _expired(ctx)
        return
    await _ask_days(ctx)


async def _tap_days(ctx: Ctx, arg: str) -> None:
    await ctx.answer()
    if arg == "pick":
        if ctx.wiz.update(ctx.user_id, step=STEP_DAYS_CUSTOM, days=list(WEEKDAYS)) is None:
            await _expired(ctx)
            return
        await ctx.edit(ctx.tr("memorize_days_prompt"),
                       reply_markup=_custom_days_keyboard(WEEKDAYS, ctx.ui_lang))
        return
    days = list(DAILY) if arg == "all" else list(WEEKDAYS)
    if ctx.wiz.update(ctx.user_id, days=days) is None:
        await _expired(ctx)
        return
    await _after_days(ctx)


async def _tap_day_toggle(ctx: Ctx, arg: str) -> None:
    await ctx.answer()
    if not arg.isdigit() or not 1 <= int(arg) <= 7:
        return
    data = ctx.wiz.data(ctx.user_id)
    chosen = set(int(d) for d in data.get("days") or ())
    chosen.symmetric_difference_update({int(arg)})
    if ctx.wiz.update(ctx.user_id, days=sorted(chosen)) is None:
        await _expired(ctx)
        return
    await ctx.edit(ctx.tr("memorize_days_prompt"),
                   reply_markup=_custom_days_keyboard(sorted(chosen), ctx.ui_lang))


async def _tap_days_confirm(ctx: Ctx) -> None:
    await ctx.answer()
    data = ctx.wiz.data(ctx.user_id)
    if not data.get("days"):
        # An empty week cannot be materialized at all (build_plan raises), so the
        # picker simply stays open.
        await ctx.edit(ctx.tr("memorize_days_prompt"),
                       reply_markup=_custom_days_keyboard((), ctx.ui_lang))
        return
    await _after_days(ctx)


async def _tap_timezone(ctx: Ctx, arg: str) -> None:
    await ctx.answer()
    if not is_valid_offset(arg):
        return
    offset = normalize_offset(arg)
    if ctx.wiz.update(ctx.user_id, offset=offset) is None:
        await _expired(ctx)
        return
    await ctx.reply(ctx.tr("timezone_saved").format(offset=offset))
    await _after_days(ctx)


async def _tap_reminder(ctx: Ctx, arg: str) -> None:
    await ctx.answer()
    value = parse_reminder_time(arg)
    if value is None:
        return
    if ctx.wiz.update(ctx.user_id, step=STEP_PREVIEW, time=format_reminder_time(value)) is None:
        await _expired(ctx)
        return
    await ctx.reply(ctx.tr("reminder_saved").format(time=format_reminder_time(value)))
    await _show_preview(ctx)


# --- Saving ---------------------------------------------------------------------

async def _save_plan(ctx: Ctx) -> None:
    """Write the plan the user just approved, and queue its first push.

    The portions are rebuilt from the draft rather than carried in it: same
    target, same pace, same weekdays, same start date, same pure function — so
    what is stored is what was previewed, row for row.
    """
    await ctx.answer()
    data = ctx.wiz.data(ctx.user_id)
    ref = _ref_from_draft(data)
    days = [int(d) for d in data.get("days") or ()]
    start = data.get("start")
    if ref is None or not days or not start:
        await _expired(ctx)
        return

    pace = int(data.get("pace") or AUTO_PACE)
    portions = build_plan(ref, pace, days, date.fromisoformat(start))
    offset = normalize_offset(data.get("offset") or DEFAULT_OFFSET)
    reminder = parse_reminder_time(data.get("time") or "") or time(7, 0)

    # "One active plan per user" is a convention, so the old one is retired here
    # rather than by a constraint that would make pause-then-create a crash.
    for plan in await ctx.store.plans.list_plans(ctx.user_id):
        if plan.status != PLAN_COMPLETE:
            await ctx.store.plans.set_plan_status(plan.id, PLAN_COMPLETE)

    plan = await ctx.store.plans.create_plan(
        ctx.user_id, _target_kind(ref), ref.start_surah, ref.start_ayah,
        ref.end_surah, ref.end_ayah, pace, days, to_day_specs(portions))

    await ctx.store.profiles.set_timezone(ctx.user_id, offset)
    await ctx.store.profiles.set_reminder_time(ctx.user_id, reminder)
    ctx.wiz.clear(ctx.user_id)

    queued = await _enqueue_next(ctx.store, ctx.user_id, ctx.chat_id, plan)
    first = local_date(queued.due_at, offset) if queued is not None \
        else portions[0].scheduled_date
    print("HIFZ: plan #%d saved for %d — %d portion(s) over %d day(s), first push %s"
          % (plan.id, ctx.user_id, len(advancing(portions)), len(portions), first))
    await ctx.reply(ctx.tr("plan_saved").format(first_date=first.isoformat()),
                    reply_markup=_plan_keyboard(plan, ctx.ui_lang))


# --- The enqueue chain ----------------------------------------------------------

async def _enqueue_next(store, user_id: int, chat_id: int, plan,
                        now: Optional[datetime] = None):
    """Queue the push for the plan's next pending portion. None if there is none.

    Called when a plan is saved, when a push fires, when a plan is resumed, and
    (harmlessly) when a portion is marked known. `enqueue` answers None on a key
    clash rather than raising, so calling it more often than strictly necessary
    is a no-op — which is what makes the chain self-healing instead of a single
    point of failure.

    The due instant is the portion's own `scheduled_date` at the user's local
    reminder time; a portion whose date has already passed (the plan was paused
    for a week, or set up after today's reminder) is pushed at the next reminder
    instead, so a backlog is delivered one portion a day rather than dropped by
    the scheduler's staleness window.
    """
    if plan is None or plan.status != PLAN_ACTIVE:
        return None

    profile = await store.profiles.get_profile(user_id)
    reminder = _as_time(profile.reminder_time) if profile is not None else None
    if reminder is None:
        print("HIFZ: plan #%d has no reminder time; nothing queued" % plan.id)
        return None
    offset = profile.timezone if profile is not None and profile.timezone else DEFAULT_OFFSET
    if not is_valid_offset(offset):
        offset = DEFAULT_OFFSET
    offset = normalize_offset(offset)

    pending = await store.plans.list_plan_days(plan.id, state=DAY_PENDING)
    if not pending:
        return None
    day = pending[0]

    now = now or _utcnow()
    due_at = to_utc(datetime.combine(day.scheduled_date, reminder), offset)
    if due_at <= now:
        due_at = next_due_utc(reminder, offset, now)

    return await enqueue(store, SEND_KIND, chat_id, due_at,
                         local_day=local_date(due_at, offset),
                         payload={"plan_day_id": day.id, "plan_id": plan.id,
                                  "user_id": user_id, "offset": offset})


@send_handler(SEND_KIND)
async def push_plan_day(ctx: SendCtx) -> None:
    """Deliver one plan day, then queue the next (the chain's re-arming step).

    Returning normally marks the queued row 'sent'; raising marks it 'failed'.
    Both "already delivered" and "the plan is no longer active" therefore
    *return*: neither is a failure, and neither should be retried.
    """
    payload = ctx.payload or {}
    plan_day_id = payload.get("plan_day_id")
    if plan_day_id is None:
        raise ValueError("plan_day payload has no 'plan_day_id' (send #%d)" % ctx.send.id)

    day = await ctx.store.plans.get_plan_day(int(plan_day_id))
    if day is None:
        print("HIFZ: plan day #%s is gone; nothing pushed" % (plan_day_id,))
        return

    plan = await ctx.store.plans.get_plan(day.plan_id)
    if plan is None or plan.status != PLAN_ACTIVE:
        # D5: a paused or abandoned plan produces no pushes. The chain stops here
        # and is restarted by `_lifecycle` on resume.
        print("HIFZ: plan #%s is %s; day #%d not pushed"
              % (day.plan_id, getattr(plan, "status", "gone"), day.id))
        return

    claimed = await ctx.store.plans.claim_plan_day(day.id)
    if claimed is None:
        # A restart between claim and mark_sent can re-deliver the queued row;
        # this conditional write is what makes that a no-op.
        print("HIFZ: plan day #%d was already delivered" % day.id)
        return

    user_id = int(payload.get("user_id") or ctx.chat_id)
    settings = await ctx.store.profiles.get_settings(user_id)
    ui_lang = getattr(settings, "ui_lang", None) or DEFAULT_UI_LANG
    translation_lang = getattr(settings, "translation_lang", None) or DEFAULT_TRANSLATION_LANG
    reciter = getattr(settings, "reciter", None) or DEFAULT_RECITER

    await _send_drill(ctx.bot, ctx.data, ctx.file, ctx.store, ctx.chat_id, plan, claimed,
                      ui_lang, translation_lang, reciter)
    await _enqueue_next(ctx.store, user_id, ctx.chat_id, plan)


# --- Drill delivery (D3) --------------------------------------------------------

async def _portion_for(store, plan, day) -> Optional[Portion]:
    """The generated `Portion` a stored `plan_day` row came from, or None.

    `plan_day` has no column for `drill` or `unit`, and it does not need one:
    the generator is pure, so re-running it over the plan's own columns and its
    own first date reproduces the identical calendar, and the row is matched by
    (date, surah, span).
    """
    days = await store.plans.list_plan_days(plan.id)
    if not days:
        return None
    try:
        portions = build_plan(_plan_ref(plan), plan.pace, plan.days_of_week,
                              days[0].scheduled_date)
    except ValueError as err:                   # a plan with no weekdays cannot exist
        print("HIFZ: cannot re-derive plan #%d: %s" % (plan.id, err))
        return None
    for portion in portions:
        if (portion.scheduled_date, portion.surah, portion.start_ayah, portion.end_ayah) \
                == (day.scheduled_date, day.surah, day.start_ayah, day.end_ayah):
            return portion
    return None


async def _day_position(store, plan, day) -> tuple:
    """(which day this is, how many days the plan has) — the `drill_title` counters."""
    days = await store.plans.list_plan_days(plan.id)
    for index, row in enumerate(days, start=1):
        if row.id == day.id:
            return index, len(days)
    return 1, len(days) or 1


async def _translation_text(surah: int, start: int, end: int, translation_lang: str) -> str:
    """The portion's translation as one message, header and escaping like main.py's.

    A range is one text, not one message per ayah — same reasoning as the single
    stitched audio: a portion is one thing to memorize, not `n` notifications.
    """
    quran = await get_translation(translation_lang)
    body = quran.get_ayahs(surah, start, end) if end > start else quran.get_ayah(surah, start)
    header = "<b>%s</b>" % html.escape(Quran.get_surah_name(surah))
    return (header + "\n\n" + html.escape(body))[:4096]


async def _send_drill(bot, data, file, store, chat_id: int, plan, day,
                      ui_lang: str, translation_lang: str, reciter: str) -> None:
    """One portion: header, Arabic, translation, and **one** audio with controls.

    The audio is the acceptance criterion: `send_combined_audio` stitches a range
    into a single file (Telegram caches it by file_id afterwards), and only a
    one-ayah portion goes through `send_quran`'s per-ayah path. A consolidation
    day wider than `MAX_RANGE_AYAHS` — a whole long surah — would be a download
    nobody wants, so it says so with the reader's existing "range too large"
    string instead of sending 200 files.
    """
    portion = await _portion_for(store, plan, day)
    index, total = await _day_position(store, plan, day)
    ref = Ref(KIND_RANGE, day.surah, day.start_ayah, day.surah, day.end_ayah)
    label = _portion_label(portion) if portion is not None else format_ref(ref)

    await bot.send_message(chat_id=chat_id,
                           text=t("drill_title", ui_lang).format(ref=label, day=index,
                                                                 total=total))
    # The Arabic image is the portion's opening ayah: `send_quran` renders one
    # ayah per photo, and a fifty-photo album is not a drill.
    await send_quran(bot, data, file, day.surah, day.start_ayah, "arabic", chat_id,
                     reciter, ui_lang, translation_lang)
    await bot.send_message(chat_id=chat_id,
                           text=await _translation_text(day.surah, day.start_ayah,
                                                        day.end_ayah, translation_lang),
                           parse_mode="HTML")

    markup = _drill_keyboard(day.id, day.surah, day.start_ayah, ui_lang)
    ayahs = day.end_ayah - day.start_ayah + 1
    if ayahs == 1:
        await send_quran(bot, data, file, day.surah, day.start_ayah, "audio", chat_id,
                         reciter, ui_lang, translation_lang, reply_markup=markup)
    elif ayahs <= MAX_RANGE_AYAHS:
        await send_combined_audio(bot, day.surah, day.start_ayah, day.end_ayah, chat_id,
                                  reciter, reply_markup=markup)
    else:
        print("HIFZ: portion %s is %d ayahs; audio skipped" % (format_ref(ref), ayahs))
        await bot.send_message(chat_id=chat_id,
                               text=t("range_too_large", ui_lang).format(n=MAX_RANGE_AYAHS),
                               reply_markup=markup)


async def _start_drill(ctx: Ctx) -> None:
    """"Start today's portion" — the manual entry point beside the daily push.

    The push creates the habit; this respects the user who is ready now. It takes
    the earliest portion not yet completed and due today or earlier, and claims
    it, so the scheduled push for the same day finds nothing left to send.
    """
    await ctx.answer()
    plan = await ctx.store.plans.get_active_plan(ctx.user_id)
    if plan is None:
        paused = await ctx.store.plans.list_plans(ctx.user_id, PLAN_PAUSED)
        if paused:
            await ctx.reply(ctx.tr("plan_paused"),
                            reply_markup=_plan_keyboard(paused[0], ctx.ui_lang))
        else:
            await ctx.reply(ctx.tr("drill_none_today"))
        return

    profile = await ctx.store.profiles.get_profile(ctx.user_id)
    offset = profile.timezone if profile is not None and profile.timezone else DEFAULT_OFFSET
    if not is_valid_offset(offset):
        offset = DEFAULT_OFFSET
    today = local_date(_utcnow(), offset)

    due = [d for d in await ctx.store.plans.list_plan_days(plan.id, on_or_before=today)
           if d.state != DAY_COMPLETED]
    if not due:
        await ctx.reply(ctx.tr("drill_none_today"))
        return

    day = due[0]
    await ctx.store.plans.claim_plan_day(day.id)     # pending -> sent, once
    await _send_drill(ctx.bot, ctx.data, ctx.file, ctx.store, ctx.chat_id, plan, day,
                      ctx.ui_lang, ctx.translation_lang, ctx.reciter)


# --- "I know this by heart" (D4) ------------------------------------------------

async def _know_by_heart(ctx: Ctx, arg: str) -> None:
    """End the drill: mark the day done, write the interval, log the session.

    The order is the correctness argument. `complete_plan_day` is a conditional
    write, so it is taken **first** and everything after it runs only on the tap
    that won: a second tap on the same portion gets None and stops, which is why
    a streak can never tick twice off one portion. `record_session` is itself
    idempotent on (user, local date, kind, portion), so even a lost update
    between the two writes cannot double-log.
    """
    if not arg.isdigit():
        await ctx.answer()
        return
    plan_day_id = int(arg)

    day = await ctx.store.plans.get_plan_day(plan_day_id)
    if day is None:
        await ctx.answer(ctx.tr("know_already"))
        return

    completed = await ctx.store.plans.complete_plan_day(plan_day_id)
    if completed is None:
        await ctx.answer(ctx.tr("know_already"))
        return
    await ctx.answer()

    await ctx.store.hifz.add_interval(ctx.user_id, day.surah, day.start_ayah, day.end_ayah)
    await record_session(ctx.user_id, KIND_DRILL, surah=day.surah,
                         start_ayah=day.start_ayah, end_ayah=day.end_ayah)

    summary = await load_summary(ctx.store, ctx.user_id, focus_surah=day.surah)
    pct = summary.focus.percent_text if summary.focus is not None \
        else summary.quran.percent_text
    ref = Ref(KIND_RANGE, day.surah, day.start_ayah, day.surah, day.end_ayah)
    await ctx.reply(ctx.tr("know_confirmed").format(ref=format_ref(ref), pct=pct))

    plan = await ctx.store.plans.get_plan(day.plan_id)
    if plan is None:
        return
    remaining = await ctx.store.plans.count_plan_days(plan.id) \
        - await ctx.store.plans.count_plan_days(plan.id, DAY_COMPLETED)
    if remaining <= 0:
        await ctx.store.plans.set_plan_status(plan.id, PLAN_COMPLETE)
        await ctx.reply(ctx.tr("plan_complete").format(target=_target_label(plan)))
        return
    # Belt and braces: the push that delivered this portion already queued the
    # next one, so this is normally a key clash answering None.
    await _enqueue_next(ctx.store, ctx.user_id, ctx.chat_id, plan)


# --- Lifecycle (D5) -------------------------------------------------------------

async def _lifecycle(ctx: Ctx, action: str) -> None:
    """Pause, resume or abandon the caller's plan.

    Pausing does not delete queued rows — the schedule repository has no such
    operation, and adding one would make a queued row a per-plan object rather
    than a per-day one. It does not need to: `push_plan_day` re-reads the plan's
    status and declines to deliver, so a queued row for a paused plan is
    delivered to nobody and the chain lapses. Resuming re-arms it.

    Abandoning moves the plan to 'complete': the column takes three values, and
    'complete' is the one that means "no longer running". The plan's rows stay,
    so what was already memorized is still counted.
    """
    await ctx.answer()
    plan = await ctx.store.plans.get_active_plan(ctx.user_id)
    if plan is None:
        paused = await ctx.store.plans.list_plans(ctx.user_id, PLAN_PAUSED)
        plan = paused[0] if paused else None
    if plan is None:
        await ctx.reply(ctx.tr("drill_none_today"))
        return

    if action == "ps":
        updated = await ctx.store.plans.set_plan_status(plan.id, PLAN_PAUSED)
        await ctx.reply(ctx.tr("plan_paused"),
                        reply_markup=_plan_keyboard(updated or plan, ctx.ui_lang))
    elif action == "rs":
        updated = await ctx.store.plans.set_plan_status(plan.id, PLAN_ACTIVE)
        await ctx.reply(ctx.tr("plan_resumed"),
                        reply_markup=_plan_keyboard(updated or plan, ctx.ui_lang))
        await _enqueue_next(ctx.store, ctx.user_id, ctx.chat_id, updated or plan)
    else:
        await ctx.store.plans.set_plan_status(plan.id, PLAN_COMPLETE)
        await ctx.reply(ctx.tr("plan_abandoned"))
