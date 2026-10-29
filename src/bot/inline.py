"""Inline mode: answering "@bot 2:255" from any chat.

A reference is answered with its translation, tafsir, recitation and Arabic
images; anything else is tried as a reciter name.
"""

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultAudio,
    InlineQueryResultCachedAudio,
    InlineQueryResultCachedPhoto,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)

from bot.keyboards.reciter import reciter_label
from bot.limits import MAX_RANGE_AYAHS
from bot.media import combined_audio_key, range_audio_url
from bot.settings import resolve_settings
from bot.text import ref_key, reference
from config.settings import get_settings
from domain.parsing import parse_ayah_range
from infra import catalog, media_cache
from lib.user_settings import UserSettings
from locales import t
from modules import Quran
from modules.quran import get_translation


def get_default_query_results(quran: Quran):
    results = []
    ayat = [
        (13, 28),
        (33, 56),
        (2, 62),
        (10, 31),
        (17, 36),
        (5, 32),
        (39, 9),
        (17, 44),
        (28, 88),
        (17, 84),
        (33, 6),
        (7, 57),
        (3, 7),
        (2, 255),
        (63, 9),
        (57, 20),
        (49, 12),
        (16, 125),
        (24, 35),
        (73, 8),
        (4, 103),
    ]
    for s, a in ayat:
        ayah = "%d:%d" % (s, a)
        english = quran.get_ayah(s, a)
        results.append(
            InlineQueryResultArticle(
                ayah + "def",
                title=ayah,
                description=english[:120],
                input_message_content=InputTextMessageContent(english),
            )
        )
    return results


# Inline answers built from the caller's own settings can't use the long shared
# cache; this only has to outlive the burst of queries Telegram fires as the user
# types, and stay short enough that changing a setting is felt straight away.
INLINE_PERSONAL_CACHE_TIME = 60


def inline_audio_result(surah: int, start: int, end: int, reciter: str, ui_lang: str):
    """The recitation of an ayah — or of a whole range, stitched into one file —
    as a shareable inline result, or None if it can't be built.

    Telegram only ever takes a file_id or a URL it fetches itself here, never an
    upload. A single ayah already has a public URL on the CDN. A range does not,
    so it is served either from the file_id an in-chat send of the same range
    left in the cache, or from our own RANGE_AUDIO_PATH.
    """
    try:
        first_url = catalog.audio_url(surah, start, reciter)
    except ValueError:
        # A saved reciter that has since left the catalog. The rest of the
        # answer is still useful, so drop the audio rather than failing.
        return None
    if not first_url.startswith(("http://", "https://")):
        # AUDIO_BASE_URL unset or pointing at a local path: neither Telegram nor
        # our own stitching route can reach it, so there is nothing to offer.
        return None

    title = reference(surah, start, ui_lang, end)
    if end > start:
        if end - start + 1 > MAX_RANGE_AYAHS:
            return None  # same bound the in-chat range send enforces
        # Bounded by 64 bytes — 4 + 11 + the longest subfolder in the catalog.
        result_id = "aur:%s:%s" % (ref_key(surah, start, end), reciter)
        cached_id = media_cache.get(combined_audio_key(surah, start, end, reciter))
        if cached_id is not None:
            # Someone has already asked for this range in a chat: replay that
            # upload instead of making Telegram fetch and stitch it again.
            return InlineQueryResultCachedAudio(result_id, audio_file_id=cached_id, caption=title)
        audio_url = range_audio_url(surah, start, end, reciter)
        if audio_url is None:
            return None  # no public base URL to stitch it from
    else:
        # Keyed by reciter as well as ayah: the same query answered before and
        # after a reciter change must not collide in Telegram's result cache.
        result_id = "au:%s:%s" % (ref_key(surah, start, end), reciter)
        audio_url = first_url
    return InlineQueryResultAudio(
        result_id, audio_url=audio_url, title=title, performer=catalog.performer_name(reciter)
    )


# A range's Arabic images come back one result per ayah; cap them so a long range
# can neither pass Telegram's 50-results-per-answer limit nor bury the translation,
# tafsir and recitation under a wall of thumbnails.
INLINE_MAX_PHOTOS = 10


