"""Sending Quran media to a chat, through the Telegram file_id cache.

Every sender tries the file_id Telegram gave us last time first and only
uploads (and caches the new id) on a miss or a rejected id.
"""

import logging
from urllib.parse import urlencode

import telegram

from bot.keyboards.page import page_keyboard
from bot.limits import REPEAT_COUNT
from bot.text import build_verse_text, page_caption, reference
from config.settings import get_settings
from domain.quran import Quran
from infra import audio as cdn_audio
from infra import catalog, media_cache, nav_state
from lib.page_image import fetch_and_stitch

logger = logging.getLogger(__name__)

_UPLOAD_ACTION = {
    "photo": telegram.constants.ChatAction.UPLOAD_PHOTO,
    "audio": telegram.constants.ChatAction.UPLOAD_VOICE,
}


async def _send(bot, kind: str, source, **kwargs) -> str:
    """Send a photo or an audio file and return the file_id Telegram assigned."""
    if kind == "photo":
        result = await bot.send_photo(photo=source, **kwargs)
        return result.photo[-1].file_id
    result = await bot.send_audio(audio=source, **kwargs)
    return result.audio.file_id


async def send_cached(
    bot, kind: str, key: str, build, *, chat_id: int, upload_action: bool = True, **kwargs
) -> str:
    """Send media through the file_id cache: replay the id cached under `key`,
    or — on a miss, or when Telegram rejects the cached id (e.g. expired) —
    upload what `build()` returns and cache the new id under `key`.

    `kind` is "photo" or "audio". `build` is a coroutine function, called only
    when an upload is needed, returning a URL or a file-like object. On an upload
    the chat sees "uploading…" first, unless `upload_action=False` (when the
    caller has shown it already).
    """
    cached_id = media_cache.get(key)
    if cached_id is not None:
        try:
            return await _send(bot, kind, cached_id, chat_id=chat_id, **kwargs)
        except telegram.error.TelegramError as err:
            # a file_id can go stale; treat the rejection as a miss, not a failure
            logger.warning("cached file_id for %s rejected (%s); re-uploading", key, err)

    if upload_action:
        await bot.send_chat_action(chat_id=chat_id, action=_UPLOAD_ACTION[kind])
    file_id = await _send(bot, kind, await build(), chat_id=chat_id, **kwargs)
    media_cache.save(key, file_id)
    return file_id


async def send_file(bot, filename, quran_type, **kwargs):
    """Send one ayah's image or recitation, keyed and uploaded by its URL."""

    async def source():
        return filename

    kind = {"arabic": "photo", "audio": "audio"}[quran_type]
    return await send_cached(bot, kind, filename, source, upload_action=False, **kwargs)


def combined_audio_key(surah: int, start: int, end: int, performer: str) -> str:
    """Telegram file_id cache key for a stitched range, shared by the in-chat send
    that produces it and the inline result that replays it."""
    return "combined:%d:%d-%d:%s" % (surah, start, end, performer)


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
    """Send a range of ayahs as a single combined audio file, cached by Telegram file_id.

    `message_thread_id` targets a forum topic (the group cluster's daily post);
    left None it posts to the chat as before.
    """
    kwargs = dict(
        title="Quran %d:%d-%d" % (surah, start, end),
        performer=catalog.performer_name(performer),
        reply_markup=reply_markup,
    )
    if message_thread_id is not None:
        kwargs["message_thread_id"] = message_thread_id

    async def stitch():
        return await cdn_audio.download_combined_audio(surah, start, end, performer)

    key = combined_audio_key(surah, start, end, performer)
    await send_cached(bot, "audio", key, stitch, chat_id=chat_id, **kwargs)
    await nav_state.save(chat_id, surah, end, "audio")


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


async def send_page(bot, page: int, chat_id: int, ui_lang: str) -> None:
    """Send mushaf page `page` as one stitched image.

    Stitching is expensive (a few hundred KB of PNGs decoded and re-encoded), so
    the upload is cached by Telegram file_id exactly like every other media file
    the bot sends — the CDN and Pillow are touched once per page, not once per
    reader.
    """

    async def stitch():
        start_s, start_a, end_s, end_a = Quran.page_range(page)
        urls = [
            catalog.page_image_url(s, a)
            for s, a in Quran.ayahs_between((start_s, start_a), (end_s, end_a))
        ]
        return await fetch_and_stitch(urls, "page_%03d.jpg" % page)

    await send_cached(
        bot,
        "photo",
        "page:%d" % page,
        stitch,
        chat_id=chat_id,
        caption=page_caption(page, ui_lang),
        reply_markup=page_keyboard(page, ui_lang),
    )


async def send_page_audio(bot, page: int, chat_id: int, performer: str, ui_lang: str) -> None:
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

    await send_cached(
        bot,
        "audio",
        "pageaudio:%d:%s" % (page, performer),
        source,
        chat_id=chat_id,
        title=page_caption(page, ui_lang).replace("\n", " · "),
        performer=catalog.performer_name(performer),
    )


async def send_repeated_audio(
    bot, surah: int, ayah: int, chat_id: int, performer: str, ui_lang: str, reply_markup=None
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

    await send_cached(
        bot,
        "audio",
        "repeat:%d:%d:%d:%s" % (REPEAT_COUNT, surah, ayah, performer),
        stitch,
        chat_id=chat_id,
        title="%s ×%d" % (reference(surah, ayah, ui_lang), REPEAT_COUNT),
        performer=catalog.performer_name(performer),
        reply_markup=reply_markup,
    )


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
    """Send one ayah in one representation, and remember it as the reader's position.

    Module level rather than a closure inside `handle_update`: the scheduler
    pushes a plan's daily portion outside any update, and the hifz drill reuses
    this same send — neither has a `handle_update` frame to close over. `bot`
    and `data` are therefore explicit leading parameters.
    """
    if quran_type in ("translation", "tafsir"):
        text = await build_verse_text(surah, ayah, quran_type, ui_lang, translation_lang, data)
        await bot.send_message(
            chat_id=chat_id, text=text, parse_mode="HTML", reply_markup=reply_markup
        )
    elif quran_type == "arabic":
        await bot.send_chat_action(
            chat_id=chat_id, action=telegram.constants.ChatAction.UPLOAD_PHOTO
        )
        image = catalog.image_url(surah, ayah)
        await send_file(
            bot,
            image,
            quran_type,
            chat_id=chat_id,
            caption=reference(surah, ayah, ui_lang),
            reply_markup=reply_markup,
        )
    elif quran_type == "audio":
        await bot.send_chat_action(
            chat_id=chat_id, action=telegram.constants.ChatAction.UPLOAD_VOICE
        )
        audio = catalog.audio_url(surah, ayah, performer)
        await send_file(
            bot,
            audio,
            quran_type,
            chat_id=chat_id,
            performer=catalog.performer_name(performer),
            title=reference(surah, ayah, ui_lang),
            reply_markup=reply_markup,
        )
    await nav_state.save(chat_id, surah, ayah, quran_type)
