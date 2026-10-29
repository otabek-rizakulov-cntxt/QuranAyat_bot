# Workstream B — profile & registration (spec items B1-B3).
#
# Owns: /profile, the leaderboard opt-in and display name, and the timezone +
# reminder-time capture that the streak day boundary and the scheduler depend on.
# Callback prefix: "hp:" (see hifz.PREFIXES). Wizard kinds: prefix them "profile_".
#
# Three things here are deliberate and worth knowing before changing them:
#
#   * **The card is the screen.** Every tap edits the same message in place and
#     answers with a one-line toast, so a user changing three settings ends up
#     with one message, not seven. The wizards (a typed name, a typed reminder
#     time) are the only paths that send a fresh message, because a typed answer
#     has already pushed the card up the chat.
#   * **Nothing is asked that has not been asked for.** A brand-new user has no
#     name, no timezone, no reminder and no plan; every line has an explicit
#     "unset" string and `/profile` renders for someone who has used nothing else.
#   * **The offset picker and the reminder parser are public** (`offset_keyboard`,
#     `offset_from_callback`, `parse_reminder_time`, `reminder_keyboard`,
#     `save_timezone`, `save_reminder_time`). B3 says timezone and reminder time
#     are captured *once*, during first plan setup — which lives in `memorize.py`
#     — and changed later from here. Both call sites must behave identically, so
#     there is one implementation and the callback prefix is a parameter: the plan
#     wizard passes its own ("hm:tz:") and keeps routing its own taps.

import html
from typing import Optional, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.rows import button_rows
from hifz import Ctx, callback, command, wizard
from lib.localtime import is_valid_offset, normalize_offset, offset_options
from services.profile import (  # noqa: F401 — re-exported (see __all__)
    NAME_MAX,
    NAME_MIN,
    active_plan_progress,
    format_reminder_time,
    join_leaderboard,
    next_push_utc,
    parse_reminder_time,
    plan_target,
    save_reminder_time,
    save_timezone,
    valid_display_name,
)

__all__ = [
    "NAME_MIN",
    "NAME_MAX",
    "PROFILE_CB",
    "NAME_CB",
    "BOARD_ON_CB",
    "BOARD_OFF_CB",
    "TIMEZONE_CB",
    "OFFSET_PREFIX",
    "REMINDER_CB",
    "REMINDER_OFF_CB",
    "WIZARD_NAME",
    "WIZARD_REMINDER",
    "offset_keyboard",
    "offset_from_callback",
    "reminder_keyboard",
    "parse_reminder_time",
    "format_reminder_time",
    "save_timezone",
    "save_reminder_time",
    "next_push_utc",
    "valid_display_name",
    "telegram_username",
    "profile_view",
]

# 2-32 characters (B2). Long enough for "Abu Bakr as-Siddiq", short enough that a
# leaderboard row still fits on a phone. Uniqueness is deliberately not required.

# --- callback_data (Telegram caps it at 64 bytes) ------------------------------
# The shapes documented in `hifz.PREFIXES` ("hp:name  hp:board:on  hp:tz
# hp:tz:+05:00  hp:rem"), because another module already spells one of them out
# rather than importing it: `hifz/leaderboard.py` puts "hp:board:on" under its
# own "join the board" button so a broken profile module cannot take the board
# down with it. Every shape is under 13 bytes and every one is parsed
# defensively — a keyboard never expires, so a tap can arrive years after the
# message that carried it.
PROFILE_CB = "hp:main"  #  7 bytes — (re)draw the card; doubles as "cancel"
NAME_CB = "hp:name"  #  7 bytes — start the display-name wizard
BOARD_ON_CB = "hp:board:on"  # 11 bytes — join the leaderboard
BOARD_OFF_CB = "hp:board:off"  # 12 bytes — leave it
TIMEZONE_CB = "hp:tz"  #  5 bytes — show the offset picker
OFFSET_PREFIX = "hp:tz:"  #  6 + up to 6 = 12 bytes with "+05:00"
REMINDER_CB = "hp:rem"  #  6 bytes — start the reminder-time wizard
REMINDER_OFF_CB = "hp:rem:off"  # 10 bytes — turn reminders off

WIZARD_NAME = "profile_name"
WIZARD_REMINDER = "profile_reminder"


# --- Display names -------------------------------------------------------------


def telegram_username(ctx: Ctx) -> Optional[str]:
    """The caller's `@username`, without the "@", or None if they have none.

    Read off whichever update the Ctx was built from. Plenty of Telegram accounts
    have no username at all, which is exactly why B2 has a typed fallback.
    """
    for source in (ctx.callback_query, ctx.message):
        user = getattr(source, "from_user", None)
        name = getattr(user, "username", None)
        if name:
            cleaned = str(name).lstrip("@").strip()
            if cleaned:
                return cleaned
    return None


# --- The UTC-offset picker (B3) ------------------------------------------------


