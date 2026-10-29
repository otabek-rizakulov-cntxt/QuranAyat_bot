"""The keyboard under every verse card.

Every verse is delivered as a self-contained "card": the verse plus an inline
keyboard that rides with it. Tapping a button fires a callback that edits the
same message in place (for the text views) rather than posting a new one, so a
reading session doesn't flood the chat with near-identical bubbles.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.limits import REPEAT_COUNT
from bot.text import nav_labels
from domain.quran import Quran
from lib.miniapp import app_row
from locales import get_language, t

# Short codes keep callback_data tiny (Telegram caps it at 64 bytes).
TYPE_BY_CODE = {"tr": "translation", "ar": "arabic", "tf": "tafsir", "au": "audio"}


CODE_BY_TYPE = {v: k for k, v in TYPE_BY_CODE.items()}


# Mode row, in display order. Only Audio carries an icon: it's the one entry that
# *plays* something rather than being another way to read the same verse.
_MODES = (
    ("translation", "btn_translation", ""),
    ("arabic", "btn_arabic", ""),
    ("tafsir", "btn_tafsir", ""),
    ("audio", "btn_audio", "🔊 "),
)


def verse_keyboard(
    surah: int, ayah: int, quran_type: str, ui_lang: str, app: bool = True
) -> InlineKeyboardMarkup:
    """The inline keyboard attached to a verse card — localized and RTL-aware.

    Three rows: choose a view (Translation / Arabic / Tafsir / Audio, the active
    one marked with a dot), navigate (Previous / Random / Next), and act
    (Language / Share). Every button except Random and Share is a "show ayah S:A
    as T" callback, so the handler stays uniform.

    `ui_lang` only: this keyboard's labels are bot UI text, independent of the
    user's chosen translation language.

    With the Mini App configured, a fourth row opens this ayah in it — except on
    an inline-mode message (`app=False`), where Telegram rejects web_app buttons.
    """

    def mode_button(mode: str, key: str, icon: str) -> InlineKeyboardButton:
        label = icon + t(key, ui_lang)
        if mode == quran_type:
            label = "• " + label  # the dot marks the view you're in now
        return InlineKeyboardButton(
            label, callback_data="vc:%s:%d:%d" % (CODE_BY_TYPE[mode], surah, ayah)
        )

    code = CODE_BY_TYPE[quran_type]
    prev_s, prev_a = Quran.get_previous_ayah(surah, ayah)
    next_s, next_a = Quran.get_next_ayah(surah, ayah)
    rnd = t("btn_random", ui_lang)
    prev_label, next_label = nav_labels(ui_lang)

    return InlineKeyboardMarkup(
        [
            [mode_button(*mode) for mode in _MODES],
            [
                InlineKeyboardButton(
                    prev_label, callback_data="vc:%s:%d:%d" % (code, prev_s, prev_a)
                ),
                InlineKeyboardButton("🎲 " + rnd, callback_data="vr:%s" % code),
                InlineKeyboardButton(
                    next_label, callback_data="vc:%s:%d:%d" % (code, next_s, next_a)
                ),
            ],
            [
                InlineKeyboardButton(
                    "🔁 %s ×%d" % (t("btn_repeat", ui_lang), REPEAT_COUNT),
                    callback_data="rep:%d:%d" % (surah, ayah),
                ),
                InlineKeyboardButton(
                    "🌐 " + get_language(ui_lang).native, callback_data="showlang"
                ),
                InlineKeyboardButton("📤", switch_inline_query="%d:%d" % (surah, ayah)),
            ],
        ]
        + (
            app_row("📱 " + t("web_btn_open_app", ui_lang), "/read/%d?a=%d" % (surah, ayah))
            if app
            else []
        )
    )
