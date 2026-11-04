"""A WhatsApp message end to end: bot.whatsapp -> handle_incoming -> the real
handlers -> the WhatsApp channel -> a mocked Graph API (MULTI_PLATFORM_PLAN P2.4).
"""

import io
import json
import os

import httpx
import pytest

import app.lifespan as lifespan
import bot.media
import channels.whatsapp as wa
from bot.whatsapp import STARTERS, as_command, handle_message, lang_hint
from channels import WHATSAPP
from channels.whatsapp import GraphClient
from infra import nav_state
from infra.store import get_store
from locales import t

WA_ID = "998901234567"
FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures", "whatsapp")


@pytest.fixture(scope="module")
def data():
    return lifespan.build_data()


class Graph:
    def __init__(self):
        self.requests = []

    def __call__(self, request):
        self.requests.append(request)
        if request.url.path.endswith("/media"):
            return httpx.Response(200, json={"id": "media-%d" % len(self.requests)})
        return httpx.Response(200, json={"messages": [{"id": "wamid.%d" % len(self.requests)}]})

    def messages(self):
        return [json.loads(r.content) for r in self.requests if r.url.path.endswith("/messages")]

    def clear(self):
        self.requests.clear()


@pytest.fixture
def graph(monkeypatch):
    async def no_sleep(_):
        return None

    monkeypatch.setattr(wa, "_sleep", no_sleep)
    return Graph()


@pytest.fixture
def client(graph):
    return GraphClient("PHONE", "TOKEN", transport=httpx.MockTransport(graph))


def text(body, wa_id=WA_ID, mid="wamid.in"):
    return {"from": wa_id, "id": mid, "type": "text", "text": {"body": body}}


def tap(data_, kind="button_reply"):
    return {
        "from": WA_ID,
        "id": "wamid.tap",
        "type": "interactive",
        "context": {"id": "wamid.card"},
        "interactive": {"type": kind, kind: {"id": data_, "title": "x"}},
    }


def fixture_message(name):
    with open(os.path.join(FIXTURES, name + ".json")) as f:
        payload = json.load(f)
    return payload["entry"][0]["changes"][0]["value"]["messages"][0]


async def known_user(client, data, graph):
    """A user past first contact, with the welcome messages cleared."""
    await handle_message(client, data, text("menu"))
    graph.clear()


def bodies(graph):
    out = []
    for m in graph.messages():
        if m["type"] == "text":
            out.append(m["text"]["body"])
        elif m["type"] == "interactive":
            out.append(m["interactive"]["body"]["text"])
    return out


class TestKeywords:
    @pytest.mark.parametrize(
        "typed, command",
        [
            ("menu", "/help"),
            ("Menyu", "/help"),
            ("reciter", "/reciter"),
            ("qori", "/reciter"),
            ("page 255", "/page 255"),
            ("sahifa  12", "/page 12"),
            ("Страница 3", "/page 3"),
            ("juz 30", "/juz 30"),
            ("2:255", "2:255"),
            ("Al-Baqara 255", "Al-Baqara 255"),
        ],
    )
    def test_words_become_commands(self, typed, command):
        assert as_command(typed) == command

    def test_language_from_the_calling_code(self):
        assert lang_hint("998901234567") == "uz"
        assert lang_hint("79161234567") == "ru"
        assert lang_hint("966501234567") == "ar"
        assert lang_hint("4915112345678") is None


class TestFirstContact:
    async def test_one_welcome_card_with_three_ways_in(self, client, data, graph):
        await handle_message(client, data, text("menu"))
        (card,) = graph.messages()
        interactive = card["interactive"]
        assert interactive["type"] == "button"
        assert interactive["header"]["text"] == t("wa_welcome_title", "uz")
        assert "STOP" in interactive["footer"]["text"]
        assert "<b>" not in interactive["body"]["text"]  # HTML converted
        ids = [b["reply"]["id"] for b in interactive["action"]["buttons"]]
        assert ids == ["hd:now", "wm:menu", "showlang"]

    async def test_uzbek_number_gets_uzbek(self, client, data, graph):
        await handle_message(client, data, text("menu"))
        assert "menyu" in graph.messages()[0]["interactive"]["body"]["text"]

    async def test_identity_and_window(self, client, data, graph):
        await handle_message(client, data, text("2:255"))
        store = await get_store()
        row = await store.identity.get(WHATSAPP, WA_ID)
        assert row.user_id >= 2**52 and row.last_inbound_at is not None

    async def test_a_first_message_is_also_answered(self, client, data, graph):
        await handle_message(client, data, text("2:255"))
        messages = graph.messages()
        assert messages[0]["interactive"]["header"]["text"] == t("wa_welcome_title", "uz")
        assert len(messages) == 2  # the welcome card, then the verse card

    async def test_opening_the_chat_sends_the_welcome_before_they_type(self, client, data, graph):
        await handle_message(client, data, {"from": WA_ID, "id": "w", "type": "request_welcome"})
        (card,) = graph.messages()
        assert card["interactive"]["header"]["text"] == t("wa_welcome_title", "uz")


