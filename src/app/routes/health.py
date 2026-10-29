"""GET / — liveness, and where state lives."""

from fastapi import APIRouter, Response

from config.redis import cache_backend
from lib.store import store_backend

router = APIRouter()


@router.get("/")
async def health(response: Response):
    """Liveness plus where state lives: `store` for user settings, `cache` for
    Redis. 503 when either is "unavailable" (the database is unreachable or
    either one isn't configured), so a misconfigured deployment fails its health
    check instead of serving a bot that forgets every user on the next restart.

    "degraded" — Redis is down but the bot is serving from memory — stays 200:
    nothing durable lives in Redis, so an outage there should not take the bot
    offline. "pending" (still booting) stays 200 too."""
    store, cache = store_backend(), cache_backend()
    healthy = "unavailable" not in (store, cache)
    if not healthy:
        response.status_code = 503
    return {"status": "ok" if healthy else "unavailable", "store": store, "cache": cache}
