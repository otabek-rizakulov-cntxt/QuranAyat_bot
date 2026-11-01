"""Characterization: every hifz keyboard renders on Telegram exactly as it did
before the features moved onto the channel seam (MULTI_PLATFORM_PLAN P3.1).

Recorded from the hand-built InlineKeyboardMarkup before the conversion, like
tests/test_keyboard_snapshots.py for the reader. Re-record only on purpose:
    UPDATE_KEYBOARD_SNAPSHOTS=1 venv/bin/python -m pytest tests/test_hifz_keyboard_snapshots.py
"""

import json
import os
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from bot.context import Ctx
from bot.features import _plan_keyboards as pk
from bot.features import check, leaderboard, profile, progress, streak
from bot.keyboards.time_pickers import offset_keyboard
from channels.telegram import to_markup
from infra.file_facade import File
from infra.store import get_store

SNAPSHOTS = os.path.join(os.path.dirname(__file__), "fixtures", "hifz_keyboard_snapshots.json")
UPDATE = os.environ.get("UPDATE_KEYBOARD_SNAPSHOTS") == "1"
APP = "https://app.example.org"
LANGS = ("en", "ar", "uz")
USER = 880001


def _as_dict(keyboard):
    if keyboard is None:
        return None
    if hasattr(keyboard, "to_dict"):
        return keyboard.to_dict()
    return to_markup(keyboard).to_dict()


class _Settings:
    def __init__(self, lang):
        self.ui_lang = lang
        self.translation_lang = "en"
        self.reciter = "Husary_128kbps"


async def _ctx(lang):
    return await Ctx.build(AsyncMock(), {}, File(), USER, USER, _Settings(lang))


def _static_cases():
    cases = []
    for app_url in ("", APP):
        for lang in LANGS:
            tag = "%s/%s" % ("app" if app_url else "noapp", lang)
            cases += [
                ("drill/%s" % tag, app_url, lambda la=lang: pk._drill_keyboard(7, 67, 1, la)),
            ]
    for lang in LANGS:
        cases += [
            ("target/%s" % lang, "", lambda la=lang: pk._target_keyboard(la)),
            ("pace/%s" % lang, "", lambda la=lang: pk._pace_keyboard(la)),
            ("days/%s" % lang, "", lambda la=lang: pk._days_keyboard(la)),
            ("reminder/%s" % lang, "", lambda la=lang: pk._reminder_keyboard(la)),
            ("preview/%s" % lang, "", lambda la=lang: pk._preview_keyboard(la)),
            ("profile_reminder/%s" % lang, "", lambda la=lang: profile.reminder_keyboard(la)),
            (
                "profile_reminder_cancel/%s" % lang,
                "",
                lambda la=lang: profile.reminder_keyboard(la, cancel_data="hp:main"),
            ),
        ]
        for selected in ((), (1, 3, 5), (1, 2, 3, 4, 5, 6, 7)):
            cases.append(
                (
                    "custom_days/%s/%s" % (lang, selected),
                    "",
                    lambda la=lang, s=selected: pk._custom_days_keyboard(s, la),
                )
            )
        for status in ("active", "paused", "abandoned"):
            cases.append(
                (
                    "plan/%s/%s" % (lang, status),
                    "",
                    lambda la=lang, st=status: pk._plan_keyboard(SimpleNamespace(status=st), la),
                )
            )
    cases += [
        (
            "offset/memorize",
            "",
            lambda: offset_keyboard("en", "hm:tz:", label_prefix="UTC", cancel_data="hm:x"),
        ),
        ("offset/profile", "", lambda: offset_keyboard("ar", "hp:tz:", cancel_data="hp:main")),
        ("offset/group", "", lambda: offset_keyboard("en", "gr:tz:")),
        (
            "check/options",
            "",
            lambda: check._options_keyboard(
                SimpleNamespace(surah=67, ayah=12, options=["أ", "ب", "ت"]), date(2026, 7, 31)
            ),
        ),
    ]
    return cases


async def _view_cases():
    rendered = {}
    store = await get_store()
    for lang in LANGS:
        ctx = await _ctx(lang)
        rendered["profile/fresh/%s" % lang] = _as_dict((await profile.profile_view(ctx))[1])
        rendered["progress/empty/%s" % lang] = _as_dict((await progress.progress_view(ctx))[1])
        rendered["leaderboard/out/%s" % lang] = _as_dict((await leaderboard._board_message(ctx))[1])
        for active in (True, False):
            rendered["streak/%s/%s" % (active, lang)] = _as_dict(
                streak._keyboard(ctx, SimpleNamespace(active_today=active))
            )
    await store.profiles.set_leaderboard_opt_in(USER, True)
    for surah, end in ((67, 30), (36, 12), (112, 4), (1, 7)):
        await store.hifz.add_interval(USER, surah, 1, end)
    for lang in LANGS:
        ctx = await _ctx(lang)
        rendered["profile/joined/%s" % lang] = _as_dict((await profile.profile_view(ctx))[1])
        rendered["progress/some/%s" % lang] = _as_dict((await progress.progress_view(ctx))[1])
        rendered["progress/focus36/%s" % lang] = _as_dict(
            (await progress.progress_view(ctx, 36))[1]
        )
        rendered["leaderboard/in/%s" % lang] = _as_dict((await leaderboard._board_message(ctx))[1])
    return rendered


async def test_hifz_keyboards_match_their_snapshots(monkeypatch):
    rendered = {}
    for name, app_url, build in _static_cases():
        monkeypatch.setenv("MINIAPP_URL", app_url)
        rendered[name] = _as_dict(build())
    monkeypatch.setenv("MINIAPP_URL", "")
    rendered.update(await _view_cases())
    if UPDATE:
        with open(SNAPSHOTS, "w", encoding="utf-8") as f:
            json.dump(rendered, f, ensure_ascii=False, indent=1, sort_keys=True)
        pytest.skip("snapshots re-recorded")
    with open(SNAPSHOTS, encoding="utf-8") as f:
        recorded = json.load(f)
    assert sorted(rendered) == sorted(recorded)
    changed = [name for name in recorded if rendered[name] != recorded[name]]
    assert not changed, "keyboards changed: %s" % changed[:10]
