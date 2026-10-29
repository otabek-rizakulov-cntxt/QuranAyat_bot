"""/language and /translation, and the taps that set them."""

from telegram import ReplyKeyboardRemove

from bot.context import Ctx
from bot.keyboards.language import language_keyboard, translation_language_keyboard
from bot.router import callback, command
from locales import get_language, normalize_lang, t
from services.user_settings import UserSettings


@command("language")
async def language(ctx: Ctx) -> None:
    await ctx.reply(t("choose_language", ctx.ui_lang), reply_markup=language_keyboard())


@command("translation")
async def translation(ctx: Ctx) -> None:
    await ctx.reply(
        t("choose_translation_language", ctx.ui_lang), reply_markup=translation_language_keyboard()
    )


@callback("showlang")  # the 🌐 button on a verse card
async def show_languages(ctx: Ctx, cb_data: str) -> None:
    await ctx.answer()
    await ctx.reply(t("choose_language", ctx.ui_lang), reply_markup=language_keyboard())


@callback("setlang:")  # UI language picked from the /language keyboard
async def set_ui_language(ctx: Ctx, cb_data: str) -> None:
    # normalize_lang already refuses translation-only codes (there is no string
    # table to show the interface in), falling back to English.
    code = normalize_lang(cb_data.split(":", 1)[1])
    await UserSettings().set_ui_lang(ctx.user_id, ctx.chat_id, code)
    await ctx.answer()
    confirm = t("language_set", code).format(lang=get_language(code).native)
    # ReplyKeyboardRemove clears the persistent keyboard left over from the
    # pre-inline UI for anyone upgrading; new users never had one.
    await ctx.reply(confirm, reply_markup=ReplyKeyboardRemove())


@callback("settranslang:")  # translation language picked from /translation
async def set_translation_language(ctx: Ctx, cb_data: str) -> None:
    code = normalize_lang(cb_data.split(":", 1)[1])
    await UserSettings().set_translation_lang(ctx.user_id, ctx.chat_id, code)
    await ctx.answer()
    await ctx.reply(
        t("translation_language_set", ctx.ui_lang).format(lang=get_language(code).native)
    )
