from telegram import Bot as TelegramBot

from config.settings import get_settings


class Bot:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            token = get_settings().token
            cls._instance = TelegramBot(token=token)
        return cls._instance
