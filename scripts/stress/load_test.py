"""Load driver for the local Koyeb-capacity test.

Fires increasing tiers of concurrent synthetic users at the stress container's
real webhook route (see docker-compose.stress.yml / run_app.py — every outbound
Telegram call is faked out, everything else is the real app), samples
`docker stats` for CPU/memory throughout, and polls the harness's
`/__stress__/stats` introspection endpoint to find out when background
processing actually drains — not just when the webhook ACKs, since ACK and
completion are deliberately decoupled (main.py fires `_process_update` as a
background task and returns immediately).

Usage:
    docker compose -f docker-compose.stress.yml up --build -d
    python3 scripts/stress/load_test.py
    docker compose -f docker-compose.stress.yml down -v
"""

import asyncio
import json
import statistics
import subprocess
import sys
import time
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).parent))
from gen_updates import batch  # noqa: E402

BASE_URL = "http://localhost:8091"
TOKEN = "stress-test-token"
CONTAINER = "quranayat-stress-app"
TIERS = [5, 10, 20, 40, 80, 150, 300, 600, 1000]
# httpx.AsyncClient defaults to max_connections=100, which would silently
# become the real bottleneck above tier 100 rather than the container itself.
CLIENT_LIMITS = httpx.Limits(max_connections=2000, max_keepalive_connections=200)
DRAIN_TIMEOUT_S = 90
DRAIN_POLL_S = 0.5
STATS_POLL_S = 0.5

RESULTS_PATH = Path(__file__).parent / "results.json"


def _docker_stats() -> dict | None:
    """One snapshot of the app container's CPU%/memory, or None if it's gone."""
    try:
        out = subprocess.run(
            ["docker", "stats", "--no-stream", "--format",
             "{{.CPUPerc}}\t{{.MemUsage}}", CONTAINER],
            capture_output=True, text=True, timeout=5,
        )
    except subprocess.TimeoutExpired:
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    cpu_str, mem_str = out.stdout.strip().split("\t")
    cpu_pct = float(cpu_str.rstrip("%"))
    mem_used = mem_str.split("/")[0].strip()
    return {"cpu_pct": cpu_pct, "mem": mem_used}


def _mem_to_mb(mem_str: str) -> float:
    value = float("".join(c for c in mem_str if c.isdigit() or c == "."))
    if "GiB" in mem_str:
        return value * 1024
    if "KiB" in mem_str:
        return value / 1024
    return value  # MiB


async def _sample_stats(stop: asyncio.Event, samples: list) -> None:
    while not stop.is_set():
        snap = await asyncio.to_thread(_docker_stats)
        if snap is not None:
            samples.append(snap)
        try:
            await asyncio.wait_for(stop.wait(), timeout=STATS_POLL_S)
        except asyncio.TimeoutError:
            pass


def _container_alive() -> bool:
    out = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", CONTAINER],
        capture_output=True, text=True,
    )
    return out.returncode == 0 and out.stdout.strip() == "true"


def _oom_killed() -> bool:
    out = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.OOMKilled}}", CONTAINER],
        capture_output=True, text=True,
    )
    return out.stdout.strip() == "true"


async def _fire_one(client: httpx.AsyncClient, update: dict) -> tuple[float, int]:
    t0 = time.perf_counter()
    try:
        resp = await client.post("/webhook/%s" % TOKEN, json=update, timeout=30)
        return time.perf_counter() - t0, resp.status_code
    except httpx.HTTPError:
        return time.perf_counter() - t0, -1


async def run_tier(client: httpx.AsyncClient, n: int) -> dict:
    print("\n=== Tier: %d concurrent updates ===" % n)

    if not _container_alive():
        print("!! Container is not running — stopping the run early.")
        return {"n": n, "container_alive": False}

    await client.post("/__stress__/reset")

    stop = asyncio.Event()
    samples: list = []
    sampler = asyncio.create_task(_sample_stats(stop, samples))

    updates = batch(n)
    t0 = time.perf_counter()
    results = await asyncio.gather(*(_fire_one(client, u) for u in updates))
    ack_elapsed = time.perf_counter() - t0
    ack_latencies = [r[0] for r in results]
    ack_statuses = [r[1] for r in results]

    # Drain: wait for the background tasks this tier spawned to finish, or time out.
    drain_deadline = time.perf_counter() + DRAIN_TIMEOUT_S
    in_flight = n
    while time.perf_counter() < drain_deadline:
        if not _container_alive():
            break
        try:
            stats = (await client.get("/__stress__/stats", timeout=10)).json()
            in_flight = stats["in_flight"]
        except httpx.HTTPError:
            break
        if in_flight <= 0:
            break
        await asyncio.sleep(DRAIN_POLL_S)
    drain_elapsed = time.perf_counter() - t0

    stop.set()
    await sampler

    alive = _container_alive()
    oom = _oom_killed() if not alive else False

    try:
        final = (await client.get("/__stress__/stats", timeout=10)).json() if alive else {}
    except httpx.HTTPError:
        final = {}

    cpu_samples = [s["cpu_pct"] for s in samples]
    mem_samples = [_mem_to_mb(s["mem"]) for s in samples]

    row = {
        "n": n,
        "container_alive": alive,
        "oom_killed": oom,
        "ack_fire_wall_time_s": round(ack_elapsed, 2),
        "ack_latency_p50_ms": round(statistics.median(ack_latencies) * 1000, 1),
        "ack_latency_p95_ms": round(_pctile(ack_latencies, 95) * 1000, 1),
        "ack_non_200": sum(1 for s in ack_statuses if s != 200),
        "drain_time_s": round(drain_elapsed, 2),
        "in_flight_at_timeout": in_flight,
        "completed": final.get("completed"),
        "errors": final.get("errors"),
        "cpu_pct_peak": max(cpu_samples) if cpu_samples else None,
        "cpu_pct_avg": round(statistics.mean(cpu_samples), 1) if cpu_samples else None,
        "mem_mb_peak": round(max(mem_samples), 1) if mem_samples else None,
    }
    print(json.dumps(row, indent=2))
    return row


def _pctile(values: list, pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = min(len(ordered) - 1, int(len(ordered) * pct / 100))
    return ordered[idx]


async def main() -> None:
    rows = []
    async with httpx.AsyncClient(base_url=BASE_URL, limits=CLIENT_LIMITS) as client:
        try:
            await client.get("/", timeout=10)
        except httpx.HTTPError as e:
            print("Cannot reach %s (%s) — is docker compose up?" % (BASE_URL, e))
            return

        for n in TIERS:
            row = await run_tier(client, n)
            rows.append(row)
            if not row.get("container_alive", True):
                print("\nStopping: container did not survive tier n=%d." % n)
                break
            await asyncio.sleep(2)  # let CPU/mem settle before the next tier

    RESULTS_PATH.write_text(json.dumps(rows, indent=2))
    print("\nResults written to %s" % RESULTS_PATH)


if __name__ == "__main__":
    asyncio.run(main())
