"""Delivering a portion (D3) and "I know this by heart" (D4)."""

import html
import logging

import services.plans as plans_service
from bot.features import Ctx
from bot.features._plan_common import _day_position, _portion_for, _target_label
from bot.features._plan_keyboards import _drill_keyboard, _plan_keyboard
from bot.features._plan_preview import _portion_label
from bot.limits import MAX_RANGE_AYAHS
from bot.media import deliver_combined_audio, deliver_quran
from domain.quran import Quran, get_translation
from domain.refs import KIND_RANGE, Ref, format_ref
from infra.store.plans import PLAN_PAUSED
from locales import t

logger = logging.getLogger(__name__)


async def _translation_text(surah: int, start: int, end: int, translation_lang: str) -> str:
    """The portion's translation as one message, header and escaping like main.py's.

    A range is one text, not one message per ayah — same reasoning as the single
    stitched audio: a portion is one thing to memorize, not `n` notifications.
    """
    quran = await get_translation(translation_lang)
    body = quran.get_ayahs(surah, start, end) if end > start else quran.get_ayah(surah, start)
    header = "<b>%s</b>" % html.escape(Quran.get_surah_name(surah))
    return (header + "\n\n" + html.escape(body))[:4096]


async def _send_drill(
    channel,
    data,
    file,
    store,
    plan,
    day,
    ui_lang: str,
    translation_lang: str,
    reciter: str,
) -> None:
    """One portion: header, Arabic, translation, and **one** audio with controls.

    The audio is the acceptance criterion: `deliver_combined_audio` stitches a
    range into a single file (cached by file_id / media id afterwards), and only a
    one-ayah portion goes through `deliver_quran`'s per-ayah path. A consolidation
    day wider than `MAX_RANGE_AYAHS` — a whole long surah — would be a download
    nobody wants, so it says so with the reader's existing "range too large"
    string instead of sending 200 files.
    """
    portion = await _portion_for(store, plan, day)
    index, total = await _day_position(store, plan, day)
    ref = Ref(KIND_RANGE, day.surah, day.start_ayah, day.surah, day.end_ayah)
    label = _portion_label(portion) if portion is not None else format_ref(ref)

    await channel.send_text(t("drill_title", ui_lang).format(ref=label, day=index, total=total))
    # The Arabic image is the portion's opening ayah: `deliver_quran` renders one
    # ayah per photo, and a fifty-photo album is not a drill.
    await deliver_quran(
        channel, data, day.surah, day.start_ayah, "arabic", reciter, ui_lang, translation_lang
    )
    await channel.send_text(
        await _translation_text(day.surah, day.start_ayah, day.end_ayah, translation_lang),
        html=True,
    )

    choices = _drill_keyboard(day.id, day.surah, day.start_ayah, ui_lang)
    ayahs = day.end_ayah - day.start_ayah + 1
    if ayahs == 1:
        await deliver_quran(
            channel,
            data,
            day.surah,
            day.start_ayah,
            "audio",
            reciter,
            ui_lang,
            translation_lang,
            choices=choices,
        )
    elif ayahs <= MAX_RANGE_AYAHS:
        await deliver_combined_audio(
            channel, day.surah, day.start_ayah, day.end_ayah, reciter, choices=choices
        )
    else:
        logger.warning("HIFZ: portion %s is %d ayahs; audio skipped" % (format_ref(ref), ayahs))
        await channel.send_text(t("range_too_large", ui_lang).format(n=MAX_RANGE_AYAHS), choices)


async def _start_drill(ctx: Ctx) -> None:
    """ "Start today's portion" — the manual entry point beside the daily push.

    The push creates the habit; this respects the user who is ready now. It takes
    the earliest portion not yet completed and due today or earlier, and claims
    it, so the scheduled push for the same day finds nothing left to send.
    """
    await ctx.answer()
    plan = await ctx.store.plans.get_active_plan(ctx.user_id)
    if plan is None:
        paused = await ctx.store.plans.list_plans(ctx.user_id, PLAN_PAUSED)
        if paused:
            await ctx.reply(ctx.tr("plan_paused"), choices=_plan_keyboard(paused[0], ctx.ui_lang))
        else:
            await ctx.reply(ctx.tr("drill_none_today"))
        return

    due = await plans_service.due_days(ctx.store, ctx.user_id, plan)
    if not due:
        await ctx.reply(ctx.tr("drill_none_today"))
        return

    day = due[0]
    await ctx.store.plans.claim_plan_day(day.id)  # pending -> sent, once
    await _send_drill(
        ctx.channel,
        ctx.data,
        ctx.file,
        ctx.store,
        plan,
        day,
        ctx.ui_lang,
        ctx.translation_lang,
        ctx.reciter,
    )


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

    result = await plans_service.complete_day(ctx.store, ctx.user_id, ctx.chat_id, plan_day_id)
    if result.status != plans_service.DONE:
        await ctx.answer(ctx.tr("know_already"))
        return
    await ctx.answer()

    day = result.day
    ref = Ref(KIND_RANGE, day.surah, day.start_ayah, day.surah, day.end_ayah)
    await ctx.reply(ctx.tr("know_confirmed").format(ref=format_ref(ref), pct=result.percent_text))
    if result.plan_completed:
        await ctx.reply(ctx.tr("plan_complete").format(target=_target_label(result.plan)))