class TestUsernames:
    """Since 2026 a sender may come with a business-scoped user id (BSUID), or only that."""

    BSUID = "UZ.13491208655302741918"

    async def test_bsuid_only_sender_is_answered_by_recipient(self, client, data, graph):
        message = {"from_user_id": self.BSUID, "id": "u1", "type": "text"}
        message["text"] = {"body": "2:255"}
        await handle_message(client, data, message)
        sent = graph.messages()
        assert sent and all(m["recipient"] == self.BSUID and "to" not in m for m in sent)
        # Uzbek from the BSUID's country, as a +998 number would be
        assert "menyu" in sent[0]["interactive"]["body"]["text"]

    async def test_number_and_bsuid_reply_by_number(self, client, data, graph):
        message = text("2:255")
        message["from_user_id"] = self.BSUID
        await handle_message(client, data, message)
        assert all(m["to"] == WA_ID for m in graph.messages())
        store = await get_store()
        assert (await store.identity.get(WHATSAPP, WA_ID)).alt_id == self.BSUID

    def test_language_from_the_bsuid_country(self):
        assert lang_hint("UZ.1349") == "uz" and lang_hint("RU.77") == "ru"
        assert lang_hint("DE.1") is None


def rows(message):
    return message["interactive"]["action"]["sections"][0]["rows"]


class TestMenu:
    async def test_menu_is_a_list_of_ten_with_descriptions(self, client, data, graph):
        await known_user(client, data, graph)
        await handle_message(client, data, text("menu"))
        (menu,) = graph.messages()
        assert menu["interactive"]["type"] == "list"
        assert menu["interactive"]["action"]["button"] == t("wa_menu_button", "uz")
        assert len(rows(menu)) == 10 and all(r.get("description") for r in rows(menu))
        assert all(len(r["title"]) <= 24 for r in rows(menu))

    async def test_slash_commands_from_the_command_list(self, client, data, graph):
        await known_user(client, data, graph)
        await handle_message(client, data, text("/menu"))
        assert graph.messages()[0]["interactive"]["type"] == "list"
        assert as_command("/daily") == "/daily" and as_command("/page 3") == "/page 3"

    @pytest.mark.parametrize("lang", ["en", "ru", "uz", "uz-Cyrl"])
    def test_every_label_fits_whatsapp(self, lang):
        from bot.keyboards.menu import main_menu, settings_menu, welcome_choices

        for row in main_menu(lang) + settings_menu(lang):
            assert len(row[0].label) <= 24 and len(row[0].hint) <= 72
        assert all(len(c.label) <= 20 for c in welcome_choices(lang)[0])
        assert len(t("wa_menu_button", lang)) <= 20
        assert len(t("wa_welcome_footer", lang)) <= 60 and len(t("wa_menu_footer", lang)) <= 60

    async def test_every_row_does_something(self, client, data, graph, monkeypatch):
        from bot.keyboards.menu import main_menu, settings_menu

        async def stitch(urls, name):  # the mushaf page row, without the network
            page = io.BytesIO(b"jpeg")
            page.name = name
            return page

        monkeypatch.setattr(bot.media, "fetch_and_stitch", stitch)
        await known_user(client, data, graph)
        for row in main_menu("uz") + settings_menu("uz"):
            graph.clear()
            await handle_message(client, data, tap(row[0].data, "list_reply"))
            assert graph.messages(), row[0].data
            assert t("wa_not_here", "uz") not in bodies(graph), row[0].data

    async def test_settings_and_back(self, client, data, graph):
        await known_user(client, data, graph)
        await handle_message(client, data, tap("wm:settings", "list_reply"))
        (settings,) = graph.messages()
        assert [r["id"] for r in rows(settings)][-1] == "wm:menu"

    async def test_todays_verse_then_the_offer(self, client, data, graph):
        await known_user(client, data, graph)
        await handle_message(client, data, tap("hd:now"))
        sent = graph.messages()
        assert sent[0]["text"]["body"].startswith("🌅 *")
        offer = sent[-1]["interactive"]
        assert offer["body"]["text"] == t("daily_offer", "uz")
        assert offer["action"]["buttons"][0]["reply"]["id"] == "hd:on"

    async def test_short_language_list_then_all(self, client, data, graph):
        await known_user(client, data, graph)
        await handle_message(client, data, tap("showlang"))
        (short,) = graph.messages()
        ids = [r["id"] for r in rows(short)]
        assert len(ids) == 10 and ids[-1] == "showlang:all" and "setlang:uz" in ids
        graph.clear()
        await handle_message(client, data, tap("showlang:all", "list_reply"))
        assert "\n48. " in graph.messages()[0]["text"]["body"]  # every language, numbered


