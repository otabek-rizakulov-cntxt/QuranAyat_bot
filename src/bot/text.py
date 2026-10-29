"""Message text shared by the reader: references, captions, verse bodies."""

import html

from locales import DEFAULT_LANG, get_language, t
from modules import Quran
from modules.quran import get_translation


def reference(surah: int, ayah: int, ui_lang: str, end: int | None = None) -> str:
    """Human-readable reference in the user's UI language: "Qur'an 2:255", or
    "Qur'an 59:22-24" when `end` names a later ayah."""
    name = t("quran_name", ui_lang)
    if end is not None and end > ayah:
        return "%s %d:%d-%d" % (name, surah, ayah, end)
    return "%s %d:%d" % (name, surah, ayah)


def ref_key(surah: int, start: int, end: int) -> str:
    """Compact ASCII form of a reference, used to build inline result ids."""
    if end > start:
        return "%d:%d-%d" % (surah, start, end)
    return "%d:%d" % (surah, start)


def nav_labels(ui_lang: str) -> tuple[str, str]:
    """(previous, next) button labels. The arrows point in reading order, so they
    flip for right-to-left scripts."""
    prev, nxt = t("btn_previous", ui_lang), t("btn_next", ui_lang)
    if get_language(ui_lang).rtl:
        return prev + " ›", "‹ " + nxt
    return "‹ " + prev, nxt + " ›"


def page_caption(page: int, ui_lang: str) -> str:
    """ "Page 255 of 604" over the ayah span it covers, e.g. "Qur'an 13:43 - 14:5"."""
    start_s, start_a, end_s, end_a = Quran.page_range(page)
    name = t("quran_name", ui_lang)
    if start_s == end_s:
        span = "%s %d:%d-%d" % (name, start_s, start_a, end_a)
    else:  # the page crosses into the next surah
        span = "%s %d:%d - %d:%d" % (name, start_s, start_a, end_s, end_a)
    return "%s\n%s" % (t("page_label", ui_lang).format(n=page, total=Quran.PAGE_COUNT), span)


async def build_verse_text(
    surah: int, ayah: int, quran_type: str, ui_lang: str, translation_lang: str, data: dict
) -> str:
    """HTML body for a text-view card: a bold surah-name header over the verse.

    Only the (untrusted) corpus text is HTML-escaped; the header is the sole tag
    and sits at the very start, so truncating an over-long tafsir at Telegram's
    4096-char limit can never split a tag.

    `ui_lang` drives the (English-only-tafsir) note text; `translation_lang`
    drives which translation corpus a "translation" view is read from — the two
    are independent settings.
    """
    if quran_type == "tafsir":
        body = data["tafsir"].get_ayah(surah, ayah)
        if ui_lang != DEFAULT_LANG:  # tafsir is English-only; note it
            body += t("tafsir_en_note", ui_lang)
    else:
        quran = await get_translation(translation_lang)
        body = quran.get_ayah(surah, ayah)
    header = "<b>%s</b>" % html.escape(Quran.get_surah_name(surah))
    return (header + "\n\n" + html.escape(body))[:4096]
