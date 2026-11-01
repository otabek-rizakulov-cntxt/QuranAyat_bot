"""/start, /help, /about, /index and /app."""

from telegram import ReplyKeyboardRemove

from bot.context import Ctx
from bot.features import group as hifz_group
from bot.miniapp import app_choice_row
from bot.router import command
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
    await _welcome(ctx)


@command("app")
async def app(ctx: Ctx) -> None:
    row = app_choice_row("📱 " + t("web_btn_open_app", ctx.ui_lang), "/")
    await ctx.reply(t("web_app_intro" if row else "web_app_unavailable", ctx.ui_lang), row)


@command("about")
async def about(ctx: Ctx) -> None:
    await ctx.reply(t("about", ctx.ui_lang), html=True)


@command("index")
async def index(ctx: Ctx) -> None:
    await ctx.reply(ctx.data["index"], html=True)
