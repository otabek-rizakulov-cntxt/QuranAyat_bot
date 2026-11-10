"""Check and fix the Muallimi soniy line timings (docs/TAJWEED_PLAN.md P2).

    python3 -m scripts.tajweed.text_debug show 4            every line of lesson 4
    python3 -m scripts.tajweed.text_debug report            weakest Arabic rows first
    python3 -m scripts.tajweed.text_debug clip 4 2 [--pad 1] that line as an mp3 to listen to
    python3 -m scripts.tajweed.text_debug set 4 2 12.3 15.8 pin Arabic row 2 to 12.3-15.8 s
    python3 -m scripts.tajweed.text_debug nudge 4 2 start -0.4
    python3 -m scripts.tajweed.text_debug unpin 4 2

`show`/`clip` take a line number as `show` prints it (#); `set`/`nudge`/`unpin`
take the Arabic *row* number (r) and only edit data/tajweed/muallimi_overrides.json.
Re-run `python3 -m scripts.tajweed.align_text 4` afterwards: a pin is a hard
constraint and the rest of the lesson is re-fitted around it.

`clip` cuts the local download (data/tajweed/downloads/, not in git) by MPEG
frames, so nothing is decoded; the clip goes to the cache folder, never the repo.
"""

import argparse
import json
import os
import sys

from scripts.tajweed.align_text import CACHE, LOW_CONF, OVERRIDES_PATH, REPO, TIMINGS_PATH, report

DOWNLOADS = os.path.join(REPO, "data", "tajweed", "downloads")
CLIPS = os.path.join(CACHE, "clips")
_BITRATES = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320]
_RATES = [44100, 48000, 32000]


def _read(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as fp:
        return json.load(fp)


def _write(path, data) -> None:
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=1, sort_keys=True)
        fp.write("\n")


def lesson_lines(n: int) -> list:
    lines = _read(TIMINGS_PATH, {"lessons": {}})["lessons"].get("ms-%03d" % n)
    if lines is None:
        sys.exit(
            "lesson %d has no timings yet: run python3 -m scripts.tajweed.align_text %d" % (n, n)
        )
    return lines


def _fmt(t) -> str:
    return "   --  " if t is None else "%7.2f" % t


def cmd_show(n: int) -> None:
    pins = _read(OVERRIDES_PATH, {}).get("ms-%03d" % n, {})
    for i, x in enumerate(lesson_lines(n)):
        tag = "r%-2d" % x["row"] if x["kind"] == "ar" else "uz "
        flag = "!" if x["kind"] == "ar" and x["conf"] < LOW_CONF else " "
        pin = " pinned" if x["kind"] == "ar" and str(x["row"]) in pins else ""
        print(
            "#%-3d %s %s-%s %s%.2f  %s%s"
            % (i, tag, _fmt(x["start"]), _fmt(x["end"]), flag, x["conf"], x["text"], pin)
        )


def _frame_starts(data: bytes) -> list:
    """(byte offset, start second) of every MPEG frame."""
    pos, t, out = 0, 0.0, []
    if data[:3] == b"ID3":
        pos = 10 + ((data[6] << 21) | (data[7] << 14) | (data[8] << 7) | data[9])
    while pos + 4 <= len(data):
        b1, b2 = data[pos + 1], data[pos + 2]
        if data[pos] == 0xFF and (b1 & 0xFE) == 0xFA and 0 < b2 >> 4 < 15 and (b2 >> 2) & 3 != 3:
            rate = _RATES[(b2 >> 2) & 3]
            out.append((pos, t))
            pos += 144000 * _BITRATES[b2 >> 4] // rate + ((b2 >> 1) & 1)
            t += 1152 / rate
        else:
            pos += 1
    return out


def cmd_clip(n: int, line: int, pad: float) -> None:
    lines = lesson_lines(n)
    if not 0 <= line < len(lines) or lines[line]["start"] is None:
        sys.exit("line #%d has no time (see `show %d`)" % (line, n))
    name = next((f for f in os.listdir(DOWNLOADS) if f.startswith("%03d_" % n)), None)
    if name is None:
        sys.exit("no local download for lesson %d in %s" % (n, DOWNLOADS))
    with open(os.path.join(DOWNLOADS, name), "rb") as fp:
        data = fp.read()
    frames = _frame_starts(data)
    a, b = max(0.0, lines[line]["start"] - pad), lines[line]["end"] + pad
    first = max([p for p, t in frames if t <= a] or [frames[0][0]])
    last = min([p for p, t in frames if t >= b] or [len(data)])
    os.makedirs(CLIPS, exist_ok=True)
    out = os.path.join(CLIPS, "%03d_line%02d.mp3" % (n, line))
    with open(out, "wb") as fp:
        fp.write(data[first:last])
    print("%s  (%.2f-%.2f s)  %s" % (out, a, b, lines[line]["text"]))


def _pin(n: int, row: int, start=None, end=None, delta=None, field=None, remove=False) -> None:
    pins = _read(OVERRIDES_PATH, {})
    mine = pins.setdefault("ms-%03d" % n, {})
    if remove:
        mine.pop(str(row), None)
    else:
        line = next((x for x in lesson_lines(n) if x.get("row") == row), None)
        if line is None:
            sys.exit("lesson %d has no Arabic row %d" % (n, row))
        cur = dict(mine.get(str(row)) or {"start": line["start"], "end": line["end"]})
        if delta is not None:
            if cur[field] is None:
                sys.exit("row %d has no time to nudge; use `set`" % row)
            cur[field] = round(cur[field] + delta, 2)
        else:
            cur = {"start": round(start, 2), "end": round(end, 2)}
        if cur["start"] >= cur["end"]:
            sys.exit("start must be before end")
        mine[str(row)] = cur
    if not mine:
        pins.pop("ms-%03d" % n)
    _write(OVERRIDES_PATH, pins)
    print("saved; now run: python3 -m scripts.tajweed.align_text %d" % n)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("show").add_argument("lesson", type=int)
    sub.add_parser("report")
    c = sub.add_parser("clip")
    c.add_argument("lesson", type=int)
    c.add_argument("line", type=int)
    c.add_argument("--pad", type=float, default=0.5)
    s = sub.add_parser("set")
    for a, t in (("lesson", int), ("row", int), ("start", float), ("end", float)):
        s.add_argument(a, type=t)
    g = sub.add_parser("nudge")
    g.add_argument("lesson", type=int)
    g.add_argument("row", type=int)
    g.add_argument("field", choices=("start", "end"))
    g.add_argument("delta", type=float)
    u = sub.add_parser("unpin")
    u.add_argument("lesson", type=int)
    u.add_argument("row", type=int)
    args = ap.parse_args()

    if args.cmd == "show":
        cmd_show(args.lesson)
    elif args.cmd == "report":
        report(_read(TIMINGS_PATH, {"lessons": {}})["lessons"])
    elif args.cmd == "clip":
        cmd_clip(args.lesson, args.line, args.pad)
    elif args.cmd == "set":
        _pin(args.lesson, args.row, args.start, args.end)
    elif args.cmd == "nudge":
        _pin(args.lesson, args.row, delta=args.delta, field=args.field)
    else:
        _pin(args.lesson, args.row, remove=True)


if __name__ == "__main__":
    main()
