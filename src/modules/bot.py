from config import Environment
from telegram import Bot as TelegramBot

class Bot():
  _instance = None

  @classmethod
  def get_instance(cls):
    if cls._instance is None:
      token = Environment.get_env("token")
      cls._instance = TelegramBot(token=token)
    return cls._instance