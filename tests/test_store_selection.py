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

import app.routes.health as health_route
from infra import postgres
from infra import store as store_module


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
    async def test_raises_instead_of_falling_back_to_memory(
        self, monkeypatch, database_url, fast_retries
    ):
        import asyncpg

        calls = []
        monkeypatch.setattr(asyncpg, "create_pool", _failing_create_pool(calls))
        with pytest.raises(postgres.DatabaseUnavailable):
            await store_module.get_store()
        assert store_module._store is None
        assert len(calls) == postgres.CONNECT_ATTEMPTS

    async def test_the_next_call_retries_and_uses_postgres(
        self, monkeypatch, database_url, fast_retries
    ):
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

    async def test_a_slow_wakeup_succeeds_within_the_attempts(
        self, monkeypatch, database_url, fast_retries
    ):
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


@pytest.fixture
def strict(monkeypatch):
    """Production defaults: the in-memory stores are not allowed."""
    monkeypatch.delenv("ALLOW_MEMORY_STORE", raising=False)


@pytest.fixture
def fresh_redis(monkeypatch):
    """A RedisSingleton that has never connected; restored after the test."""
    from infra.redis_client import RedisSingleton

    monkeypatch.setattr(RedisSingleton, "_instance", None)
    monkeypatch.setattr(RedisSingleton, "last_error", None)
    monkeypatch.setattr(RedisSingleton, "_failed_at", None)
    return RedisSingleton


class TestStrictByDefault:
    """Regression: the production database URL lived in a platform secret the
    service never referenced, so it read as unset and the bot ran on memory —
    every setting lost at each restart, with nothing failing visibly."""

    async def test_an_unset_database_url_raises_without_the_flag(self, strict):
        with pytest.raises(postgres.DatabaseUnavailable):
            await store_module.get_store()
        assert store_module._store is None
        assert store_module.store_backend() == "unavailable"

    async def test_an_unset_database_url_uses_memory_with_the_flag(self):
        store = await store_module.get_store()
        assert isinstance(store, store_module.InMemoryStore)
        assert store_module.store_backend() == "memory"

    def test_an_unset_redis_url_raises_without_the_flag(self, strict, fresh_redis, monkeypatch):
        from infra.redis_client import CacheUnavailable, cache_backend

        monkeypatch.setenv("REDIS_HOST_URL", "")
        with pytest.raises(CacheUnavailable):
            fresh_redis()
        assert cache_backend() == "unavailable"

    def test_an_unreachable_redis_degrades_instead_of_failing(
        self, strict, fresh_redis, monkeypatch
    ):
        # Production incident: the Upstash database behind the configured URL was
        # deleted, its hostname stopped resolving, and every update and Mini App
        # login failed — though nothing durable lives in Redis.
        from infra import redis_client as redis_module

        monkeypatch.setenv("REDIS_HOST_URL", "redis://cache.invalid:6379")
        monkeypatch.setattr(
            redis_module.StrictRedis, "from_url", classmethod(lambda cls, *a, **k: _Unreachable())
        )
        instance = fresh_redis()
        assert isinstance(instance.connection, redis_module.MemoryStore)
        assert redis_module.cache_backend() == "degraded"
        instance.connection.set("k", "v")  # usable while degraded
        assert instance.connection.get("k") == "v"

    async def test_a_degraded_cache_keeps_the_health_check_green(
        self, strict, fresh_redis, monkeypatch
    ):
        from fastapi import Response

        from infra import redis_client as redis_module

        monkeypatch.setenv("REDIS_HOST_URL", "redis://cache.invalid:6379")
        monkeypatch.setattr(
            redis_module.StrictRedis, "from_url", classmethod(lambda cls, *a, **k: _Unreachable())
        )
        fresh_redis()
        response = Response()
        body = await health_route.health(response)
        assert body["cache"] == "degraded" and body["status"] == "ok"
        assert response.status_code == 200

    def test_a_degraded_cache_recovers_when_redis_returns(self, strict, fresh_redis, monkeypatch):
        from infra import redis_client as redis_module

        monkeypatch.setenv("REDIS_HOST_URL", "redis://cache.invalid:6379")
        attempts = []
        healthy = _Reachable()

        def from_url(cls, *a, **k):
            attempts.append(1)
            return healthy if len(attempts) >= 3 else _Unreachable()

        monkeypatch.setattr(redis_module.StrictRedis, "from_url", classmethod(from_url))
        fresh_redis()  # attempt 1: down -> degraded
        fresh_redis()
        fresh_redis()  # inside the cooldown: no new attempt
        assert len(attempts) == 1

        expire = lambda: monkeypatch.setattr(  # noqa: E731
            fresh_redis, "_failed_at", fresh_redis._failed_at - redis_module.RETRY_AFTER_SECONDS - 1
        )
        expire()
        fresh_redis()  # attempt 2: still down
        assert redis_module.cache_backend() == "degraded" and len(attempts) == 2
        expire()
        instance = fresh_redis()  # attempt 3: back
        assert instance.connection is healthy
        assert redis_module.cache_backend() == "redis"

    def test_an_unreachable_redis_falls_back_to_memory_with_the_flag(
        self, fresh_redis, monkeypatch
    ):
        from infra import redis_client as redis_module

        monkeypatch.setenv("REDIS_HOST_URL", "redis://cache.invalid:6379")
        monkeypatch.setattr(
            redis_module.StrictRedis, "from_url", classmethod(lambda cls, *a, **k: _Unreachable())
        )
        assert isinstance(fresh_redis().connection, redis_module.MemoryStore)
        assert redis_module.cache_backend() == "memory"

    def test_a_failed_redis_connect_is_not_retried_on_every_update(
        self, strict, fresh_redis, monkeypatch
    ):
        # The client is synchronous: retrying on every update while Redis is down
        # would block the event loop for the connect timeout each time.
        from infra import redis_client as redis_module

        attempts = []
        real = redis_module.RedisSingleton._make_connection.__func__

        def counting(cls):
            attempts.append(1)
            return real(cls)

        monkeypatch.setenv("REDIS_HOST_URL", "")
        monkeypatch.setattr(redis_module.RedisSingleton, "_make_connection", classmethod(counting))
        for _ in range(3):
            with pytest.raises(redis_module.CacheUnavailable):
                fresh_redis()
        assert len(attempts) == 1

        # Once the cooldown has passed it tries again — and recovers.
        monkeypatch.setattr(
            fresh_redis, "_failed_at", fresh_redis._failed_at - redis_module.RETRY_AFTER_SECONDS - 1
        )
        monkeypatch.setenv("ALLOW_MEMORY_STORE", "1")
        assert isinstance(fresh_redis().connection, redis_module.MemoryStore)
        assert len(attempts) == 2
        assert redis_module.cache_backend() == "memory"


