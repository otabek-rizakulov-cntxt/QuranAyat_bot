# Workstream G — streaks & activity graph (spec items G2, G3).
#
# Owns: /streak, the 12-week activity graph, and the fixed milestone copy at
# 7 / 30 / 100 / 365 days. A day ticks when a session is completed, never when a
# command is typed, so the grid is bot-measured throughout.
# Callback prefix: "hs:" (see hifz.PREFIXES).
#
# **The grid is a PNG, not an emoji block.** §4 G2 and assumption 1 called for an
# emoji grid; that was overridden with approval and `lib/streak_image.py` renders
# a real contribution graph. An emoji grid wraps at a different column on every
# client; a PNG is one image that looks the same everywhere, and it is the thing
# people screenshot into their circle.
#
# **No percentile line exists here.** G3 holds the "top X% of users" claim dark
# until >=200 users have a streak. `streak_summary` takes a `population` argument
# that this module never passes, so `summary.percentile` is None on every path,
# and there is no string in the table to render it with anyway.
#
# The rendered PNG is cached by Telegram `file_id` per (user, local date) — see
# `streak_image.cache_key` — through the same `File.save_file` / `File.get_file`
# pair `main.send_file` uses, so hammering /streak costs one render a day.

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from hifz import Ctx, callback, command
from lib.streak_image import cache_key, render_streak_graph
from lib.streaks import StreakSummary, streak_summary

# --- callback_data shapes ------------------------------------------------------
# hs:grid   re-send the graph card (for other screens to link to) — 7 bytes
CB_GRID = "hs:grid"

# The check module's "start a check" tap, spelled out rather than imported: the
# seam guarantees one broken feature module cannot take another down, and an
# import here would give that guarantee back. See hifz.PREFIXES ("hc:").
CB_CHECK_START = "hc:start"


@command("streak")
async def streak(ctx: Ctx) -> None:
    """`/streak` — current, longest, milestone copy, and the 12-week graph."""
    summary = await streak_summary(ctx.user_id)     # no population: G3 stays dark

    if summary.current == 0 and summary.longest == 0:
        # Nothing has ever been logged. An all-grey card is an honest picture but
        # a discouraging one, and it costs a render; the invitation is better.
        await ctx.reply("%s\n\n%s" % (ctx.tr("streak_title"), ctx.tr("streak_none")),
                        reply_markup=_keyboard(ctx, summary))
        return

    await _send_graph(ctx, summary)


@callback("hs:")
async def on_streak(ctx: Ctx, cb_data: str) -> None:
    """Every "hs:" tap. Parsed defensively; an unknown shape is just acknowledged."""
    await ctx.answer()
    if cb_data == CB_GRID:
        await streak(ctx)


def _caption(ctx: Ctx, summary: StreakSummary) -> str:
    """Title, both counters, and the milestone line on the day it is reached.

    `milestone.reached` is set only when the streak *equals* a milestone, so the
    congratulation fires once instead of every day after day seven.
    """
    lines = [ctx.tr("streak_title"),
             ctx.tr("streak_current", n=summary.current),
             ctx.tr("streak_longest", n=summary.longest)]
    if summary.milestone.reached is not None:
        lines.append(ctx.tr(summary.milestone.key))
    lines.append(ctx.tr("streak_graph_caption"))
    return "\n".join(lines)


def _keyboard(ctx: Ctx, summary: StreakSummary):
    """A way to earn today, offered only while today is still unearned.

    The recall check is the one path that works for a user with no plan, so it is
    the right button to put under a streak that is about to break.
    """
    if summary.active_today:
        return None
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(ctx.tr("btn_check_start"), callback_data=CB_CHECK_START)]])


async def _send_graph(ctx: Ctx, summary: StreakSummary) -> None:
    """Send the graph, preferring a cached file_id over a fresh render.

    Same shape as `main.send_file`: try the cached id, and treat Telegram
    rejecting it as a cache miss rather than an error — a file_id can go stale,
    and a user must never see a failed /streak because of it.
    """
    caption = _caption(ctx, summary)
    markup = _keyboard(ctx, summary)
    key = cache_key(ctx.user_id, summary.today)

    cached = ctx.file.get_file(key)
    if cached is not None:
        try:
            await ctx.bot.send_photo(chat_id=ctx.chat_id, photo=cached,
                                     caption=caption, reply_markup=markup)
            return
        except telegram.error.TelegramError:
            print("streak: cached graph file_id rejected for %s; re-rendering" % (key,))

    graph = await render_streak_graph(ctx.user_id, today=summary.today)
    message = await ctx.bot.send_photo(chat_id=ctx.chat_id, photo=graph,
                                       caption=caption, reply_markup=markup)

    photo = getattr(message, "photo", None)
    if photo:
        # Largest size last, as main.send_file does.
        ctx.file.save_file(key, photo[-1].file_id)
