"""Tajweed lessons in Uzbek (docs/TAJWEED_PLAN.md §8).

    /tajvid                 the units
    tj:u:<unit>             a unit's lessons
    tj:l:<lesson>           a lesson card: text, marked example ayahs, 🔊 per example
    tj:p:<lesson>:<n>       play example n in the user's reciter
    tj:ok:<lesson>          reviewer: approve this exact text
    tj:no:<lesson>          reviewer: back to draft
    tj:units                back to the units

Lessons are drafts until a reviewer (settings.tajweed_reviewers) approves them;
approval is stored with the lesson's content hash, so editing the text sends it
back to draft. Everyone else sees approved lessons only. Uzbek UI only for now.
"""

import html

from bot.features import Ctx, callback, command
from bot.media import deliver_quran
from channels import Choice
from config.settings import get_settings
from domain import tajweed, tajweed_lessons

_PREFIX = "tj:"
_LANGS = tajweed_lessons.LANGS
_MAX_TEXT = 4000  # Telegram's message limit is 4096


def _reviewer(ctx: Ctx) -> bool:
    return ctx.user_id in get_settings().tajweed_reviewers


async def _visible(ctx: Ctx) -> tuple:
    """(lessons this user may see, ids of the approved ones)."""
    approvals = await ctx.store.tajweed.approvals()
    lessons = tajweed_lessons.lessons(ctx.ui_lang)
    approved = {
        x.id
        for x in lessons
        if x.id in approvals and approvals[x.id].content_hash == x.content_hash
    }
    if _reviewer(ctx):
        return lessons, approved
    return tuple(x for x in lessons if x.id in approved), approved


async def _units(ctx: Ctx, edit: bool) -> None:
    lessons, _ = await _visible(ctx)
    present = {x.unit for x in lessons}
    units = [u for u in tajweed_lessons.units(ctx.ui_lang) if u.id in present]
    if not units:
        text, choices = ctx.tr("tj_soon"), None
    else:
        text = "<b>%s</b>\n\n%s" % (ctx.tr("tj_title"), ctx.tr("tj_pick_unit"))
        choices = [[Choice(u.title, data="tj:u:" + u.id)] for u in units]
    if edit:
        await ctx.edit(text, choices, html=True)
    else:
        await ctx.reply(text, choices, html=True)


async def _unit(ctx: Ctx, unit_id: str) -> None:
    lessons, approved = await _visible(ctx)
    mine = [x for x in lessons if x.unit == unit_id]
    unit = next((u for u in tajweed_lessons.units(ctx.ui_lang) if u.id == unit_id), None)
    if unit is None or not mine:
        await _units(ctx, edit=True)
        return
    rows = [
        [
            Choice(
                x.title + ("" if x.id in approved else " · " + ctx.tr("tj_draft")),
                data="tj:l:" + x.id,
            )
        ]
        for x in mine
    ]
    rows.append([Choice(ctx.tr("tj_back"), data="tj:units")])
    await ctx.edit("<b>%s</b>" % html.escape(unit.title), rows, html=True)


def _card_text(ctx: Ctx, lesson, approved: bool) -> str:
    parts = ["<b>%s</b>" % html.escape(lesson.title), *lesson.body]
    if lesson.examples:
        parts.append("<b>%s</b>" % ctx.tr("tj_examples"))
        for n, (s, a, rules) in enumerate(lesson.examples, start=1):
            marked = tajweed.marked_html(s, a, rules) if rules else html.escape(tajweed.text(s, a))
            parts.append("%d. %s  (%d:%d)" % (n, marked, s, a))
    if _reviewer(ctx):
        parts.append(ctx.tr("tj_status_approved") if approved else ctx.tr("tj_status_draft"))
    text = "\n\n".join(parts)
    while len(text) > _MAX_TEXT and len(parts) > 2:  # drop examples from the end, never the body
        parts.pop(-2 if _reviewer(ctx) else -1)
        text = "\n\n".join(parts)
    return text


