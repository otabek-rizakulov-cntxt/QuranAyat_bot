import asyncio
from .env import Environment

# Sentinel-free two-flag cache: `_pool` is the pool (or None when there isn't
# one), `_pool_resolved` says whether we have already decided. Without the second
# flag a None result would be re-derived — and the warning re-printed — on every
# call.
_pool = None
_pool_resolved = False

_pool_lock = None
_pool_lock_loop = None


def _lock() -> asyncio.Lock:
  """The creation lock, rebuilt whenever the running event loop changes.

  An asyncio.Lock binds to the loop it is first awaited in. Production has a
  single loop for the process lifetime; pytest-asyncio gives each test its own,
  so a module-level lock would be bound to a dead loop by the second test. Same
  pattern as `lib/page_image.py`'s stitch semaphore.
  """
  global _pool_lock, _pool_lock_loop
  loop = asyncio.get_running_loop()
  if _pool_lock is None or _pool_lock_loop is not loop:
    _pool_lock = asyncio.Lock()
    _pool_lock_loop = loop
  return _pool_lock


# Connecting at boot races the database waking up (Neon suspends idle free-tier
# compute; the first connection can take several seconds), so try a few times
# before giving up on this call.
CONNECT_ATTEMPTS = 4
CONNECT_BACKOFF_SECONDS = 1.5


class DatabaseUnavailable(RuntimeError):
  """DATABASE_URL is set but Postgres could not be reached.

  Deliberately *not* a fallback to the in-memory store: doing that silently
  meant every setting a user changed lived only in process memory and vanished
  at the next restart — users saw their language and reciter reset every week or
  two. Failing loudly makes the outage visible, and because nothing is cached on
  failure, the next call tries to connect again.
  """


async def get_pool():
  """Lazily create (once) and return the shared Postgres connection pool.

  Returns **None** only when DATABASE_URL is unset/empty — local dev and tests —
  in which case `get_store()` builds the in-memory repository. When DATABASE_URL
  is set and the server cannot be reached, raises `DatabaseUnavailable` and
  caches nothing, so the next call retries.
  """
  global _pool, _pool_resolved
  if _pool_resolved:
    return _pool

  async with _lock():
    if _pool_resolved:  # re-check: another caller may have won the race
      return _pool

    database_url = Environment.get_env("database_url")
    if not database_url:
      print("WARNING: DATABASE_URL is not set — using the in-memory store. "
            "Every user setting is lost on restart; never run production like this.")
      _pool_resolved = True
      return None

    import asyncpg  # imported lazily so the in-memory path never requires the dependency

    last_error = None
    for attempt in range(1, CONNECT_ATTEMPTS + 1):
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
        _pool_resolved = True
        return _pool
      except Exception as e:
        last_error = e
        print("WARNING: Postgres connect attempt %d/%d failed (%s)"
              % (attempt, CONNECT_ATTEMPTS, type(e).__name__))
        if attempt < CONNECT_ATTEMPTS:
          await asyncio.sleep(CONNECT_BACKOFF_SECONDS * attempt)
    raise DatabaseUnavailable("Postgres unreachable after %d attempts" % CONNECT_ATTEMPTS) from last_error


async def close_pool():
  global _pool, _pool_resolved
  if _pool is not None:
    await _pool.close()
  _pool = None
  _pool_resolved = False


def reset_for_tests():
  """Forget the pool and its creation lock. Called by `lib.store.reset_for_tests`."""
  global _pool, _pool_resolved, _pool_lock, _pool_lock_loop
  _pool = None
  _pool_resolved = False
  _pool_lock = None
  _pool_lock_loop = None
