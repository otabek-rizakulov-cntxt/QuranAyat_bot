"""The WhatsApp channel against a mocked Graph API: one test per message shape,
plus how it degrades what WhatsApp cannot show."""

import io
import json

import httpx
import pytest

import channels.whatsapp as wa
from channels import WHATSAPP, Choice, for_platform
from channels.whatsapp import GraphClient, WhatsAppChannel, WhatsAppError, WindowClosed
from infra import choice_memory, media_cache

WA_ID = "998901234567"
UID = 2**52


class Graph:
    """Records every request; answers with queued responses, else a sent message."""

    def __init__(self):
        self.requests = []
        self.queue = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if self.queue:
            return self.queue.pop(0)
        if request.url.path.endswith("/media"):
            return httpx.Response(200, json={"id": "media-%d" % len(self.requests)})
        return httpx.Response(200, json={"messages": [{"id": "wamid.%d" % len(self.requests)}]})

    def messages(self):
        return [json.loads(r.content) for r in self.requests if r.url.path.endswith("/messages")]


@pytest.fixture
def graph(monkeypatch):
    async def no_sleep(_):
        return None

    monkeypatch.setattr(wa, "_sleep", no_sleep)
    return Graph()


@pytest.fixture
def channel(graph):
    client = GraphClient("PHONE", "TOKEN", transport=httpx.MockTransport(graph))
    return WhatsAppChannel(client, WA_ID, UID)


@pytest.fixture
def cache(monkeypatch):
    store = {}
    monkeypatch.setattr(media_cache, "get", store.get)
    monkeypatch.setattr(media_cache, "save", store.__setitem__)
    return store


def taps(*labels):
    return [[Choice(label, data="d:%d" % n) for n, label in enumerate(labels)]]


class TestTransport:
    async def test_addresses_and_authenticates(self, channel, graph):
        assert await channel.send_text("hi") == "wamid.1"
        request = graph.requests[0]
        assert request.url.path == "/%s/PHONE/messages" % wa.DEFAULT_GRAPH_VERSION
        assert request.headers["Authorization"] == "Bearer TOKEN"
        assert graph.messages()[0] == {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": WA_ID,
            "type": "text",
            "text": {"body": "hi", "preview_url": False},
        }

    async def test_retries_rate_limits_then_succeeds(self, channel, graph):
        graph.queue = [httpx.Response(429), httpx.Response(503)]
        assert await channel.send_text("hi") == "wamid.3"
        assert len(graph.requests) == 3

    async def test_gives_up_after_the_last_retry(self, channel, graph):
        graph.queue = [httpx.Response(500)] * 4
        with pytest.raises(WhatsAppError):
            await channel.send_text("hi")

    async def test_window_closed_is_its_own_error(self, channel, graph):
        graph.queue = [
            httpx.Response(400, json={"error": {"code": 131047, "message": "Re-engagement"}})
        ]
        with pytest.raises(WindowClosed) as err:
            await channel.send_text("hi")
        assert err.value.code == 131047

    async def test_client_errors_are_not_retried(self, channel, graph):
        graph.queue = [httpx.Response(400, json={"error": {"code": 100, "message": "bad"}})]
        with pytest.raises(WhatsAppError):
            await channel.send_text("hi")
        assert len(graph.requests) == 1


class TestText:
    async def test_html_is_converted(self, channel, graph):
        await channel.send_text("<b>2:255</b> &amp; more", html=True, parse_mode="HTML")
        assert graph.messages()[0]["text"]["body"] == "*2:255* & more"

    async def test_long_text_is_split(self, channel, graph):
        await channel.send_text(("word " * 1000).strip())
        bodies = [m["text"]["body"] for m in graph.messages()]
        assert len(bodies) == 2 and all(len(b) <= 4096 for b in bodies)

    async def test_telegram_only_options_are_ignored(self, channel, graph):
        await channel.send_text("hi", reply_markup=object(), disable_web_page_preview=True)
        assert graph.messages()[0]["text"] == {"body": "hi", "preview_url": False}


class TestChoices:
    async def test_up_to_three_short_choices_are_buttons(self, channel, graph):
        await channel.send_text("Pick", taps("One", "Two", "Three"))
        (message,) = graph.messages()
        assert message["type"] == "interactive"
        interactive = message["interactive"]
        assert interactive["type"] == "button" and interactive["body"] == {"text": "Pick"}
        assert [b["reply"] for b in interactive["action"]["buttons"]] == [
            {"id": "d:0", "title": "One"},
            {"id": "d:1", "title": "Two"},
            {"id": "d:2", "title": "Three"},
        ]

    async def test_a_long_label_makes_it_a_list(self, channel, graph):
        await channel.send_text("Pick", taps("One", "A label longer than twenty characters"))
        interactive = graph.messages()[0]["interactive"]
        assert interactive["type"] == "list"
        rows = interactive["action"]["sections"][0]["rows"]
        assert rows[0] == {"id": "d:0", "title": "One"}
        assert len(rows[1]["title"]) <= 24 and rows[1]["description"].startswith("A label")

    async def test_up_to_ten_choices_are_a_list(self, channel, graph):
        await channel.send_text("Pick", taps(*["#%d" % n for n in range(10)]))
        interactive = graph.messages()[0]["interactive"]
        assert interactive["type"] == "list"
        assert len(interactive["action"]["sections"][0]["rows"]) == 10

    async def test_more_become_numbered_text_answered_by_number(self, channel, graph):
        await channel.send_text("Pick", taps(*["Reciter %d" % n for n in range(12)]))
        body = graph.messages()[0]["text"]["body"]
        assert body.startswith("Pick\n\n1. Reciter 0\n2. Reciter 1")
        assert choice_memory.pick(UID, "12") == "d:11"
        assert choice_memory.pick(UID, " 3. ") == "d:2"
        assert choice_memory.pick(UID, "13") is None
        assert choice_memory.pick(UID, "2:255") is None

    async def test_links_are_appended_and_app_buttons_dropped(self, channel, graph):
        rows = [
            [Choice("Site", url="https://q.example")],
            [Choice("App", web_app="https://app.example"), Choice("📤", switch_inline="2:255")],
        ]
        await channel.send_text("Read", rows)
        (message,) = graph.messages()
        assert message["text"] == {"body": "Read\n\nSite: https://q.example", "preview_url": True}

    async def test_buttons_ride_on_the_last_chunk(self, channel, graph):
        await channel.send_text(("word " * 1000).strip(), taps("Next"))
        first, second = graph.messages()
        assert first["type"] == "text" and second["type"] == "interactive"
        assert (
            len(second["interactive"]["body"]["text"]) <= 1024
            or second["interactive"]["body"]["text"] == wa.CHOICES_BODY
        )

    async def test_an_edit_is_a_new_message(self, channel, graph):
        assert await channel.edit_text("wamid.0", "new", taps("A")) is False
        assert graph.messages()[0]["interactive"]["body"]["text"] == "new"
        assert await channel.edit_choices("wamid.0", taps("A")) is False