def inline_photo_results(surah: int, start: int, end: int, ui_lang: str) -> list:
    """The rendered Arabic image of each ayah in the reference, as shareable inline
    photo results.

    Preferring the file_id an in-chat send left in the cache is not just a saved
    round-trip here: the Bot API documents an inline photo *URL* as having to be
    JPEG, and our rendered ayahs are PNG, so replaying a file Telegram already
    holds is also the more dependable of the two. The URL is the fallback for an
    ayah nobody has viewed yet, and needs PHOTO_BASE_URL to be a public URL; when
    it points at a local directory, only already-cached ayahs can be offered.
    """
    if not get_settings().photo_base_url:
        return []  # no images configured at all
    results = []
    for ayah in range(start, min(end, start + INLINE_MAX_PHOTOS - 1) + 1):
        result_id = "ph:%d:%d" % (surah, ayah)
        ref = reference(surah, ayah, ui_lang)
        common = dict(title=t("btn_arabic", ui_lang), description=ref, caption=ref)
        # the same key `send_quran`'s arabic branch caches under
        source = catalog.image_url(surah, ayah)
        cached_id = media_cache.get(source)
        if cached_id is not None:
            results.append(
                InlineQueryResultCachedPhoto(result_id, photo_file_id=cached_id, **common)
            )
        elif source.startswith(("http://", "https://")):
            results.append(
                InlineQueryResultPhoto(result_id, photo_url=source, thumbnail_url=source, **common)
            )
    return results


async def answer_inline_query(bot, data: dict, inline_query) -> None:
    """Answer one inline query: a reference in every representation, a reciter
    search, or the default suggestions."""
    user_settings = UserSettings()
    query_id = inline_query.id
    query = inline_query.query
    user = inline_query.from_user
    # inline users have no chat with us; key the preference by their user id
    settings = await resolve_settings(user_settings, None, user)
    ui_lang, translation_lang = settings.ui_lang, settings.translation_lang
    results = []
    cache_time = 66 * (60**2 * 24)
    is_personal = False
    # A range ("59:22-24") is answered as a range in every representation, the
    # same as in a chat — a single ayah is just the degenerate case start == end.
    surah, start, end = parse_ayah_range(query)
    if surah is not None and Quran.exists(surah, start) and Quran.exists(surah, end):
        ref = ref_key(surah, start, end)
        quran = await get_translation(translation_lang)
        if end > start:
            translation = quran.get_ayahs(surah, start, end)
            tafsir = "\n\n".join(data["tafsir"].get_ayah(surah, a) for a in range(start, end + 1))
        else:
            translation = quran.get_ayah(surah, start)
            tafsir = data["tafsir"].get_ayah(surah, start)
        # Every result here is rendered from the caller's own settings —
        # translation_lang for the text, reciter for the audio — so this
        # branch is per-user too, and cannot use a long shared cache. The
        # short cache_time still absorbs the keystroke-by-keystroke repeats
        # Telegram sends while the query is being typed.
        cache_time, is_personal = INLINE_PERSONAL_CACHE_TIME, True
        results.append(
            InlineQueryResultArticle(
                ref + "translation",
                title=t("btn_translation", ui_lang),
                description=translation[:120],
                # a long range's text can outgrow Telegram's message limit
                input_message_content=InputTextMessageContent(translation[:4096]),
            )
        )
        results.append(
            InlineQueryResultArticle(
                ref + "tafsir",
                title=t("btn_tafsir", ui_lang),
                description=tafsir[:120],
                input_message_content=InputTextMessageContent(tafsir[:4096]),
            )
        )
        audio = inline_audio_result(surah, start, end, settings.reciter, ui_lang)
        if audio is not None:
            results.append(audio)
        results.extend(inline_photo_results(surah, start, end, ui_lang))
    else:
        # Not an ayah reference — try it as a reciter name, so the picker is
        # reachable from any chat without opening a DM with the bot first.
        matches = catalog.search(query)
        if matches:
            # Unlike the immutable ayah text above, these are rendered in the
            # caller's own UI language and lead to a state change, so they must
            # not be served from a shared, long-lived cache.
            cache_time, is_personal = 0, True
            for p in matches:
                # the subfolder keys the id: two entries can share a name (same
                # reciter at different bitrates) and Telegram rejects duplicates
                results.append(
                    InlineQueryResultArticle(
                        "reciter:" + p["subfolder"],
                        title=reciter_label(p),
                        description=t("reciter_inline_description", ui_lang),
                        input_message_content=InputTextMessageContent(
                            t("reciter_set", ui_lang).format(reciter=p["name"])
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        t("btn_set_reciter", ui_lang),
                                        callback_data="setreciter:" + p["subfolder"],
                                    )
                                ]
                            ]
                        ),
                    )
                )
        else:
            results = data["default_query_results"]
    await bot.answer_inline_query(
        inline_query_id=query_id,
        cache_time=cache_time,
        results=results,
        is_personal=is_personal,
    )
