"""The plan preview (D1: the preview is the plan): the same build_plan call the
saved plan is written from, rendered as a calendar."""

from datetime import date
from typing import Sequence

from bot.features import Ctx
from bot.features._plan_common import (
    PREVIEW_MAX_ROWS,
    REVIEW_MARK,
    STEP_PREVIEW,
    _expired,
    _ref_from_draft,
    _utcnow,
)
from bot.features._plan_keyboards import _preview_keyboard
from domain.localtime import DEFAULT_OFFSET, local_date
from domain.plan_builder import AUTO_PACE, Portion, build_plan
from domain.refs import format_ref
from locales import t


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
    await ctx.edit(
        _preview_text(portions, ctx.ui_lang), reply_markup=_preview_keyboard(ctx.ui_lang)
    )


def _preview_text(portions: Sequence[Portion], ui_lang: str) -> str:
    """The preview calendar: one row per date, review days marked.

    `{days}` is filled with the number of **calendar dates**, not with the number
    of advancing portions — Al-Mulk over weekdays is 15 portions spread over 18
    days, and calling that "15 days" would misstate when the plan ends. The
    manifest has no key that can say both numbers in one sentence; see
    docs/HIFZ_STRINGS_GAPS.md.
    """
    header = t("memorize_preview_title", ui_lang).format(
        days=len(portions),
        start=portions[0].scheduled_date.isoformat(),
        end=portions[-1].scheduled_date.isoformat(),
    )
    row = t("memorize_preview_row", ui_lang)
    lines = [header]
    for portion in portions[:PREVIEW_MAX_ROWS]:
        lines.append(
            row.format(date=portion.scheduled_date.isoformat(), ref=_portion_label(portion))
        )
    hidden = len(portions) - PREVIEW_MAX_ROWS
    if hidden > 0:
        lines.append("… +%d" % hidden)
    return "\n".join(lines)


def _portion_label(portion: Portion) -> str:
    """ "67:1-2", or "🔁 67:1-12" when the day consolidates ground already covered."""
    label = format_ref(portion.as_ref())
    return (REVIEW_MARK + label) if portion.is_consolidation else label
