"""Verse of the day: one ayah a day at a time the reader picks (MULTI_PLATFORM_PLAN P2.5).

The same ayah reaches everyone on a given local date (`domain.daily_ayah`). Built
on the channel seam, so the one implementation serves Telegram and WhatsApp:

    /daily (or "daily")  -> status, with Turn on / Change time / Turn off
    hd:on                -> the time-zone picker if the profile has none, else times
    hd:tz:+05:00         -> saves the profile's time zone, then times
    hd:t:07:00           -> Telegram: on. WhatsApp: the explicit consent message first,
    hd:ok:07:00          -> ...whose "Yes" records consent and turns it on
    hd:off               -> off (the row is kept, so the time is remembered)
    hd:now               -> today's verse right away (the WhatsApp menu), then an
                            offer to get it every day if they don't already

Delivery is the `daily_ayah` send kind below, through `deliver_push`: a free
message on Telegram and inside WhatsApp's 24-hour window, the approved
`daily_ayah` template outside it, nothing without consent.
"""

import html
import logging
import re
from datetime import datetime, time, timedelta, timezone

from bot.features import Ctx, callback, command
from bot.keyboards.rows import button_rows
from bot.keyboards.time_pickers import offset_choices
from bot.keyboards.verse import verse_keyboard
from bot.media import deliver_quran
from bot.text import build_verse_text, reference
from channels import WHATSAPP, Choice
from domain.daily_ayah import ayah_for
from domain.localtime import local_date
from infra.scheduler import SendCtx, schedule_daily, send_handler
from infra.scheduler.push import DROPPED, Template, deliver_push, template_lang
from locales import t
from services.user_settings import UserSettings

logger = logging.getLogger(__name__)

SEND_KIND = "daily_ayah"
CB = "hd:"
TIMES = ("05:00", "06:00", "07:00", "08:00", "09:00", "12:00", "18:00", "20:00", "21:00")

TEMPLATE_TEXT_MAX = 600  # leaves room in the 1,024-char body for the template's own words


def _hhmm(value: time) -> str:
    return value.strftime("%H:%M")


def _parse_time(text: str) -> time:
    hours, minutes = text.split(":")
    return time(int(hours), int(minutes))


async def _offset(ctx: Ctx):
    profile = await ctx.store.profiles.get_profile(ctx.user_id)
    return profile.timezone if profile is not None else None


async def _status(ctx: Ctx) -> None:
    sub = await ctx.store.daily.get(ctx.user_id)
    if sub is not None and sub.enabled:
        text = ctx.tr("daily_status_on", time=_hhmm(sub.send_time), offset=await _offset(ctx))
        choices = [
            [
                Choice(ctx.tr("daily_btn_change"), data=CB + "on"),
                Choice(ctx.tr("daily_btn_off"), data=CB + "off"),
            ]
        ]
    else:
        text = ctx.tr("daily_status_off")
        choices = [[Choice(ctx.tr("daily_btn_on"), data=CB + "on")]]
    await ctx.reply(text, choices)


async def _ask_time(ctx: Ctx) -> None:
    choices = button_rows([Choice(hhmm, data=CB + "t:" + hhmm) for hhmm in TIMES], 3)
    await ctx.reply(ctx.tr("daily_pick_time"), choices)


async def _enable(ctx: Ctx, send_time: time) -> None:
    offset = await _offset(ctx)
    await ctx.store.daily.upsert(ctx.user_id, ctx.platform, send_time, True)
    await schedule_daily(
        ctx.store,
        SEND_KIND,
        ctx.user_id,
        send_time,
        offset,
        payload={"time": _hhmm(send_time)},
        platform=ctx.platform,
        key_extra=_hhmm(send_time),
    )
    await ctx.reply(ctx.tr("daily_enabled", time=_hhmm(send_time)))


async def _send_today(channel, data, surah, ayah, ui_lang, translation_lang, reciter) -> None:
    """Today's verse card: the header, then the verse with its usual buttons."""
    await channel.send_text(t("daily_header", ui_lang), html=True)
    await deliver_quran(
        channel,
        data,
        surah,
        ayah,
        "translation",
        reciter,
        ui_lang,
        translation_lang,
        # web_app doubles as "is Telegram": the Uzbek audio row is Telegram-only too
        choices=verse_keyboard(
            surah,
            ayah,
            "translation",
            ui_lang,
            app=channel.caps.web_app,
            uz_audio=channel.caps.web_app,
        ),
    )


