"""Which store the bot runs on, and that it never silently runs on memory when a
database is configured.

Regression: when DATABASE_URL was set but Postgres was unreachable at the
moment of the first connect (Neon waking from suspend, a network blip at boot),
`get_pool` answered None and `get_store` built the in-memory store — for the
rest of that process's life. Every language, reciter and translation a user
chose was written to memory and lost at the next restart, which users saw as
their settings resetting every week or two.
"""

import pytest

from config import postgres
from lib import store as store_module


class _FakePool:
    def __init__(self):
        self.executed = []

    async def execute(self, query, *args):
        self.executed.append(query)


@pytest.fixture
def fast_retries(monkeypatch):
    monkeypatch.setattr(postgres, "CONNECT_BACKOFF_SECONDS", 0)


@pytest.fixture
def database_url(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://db.invalid/quranayat")


def _failing_create_pool(calls):
    async def create_pool(*args, **kwargs):
        calls.append(1)
        raise OSError("connection refused")
    return create_pool


class TestUnreachableDatabase:
    async def test_raises_instead_of_falling_back_to_memory(self, monkeypatch, database_url, fast_retries):
        import asyncpg
        calls = []
        monkeypatch.setattr(asyncpg, "create_pool", _failing_create_pool(calls))
        with pytest.raises(postgres.DatabaseUnavailable):
            await store_module.get_store()
        assert store_module._store is None
        assert len(calls) == postgres.CONNECT_ATTEMPTS

    async def test_the_next_call_retries_and_uses_postgres(self, monkeypatch, database_url, fast_retries):
        import asyncpg
        calls = []
        monkeypatch.setattr(asyncpg, "create_pool", _failing_create_pool(calls))
        with pytest.raises(postgres.DatabaseUnavailable):
            await store_module.get_store()

        pool = _FakePool()

        async def create_pool(*args, **kwargs):
            return pool
        monkeypatch.setattr(asyncpg, "create_pool", create_pool)
        store = await store_module.get_store()
        assert isinstance(store, store_module.PostgresStore)

    async def test_a_slow_wakeup_succeeds_within_the_attempts(self, monkeypatch, database_url, fast_retries):
        import asyncpg
        pool = _FakePool()
        attempts = []

        async def create_pool(*args, **kwargs):
            attempts.append(1)
            if len(attempts) < postgres.CONNECT_ATTEMPTS:
                raise OSError("still waking up")
            return pool
        monkeypatch.setattr(asyncpg, "create_pool", create_pool)
        store = await store_module.get_store()
        assert isinstance(store, store_module.PostgresStore)

    async def test_first_connect_applies_the_schema(self, monkeypatch, database_url):
        # Boot may have failed to apply it while the database was down; the
        # reader_position table must exist before the first query touches it.
        import asyncpg
        pool = _FakePool()

        async def create_pool(*args, **kwargs):
            return pool
        monkeypatch.setattr(asyncpg, "create_pool", create_pool)
        await store_module.get_store()
        assert any("reader_position" in q for q in pool.executed)


class TestHealthReportsTheStore:
    async def test_memory_store_is_visible_on_the_health_endpoint(self):
        import main
        await store_module.get_store()
        assert await main.health() == {"status": "ok", "store": "memory"}
