"""Find and fix a wrong ayah timing (docs/MULTILINGUAL_PLAN.md §8.1.10).

    python3 -m scripts.uz_audio.debug show 2:255          what we cut, and why
    python3 -m scripts.uz_audio.debug clip 2:255 [--pad 3] [--server]
    python3 -m scripts.uz_audio.debug clip 2:284-285
    python3 -m scripts.uz_audio.debug set 2:255 start 1234.5
    python3 -m scripts.uz_audio.debug nudge 2:255 end -0.4
    python3 -m scripts.uz_audio.debug verify 2 "listened 2:1-20, 2:280-286"
    python3 -m scripts.uz_audio.debug report [2]          weakest boundaries first
    python3 -m scripts.uz_audio.debug smoke               live check against newbooks.uz
    python3 -m scripts.uz_audio.debug purge 2:255         cache keys a fix makes stale

`set`/`nudge`/`verify` only edit data/uz_audio_overrides.json; run
`python3 -m scripts.uz_audio.align S && python3 -m scripts.uz_audio.export`
afterwards (an override is a hard pin, so align re-fits the ayahs around it).
`show` and `report` read the committed table plus the local cache (transcript,
pauses) when it exists, so they work on any machine; `clip --server` needs only
the network.
"""

import argparse
import os
import sys
import urllib.request

from scripts.uz_audio.align import ALIGN_DIR
from scripts.uz_audio.common import (
    ENERGY_DIR,
    OVERRIDES_PATH,
    REPO,
    SOURCE_URL,
    TIMINGS_PATH,
    TRANSCRIPT_DIR,
    load_reference,
    mp3_path,
    read_json,
    write_json,
)

SAMPLES = os.path.join(REPO, "audio-samples")  # excluded via .git/info/exclude


def parse_ref(ref: str) -> tuple:
    surah, ayahs = ref.split(":")
    first, _, last = ayahs.partition("-")
    return int(surah), int(first), int(last or first)


def table() -> dict:
    data = read_json(TIMINGS_PATH)
    if data is None:
        sys.exit("no %s yet — run align and export first" % TIMINGS_PATH)
    return data["surahs"]


def frame_s(entry: dict) -> float:
    return 1152 / entry["sample_rate"]


def fmt(t: float) -> str:
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return "%d:%02d:%05.2f" % (h, m, s) if h else "%d:%05.2f" % (m, s)


# --- show -------------------------------------------------------------------------


def words_near(surah: int, t: float, span: float = 5.0) -> str:
    tr = read_json(os.path.join(TRANSCRIPT_DIR, "%03d.json" % surah))
    if tr is None:
        return "    (no local transcript; run transcribe %d to see words here)" % surah
    out, marked = [], False
    for seg in tr["segments"]:
        for w0, _w1, word in seg["words"]:
            if t - span <= w0 <= t + span:
                if not marked and w0 >= t:
                    out.append("‖")
                    marked = True
                out.append(word)
    if not marked:
        out.append("‖")
    return "    " + " ".join(out)


def pauses_near(surah: int, t: float, span: float = 5.0) -> str:
    path = os.path.join(ENERGY_DIR, "%03d.npy" % surah)
    if not os.path.exists(path):
        return ""
    import numpy as np

    from scripts.uz_audio.align import quiet_mask, quiet_runs

    runs = quiet_runs(quiet_mask(np.load(path)), t - span, t + span)
    return "    pauses: " + ", ".join("%s–%s" % (fmt(a), fmt(b)) for a, b in runs)


