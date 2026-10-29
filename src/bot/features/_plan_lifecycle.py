"""Pause, resume and abandon a plan (D5)."""

import services.plans as plans_service
from bot.features import Ctx
from bot.features._plan_keyboards import _plan_keyboard


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
    action = {"ps": plans_service.PAUSE, "rs": plans_service.RESUME}.get(
        action, plans_service.ABANDON
    )
    plan = await plans_service.change_status(ctx.store, ctx.user_id, ctx.chat_id, action)
    if plan is None:
        await ctx.reply(ctx.tr("drill_none_today"))
        return

    if action == plans_service.PAUSE:
        await ctx.reply(ctx.tr("plan_paused"), reply_markup=_plan_keyboard(plan, ctx.ui_lang))
    elif action == plans_service.RESUME:
        await ctx.reply(ctx.tr("plan_resumed"), reply_markup=_plan_keyboard(plan, ctx.ui_lang))
    else:
        await ctx.reply(ctx.tr("plan_abandoned"))
