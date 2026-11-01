"""The mushaf page reader's pager.

The page, not the ayah, is the unit people actually read and memorize in. A page
card is one stitched image of the whole page (see infra/page_image.py) under a
1-604 pager, with its recitation one tap away rather than attached — a page of
audio is ~1 MB nobody asked for if they only wanted to read.
"""

from bot.keyboards.verse import CODE_BY_TYPE
from bot.miniapp import app_choice_row
from bot.text import nav_labels
from channels import Choice, Choices
from domain.quran import Quran
from locales import t


def page_keyboard(page: int, ui_lang: str) -> Choices:
    """Pager over the mushaf, plus this page's recitation and a way back into the
    per-ayah reader. Pages wrap at both ends, like the reciter picker's."""
    total = Quran.PAGE_COUNT
    previous = page - 1 if page > 1 else total
    following = page + 1 if page < total else 1
    start_s, start_a, _, _ = Quran.page_range(page)
    prev_label, next_label = nav_labels(ui_lang)
    return [
        [
            Choice(prev_label, data="pg:%d" % previous),
            Choice("%d/%d" % (page, total), data="pgnoop"),
            Choice(next_label, data="pg:%d" % following),
        ],
        [
            Choice("🔊 " + t("btn_audio", ui_lang), data="pga:%d" % page),
            Choice(
                "📖 " + t("btn_ayah_view", ui_lang),
                data="vc:%s:%d:%d" % (CODE_BY_TYPE["translation"], start_s, start_a),
            ),
        ],
    ] + app_choice_row("📱 " + t("web_btn_open_app", ui_lang), "/mushaf/%d" % page)
