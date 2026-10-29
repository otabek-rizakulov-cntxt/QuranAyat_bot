"""The /memorize setup wizard: target -> pace -> days -> timezone -> reminder ->
preview -> confirm. The typed steps and the taps both land here; memorize.py
routes them."""

from datetime import date, time
from typing import Optional

from telegram import InlineKeyboardMarkup

import services.plans as plans_service
from bot.features import Ctx
from bot.features._plan_common import (
    DAILY,
    PACE_MAX,
    PACE_MIN,
    STEP_DAYS,
    STEP_DAYS_CUSTOM,
    STEP_PACE,
    STEP_PACE_TEXT,
    STEP_PREVIEW,
    STEP_REMINDER,
    STEP_TARGET_TEXT,
    STEP_TIMEZONE,
    WEEKDAYS,
    _as_time,
    _expired,
    _ref_from_draft,
    _ref_to_draft,
)
from bot.features._plan_keyboards import (
    _cancel_row,
    _custom_days_keyboard,
    _days_keyboard,
    _pace_keyboard,
    _plan_keyboard,
    _reminder_keyboard,
)
from bot.features._plan_preview import _show_preview
from bot.features.profile import format_reminder_time, parse_reminder_time
from bot.keyboards.time_pickers import offset_keyboard
from domain.localtime import DEFAULT_OFFSET, is_valid_offset, normalize_offset
from domain.plan_builder import AUTO_PACE
from domain.refs import juz_ref, parse_reference, surah_ref


async def _ask_pace(ctx: Ctx) -> None:
    await ctx.edit(ctx.tr("memorize_choose_pace"), reply_markup=_pace_keyboard(ctx.ui_lang))


async def _ask_days(ctx: Ctx) -> None:
    await ctx.edit(ctx.tr("memorize_choose_days"), reply_markup=_days_keyboard(ctx.ui_lang))


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
        await ctx.edit(
            ctx.tr("timezone_prompt"),
            reply_markup=offset_keyboard(
                ctx.ui_lang, "hm:tz:", label_prefix="UTC", cancel_data="hm:x"
            ),
        )
        return

    reminder = draft.get("time") or (
        _as_time(profile.reminder_time) if profile is not None else None
    )
    if not reminder:
        if ctx.wiz.update(ctx.user_id, step=STEP_REMINDER, offset=normalize_offset(offset)) is None:
            await _expired(ctx)
            return
        await ctx.edit(ctx.tr("reminder_prompt"), reply_markup=_reminder_keyboard(ctx.ui_lang))
        return

    if (
        ctx.wiz.update(
            ctx.user_id,
            step=STEP_PREVIEW,
            offset=normalize_offset(offset),
            time=reminder if isinstance(reminder, str) else format_reminder_time(reminder),
        )
        is None
    ):
        await _expired(ctx)
        return
    await _show_preview(ctx)


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


async def _tap_target(ctx: Ctx, arg: str) -> None:
    prompts = {
        "s": "memorize_surah_prompt",
        "j": "memorize_juz_prompt",
        "r": "memorize_range_prompt",
    }
    if arg not in prompts:
        await ctx.answer()
        return
    await ctx.answer()
    if ctx.wiz.update(ctx.user_id, step=STEP_TARGET_TEXT, tk=arg) is None:
        await _expired(ctx)
        return
    await ctx.edit(
        ctx.tr(prompts[arg]), reply_markup=InlineKeyboardMarkup([_cancel_row(ctx.ui_lang)])
    )


async def _tap_pace(ctx: Ctx, arg: str) -> None:
    await ctx.answer()
    if arg == "c":
        if ctx.wiz.set_step(ctx.user_id, STEP_PACE_TEXT) is None:
            await _expired(ctx)
            return
        await ctx.edit(
            ctx.tr("memorize_pace_prompt"),
            reply_markup=InlineKeyboardMarkup([_cancel_row(ctx.ui_lang)]),
        )
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
        await ctx.edit(
            ctx.tr("memorize_days_prompt"),
            reply_markup=_custom_days_keyboard(WEEKDAYS, ctx.ui_lang),
        )
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
    await ctx.edit(
        ctx.tr("memorize_days_prompt"),
        reply_markup=_custom_days_keyboard(sorted(chosen), ctx.ui_lang),
    )


async def _tap_days_confirm(ctx: Ctx) -> None:
    await ctx.answer()
    data = ctx.wiz.data(ctx.user_id)
    if not data.get("days"):
        # An empty week cannot be materialized at all (build_plan raises), so the
        # picker simply stays open.
        await ctx.edit(
            ctx.tr("memorize_days_prompt"), reply_markup=_custom_days_keyboard((), ctx.ui_lang)
        )
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

    saved = await plans_service.save_plan(
        ctx.store,
        ctx.user_id,
        ctx.chat_id,
        ref,
        int(data.get("pace") or AUTO_PACE),
        days,
        date.fromisoformat(start),
        data.get("offset") or DEFAULT_OFFSET,
        parse_reminder_time(data.get("time") or "") or time(7, 0),
    )
    plan, first = saved.plan, saved.first_date
    ctx.wiz.clear(ctx.user_id)
    await ctx.reply(
        ctx.tr("plan_saved").format(first_date=first.isoformat()),
        reply_markup=_plan_keyboard(plan, ctx.ui_lang),
    )