def offset_keyboard(
    ui_lang: str, prefix: str = OFFSET_PREFIX, columns: int = 4, cancel_data: Optional[str] = None
) -> InlineKeyboardMarkup:
    """The 34-offset picker, as an inline keyboard.

    The labels *are* the offsets ("+05:00"), so this keyboard needs no
    translation — half the reason the fixed-offset model was chosen over IANA
    zone names. `prefix` is what each button's callback_data starts with, so
    another wizard can own its own taps: `offset_keyboard(lang, prefix="hm:tz:")`.
    `cancel_data` adds a trailing Cancel row when given.
    """
    from locales import t

    buttons = [
        InlineKeyboardButton(offset, callback_data=prefix + offset) for offset in offset_options()
    ]
    rows = button_rows(buttons, columns)
    if cancel_data:
        rows.append([InlineKeyboardButton(t("btn_cancel", ui_lang), callback_data=cancel_data)])
    return InlineKeyboardMarkup(rows)


def offset_from_callback(cb_data: str, prefix: str = OFFSET_PREFIX) -> Optional[str]:
    """The normalized offset a picker tap carries ("+05:00"), or None.

    None for anything that is not this prefix, or whose payload is not a real
    offset — a keyboard is never expired by Telegram, so this input is untrusted
    even when we built the keyboard ourselves.
    """
    if not cb_data or not cb_data.startswith(prefix):
        return None
    payload = cb_data[len(prefix) :].strip()
    if not payload or not is_valid_offset(payload):
        return None
    return normalize_offset(payload)


# --- Reminder time (B3) --------------------------------------------------------


def reminder_keyboard(
    ui_lang: str, off_data: str = REMINDER_OFF_CB, cancel_data: Optional[str] = None
) -> InlineKeyboardMarkup:
    """The keyboard under `reminder_prompt`: turn reminders off, or back out.

    The time itself is typed, not picked — a picker for 1,440 minutes is either
    24 buttons and wrong for anyone who wants 07:30, or a two-step drill-down for
    something a person can type in three seconds. `off_data` and `cancel_data`
    are parameters so another wizard can route the same keyboard to itself.
    """
    from locales import t

    rows = [[InlineKeyboardButton(t("btn_reminder_off", ui_lang), callback_data=off_data)]]
    if cancel_data:
        rows.append([InlineKeyboardButton(t("btn_cancel", ui_lang), callback_data=cancel_data)])
    return InlineKeyboardMarkup(rows)


# --- The card (B1) -------------------------------------------------------------


async def _plan_line(ctx: Ctx) -> str:
    progress = await active_plan_progress(ctx.store, ctx.user_id)
    if progress is None:
        return ctx.tr("profile_plan_none")
    plan, day, total = progress
    return ctx.tr(
        "profile_plan_active", target=html.escape(plan_target(plan)), day=day, total=total
    )


async def profile_view(ctx: Ctx) -> Tuple[str, InlineKeyboardMarkup]:
    """The `/profile` card: its HTML text and its keyboard.

    Every field has an unset state, so this renders for a user who has never used
    any other feature — which is B1's done-when.
    """
    profile = await ctx.store.profiles.ensure_profile(ctx.user_id)

    lines = ["<b>%s</b>" % html.escape(ctx.tr("profile_title")), ""]
    if profile.display_name:
        # The one piece of user-supplied text on the screen: escaped here, exactly
        # as `main.build_verse_text` escapes corpus text, and stored raw.
        lines.append(ctx.tr("profile_name_set", name=html.escape(profile.display_name)))
    else:
        lines.append(ctx.tr("profile_name_unset"))
    lines.append(
        ctx.tr(
            "profile_leaderboard_on" if profile.leaderboard_opt_in else "profile_leaderboard_off"
        )
    )
    if profile.timezone and is_valid_offset(profile.timezone):
        lines.append(ctx.tr("profile_timezone_set", offset=normalize_offset(profile.timezone)))
    else:
        lines.append(ctx.tr("profile_timezone_unset"))
    if profile.reminder_time is not None:
        lines.append(
            ctx.tr("profile_reminder_set", time=format_reminder_time(profile.reminder_time))
        )
    else:
        lines.append(ctx.tr("profile_reminder_unset"))
    lines.append(await _plan_line(ctx))

    board_button = (
        InlineKeyboardButton(ctx.tr("btn_leave_board"), callback_data=BOARD_OFF_CB)
        if profile.leaderboard_opt_in
        else InlineKeyboardButton(ctx.tr("btn_join_board"), callback_data=BOARD_ON_CB)
    )
    markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(ctx.tr("btn_edit_name"), callback_data=NAME_CB)],
            [board_button],
            [InlineKeyboardButton(ctx.tr("btn_edit_timezone"), callback_data=TIMEZONE_CB)],
            [InlineKeyboardButton(ctx.tr("btn_edit_reminder"), callback_data=REMINDER_CB)],
        ]
    )
    return "\n".join(lines), markup


