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
from bot.whatsapp import as_command, handle_message, lang_hint
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
    async def test_welcome_hint_and_language_picker(self, client, data, graph):
        await handle_message(client, data, text("menu"))
        messages = graph.messages()
        assert len(messages) == 3  # welcome, the WhatsApp hint, the language picker
        assert "*" in messages[0]["text"]["body"]  # HTML converted, not raw <b>
        assert "<b>" not in messages[1]["text"]["body"]
        # 48 interface languages: more than a list holds, so a numbered menu
        assert messages[2]["type"] == "text" and "\n1. " in messages[2]["text"]["body"]

    async def test_uzbek_number_gets_uzbek(self, client, data, graph):
        await handle_message(client, data, text("menu"))
        hint = graph.messages()[1]["text"]["body"]
        assert "kunlik" in hint

    async def test_identity_and_window(self, client, data, graph):
        await handle_message(client, data, text("2:255"))
        store = await get_store()
        row = await store.identity.get(WHATSAPP, WA_ID)
        assert row.user_id >= 2**52 and row.last_inbound_at is not None

    async def test_a_first_message_is_also_answered(self, client, data, graph):
        await handle_message(client, data, text("2:255"))
        assert len(graph.messages()) == 4  # the welcome trio, then the verse card


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
