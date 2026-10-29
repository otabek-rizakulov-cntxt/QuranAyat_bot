"""The mushaf page reader's pager.

The page, not the ayah, is the unit people actually read and memorize in. A page
card is one stitched image of the whole page (see lib/page_image.py) under a
1-604 pager, with its recitation one tap away rather than attached — a page of
audio is ~1 MB nobody asked for if they only wanted to read.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.verse import CODE_BY_TYPE
from bot.text import nav_labels
from lib.miniapp import app_row
from locales import t
from modules import Quran


def page_keyboard(page: int, ui_lang: str) -> InlineKeyboardMarkup:
    """Pager over the mushaf, plus this page's recitation and a way back into the
    per-ayah reader. Pages wrap at both ends, like the reciter picker's."""
    total = Quran.PAGE_COUNT
    previous = page - 1 if page > 1 else total
    following = page + 1 if page < total else 1
    start_s, start_a, _, _ = Quran.page_range(page)
    prev_label, next_label = nav_labels(ui_lang)
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(prev_label, callback_data="pg:%d" % previous),
                InlineKeyboardButton("%d/%d" % (page, total), callback_data="pgnoop"),
                InlineKeyboardButton(next_label, callback_data="pg:%d" % following),
            ],
            [
                InlineKeyboardButton(
                    "🔊 " + t("btn_audio", ui_lang), callback_data="pga:%d" % page
                ),
                InlineKeyboardButton(
                    "📖 " + t("btn_ayah_view", ui_lang),
                    callback_data="vc:%s:%d:%d" % (CODE_BY_TYPE["translation"], start_s, start_a),
                ),
            ],
        ]
        + app_row("📱 " + t("web_btn_open_app", ui_lang), "/mushaf/%d" % page)
    )
