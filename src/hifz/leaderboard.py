# Workstream H — weekly leaderboard (spec items H1, H2).
#
# Owns: /leaderboard. Ranks sessions completed in the Mon->Sun week local to the
# user (see lib/localtime.week_bounds), ties broken by streak length, opted-in
# users only. The caller's own row is always shown, even outside the top N.
# Callback prefix: "hl:" (see hifz.PREFIXES).
#
# Three things this module deliberately does *not* do:
#
#   * It does not filter. `lib.leaderboard.weekly_board` composes two store
#     queries that join on `leaderboard_opt_in`, so an opted-out user is absent
#     from the data, not hidden by this renderer. A renderer that filtered would
#     leak a position count and would put a private user on a public list the
#     first time someone forgot a template.
#   * It does not draw the caller twice. `WeeklyBoard.me_in_top` says whether
#     their row is already among `entries`; the extra "you" row is drawn only
#     when it is not.
#   * It does not own the opt-in. Workstream B (src/hifz/profile.py) owns that
#     flow; this offers a button into it and names /profile in the copy, so the
#     user has a path even if the button's owner is not loaded.
#
# Messages here are plain text, never parse_mode="HTML": display names are
# user-supplied, and the surest way to keep a name out of the markup parser is to
# have no markup parser. Nothing is escaped because nothing is interpreted.

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from hifz import Ctx, callback, command
from lib.leaderboard import weekly_board

# --- callback_data shapes ------------------------------------------------------
# hl:me     re-send the board (for other screens to link to) — 5 bytes
CB_ME = "hl:me"

# Workstream B's opt-in tap. Spelled out rather than imported so a broken profile
# module cannot take the board down with it; see hifz.PREFIXES ("hp:board:on").
CB_JOIN = "hp:board:on"

# A row for an opted-in user who somehow has no display name. B2 sets one at
# opt-in, so this is a belt, not a case — but printing a raw telegram user id on
# a public board because a name was missing is not an acceptable failure mode.
ANONYMOUS = "—"


@command("leaderboard")
async def leaderboard(ctx: Ctx) -> None:
    """`/leaderboard` — this week's global board, in DM."""
    text, markup = await _board_message(ctx)
    await ctx.reply(text, reply_markup=markup)


@callback("hl:")
async def on_leaderboard(ctx: Ctx, cb_data: str) -> None:
    """Every "hl:" tap. Parsed defensively; an unknown shape is just acknowledged."""
    await ctx.answer()
    if cb_data == CB_ME:
        await leaderboard(ctx)


async def _board_message(ctx: Ctx):
    """(text, reply_markup) for the current week as this caller sees it."""
    board = await weekly_board(ctx.user_id)
    lines = [ctx.tr("leaderboard_title")]

    if not board.entries:
        lines.append(ctx.tr("leaderboard_empty"))
    else:
        lines.extend(ctx.tr("leaderboard_row", rank=entry.position,
                            name=entry.display_name or ANONYMOUS,
                            sessions=entry.sessions)
                     for entry in board.entries)

    # H2: always show where the caller stands — but only once. `me_in_top` is
    # exactly the "did I already draw this row" answer.
    if board.me is not None and not board.me_in_top:
        lines.append(ctx.tr("leaderboard_you_row", rank=board.me.position,
                            sessions=board.me.sessions))

    markup = None
    if not board.opted_in:
        lines.append(ctx.tr("leaderboard_not_opted_in"))
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(ctx.tr("btn_join_board"), callback_data=CB_JOIN)]])

    return "\n".join(lines), markup