async def _lesson(ctx: Ctx, lesson_id: str) -> bool:
    """Show the lesson card; False if this user can't see that lesson (nothing sent)."""
    lessons, approved = await _visible(ctx)
    ids = [x.id for x in lessons]
    lesson = tajweed_lessons.lesson(lesson_id, ctx.ui_lang)
    if lesson is None or lesson_id not in ids:
        return False
    rows = []
    if lesson.examples:
        rows.append(
            [
                Choice("🔊 %d" % n, data="tj:p:%s:%d" % (lesson.id, n))
                for n in range(1, len(lesson.examples) + 1)
            ]
        )
    prev_id, next_id = tajweed_lessons.neighbours(lesson.id, ids)
    nav = []
    if prev_id:
        nav.append(Choice("◀", data="tj:l:" + prev_id))
    nav.append(Choice(ctx.tr("tj_back"), data="tj:u:" + lesson.unit))
    if next_id:
        nav.append(Choice("▶", data="tj:l:" + next_id))
    rows.append(nav)
    if _reviewer(ctx):
        rows.append(
            [Choice(ctx.tr("tj_unapprove"), data="tj:no:" + lesson.id)]
            if lesson.id in approved
            else [Choice(ctx.tr("tj_approve"), data="tj:ok:" + lesson.id)]
        )
    await ctx.edit(_card_text(ctx, lesson, lesson.id in approved), rows, html=True)
    return True


async def _play(ctx: Ctx, lesson_id: str, n: str) -> None:
    lessons, _ = await _visible(ctx)
    lesson = next((x for x in lessons if x.id == lesson_id), None)
    if lesson is None or not n.isdigit() or not 1 <= int(n) <= len(lesson.examples):
        await ctx.answer(ctx.tr("tj_unavailable"))
        return
    await ctx.answer()
    s, a, _ = lesson.examples[int(n) - 1]
    await deliver_quran(
        ctx.channel, ctx.data, s, a, "audio", ctx.reciter, ctx.ui_lang, ctx.translation_lang
    )


async def _review(ctx: Ctx, lesson_id: str, approve: bool) -> None:
    lesson = tajweed_lessons.lesson(lesson_id, ctx.ui_lang)
    if not _reviewer(ctx) or lesson is None:
        await ctx.answer(ctx.tr("tj_not_reviewer"))
        return
    if approve:
        await ctx.store.tajweed.approve(lesson.id, lesson.content_hash, ctx.user_id)
    else:
        await ctx.store.tajweed.revoke(lesson.id)
    await ctx.answer(ctx.tr("tj_approved_ok") if approve else ctx.tr("tj_unapproved_ok"))
    await _lesson(ctx, lesson.id)  # a reviewer always sees it


@command("tajvid")
async def tajvid(ctx: Ctx) -> None:
    if ctx.ui_lang not in _LANGS:
        await ctx.reply(ctx.tr("tj_uzbek_only"))
        return
    await _units(ctx, edit=False)


@callback(_PREFIX)
async def on_tajweed(ctx: Ctx, cb_data: str) -> None:
    """Every tj: tap. callback_data is untrusted: unknown shapes are just acknowledged."""
    if ctx.ui_lang not in _LANGS:
        await ctx.answer(ctx.tr("tj_uzbek_only"))
        return
    parts = cb_data[len(_PREFIX) :].split(":")
    kind, args = parts[0], parts[1:]
    if kind == "units":
        await ctx.answer()
        await _units(ctx, edit=True)
    elif kind == "u" and len(args) == 1:
        await ctx.answer()
        await _unit(ctx, args[0])
    elif kind == "l" and len(args) == 1:
        shown = await _lesson(ctx, args[0])
        await ctx.answer() if shown else await ctx.answer(ctx.tr("tj_unavailable"))
    elif kind == "p" and len(args) == 2:
        await _play(ctx, args[0], args[1])
    elif kind in ("ok", "no") and len(args) == 1:
        await _review(ctx, args[0], approve=kind == "ok")
    else:
        await ctx.answer()
