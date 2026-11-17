"""How long Mini App audio takes to start (docs/MAKHRAJ_3D_PLAN.md §9).

The Mini App reports one sample per play: tap -> first `playing` event, in ms, with the
audio host, what kind of audio it was, whether the browser had it cached, the network
type and the platform. Nothing about the user is kept. Each sample is logged as one
line (Koyeb's log search), and the last SAMPLES are kept in memory so reviewers can
read p50/p95 per host and kind without digging through logs. The memory resets on
each deploy, which is fine for before/after comparisons.
"""

import logging
from collections import deque
from typing import Deque, Dict, List, NamedTuple, Tuple

logger = logging.getLogger(__name__)

SAMPLES = 5000
KINDS = ("ayah", "page", "lesson", "translation", "other")


class Sample(NamedTuple):
    host: str
    kind: str
    ms: int
    cached: bool
    net: str
    platform: str


_samples: Deque[Sample] = deque(maxlen=SAMPLES)


def record(sample: Sample) -> None:
    _samples.append(sample)
    logger.info(
        "audio_start host=%s kind=%s ms=%d cached=%s net=%s platform=%s",
        sample.host,
        sample.kind,
        sample.ms,
        int(sample.cached),
        sample.net,
        sample.platform,
    )


def _pct(values: List[int], p: float) -> int:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(p * len(ordered)))]


def summary() -> List[Dict]:
    """p50/p95 per (host, kind, cached), the slowest p95 first."""
    groups: Dict[Tuple[str, str, bool], List[int]] = {}
    for s in _samples:
        groups.setdefault((s.host, s.kind, s.cached), []).append(s.ms)
    rows = [
        {"host": h, "kind": k, "cached": c, "n": len(v), "p50": _pct(v, 0.5), "p95": _pct(v, 0.95)}
        for (h, k, c), v in groups.items()
    ]
    return sorted(rows, key=lambda r: -r["p95"])


def reset_for_tests() -> None:
    _samples.clear()
