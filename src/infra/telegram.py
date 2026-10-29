"""The Telegram Bot API client."""

import telegram

from config.settings import Settings


def create_bot(settings: Settings) -> telegram.Bot:
    """A client for the configured bot. Created once at startup and kept on
    app.state.runtime (app/state.py), so nothing needs a singleton. Constructing
    it does no network I/O."""
    return telegram.Bot(token=settings.token)
