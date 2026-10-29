"""GET / — liveness, and where state lives."""

from fastapi import APIRouter, Response

from config.redis import cache_backend
from lib.store import store_backend

router = APIRouter()


@router.get("/")
async def health(response: Response):
    """Liveness plus where state lives: `store` for user settings, `cache` for
    Redis. 503 when either could not be reached or isn't configured, so a
    deployment missing its database or Redis fails its health check instead of
    serving a bot that forgets every user on the next restart. "pending" (still
    booting) stays 200, so a slow start isn't mistaken for an outage."""
    store, cache = store_backend(), cache_backend()
    healthy = "unavailable" not in (store, cache)
    if not healthy:
        response.status_code = 503
    return {"status": "ok" if healthy else "unavailable", "store": store, "cache": cache}
