"""One week of hifz, run on Telegram and on WhatsApp (MULTI_PLATFORM_PLAN Phase 3).

The phase's done-when: a plan created on WhatsApp runs a full week of drills with
the same state transitions the Telegram flow produces. Each platform is driven
through its real entry point — Telegram updates into `handle_update`, WhatsApp
messages into `handle_message`, scheduled pushes through the scheduler's `tick` —
with only the network mocked (the audio CDN, Telegram's API, Meta's Graph API).
"""

import io
import json
from datetime import timedelta
from unittest.mock import AsyncMock

import httpx
import pytest
import telegram

import app.lifespan as lifespan
import bot.dispatch as dispatch
import bot.media
import channels.whatsapp as wa
import infra.scheduler as scheduler
import infra.scheduler.push as push
from bot.whatsapp import handle_message
from channels.whatsapp import GraphClient
from infra.store import get_store
from infra.store.plans import DAY_COMPLETED

TG_USER = 940100
WA_ID = "998901112233"
DAYS = 7


@pytest.fixture(scope="module")
def data():
    return lifespan.build_data()


@pytest.fixture(autouse=True)
def no_cdn(monkeypatch):
    async def combined(surah, start, end, performer):
        clip = io.BytesIO(b"mp3")
        clip.name = "quran_%d_%d-%d.mp3" % (surah, start, end)
        return clip

    monkeypatch.setattr(bot.media.cdn_audio, "download_combined_audio", combined)


class Telegram:
    platform = "telegram"

    def __init__(self, data):
        self.data = data
        self.tg = telegram.Bot("123456:TEST-abcdefghijklmnopqrstuvwxyz")
        self.bot = AsyncMock()
        self.user_id = TG_USER
        self.n = 0

    async def start(self):
        pass

    async def say(self, text):
        self.n += 1
        update = {
            "update_id": self.n,
            "message": {
                "message_id": self.n,
                "date": 1700000000,
                "chat": {"id": TG_USER, "type": "private"},
                "from": {"id": TG_USER, "is_bot": False, "first_name": "T", "language_code": "en"},
                "text": text,
            },
        }
        await dispatch.handle_update(self.bot, self.data, telegram.Update.de_json(update, self.tg))

    async def tap(self, cb):
        self.n += 1
        update = {
            "update_id": self.n,
            "callback_query": {
                "id": "cb%d" % self.n,
                "from": {"id": TG_USER, "is_bot": False, "first_name": "T"},
                "chat_instance": "ci",
                "data": cb,
                "message": {
                    "message_id": 1,
                    "date": 1700000000,
                    "chat": {"id": TG_USER, "type": "private"},
                    "text": "x",
                },
            },
        }
        await dispatch.handle_update(self.bot, self.data, telegram.Update.de_json(update, self.tg))


class WhatsApp:
    platform = "whatsapp"

    def __init__(self, data, monkeypatch):
        self.data = data
        self.sent = []

        def graph(request):
            if request.url.path.endswith("/messages"):
                self.sent.append(json.loads(request.content))
            return httpx.Response(200, json={"messages": [{"id": "wamid.x"}], "id": "media-1"})

        async def no_sleep(_):
            return None

        monkeypatch.setattr(wa, "_sleep", no_sleep)
        self.client = GraphClient("P", "T", transport=httpx.MockTransport(graph))
        monkeypatch.setattr(push, "_whatsapp_client", self.client)
        self.bot = None
        self.n = 0

    async def start(self):
        await self.say("menu")  # first contact: welcome, hint, language picker
        store = await get_store()
        self.user_id = (await store.identity.get("whatsapp", WA_ID)).user_id
        await self.tap("setlang:en")

    async def say(self, text):
        self.n += 1
        message = {"from": WA_ID, "id": "in%d" % self.n, "type": "text", "text": {"body": text}}
        await handle_message(self.client, self.data, message)

    async def tap(self, cb):
        self.n += 1
        message = {
            "from": WA_ID,
            "id": "in%d" % self.n,
            "type": "interactive",
            "interactive": {"type": "list_reply", "list_reply": {"id": cb, "title": "x"}},
        }
        await handle_message(self.client, self.data, message)


