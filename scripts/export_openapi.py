#!/usr/bin/env python3
# BismillahBot -- Explore the Holy Qur'an on Telegram
#
# Write the Mini App API's OpenAPI document (docs/MINI_APP_PLAN.md task P0.3).
# The frontend generates its TypeScript types from this file, so a changed
# response shape here fails the frontend's typecheck rather than production.
# Run from the repo root:
#
#     python3 scripts/export_openapi.py [OUT_FILE]       # default: build/openapi.json
#
# Only /api/v1 routes are kept: the webhook and media routes are not part of the
# app's contract (and the webhook path embeds the bot token placeholder).

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from fastapi.openapi.utils import get_openapi  # noqa: E402

DEFAULT_OUT = os.path.join(ROOT, "build", "openapi.json")


def build() -> dict:
    import main

    routes = [r for r in main.app.routes if getattr(r, "path", "").startswith("/api/v1")]
    return get_openapi(title="BismillahBot Mini App API", version="1", routes=routes)


def main_() -> int:
    out = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print("Wrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main_())
