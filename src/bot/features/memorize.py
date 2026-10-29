# Workstream D — plans & drills (spec items D1, D3-D5).
#
# Owns: /memorize (the setup wizard: target -> pace -> days -> preview ->
# confirm), drill delivery, the "I know this by heart" button, and the plan
# lifecycle (pause / resume / abandon / complete).
# Callback prefix: "hm:" (see bot.features.PREFIXES). Wizard kinds: prefix them "plan_".
#
# This module holds the registered entry points — /memorize, the wizard step,
# the "hm:" tap router and the daily-push handler — and routes to the pieces,
# which live in modules the router does not discover (leading underscore):
#
#     _plan_common.py     knobs, draft conversions, the plan-service names
#     _plan_keyboards.py  every keyboard of the flow
#     _plan_setup.py      the wizard's typed steps and taps, and saving
#     _plan_preview.py    the preview calendar (D1)
#     _plan_drill.py      drill delivery (D3) and "I know this by heart" (D4)
#     _plan_lifecycle.py  pause / resume / abandon (D5)
#
# Drill delivery uses bot.media's `send_quran` and `send_combined_audio`, the
# same senders the scheduler and the reader use.
#
# Four properties are load-bearing here, and each has a test named after it:
#
#   D1  **the preview is the plan.** `domain.plan_builder.build_plan` is pure, so
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
import logging

from bot.features import Ctx, callback, command, wizard
from bot.features._plan_common import (  # re-exported: tests and the scheduler use these names
    STEP_PACE,
    STEP_PACE_TEXT,
    STEP_REMINDER,
    STEP_TARGET,
    STEP_TARGET_TEXT,
    WIZARD_KIND,
    _enqueue_next,
    _ref_to_draft,
)
from bot.features._plan_drill import _know_by_heart, _send_drill, _start_drill
from bot.features._plan_keyboards import _plan_keyboard, _target_keyboard
from bot.features._plan_lifecycle import _lifecycle
from bot.features._plan_setup import (
    _ask_pace,
    _read_pace,
    _read_reminder,
    _read_target,
    _save_plan,
    _tap_day_toggle,
    _tap_days,
    _tap_days_confirm,
    _tap_pace,
    _tap_reminder,
    _tap_target,
    _tap_timezone,
)
from domain.refs import parse_reference
from infra.scheduler import SendCtx, send_handler
from infra.store.plans import PLAN_ACTIVE, PLAN_PAUSED
from services.plans import SEND_KIND
from services.user_settings import DEFAULT_RECITER, DEFAULT_TRANSLATION_LANG, DEFAULT_UI_LANG

logger = logging.getLogger(__name__)

__all__ = [
    "memorize",
    "on_tap",
    "plan_step",
    "push_plan_day",
    "SEND_KIND",
    "WIZARD_KIND",
    "_enqueue_next",
    "_send_drill",
]


# --- Knobs ---------------------------------------------------------------------


# The scheduled-send kind. `infra.scheduler` dispatches on it; nothing else uses it.


# --- Small conversions ---------------------------------------------------------


# --- Keyboards -----------------------------------------------------------------
# Every callback_data here is `hm:` plus a two-letter selector plus, at most, a
# number or an offset — the longest is `hm:kn:<plan_day_id>`, comfortably inside
# Telegram's 64-byte cap. Nothing about the wizard's state travels in a button:
# it all lives in the draft, because callback_data is neither private nor
# reliably fresh.


# --- end of the Wave 2A duplication -------------------------------------------


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
        await ctx.reply(ctx.tr("plan_paused"), reply_markup=_plan_keyboard(paused[0], ctx.ui_lang))
        return

    ctx.wiz.start(ctx.user_id, WIZARD_KIND, step=STEP_TARGET)

    # "/memorize 67" skips the first question — the argument is a reference the
    # same parser reads at the typed step, so nothing is special-cased.
    ref = parse_reference(ctx.argument) if ctx.argument else None
    if ref is not None and ref.count() > 0:
        ctx.wiz.update(ctx.user_id, step=STEP_PACE, ref=_ref_to_draft(ref))
        await _ask_pace(ctx)
        return

    await ctx.reply(ctx.tr("memorize_choose_target"), reply_markup=_target_keyboard(ctx.ui_lang))


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
    action, _, arg = cb_data[len("hm:") :].partition(":")

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
        await ctx.answer()  # stale or forged: acknowledge, do nothing


# --- Saving ---------------------------------------------------------------------


# --- The enqueue chain ----------------------------------------------------------


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
        logger.warning("HIFZ: plan day #%s is gone; nothing pushed" % (plan_day_id,))
        return

    plan = await ctx.store.plans.get_plan(day.plan_id)
    if plan is None or plan.status != PLAN_ACTIVE:
        # D5: a paused or abandoned plan produces no pushes. The chain stops here
        # and is restarted by `_lifecycle` on resume.
        logger.warning(
            "HIFZ: plan #%s is %s; day #%d not pushed"
            % (day.plan_id, getattr(plan, "status", "gone"), day.id)
        )
        return

    claimed = await ctx.store.plans.claim_plan_day(day.id)
    if claimed is None:
        # A restart between claim and mark_sent can re-deliver the queued row;
        # this conditional write is what makes that a no-op.
        logger.info("HIFZ: plan day #%d was already delivered" % day.id)
        return

    user_id = int(payload.get("user_id") or ctx.chat_id)
    settings = await ctx.store.profiles.get_settings(user_id)
    ui_lang = getattr(settings, "ui_lang", None) or DEFAULT_UI_LANG
    translation_lang = getattr(settings, "translation_lang", None) or DEFAULT_TRANSLATION_LANG
    reciter = getattr(settings, "reciter", None) or DEFAULT_RECITER

    await _send_drill(
        ctx.bot,
        ctx.data,
        ctx.file,
        ctx.store,
        ctx.chat_id,
        plan,
        claimed,
        ui_lang,
        translation_lang,
        reciter,
    )
    await _enqueue_next(ctx.store, user_id, ctx.chat_id, plan, now=ctx.now)


# --- Drill delivery (D3) --------------------------------------------------------


# --- "I know this by heart" (D4) ------------------------------------------------


# --- Lifecycle (D5) -------------------------------------------------------------
