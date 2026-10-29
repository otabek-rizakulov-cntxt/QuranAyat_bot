"""The mushaf page reader: /page, /juz, /sajda and the pager's taps."""

from bot.context import Ctx
from bot.handlers.reader import reader_position
from bot.keyboards.sajda import sajda_keyboard
from bot.media import send_page, send_page_audio
from bot.router import callback, command
from domain.parsing import as_int
from domain.quran import Quran
from locales import t


@command("page")
async def page(ctx: Ctx) -> None:
    # bare /page opens where the reader already is, rather than erroring
    if ctx.argument:
        number = as_int(ctx.argument)
    else:
        surah, ayah, _ = await reader_position(ctx)
        number = Quran.page_of(surah, ayah)
    if number is None or not 1 <= number <= Quran.PAGE_COUNT:
        await ctx.reply(t("page_out_of_range", ctx.ui_lang).format(total=Quran.PAGE_COUNT))
        return
    await send_page(ctx.bot, number, ctx.chat_id, ctx.ui_lang)


@command("juz")
async def juz(ctx: Ctx) -> None:
    if ctx.argument:
        number = as_int(ctx.argument)
    else:
        surah, ayah, _ = await reader_position(ctx)
        number = Quran.juz_of(surah, ayah)
    if number is None or not 1 <= number <= Quran.JUZ_COUNT:
        await ctx.reply(t("juz_out_of_range", ctx.ui_lang).format(total=Quran.JUZ_COUNT))
        return
    # a juz is ~20 pages of reading, so it opens the page reader at its first
    # page rather than trying to be a single message or audio file
    start_s, start_a, _, _ = Quran.juz_range(number)
    await send_page(ctx.bot, Quran.page_of(start_s, start_a), ctx.chat_id, ctx.ui_lang)


@command("sajda")
async def sajda(ctx: Ctx) -> None:
    await ctx.reply(t("sajda_list_title", ctx.ui_lang), reply_markup=sajda_keyboard(ctx.ui_lang))


@callback("pg:")  # the mushaf pager
async def turn_page(ctx: Ctx, cb_data: str) -> None:
    number = int(cb_data.split(":", 1)[1])
    await ctx.answer()
    if 1 <= number <= Quran.PAGE_COUNT:
        # a page arrives as an image, so it is a fresh message rather than an
        # edit of the one that was tapped
        await send_page(ctx.bot, number, ctx.chat_id, ctx.ui_lang)


@callback("pga:")  # "listen to this page"
async def page_audio(ctx: Ctx, cb_data: str) -> None:
    number = int(cb_data.split(":", 1)[1])
    await ctx.answer()
    if 1 <= number <= Quran.PAGE_COUNT:
        await send_page_audio(ctx.bot, number, ctx.chat_id, ctx.reciter, ctx.ui_lang)
