"""Stress-test entrypoint — runs the real app with the Telegram side faked out.

Not part of the deployed image (see docker-compose.stress.yml, which is the
only thing that runs this). It exists so `docs/KOYEB_CAPACITY_REPORT.md` can be
produced against the real `handle_update` code path, under Koyeb-equivalent
CPU/memory limits, without a single real request reaching Telegram's API or a
real bot token/chat.

How the fake-out works: `modules.bot.Bot.get_instance()` lazily builds one
`telegram.Bot` and caches it forever. Pre-seeding that cache with an
`AsyncMock()` *before* `main` is imported means `_initialize()`'s
`bot = Bot.get_instance()` picks up the mock and every outbound call
(`send_message`, `send_photo`, `set_webhook`, ...) resolves instantly with no
network — exactly the pattern the whole test suite already relies on
(`tests/test_handle_update.py`, `tests/test_acceptance.py`), reused here
instead of inventing a second way to fake a bot.

Everything else is real: real corpora parsing, real Postgres pool and schema,
real image/audio fetches from the CDN in .env, real `handle_update` routing,
memory allocation and CPU cost. Only the one network call this project cannot
safely make in a load test — to Telegram — is removed.
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path
from unittest.mock import AsyncMock

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))
os.chdir(REPO_ROOT)  # corpus files (quran-data.xml, translations/*) resolve relative to CWD

import telegram  # noqa: E402
import modules.bot as bot_module  # noqa: E402

# A plain AsyncMock() breaks `telegram.Update.de_json` (main.py's webhook route
# calls it with this same bot): mock auto-attribute creation makes
# `hasattr(bot, "defaults")` true, and de_json reads `bot.defaults.tzinfo`,
# which is itself a Mock rather than a real tzinfo or None. `spec=telegram.Bot`
# restricts the mock to Bot's real attribute surface — `defaults` lives only on
# `telegram.ext.ExtBot`, so `hasattr` correctly comes back False and de_json
# takes its "no defaults configured" path, same as a real Bot would.
bot_module.Bot._instance = AsyncMock(spec=telegram.Bot)

import main  # noqa: E402 — imported only after the bot is faked out

# --- Instrumentation ---------------------------------------------------------
#
# `telegram_webhook` (main.py) does `asyncio.create_task(_process_update(update))`
# and looks `_process_update` up from main's module globals *at call time*, so
# reassigning `main._process_update` here — after import — is picked up by every
# webhook call from this point on. No edit to main.py needed.

_latencies_ns: list = []
_errors = 0
_started = 0
_stats_lock = asyncio.Lock()

_orig_process_update = main._process_update


async def _instrumented_process_update(update):
    global _errors, _started
    async with _stats_lock:
        _started += 1
    t0 = time.perf_counter()
    try:
        await _orig_process_update(update)
    except Exception:
        async with _stats_lock:
            _errors += 1
        raise
    finally:
        async with _stats_lock:
            _latencies_ns.append(time.perf_counter() - t0)


main._process_update = _instrumented_process_update


@main.app.get("/__stress__/stats")
async def _stress_stats():
    async with _stats_lock:
        latencies = list(_latencies_ns)
        started, errors = _started, _errors
    return {
        "started": started,
        "completed": len(latencies),
        "in_flight": len(main._background_tasks) - 1,  # minus the scheduler's own task
        "errors": errors,
        "latencies_tail": latencies[-2000:],
    }


@main.app.post("/__stress__/reset")
async def _stress_reset():
    global _errors, _started
    async with _stats_lock:
        _latencies_ns.clear()
        _errors = 0
        _started = 0
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(main.app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
