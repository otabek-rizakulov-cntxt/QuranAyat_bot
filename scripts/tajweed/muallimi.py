#!/usr/bin/env python3
"""The Muallimi soniy audio lessons -> data/tajweed/muallimi.json.

    python3 scripts/tajweed/muallimi.py

Reads the 73 lesson mp3s from data/tajweed/downloads/ (NNN_<Slug>.mp3, gitignored;
the files themselves live on R2, see scripts/tajweed/upload_r2.py) and writes the
committed manifest: id, title, unit, R2 file name, size, duration and sha256 per
lesson. Durations come from walking the MPEG frames, so nothing is decoded.
Deterministic and light: one read of ~134 MB, seconds.
"""

import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOWNLOADS = os.path.join(ROOT, "data", "tajweed", "downloads")
OUT = os.path.join(ROOT, "data", "tajweed", "muallimi.json")

# Lesson titles as the book names them (apostrophes normalised to ʻ / ʼ).
TITLES = {
    1: "Arab alifbosi",
    2: "Alif harfi",
    3: "Ro harfi",
    4: "Za harfi",
    5: "Mim harfi",
    6: "Ta harfi",
    7: "Nun harfi",
    8: "Ya harfi",
    9: "Ba harfi",
    10: "Kaf harfi",
    11: "Lam harfi",
    12: "Vav harfi",
    13: "Ha harfi",
    14: "Fa harfi",
    15: "Qof harfi",
    16: "Shin harfi",
    17: "Sin harfi",
    18: "Sa harfi",
    19: "Sod harfi",
    20: "To harfi",
    21: "Jim harfi",
    22: "Xo harfi",
    23: "Haa harfi",
    24: "Gʻayn harfi",
    25: "Ayn harfi",
    26: "Dal harfi",
    27: "Zod harfi",
    28: "Zal harfi",
    29: "Zo harfi",
    30: "Madli harflar",
    31: "Tashdidli harflar",
    32: "Tanvinli harflar",
    33: "Tanvinli tashdid",
    34: "Alif va hamza",
    35: "Ta marbuta",
    36: "Yozilmasa ham oʻqiladigan harflar",
    37: "Yoi muqaddara",
    38: "Vovi muqaddara",
    39: "Yoi alifiya",
    40: "Vovi alifiya",
    41: "Yozilsa ham oʻqilmaydigan harflar",
    42: "Idgʻom shamsiya",
    43: "Izhor qamariya",
    44: "Vasl (qoʻshib oʻqish)",
    45: "Vaqf (toʻxtash)",
    46: "Mad (choʻzib oʻqish) qoidalari",
    47: "Tabiiy mad",
    48: "Muttasil mad",
    49: "Munfasil mad",
    50: "Lozim mad",
    51: "Oriz mad",
    52: "Lin lozim mad",
    53: "Lin oriz mad",
    54: "Izhor",
    55: "Iqlob",
    56: "Gʻunnali idgʻom",
    57: "Gʻunnasiz idgʻom",
    58: "Ixfo",
    59: "Tafximli ro",
    60: "Tarqiqli ro",
    61: "Alloh lafzi",
    62: "Muqattaot harflari",
    63: "Sakta",
    64: "Istiʼoza",
    65: "Basmala",
    66: "Hamza haqida",
    67: "Kalimai tayyiba",
    68: "Kalimai shahodat",
    69: "Kalimai tavhid",
    70: "Iymoni mufassal",
    71: "Kalimai istigʻfor",
    72: "Kalimai tamjid",
    73: "Soʻz boshi",
}

# (unit id, title, lesson numbers in teaching order). The preface comes first.
UNITS = [
    ("ms-kirish", "Kirish", [73, 1]),
    ("ms-harflar", "Harflar", list(range(2, 30))),
    ("ms-belgilar", "Harakat va belgilar", list(range(30, 42))),
    ("ms-lom-vasl-vaqf", "Lom, vasl va vaqf", list(range(42, 46))),
    ("ms-mad", "Mad (choʻzib oʻqish)", list(range(46, 54))),
    ("ms-nun-sokin", "Nun sokin va tanvin", list(range(54, 59))),
    ("ms-boshqa", "Boshqa qoidalar", list(range(59, 67))),
    ("ms-kalimalar", "Kalimalar", list(range(67, 73))),
]

_BITRATES = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320]  # MPEG-1 L3
_RATES = [44100, 48000, 32000]


def _id3_size(data: bytes) -> int:
    if data[:3] != b"ID3":
        return 0
    size = (data[6] << 21) | (data[7] << 14) | (data[8] << 7) | data[9]
    return 10 + size + (10 if data[5] & 0x10 else 0)


def duration(data: bytes) -> float:
    """Seconds of MPEG-1 Layer III audio, by walking frame headers."""
    pos, seconds, n = _id3_size(data), 0.0, len(data)
    while pos + 4 <= n:
        b1, b2 = data[pos + 1], data[pos + 2]
        if data[pos] != 0xFF or (b1 & 0xFE) != 0xFA:  # sync + MPEG-1 + Layer III
            pos += 1
            continue
        br, sr = b2 >> 4, (b2 >> 2) & 3
        if not 0 < br < 15 or sr == 3:
            pos += 1
            continue
        rate = _RATES[sr]
        size = 144000 * _BITRATES[br] // rate + ((b2 >> 1) & 1)
        seconds += 1152 / rate
        pos += size
    return seconds


def main() -> int:
    files = {}
    for name in os.listdir(DOWNLOADS):
        m = re.match(r"^(\d{3})_.+\.mp3$", name)
        if m:
            files[int(m.group(1))] = os.path.join(DOWNLOADS, name)
    missing = sorted(set(TITLES) - set(files))
    if missing:
        print("missing downloads:", missing, file=sys.stderr)
        return 1

    unit_of = {n: u for u, _, ns in UNITS for n in ns}
    lessons = []
    for _, _, numbers in UNITS:
        for n in numbers:
            with open(files[n], "rb") as fp:
                data = fp.read()
            lessons.append(
                {
                    "id": "ms-%03d" % n,
                    "n": n,
                    "unit": unit_of[n],
                    "title": TITLES[n],
                    "file": "%03d.mp3" % n,
                    "bytes": len(data),
                    "seconds": round(duration(data), 1),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
    doc = {
        "about": "Muallimi soniy audio lessons. Audio lives on R2 under "
        "tajweed/muallimi-soniy/<file>; this manifest is generated by "
        "scripts/tajweed/muallimi.py (docs/TAJWEED_PLAN.md).",
        "units": [{"id": u, "title": t} for u, t, _ in UNITS],
        "lessons": lessons,
    }
    with open(OUT, "w", encoding="utf-8") as fp:
        json.dump(doc, fp, ensure_ascii=False, indent=1)
        fp.write("\n")
    total = sum(x["seconds"] for x in lessons)
    print(
        "%d lessons, %.1f min, %.1f MB -> %s"
        % (len(lessons), total / 60, sum(x["bytes"] for x in lessons) / 1e6, OUT)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
