from telegram import Bot as TelegramBot

from config import Environment


class Bot:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            token = Environment.get_env("token")
            cls._instance = TelegramBot(token=token)
        return cls._instance
