"""Parsing what users type: ayah references ("2:255", "53:1-7") and numeric
command arguments ("/page 255")."""

import re


def parse_ayah(message: str):
    match = re.match(r"/?(\d+)[ :\-;.,]*(\d*)", message)
    if match is not None:
        surah = int(match.group(1))
        ayah = int(match.group(2)) if match.group(2) else 1
        return surah, ayah
    else:
        return None, None


def as_int(text: str):
    """`text` as an int, or None if it isn't one — for command arguments like the
    "255" in "/page 255", where a non-number is a user error, not a crash."""
    try:
        return int(text)
    except ValueError:
        return None


def parse_ayah_range(message: str):
    """Parse a reference into (surah, start, end).

    A range like "53:1-7" -> (53, 1, 7). A single ayah like "2:255" -> (2, 255, 255).
    Returns (None, None, None) when nothing parses.
    """
    # surah <sep> start <dash> end  (three numbers, second separator is a dash)
    match = re.match(r"/?(\d+)[ :.;,]+(\d+)\s*[-–]\s*(\d+)", message)
    if match is not None:
        surah, start, end = (int(match.group(i)) for i in (1, 2, 3))
        if end < start:
            start, end = end, start
        return surah, start, end
    surah, ayah = parse_ayah(message)
    if surah is None:
        return None, None, None
    return surah, ayah, ayah
