"""Building the FastAPI app: routes, CORS and the startup/shutdown lifespan."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router
from app.lifespan import lifespan
from app.routes import health, media, webhook
from app.state import AppState
from config import Environment


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.state.runtime = AppState()
    app.include_router(api_router)
    app.include_router(health.router)
    app.include_router(media.router)
    app.include_router(webhook.router)

    # The Mini App is served from its own origin (docs/MINI_APP_PLAN.md §4.3), so
    # the browser needs CORS to reach /api/v1. Allow-list only, bearer header only —
    # no cookies. With no origins configured the middleware is not installed at all.
    origins = [
        o.strip() for o in (Environment.get_env("miniapp_origins") or "").split(",") if o.strip()
    ]
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
            allow_headers=["Authorization", "Content-Type"],
            allow_credentials=False,
            max_age=600,
        )
    return app
