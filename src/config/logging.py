"""Process-wide logging setup: one stdout handler, so platform logs (Koyeb,
Docker) show everything exactly where the old print() calls put it.

Modules log through `logging.getLogger(__name__)`; this only decides where the
records go and from what level (LOG_LEVEL, default INFO).
"""

import logging
import os
import sys

FORMAT = "%(levelname)s %(name)s: %(message)s"

# Telegram's Bot API puts the bot token in every request URL
# (https://api.telegram.org/bot<TOKEN>/sendMessage), and httpx logs each
# request's URL at INFO. Kept at WARNING so the token never reaches the logs.
QUIET_LOGGERS = ("httpx", "httpcore")


def setup_logging() -> None:
    """Install the stdout handler on the root logger, once. A no-op when the
    root logger is already configured (e.g. by a test runner)."""
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(stream=sys.stdout, level=level, format=FORMAT)
    for name in QUIET_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)
