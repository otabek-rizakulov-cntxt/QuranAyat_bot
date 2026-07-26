import asyncio
import os
import threading
import time
from typing import Optional
from .env import Environment


class FakePostgresPool:
  """Minimal in-process stand-in for an asyncpg.Pool, used when DATABASE_URL is
  unset (mirrors config/redis.py's MemoryStore fallback for Redis).

  Only understands the handful of fixed query shapes `lib.user_settings.UserSettings`
  issues — this is a test/dev double for one small table, not a SQL engine.
  """

  def __init__(self):
    self._rows = {}
    self._lock = threading.Lock()

  async def fetchrow(self, query: str, *args):
    with self._lock:
      if "SELECT" in query:
        user_id = args[0]
        row = self._rows.get(user_id)
        return dict(row) if row is not None else None

      if "INSERT INTO user_settings" in query:
        user_id, ui_lang, translation_lang, reciter = args
        if user_id in self._rows:
          return None  # ON CONFLICT DO NOTHING RETURNING -> no row on conflict
        row = {
          "telegram_user_id": user_id,
          "ui_lang": ui_lang,
          "translation_lang": translation_lang,
          "reciter": reciter,
        }
        self._rows[user_id] = row
        return dict(row)

      raise ValueError("FakePostgresPool.fetchrow: unrecognized query: %r" % query)

  async def execute(self, query: str, *args):
    with self._lock:
      if "UPDATE user_settings" in query:
        user_id, value = args
        row = self._rows.setdefault(user_id, {
          "telegram_user_id": user_id,
          "ui_lang": "en",
          "translation_lang": "en",
          "reciter": "Husary_128kbps",
        })
        if "SET ui_lang" in query:
          row["ui_lang"] = value
        elif "SET translation_lang" in query:
          row["translation_lang"] = value
        elif "SET reciter" in query:
          row["reciter"] = value
        else:
          raise ValueError("FakePostgresPool.execute: unrecognized column in query: %r" % query)
        return "UPDATE 1"

      if "CREATE TABLE" in query:
        return "CREATE TABLE"  # DDL is a no-op against the dict-backed fake

      raise ValueError("FakePostgresPool.execute: unrecognized query: %r" % query)

  def acquire(self):
    return _NullAcquireContext(self)


class _NullAcquireContext:
  """asyncpg's `async with pool.acquire() as conn:` is unused by this app (we only
  ever call pool.fetchrow/execute directly, which asyncpg's real Pool also
  supports), but this keeps the fake's surface closer to the real one."""

  def __init__(self, pool):
    self._pool = pool

  async def __aenter__(self):
    return self._pool

  async def __aexit__(self, *exc):
    return False


_pool = None
_pool_lock = asyncio.Lock()


async def get_pool():
  """Lazily create (once) and return the shared Postgres connection pool.

  Falls back to an in-process FakePostgresPool when DATABASE_URL is unset/empty,
  the same convention config/redis.py uses for REDIS_HOST_URL — keeps tests and
  local dev free of a real Postgres dependency.
  """
  global _pool
  if _pool is not None:
    return _pool

  async with _pool_lock:
    if _pool is not None:  # re-check: another caller may have won the race
      return _pool

    database_url = Environment.get_env("database_url")
    if not database_url:
      print("WARNING: DATABASE_URL is not set — falling back to in-memory settings store. "
            "User settings will be lost on restart.")
      _pool = FakePostgresPool()
      return _pool

    import asyncpg  # imported lazily so the fake-pool path never requires the dependency

    try:
      _pool = await asyncpg.create_pool(
        database_url,
        min_size=1,
        max_size=5,
        command_timeout=10,
        # Neon's pooled (pgbouncer, transaction-mode) endpoint doesn't support
        # prepared statements persisting across pooled connections.
        statement_cache_size=0,
      )
    except Exception as e:
      print("WARNING: Postgres unreachable (%s: %s) — falling back to in-memory settings store."
            % (type(e).__name__, e))
      _pool = FakePostgresPool()
    return _pool


async def close_pool():
  global _pool
  if _pool is not None and hasattr(_pool, "close"):
    await _pool.close()
  _pool = None
