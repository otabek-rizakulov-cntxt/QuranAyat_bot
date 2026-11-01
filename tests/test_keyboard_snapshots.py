"""Characterization: every keyboard the Channel seam converted renders exactly as
it did before (docs/MULTI_PLATFORM_PLAN.md P1.3).

The snapshots in tests/fixtures/keyboard_snapshots.json were recorded from the
hand-built InlineKeyboardMarkup *before* the builders started returning neutral
`Choices`; this test renders today's builders through `to_markup` and requires
the same Telegram JSON, button for button.

Re-record only on a deliberate keyboard change:
    UPDATE_KEYBOARD_SNAPSHOTS=1 venv/bin/python -m pytest tests/test_keyboard_snapshots.py
"""

import json
import os
from unittest.mock import AsyncMock

import pytest

import bot.dispatch as dispatch
from bot.keyboards import language as language_kb
from bot.keyboards import page as page_kb
from bot.keyboards import reciter as reciter_kb
from bot.keyboards import sajda as sajda_kb
from bot.keyboards import verse as verse_kb
from channels.telegram import TelegramChannel, to_markup

SNAPSHOTS = os.path.join(os.path.dirname(__file__), "fixtures", "keyboard_snapshots.json")
UPDATE = os.environ.get("UPDATE_KEYBOARD_SNAPSHOTS") == "1"
APP = "https://app.example.org"
LANGS = ("en", "ar", "uz")


def _as_dict(keyboard):
    """Telegram JSON for a keyboard, whichever shape the builder returns."""
    if keyboard is None:
        return None
    if hasattr(keyboard, "to_dict"):
        return keyboard.to_dict()
    return to_markup(keyboard).to_dict()


def _keyboards():
    """(name, zero-arg builder) for every case; the Mini App URL is set per case."""
    cases = []
    for app_url in ("", APP):
        tag = "app" if app_url else "noapp"
        for lang in LANGS:
            for surah, ayah in ((2, 255), (1, 1), (114, 6)):
                for view in ("translation", "arabic", "tafsir", "audio"):
                    for app in (True, False):
                        cases.append(
                            (
                                "verse/%s/%s/%d:%d/%s/%s" % (tag, lang, surah, ayah, view, app),
                                app_url,
                                lambda s=surah, a=ayah, v=view, la=lang, ap=app: (
                                    verse_kb.verse_keyboard(s, a, v, la, app=ap)
                                ),
                            )
                        )
            for page in (1, 255, 604):
                cases.append(
                    (
                        "page/%s/%s/%d" % (tag, lang, page),
                        app_url,
                        lambda p=page, la=lang: page_kb.page_keyboard(p, la),
                    )
                )
    for lang in LANGS:
        for kind in ("recitation", "riwayah", "translation"):
            for page in (0, 1, 99):
                for current in (None, "Husary_128kbps"):
                    cases.append(
                        (
                            "reciter/%s/%s/%d/%s" % (lang, kind, page, current),
                            "",
                            lambda la=lang, k=kind, p=page, c=current: reciter_kb.reciter_keyboard(
                                la, k, p, current=c
                            ),
                        )
                    )
        cases.append(("sajda/%s" % lang, "", lambda la=lang: sajda_kb.sajda_keyboard(la)))
    cases.append(("language/ui", "", language_kb.language_keyboard))
    cases.append(("language/translation", "", language_kb.translation_language_keyboard))
    return cases


async def _search_markup(query):
    """The keyboard the reciter search posts for `query` (None: no matches)."""
    bot = AsyncMock()
    await dispatch._search_reciters(TelegramChannel(bot, 555000), query, "en")
    return bot.send_message.await_args.kwargs.get("reply_markup")


SEARCHES = ("husary", "afasy", "minsh", "abdul", "no-such-reciter-xyz")


async def _render(monkeypatch):
    rendered = {}
    for name, app_url, build in _keyboards():
        monkeypatch.setenv("MINIAPP_URL", app_url)
        rendered[name] = _as_dict(build())
    monkeypatch.setenv("MINIAPP_URL", "")
    for query in SEARCHES:
        rendered["search/%s" % query] = _as_dict(await _search_markup(query))
    return rendered


async def test_keyboards_match_their_snapshots(monkeypatch):
    rendered = await _render(monkeypatch)
    if UPDATE:
        os.makedirs(os.path.dirname(SNAPSHOTS), exist_ok=True)
        with open(SNAPSHOTS, "w", encoding="utf-8") as f:
            json.dump(rendered, f, ensure_ascii=False, indent=1, sort_keys=True)
        pytest.skip("snapshots re-recorded")
    with open(SNAPSHOTS, encoding="utf-8") as f:
        recorded = json.load(f)
    assert sorted(rendered) == sorted(recorded)
    changed = [name for name in recorded if rendered[name] != recorded[name]]
    assert not changed, "keyboards changed: %s" % changed[:10]
