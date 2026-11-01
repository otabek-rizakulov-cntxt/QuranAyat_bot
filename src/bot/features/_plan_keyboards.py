"""Every keyboard the /memorize flow shows: the setup wizard, the preview, the
plan card and the drill card."""

from typing import Sequence

from bot.features._plan_common import _DAY_KEYS, PACE_CHOICES, REMINDER_CHOICES
from bot.keyboards.rows import button_rows
from bot.limits import REPEAT_COUNT
from bot.miniapp import app_choice_row
from channels import Choice, Choices
from infra.store.plans import PLAN_ACTIVE, PLAN_PAUSED
from locales import t


def _cancel_row(ui_lang: str) -> list:
    return [Choice(t("btn_cancel", ui_lang), data="hm:x")]


def _target_keyboard(ui_lang: str) -> Choices:
    return [
        [Choice(t("btn_target_surah", ui_lang), data="hm:t:s")],
        [Choice(t("btn_target_juz", ui_lang), data="hm:t:j")],
        [Choice(t("btn_target_range", ui_lang), data="hm:t:r")],
        _cancel_row(ui_lang),
    ]


def _pace_keyboard(ui_lang: str) -> Choices:
    return [
        [Choice(t("btn_pace_auto", ui_lang), data="hm:p:0")],
        [Choice(str(n), data="hm:p:%d" % n) for n in PACE_CHOICES],
        # No `btn_pace_custom` exists in the frozen manifest, so the "type your
        # own" affordance is a pencil rather than an invented word.
        [Choice("✏️", data="hm:p:c")],
        _cancel_row(ui_lang),
    ]


def _days_keyboard(ui_lang: str) -> Choices:
    return [
        [Choice(t("btn_days_daily", ui_lang), data="hm:d:all")],
        [Choice(t("btn_days_weekdays", ui_lang), data="hm:d:wk")],
        [Choice(t("btn_days_custom", ui_lang), data="hm:d:pick")],
        _cancel_row(ui_lang),
    ]


def _custom_days_keyboard(selected: Sequence[int], ui_lang: str) -> Choices:
    chosen = set(int(d) for d in selected or ())
    row = []
    for index, key in enumerate(_DAY_KEYS, start=1):
        label = t(key, ui_lang)
        row.append(Choice(("✅ " if index in chosen else "") + label, data="hm:dt:%d" % index))
    return [
        row[:4],
        row[4:],
        [Choice(t("btn_confirm", ui_lang), data="hm:dok")],
        _cancel_row(ui_lang),
    ]


def _reminder_keyboard(ui_lang: str) -> Choices:
    """Preset reminder times, with free text as the escape for anything else.

    Not profile.reminder_keyboard: /profile deliberately has the time typed with
    no presets (docs/REFACTOR_PLAN.md §10 lists the difference as a UX decision).
    """
    buttons = [Choice(choice, data="hm:rt:" + choice) for choice in REMINDER_CHOICES]
    rows = button_rows(buttons, 3)
    rows.append(_cancel_row(ui_lang))
    return rows


def _preview_keyboard(ui_lang: str) -> Choices:
    return [
        [Choice(t("btn_confirm_plan", ui_lang), data="hm:ok")],
        _cancel_row(ui_lang),
    ]


def _plan_keyboard(plan, ui_lang: str) -> Choices:
    """The lifecycle controls for a plan the user already has (D5)."""
    rows = []
    if plan.status == PLAN_ACTIVE:
        rows.append([Choice(t("btn_start_drill", ui_lang), data="hm:go")])
        rows.append([Choice(t("btn_pause_plan", ui_lang), data="hm:ps")])
    elif plan.status == PLAN_PAUSED:
        rows.append([Choice(t("btn_resume_plan", ui_lang), data="hm:rs")])
    rows.append([Choice(t("btn_abandon_plan", ui_lang), data="hm:ab")])
    return rows


def _drill_keyboard(plan_day_id: int, surah: int, ayah: int, ui_lang: str) -> Choices:
    """The drill controls: mark it known, hear it again, or stop the plan.

    The repeat button carries the reader's own `rep:` callback_data on purpose —
    "🔁 Repeat ×3" already exists in `main.verse_keyboard` and is handled by
    main.py's chain, so the drill reuses the behaviour instead of copying it.
    """
    return [
        [Choice(t("btn_know_by_heart", ui_lang), data="hm:kn:%d" % plan_day_id)],
        [
            Choice(
                "🔁 %s ×%d" % (t("btn_repeat", ui_lang), REPEAT_COUNT),
                data="rep:%d:%d" % (surah, ayah),
            )
        ],
        [Choice(t("btn_pause_plan", ui_lang), data="hm:ps")],
    ] + app_choice_row("📱 " + t("web_btn_open_app", ui_lang), "/drill")
