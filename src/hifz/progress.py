# Workstream C — hifz progress (spec item C3).
#
# Owns: /progress (surah / juz / whole-Qur'an percentages derived from the
# interval store) and /forgot (unmark a range, splitting intervals as needed).
# Percentages are always derived arithmetic — no counter is ever stored.
# Callback prefix: "hg:" (see hifz.PREFIXES).
#
# **The headline uses two units on purpose.** The surah is quoted in *ayahs*
# ("Al-Mulk 8/30 — 27%") because that is how a surah is learned and how the spec's
# acceptance criterion is stated. The juz and the whole Qur'an are quoted in
# *mushaf pages*, because that is how a hafiz measures them: a juz is "twenty
# pages", never "431 ayahs", and by ayah count the first eight ayahs of Al-Mulk
# are 3% of juz 29 while by pages they are closer to what the reader feels. So the
# headline reads `summary.focus` (ayahs), `summary.focus_juz_pages` and
# `summary.quran_pages` (pages); the ayah-based `summary.quran` / `summary.juzs`
# stay for the breakdown beneath it, where the unit is stated by context.

import html
from typing import List, Optional, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from hifz import Ctx, callback, command
from hifz.refs import Ref, format_ref, parse_reference
from lib.hifz_progress import load_summary
from modules import Quran

__all__ = [
    "REFRESH_CB", "SURAH_PREFIX", "MAX_BREAKDOWN_ROWS",
    "progress_view", "surah_spans", "unmark",
]

# --- callback_data (Telegram caps it at 64 bytes) ------------------------------
REFRESH_CB = "hg:r"             # 4 bytes — redraw the summary in place
SURAH_PREFIX = "hg:s:"          # 5 + up to 3 = 8 bytes with "114"

# A user deep into hifz has started dozens of surahs; the breakdown is a summary,
# not a ledger. Anything past this is reachable by asking for the surah directly.
MAX_BREAKDOWN_ROWS = 8


def _surah_line(ctx: Ctx, progress) -> str:
    """One "{name}: {done}/{total} ayahs — {pct}%" line. Ayahs, always."""
    return ctx.tr("progress_surah_line",
                  name=html.escape(Quran.get_surah_name(progress.surah)),
                  done=progress.done, total=progress.total,
                  pct=progress.percent_text)


async def progress_view(ctx: Ctx, focus_surah: Optional[int] = None
                        ) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
    """The `/progress` screen: its HTML text and its keyboard (None when empty).

    `focus_surah` names the surah the headline leads with; left out, the summary
    picks the most recently marked one.
    """
    summary = await load_summary(ctx.store, ctx.user_id, focus_surah)
    if summary.is_empty:
        return ctx.tr("progress_empty"), None

    lines = ["<b>%s</b>" % html.escape(ctx.tr("progress_title")), ""]

    if summary.focus is not None:
        lines.append(_surah_line(ctx, summary.focus))
    if summary.focus_juz is not None and summary.focus_juz_pages is not None:
        # Pages, not ayahs — see the module docstring.
        lines.append(ctx.tr("progress_juz_line", n=summary.focus_juz.juz,
                            pct=summary.focus_juz_pages.percent_text))
    pages = summary.quran_pages
    lines.append(ctx.tr("progress_quran_line",
                        pct=pages.percent_text if pages is not None
                        else summary.quran.percent_text))

    focus_number = summary.focus.surah if summary.focus is not None else None
    others = [s for s in summary.surahs if s.surah != focus_number]
    if others:
        lines.append("")
        lines.extend(_surah_line(ctx, s) for s in others[:MAX_BREAKDOWN_ROWS])

    focus_juz_number = summary.focus_juz.juz if summary.focus_juz is not None else None
    # The breakdown quotes juz in ayahs. The focus juz is excluded rather than
    # repeated, because the headline already showed it in pages and two different
    # percentages for "juz 29" on one screen would read as a bug.
    juzs = [j for j in summary.juzs if j.juz != focus_juz_number]
    if juzs:
        lines.append("")
        lines.extend(ctx.tr("progress_juz_line", n=j.juz, pct=j.percent_text)
                     for j in juzs[:MAX_BREAKDOWN_ROWS])

    buttons = [InlineKeyboardButton(Quran.get_surah_name(s.surah),
                                    callback_data=SURAH_PREFIX + str(s.surah))
               for s in others[:MAX_BREAKDOWN_ROWS]]
    rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    markup = InlineKeyboardMarkup(rows) if rows else None
    return "\n".join(lines), markup


