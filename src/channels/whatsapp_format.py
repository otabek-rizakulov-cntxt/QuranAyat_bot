"""Telegram HTML → WhatsApp text formatting (docs/MULTI_PLATFORM_PLAN.md §2).

Every message builder and locale string emits Telegram HTML, and stays that way:
one source format, so Telegram output is byte-identical. WhatsApp has no HTML,
only inline markers, so its channel runs each text through `to_whatsapp`:

    <b>  → *bold*        <i>  → _italic_     <s>   → ~strike~
    <code> → `code`      <pre> → ```block``` <a href> → text (url)
    <blockquote> → "> " lines                <br> → newline

Tags WhatsApp cannot show (<u>, <tg-spoiler>, anything unknown) keep their text
and lose the tag. Entities (`&amp;`, `&lt;` …) are decoded.

WhatsApp only applies a marker that hugs its text — "*bold*", never "* bold *" —
so whitespace at the edge of a formatted run is moved outside the marker.
"""

from html.parser import HTMLParser
from typing import List

MAX_TEXT = 4096  # WhatsApp's limit on a text message body, in characters

_MARKERS = {
    "b": "*",
    "strong": "*",
    "i": "_",
    "em": "_",
    "s": "~",
    "strike": "~",
    "del": "~",
    "code": "`",
    "pre": "```",
}


class _Converter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        # Each open element is a frame collecting its own text, so a marker can be
        # wrapped around exactly that run once the element closes.
        self.frames: List[list] = [["", None, None]]  # [text, tag, href]

    def handle_starttag(self, tag, attrs):
        if tag == "br":
            self.handle_data("\n")
            return
        self.frames.append(["", tag, dict(attrs).get("href") if tag == "a" else None])

    def handle_startendtag(self, tag, attrs):
        if tag == "br":
            self.handle_data("\n")

    def handle_endtag(self, tag):
        # Close back to the matching open tag; a stray end tag is ignored.
        if not any(frame[1] == tag for frame in self.frames[1:]):
            return
        while True:
            text, open_tag, href = self.frames.pop()
            self.frames[-1][0] += _render(open_tag, text, href)
            if open_tag == tag:
                return

    def handle_data(self, data):
        self.frames[-1][0] += data

    def result(self) -> str:
        while len(self.frames) > 1:  # unclosed tags: render what they hold
            text, tag, href = self.frames.pop()
            self.frames[-1][0] += _render(tag, text, href)
        return self.frames[0][0]


def _wrap(text: str, marker: str) -> str:
    """`marker` around `text`, with edge whitespace moved outside it."""
    core = text.strip()
    if not core:
        return text
    lead = text[: len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()) :]
    return lead + marker + core + marker + trail


def _render(tag, text: str, href) -> str:
    if tag in _MARKERS:
        marker = _MARKERS[tag]
        if tag == "pre":
            return "```" + text.strip("\n") + "```" if text.strip() else text
        return _wrap(text, marker)
    if tag == "a":
        if not href or href == text.strip():
            return text
        return "%s (%s)" % (text, href) if text.strip() else href
    if tag == "blockquote":
        return "\n".join("> " + line for line in text.strip("\n").split("\n"))
    return text  # <u>, <tg-spoiler>, <span>, unknown: keep the words, drop the tag


def to_whatsapp(html: str) -> str:
    """Telegram HTML as WhatsApp-formatted plain text."""
    converter = _Converter()
    converter.feed(html)
    converter.close()
    return converter.result()


def split(text: str, limit: int = MAX_TEXT) -> List[str]:
    """`text` in chunks of at most `limit` characters, for WhatsApp's body limit.

    Breaks at the last paragraph break that fits, else the last line break, else
    the last space, and only cuts mid-word when a single word is longer than
    `limit`. Separators at a break are dropped; nothing else is.
    """
    chunks = []
    while len(text) > limit:
        window = text[: limit + 1]
        for sep in ("\n\n", "\n", " "):
            cut = window.rfind(sep, 1, limit + 1)
            if cut > 0:
                chunks.append(text[:cut])
                text = text[cut + len(sep) :]
                break
        else:
            chunks.append(text[:limit])
            text = text[limit:]
    if text or not chunks:
        chunks.append(text)
    return chunks
