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
import re
from datetime import datetime, time, timezone as _timezone
from typing import List, Optional, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from hifz import Ctx, callback, command, wizard
from hifz.refs import KIND_RANGE, Ref, format_ref
from lib.localtime import (is_valid_offset, next_due_utc, normalize_offset,
                           offset_options)
from lib.store.plans import DAY_COMPLETED
from modules import Quran

__all__ = [
    "NAME_MIN", "NAME_MAX",
    "PROFILE_CB", "NAME_CB", "BOARD_ON_CB", "BOARD_OFF_CB", "TIMEZONE_CB",
    "OFFSET_PREFIX", "REMINDER_CB", "REMINDER_OFF_CB",
    "WIZARD_NAME", "WIZARD_REMINDER",
    "offset_keyboard", "offset_from_callback", "reminder_keyboard",
    "parse_reminder_time", "format_reminder_time",
    "save_timezone", "save_reminder_time", "next_push_utc",
    "valid_display_name", "telegram_username", "profile_view",
]

# 2-32 characters (B2). Long enough for "Abu Bakr as-Siddiq", short enough that a
# leaderboard row still fits on a phone. Uniqueness is deliberately not required.
NAME_MIN = 2
NAME_MAX = 32

# --- callback_data (Telegram caps it at 64 bytes) ------------------------------
# The shapes documented in `hifz.PREFIXES` ("hp:name  hp:board:on  hp:tz
# hp:tz:+05:00  hp:rem"), because another module already spells one of them out
# rather than importing it: `hifz/leaderboard.py` puts "hp:board:on" under its
# own "join the board" button so a broken profile module cannot take the board
# down with it. Every shape is under 13 bytes and every one is parsed
# defensively — a keyboard never expires, so a tap can arrive years after the
# message that carried it.
PROFILE_CB = "hp:main"          #  7 bytes — (re)draw the card; doubles as "cancel"
NAME_CB = "hp:name"             #  7 bytes — start the display-name wizard
BOARD_ON_CB = "hp:board:on"     # 11 bytes — join the leaderboard
BOARD_OFF_CB = "hp:board:off"   # 12 bytes — leave it
TIMEZONE_CB = "hp:tz"           #  5 bytes — show the offset picker
OFFSET_PREFIX = "hp:tz:"        #  6 + up to 6 = 12 bytes with "+05:00"
REMINDER_CB = "hp:rem"          #  6 bytes — start the reminder-time wizard
REMINDER_OFF_CB = "hp:rem:off"  # 10 bytes — turn reminders off

WIZARD_NAME = "profile_name"
WIZARD_REMINDER = "profile_reminder"


# --- Display names -------------------------------------------------------------

def valid_display_name(text: str) -> Optional[str]:
    """The cleaned display name, or None if it is not 2-32 characters.

    Whitespace is collapsed rather than rejected: someone typing "Abu   Bakr" or
    pasting a name with a trailing newline meant the name, not an error. What is
    stored is the *raw* text — escaping happens at render time (see `_name_line`),
    because storing escaped text would double-escape it the next time it is shown.
    """
    name = " ".join((text or "").split())
    if not NAME_MIN <= len(name) <= NAME_MAX:
        return None
    return name


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

def offset_keyboard(ui_lang: str, prefix: str = OFFSET_PREFIX, columns: int = 4,
                    cancel_data: Optional[str] = None) -> InlineKeyboardMarkup:
    """The 34-offset picker, as an inline keyboard.

    The labels *are* the offsets ("+05:00"), so this keyboard needs no
    translation — half the reason the fixed-offset model was chosen over IANA
    zone names. `prefix` is what each button's callback_data starts with, so
    another wizard can own its own taps: `offset_keyboard(lang, prefix="hm:tz:")`.
    `cancel_data` adds a trailing Cancel row when given.
    """
    from locales import t
    buttons = [InlineKeyboardButton(offset, callback_data=prefix + offset)
               for offset in offset_options()]
    columns = max(1, int(columns))
    rows: List[List[InlineKeyboardButton]] = [buttons[i:i + columns]
                                              for i in range(0, len(buttons), columns)]
    if cancel_data:
        rows.append([InlineKeyboardButton(t("btn_cancel", ui_lang),
                                          callback_data=cancel_data)])
    return InlineKeyboardMarkup(rows)


