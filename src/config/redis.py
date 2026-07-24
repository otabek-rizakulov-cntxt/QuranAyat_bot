import threading
from redis import StrictRedis
from .env import Environment  # Importing the base Environment class

class RedisSingleton(Environment):
  _instance = None
  _lock = threading.Lock()

  def __new__(cls):
    if cls._instance is None:
      with cls._lock:
        if cls._instance is None:
          instance = super().__new__(cls)
          redis_url = cls.get_env("redis")
          instance.connection = StrictRedis.from_url(
            redis_url,
            decode_responses=True,
            socket_connect_timeout=5,     # fail fast instead of hanging the request
            socket_keepalive=True,        # keep NAT/proxy from silently dropping idle conns
            health_check_interval=30,     # re-validate a pooled conn before reusing it
            retry_on_timeout=True,
          )
          cls._instance = instance
    return cls._instance
