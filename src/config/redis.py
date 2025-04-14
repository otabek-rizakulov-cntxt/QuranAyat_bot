import threading
from redis import StrictRedis
from .env import Environment  # Importing the base Environment class

class RedisSingleton(Environment):

  def __init__(self):
    if not hasattr(self, "connection"):  # Prevent re-initialization
      redis_url = self.get_env("redis")  # Directly accessing get_env()
      self.connection = StrictRedis.from_url(redis_url, decode_responses=True)
