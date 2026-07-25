# Pytest bootstrap for the BismillahBot / QuranAyat_bot test suite.
#
# The application is imported the same way it runs in production
# (`uvicorn main:app --app-dir src`, CWD at the repo root):
#   * `src/` is on the import path so `import main`, `from locales import ...`,
#     `from modules import ...` resolve as top-level packages.
#   * the process CWD is the repo root so the corpus files resolved relative to
#     CWD load correctly. `modules.quran` parses `quran-data.xml` in a class body
#     at import time, so this must be set BEFORE any app module is imported.
#
# Test environment is pinned here, before the first app import, so that:
#   * `config.env` reads deterministic values, and
#   * `main.load_dotenv()` (which does NOT override already-set vars) can never
#     pull real secrets from a local `.env` into the test process.
# An empty REDIS_HOST_URL forces the in-memory store (config/redis.py), so tests
# never touch the network or a real Redis.

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

if SRC not in sys.path:
    sys.path.insert(0, SRC)

os.chdir(ROOT)

os.environ["TOKEN"] = "123456:TEST-abcdefghijklmnopqrstuvwxyz012345"
os.environ["REDIS_HOST_URL"] = ""          # -> in-memory store, no network
os.environ["AUDIO_BASE_URL"] = "https://cdn.test/audio"
os.environ["PHOTO_BASE_URL"] = "https://cdn.test/images"

import pytest


@pytest.fixture(autouse=True)
def _clean_state_store():
    """Reset the in-memory Redis stand-in between tests.

    The store lives on a process-wide singleton (RedisSingleton), so without this
    one test's saved user state / language would leak into the next.
    """
    from lib.utils import File

    store = File().redis
    if hasattr(store, "_data"):          # MemoryStore, not a real Redis connection
        store._data.clear()
    yield
    if hasattr(store, "_data"):
        store._data.clear()
