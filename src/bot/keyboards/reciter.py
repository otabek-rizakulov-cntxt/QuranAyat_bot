"""The /reciter picker: tabs per recording kind, paged, with search."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.text import nav_labels
from lib.utils import File
from locales import t
from services.reciters import (
    _KIND_WARNING_KEYS,
    DEFAULT_RECITER_KIND,
    RECITER_KINDS,
    reciter_group,
    reciter_kind,
)

# How many reciters one page of the picker shows. Equal to the shortlist length, so
# page 1 is exactly the shortlist.
RECITER_PAGE_SIZE = 10


_KIND_LABEL_KEYS = {
    "recitation": "reciter_group_recitation",
    "riwayah": "reciter_group_riwayah",
    "translation": "reciter_group_translation",
}


# Icons live here rather than in the locale tables: three tabs share one keyboard
# row, so the labels have to stay short in every language, and the icon does the
# disambiguating that a longer word otherwise would.
_KIND_ICONS = {"recitation": "🎙 ", "riwayah": "📖 ", "translation": "🗣 "}


def reciter_label(performer: dict) -> str:
    """Button label for a reciter: name plus bitrate.

    The bitrate is what tells two entries of the same reciter apart, and it is
    also how much phone storage a recitation will cost — so it belongs on the
    button, not one tap away.
    """
    bitrate = performer.get("bitrate", "").replace("Kbps", "kbps")
    if not bitrate:
        return performer["name"]
    return "%s · %s" % (performer["name"], bitrate)


def reciter_page_count(kind: str = DEFAULT_RECITER_KIND) -> int:
    """How many pages one group needs. Groups are paged independently, so the
    3-entry riwayah tab is one page while recitation is seven."""
    return max(1, -(-len(reciter_group(kind)) // RECITER_PAGE_SIZE))


def reciter_page_of(subfolder: str) -> tuple[str, int]:
    """The (kind, page) holding `subfolder`, so /reciter opens where the user
    already is — including on the right tab. Falls back to the first page of the
    recitation tab for a preference no longer in the catalog."""
    kind = reciter_kind(subfolder)
    for i, p in enumerate(reciter_group(kind)):
        if p["subfolder"] == subfolder:
            return kind, i // RECITER_PAGE_SIZE
    return DEFAULT_RECITER_KIND, 0


def reciter_keyboard(
    ui_lang: str, kind: str = DEFAULT_RECITER_KIND, page: int = 0, current: str | None = None
) -> InlineKeyboardMarkup:
    """One page of one group of the reciter catalog, two per row, under a group-tab
    row, a Previous / n-of-m / Next pager and a search button.

    The catalog is ~80 entries across three kinds, so it is grouped *and* paged
    rather than dumped in one keyboard: the tabs say what kind of recording you are
    choosing, the pager walks that group, and the search button jumps straight to a
    name. Pages wrap, so neither arrow is ever a dead button. Both the active tab
    and the active reciter are marked with a dot, the same way the verse card marks
    the active view.
    """
    if kind not in RECITER_KINDS:
        kind = DEFAULT_RECITER_KIND
    entries = reciter_group(kind)
    pages = reciter_page_count(kind)
    page %= pages

    # Tab row first: what kind of recording this list is, before any of the names.
    rows = [
        [
            InlineKeyboardButton(
                ("• " if k == kind else "") + _KIND_ICONS[k] + t(_KIND_LABEL_KEYS[k], ui_lang),
                callback_data="recgrp:%s:0" % k,
            )
            for k in RECITER_KINDS
        ]
    ]

    row = []
    for p in entries[page * RECITER_PAGE_SIZE : (page + 1) * RECITER_PAGE_SIZE]:
        label = reciter_label(p)
        if p["subfolder"] == current:
            label = "• " + label
        row.append(InlineKeyboardButton(label, callback_data="setreciter:" + p["subfolder"]))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    prev_label, next_label = nav_labels(ui_lang)
    rows.append(
        [
            InlineKeyboardButton(
                prev_label, callback_data="recgrp:%s:%d" % (kind, (page - 1) % pages)
            ),
            InlineKeyboardButton("%d/%d" % (page + 1, pages), callback_data="recpage_noop"),
            InlineKeyboardButton(
                next_label, callback_data="recgrp:%s:%d" % (kind, (page + 1) % pages)
            ),
        ]
    )
    rows.append(
        [
            InlineKeyboardButton(
                "🔍 " + t("btn_search_reciter", ui_lang), callback_data="reciter_search"
            )
        ]
    )
    return InlineKeyboardMarkup(rows)


def reciter_set_confirmation(subfolder: str, ui_lang: str) -> str:
    """The "reciter set" message, with a warning appended when the chosen entry is
    not ordinary Arabic recitation.

    Said at the moment of choosing rather than buried in the picker: this is the
    point where someone could otherwise silently stop hearing the Qur'an recited.
    """
    text = t("reciter_set", ui_lang).format(reciter=File.get_performer_name(subfolder))
    warning_key = _KIND_WARNING_KEYS.get(reciter_kind(subfolder))
    if warning_key is not None:
        text += "\n\n" + t(warning_key, ui_lang)
    return text
