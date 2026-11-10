"""Tajweed lessons in Uzbek, in two tracks (docs/TAJWEED_PLAN.md).

    /tajvid                 the tracks (straight to the units when only one is open)
    tj:units                back to that start screen
    tj:t:<track>            a track's units: alifbo (audio lessons) or qoidalar (rules)
    tj:u:<unit>             a unit's lessons, ✓ on the ones done
    tj:l:<lesson>           a lesson card
    tj:a:<lesson>           send an audio lesson (alifbo)
    tj:d:<lesson>           ✅ Oʻqidim: mark the lesson done (a streak session, once)
    tj:p:<lesson>:<n>       play example n of a rules lesson in the user's reciter
    tj:ok:<lesson>          reviewer: approve this exact text
    tj:no:<lesson>          reviewer: back to draft

Who may open what is services.tajweed (shared with the Mini App API): the audio
track once its base URL is configured, rules lessons once approved (drafts for
reviewers). Uzbek UI only for now.
"""

import html

from bot.features import Ctx, callback, command
from bot.media import deliver_quran
from channels import Choice
from domain import tajweed, tajweed_lessons
from domain.tajweed_lessons import TRACK_AUDIO, TRACK_RULES
from services import tajweed as service

_PREFIX = "tj:"
_LANGS = tajweed_lessons.LANGS
_MAX_TEXT = 4000  # Telegram's message limit is 4096
_TRACK_KEYS = {TRACK_AUDIO: "tj_track_alifbo", TRACK_RULES: "tj_track_qoidalar"}


async def _rules_visible(ctx: Ctx) -> tuple:
    """(rules lessons this user may see, ids of the approved ones)."""
    approved = await service.approved_ids(ctx.store)
    lessons = tajweed_lessons.lessons(ctx.ui_lang)
    if service.is_reviewer(ctx.user_id):
        return lessons, approved
    return tuple(x for x in lessons if x.id in approved), approved


async def _say(ctx: Ctx, edit: bool, text: str, choices) -> None:
    if edit:
        await ctx.edit(text, choices, html=True)
    else:
        await ctx.reply(text, choices, html=True)


async def _start(ctx: Ctx, edit: bool) -> None:
    tracks = await service.visible_tracks(ctx.store, ctx.user_id)
    if not tracks:
        await _say(ctx, edit, ctx.tr("tj_soon"), None)
    elif len(tracks) == 1:
        await _track(ctx, tracks[0], edit, alone=True)
    else:
        text = "<b>%s</b>\n\n%s" % (ctx.tr("tj_title"), ctx.tr("tj_pick_track"))
        choices = [[Choice(ctx.tr(_TRACK_KEYS[t]), data="tj:t:" + t)] for t in tracks]
        await _say(ctx, edit, text, choices)


async def _track(ctx: Ctx, track: str, edit: bool = True, alone: bool = False) -> None:
    if track not in await service.visible_tracks(ctx.store, ctx.user_id):
        await _start(ctx, edit)
        return
    done = await ctx.store.tajweed.done(ctx.user_id)
    if track == TRACK_AUDIO:
        units, lessons = tajweed_lessons.audio_units(ctx.ui_lang), tajweed_lessons.audio_lessons()
    else:
        units, lessons = tajweed_lessons.units(ctx.ui_lang), (await _rules_visible(ctx))[0]
    rows = []
    for u in units:
        mine = [x.id for x in lessons if x.unit == u.id]
        if mine:
            count = sum(1 for i in mine if i in done)
            rows.append([Choice("%s  %d/%d" % (u.title, count, len(mine)), data="tj:u:" + u.id)])
    if not alone:
        rows.append([Choice(ctx.tr("tj_tracks"), data="tj:units")])
    text = "<b>%s</b>\n\n%s" % (ctx.tr(_TRACK_KEYS[track]), ctx.tr("tj_pick_unit"))
    await _say(ctx, edit, text, rows)


def _unit_track(unit_id: str):
    if any(u.id == unit_id for u in tajweed_lessons.audio_units()):
        return TRACK_AUDIO
    if any(u.id == unit_id for u in tajweed_lessons.units()):
        return TRACK_RULES
    return None