async def _show(ctx: Ctx, focus_surah: Optional[int] = None,
                prefix: str = "") -> None:
    text, markup = await progress_view(ctx, focus_surah)
    if prefix:
        text = html.escape(prefix) + "\n\n" + text
    if ctx.callback_query is not None:
        await ctx.answer()
        await ctx.edit(text, parse_mode="HTML", reply_markup=markup)
    else:
        await ctx.reply(text, parse_mode="HTML", reply_markup=markup)


@command("progress")
async def progress_command(ctx: Ctx) -> None:
    """`/progress` — the motivation line, plus the breakdown beneath it.

    An argument is accepted ("/progress 67") so the line can be pointed at a
    surah the user is not currently working through.
    """
    focus = None
    ref = parse_reference(ctx.argument) if (ctx.argument or "").strip() else None
    if ref is not None:
        focus = ref.start_surah
    await _show(ctx, focus)


@callback("hg:")
async def on_progress_tap(ctx: Ctx, cb_data: str) -> None:
    """Every "hg:" tap: refocus the summary on a surah, or redraw it.

    Parsed defensively — "hg:s:" with a missing, non-numeric or out-of-range
    number redraws the default view instead of raising.
    """
    focus = None
    if cb_data and cb_data.startswith(SURAH_PREFIX):
        payload = cb_data[len(SURAH_PREFIX):].strip()
        if payload.isdigit() and 1 <= int(payload) <= 114:
            focus = int(payload)
    await _show(ctx, focus)


# --- /forgot -------------------------------------------------------------------

def surah_spans(ref: Ref) -> List[Tuple[int, int, int]]:
    """`ref` split into one (surah, start_ayah, end_ayah) triple per surah.

    `store.hifz.remove_range` is per-surah — an interval never crosses a surah
    boundary — while a reference happily does ("/forgot 67:30-68:2", and every
    juz). Splitting here keeps that arithmetic in one place.
    """
    spans = []
    for surah in range(ref.start_surah, ref.end_surah + 1):
        start = ref.start_ayah if surah == ref.start_surah else 1
        end = (ref.end_ayah if surah == ref.end_surah
               else Quran.get_surah_length(surah))
        if start <= end:
            spans.append((surah, start, end))
    return spans


async def unmark(store, user_id: int, ref: Ref) -> bool:
    """Unmark everything `ref` covers. True if anything was actually memorized.

    The intervals are read once first, so a juz-wide `/forgot` costs one read plus
    a write per surah the user has actually touched — not 37 writes — and so the
    answer to "was any of this marked?" is known without a second count.
    `remove_range` returning [] is not that answer: it also means "the interval
    was erased whole".
    """
    intervals = await store.hifz.list_intervals(user_id)
    removed = False
    for surah, start, end in surah_spans(ref):
        if not any(row.surah == surah and row.start_ayah <= end
                   and row.end_ayah >= start for row in intervals):
            continue
        await store.hifz.remove_range(user_id, surah, start, end)
        removed = True
    return removed


@command("forgot")
async def forgot_command(ctx: Ctx) -> None:
    """`/forgot <ref>` — unmark a range, splitting the stored intervals as needed."""
    argument = (ctx.argument or "").strip()
    if not argument:
        await ctx.reply(ctx.tr("forgot_usage"))
        return
    ref = parse_reference(argument)
    if ref is None:
        await ctx.reply(ctx.tr("ref_invalid"))
        return
    if not await unmark(ctx.store, ctx.user_id, ref):
        await ctx.reply(ctx.tr("forgot_nothing"))
        return
    # The confirmation carries the updated numbers: unmarking is the one moment a
    # percentage goes down, and hiding that would make the next /progress a shock.
    await _show(ctx, ref.start_surah, prefix=ctx.tr("forgot_done",
                                                    ref=format_ref(ref)))
