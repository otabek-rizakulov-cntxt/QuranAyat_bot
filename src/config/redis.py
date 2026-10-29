import logging
import threading
import time

from redis import StrictRedis

from .env import Environment  # Importing the base Environment class

logger = logging.getLogger(__name__)


class MemoryStore:
    """Minimal in-process stand-in for Redis (get/set with TTL).

    Used only when ALLOW_MEMORY_STORE is on (tests, local dev) and REDIS_HOST_URL is
    unset or unreachable. State lives only in this process and is lost on restart;
    without the flag a missing Redis raises `CacheUnavailable` instead.
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


# After a failed connect, don't try again for this long. The client is
# synchronous and a connect can block for its full 5 s timeout, so retrying on
# every update while Redis is down would stall the event loop for everyone.
RETRY_AFTER_SECONDS = 30


class CacheUnavailable(RuntimeError):
    """Redis is not configured or could not be reached, and the in-memory store
    is not allowed to stand in for it (see `config.env.memory_store_allowed`)."""


class RedisSingleton(Environment):
    _instance = None
    _lock = threading.Lock()
    # Why the last connect failed, and when (time.monotonic()); None once connected.
    last_error = None
    _failed_at = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    if (
                        cls._failed_at is not None
                        and time.monotonic() - cls._failed_at < RETRY_AFTER_SECONDS
                    ):
                        raise CacheUnavailable("Redis %s; retrying shortly" % cls.last_error)
                    try:
                        connection = cls._make_connection()
                    except CacheUnavailable as e:
                        cls.last_error = str(e)
                        cls._failed_at = time.monotonic()
                        raise
                    instance = super().__new__(cls)
                    instance.connection = connection
                    cls._instance = instance
                    cls.last_error = None
                    cls._failed_at = None
        return cls._instance

    @classmethod
    def _make_connection(cls):
        from .env import memory_store_allowed

        redis_url = cls.get_env("redis")
        if not redis_url:
            if not memory_store_allowed():
                raise CacheUnavailable("not configured")
            logger.warning(
                "REDIS_HOST_URL is not set — falling back to in-memory store. "
                "User state and the media cache will be lost on restart."
            )
            return MemoryStore()

        try:
            connection = StrictRedis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=5,  # fail fast instead of hanging the request
                socket_keepalive=True,  # keep NAT/proxy from silently dropping idle conns
                health_check_interval=30,  # re-validate a pooled conn before reusing it
                retry_on_timeout=True,
            )
            connection.ping()  # verify once up-front rather than on every request
            return connection
        except Exception as e:
            if not memory_store_allowed():
                raise CacheUnavailable("unreachable (%s)" % type(e).__name__) from e
            logger.warning(
                "Redis unreachable (%s: %s) — falling back to in-memory store."
                % (type(e).__name__, e)
            )
            return MemoryStore()


def cache_backend() -> str:
    """Where the cache lives right now, for the health check: "redis", "memory",
    "unavailable" (the last connect failed) or "pending" (not connected yet)."""
    instance = RedisSingleton._instance
    if instance is not None:
        return "memory" if isinstance(instance.connection, MemoryStore) else "redis"
    return "unavailable" if RedisSingleton.last_error else "pending"
