"""bot.errors.ignore_not_modified."""

import pytest
import telegram

from bot.errors import ignore_not_modified


def test_not_modified_is_swallowed():
    with ignore_not_modified():
        raise telegram.error.BadRequest("Message is not modified: specified new message content")


def test_any_other_bad_request_propagates():
    with pytest.raises(telegram.error.BadRequest), ignore_not_modified():
        raise telegram.error.BadRequest("Message to edit not found")


def test_other_errors_propagate():
    with pytest.raises(telegram.error.Forbidden), ignore_not_modified():
        raise telegram.error.Forbidden("bot was blocked by the user")
