"""Stage 3: alignments + hand fixes -> data/uz_audio_timings.json (the committed table).

    python3 -m scripts.uz_audio.export

For every surah: probe its mp3 (bitrate, frame size, frame count), convert the
aligned seconds to frame indices, apply data/uz_audio_overrides.json, run the
quality gate, and set `status`: "verified" only when a human signed the surah off
in the overrides' "verified" map, otherwise "estimated". Surahs that are not
aligned yet are left out (the bot then shows no buttons for them).

The gate (docs/MULTILINGUAL_PLAN.md §8.1.9) never blocks export; it prints every
problem so `debug report` and the listening pass know where to look, and the CI
test (tests/test_uz_audio_timings.py) enforces the structural half of it.
"""

import hashlib
import json
import os

from scripts.uz_audio.align import ALIGN_DIR
from scripts.uz_audio.common import (
    AYAH_COUNTS,
    OVERRIDES_PATH,
    SOURCE_URL,
    TIMINGS_PATH,
    mp3_path,
    probe,
    read_json,
    write_json,
)

MIN_AYAH_S = 0.8
MIN_CONF = 0.5


def frames_of(seconds: float, frame_s: float) -> int:
    return int(seconds / frame_s)  # round down: a cut never moves into the next word


def overrides() -> tuple:
    """({(surah, ayah): {"start": s, "end": s}}, {surah: note})"""
    raw = read_json(OVERRIDES_PATH, {}) or {}
    fixes = {}
    for key, val in raw.items():
        if ":" in key and isinstance(val, dict):
            s, a = (int(x) for x in key.split(":"))
            fixes[(s, a)] = val
    verified = {int(k): v for k, v in (raw.get("verified") or {}).items()}
    return fixes, verified


def build_surah(surah: int, aligned: dict, fixes: dict, verified: dict) -> tuple:
    """(table entry, [problems]) for one surah."""
    info = probe(mp3_path(surah))
    if info.first_frame != 0:
        raise ValueError("surah %d: audio does not start at byte 0" % surah)
    frame_s = info.frame_seconds
    n = AYAH_COUNTS[surah - 1]
    starts = [a["start"] for a in aligned["ayahs"]]
    end = aligned["ayahs"][-1]["end"]
    confs = [a["conf"] for a in aligned["ayahs"]]
    # A fix moves the shared edge: ayah a's start *is* ayah a-1's end.
    for (s, a), fix in fixes.items():
        if s != surah or not 1 <= a <= n:
            continue
        if "start" in fix:
            starts[a - 1], confs[a - 1] = float(fix["start"]), 1.0
        if "end" in fix:
            if a < n:
                starts[a], confs[a] = float(fix["end"]), 1.0
            else:
                end = float(fix["end"])
    bounds = [frames_of(t, frame_s) for t in starts] + [min(frames_of(end, frame_s), info.frames)]
    ayahs = [[bounds[k], bounds[k + 1], round(confs[k], 3)] for k in range(n)]

    problems = []
    if len(ayahs) != n:
        problems.append("%d ayahs, expected %d" % (len(ayahs), n))
    for k, (a, b, c) in enumerate(ayahs, start=1):
        if not 0 <= a < b <= info.frames:
            problems.append("%d:%d frames %d-%d out of order or out of file" % (surah, k, a, b))
        elif (b - a) * frame_s < MIN_AYAH_S:
            problems.append("%d:%d only %.2fs long" % (surah, k, (b - a) * frame_s))
        if c < MIN_CONF:
            problems.append("%d:%d low confidence %.2f" % (surah, k, c))
    entry = {
        "kbps": info.kbps,
        "sample_rate": info.sample_rate,
        "frame_bytes": info.frame_bytes,
        "frames": info.frames,
        "size": info.size,
        "status": "verified" if surah in verified else "estimated",
        "ayahs": ayahs,
    }
    digest = hashlib.sha1(json.dumps([entry["ayahs"], entry["size"]]).encode()).hexdigest()
    entry["ver"] = digest[:8]
    return entry, problems


def main() -> None:
    fixes, verified = overrides()
    surahs, total, flagged = {}, 0, 0
    for surah in range(1, 115):
        aligned = read_json(os.path.join(ALIGN_DIR, "%03d.json" % surah))
        if aligned is None:
            continue
        entry, problems = build_surah(surah, aligned, fixes, verified)
        surahs[str(surah)] = entry
        total += len(entry["ayahs"])
        low = [p for p in problems if "low confidence" in p]
        hard = [p for p in problems if "low confidence" not in p]
        flagged += len(problems)
        for p in hard:
            print("  ! " + p)
        print(
            "%03d  %-9s %3d ayahs  %3d kbps  low-confidence %d"
            % (surah, entry["status"], len(entry["ayahs"]), entry["kbps"], len(low))
        )
    write_json(
        TIMINGS_PATH, {"version": 1, "source": SOURCE_URL, "surahs": surahs}, separators=(",", ":")
    )
    print(
        "wrote %s: %d surahs, %d ayahs, %d flagged boundaries"
        % (os.path.relpath(TIMINGS_PATH), len(surahs), total, flagged)
    )


if __name__ == "__main__":
    main()
