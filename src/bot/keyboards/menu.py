"""The WhatsApp main menu and settings menu (list messages, ≤10 rows each).

Telegram has a slash-command menu and the /help text; WhatsApp people tap a list
instead. A row's `wm:<command>` runs that command (bot/handlers/menu.py); the
rest reuse existing callbacks, so they behave exactly as the same button would.
"""

from channels import Choice, Choices
from locales import t

MENU = "wm:"


def _rows(lang: str, items) -> Choices:
    return [[Choice(t(label, lang), data=data, hint=t(hint, lang))] for label, hint, data in items]


def main_menu(lang: str) -> Choices:
    return _rows(
        lang,
        (
            ("wa_menu_read", "wa_menu_read_hint", MENU + "read"),
            ("wa_menu_daily", "wa_menu_daily_hint", "hd:now"),
            ("wa_menu_random", "wa_menu_random_hint", MENU + "random"),
            ("wa_menu_index", "wa_menu_index_hint", MENU + "index"),
            ("wa_menu_page", "wa_menu_page_hint", MENU + "page"),
            ("wa_menu_memorize", "wa_menu_memorize_hint", MENU + "memorize"),
            ("wa_menu_progress", "wa_menu_progress_hint", MENU + "progress"),
            ("wa_menu_app", "wa_menu_app_hint", MENU + "app"),
            ("wa_menu_settings", "wa_menu_settings_hint", MENU + "settings"),
            ("wa_menu_about", "wa_menu_about_hint", MENU + "about"),
        ),
    )


def settings_menu(lang: str) -> Choices:
    return _rows(
        lang,
        (
            ("wa_set_language", "wa_set_language_hint", "showlang"),
            ("wa_set_translation", "wa_set_translation_hint", MENU + "translation"),
            ("wa_set_reciter", "wa_set_reciter_hint", MENU + "reciter"),
            ("wa_set_daily", "wa_set_daily_hint", MENU + "daily"),
            ("wa_set_link", "wa_set_link_hint", MENU + "link"),
            ("wa_set_back", "wa_set_back_hint", MENU + "menu"),
        ),
    )


def welcome_choices(lang: str) -> Choices:
    """The three buttons on the first-contact card."""
    return [
        [
            Choice(t("wa_btn_today", lang), data="hd:now"),
            Choice(t("wa_btn_menu", lang), data=MENU + "menu"),
            Choice(t("wa_btn_language", lang), data="showlang"),
        ]
    ]
