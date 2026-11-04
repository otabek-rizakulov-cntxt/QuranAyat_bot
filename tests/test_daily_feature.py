"""Verse of the day end to end, on Telegram and WhatsApp (MULTI_PLATFORM_PLAN P2.5)."""

import json
from datetime import datetime, time, timedelta, timezone
from unittest.mock import AsyncMock

import httpx
import pytest
import telegram

import app.lifespan as lifespan
import bot.dispatch as dispatch
import channels.whatsapp as wa
import infra.scheduler.push as push
from bot.features import daily
from bot.whatsapp import handle_message
from channels.whatsapp import GraphClient
from domain.daily_ayah import ayah_for
from infra.scheduler import SendCtx
from infra.store import get_store
from locales import t

USER = 555700
WA_ID = "998901234567"
NOW = datetime(2026, 11, 2, 2, 0, tzinfo=timezone.utc)  # 07:00 at +05:00


@pytest.fixture(scope="module")
def data():
    return lifespan.build_data()


@pytest.fixture(scope="module")
def tg_bot():
    return telegram.Bot("123456:TEST-abcdefghijklmnopqrstuvwxyz")


def _message(tg_bot, text):
    return telegram.Update.de_json(
        {
            "update_id": 1,
            "message": {
                "message_id": 1,
                "date": 1700000000,
                "chat": {"id": USER, "type": "private"},
                "from": {"id": USER, "is_bot": False, "first_name": "T", "language_code": "en"},
                "text": text,
            },
        },
        tg_bot,
    )


def _tap(tg_bot, cb_data):
    return telegram.Update.de_json(
        {
            "update_id": 2,
            "callback_query": {
                "id": "cb",
                "from": {"id": USER, "is_bot": False, "first_name": "T"},
                "chat_instance": "ci",
                "data": cb_data,
                "message": {
                    "message_id": 9,
                    "date": 1700000000,
                    "chat": {"id": USER, "type": "private"},
                    "text": "x",
                },
            },
        },
        tg_bot,
    )


def _texts(bot):
    return [c.kwargs["text"] for c in bot.send_message.await_args_list]


def _buttons(bot):
    markup = bot.send_message.await_args.kwargs.get("reply_markup")
    return [b.callback_data for row in markup.inline_keyboard for b in row] if markup else []


async def _due_rows(store):
    return [r for r in store.state.scheduled_send.values() if r.kind == daily.SEND_KIND]


class TestTelegramSetup:
    async def test_off_by_default_with_a_turn_on_button(self, tg_bot, data):
        bot = AsyncMock()
        await dispatch.handle_update(bot, data, _message(tg_bot, "/daily"))
        assert _texts(bot) == [t("daily_status_off", "en")]
        assert _buttons(bot) == ["hd:on"]

    async def test_full_flow_queues_the_first_send(self, tg_bot, data):
        bot = AsyncMock()
        await dispatch.handle_update(bot, data, _tap(tg_bot, "hd:on"))
        assert _texts(bot)[-1] == t("daily_pick_timezone", "en")
        assert "hd:tz:+05:00" in _buttons(bot)
        await dispatch.handle_update(bot, data, _tap(tg_bot, "hd:tz:+05:00"))
        assert _texts(bot)[-1] == t("daily_pick_time", "en")
        await dispatch.handle_update(bot, data, _tap(tg_bot, "hd:t:07:00"))
        assert _texts(bot)[-1] == t("daily_enabled", "en").format(time="07:00")

        store = await get_store()
        sub = await store.daily.get(USER)
        assert (sub.platform, sub.send_time, sub.enabled) == ("telegram", time(7, 0), True)
        (row,) = await _due_rows(store)
        assert row.platform == "telegram" and row.payload["time"] == "07:00"
        assert row.idempotency_key.endswith(":07:00")

        await dispatch.handle_update(bot, data, _message(tg_bot, "/daily"))
        assert _texts(bot)[-1] == t("daily_status_on", "en").format(time="07:00", offset="+05:00")

    async def test_known_time_zone_skips_the_picker(self, tg_bot, data):
        store = await get_store()
        await store.profiles.set_timezone(USER, "+03:00")
        bot = AsyncMock()
        await dispatch.handle_update(bot, data, _tap(tg_bot, "hd:on"))
        assert _texts(bot)[-1] == t("daily_pick_time", "en")

    async def test_changing_the_time_the_same_day_queues_the_new_one(self, tg_bot, data):
        store = await get_store()
        await store.profiles.set_timezone(USER, "+05:00")
        bot = AsyncMock()
        await dispatch.handle_update(bot, data, _tap(tg_bot, "hd:t:07:00"))
        await dispatch.handle_update(bot, data, _tap(tg_bot, "hd:t:20:00"))
        times = sorted(r.payload["time"] for r in await _due_rows(store))
        assert times == ["07:00", "20:00"]

    async def test_turn_off(self, tg_bot, data):
        store = await get_store()
        await store.profiles.set_timezone(USER, "+05:00")
        bot = AsyncMock()
        await dispatch.handle_update(bot, data, _tap(tg_bot, "hd:t:07:00"))
        await dispatch.handle_update(bot, data, _tap(tg_bot, "hd:off"))
        assert (await store.daily.get(USER)).enabled is False
        assert _texts(bot)[-1] == t("daily_disabled", "en")