async def _week(user, data):
    """Create a plan, drill the first portion by hand, then six scheduled pushes.
    Returns the state trail: each day's state after each step, plus the totals."""
    store = await get_store()
    trail = []
    await user.start()

    # The wizard: surah 67 at two ayat a day, every day, +05:00, reminder 07:00.
    await user.say("/memorize")
    await user.tap("hm:t:s")
    await user.say("67")
    await user.tap("hm:p:2")
    await user.tap("hm:d:all")
    await user.tap("hm:tz:+05:00")
    await user.tap("hm:rt:07:00")
    await user.tap("hm:ok")
    if user.platform == "whatsapp":
        await user.tap("hm:cy")  # allow daily reminders (WhatsApp opt-in)

    plan = await store.plans.get_active_plan(user.user_id)
    assert plan is not None, "the wizard should have saved a plan"

    async def states():
        return [d.state for d in await store.plans.list_plan_days(plan.id)][:DAYS]

    # Day 1 by hand: "Start today's portion", then "I know this by heart".
    await user.tap("hm:go")
    trail.append(("go", await states()))
    day = next(d for d in await store.plans.list_plan_days(plan.id) if d.state == "sent")
    await user.tap("hm:kn:%d" % day.id)
    trail.append(("known", await states()))

    # Days 2..7 by the scheduler: each push delivers, then the user marks it known.
    for _ in range(DAYS - 1):
        done = {d.id for d in await store.plans.list_plan_days(plan.id) if d.state != "pending"}
        pending = [
            r
            for r in store.state.scheduled_send.values()
            if r.state == "pending"
            and r.kind == "plan_day"
            and r.payload["plan_day_id"] not in done  # day 1's push was overtaken by hand
        ]
        assert pending, "the chain must keep one push queued"
        row = min(pending, key=lambda r: r.due_at)
        assert row.platform == user.platform
        await scheduler.tick(user.bot, data, now=row.due_at + timedelta(seconds=30), store=store)
        trail.append(("push", await states()))
        day = next(d for d in await store.plans.list_plan_days(plan.id) if d.state == "sent")
        await user.tap("hm:kn:%d" % day.id)
        trail.append(("known", await states()))

    days = await store.plans.list_plan_days(plan.id)
    totals = {
        "completed": sum(d.state == DAY_COMPLETED for d in days),
        "memorized_ayahs": await store.hifz.count_ayahs(user.user_id, 67),
        "plan_status": (await store.plans.get_plan(plan.id)).status,
    }
    return trail, totals


async def test_a_week_on_whatsapp_matches_a_week_on_telegram(data, monkeypatch):
    tg_trail, tg_totals = await _week(Telegram(data), data)
    whatsapp = WhatsApp(data, monkeypatch)
    wa_trail, wa_totals = await _week(whatsapp, data)

    assert tg_totals["completed"] == DAYS and tg_totals["plan_status"] == "active"
    assert tg_totals["memorized_ayahs"] > 0  # some days may be review days (plan_builder)
    assert wa_totals == tg_totals
    assert wa_trail == tg_trail

    # And WhatsApp really was talked to: drills arrived as messages or templates.
    kinds = {m["type"] for m in whatsapp.sent}
    assert "audio" in kinds or "template" in kinds


async def test_without_consent_whatsapp_gets_no_reminders(data, monkeypatch):
    user = WhatsApp(data, monkeypatch)
    store = await get_store()
    await user.start()
    for step in ("/memorize",):
        await user.say(step)
    for cb in ("hm:t:s",):
        await user.tap(cb)
    await user.say("67")
    for cb in ("hm:p:2", "hm:d:all", "hm:tz:+05:00", "hm:rt:07:00", "hm:ok", "hm:cn"):
        await user.tap(cb)
    plan = await store.plans.get_active_plan(user.user_id)
    row = next(r for r in store.state.scheduled_send.values() if r.kind == "plan_day")
    user.sent.clear()
    await scheduler.tick(None, data, now=row.due_at + timedelta(seconds=30), store=store)
    assert user.sent == []  # nothing pushed
    assert all(d.state == "pending" for d in await store.plans.list_plan_days(plan.id))
    # ...but the portion is still there on demand
    await user.tap("hm:go")
    assert any(m["type"] in ("audio", "interactive", "text") for m in user.sent)
