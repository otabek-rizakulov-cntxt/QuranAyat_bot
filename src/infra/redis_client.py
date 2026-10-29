import logging
import threading
import time

from redis import StrictRedis

from config.settings import get_settings

logger = logging.getLogger(__name__)


class MemoryStore:
    """Minimal in-process stand-in for Redis (get/set with TTL).

    Used when ALLOW_MEMORY_STORE is on (tests, local dev) and REDIS_HOST_URL is
    unset or unreachable, and — degraded — while a configured Redis is down (see
    RedisSingleton). State lives only in this process and is lost on restart.
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


# How long to wait between connection attempts after one fails. The client is
# synchronous and a connect can block for its full 5 s timeout, so retrying on
# every update while Redis is down would stall the event loop for everyone.
RETRY_AFTER_SECONDS = 30


class CacheUnavailable(RuntimeError):
    """Redis is not configured and the in-memory store is not allowed to stand
    in for it (see `Settings.allow_memory_store`)."""


class RedisSingleton:
    """The process's Redis connection.

    Redis holds only what can be rebuilt — the Telegram file_id cache, wizard
    drafts, the pending reciter-search flag — while every durable setting lives
    in Postgres. So the two failure modes are treated differently:

    * **Not configured** (no URL) is a deployment mistake: without
      ALLOW_MEMORY_STORE it raises `CacheUnavailable`, and the health check
      answers 503.
    * **Unreachable** (the URL is set but Redis is down, or its database was
      deleted) is an outage: the bot keeps serving from memory, reports
      "degraded", and retries Redis every RETRY_AFTER_SECONDS, switching back as
      soon as it answers.
    """

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
                        connection, degraded = cls._make_connection()
                    except CacheUnavailable as e:
                        cls.last_error = str(e)
                        cls._failed_at = time.monotonic()
                        raise
                    instance = super().__new__(cls)
                    instance.connection = connection
                    instance.degraded = degraded
                    cls._instance = instance
                    if not degraded:
                        cls.last_error = None
                        cls._failed_at = None
        elif cls._instance.degraded and time.monotonic() - cls._failed_at >= RETRY_AFTER_SECONDS:
            cls._try_to_recover()
        return cls._instance

    @classmethod
    def _try_to_recover(cls) -> None:
        """While degraded, try the real Redis again; swap it in if it answers."""
        with cls._lock:
            instance = cls._instance
            if not instance.degraded or time.monotonic() - cls._failed_at < RETRY_AFTER_SECONDS:
                return  # another caller got here first
            cls._failed_at = time.monotonic()
            try:
                instance.connection = cls._connect(get_settings().redis_url)
            except Exception as e:
                cls.last_error = "unreachable (%s)" % type(e).__name__
                return
            instance.degraded = False
            cls.last_error = None
            cls._failed_at = None
            logger.warning("Redis is reachable again; left the in-memory fallback")

    @staticmethod
    def _connect(redis_url: str):
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

    @classmethod
    def _make_connection(cls):
        """(connection, degraded). Raises CacheUnavailable only when Redis is not
        configured and memory is not allowed."""
        redis_url = get_settings().redis_url
        if not redis_url:
            if not get_settings().allow_memory_store:
                raise CacheUnavailable("not configured")
            logger.warning(
                "REDIS_HOST_URL is not set — falling back to in-memory store. "
                "User state and the media cache will be lost on restart."
            )
            return MemoryStore(), False

        try:
            return cls._connect(redis_url), False
        except Exception as e:
            if get_settings().allow_memory_store:
                logger.warning(
                    "Redis unreachable (%s: %s) — falling back to in-memory store."
                    % (type(e).__name__, e)
                )
                return MemoryStore(), False
            cls.last_error = "unreachable (%s)" % type(e).__name__
            cls._failed_at = time.monotonic()
            logger.error(
                "Redis unreachable (%s) — serving from memory (degraded); the file_id "
                "cache and wizard drafts are temporary until it recovers. Retrying "
                "every %ds." % (type(e).__name__, RETRY_AFTER_SECONDS)
            )
            return MemoryStore(), True


def cache_backend() -> str:
    """Where the cache lives right now, for the health check: "redis", "memory"
    (allowed in dev/tests), "degraded" (Redis is down; serving from memory),
    "unavailable" (not configured) or "pending" (not connected yet)."""
    instance = RedisSingleton._instance
    if instance is not None:
        if instance.degraded:
            return "degraded"
        return "memory" if isinstance(instance.connection, MemoryStore) else "redis"
    return "unavailable" if RedisSingleton.last_error else "pending"