def offset_from_callback(cb_data: str, prefix: str = OFFSET_PREFIX) -> Optional[str]:
    """The normalized offset a picker tap carries ("+05:00"), or None.

    None for anything that is not this prefix, or whose payload is not a real
    offset — a keyboard is never expired by Telegram, so this input is untrusted
    even when we built the keyboard ourselves.
    """
    if not cb_data or not cb_data.startswith(prefix):
        return None
    payload = cb_data[len(prefix):].strip()
    if not payload or not is_valid_offset(payload):
        return None
    return normalize_offset(payload)


async def save_timezone(store, user_id: int, offset: str):
    """Store the user's fixed UTC offset, normalized to "+05:00" form.

    Returns the updated `ProfileRow` (created if this is their first write).
    Raises ValueError if `offset` is not a UTC offset — validate a tap with
    `offset_from_callback` and typed text with `lib.localtime.is_valid_offset`.
    """
    return await store.profiles.set_timezone(user_id, normalize_offset(offset))


# --- Reminder time (B3) --------------------------------------------------------

# "07:30", "7:30", "0730", "730", "7", "7.30", "7h30". 12-hour input is not
# accepted: `reminder_prompt` asks for 24-hour form in all 48 languages, and
# guessing at an unqualified "7" being the evening is worse than a re-prompt.
_TIME_RE = re.compile(r"^(?P<h>\d{1,2})\s*(?:[:.,;h\-]\s*(?P<m>\d{1,2})|(?P<m2>\d{2}))?$",
                      re.IGNORECASE)


def parse_reminder_time(text: str) -> Optional[time]:
    """A typed 24-hour time as a `datetime.time`, or None if it does not parse."""
    cleaned = (text or "").strip()
    if not cleaned:
        return None
    match = _TIME_RE.match(cleaned)
    if match is None:
        return None
    hour = int(match.group("h"))
    minute = int(match.group("m") or match.group("m2") or 0)
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    return time(hour=hour, minute=minute)


def format_reminder_time(value: Optional[time]) -> str:
    """A stored reminder time as the "07:30" token a `{time}` placeholder wants."""
    if value is None:
        return ""
    return "%02d:%02d" % (value.hour, value.minute)


def reminder_keyboard(ui_lang: str, off_data: str = REMINDER_OFF_CB,
                      cancel_data: Optional[str] = None) -> InlineKeyboardMarkup:
    """The keyboard under `reminder_prompt`: turn reminders off, or back out.

    The time itself is typed, not picked — a picker for 1,440 minutes is either
    24 buttons and wrong for anyone who wants 07:30, or a two-step drill-down for
    something a person can type in three seconds. `off_data` and `cancel_data`
    are parameters so another wizard can route the same keyboard to itself.
    """
    from locales import t
    rows = [[InlineKeyboardButton(t("btn_reminder_off", ui_lang), callback_data=off_data)]]
    if cancel_data:
        rows.append([InlineKeyboardButton(t("btn_cancel", ui_lang),
                                          callback_data=cancel_data)])
    return InlineKeyboardMarkup(rows)


async def save_reminder_time(store, user_id: int, value: Optional[time]):
    """Store (or clear, with None) the local time of day for the daily push."""
    return await store.profiles.set_reminder_time(user_id, value)


def next_push_utc(profile, now: Optional[datetime] = None) -> Optional[datetime]:
    """When this profile's next daily push is due, in UTC — or None if it has no
    reminder time.

    The scheduler queues each day's push from the profile as it stands, so this
    is the falsifiable half of B3: change the timezone and the instant moves by
    exactly the difference between the two offsets, with no row to migrate.
    """
    reminder = getattr(profile, "reminder_time", None)
    if reminder is None:
        return None
    offset = getattr(profile, "timezone", None) or "+00:00"
    if not is_valid_offset(offset):
        offset = "+00:00"
    return next_due_utc(reminder, offset, now or datetime.now(_timezone.utc))


# --- The card (B1) -------------------------------------------------------------

