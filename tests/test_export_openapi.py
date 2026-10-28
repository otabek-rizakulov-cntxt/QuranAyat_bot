"""OpenAPI export for the Mini App's generated client (MINI_APP_PLAN.md P0.3)."""

import importlib.util
import os

_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "export_openapi.py")
_spec = importlib.util.spec_from_file_location("export_openapi", _SCRIPT)
exporter = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(exporter)


def test_only_the_api_is_exported():
    doc = exporter.build()
    assert doc["paths"], "no /api/v1 routes found"
    assert all(path.startswith("/api/v1/") for path in doc["paths"])
    assert "/api/v1/auth/telegram" in doc["paths"]


def test_me_requires_bearer_auth():
    doc = exporter.build()
    assert doc["paths"]["/api/v1/me"]["get"]["security"] == [{"HTTPBearer": []}]
