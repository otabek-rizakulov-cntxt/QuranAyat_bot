"""Telegram errors the bot treats as expected outcomes, not failures.

The handling itself is Telegram transport and lives in channels/telegram.py;
it is re-exported here for the handlers that still edit through the bot.
"""

from channels.telegram import ignore_not_modified

__all__ = ["ignore_not_modified"]
