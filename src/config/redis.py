import threading
import time
from redis import StrictRedis
from .env import Environment  # Importing the base Environment class


class MemoryStore:
  """Minimal in-process stand-in for Redis (get/set with TTL).

  Used when REDIS_HOST_URL is unset or the server is unreachable, so the bot keeps
  working instead of failing every update. State lives only in this process, so it is
  lost on restart — configure Redis for real persistence.
  """

  def __init__(self):
    self._data = {}
    self._lock = threading.Lock()

  def get(self, key):
    with self._lock:
      entry = self._data.get(key)
      if entry is None:
        return None
      value, expires_at = entry
      if expires_at is not None and expires_at < time.time():
        self._data.pop(key, None)
        return None
      return value

  def set(self, key, value, ex=None):
    with self._lock:
      self._data[key] = (value, time.time() + ex if ex else None)

  def delete(self, key):
    with self._lock:
      self._data.pop(key, None)


class RedisSingleton(Environment):
  _instance = None
  _lock = threading.Lock()

  def __new__(cls):
    if cls._instance is None:
      with cls._lock:
        if cls._instance is None:
          instance = super().__new__(cls)
          instance.connection = cls._make_connection()
          cls._instance = instance
    return cls._instance

  @classmethod
  def _make_connection(cls):
    redis_url = cls.get_env("redis")
    if not redis_url:
      print("WARNING: REDIS_HOST_URL is not set — falling back to in-memory store. "
            "User state and the media cache will be lost on restart.")
      return MemoryStore()

    try:
      connection = StrictRedis.from_url(
        redis_url,
        decode_responses=True,
        socket_connect_timeout=5,     # fail fast instead of hanging the request
        socket_keepalive=True,        # keep NAT/proxy from silently dropping idle conns
        health_check_interval=30,     # re-validate a pooled conn before reusing it
        retry_on_timeout=True,
      )
      connection.ping()               # verify once up-front rather than on every request
      return connection
    except Exception as e:
      print("WARNING: Redis unreachable (%s: %s) — falling back to in-memory store."
            % (type(e).__name__, e))
      return MemoryStore()
