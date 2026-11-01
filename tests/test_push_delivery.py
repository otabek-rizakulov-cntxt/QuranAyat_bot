"""Window-aware delivery of scheduled pushes (MULTI_PLATFORM_PLAN P2.6).

The policy and money risks: a template must never go to someone who has not
opted in, and a free session message must be used whenever the window is open.
"""

import json
import logging
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import httpx
import pytest

import channels.whatsapp as wa
import infra.scheduler.push as push
from channels.whatsapp import GraphClient
from infra.scheduler import SendCtx
from infra.scheduler.push import DROPPED, SESSION, TEMPLATE, Template, deliver_push
from infra.store import InMemoryStore
from infra.store.schedule import ScheduledSend

NOW = datetime(2026, 11, 2, 7, 0, tzinfo=timezone.utc)
WA_ID = "998901234567"
TEMPLATE_ = Template("daily_ayah", "uz", ["2:255", "Allah"], ["vc:tr:2:255"])


class Graph:
    def __init__(self):
        self.sent = []
        self.queue = []

    def __call__(self, request):
        self.sent.append(json.loads(request.content))
        if self.queue:
            return self.queue.pop(0)
        return httpx.Response(200, json={"messages": [{"id": "wamid.x"}]})


@pytest.fixture
def graph(monkeypatch):
    graph = Graph()

    async def no_sleep(_):
        return None

    monkeypatch.setattr(wa, "_sleep", no_sleep)
    monkeypatch.setattr(
        push, "_whatsapp_client", GraphClient("P", "T", transport=httpx.MockTransport(graph))
    )
    return graph


@pytest.fixture
def store():
    return InMemoryStore()


def ctx_for(store, user_id, platform, bot=None):
    row = ScheduledSend(
        id=1,
        kind="daily_ayah",
        target_chat_id=user_id,
        due_at=NOW,
        idempotency_key="k",
        platform=platform,
    )
    return SendCtx(bot=bot or AsyncMock(), data={}, file=None, store=store, send=row, now=NOW)


async def wa_user(store, *, consent=True, wrote_ago=None):
    uid = await store.identity.resolve("whatsapp", WA_ID)
    if consent:
        await store.identity.opt_in(uid, "whatsapp", NOW - timedelta(days=3))
    if wrote_ago is not None:
        await store.identity.touch_inbound(uid, "whatsapp", NOW - wrote_ago)
    return uid


async def say_hi(channel):
    await channel.send_text("hi")


class TestTelegram:
    async def test_always_the_session_message(self, store):
        bot = AsyncMock()
        outcome = await deliver_push(ctx_for(store, 42, "telegram", bot), session=say_hi)
        assert outcome == SESSION
        bot.send_message.assert_awaited_once_with(chat_id=42, text="hi")


class TestWhatsApp:
    async def test_inside_the_window_is_free(self, store, graph):
        uid = await wa_user(store, wrote_ago=timedelta(hours=2))
        outcome = await deliver_push(
            ctx_for(store, uid, "whatsapp"), session=say_hi, template=TEMPLATE_
        )
        assert outcome == SESSION
        assert [m["type"] for m in graph.sent] == ["text"]
        assert graph.sent[0]["to"] == WA_ID

    async def test_outside_the_window_is_the_template(self, store, graph):
        uid = await wa_user(store, wrote_ago=timedelta(hours=30))
        outcome = await deliver_push(
            ctx_for(store, uid, "whatsapp"), session=say_hi, template=TEMPLATE_
        )
        assert outcome == TEMPLATE
        (message,) = graph.sent
        assert message["template"]["name"] == "daily_ayah"
        assert message["template"]["components"][1]["parameters"][0]["payload"] == "vc:tr:2:255"

    async def test_never_wrote_is_outside_the_window(self, store, graph):
        uid = await wa_user(store)
        outcome = await deliver_push(
            ctx_for(store, uid, "whatsapp"), session=say_hi, template=TEMPLATE_
        )
        assert outcome == TEMPLATE

    async def test_the_window_edge_is_conservative(self, store, graph):
        uid = await wa_user(store, wrote_ago=timedelta(hours=23, minutes=55))
        outcome = await deliver_push(
            ctx_for(store, uid, "whatsapp"), session=say_hi, template=TEMPLATE_
        )
        assert outcome == TEMPLATE

    async def test_meta_saying_closed_falls_back_to_the_template(self, store, graph):
        uid = await wa_user(store, wrote_ago=timedelta(hours=1))
        graph.queue = [httpx.Response(400, json={"error": {"code": 131047, "message": "closed"}})]
        outcome = await deliver_push(
            ctx_for(store, uid, "whatsapp"), session=say_hi, template=TEMPLATE_
        )
        assert outcome == TEMPLATE

    async def test_no_template_outside_the_window_sends_nothing(self, store, graph):
        uid = await wa_user(store, wrote_ago=timedelta(hours=30))
        assert await deliver_push(ctx_for(store, uid, "whatsapp"), session=say_hi) == DROPPED
        assert graph.sent == []


class TestConsent:
    """No template — and no message at all — without opt-in."""

    @pytest.mark.parametrize("wrote_ago", [None, timedelta(hours=1), timedelta(hours=30)])
    async def test_never_opted_in(self, store, graph, wrote_ago):
        uid = await wa_user(store, consent=False, wrote_ago=wrote_ago)
        outcome = await deliver_push(
            ctx_for(store, uid, "whatsapp"), session=say_hi, template=TEMPLATE_
        )
        assert outcome == DROPPED and graph.sent == []

    async def test_after_stop(self, store, graph):
        uid = await wa_user(store, wrote_ago=timedelta(hours=1))
        await store.identity.opt_out(uid, "whatsapp", NOW - timedelta(minutes=5))
        outcome = await deliver_push(
            ctx_for(store, uid, "whatsapp"), session=say_hi, template=TEMPLATE_
        )
        assert outcome == DROPPED and graph.sent == []

    async def test_unknown_user(self, store, graph):
        outcome = await deliver_push(
            ctx_for(store, 2**52 + 9, "whatsapp"), session=say_hi, template=TEMPLATE_
        )
        assert outcome == DROPPED and graph.sent == []

    async def test_whatsapp_off(self, store, graph, monkeypatch):
        monkeypatch.setattr(push, "_whatsapp_client", None)
        uid = await wa_user(store, wrote_ago=timedelta(hours=1))
        outcome = await deliver_push(
            ctx_for(store, uid, "whatsapp"), session=say_hi, template=TEMPLATE_
        )
        assert outcome == DROPPED and graph.sent == []


async def test_every_push_is_logged_for_cost_tracking(store, graph, caplog):
    uid = await wa_user(store, wrote_ago=timedelta(hours=30))
    with caplog.at_level(logging.INFO, logger="infra.scheduler.push"):
        await deliver_push(ctx_for(store, uid, "whatsapp"), session=say_hi, template=TEMPLATE_)
    (line,) = [r.getMessage() for r in caplog.records]
    assert "platform=whatsapp" in line and "outcome=template" in line
    assert "category=marketing" in line and "template=daily_ayah" in line
