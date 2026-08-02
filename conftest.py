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
os.environ["DATABASE_URL"] = ""            # -> in-memory settings store, no network
os.environ["AUDIO_BASE_URL"] = "https://cdn.test/audio"
os.environ["PHOTO_BASE_URL"] = "https://cdn.test/images"
# Pinned empty so the local .env's real public URL can't leak in: it decides whether
# inline range recitations are offered, and tests that want it set it themselves.
os.environ["WEBHOOK_URL"] = ""

import pytest


@pytest.fixture(autouse=True)
def _clean_state_store():
    """Reset the in-memory Redis and the repository layer between tests.

    Both live on process-wide module state, so without this one test's saved
    user state / language / reciter would leak into the next.

    `lib.store.reset_for_tests()` drops the store singleton, every in-memory row
    and the creation locks. The locks matter because an asyncio.Lock binds to the
    loop it is first awaited in and pytest-asyncio gives each test its own loop;
    production has a single loop for the process lifetime, so this only bites
    under test.
    """
    from lib.utils import File
    from lib.store import reset_for_tests

    redis = File().redis
    if hasattr(redis, "_data"):          # MemoryStore, not a real Redis connection
        redis._data.clear()
    reset_for_tests()
    yield
    if hasattr(redis, "_data"):
        redis._data.clear()
    reset_for_tests()
