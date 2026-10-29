"""The verse reader: the card's buttons, /random, and typed references.

`read_text` is the last stop for a text message — after commands, a pending
prompt and any wizard have had their turn (see bot.dispatch).
"""

from bot.context import Ctx
from bot.errors import ignore_not_modified
from bot.keyboards.verse import TYPE_BY_CODE, verse_keyboard
from bot.limits import MAX_RANGE_AYAHS
from bot.media import send_combined_audio, send_quran, send_repeated_audio
from bot.router import callback, command
from bot.text import build_verse_text
from domain.parsing import parse_ayah_range
from infra import nav_state
from locales import button_action, t
from modules import Quran


async def reader_position(ctx: Ctx) -> tuple:
    """(surah, ayah, view) where the user stopped reading; 1:1 translation if never."""
    state = await nav_state.get(ctx.chat_id)
    if state is None:
        return 1, 1, "translation"
    surah, ayah, quran_type = state
    if quran_type == "english":  # legacy stored value -> canonical name
        quran_type = "translation"
    return surah, ayah, quran_type


async def _send_verse(ctx: Ctx, surah: int, ayah: int, quran_type: str, **kwargs) -> None:
    """send_quran with the caller's settings, under a fresh verse card."""
    await send_quran(
        ctx.bot,
        ctx.data,
        surah,
        ayah,
        quran_type,
        ctx.chat_id,
        ctx.reciter,
        ctx.ui_lang,
        ctx.translation_lang,
        reply_markup=kwargs.pop("reply_markup", None)
        or verse_keyboard(surah, ayah, quran_type, ctx.ui_lang),
    )


@command("random")
async def random_ayah(ctx: Ctx) -> None:
    _, _, quran_type = await reader_position(ctx)
    surah, ayah = Quran.get_random_ayah()
    await _send_verse(ctx, surah, ayah, quran_type)


@callback("rep:")  # "🔁 Repeat ×3" on a verse card
async def repeat(ctx: Ctx, cb_data: str) -> None:
    _, surah_s, ayah_s = cb_data.split(":", 2)
    surah, ayah = int(surah_s), int(ayah_s)
    await ctx.answer()
    if Quran.exists(surah, ayah):
        await send_repeated_audio(
            ctx.bot,
            surah,
            ayah,
            ctx.chat_id,
            ctx.reciter,
            ctx.ui_lang,
            reply_markup=verse_keyboard(surah, ayah, "audio", ctx.ui_lang),
        )


@callback("vc:", "vr:")  # a verse-card tap: vc:<view>:<surah>:<ayah>, or vr:<view> (random)
async def verse_card(ctx: Ctx, cb_data: str) -> None:
    parts = cb_data.split(":")
    if cb_data.startswith("vr:"):  # random ayah, same view
        surah, ayah = Quran.get_random_ayah()
    else:
        surah, ayah = int(parts[2]), int(parts[3])
    quran_type = TYPE_BY_CODE.get(parts[1], "translation")
    if not Quran.exists(surah, ayah):
        await ctx.answer()
        return
    message = ctx.callback_query.message
    from_inline = message is None
    markup = verse_keyboard(surah, ayah, quran_type, ctx.ui_lang, app=not from_inline)
    if quran_type in ("translation", "tafsir"):
        text = await build_verse_text(
            surah, ayah, quran_type, ctx.ui_lang, ctx.translation_lang, ctx.data
        )
        if from_inline or message.photo or message.audio:
            # can't turn a photo/audio message into text — post a fresh card
            await ctx.reply(text, parse_mode="HTML", reply_markup=markup)
        else:
            # the common path: turn the page in place; re-tapping the current
            # view yields an identical message, which is fine
            with ignore_not_modified():
                await ctx.bot.edit_message_text(
                    text=text,
                    chat_id=ctx.chat_id,
                    message_id=message.message_id,
                    parse_mode="HTML",
                    reply_markup=markup,
                )
        await nav_state.save(ctx.chat_id, surah, ayah, quran_type)
    else:  # arabic/audio arrive as fresh media messages
        await _send_verse(ctx, surah, ayah, quran_type, reply_markup=markup)
    await ctx.answer()


async def read_text(ctx: Ctx, text: str) -> None:
    """A button label from the old reply keyboard, or an ayah reference.

    `text` is lowercased. Anything else is ignored.
    """
    surah, ayah, quran_type = await reader_position(ctx)

    action = button_action(text, ctx.ui_lang)
    if action in ("arabic", "audio", "translation", "tafsir"):
        await _send_verse(ctx, surah, ayah, action)
        return
    if action in ("next", "previous", "random"):
        if action == "next":
            surah, ayah = Quran.get_next_ayah(surah, ayah)
        elif action == "previous":
            surah, ayah = Quran.get_previous_ayah(surah, ayah)
        else:
            surah, ayah = Quran.get_random_ayah()
        await _send_verse(ctx, surah, ayah, quran_type)
        return

    surah, start, end = parse_ayah_range(text)
    if not surah:
        return
    if end > start:  # a range like "53:1-7" -> one combined audio
        if not (Quran.exists(surah, start) and Quran.exists(surah, end)):
            await ctx.reply(t("ayah_not_found", ctx.ui_lang))
        elif end - start + 1 > MAX_RANGE_AYAHS:
            await ctx.reply(t("range_too_large", ctx.ui_lang).format(n=MAX_RANGE_AYAHS))
        else:
            await send_combined_audio(
                ctx.bot,
                surah,
                start,
                end,
                ctx.chat_id,
                ctx.reciter,
                reply_markup=verse_keyboard(surah, end, "audio", ctx.ui_lang),
            )
    elif Quran.exists(surah, start):
        await _send_verse(ctx, surah, start, quran_type)
    else:
        await ctx.reply(t("ayah_not_found", ctx.ui_lang))
