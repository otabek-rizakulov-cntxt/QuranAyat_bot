"""Uzbek translation audio (docs/MULTILINGUAL_PLAN.md §8.1).

The whole Qur'an read in Uzbek, one mp3 per surah on newbooks.uz; the sending
itself (Range cuts, parts, captions, cache keys) is infra.uz_audio_delivery,
shared with the Mini App's "send to chat". This module is the buttons.

Callback prefix "uz:" (bot.features.PREFIXES):

    uz:a:2:284        one ayah
    uz:r:2:284:285    a range (≤ MAX_CLIP_AYAHS)
    uz:s:2            the whole surah

The buttons are shown to Uzbek UI users only (bot/keyboards/verse.py); a tap is
served for anyone, since an old keyboard may outlive a language switch.
"""

import logging

import httpx

from bot.features import Ctx, callback
from infra.uz_audio_delivery import send_clip, send_surah, valid_clip
from locales import t

logger = logging.getLogger(__name__)

_PREFIX = "uz:"


def parse(cb_data: str):
    """`uz:a:S:A` / `uz:r:S:A:B` / `uz:s:S` -> (kind, surah, first, last), or None."""
    fields = cb_data[len(_PREFIX) :].split(":")
    try:
        kind, nums = fields[0], [int(x) for x in fields[1:]]
    except (ValueError, IndexError):
        return None
    if kind == "s" and len(nums) == 1:
        surah, first, last = nums[0], 1, 1
    elif kind == "a" and len(nums) == 2:
        surah, first, last = nums[0], nums[1], nums[1]
    elif kind == "r" and len(nums) == 3:
        surah, first, last = nums
    else:
        return None
    if not valid_clip(surah, first, last):
        return None
    return kind, surah, first, last


@callback(_PREFIX)
async def on_uz_audio(ctx: Ctx, cb_data: str) -> None:
    parsed = parse(cb_data)
    if parsed is None:
        await ctx.answer(t("uza_unavailable", ctx.ui_lang))
        return
    kind, surah, first, last = parsed
    await ctx.answer()
    try:
        if kind == "s":
            await send_surah(ctx.channel, surah, ctx.ui_lang)
        else:
            await send_clip(ctx.channel, surah, first, last, ctx.ui_lang)
    except (OSError, httpx.HTTPError) as err:
        logger.warning("uz audio %s failed: %s", cb_data, err)
        await ctx.reply(t("uza_failed", ctx.ui_lang))
