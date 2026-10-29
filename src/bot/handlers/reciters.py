"""/reciter: the picker, its tabs and pager, search, and choosing one."""

from bot.context import Ctx
from bot.errors import ignore_not_modified
from bot.keyboards.reciter import reciter_keyboard, reciter_page_of, reciter_set_confirmation
from bot.router import callback, command
from infra import pending_input
from locales import t
from services.user_settings import UserSettings


@command("reciter")
async def reciter(ctx: Ctx) -> None:
    # open on the tab and page the current reciter is on, with it marked
    kind, page = reciter_page_of(ctx.reciter)
    await ctx.reply(
        t("choose_reciter", ctx.ui_lang),
        reply_markup=reciter_keyboard(ctx.ui_lang, kind, page, current=ctx.reciter),
    )


@callback("recgrp:")  # a group tab or the pager on the picker
async def turn_page(ctx: Ctx, cb_data: str) -> None:
    _, kind, page_s = cb_data.split(":", 2)
    await ctx.answer()
    message = ctx.callback_query.message
    if message is None:
        return  # no message of ours to turn the page in
    with ignore_not_modified():  # swap the keyboard, don't post a new list
        await ctx.bot.edit_message_reply_markup(
            chat_id=ctx.chat_id,
            message_id=message.message_id,
            reply_markup=reciter_keyboard(ctx.ui_lang, kind, int(page_s), current=ctx.reciter),
        )


@callback("reciter_search")  # the search button on the reciter picker
async def start_search(ctx: Ctx, cb_data: str) -> None:
    pending_input.expect(ctx.chat_id, "reciter_search")
    await ctx.answer()
    await ctx.reply(t("reciter_search_prompt", ctx.ui_lang))


@callback("setreciter:")  # picked from the picker, search results or an inline card
async def set_reciter(ctx: Ctx, cb_data: str) -> None:
    subfolder = cb_data.split(":", 1)[1]
    from_inline = ctx.callback_query.message is None
    await UserSettings().set_reciter(ctx.user_id, None if from_inline else ctx.chat_id, subfolder)
    confirm = reciter_set_confirmation(subfolder, ctx.ui_lang)
    if from_inline:
        # DMing someone who never started the bot raises Forbidden; the callback
        # answer reaches them wherever the card was shared instead.
        await ctx.bot.answer_callback_query(ctx.callback_query.id, text=confirm)
    else:
        await ctx.answer()
        await ctx.reply(confirm)
