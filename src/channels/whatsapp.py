"""The WhatsApp channel: `Channel` calls onto Meta's WhatsApp Cloud API.

One conversation is one WhatsApp user (`wa_id`). What WhatsApp cannot do, the
channel degrades rather than fails:

  * text is Telegram HTML converted to WhatsApp markers and split at 4,096 chars
    (channels/whatsapp_format.py);
  * `Choices` become reply buttons (≤3, short labels), else one list message
    (≤10 rows), else numbered lines whose numbers `infra/choice_memory.py`
    maps back to `Choice.data`. Link choices are appended as URLs; Mini App
    and inline-share choices have no WhatsApp form and are dropped;
  * nothing is edited in place (`can_edit=False`), so an edit is a new message;
  * media goes by link when the source is a URL, and otherwise is uploaded once
    and its media id cached under the same key Telegram's file_id uses, prefixed
    `wa:` — the same "upload once, replay the id" idea as `send_cached`;
  * audio carries no caption on WhatsApp, so its title and buttons follow it as
    a short text message.

Telegram-only keyword arguments (`reply_markup`, `parse_mode`, …) that a shared
handler passes are ignored here.
"""

import asyncio
import logging
import mimetypes
from typing import Any, List, Optional

import httpx

from channels.base import WHATSAPP, Caps, Choice, Choices, MediaSource
from channels.whatsapp_format import split, to_whatsapp
from infra import choice_memory, media_cache

logger = logging.getLogger(__name__)

CAPS = Caps(max_buttons=3, list_rows=10, can_edit=False, inline_mode=False, web_app=False)

GRAPH_URL = "https://graph.facebook.com"
DEFAULT_GRAPH_VERSION = "v23.0"

BUTTON_TITLE_MAX = 20  # reply-button title
ROW_TITLE_MAX = 24  # list-row title
ROW_DESCRIPTION_MAX = 72  # list-row description
INTERACTIVE_BODY_MAX = 1024  # body of a button or list message
CAPTION_MAX = 1024  # image caption
CHOICES_BODY = "👇"  # body for buttons that follow media or a split text
LIST_BUTTON = "☰"  # the button that opens a list message

# Error 131047: more than 24 hours since the user last wrote — only a template
# may be sent. https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes
WINDOW_CLOSED_CODE = 131047
RETRY_STATUSES = {429, 500, 502, 503, 504}
RETRY_DELAYS = (0.5, 1.5, 4.0)

_sleep = asyncio.sleep  # patched in tests


class WhatsAppError(RuntimeError):
    def __init__(self, status: int, code: Optional[int], message: str):
        super().__init__("WhatsApp API %s (code %s): %s" % (status, code, message))
        self.status = status
        self.code = code


class WindowClosed(WhatsAppError):
    """The 24-hour service window is closed: send an approved template instead."""


class GraphClient:
    """The few Graph API calls the channel needs, over one shared httpx client."""

    def __init__(
        self,
        phone_number_id: str,
        access_token: str,
        version: str = DEFAULT_GRAPH_VERSION,
        transport: Optional[httpx.AsyncBaseTransport] = None,
    ):
        self.phone_number_id = phone_number_id
        self._token = access_token
        self._version = version
        self._transport = transport
        self._client: Optional[httpx.AsyncClient] = None

    @classmethod
    def from_settings(cls, settings) -> "GraphClient":
        return cls(settings.whatsapp_phone_number_id, settings.whatsapp_access_token)

    def _http(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url="%s/%s/" % (GRAPH_URL, self._version),
                headers={"Authorization": "Bearer " + self._token},
                timeout=30,
                transport=self._transport,
            )
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        """One API call, retried with backoff on rate limits and server errors."""
        for attempt, delay in enumerate((*RETRY_DELAYS, None)):
            response = await self._http().request(method, path, **kwargs)
            if response.status_code < 400:
                return response.json() if response.content else {}
            if response.status_code in RETRY_STATUSES and delay is not None:
                logger.warning(
                    "WhatsApp %s %s: HTTP %d, retry %d", method, path, response.status_code, attempt
                )
                await _sleep(delay)
                continue
            raise _error(response)
        raise AssertionError("unreachable")

    async def send(self, to: str, message: dict) -> Optional[str]:
        """POST one message to `to`; returns its WhatsApp message id."""
        body = {"messaging_product": "whatsapp", "recipient_type": "individual", "to": to}
        body.update(message)
        result = await self._request("POST", "%s/messages" % self.phone_number_id, json=body)
        messages = result.get("messages") or [{}]
        return messages[0].get("id")

    async def upload(self, content: bytes, filename: str, mime: str) -> str:
        """Upload media for later sends; returns the media id."""
        result = await self._request(
            "POST",
            "%s/media" % self.phone_number_id,
            data={"messaging_product": "whatsapp", "type": mime},
            files={"file": (filename, content, mime)},
        )
        return result["id"]

    async def media_url(self, media_id: str) -> str:
        """The short-lived download URL of a received media id (voice notes)."""
        return (await self._request("GET", media_id))["url"]

    async def download(self, url: str) -> bytes:
        response = await self._http().get(url)
        response.raise_for_status()
        return response.content


