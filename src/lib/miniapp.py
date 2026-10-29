# Links from the bot into the Mini App (docs/MINI_APP_PLAN.md §7).
#
# Everything here is off until MINIAPP_URL is set: no button, no menu entry, so
# the bot behaves exactly as before on a deployment without the app.
#
# `web_app` buttons open the app *inside* Telegram with signed initData, and are
# only allowed in private chats — never on an inline-mode message, which is why
# callers that may be editing one (the verse card) can switch them off.

from typing import Optional

from telegram import InlineKeyboardButton, MenuButtonWebApp, WebAppInfo

from config.settings import get_settings


def app_url(path: str = "/") -> Optional[str]:
    """The Mini App URL for an app route ("/read/2?a=255"), or None when unset."""
    base = (get_settings().miniapp_url or "").rstrip("/")
    if not base:
        return None
    return base + (path if path.startswith("/") else "/" + path)


def app_button(label: str, path: str = "/") -> Optional[InlineKeyboardButton]:
    url = app_url(path)
    return InlineKeyboardButton(label, web_app=WebAppInfo(url=url)) if url else None


def app_row(label: str, path: str = "/") -> list:
    """`[[button]]` to append to a keyboard's rows, or `[]` when the app is off."""
    button = app_button(label, path)
    return [[button]] if button is not None else []


async def set_menu_button(bot) -> bool:
    """Make the chat menu button open the app, for every user. False if off."""
    url = app_url("/")
    if url is None:
        return False
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="📖 Open", web_app=WebAppInfo(url=url))
    )
    return True
