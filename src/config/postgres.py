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


async def get_pool():
  """Lazily create (once) and return the shared Postgres connection pool.

  Returns **None** when DATABASE_URL is unset/empty or the server is unreachable.
  There is no fake pool any more: the fallback for a missing database is the
  in-memory *repository* (`lib.store.InMemoryStore`), which is what `get_store()`
  builds when this returns None.
  """
  global _pool, _pool_resolved
  if _pool_resolved:
    return _pool

  async with _lock():
    if _pool_resolved:  # re-check: another caller may have won the race
      return _pool

    database_url = Environment.get_env("database_url")
    if not database_url:
      print("WARNING: DATABASE_URL is not set — falling back to in-memory settings store. "
            "User settings will be lost on restart.")
      _pool_resolved = True
      return None

    import asyncpg  # imported lazily so the in-memory path never requires the dependency

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
      _pool = None
    _pool_resolved = True
    return _pool


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