async def _unit(ctx: Ctx, unit_id: str) -> None:
    track = _unit_track(unit_id)
    if track is None or track not in await service.visible_tracks(ctx.store, ctx.user_id):
        await _start(ctx, edit=True)
        return
    done = await ctx.store.tajweed.done(ctx.user_id)
    if track == TRACK_AUDIO:
        units = tajweed_lessons.audio_units(ctx.ui_lang)
        mine = [x for x in tajweed_lessons.audio_lessons(ctx.ui_lang) if x.unit == unit_id]
        approved = {x.id for x in mine}
        per_row = 2 if len(mine) > 8 else 1  # the 28 letters fit as two columns
    else:
        units = tajweed_lessons.units(ctx.ui_lang)
        lessons, approved = await _rules_visible(ctx)
        mine = [x for x in lessons if x.unit == unit_id]
        per_row = 1
    unit = next(u for u in units if u.id == unit_id)
    buttons = [
        Choice(
            ("✓ " if x.id in done else "")
            + x.title
            + ("" if x.id in approved else " · " + ctx.tr("tj_draft")),
            data="tj:l:" + x.id,
        )
        for x in mine
    ]
    rows = [buttons[i : i + per_row] for i in range(0, len(buttons), per_row)]
    rows.append([Choice(ctx.tr("tj_back"), data="tj:t:" + track)])
    await ctx.edit("<b>%s</b>" % html.escape(unit.title), rows, html=True)


def _rules_text(ctx: Ctx, lesson, approved: bool) -> str:
    parts = ["<b>%s</b>" % html.escape(lesson.title), *lesson.body]
    if lesson.examples:
        parts.append("<b>%s</b>" % ctx.tr("tj_examples"))
        for n, (s, a, rules) in enumerate(lesson.examples, start=1):
            marked = tajweed.marked_html(s, a, rules) if rules else html.escape(tajweed.text(s, a))
            parts.append("%d. %s  (%d:%d)" % (n, marked, s, a))
    reviewer = service.is_reviewer(ctx.user_id)
    if reviewer:
        parts.append(ctx.tr("tj_status_approved") if approved else ctx.tr("tj_status_draft"))
    text = "\n\n".join(parts)
    while len(text) > _MAX_TEXT and len(parts) > 2:  # drop examples from the end, never the body
        parts.pop(-2 if reviewer else -1)
        text = "\n\n".join(parts)
    return text


def _done_row(ctx: Ctx, lesson_id: str, done: set) -> list:
    if lesson_id in done:
        return [Choice(ctx.tr("tj_done_already"), data="tj:d:" + lesson_id)]
    return [Choice(ctx.tr("tj_mark_done"), data="tj:d:" + lesson_id)]


def _nav_row(ctx: Ctx, lesson_id: str, unit_id: str, ids: list) -> list:
    prev_id, next_id = tajweed_lessons.neighbours(lesson_id, ids)
    nav = []
    if prev_id:
        nav.append(Choice("◀", data="tj:l:" + prev_id))
    nav.append(Choice(ctx.tr("tj_back"), data="tj:u:" + unit_id))
    if next_id:
        nav.append(Choice("▶", data="tj:l:" + next_id))
    return nav


