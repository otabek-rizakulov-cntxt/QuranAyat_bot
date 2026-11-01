"""Sending Quran media to a conversation.

The `deliver_*` functions take a `Channel` (channels/), so the same send works
on every platform. On Telegram each media send replays the file_id cached under
its key and only uploads (and caches the new id) on a miss or a rejected id —
`send_cached` in channels/telegram.py. The `send_*` functions are the original
`(bot, …, chat_id, …)` entry points, kept as thin Telegram wrappers for the
callers that have not moved to a channel yet (the hifz drill and the group post,
docs/MULTI_PLATFORM_PLAN.md P3.1).
"""

from urllib.parse import urlencode

from bot.keyboards.page import page_keyboard
from bot.limits import REPEAT_COUNT
from bot.text import build_verse_text, page_caption, reference
from channels.telegram import TelegramChannel
from config.settings import get_settings
from domain.quran import Quran
from infra import audio as cdn_audio
from infra import catalog, nav_state
from infra.page_image import fetch_and_stitch


def combined_audio_key(surah: int, start: int, end: int, performer: str) -> str:
    """Telegram file_id cache key for a stitched range, shared by the in-chat send
    that produces it and the inline result that replays it."""
    return "combined:%d:%d-%d:%s" % (surah, start, end, performer)


# Route (on this very app) that stitches a range of recitations on demand. An
# inline audio result can only carry a file_id or a URL Telegram fetches itself —
# never an upload — so a range nobody has sent in a chat yet needs a public place
# to be fetched from, and this is it.
RANGE_AUDIO_PATH = "/media/range.mp3"


def range_audio_url(surah: int, start: int, end: int, performer: str) -> str | None:
    """Public URL of the stitched recitation of `surah:start-end`, or None when we
    have no public base URL to serve it from (local dev without WEBHOOK_URL)."""
    base = get_settings().webhook_base_url
    if not base or not base.startswith("https://"):
        return None
    query = urlencode({"surah": surah, "start": start, "end": end, "reciter": performer})
    return base + RANGE_AUDIO_PATH + "?" + query


async def deliver_quran(
    channel,
    data: dict,
    surah: int,
    ayah: int,
    quran_type: str,
    performer: str,
    ui_lang: str,
    translation_lang: str,
    choices=None,
    **opts,
) -> None:
    """Send one ayah in one representation, and remember it as the reader's position.

    Module level rather than a closure inside `handle_update`: the scheduler
    pushes a plan's daily portion outside any update, and the hifz drill reuses
    this same send — neither has an update to close over.
    """
    if quran_type in ("translation", "tafsir"):
        text = await build_verse_text(surah, ayah, quran_type, ui_lang, translation_lang, data)
        await channel.send_text(text, choices, html=True, **opts)
    elif quran_type == "arabic":
        await channel.typing("photo")
        image = catalog.image_url(surah, ayah)
        await channel.send_image(
            image,
            caption=reference(surah, ayah, ui_lang),
            choices=choices,
            cache_key=image,
            upload_action=False,
            **opts,
        )
    elif quran_type == "audio":
        await channel.typing("audio")
        audio = catalog.audio_url(surah, ayah, performer)
        await channel.send_audio(
            audio,
            title=reference(surah, ayah, ui_lang),
            performer=catalog.performer_name(performer),
            choices=choices,
            cache_key=audio,
            upload_action=False,
            **opts,
        )
    await nav_state.save(channel.chat_id, surah, ayah, quran_type)


async def deliver_combined_audio(
    channel, surah: int, start: int, end: int, performer: str, choices=None, **opts
) -> None:
    """Send a range of ayahs as a single combined audio file, cached by its range."""

    async def stitch():
        return await cdn_audio.download_combined_audio(surah, start, end, performer)

    await channel.send_audio(
        stitch,
        title="Quran %d:%d-%d" % (surah, start, end),
        performer=catalog.performer_name(performer),
        choices=choices,
        cache_key=combined_audio_key(surah, start, end, performer),
        **opts,
    )
    await nav_state.save(channel.chat_id, surah, end, "audio")


