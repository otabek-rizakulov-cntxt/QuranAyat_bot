"""The /sajda list."""

from bot.keyboards.rows import button_rows
from bot.keyboards.verse import CODE_BY_TYPE
from channels import Choice, Choices
from domain.quran import Quran


def sajda_keyboard(ui_lang: str) -> Choices:
    """The 15 ayahs of prostration, each opening its verse card.

    Labelled with ۩, the mushaf's own sajda sign, so the list needs no translated
    word for "prostration" beyond its heading.
    """
    buttons = [
        Choice(
            "۩ %s %d:%d" % (Quran.get_surah_name(surah), surah, ayah),
            data="vc:%s:%d:%d" % (CODE_BY_TYPE["translation"], surah, ayah),
        )
        for surah, ayah, _kind in Quran.sajdas
    ]
    return button_rows(buttons, 2)
