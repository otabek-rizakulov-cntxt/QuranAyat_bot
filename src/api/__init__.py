# The Mini App's HTTP API, mounted on the bot's FastAPI app at /api/v1
# (docs/MINI_APP_PLAN.md §5).
#
# Routes here are thin adapters: they authenticate, validate shapes and call
# into `services/*` and `domain/*` — the same code the bot handlers run. No SQL
# lives in this package (tests/test_service_layer.py); persistence goes through
# `infra.store`.

from fastapi import APIRouter

from . import catalog, check, plans, progress, session, stats
from .auth import require_user

__all__ = ["router", "require_user"]

router = APIRouter(prefix="/api/v1")
for module in (session, catalog, plans, check, progress, stats):
    router.include_router(module.router)
