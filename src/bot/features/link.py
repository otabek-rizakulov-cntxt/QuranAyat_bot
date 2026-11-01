"""Linking a Telegram account and a WhatsApp number (MULTI_PLATFORM_PLAN Phase 6).

    link           -> a six-digit code to send from the other app
    link 123456    -> joins the two accounts
    unlink         -> separates them again

The Telegram account is the one that is kept: the WhatsApp number is re-pointed
at the Telegram user id, so from then on both apps read and write the same plan,
progress, streak and settings. What the WhatsApp number had built on its own
stays under its old id, untouched but no longer reachable — nothing is merged
row by row, so nothing can be merged wrongly. Scheduled pushes go to Telegram
(the account's home platform); the old WhatsApp-only verse of the day stops.
"""

from bot.features import Ctx, command
from channels import TELEGRAM, WHATSAPP
from infra import account_link
from infra.store.identity import NON_TELEGRAM_ID_START


def _is_telegram_id(user_id: int) -> bool:
    return user_id < NON_TELEGRAM_ID_START


@command("link")
async def link(ctx: Ctx) -> None:
    code = ctx.argument.strip()
    if not code:
        await ctx.reply(ctx.tr("link_code", code=account_link.issue(ctx.user_id)), html=True)
        return
    if account_link.too_many_tries(ctx.user_id):
        await ctx.reply(ctx.tr("link_too_many"))
        return
    other = account_link.redeem(code, ctx.user_id)
    if other is None:
        await ctx.reply(ctx.tr("link_bad_code"))
        return
    pair = {ctx.user_id, other}
    telegram_ids = [u for u in pair if _is_telegram_id(u)]
    if len(pair) != 2 or len(telegram_ids) != 1:
        await ctx.reply(ctx.tr("link_same"))  # both codes from the same side
        return
    telegram_id = telegram_ids[0]
    (whatsapp_id,) = pair - {telegram_id}
    row = await ctx.store.identity.get_by_user(whatsapp_id, WHATSAPP)
    if row is None or not await ctx.store.identity.relink(WHATSAPP, row.external_id, telegram_id):
        await ctx.reply(ctx.tr("link_taken"))
        return
    # The number's own daily pushes belonged to the account it no longer is.
    await ctx.store.daily.set_enabled(whatsapp_id, False)
    await ctx.reply(ctx.tr("link_done"))


@command("unlink")
async def unlink(ctx: Ctx) -> None:
    if ctx.platform == WHATSAPP:
        row = await ctx.store.identity.get_by_user(ctx.user_id, WHATSAPP)
        linked = row is not None and _is_telegram_id(row.user_id)
        if linked:
            await ctx.store.identity.unlink(WHATSAPP, row.external_id)
    elif ctx.platform == TELEGRAM:
        row = await ctx.store.identity.get_by_user(ctx.user_id, WHATSAPP)
        linked = row is not None
        if linked:
            await ctx.store.identity.unlink(WHATSAPP, row.external_id)
    else:
        linked = False
    await ctx.reply(ctx.tr("link_unlinked" if linked else "link_not_linked"))
