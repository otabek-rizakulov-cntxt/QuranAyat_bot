"""/start, /help, /about, /index and /app."""

from telegram import ReplyKeyboardRemove

from bot.context import Ctx
from bot.features import group as hifz_group
from bot.handlers.menu import show_main_menu
from bot.miniapp import app_choice_row, app_link
from bot.router import command
from channels import WHATSAPP, Choice
from locales import t, welcome_text


async def _welcome(ctx: Ctx) -> None:
    # ReplyKeyboardRemove clears the old persistent keyboard for anyone upgrading
    # from the pre-inline UI; new users never see one.
    await ctx.reply(welcome_text(ctx.ui_lang), html=True, reply_markup=ReplyKeyboardRemove())


@command("start")
async def start(ctx: Ctx) -> None:
    # A /start deep link (t.me/bot?start=gs_-100…) carries a group payload the
    # group feature owns — admin setup, or a member joining the board.
    if ctx.argument and await hifz_group.handle_start_payload(ctx, ctx.argument):
        return
    await _welcome(ctx)


@command("help")
async def help_(ctx: Ctx) -> None:
    if ctx.platform == WHATSAPP:
        # The Telegram help lists /commands and inline mode; WhatsApp gets a menu.
        await show_main_menu(ctx)
        return
    await _welcome(ctx)


@command("app")
async def app(ctx: Ctx) -> None:
    label = "📱 " + t("web_btn_open_app", ctx.ui_lang)
    if ctx.channel.caps.web_app:
        row = app_choice_row(label, "/")
    else:
        # No in-chat Mini App outside Telegram: a one-time sign-in link instead.
        link = app_link(ctx.user_id, "/")
        row = [[Choice(label, url=link)]] if link else []
    await ctx.reply(t("web_app_intro" if row else "web_app_unavailable", ctx.ui_lang), row)


@command("about")
async def about(ctx: Ctx) -> None:
    key = "wa_about" if ctx.platform == WHATSAPP else "about"
    await ctx.reply(t(key, ctx.ui_lang), html=True)


@command("index")
async def index(ctx: Ctx) -> None:
    await ctx.reply(ctx.data["index"], html=True)