async def _today(ctx: Ctx) -> None:
    surah, ayah = ayah_for(local_date(datetime.now(timezone.utc), await _offset(ctx) or "+00:00"))
    await _send_today(
        ctx.channel, ctx.data, surah, ayah, ctx.ui_lang, ctx.translation_lang, ctx.reciter
    )
    sub = await ctx.store.daily.get(ctx.user_id)
    if sub is None or not sub.enabled:
        await ctx.reply(ctx.tr("daily_offer"), [[Choice(ctx.tr("daily_btn_on"), data=CB + "on")]])


@command("daily")
async def daily(ctx: Ctx) -> None:
    await _status(ctx)


@callback(CB)
async def on_tap(ctx: Ctx, cb_data: str) -> None:
    await ctx.answer()
    action, _, value = cb_data[len(CB) :].partition(":")
    if action == "now":
        await _today(ctx)
    elif action == "on":
        if await _offset(ctx) is None:
            await ctx.reply(ctx.tr("daily_pick_timezone"), offset_choices(ctx.ui_lang, CB + "tz:"))
        else:
            await _ask_time(ctx)
    elif action == "tz":
        await ctx.store.profiles.set_timezone(ctx.user_id, value)
        await _ask_time(ctx)
    elif action == "t":
        send_time = _parse_time(value)
        consent = await ctx.store.identity.get_by_user(ctx.user_id, WHATSAPP)
        if ctx.platform == WHATSAPP and not (consent is not None and consent.consented):
            # WhatsApp requires explicit opt-in that names us and the channel.
            await ctx.reply(
                ctx.tr("daily_consent", time=value),
                [
                    [
                        Choice(ctx.tr("daily_btn_yes"), data=CB + "ok:" + value),
                        Choice(ctx.tr("daily_btn_no"), data=CB + "no"),
                    ]
                ],
            )
            return
        await _enable(ctx, send_time)
    elif action == "ok":
        await ctx.store.identity.opt_in(ctx.user_id, WHATSAPP, datetime.now(timezone.utc))
        await _enable(ctx, _parse_time(value))
    elif action == "off":
        await ctx.store.daily.set_enabled(ctx.user_id, False)
        await ctx.reply(ctx.tr("daily_disabled"))
    elif action == "no":
        await _status(ctx)


def _template_text(card_html: str) -> str:
    """A verse card's text as a template parameter: plain, one line, bounded.

    Template parameters may not contain newlines, tabs or long runs of spaces.
    """
    text = html.unescape(re.sub(r"<[^>]+>", "", card_html))
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= TEMPLATE_TEXT_MAX else text[: TEMPLATE_TEXT_MAX - 1] + "…"


@send_handler(SEND_KIND)
async def push_daily(ctx: SendCtx) -> None:
    """Deliver today's verse, then queue tomorrow's."""
    sub = await ctx.store.daily.get(ctx.chat_id)
    if sub is None or not sub.enabled or _hhmm(sub.send_time) != ctx.payload.get("time"):
        return  # turned off, or the time changed and a newer row carries the new one
    offset = ctx.payload.get("offset") or "+00:00"
    now = ctx.now or datetime.now(timezone.utc)
    surah, ayah = ayah_for(local_date(now, offset))
    settings = await UserSettings().get(ctx.chat_id, ctx.chat_id)
    ui_lang, translation_lang = settings.ui_lang, settings.translation_lang

    async def session(channel) -> None:
        await _send_today(
            channel, ctx.data, surah, ayah, ui_lang, translation_lang, settings.reciter
        )

    card = await build_verse_text(surah, ayah, "translation", ui_lang, translation_lang, ctx.data)
    template = Template(
        SEND_KIND,
        template_lang(ui_lang),
        [reference(surah, ayah, ui_lang), _template_text(card)],
        ["vc:tr:%d:%d" % (surah, ayah)],
    )
    outcome = await deliver_push(ctx, session=session, template=template)
    if outcome == DROPPED and ctx.platform == WHATSAPP:
        # No consent (or no way to reach them): stop queueing, don't keep trying.
        await ctx.store.daily.set_enabled(ctx.chat_id, False)
        return
    await schedule_daily(
        ctx.store,
        SEND_KIND,
        ctx.chat_id,
        sub.send_time,
        offset,
        now=now + timedelta(minutes=1),
        payload={"time": _hhmm(sub.send_time)},
        platform=ctx.platform,
        key_extra=_hhmm(sub.send_time),
    )
