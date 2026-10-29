"""Every keyboard the /memorize flow shows: the setup wizard, the preview, the
plan card and the drill card."""

from typing import Sequence

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.features._plan_common import _DAY_KEYS, PACE_CHOICES, REMINDER_CHOICES
from bot.keyboards.rows import button_rows
from bot.limits import REPEAT_COUNT
from bot.miniapp import app_row
from infra.store.plans import PLAN_ACTIVE, PLAN_PAUSED
from locales import t


def _cancel_row(ui_lang: str) -> list:
    return [InlineKeyboardButton(t("btn_cancel", ui_lang), callback_data="hm:x")]


def _target_keyboard(ui_lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t("btn_target_surah", ui_lang), callback_data="hm:t:s")],
            [InlineKeyboardButton(t("btn_target_juz", ui_lang), callback_data="hm:t:j")],
            [InlineKeyboardButton(t("btn_target_range", ui_lang), callback_data="hm:t:r")],
            _cancel_row(ui_lang),
        ]
    )


def _pace_keyboard(ui_lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t("btn_pace_auto", ui_lang), callback_data="hm:p:0")],
            [InlineKeyboardButton(str(n), callback_data="hm:p:%d" % n) for n in PACE_CHOICES],
            # No `btn_pace_custom` exists in the frozen manifest, so the "type your
            # own" affordance is a pencil rather than an invented word.
            [InlineKeyboardButton("✏️", callback_data="hm:p:c")],
            _cancel_row(ui_lang),
        ]
    )


def _days_keyboard(ui_lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t("btn_days_daily", ui_lang), callback_data="hm:d:all")],
            [InlineKeyboardButton(t("btn_days_weekdays", ui_lang), callback_data="hm:d:wk")],
            [InlineKeyboardButton(t("btn_days_custom", ui_lang), callback_data="hm:d:pick")],
            _cancel_row(ui_lang),
        ]
    )


def _custom_days_keyboard(selected: Sequence[int], ui_lang: str) -> InlineKeyboardMarkup:
    chosen = set(int(d) for d in selected or ())
    row = []
    for index, key in enumerate(_DAY_KEYS, start=1):
        label = t(key, ui_lang)
        row.append(
            InlineKeyboardButton(
                ("✅ " if index in chosen else "") + label, callback_data="hm:dt:%d" % index
            )
        )
    return InlineKeyboardMarkup(
        [
            row[:4],
            row[4:],
            [InlineKeyboardButton(t("btn_confirm", ui_lang), callback_data="hm:dok")],
            _cancel_row(ui_lang),
        ]
    )


def _reminder_keyboard(ui_lang: str) -> InlineKeyboardMarkup:
    """Preset reminder times, with free text as the escape for anything else.

    Not profile.reminder_keyboard: /profile deliberately has the time typed with
    no presets (docs/REFACTOR_PLAN.md §10 lists the difference as a UX decision).
    """
    buttons = [
        InlineKeyboardButton(choice, callback_data="hm:rt:" + choice) for choice in REMINDER_CHOICES
    ]
    rows = button_rows(buttons, 3)
    rows.append(_cancel_row(ui_lang))
    return InlineKeyboardMarkup(rows)


def _preview_keyboard(ui_lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t("btn_confirm_plan", ui_lang), callback_data="hm:ok")],
            _cancel_row(ui_lang),
        ]
    )


def _plan_keyboard(plan, ui_lang: str) -> InlineKeyboardMarkup:
    """The lifecycle controls for a plan the user already has (D5)."""
    rows = []
    if plan.status == PLAN_ACTIVE:
        rows.append([InlineKeyboardButton(t("btn_start_drill", ui_lang), callback_data="hm:go")])
        rows.append([InlineKeyboardButton(t("btn_pause_plan", ui_lang), callback_data="hm:ps")])
    elif plan.status == PLAN_PAUSED:
        rows.append([InlineKeyboardButton(t("btn_resume_plan", ui_lang), callback_data="hm:rs")])
    rows.append([InlineKeyboardButton(t("btn_abandon_plan", ui_lang), callback_data="hm:ab")])
    return InlineKeyboardMarkup(rows)


def _drill_keyboard(plan_day_id: int, surah: int, ayah: int, ui_lang: str) -> InlineKeyboardMarkup:
    """The drill controls: mark it known, hear it again, or stop the plan.

    The repeat button carries the reader's own `rep:` callback_data on purpose —
    "🔁 Repeat ×3" already exists in `main.verse_keyboard` and is handled by
    main.py's chain, so the drill reuses the behaviour instead of copying it.
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    t("btn_know_by_heart", ui_lang), callback_data="hm:kn:%d" % plan_day_id
                )
            ],
            [
                InlineKeyboardButton(
                    "🔁 %s ×%d" % (t("btn_repeat", ui_lang), REPEAT_COUNT),
                    callback_data="rep:%d:%d" % (surah, ayah),
                )
            ],
            [InlineKeyboardButton(t("btn_pause_plan", ui_lang), callback_data="hm:ps")],
        ]
        + app_row("📱 " + t("web_btn_open_app", ui_lang), "/drill")
    )
