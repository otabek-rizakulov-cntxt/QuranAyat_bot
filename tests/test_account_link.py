"""Linking a Telegram account and a WhatsApp number (MULTI_PLATFORM_PLAN Phase 6)."""

import json
import re
from unittest.mock import AsyncMock

import httpx
import pytest
import telegram

import app.lifespan as lifespan
import bot.dispatch as dispatch
import channels.whatsapp as wa
from bot.whatsapp import handle_message
from channels.whatsapp import GraphClient
from infra import account_link
from infra.store import get_store
from locales import t

TG = 777001
WA_ID = "998907770001"


@pytest.fixture(scope="module")
def data():
    return lifespan.build_data()


class Apps:
    """A user with Telegram and WhatsApp, driven through both real entry points."""

    def __init__(self, data, monkeypatch):
        self.data = data
        self.tg = telegram.Bot("123456:TEST-abcdefghijklmnopqrstuvwxyz")
        self.bot = AsyncMock()
        self.wa_sent = []

        def graph(request):
            self.wa_sent.append(json.loads(request.content))
            return httpx.Response(200, json={"messages": [{"id": "wamid.x"}]})

        async def no_sleep(_):
            return None

        monkeypatch.setattr(wa, "_sleep", no_sleep)
        self.client = GraphClient("P", "T", transport=httpx.MockTransport(graph))
        self.n = 0

    async def telegram(self, text, user=TG):
        self.n += 1
        update = {
            "update_id": self.n,
            "message": {
                "message_id": self.n,
                "date": 1700000000,
                "chat": {"id": user, "type": "private"},
                "from": {"id": user, "is_bot": False, "first_name": "T", "language_code": "en"},
                "text": text,
            },
        }
        await dispatch.handle_update(self.bot, self.data, telegram.Update.de_json(update, self.tg))
        return self.bot.send_message.await_args.kwargs["text"]

    async def whatsapp(self, text, wa_id=WA_ID):
        self.n += 1
        self.wa_sent.clear()
        message = {"from": wa_id, "id": "m%d" % self.n, "type": "text", "text": {"body": text}}
        await handle_message(self.client, self.data, message)
        return self.wa_sent[-1]["text"]["body"] if self.wa_sent else None

    async def wa_user(self, wa_id=WA_ID):
        store = await get_store()
        await self.whatsapp("menu", wa_id)  # first contact
        return (await store.identity.get("whatsapp", wa_id)).user_id


def _code(text):
    return re.search(r"link (\d{6})", text).group(1)


@pytest.fixture
def apps(data, monkeypatch):
    return Apps(data, monkeypatch)


class TestCodes:
    def test_single_use(self):
        code = account_link.issue(1)
        assert account_link.redeem(code, 2) == 1
        assert account_link.redeem(code, 2) is None

    def test_wrong_codes_are_limited(self):
        for _ in range(account_link.MAX_TRIES):
            assert not account_link.too_many_tries(9)
            assert account_link.redeem("000000", 9) is None
        assert account_link.too_many_tries(9)


class TestLinking:
    async def test_telegram_code_entered_on_whatsapp(self, apps):
        store = await get_store()
        old_wa = await apps.wa_user()
        await store.hifz.add_interval(TG, 112, 1, 4)  # progress made on Telegram
        await store.daily.upsert(old_wa, "whatsapp", __import__("datetime").time(7, 0))

        code = _code(await apps.telegram("/link"))
        reply = await apps.whatsapp("link " + code)
        assert reply == t("link_done", "uz")

        assert await store.identity.resolve("whatsapp", WA_ID) == TG
        assert (await store.daily.get(old_wa)).enabled is False
        # WhatsApp now reads the Telegram account's progress (and its settings)
        progress = await apps.whatsapp("progress")
        assert progress != t("progress_empty", "en") and progress != t("progress_empty", "uz")

    async def test_whatsapp_code_entered_on_telegram(self, apps):
        store = await get_store()
        await apps.wa_user()
        apps.wa_sent.clear()
        await apps.whatsapp("link")
        code = _code(apps.wa_sent[-1]["text"]["body"])
        assert await apps.telegram("/link " + code) == t("link_done", "en")
        assert await store.identity.resolve("whatsapp", WA_ID) == TG

    async def test_two_telegram_accounts_cannot_link(self, apps):
        code = _code(await apps.telegram("/link", user=TG))
        assert await apps.telegram("/link " + code, user=TG + 1) == t("link_same", "en")

    async def test_one_number_per_telegram_account(self, apps):
        await apps.wa_user()
        await apps.wa_user("998907770002")
        code = _code(await apps.telegram("/link"))
        await apps.whatsapp("link " + code)
        code = _code(await apps.telegram("/link"))
        assert await apps.whatsapp("link " + code, "998907770002") == t("link_taken", "uz")

    async def test_a_bad_code(self, apps):
        await apps.wa_user()
        assert await apps.whatsapp("link 123456") == t("link_bad_code", "uz")

    async def test_unlink_from_whatsapp_starts_fresh(self, apps):
        store = await get_store()
        await apps.wa_user()
        await apps.whatsapp("link " + _code(await apps.telegram("/link")))
        # linked, the number speaks the Telegram account's language
        assert await apps.whatsapp("unlink") == t("link_unlinked", "en")
        await apps.whatsapp("menu")
        fresh = await store.identity.resolve("whatsapp", WA_ID)
        assert fresh != TG and fresh >= 2**52

    async def test_unlink_from_telegram(self, apps):
        store = await get_store()
        await apps.wa_user()
        await apps.whatsapp("link " + _code(await apps.telegram("/link")))
        assert await apps.telegram("/unlink") == t("link_unlinked", "en")
        assert await store.identity.get_by_user(TG, "whatsapp") is None

    async def test_nothing_to_unlink(self, apps):
        assert await apps.telegram("/unlink") == t("link_not_linked", "en")
