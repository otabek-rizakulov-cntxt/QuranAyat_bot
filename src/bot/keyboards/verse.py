"""The keyboard under every verse card.

Every verse is delivered as a self-contained "card": the verse plus an inline
keyboard that rides with it. Tapping a button fires a callback that edits the
same message in place (for the text views) rather than posting a new one, so a
reading session doesn't flood the chat with near-identical bubbles.
"""

from bot.limits import REPEAT_COUNT
from bot.miniapp import app_choice_row
from bot.text import nav_labels
from channels import Choice, Choices
from domain.quran import Quran
from infra import uz_audio
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


# UI languages that get the Uzbek translation audio buttons (MULTILINGUAL_PLAN §8.1).
UZ_AUDIO_LANGS = frozenset({"uz", "uz-Cyrl"})


def uz_audio_row(surah: int, first: int, last: int, ui_lang: str) -> Choices:
    """`[🎧 Tarjima] [📚 Sura tarjimasi]` for Uzbek users; nothing for anyone else.

    With `last > first` it is the single button for that range (a typed range
    reply, whose verse keyboard below already carries the surah button)."""
    if ui_lang not in UZ_AUDIO_LANGS or not uz_audio.available(surah):
        return []
    if last > first:
        label = "%s %d:%d-%d" % (t("uza_btn_ayah", ui_lang), surah, first, last)
        return [[Choice(label, data="uz:r:%d:%d:%d" % (surah, first, last))]]
    return [
        [
            Choice(t("uza_btn_ayah", ui_lang), data="uz:a:%d:%d" % (surah, first)),
            Choice(t("uza_btn_surah", ui_lang), data="uz:s:%d" % surah),
        ]
    ]


def verse_keyboard(
    surah: int,
    ayah: int,
    quran_type: str,
    ui_lang: str,
    app: bool = True,
    uz_audio: bool = False,
) -> Choices:
    """The keyboard attached to a verse card — localized and RTL-aware.

    Three rows: choose a view (Translation / Arabic / Tafsir / Audio, the active
    one marked with a dot), navigate (Previous / Random / Next), and act
    (Language / Share). Every button except Random and Share is a "show ayah S:A
    as T" callback, so the handler stays uniform.

    `ui_lang` only: this keyboard's labels are bot UI text, independent of the
    user's chosen translation language.

    With `uz_audio` (Telegram only: the clips are sent as Telegram audio, and a
    WhatsApp card has no room for more buttons), Uzbek UI users get one more row
    for the Uzbek translation audio (`uz_audio_row`). With the Mini App configured, a last row opens this ayah in
    it — except on an inline-mode message (`app=False`), where Telegram rejects
    web_app buttons.
    """

    def mode_button(mode: str, key: str, icon: str) -> Choice:
        label = icon + t(key, ui_lang)
        if mode == quran_type:
            label = "• " + label  # the dot marks the view you're in now
        return Choice(label, data="vc:%s:%d:%d" % (CODE_BY_TYPE[mode], surah, ayah))

    code = CODE_BY_TYPE[quran_type]
    prev_s, prev_a = Quran.get_previous_ayah(surah, ayah)
    next_s, next_a = Quran.get_next_ayah(surah, ayah)
    rnd = t("btn_random", ui_lang)
    prev_label, next_label = nav_labels(ui_lang)

    return (
        [
            [mode_button(*mode) for mode in _MODES],
            [
                Choice(prev_label, data="vc:%s:%d:%d" % (code, prev_s, prev_a)),
                Choice("🎲 " + rnd, data="vr:%s" % code),
                Choice(next_label, data="vc:%s:%d:%d" % (code, next_s, next_a)),
            ],
            [
                Choice(
                    "🔁 %s ×%d" % (t("btn_repeat", ui_lang), REPEAT_COUNT),
                    data="rep:%d:%d" % (surah, ayah),
                ),
                Choice("🌐 " + get_language(ui_lang).native, data="showlang"),
                Choice("📤", switch_inline="%d:%d" % (surah, ayah)),
            ],
        ]
        + (uz_audio_row(surah, ayah, ayah, ui_lang) if uz_audio else [])
        + (
            app_choice_row("📱 " + t("web_btn_open_app", ui_lang), "/read/%d?a=%d" % (surah, ayah))
            if app
            else []
        )
    )