def _duration(seconds: float) -> str:
    s = int(round(seconds))
    return "%d:%02d" % (s // 60, s % 60)


async def _lesson(ctx: Ctx, lesson_id: str) -> bool:
    """Show the lesson card; False if this user can't open that lesson (nothing sent)."""
    if not await service.can_open(ctx.store, ctx.user_id, lesson_id):
        return False
    done = await ctx.store.tajweed.done(ctx.user_id)
    audio = tajweed_lessons.audio_lesson(lesson_id, ctx.ui_lang)
    if audio is not None:
        unit = next(u for u in tajweed_lessons.audio_units(ctx.ui_lang) if u.id == audio.unit)
        text = "<b>%s</b>\n<i>%s</i> · %s" % (
            html.escape(audio.title),
            html.escape(unit.title),
            _duration(audio.seconds),
        )
        ids = [x.id for x in tajweed_lessons.audio_lessons()]
        rows = [
            [Choice(ctx.tr("tj_listen"), data="tj:a:" + audio.id)],
            _done_row(ctx, audio.id, done),
            _nav_row(ctx, audio.id, audio.unit, ids),
        ]
        await ctx.edit(text, rows, html=True)
        return True

    lessons, approved = await _rules_visible(ctx)
    lesson = tajweed_lessons.lesson(lesson_id, ctx.ui_lang)
    rows = []
    if lesson.examples:
        rows.append(
            [
                Choice("🔊 %d" % n, data="tj:p:%s:%d" % (lesson.id, n))
                for n in range(1, len(lesson.examples) + 1)
            ]
        )
    rows.append(_done_row(ctx, lesson.id, done))
    rows.append(_nav_row(ctx, lesson.id, lesson.unit, [x.id for x in lessons]))
    if service.is_reviewer(ctx.user_id):
        rows.append(
            [Choice(ctx.tr("tj_unapprove"), data="tj:no:" + lesson.id)]
            if lesson.id in approved
            else [Choice(ctx.tr("tj_approve"), data="tj:ok:" + lesson.id)]
        )
    await ctx.edit(_rules_text(ctx, lesson, lesson.id in approved), rows, html=True)
    return True


async def _listen(ctx: Ctx, lesson_id: str) -> None:
    audio = tajweed_lessons.audio_lesson(lesson_id, ctx.ui_lang)
    base = service.audio_base()
    if audio is None or base is None:
        await ctx.answer(ctx.tr("tj_unavailable"))
        return
    await ctx.answer()
    await ctx.channel.send_audio(
        tajweed_lessons.audio_url(audio, base),
        title=audio.title,
        performer=ctx.tr("tj_track_alifbo"),
        caption="🎧 " + audio.title,
        cache_key="tjm:" + audio.sha256[:12],
    )


async def _mark_done(ctx: Ctx, lesson_id: str) -> None:
    if not await service.can_open(ctx.store, ctx.user_id, lesson_id):
        await ctx.answer(ctx.tr("tj_unavailable"))
        return
    outcome = await service.complete(ctx.store, ctx.user_id, lesson_id)
    if outcome is None:
        await ctx.answer(ctx.tr("tj_done_already"))
        return
    await ctx.answer(ctx.tr("tj_done_ok").format(days=outcome.streak.current))
    await _lesson(ctx, lesson_id)  # the button turns into ✓


async def _play(ctx: Ctx, lesson_id: str, n: str) -> None:
    lessons, _ = await _rules_visible(ctx)
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
    if not service.is_reviewer(ctx.user_id) or lesson is None:
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
    await _start(ctx, edit=False)


@callback(_PREFIX)
async def on_tajweed(ctx: Ctx, cb_data: str) -> None:
    """Every tj: tap. callback_data is untrusted: unknown shapes are just acknowledged."""
    if ctx.ui_lang not in _LANGS:
        await ctx.answer(ctx.tr("tj_uzbek_only"))
        return
    parts = cb_data[len(_PREFIX) :].split(":")
    kind, args = parts[0], parts[1:]
    if kind == "units" and not args:
        await ctx.answer()
        await _start(ctx, edit=True)
    elif kind == "t" and len(args) == 1 and args[0] in _TRACK_KEYS:
        await ctx.answer()
        await _track(ctx, args[0])
    elif kind == "u" and len(args) == 1:
        await ctx.answer()
        await _unit(ctx, args[0])
    elif kind == "l" and len(args) == 1:
        shown = await _lesson(ctx, args[0])
        await ctx.answer() if shown else await ctx.answer(ctx.tr("tj_unavailable"))
    elif kind == "a" and len(args) == 1:
        await _listen(ctx, args[0])
    elif kind == "d" and len(args) == 1:
        await _mark_done(ctx, args[0])
    elif kind == "p" and len(args) == 2:
        await _play(ctx, args[0], args[1])
    elif kind in ("ok", "no") and len(args) == 1:
        await _review(ctx, args[0], approve=kind == "ok")
    else:
        await ctx.answer()