class _Unreachable:
    def ping(self):
        raise ConnectionError("connection refused")


class _Reachable:
    def ping(self):
        return True


class TestHealthReportsTheStores:
    async def test_memory_stores_are_visible_on_the_health_endpoint(self):
        from fastapi import Response

        await store_module.get_store()
        response = Response()
        assert await health_route.health(response) == {
            "status": "ok",
            "store": "memory",
            "cache": "memory",
        }
        assert response.status_code == 200

    async def test_a_store_that_is_not_built_yet_is_pending_not_down(self, fresh_redis):
        from fastapi import Response

        response = Response()
        body = await health_route.health(response)
        assert (body["store"], body["cache"]) == ("pending", "pending")
        assert response.status_code == 200

    async def test_a_missing_database_fails_the_health_check(self, strict):
        from fastapi import Response

        with pytest.raises(postgres.DatabaseUnavailable):
            await store_module.get_store()
        response = Response()
        body = await health_route.health(response)
        assert body["status"] == "unavailable" and body["store"] == "unavailable"
        assert response.status_code == 503

    async def test_a_missing_redis_fails_the_health_check(self, strict, fresh_redis, monkeypatch):
        from fastapi import Response

        from infra.redis_client import CacheUnavailable

        monkeypatch.setenv("REDIS_HOST_URL", "")
        with pytest.raises(CacheUnavailable):
            fresh_redis()
        response = Response()
        body = await health_route.health(response)
        assert body["cache"] == "unavailable"
        assert response.status_code == 503
