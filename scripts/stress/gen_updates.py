"""Synthetic Telegram Update payloads for the local capacity test.

Same JSON shape `tests/test_handle_update.py` builds by hand for `handle_update`
unit tests — reused here as plain dicts POSTed over HTTP to the real webhook
route (`main.py`'s `telegram_webhook` does the `Update.de_json` parsing itself).

The mix is Phase-1 DM personal-feature traffic only (registration-free), no
group flows — matching the "dozens to low hundreds of users" scale this report
is scoped to. Weighted by how heavy each operation actually is: plain commands
are near-free, `/streak` renders a PNG with Pillow, and a bare ayah reference
drives the CDN fetch-and-stitch path `send_quran` uses.
"""

import itertools
import random

_update_id = itertools.count(1)

# (weight, text) — weights are relative, not percentages.
_TRAFFIC_MIX = [
    (30, "/start"),
    (15, "/progress"),
    (15, "/streak"),
    (15, "67:5"),          # single ayah -> send_quran: image + audio + translation
    (10, "67:1-5"),        # range -> combined stitched audio
    (10, "/check 67"),
    (5, "/leaderboard"),
]
_WEIGHTS = [w for w, _ in _TRAFFIC_MIX]
_TEXTS = [text for _, text in _TRAFFIC_MIX]


def random_text() -> str:
    return random.choices(_TEXTS, weights=_WEIGHTS, k=1)[0]


def message_update(chat_id: int, text: str | None = None) -> dict:
    """One synthetic user (`chat_id`) sending one message."""
    text = text if text is not None else random_text()
    return {
        "update_id": next(_update_id),
        "message": {
            "message_id": 1,
            "date": 1700000000,
            "chat": {"id": chat_id, "type": "private"},
            "from": {"id": chat_id, "is_bot": False, "first_name": "StressUser %d" % chat_id,
                     "language_code": "en"},
            "text": text,
        },
    }


def batch(n: int, first_chat_id: int = 900_000_000) -> list:
    """`n` synthetic updates, one simulated user each, sharing no state."""
    return [message_update(first_chat_id + i) for i in range(n)]