async def _send_ctx(store, data, bot, row):
    return SendCtx(bot=bot, data=data, file=None, store=store, send=row, now=NOW)


class TestTelegramDelivery:
    async def _subscribe(self, store, at="07:00"):
        await store.profiles.set_timezone(USER, "+05:00")
        await store.daily.upsert(USER, "telegram", time(*map(int, at.split(":"))))
        await daily.schedule_daily(
            store,
            daily.SEND_KIND,
            USER,
            time(*map(int, at.split(":"))),
            "+05:00",
            now=NOW - timedelta(hours=1),
            payload={"time": at},
            key_extra=at,
        )
        (row,) = await _due_rows(store)
        return row

    async def test_sends_todays_ayah_and_queues_tomorrow(self, data):
        store = await get_store()
        row = await self._subscribe(store)
        bot = AsyncMock()
        await daily.push_daily(await _send_ctx(store, data, bot, row))
        texts = _texts(bot)
        assert texts[0] == t("daily_header", "en") and len(texts) == 2
        surah, ayah = ayah_for(NOW.date())
        assert "vc:ar:%d:%d" % (surah, ayah) in _buttons(bot)
        rows = await _due_rows(store)
        assert len(rows) == 2
        tomorrow = max(rows, key=lambda r: r.due_at)
        assert tomorrow.due_at - row.due_at == timedelta(days=1)

    async def test_turned_off_sends_nothing_and_stops(self, data):
        store = await get_store()
        row = await self._subscribe(store)
        await store.daily.set_enabled(USER, False)
        bot = AsyncMock()
        await daily.push_daily(await _send_ctx(store, data, bot, row))
        bot.send_message.assert_not_awaited()
        assert len(await _due_rows(store)) == 1

    async def test_a_row_for_an_old_time_is_skipped(self, data):
        store = await get_store()
        row = await self._subscribe(store)
        await store.daily.upsert(USER, "telegram", time(20, 0))
        bot = AsyncMock()
        await daily.push_daily(await _send_ctx(store, data, bot, row))
        bot.send_message.assert_not_awaited()


class Graph:
    def __init__(self):
        self.sent = []

    def __call__(self, request):
        if request.url.path.endswith("/messages"):
            self.sent.append(json.loads(request.content))
        return httpx.Response(200, json={"messages": [{"id": "wamid.x"}], "id": "m"})

    def bodies(self):
        out = []
        for m in self.sent:
            if m["type"] == "text":
                out.append(m["text"]["body"])
            elif m["type"] == "interactive":
                out.append(m["interactive"]["body"]["text"])
            else:
                out.append(m["type"])
        return out


@pytest.fixture
def graph(monkeypatch):
    async def no_sleep(_):
        return None

    monkeypatch.setattr(wa, "_sleep", no_sleep)
    graph = Graph()
    client = GraphClient("P", "T", transport=httpx.MockTransport(graph))
    monkeypatch.setattr(push, "_whatsapp_client", client)
    graph.client = client
    return graph


def wa_text(body):
    return {"from": WA_ID, "id": "in-" + body, "type": "text", "text": {"body": body}}


def wa_tap(cb):
    return {
        "from": WA_ID,
        "id": "tap-" + cb,
        "type": "interactive",
        "interactive": {"type": "button_reply", "button_reply": {"id": cb, "title": "x"}},
    }