async def deliver_page(channel, page: int, ui_lang: str) -> None:
    """Send mushaf page `page` as one stitched image.

    Stitching is expensive (a few hundred KB of PNGs decoded and re-encoded), so
    the upload is cached exactly like every other media file the bot sends — the
    CDN and Pillow are touched once per page, not once per reader.
    """

    async def stitch():
        start_s, start_a, end_s, end_a = Quran.page_range(page)
        urls = [
            catalog.page_image_url(s, a)
            for s, a in Quran.ayahs_between((start_s, start_a), (end_s, end_a))
        ]
        return await fetch_and_stitch(urls, "page_%03d.jpg" % page)

    await channel.send_image(
        stitch,
        caption=page_caption(page, ui_lang),
        choices=page_keyboard(page, ui_lang),
        cache_key="page:%d" % page,
    )


async def deliver_page_audio(channel, page: int, performer: str, ui_lang: str) -> None:
    """Send the recitation of one mushaf page.

    Most reciters have a single Page<NNN>.mp3 upstream; 19 of the 79 catalog
    entries do not, and those are served by stitching the page's ayah recitations
    together instead (the same machinery an ayah range uses, generalized to cross
    surah boundaries — which a page routinely does).
    """

    async def source():
        if catalog.has_page_audio(performer):
            return catalog.page_audio_url(page, performer)
        start_s, start_a, end_s, end_a = Quran.page_range(page)
        return await cdn_audio.download_stitched_audio(
            Quran.ayahs_between((start_s, start_a), (end_s, end_a)),
            performer,
            "quran_page_%03d.mp3" % page,
        )

    await channel.send_audio(
        source,
        title=page_caption(page, ui_lang).replace("\n", " · "),
        performer=catalog.performer_name(performer),
        cache_key="pageaudio:%d:%s" % (page, performer),
    )


async def deliver_repeated_audio(
    channel, surah: int, ayah: int, performer: str, ui_lang: str, choices=None, **opts
) -> None:
    """Send one ayah recited REPEAT_COUNT times back to back, for memorization.

    No timing data is involved and none is needed: repeating an ayah is the same
    concatenation an ayah range already does, with the same ayah listed more than
    once. That also means it is exact for every reciter in the catalog rather than
    only the ones an upstream timings file happens to cover.
    """

    async def stitch():
        return await cdn_audio.download_stitched_audio(
            [(surah, ayah)] * REPEAT_COUNT,
            performer,
            "quran_%d_%d_x%d.mp3" % (surah, ayah, REPEAT_COUNT),
        )

    await channel.send_audio(
        stitch,
        title="%s ×%d" % (reference(surah, ayah, ui_lang), REPEAT_COUNT),
        performer=catalog.performer_name(performer),
        choices=choices,
        cache_key="repeat:%d:%d:%d:%s" % (REPEAT_COUNT, surah, ayah, performer),
        **opts,
    )


# --- Telegram entry points ---------------------------------------------------------
# `reply_markup` is passed through as-is (an InlineKeyboardMarkup, or None), so
# these send exactly what they sent before the channel seam existed.


async def send_quran(
    bot,
    data: dict,
    surah: int,
    ayah: int,
    quran_type: str,
    chat_id: int,
    performer: str,
    ui_lang: str,
    translation_lang: str,
    reply_markup=None,
) -> None:
    await deliver_quran(
        TelegramChannel(bot, chat_id),
        data,
        surah,
        ayah,
        quran_type,
        performer,
        ui_lang,
        translation_lang,
        reply_markup=reply_markup,
    )


async def send_combined_audio(
    bot,
    surah: int,
    start: int,
    end: int,
    chat_id: int,
    performer: str,
    reply_markup=None,
    message_thread_id=None,
) -> None:
    """`message_thread_id` targets a forum topic (the group cluster's daily post)."""
    await deliver_combined_audio(
        TelegramChannel(bot, chat_id, message_thread_id),
        surah,
        start,
        end,
        performer,
        reply_markup=reply_markup,
    )


async def send_page(bot, page: int, chat_id: int, ui_lang: str) -> None:
    await deliver_page(TelegramChannel(bot, chat_id), page, ui_lang)


async def send_page_audio(bot, page: int, chat_id: int, performer: str, ui_lang: str) -> None:
    await deliver_page_audio(TelegramChannel(bot, chat_id), page, performer, ui_lang)


async def send_repeated_audio(
    bot, surah: int, ayah: int, chat_id: int, performer: str, ui_lang: str, reply_markup=None
) -> None:
    await deliver_repeated_audio(
        TelegramChannel(bot, chat_id), surah, ayah, performer, ui_lang, reply_markup=reply_markup
    )
