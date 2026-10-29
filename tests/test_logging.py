"""Logging setup (src/config/logging.py)."""

import logging

from config.logging import QUIET_LOGGERS, setup_logging


def test_http_client_request_urls_are_never_logged():
    # Every Bot API URL carries the bot token; httpx logs request URLs at INFO.
    setup_logging()
    for name in QUIET_LOGGERS:
        assert not logging.getLogger(name).isEnabledFor(logging.INFO), name


def test_the_http_client_loggers_are_the_ones_python_telegram_bot_uses():
    import telegram.request._httpxrequest as ptb_request

    assert "httpx" in QUIET_LOGGERS
    assert ptb_request.httpx.__name__ == "httpx"