def _plan_target(plan) -> str:
    """What to call the plan's target: a surah name when it is a whole surah,
    otherwise the compact reference. Both are un-localized by design — a surah
    name is a proper noun and `format_ref` is machine text."""
    whole_surah = (plan.start_surah == plan.end_surah and plan.start_ayah == 1
                   and plan.end_ayah == Quran.get_surah_length(plan.start_surah))
    if plan.target_kind == "surah" or whole_surah:
        return Quran.get_surah_name(plan.start_surah)
    return format_ref(Ref(KIND_RANGE, plan.start_surah, plan.start_ayah,
                          plan.end_surah, plan.end_ayah))


async def _plan_line(ctx: Ctx) -> str:
    plan = await ctx.store.plans.get_active_plan(ctx.user_id)
    if plan is None:
        return ctx.tr("profile_plan_none")
    total = await ctx.store.plans.count_plan_days(plan.id)
    done = await ctx.store.plans.count_plan_days(plan.id, DAY_COMPLETED)
    day = min(done + 1, total) if total else 0
    return ctx.tr("profile_plan_active", target=html.escape(_plan_target(plan)),
                  day=day, total=total)


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
        lines.append(ctx.tr("profile_name_set",
                            name=html.escape(profile.display_name)))
    else:
        lines.append(ctx.tr("profile_name_unset"))
    lines.append(ctx.tr("profile_leaderboard_on" if profile.leaderboard_opt_in
                        else "profile_leaderboard_off"))
    if profile.timezone and is_valid_offset(profile.timezone):
        lines.append(ctx.tr("profile_timezone_set",
                            offset=normalize_offset(profile.timezone)))
    else:
        lines.append(ctx.tr("profile_timezone_unset"))
    if profile.reminder_time is not None:
        lines.append(ctx.tr("profile_reminder_set",
                            time=format_reminder_time(profile.reminder_time)))
    else:
        lines.append(ctx.tr("profile_reminder_unset"))
    lines.append(await _plan_line(ctx))

    board_button = (InlineKeyboardButton(ctx.tr("btn_leave_board"),
                                         callback_data=BOARD_OFF_CB)
                    if profile.leaderboard_opt_in
                    else InlineKeyboardButton(ctx.tr("btn_join_board"),
                                              callback_data=BOARD_ON_CB))
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(ctx.tr("btn_edit_name"), callback_data=NAME_CB)],
        [board_button],
        [InlineKeyboardButton(ctx.tr("btn_edit_timezone"), callback_data=TIMEZONE_CB)],
        [InlineKeyboardButton(ctx.tr("btn_edit_reminder"), callback_data=REMINDER_CB)],
    ])
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
    ctx.wiz.clear(ctx.user_id)          # a command always escapes a pending wizard
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

    action = (cb_data or "")[len("hp:"):]

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
        await ctx.edit(ctx.tr("timezone_prompt"),
                       reply_markup=offset_keyboard(ctx.ui_lang,
                                                    cancel_data=PROFILE_CB))
        return

    if action in ("rem", "r"):
        ctx.wiz.start(ctx.user_id, WIZARD_REMINDER)
        await ctx.answer()
        await ctx.edit(ctx.tr("reminder_prompt"),
                       reply_markup=reminder_keyboard(ctx.ui_lang,
                                                      cancel_data=PROFILE_CB))
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
        [[InlineKeyboardButton(ctx.tr("btn_cancel"), callback_data=PROFILE_CB)]])


# --- Leaderboard opt-in (B2) ---------------------------------------------------

async def _join_board(ctx: Ctx) -> None:
    """Opt in, adopting the Telegram @username when there is one.

    Someone with no username — a large minority of Telegram accounts — is asked
    for a name instead, and only joins once they have supplied one. Nobody is put
    on a public board under a blank label.
    """
    profile = await ctx.store.profiles.ensure_profile(ctx.user_id)
    name = profile.display_name or telegram_username(ctx)
    if not name:
        ctx.wiz.start(ctx.user_id, WIZARD_NAME, join=True)
        await ctx.answer()
        await ctx.edit(ctx.tr("name_prompt"), reply_markup=_cancel_keyboard(ctx))
        return
    if not profile.display_name:
        await ctx.store.profiles.set_display_name(ctx.user_id, name)
    await ctx.store.profiles.set_leaderboard_opt_in(ctx.user_id, True)
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
    await _show_card(ctx, prefix=ctx.tr("reminder_saved",
                                        time=format_reminder_time(value)))
