"""Telegram errors the bot treats as expected outcomes, not failures."""

from contextlib import contextmanager

import telegram


@contextmanager
def ignore_not_modified():
    """Swallow Telegram's "message is not modified", re-raise every other BadRequest.

    Re-tapping the view a message already shows edits it into an identical
    message, and Telegram rejects that edit. Nothing went wrong: the message
    already says what the tap asked for.
    """
    try:
        yield
    except telegram.error.BadRequest as err:
        if "not modified" not in str(err).lower():
            raise