class TestMedia:
    async def test_a_url_goes_by_link(self, channel, graph):
        await channel.send_image("https://img/2_255.png", caption="2:255")
        assert graph.messages()[0] == {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": WA_ID,
            "type": "image",
            "image": {"link": "https://img/2_255.png", "caption": "2:255"},
        }

    async def test_bytes_are_uploaded_once_and_the_id_cached(self, channel, graph, cache):
        built = []

        async def stitch():
            built.append(1)
            page = io.BytesIO(b"jpeg")
            page.name = "page_255.jpg"
            return page

        await channel.send_image(stitch, caption="Page 255", cache_key="page:255")
        await channel.send_image(stitch, caption="Page 255", cache_key="page:255")
        uploads = [r for r in graph.requests if r.url.path.endswith("/media")]
        assert len(uploads) == 1 and len(built) == 1
        assert b"image/jpeg" in uploads[0].content
        assert cache["wa:page:255"] == "media-1"
        images = [m["image"] for m in graph.messages()]
        assert images == [{"id": "media-1", "caption": "Page 255"}] * 2

    async def test_choices_after_an_image_follow_it(self, channel, graph):
        await channel.send_image("https://img/p.png", choices=taps("Prev", "Next"))
        image, buttons = graph.messages()
        assert image["type"] == "image" and buttons["type"] == "interactive"

    async def test_audio_title_and_buttons_follow_the_audio(self, channel, graph):
        await channel.send_audio(
            "https://audio/002255.mp3", title="2:255", performer="Husary", choices=taps("Next")
        )
        audio, label = graph.messages()
        assert audio["audio"] == {"link": "https://audio/002255.mp3"}
        assert label["interactive"]["body"]["text"] == "2:255 · Husary"

    async def test_uploaded_audio_is_mp3(self, channel, graph, cache):
        clip = io.BytesIO(b"mp3")
        clip.name = "quran_2_255_x3.mp3"
        await channel.send_audio(clip, cache_key="repeat:3:2:255:Husary")
        upload = next(r for r in graph.requests if r.url.path.endswith("/media"))
        assert b"audio/mpeg" in upload.content


class TestTheRest:
    async def test_template(self, channel, graph):
        await channel.send_template("daily_ayah", "en", ["2:255", "Allah"])
        assert graph.messages()[0]["template"] == {
            "name": "daily_ayah",
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": "2:255"},
                        {"type": "text", "text": "Allah"},
                    ],
                }
            ],
        }

    async def test_answer_text_becomes_a_message(self, channel, graph):
        await channel.answer("tap-1")
        assert graph.messages() == []
        await channel.answer("tap-1", "Saved")
        assert graph.messages()[0]["text"]["body"] == "Saved"

    async def test_typing_is_a_no_op(self, channel, graph):
        await channel.typing("audio")
        assert graph.requests == []

    async def test_factory(self, channel):
        built = for_platform(WHATSAPP, external_id=WA_ID, chat_id=UID, client=channel.client)
        assert isinstance(built, WhatsAppChannel)
        assert (built.wa_id, built.chat_id, built.caps.can_edit) == (WA_ID, UID, False)
        with pytest.raises(ValueError):
            for_platform(WHATSAPP, external_id=WA_ID)


class TestNumberedMenuLifetime:
    async def test_a_later_message_retires_the_menu(self, channel, graph):
        await channel.send_text("Pick", taps(*["Option %d" % n for n in range(12)]))
        assert choice_memory.pick(UID, "2") == "d:1"
        await channel.send_text("How many ayat a day?")
        assert choice_memory.pick(UID, "2") is None  # now a typed answer, not option 2


class TestVoiceNotes:
    """What the recitation checker (Phase 4) needs from WhatsApp: a received
    voice note's bytes, by media id."""

    async def test_media_id_to_bytes(self, channel, graph):
        def media(request):
            graph.requests.append(request)
            if request.url.path.endswith("/MEDIA1"):
                return httpx.Response(200, json={"url": "https://lookaside.example/voice"})
            return httpx.Response(200, content=b"OggS-voice")

        channel.client._transport = httpx.MockTransport(media)
        channel.client._client = None
        url = await channel.client.media_url("MEDIA1")
        assert url == "https://lookaside.example/voice"
        assert await channel.client.download(url) == b"OggS-voice"
        assert graph.requests[-1].headers["Authorization"] == "Bearer TOKEN"