def cmd_show(ref: str) -> None:
    surah, first, last = parse_ref(ref)
    entry = table().get(str(surah))
    if entry is None:
        sys.exit("surah %d has no timings" % surah)
    fs, fb = frame_s(entry), entry["frame_bytes"]
    fixes = read_json(OVERRIDES_PATH, {}) or {}
    reference = load_reference()
    aligned = read_json(os.path.join(ALIGN_DIR, "%03d.json" % surah))
    print(
        "surah %d: %s, %d kbps, frame %d B / %.3f s, file %d B, ver %s"
        % (surah, entry["status"], entry["kbps"], fb, fs, entry["size"], entry["ver"])
    )
    for a in range(first, last + 1):
        f0, f1, conf = entry["ayahs"][a - 1]
        print(
            "\n%d:%d  %s → %s  (%.1fs)  confidence %.2f"
            % (surah, a, fmt(f0 * fs), fmt(f1 * fs), (f1 - f0) * fs, conf)
        )
        print("    frames %d-%d  Range: bytes=%d-%d" % (f0, f1, f0 * fb, f1 * fb - 1))
        if "%d:%d" % (surah, a) in fixes:
            print("    override: %s" % fixes["%d:%d" % (surah, a)])
        if aligned:
            print("    heard: %s" % aligned["ayahs"][a - 1]["text"][:200])
        print("    ref:   %s" % reference[(surah, a)].split("(")[0][:200])
        for label, t in (("start", f0 * fs), ("end", f1 * fs)):
            print("  %s cut at %s:" % (label, fmt(t)))
            print(words_near(surah, t))
            p = pauses_near(surah, t)
            if p:
                print(p)


# --- clip -------------------------------------------------------------------------


