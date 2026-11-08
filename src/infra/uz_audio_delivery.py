"""Sending the Uzbek translation audio to a chat (docs/MULTILINGUAL_PLAN.md §8.1).

Shared by the bot's buttons (bot/features/uz_audio.py) and the Mini App's "send
to chat" (api/uz_audio.py), so both produce the same message and share one
file_id cache entry. Lives in the infra tier because it builds channel messages
(the same tier as infra.scheduler's pushes), which `api` and `bot` may both use.

An ayah or a range is cut out of the surah mp3 with one HTTP Range request
(infra.uz_audio). A whole surah goes as Telegram's own URL fetch, or in
ayah-aligned parts when it is over Telegram's 20 MB URL limit. Every send goes
through the file_id cache, so each clip crosses our server once, in memory, and
never touches disk.
"""

from channels import Choice
from channels.telegram import TelegramChannel
from domain.quran import Quran
from infra import uz_audio
from locales import t

# Same cap as bot.limits.MAX_RANGE_AYAHS (tests/test_uz_audio_feature.py pins it):
# the API can't import `bot`, and a range clip is bounded the same way.
MAX_CLIP_AYAHS = 50


def ayah_key(surah: int, first: int, last: int) -> str:
    return "uzt:%s:%d:%d-%d" % (uz_audio.version(surah), surah, first, last)


def part_key(surah: int, index: int) -> str:
    return "uzt:%s:%d:p%d" % (uz_audio.version(surah), surah, index)


def surah_key(surah: int) -> str:
    return "uzt:%d" % surah  # the untouched upstream file: timings don't affect it


def valid_clip(surah: int, first: int, last: int) -> bool:
    """A range we can cut: timings exist, the ayahs exist, in order, not too many."""
    return (
        uz_audio.available(surah)
        and Quran.exists(surah, first)
        and Quran.exists(surah, last)
        and first <= last
        and last - first + 1 <= MAX_CLIP_AYAHS
    )


def _reference(surah: int, first: int, last: int, ui_lang: str) -> str:
    """ "Qur'on 2:284" / "Qur'on 2:284-285" (bot.text.reference, which infra can't import)."""
    span = "%d:%d" % (surah, first) + ("-%d" % last if last > first else "")
    return "%s %s" % (t("quran_name", ui_lang), span)


def _caption(surah: int, ui_lang: str, cut: bool) -> str:
    lines = [t("uza_credit", ui_lang)]
    if cut and uz_audio.estimated(surah):
        lines.append(t("uza_estimated", ui_lang))
    return "\n".join(lines)


def _clip_choices(surah: int, ayah: int, ui_lang: str):
    """◀ / ▶ to walk the translation ayah by ayah, staying inside the surah."""
    row = []
    if ayah > 1:
        row.append(Choice("◀ %d:%d" % (surah, ayah - 1), data="uz:a:%d:%d" % (surah, ayah - 1)))
    if ayah < Quran.get_surah_length(surah):
        row.append(Choice("%d:%d ▶" % (surah, ayah + 1), data="uz:a:%d:%d" % (surah, ayah + 1)))
    row.append(Choice(t("uza_btn_surah", ui_lang), data="uz:s:%d" % surah))
    return [row]


async def send_clip(channel, surah: int, first: int, last: int, ui_lang: str) -> None:
    """Ayahs first..last of the Uzbek translation, as one audio message."""
    start, end = uz_audio.byte_range(surah, first, last)

    async def build():
        return await uz_audio.fetch(surah, start, end, "uz_%d_%d-%d.mp3" % (surah, first, last))

    await channel.send_audio(
        build,
        title=_reference(surah, first, last, ui_lang) + " · " + t("uza_title", ui_lang),
        performer=t("uza_performer", ui_lang),
        caption=_caption(surah, ui_lang, cut=True),
        choices=_clip_choices(surah, last, ui_lang) if first == last else None,
        cache_key=ayah_key(surah, first, last),
    )


async def send_surah(channel, surah: int, ui_lang: str) -> None:
    """The whole surah: Telegram fetches it itself when it can, else in parts."""
    name = Quran.get_surah_name(surah)
    performer = t("uza_performer", ui_lang)
    if uz_audio.size(surah) <= uz_audio.URL_SEND_LIMIT:
        await channel.send_audio(
            uz_audio.url(surah),
            title="%d. %s · %s" % (surah, name, t("uza_title", ui_lang)),
            performer=performer,
            caption=_caption(surah, ui_lang, cut=False),
            cache_key=surah_key(surah),
        )
        return
    parts = uz_audio.parts(surah)
    for part in parts:

        async def build(part=part):
            return await uz_audio.fetch(
                surah, part.start_byte, part.end_byte, "uz_%d_part%d.mp3" % (surah, part.index)
            )

        title = t("uza_part", ui_lang).format(
            name="%d. %s" % (surah, name),
            i=part.index,
            n=len(parts),
            first=part.first_ayah,
            last=part.last_ayah,
        )
        await channel.send_audio(
            build,
            title=title,
            performer=performer,
            caption=_caption(surah, ui_lang, cut=True) if part.index == len(parts) else None,
            cache_key=part_key(surah, part.index),
        )


async def send_to_user(bot, user_id: int, surah: int, first, last, ui_lang: str) -> None:
    """The Mini App's "send to chat": a private chat's id is the user's id.

    `first` None means the whole surah."""
    channel = TelegramChannel(bot, user_id)
    if first is None:
        await send_surah(channel, surah, ui_lang)
    else:
        await send_clip(channel, surah, first, last, ui_lang)
