# The repository layer: the only place in this codebase that contains SQL.
#
# Two implementations sit behind one interface — asyncpg-backed when DATABASE_URL
# is set, in-memory otherwise. That is the same dev/test convenience the old
# FakePostgresPool provided, without the pretence of being a SQL engine: it fakes
# the *repository*, which has a dozen well-defined methods, instead of faking
# query strings, which are unbounded.
#
# `tests/test_store_contract.py` runs one suite against both implementations so
# they cannot silently drift apart.

import asyncio
import os

from config.postgres import get_pool

from ._state import MemoryState
from .hifz import HifzStore, InMemoryHifzStore, PostgresHifzStore
from .plans import InMemoryPlanStore, PlanStore, PostgresPlanStore
from .profiles import InMemoryProfileStore, PostgresProfileStore, ProfileStore
from .schedule import InMemoryScheduleStore, PostgresScheduleStore, ScheduleStore
from .sessions import InMemorySessionStore, PostgresSessionStore, SessionStore
from .groups import GroupStore, InMemoryGroupStore, PostgresGroupStore

__all__ = [
  "Store", "InMemoryStore", "PostgresStore",
  "get_store", "apply_schema", "reset_for_tests",
  "HifzStore", "PlanStore", "ProfileStore", "ScheduleStore", "SessionStore",
  "GroupStore",
]

# src/lib/store/__init__.py -> src/lib/store -> src/lib -> src
_SRC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHEMA_PATH = os.path.join(_SRC_DIR, "common", "schema.sql")


class Store:
  """Container for the five aggregate repositories.

  Callers reach storage through `store.profiles`, `store.hifz`, `store.plans`,
  `store.sessions` and `store.schedule` — never through a pool, a connection or a
  query string.
  """

  profiles: ProfileStore
  hifz: HifzStore
  plans: PlanStore
  sessions: SessionStore
  schedule: ScheduleStore
  groups: GroupStore

  async def apply_schema(self) -> None:
    """Create any missing tables and indexes. Idempotent."""
    raise NotImplementedError

  async def close(self) -> None:
    """Release whatever the implementation holds open."""


class InMemoryStore(Store):
  """Process-local store. Everything is lost on restart, which is why the boot
  warning says so."""

  def __init__(self, state: MemoryState = None):
    self.state = state if state is not None else MemoryState()
    self.profiles = InMemoryProfileStore(self.state)
    self.hifz = InMemoryHifzStore(self.state)
    self.plans = InMemoryPlanStore(self.state)
    self.sessions = InMemorySessionStore(self.state)
    self.schedule = InMemoryScheduleStore(self.state)
    self.groups = InMemoryGroupStore(self.state)

  async def apply_schema(self) -> None:
    """No-op: there is no schema to apply to a dict."""

  def clear(self) -> None:
    """Drop every row (tests only)."""
    self.state.clear()


class PostgresStore(Store):
  """asyncpg-backed store, wrapping a pool created by `config.postgres.get_pool`."""

  def __init__(self, pool):
    self.pool = pool
    self.profiles = PostgresProfileStore(pool)
    self.hifz = PostgresHifzStore(pool)
    self.plans = PostgresPlanStore(pool)
    self.sessions = PostgresSessionStore(pool)
    self.schedule = PostgresScheduleStore(pool)
    self.groups = PostgresGroupStore(pool)

  async def apply_schema(self) -> None:
    """Apply `src/common/schema.sql` in one multi-statement execute.

    The whole file goes in a single call, so it has to stay valid as one script —
    every statement is `IF NOT EXISTS`, and there is no migration framework by
    design at this scale.
    """
    with open(SCHEMA_PATH, "r", encoding="utf-8") as fp:
      await self.pool.execute(fp.read())

  async def close(self) -> None:
    await self.pool.close()


_store = None
_store_lock = None
_store_lock_loop = None


def _lock() -> asyncio.Lock:
  """The creation lock, rebuilt whenever the running event loop changes.

  An asyncio.Lock binds to the loop it is first awaited in. Production has one
  loop for the process lifetime, but pytest-asyncio gives every test its own —
  same concern, and the same fix, as `lib/page_image.py`'s stitch semaphore.
  """
  global _store_lock, _store_lock_loop
  loop = asyncio.get_running_loop()
  if _store_lock is None or _store_lock_loop is not loop:
    _store_lock = asyncio.Lock()
    _store_lock_loop = loop
  return _store_lock


async def get_store() -> Store:
  """Lazily build (once) and return the process-wide store.

  Postgres-backed when DATABASE_URL is set and reachable; in-memory when it is
  unset, or when the pool could not be created (`config.postgres.get_pool`
  returns None in both cases, having printed the warning).
  """
  global _store
  if _store is not None:
    return _store

  async with _lock():
    if _store is not None:              # re-check: another caller may have won the race
      return _store

    # get_pool() answers None — having printed the warning — both when
    # DATABASE_URL is unset and when the server could not be reached.
    pool = await get_pool()
    _store = PostgresStore(pool) if pool is not None else InMemoryStore()
    return _store


async def apply_schema() -> None:
  """Apply the schema through the active store. A no-op on the in-memory one."""
  store = await get_store()
  await store.apply_schema()


def reset_for_tests() -> None:
  """Drop the singleton and every byte of in-memory state.

  Called from conftest's autouse fixture between tests, so nothing leaks from one
  test into the next and the creation lock is never reused across event loops.
  """
  global _store, _store_lock, _store_lock_loop
  if isinstance(_store, InMemoryStore):
    _store.clear()
  _store = None
  _store_lock = None
  _store_lock_loop = None

  from config import postgres
  postgres.reset_for_tests()
