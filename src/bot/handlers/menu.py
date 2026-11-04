"""The WhatsApp menus' taps (bot/keyboards/menu.py).

`wm:<command>` runs that command as if it had been typed, so a menu row and the
typed word can never drift apart. `wm:menu`, `wm:settings` and `wm:read` are the
menu's own screens.
"""

from bot import router
from bot.context import Ctx
from bot.keyboards.menu import MENU, main_menu, settings_menu
from bot.router import callback


async def show_main_menu(ctx: Ctx) -> None:
    await ctx.reply(
        ctx.tr("wa_menu_body"),
        main_menu(ctx.ui_lang),
        html=True,
        header=ctx.tr("wa_menu_title"),
        footer=ctx.tr("wa_menu_footer"),
        button=ctx.tr("wa_menu_button"),
    )


@callback(MENU)
async def on_menu(ctx: Ctx, cb_data: str) -> None:
    await ctx.answer()
    name = cb_data[len(MENU) :]
    if name == "menu":
        await show_main_menu(ctx)
    elif name == "settings":
        await ctx.reply(
            ctx.tr("wa_settings_body"),
            settings_menu(ctx.ui_lang),
            header=ctx.tr("wa_menu_settings"),
            button=ctx.tr("wa_menu_button"),
        )
    elif name == "read":
        await ctx.reply(ctx.tr("wa_read_hint"), html=True)
    elif router.handles(name):
        await router.dispatch_command(ctx, name)