class TestWhatsApp:
    async def _set_up(self, graph, data):
        await handle_message(graph.client, data, wa_text("menu"))  # first contact
        store = await get_store()
        uid = (await store.identity.get("whatsapp", WA_ID)).user_id
        await store.profiles.set_timezone(uid, "+05:00")
        graph.sent.clear()
        return store, uid

    async def test_consent_is_asked_before_anything_is_queued(self, graph, data):
        store, uid = await self._set_up(graph, data)
        await handle_message(graph.client, data, wa_text("kunlik"))
        await handle_message(graph.client, data, wa_tap("hd:on"))
        await handle_message(graph.client, data, wa_tap("hd:t:07:00"))
        assert graph.bodies()[-1] == t("daily_consent", "uz").format(time="07:00")
        assert await store.daily.get(uid) is None and await _due_rows(store) == []

        await handle_message(graph.client, data, wa_tap("hd:ok:07:00"))
        assert (await store.identity.get_by_user(uid, "whatsapp")).consented
        (row,) = await _due_rows(store)
        assert row.platform == "whatsapp" and row.target_chat_id == uid

    async def test_not_now_queues_nothing(self, graph, data):
        store, uid = await self._set_up(graph, data)
        await handle_message(graph.client, data, wa_tap("hd:t:07:00"))
        await handle_message(graph.client, data, wa_tap("hd:no"))
        assert await _due_rows(store) == []
        assert graph.bodies()[-1] == t("daily_status_off", "uz")

    async def test_outside_the_window_the_template_goes_out(self, graph, data, monkeypatch):
        monkeypatch.setenv("WHATSAPP_TEMPLATES", "1")
        store, uid = await self._set_up(graph, data)
        await handle_message(graph.client, data, wa_tap("hd:t:07:00"))
        await handle_message(graph.client, data, wa_tap("hd:ok:07:00"))
        (row,) = await _due_rows(store)
        graph.sent.clear()
        # two days after they last wrote (now, in _set_up), whatever today is
        later = datetime.now(timezone.utc) + timedelta(days=2)
        ctx = SendCtx(bot=None, data=data, file=None, store=store, send=row, now=later)
        await daily.push_daily(ctx)
        (message,) = graph.sent
        assert message["type"] == "template"
        template = message["template"]
        assert (template["name"], template["language"]["code"]) == ("daily_ayah", "uz")
        params = template["components"][0]["parameters"]
        assert all("\n" not in p["text"] for p in params) and len(params[1]["text"]) <= 600

    async def test_inside_the_window_the_verse_card_goes_out_free(self, graph, data):
        store, uid = await self._set_up(graph, data)
        await handle_message(graph.client, data, wa_tap("hd:t:07:00"))
        await handle_message(graph.client, data, wa_tap("hd:ok:07:00"))
        (row,) = await _due_rows(store)
        graph.sent.clear()
        ctx = SendCtx(
            bot=None, data=data, file=None, store=store, send=row, now=datetime.now(timezone.utc)
        )
        await daily.push_daily(ctx)
        assert [m["type"] for m in graph.sent] == ["text", "interactive"]
        assert graph.sent[0]["text"]["body"].startswith("🌅 *")

    async def test_free_mode_skips_outside_the_window_and_keeps_the_subscription(self, graph, data):
        store, uid = await self._set_up(graph, data)
        await handle_message(graph.client, data, wa_tap("hd:t:07:00"))
        await handle_message(graph.client, data, wa_tap("hd:ok:07:00"))
        (row,) = await _due_rows(store)
        graph.sent.clear()
        later = datetime.now(timezone.utc) + timedelta(days=2)  # no message since: no window
        ctx = SendCtx(bot=None, data=data, file=None, store=store, send=row, now=later)
        await daily.push_daily(ctx)
        assert graph.sent == []  # nothing billed
        assert (await store.daily.get(uid)).enabled is True  # still subscribed
        assert len(await _due_rows(store)) == 2  # and tomorrow is queued

    async def test_stop_turns_it_off_and_later_sends_are_dropped(self, graph, data):
        store, uid = await self._set_up(graph, data)
        await handle_message(graph.client, data, wa_tap("hd:t:07:00"))
        await handle_message(graph.client, data, wa_tap("hd:ok:07:00"))
        await handle_message(graph.client, data, wa_text("STOP"))
        assert (await store.daily.get(uid)).enabled is False
        (row,) = await _due_rows(store)
        graph.sent.clear()
        ctx = SendCtx(bot=None, data=data, file=None, store=store, send=row, now=NOW)
        await daily.push_daily(ctx)
        assert graph.sent == []