class TestStarters:
    @pytest.mark.parametrize("starter", list(STARTERS))
    async def test_each_starter_is_understood(self, client, data, graph, starter):
        await known_user(client, data, graph)
        await handle_message(client, data, text(starter))
        sent = bodies(graph)
        assert sent and t("wa_not_here", "uz") not in sent
        assert not any(b.startswith(t("ayah_not_found", "uz")) for b in sent)


class TestReader:
    async def test_a_reference_gets_a_verse_card_with_buttons(self, client, data, graph):
        await known_user(client, data, graph)
        await handle_message(client, data, text("2:255"))
        (card,) = graph.messages()
        assert card["type"] == "interactive" and card["interactive"]["type"] == "list"
        assert card["interactive"]["body"]["text"].startswith("*")
        ids = [r["id"] for r in card["interactive"]["action"]["sections"][0]["rows"]]
        assert "vc:ar:2:255" in ids and "showlang" in ids
        store = await get_store()
        uid = (await store.identity.get(WHATSAPP, WA_ID)).user_id
        assert list(await nav_state.get(uid))[:2] == [2, 255]

    async def test_a_tapped_view_sends_the_arabic_image_by_link(self, client, data, graph):
        await known_user(client, data, graph)
        await handle_message(client, data, fixture_message("button_reply"))
        image = graph.messages()[0]
        assert image["type"] == "image" and image["image"]["link"].startswith("http")

    async def test_a_tapped_text_view_is_a_new_message(self, client, data, graph):
        await known_user(client, data, graph)
        await handle_message(client, data, tap("vc:tf:1:1", "list_reply"))
        assert len(graph.messages()) == 1  # no edit on WhatsApp: a fresh card

    async def test_a_page_is_uploaded_once(self, client, data, graph, monkeypatch):
        async def stitch(urls, name):
            page = io.BytesIO(b"jpeg")
            page.name = name
            return page

        monkeypatch.setattr(bot.media, "fetch_and_stitch", stitch)
        await known_user(client, data, graph)
        await handle_message(client, data, text("page 1"))
        await handle_message(client, data, text("sahifa 1"))
        uploads = [r for r in graph.requests if r.url.path.endswith("/media")]
        assert len(uploads) == 1
        images = [m for m in graph.messages() if m["type"] == "image"]
        assert len(images) == 2 and all("id" in m["image"] for m in images)

    async def test_the_reciter_menu_is_numbered_and_answered_by_number(self, client, data, graph):
        await known_user(client, data, graph)
        await handle_message(client, data, text("reciter"))
        (menu,) = graph.messages()
        assert menu["type"] == "text" and "\n1. " in menu["text"]["body"]
        graph.clear()
        await handle_message(client, data, text("1"))  # the first tab: Reciters
        assert graph.messages(), "a numbered reply should act like a tap"

    async def test_language_change_by_list_reply(self, client, data, graph):
        await known_user(client, data, graph)
        await handle_message(client, data, fixture_message("list_reply"))
        assert bodies(graph)[-1] == t("language_set", "ru").format(lang="Русский")


class TestBoundaries:
    async def test_telegram_only_features_are_not_offered(self, client, data, graph):
        # hifz groups live in Telegram supergroups; there is no WhatsApp form yet
        await known_user(client, data, graph)
        await handle_message(client, data, text("/start gs_-100123"))
        assert "*" in bodies(graph)[0]  # the plain welcome, not group setup
        graph.clear()
        await handle_message(client, data, tap("gr:ok"))
        await handle_message(client, data, text("/admin"))
        assert bodies(graph) == [t("wa_not_here", "uz")] * 2

    async def test_media_we_cannot_read(self, client, data, graph):
        await known_user(client, data, graph)
        await handle_message(client, data, fixture_message("image"))
        assert bodies(graph) == [t("wa_unsupported", "uz")]

    async def test_reactions_are_silent(self, client, data, graph):
        await known_user(client, data, graph)
        await handle_message(
            client, data, {"from": WA_ID, "id": "r", "type": "reaction", "reaction": {}}
        )
        assert graph.messages() == []

    async def test_stop_withdraws_consent(self, client, data, graph):
        await known_user(client, data, graph)
        store = await get_store()
        uid = (await store.identity.get(WHATSAPP, WA_ID)).user_id
        await store.identity.opt_in(
            uid, WHATSAPP, (await store.identity.get(WHATSAPP, WA_ID)).last_inbound_at
        )
        await handle_message(client, data, text("STOP"))
        assert not (await store.identity.get_by_user(uid, WHATSAPP)).consented
        assert bodies(graph) == [t("wa_stopped", "uz")]