def cmd_clip(ref: str, pad: float, server: bool) -> None:
    surah, first, last = parse_ref(ref)
    entry = table()[str(surah)]
    fs, fb = frame_s(entry), entry["frame_bytes"]
    f0 = max(0, entry["ayahs"][first - 1][0] - int(pad / fs))
    f1 = min(entry["frames"], entry["ayahs"][last - 1][1] + int(pad / fs))
    start, end = f0 * fb, f1 * fb - 1
    if server:
        req = urllib.request.Request(
            SOURCE_URL % surah,
            headers={"Range": "bytes=%d-%d" % (start, end), "User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
    else:
        with open(mp3_path(surah), "rb") as fp:
            fp.seek(start)
            data = fp.read(end - start + 1)
    os.makedirs(SAMPLES, exist_ok=True)
    name = "%d-%d%s%s.mp3" % (
        surah,
        first,
        "-%d" % last if last > first else "",
        "_pad%g" % pad if pad else "",
    )
    path = os.path.join(SAMPLES, name)
    with open(path, "wb") as fp:
        fp.write(data)
    print(
        "%s  %s → %s  bytes=%d-%d" % (os.path.relpath(path), fmt(f0 * fs), fmt(f1 * fs), start, end)
    )
    if pad:
        print("  the ayah itself starts %.2fs in and ends %.2fs before the end" % (pad, pad))


# --- overrides ----------------------------------------------------------------------


def _save_override(key: str, field: str, value) -> None:
    data = read_json(OVERRIDES_PATH, {}) or {}
    if field == "verified":
        data.setdefault("verified", {})[key] = value
    else:
        data.setdefault(key, {})[field] = round(value, 3)
    write_json(OVERRIDES_PATH, dict(sorted(data.items())), indent=1)
    print("%s: %s = %s" % (os.path.relpath(OVERRIDES_PATH), key, value))


def cmd_set(ref: str, field: str, seconds: float) -> None:
    surah, a, _ = parse_ref(ref)
    _save_override("%d:%d" % (surah, a), field, seconds)


def cmd_nudge(ref: str, field: str, delta: float) -> None:
    surah, a, _ = parse_ref(ref)
    entry = table()[str(surah)]
    f0, f1, _ = entry["ayahs"][a - 1]
    current = (f0 if field == "start" else f1) * frame_s(entry)
    _save_override("%d:%d" % (surah, a), field, current + delta)


# --- report / smoke / purge -----------------------------------------------------------


def cmd_report(surah: int | None) -> None:
    surahs = table()
    if surah is None:
        print("surah  status     ayahs  min-conf  <0.5")
        for k in sorted(surahs, key=int):
            confs = [c for _, _, c in surahs[k]["ayahs"]]
            print(
                "%5s  %-9s  %5d  %8.2f  %4d"
                % (k, surahs[k]["status"], len(confs), min(confs), sum(c < 0.5 for c in confs))
            )
        return
    entry = surahs[str(surah)]
    fs = frame_s(entry)
    rows = sorted(enumerate(entry["ayahs"], start=1), key=lambda r: r[1][2])
    for a, (f0, f1, conf) in rows[:30]:
        print("%d:%-4d conf %.2f  %s → %s" % (surah, a, conf, fmt(f0 * fs), fmt(f1 * fs)))


def cmd_smoke() -> None:
    """Every surah: newbooks.uz still serves the same file, and our first and last
    ayah boundaries still land on MPEG frame headers."""
    bad = 0
    for k, entry in sorted(table().items(), key=lambda kv: int(kv[0])):
        surah, fb = int(k), entry["frame_bytes"]
        for frame in (entry["ayahs"][0][0], entry["ayahs"][-1][0]):
            req = urllib.request.Request(
                SOURCE_URL % surah,
                headers={
                    "Range": "bytes=%d-%d" % (frame * fb, frame * fb + 1),
                    "User-Agent": "Mozilla/5.0",
                },
            )
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    total = int(resp.headers["Content-Range"].split("/")[1])
                    head = resp.read()
                    ok = (
                        resp.status == 206
                        and total == entry["size"]
                        and head[0] == 0xFF
                        and head[1] & 0xE0 == 0xE0
                    )
            except Exception as err:  # report and keep checking the rest
                ok, total = False, err
            if not ok:
                bad += 1
                print("FAIL %03d frame %d: %s" % (surah, frame, total))
    print("smoke: %s" % ("all good" if not bad else "%d failures" % bad))
    sys.exit(1 if bad else 0)


def cmd_purge(ref: str) -> None:
    sys.path.insert(0, os.path.join(REPO, "src"))
    from infra import uz_audio

    surah, a, _ = parse_ref(ref)
    ver = table()[str(surah)]["ver"]
    print("Clips are keyed by the surah's timing version (now %s): after a re-export" % ver)
    print("the bot uses new keys by itself. Stale ids still in Redis, if you want them gone:")
    print(
        "  uzt:<old ver>:%d:%d-%d   and any range uzt:<old ver>:%d:<a>-<b> covering %d"
        % (surah, a, a, surah, a)
    )
    uz_audio.reset_for_tests({str(surah): table()[str(surah)]})
    for p in uz_audio.parts(surah):
        if p.first_ayah <= a <= p.last_ayah:
            print("  uzt:<old ver>:%d:p%d   (whole-surah part %d)" % (surah, p.index, p.index))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("show").add_argument("ref")
    c = sub.add_parser("clip")
    c.add_argument("ref")
    c.add_argument("--pad", type=float, default=0.0)
    c.add_argument("--server", action="store_true")
    for name in ("set", "nudge"):
        p = sub.add_parser(name)
        p.add_argument("ref")
        p.add_argument("field", choices=["start", "end"])
        p.add_argument("value", type=float)
    v = sub.add_parser("verify")
    v.add_argument("surah", type=int)
    v.add_argument("note")
    r = sub.add_parser("report")
    r.add_argument("surah", type=int, nargs="?")
    sub.add_parser("smoke")
    sub.add_parser("purge").add_argument("ref")
    args = ap.parse_args()
    if args.cmd == "show":
        cmd_show(args.ref)
    elif args.cmd == "clip":
        cmd_clip(args.ref, args.pad, args.server)
    elif args.cmd == "set":
        cmd_set(args.ref, args.field, args.value)
    elif args.cmd == "nudge":
        cmd_nudge(args.ref, args.field, args.value)
    elif args.cmd == "verify":
        _save_override(str(args.surah), "verified", args.note)
    elif args.cmd == "report":
        cmd_report(args.surah)
    elif args.cmd == "smoke":
        cmd_smoke()
    else:
        cmd_purge(args.ref)


if __name__ == "__main__":
    main()