def _error(response: httpx.Response) -> WhatsAppError:
    try:
        err = response.json().get("error", {})
    except ValueError:
        err = {}
    code = err.get("code")
    message = err.get("message") or response.text[:200]
    cls = WindowClosed if code == WINDOW_CLOSED_CODE else WhatsAppError
    return cls(response.status_code, code, message)


def _clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


async def _resolve(source: MediaSource) -> Any:
    return await source() if callable(source) else source


def _bytes_and_name(media, default_name: str):
    """(bytes, filename) from bytes or a file-like object such as a BytesIO."""
    if isinstance(media, (bytes, bytearray)):
        return bytes(media), default_name
    if hasattr(media, "getvalue"):
        return media.getvalue(), getattr(media, "name", None) or default_name
    return media.read(), getattr(media, "name", None) or default_name


class WhatsAppChannel:
    """One WhatsApp user, addressed by `wa_id`; `chat_id` is our user id for them."""

    platform = WHATSAPP
    caps = CAPS

    def __init__(self, client: GraphClient, wa_id: str, chat_id: int):
        self.client = client
        self.wa_id = wa_id
        self.chat_id = chat_id

    def __repr__(self) -> str:
        return "WhatsAppChannel(chat_id=%r)" % (self.chat_id,)

    # --- text and choices ---------------------------------------------------------

    async def send_text(
        self, text: str, choices: Optional[Choices] = None, *, html: bool = False, **opts
    ) -> Any:
        body = to_whatsapp(text) if html else text
        taps, links = _split_choices(choices)
        if links:
            body = body.rstrip() + "\n\n" + "\n".join("%s: %s" % (c.label, c.url) for c in links)
        chunks = split(body)
        if not taps:
            last = None
            for chunk in chunks:
                last = await self._send(
                    {"type": "text", "text": {"body": chunk, "preview_url": bool(links)}}
                )
            return last
        # The buttons ride on the last chunk when it fits an interactive body.
        *head, tail = chunks
        for chunk in head:
            await self._send({"type": "text", "text": {"body": chunk}})
        if len(tail) > INTERACTIVE_BODY_MAX:
            await self._send({"type": "text", "text": {"body": tail}})
            tail = CHOICES_BODY
        return await self._send_choices(tail or CHOICES_BODY, taps)

    async def _send_choices(self, body: str, taps: List[Choice]) -> Any:
        if len(taps) <= CAPS.max_buttons and all(len(c.label) <= BUTTON_TITLE_MAX for c in taps):
            buttons = [{"type": "reply", "reply": {"id": c.data, "title": c.label}} for c in taps]
            message = {"type": "button", "body": {"text": body}, "action": {"buttons": buttons}}
            return await self._send({"type": "interactive", "interactive": message})
        if len(taps) <= CAPS.list_rows:
            rows = []
            for c in taps:
                row = {"id": c.data, "title": _clip(c.label, ROW_TITLE_MAX)}
                if len(c.label) > ROW_TITLE_MAX:
                    row["description"] = _clip(c.label, ROW_DESCRIPTION_MAX)
                rows.append(row)
            message = {
                "type": "list",
                "body": {"text": body},
                "action": {"button": LIST_BUTTON, "sections": [{"title": " ", "rows": rows}]},
            }
            return await self._send({"type": "interactive", "interactive": message})
        # Too many for a list: numbered lines, answered by typing the number.
        choice_memory.remember(self.chat_id, [c.data for c in taps])
        lines = "\n".join("%d. %s" % (n, c.label) for n, c in enumerate(taps, 1))
        text = body + "\n\n" + lines if body != CHOICES_BODY else lines
        last = None
        for chunk in split(text):
            last = await self._send({"type": "text", "text": {"body": chunk}})
        return last

    async def edit_text(
        self,
        message_id: Any,
        text: str,
        choices: Optional[Choices] = None,
        *,
        html: bool = False,
        **opts,
    ) -> bool:
        """WhatsApp cannot edit: the new version goes out as a new message."""
        await self.send_text(text, choices, html=html)
        return False

    async def edit_choices(self, message_id: Any, choices: Optional[Choices]) -> bool:
        return False  # nothing to swap in place; Ctx.edit_choices resends instead

    # --- media ------------------------------------------------------------------------

    async def _media_ref(self, kind: str, source: MediaSource, cache_key: Optional[str]) -> dict:
        """{"link": url} or {"id": media_id}, uploading (once per cache key) if needed."""
        if isinstance(source, str) and source.startswith(("http://", "https://")):
            return {"link": source}
        key = "wa:" + cache_key if cache_key else None
        if key is not None:
            cached = media_cache.get(key)
            if cached:
                return {"id": cached}
        media = await _resolve(source)
        if isinstance(media, str) and media.startswith(("http://", "https://")):
            return {"link": media}
        content, name = _bytes_and_name(media, "quran.mp3" if kind == "audio" else "quran.jpg")
        mime = mimetypes.guess_type(name)[0] or ("audio/mpeg" if kind == "audio" else "image/jpeg")
        media_id = await self.client.upload(content, name, mime)
        if key is not None:
            media_cache.save(key, media_id)
        return {"id": media_id}

    async def send_image(
        self,
        source: MediaSource,
        *,
        caption: Optional[str] = None,
        choices: Optional[Choices] = None,
        cache_key: Optional[str] = None,
        **opts,
    ) -> Any:
        image = await self._media_ref("image", source, cache_key)
        if caption:
            image["caption"] = _clip(caption, CAPTION_MAX)
        sent = await self._send({"type": "image", "image": image})
        if _split_choices(choices) != ([], []):
            await self.send_text(CHOICES_BODY, choices)
        return sent

    async def send_audio(
        self,
        source: MediaSource,
        *,
        title: Optional[str] = None,
        performer: Optional[str] = None,
        caption: Optional[str] = None,
        choices: Optional[Choices] = None,
        cache_key: Optional[str] = None,
        **opts,
    ) -> Any:
        audio = await self._media_ref("audio", source, cache_key)
        sent = await self._send({"type": "audio", "audio": audio})
        label = " · ".join(p for p in (caption or title, performer) if p)
        if label or _split_choices(choices) != ([], []):
            await self.send_text(label or CHOICES_BODY, choices)
        return sent

    # --- the rest -----------------------------------------------------------------------

    async def answer(
        self, callback_id: Optional[str], text: Optional[str] = None, alert: bool = False
    ) -> None:
        """WhatsApp has no tap acknowledgement or toast: an answer's text is a message."""
        if text:
            await self.send_text(text)

    async def typing(self, kind: str = "text") -> None:
        return None  # no chat action without a message id to attach it to

    async def send_template(self, name: str, lang: str, params: List[str]) -> Any:
        template = {"name": name, "language": {"code": lang}}
        if params:
            template["components"] = [
                {"type": "body", "parameters": [{"type": "text", "text": p} for p in params]}
            ]
        return await self._send({"type": "template", "template": template})

    async def _send(self, message: dict) -> Optional[str]:
        return await self.client.send(self.wa_id, message)


def _split_choices(choices: Optional[Choices]):
    """(tappable choices, link choices), flattened; other kinds are dropped."""
    taps, links = [], []
    for row in choices or []:
        for choice in row:
            if choice.data is not None:
                taps.append(choice)
            elif choice.url is not None:
                links.append(choice)
    return taps, links
