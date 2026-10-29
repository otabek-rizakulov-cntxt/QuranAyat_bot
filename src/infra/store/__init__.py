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

from infra.postgres import get_pool

from ._state import MemoryState
from .groups import GroupStore, InMemoryGroupStore, PostgresGroupStore
from .hifz import HifzStore, InMemoryHifzStore, PostgresHifzStore
from .plans import InMemoryPlanStore, PlanStore, PostgresPlanStore
from .profiles import InMemoryProfileStore, PostgresProfileStore, ProfileStore
from .schedule import InMemoryScheduleStore, PostgresScheduleStore, ScheduleStore
from .sessions import InMemorySessionStore, PostgresSessionStore, SessionStore

__all__ = [
    "Store",
    "InMemoryStore",
    "PostgresStore",
    "get_store",
    "apply_schema",
    "store_backend",
    "reset_for_tests",
    "HifzStore",
    "PlanStore",
    "ProfileStore",
    "ScheduleStore",
    "SessionStore",
    "GroupStore",
]

# src/infra/store/__init__.py -> src/infra/store -> src/lib -> src
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
    """asyncpg-backed store, wrapping a pool created by `infra.postgres.get_pool`."""

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
        with open(SCHEMA_PATH, encoding="utf-8") as fp:
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
    same concern, and the same fix, as `infra/page_image.py`'s stitch semaphore.
    """
    global _store_lock, _store_lock_loop
    loop = asyncio.get_running_loop()
    if _store_lock is None or _store_lock_loop is not loop:
        _store_lock = asyncio.Lock()
        _store_lock_loop = loop
    return _store_lock


async def get_store() -> Store:
    """Lazily build (once) and return the process-wide store.

    Postgres-backed when DATABASE_URL is set; in-memory only when it is unset and
    ALLOW_MEMORY_STORE is on (tests, local dev) — otherwise `get_pool` raises.
    When it is set but the server cannot be reached, `get_pool` raises
    `DatabaseUnavailable` and nothing is cached, so the next call retries — the
    store never silently degrades to memory in a deployment that has a database.
    """
    global _store
    if _store is not None:
        return _store

    async with _lock():
        if _store is not None:  # re-check: another caller may have won the race
            return _store

        # None only when DATABASE_URL is unset and memory is allowed; else it raises.
        pool = await get_pool()
        if pool is None:
            _store = InMemoryStore()
            return _store
        store = PostgresStore(pool)
        # Apply the (idempotent) schema on first connect rather than trusting boot to
        # have done it: if the database was down at boot, this is the first time we
        # can, and new tables must exist before the first query touches them.
        await store.apply_schema()
        _store = store
        return _store


def store_backend() -> str:
    """Where user settings live right now, for the health check: "postgres",
    "memory", "unavailable" (the last connect failed) or "pending" (not built yet)."""
    if _store is not None:
        return "memory" if isinstance(_store, InMemoryStore) else "postgres"
    from infra import postgres

    return "unavailable" if postgres.last_error else "pending"


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

    from infra import postgres

    postgres.reset_for_tests()