async def _show_card(ctx: Ctx, prefix: str = "", toast: Optional[str] = None) -> None:
    """Draw the card: in place on a tap, as a fresh message otherwise.

    `prefix` is a confirmation line that rides above the card when the change came
    from typed input (where a toast has nowhere to appear); `toast` is the same
    confirmation for a tap.
    """
    text, markup = await profile_view(ctx)
    if prefix:
        text = html.escape(prefix) + "\n\n" + text
    if ctx.callback_query is not None:
        await ctx.answer(toast)
        await ctx.edit(text, parse_mode="HTML", reply_markup=markup)
    else:
        await ctx.reply(text, parse_mode="HTML", reply_markup=markup)


# --- /profile ------------------------------------------------------------------


@command("profile")
async def profile_command(ctx: Ctx) -> None:
    """`/profile` — name, leaderboard status, timezone, reminder and plan."""
    ctx.wiz.clear(ctx.user_id)  # a command always escapes a pending wizard
    await _show_card(ctx)


# --- The taps ------------------------------------------------------------------


@callback("hp:")
async def on_profile_tap(ctx: Ctx, cb_data: str) -> None:
    """Every "hp:" tap. Unrecognized data redraws the card rather than failing:
    a stale keyboard from an older build must not leave a dead button."""
    offset = offset_from_callback(cb_data)
    if offset is not None:
        await save_timezone(ctx.store, ctx.user_id, offset)
        await _show_card(ctx, toast=ctx.tr("timezone_saved", offset=offset))
        return

    action = (cb_data or "")[len("hp:") :]

    if action in ("name", "n"):
        ctx.wiz.start(ctx.user_id, WIZARD_NAME, join=False)
        await ctx.answer()
        await ctx.edit(ctx.tr("name_prompt"), reply_markup=_cancel_keyboard(ctx))
        return

    if action in ("board:on", "b:1"):
        await _join_board(ctx)
        return

    if action in ("board:off", "b:0"):
        await ctx.store.profiles.set_leaderboard_opt_in(ctx.user_id, False)
        ctx.wiz.clear(ctx.user_id)
        await _show_card(ctx, toast=ctx.tr("board_left"))
        return

    if action == "tz":
        await ctx.answer()
        await ctx.edit(
            ctx.tr("timezone_prompt"),
            reply_markup=offset_keyboard(ctx.ui_lang, cancel_data=PROFILE_CB),
        )
        return

    if action in ("rem", "r"):
        ctx.wiz.start(ctx.user_id, WIZARD_REMINDER)
        await ctx.answer()
        await ctx.edit(
            ctx.tr("reminder_prompt"),
            reply_markup=reminder_keyboard(ctx.ui_lang, cancel_data=PROFILE_CB),
        )
        return

    if action in ("rem:off", "r:off"):
        await save_reminder_time(ctx.store, ctx.user_id, None)
        ctx.wiz.clear(ctx.user_id)
        await _show_card(ctx, toast=ctx.tr("reminder_off"))
        return

    # "hp:main", and anything unrecognized: back to the card, wizard abandoned.
    ctx.wiz.clear(ctx.user_id)
    await _show_card(ctx)


def _cancel_keyboard(ctx: Ctx) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(ctx.tr("btn_cancel"), callback_data=PROFILE_CB)]]
    )


# --- Leaderboard opt-in (B2) ---------------------------------------------------


async def _join_board(ctx: Ctx) -> None:
    """Opt in, adopting the Telegram @username when there is one.

    Someone with no username — a large minority of Telegram accounts — is asked
    for a name instead, and only joins once they have supplied one. Nobody is put
    on a public board under a blank label.
    """
    if not await join_leaderboard(ctx.store, ctx.user_id, telegram_username(ctx)):
        ctx.wiz.start(ctx.user_id, WIZARD_NAME, join=True)
        await ctx.answer()
        await ctx.edit(ctx.tr("name_prompt"), reply_markup=_cancel_keyboard(ctx))
        return
    await _show_card(ctx, toast=ctx.tr("board_joined"))


@wizard(WIZARD_NAME)
async def name_step(ctx: Ctx, text: str) -> None:
    """The typed display name."""
    name = valid_display_name(text)
    if name is None:
        # The draft stays in flight: a too-long name is a retry, not a dead end.
        await ctx.reply(ctx.tr("name_invalid", min=NAME_MIN, max=NAME_MAX))
        return
    join = bool(ctx.wiz.data(ctx.user_id).get("join"))
    ctx.wiz.clear(ctx.user_id)
    await ctx.store.profiles.set_display_name(ctx.user_id, name)
    confirmations = [ctx.tr("name_saved", name=name)]
    if join:
        await ctx.store.profiles.set_leaderboard_opt_in(ctx.user_id, True)
        confirmations.append(ctx.tr("board_joined"))
    await _show_card(ctx, prefix="\n".join(confirmations))


@wizard(WIZARD_REMINDER)
async def reminder_step(ctx: Ctx, text: str) -> None:
    """The typed daily reminder time."""
    value = parse_reminder_time(text)
    if value is None:
        await ctx.reply(ctx.tr("reminder_invalid"))
        return
    ctx.wiz.clear(ctx.user_id)
    await save_reminder_time(ctx.store, ctx.user_id, value)
    await _show_card(ctx, prefix=ctx.tr("reminder_saved", time=format_reminder_time(value)))
