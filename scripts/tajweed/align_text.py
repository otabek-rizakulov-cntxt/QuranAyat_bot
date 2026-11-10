"""Line-by-line timings for the Muallimi soniy audio lessons (docs/TAJWEED_PLAN.md P2).

    python3 -m scripts.tajweed.align_text [N ...]        default: every transcribed lesson
    python3 -m scripts.tajweed.align_text --report       weakest lines first

Inputs: the typed Arabic rows (data/tajweed/muallimi_text.txt), the Whisper
transcripts and pause profiles from Colab (TAJWEED_CACHE: transcripts/NNN.json,
energy/NNN.npy) and hand fixes (data/tajweed/muallimi_overrides.json).
Output: data/tajweed/muallimi_timings.json, every line of every lesson in reading
order, each with [start, end] seconds and a confidence.

How: the narrator reads each Arabic row aloud and explains in Uzbek between rows.
Whisper (language "uz") writes the Arabic as Latin syllables ("zar zir zur"), so
every row is romanised the same way (زَرْ → "zar") and both sides are folded into
one rough sound alphabet. A dynamic programme then walks the words in order and
gives each row the run of words that sounds most like it; words no row takes are
the Uzbek explanation, split into lines at pauses. Boundaries are moved into the
quietest 20 ms between the two words, using the pause profile.

The core works on plain lists, so it is tested without numpy (tests/
test_tajweed_align.py); numpy is only needed to read the real .npy profiles.
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from typing import List, Optional, Sequence

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "src"))

from domain import tajweed_lessons  # noqa: E402
from domain.uz_translit import to_latin  # noqa: E402

CACHE = os.path.expanduser(os.environ.get("TAJWEED_CACHE", "~/.cache/quranayat/muallimi"))
TIMINGS_PATH = os.path.join(REPO, "data", "tajweed", "muallimi_timings.json")
OVERRIDES_PATH = os.path.join(REPO, "data", "tajweed", "muallimi_overrides.json")
HOP_S = 0.02  # one energy value per 20 ms
VERSION = 1

MAX_ROW_WORDS = 40  # a row is never read as more words than this
UZ_SPLIT_PAUSE = 0.7  # seconds of silence that end an Uzbek line
UZ_MAX_S = 12.0  # ...or this long, at the widest gap inside it
MIN_SIM = 0.5  # below this a row "match" is noise: the row is marked unmatched
LOW_CONF = 0.65
SEED_SIM = 0.5  # a word this close to a row's first syllable may start that row

# --- romanising --------------------------------------------------------------------

# Letter -> its consonant in the folded alphabet ("" for the glottals the narrator
# rarely makes audible to Whisper). Emphatics fold into their plain pairs.
_CONS = {
    "ء": "",
    "أ": "",
    "إ": "",
    "ؤ": "",
    "ئ": "",
    "ا": "",
    "آ": "",
    "ٱ": "",
    "ب": "b",
    "ت": "t",
    "ة": "t",
    "ث": "s",
    "ج": "j",
    "ح": "h",
    "خ": "h",
    "د": "d",
    "ذ": "z",
    "ر": "r",
    "ز": "z",
    "س": "s",
    "ش": "sh",
    "ص": "s",
    "ض": "d",
    "ط": "t",
    "ظ": "z",
    "ع": "",
    "غ": "g",
    "ف": "f",
    "ق": "k",
    "ك": "k",
    "ل": "l",
    "م": "m",
    "ن": "n",
    "ه": "h",
    "و": "v",
    "ي": "y",
    "ى": "y",
}
_NAMES = {  # a bare letter (no haraka) is read by its name, as in lesson 1
    "ا": "alif",
    "ب": "ba",
    "ت": "ta",
    "ث": "sa",
    "ج": "jim",
    "ح": "ha",
    "خ": "ha",
    "د": "dal",
    "ذ": "zal",
    "ر": "ra",
    "ز": "za",
    "س": "sin",
    "ش": "shin",
    "ص": "sad",
    "ض": "dad",
    "ط": "ta",
    "ظ": "za",
    "ع": "ayn",
    "غ": "gayn",
    "ف": "fa",
    "ق": "kaf",
    "ك": "kaf",
    "ل": "lam",
    "م": "mim",
    "ن": "nun",
    "و": "vav",
    "ه": "ha",
    "ي": "ya",
    "ى": "ya",
}
_FATHA, _KASRA, _DAMMA, _SUKUN, _SHADDA = "َ", "ِ", "ُ", "ْ", "ّ"
_TANWIN = {"ً": "an", "ٍ": "in", "ٌ": "un"}
_LONG = {"ٰ": "a", "ٓ": ""}  # dagger alif lengthens; madda is only a sign
_SKIP = {"ـ", "ٔ", "ٕ"}  # tatweel, hamza marks


def romanize(row: str) -> str:
    """An Arabic exercise row as the folded Latin a listener would write down."""
    words = []
    for word in re.split(r"[\s.–\-]+", row.strip()):
        if not word:
            continue
        letters = [c for c in word if c not in _SKIP]
        bare = all(c in _NAMES or c in _CONS for c in letters) and len(letters) <= 2
        muqattaat = "\u0653" in word and not set(word) & {_FATHA, _KASRA, _DAMMA, "\u0670"}
        if bare or muqattaat:
            # bare letters (lesson 1) and muqatta'at (الٓمٓ) are read by their names
            words.append(" ".join(_NAMES[c] for c in letters if c in _NAMES))
            continue
        out = []
        for i, c in enumerate(letters):
            nxt = letters[i + 1] if i + 1 < len(letters) else ""
            vowel_next = nxt in (_FATHA, _KASRA, _DAMMA, _SUKUN, _SHADDA) or nxt in _TANWIN
            if c in "يى" and out and out[-1] == "i" and not vowel_next:
                continue  # bī: the yā lengthens the kasra
            if c == "و" and out and out[-1] == "u" and not vowel_next:
                continue  # bū
            if c in _CONS:
                out.append(_CONS[c])
            elif c == _FATHA:
                out.append("a")
            elif c == _KASRA:
                out.append("i")
            elif c == _DAMMA:
                out.append("u")
            elif c in _TANWIN:
                out.append(_TANWIN[c])
            elif c in _LONG:
                out.append(_LONG[c])
        words.append(fold("".join(out)))
    return " ".join(w for w in words if w)


# Uzbek/Latin spellings folded to the same alphabet: one vowel per quality, no
# doubled letters, emphatic/near pairs merged, apostrophes gone.
_LATIN = [
    ("oʻ", "u"),
    ("o'", "u"),
    ("gʻ", "g"),
    ("g'", "g"),
    ("ch", "j"),
    ("ng", "n"),
    ("x", "h"),
    ("q", "k"),
    ("w", "v"),
    ("e", "i"),
    ("o", "u"),
    ("p", "b"),
    ("c", "k"),
    ("dh", "z"),
    ("th", "s"),
]


def fold(text: str) -> str:
    s = unicodedata.normalize("NFC", text.lower())
    if re.search(r"[Ѐ-ӿ]", s):
        s = to_latin(s).lower()
    if re.search(r"[ء-ي]", s):
        s = romanize(s)
    for a, b in _LATIN:
        s = s.replace(a, b)
    s = re.sub(r"[^a-z ]", "", s)
    s = re.sub(r"(.)\1+", r"\1", s)  # shadda, long vowels, stretched syllables
    return re.sub(r"\s+", " ", s).strip()


def similarity(row_sound: str, heard: str) -> float:
    a, b = row_sound.replace(" ", ""), fold(heard).replace(" ", "")
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b, autojunk=False).ratio()


# --- aligning ----------------------------------------------------------------------


def words_of(transcript: dict) -> List[list]:
    """[[start, end, text], ...] in time order, empty words dropped."""
    out = []
    for seg in transcript.get("segments", []):
        for w in seg.get("words") or [[seg["start"], seg["end"], seg["text"]]]:
            if w[2].strip():
                out.append([float(w[0]), float(w[1]), w[2].strip()])
    return out


def _quietest(energy: Optional[Sequence[float]], a: float, b: float) -> float:
    """The quietest 20 ms between a and b (their midpoint without a profile)."""
    if b <= a:
        return round(b, 2)
    if not energy:
        return round((a + b) / 2, 2)
    i, j = int(a / HOP_S), min(len(energy), int(b / HOP_S) + 1)
    if j <= i:
        return round((a + b) / 2, 2)
    k = min(range(i, j), key=lambda n: energy[n])
    return round(k * HOP_S + HOP_S / 2, 2)


def align(rows: Sequence[str], words: Sequence[list], energy=None, pins: Optional[dict] = None):
    """Lines in reading order: dicts {kind, text, start, end, conf, row?}.

    `rows` are the lesson's Arabic rows in order; `words` the Whisper words. Each
    row takes a contiguous run of words (or none, if nothing sounds like it); the
    words between rows become Uzbek lines. `pins` maps a row index to a hand-set
    {"start", "end"}: that row is forced onto the words inside that span.
    """
    pins = pins or {}
    sounds = [romanize(r).replace(" ", "") for r in rows]
    heard_folded = [fold(w[2]).replace(" ", "") for w in words]  # once, not per comparison
    n, m = len(rows), len(words)
    NEG = float("-inf")
    # best[i][j]: best score having placed rows[:i] using words[:j]
    best = [[NEG] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0.0
    # A reading of a row starts with its first syllable: only words that sound like
    # it may open a row. That keeps the search to a few starts per row instead of
    # every word in the lesson (a 25-row, 1500-word lesson in seconds, not minutes).
    starts = []
    for r in rows:
        first = (romanize(r).split() or [""])[0]
        seed = SequenceMatcher(None, autojunk=False)
        seed.set_seq2(first)
        ok = set()
        for j, h in enumerate(heard_folded):
            if h and first:
                seed.set_seq1(h[: len(first) + 2])  # Whisper may glue syllables: "aziz"
                if seed.ratio() >= SEED_SIM:
                    ok.add(j)
        starts.append(ok)
    matchers = []
    for sound in sounds:
        sm = SequenceMatcher(None, autojunk=False)
        sm.set_seq2(sound)  # SequenceMatcher caches its analysis of seq2
        matchers.append(sm)
    for i in range(n + 1):
        for j in range(m + 1):
            here = best[i][j]
            if here == NEG:
                continue
            if j < m and here > best[i][j + 1]:  # word j is Uzbek talk, not a row
                best[i][j + 1], back[i][j + 1] = here, ("skip",)
            if i == n:
                continue
            pin = pins.get(i)
            if here - 0.5 > best[i + 1][j] and pin is None:  # row i not heard at all
                best[i + 1][j], back[i + 1][j] = here - 0.5, ("miss",)
            if pin is None and j not in starts[i]:
                continue
            sm, heard, limit = matchers[i], "", 2.5 * len(sounds[i]) + 8
            for k in range(j, min(m, j + MAX_ROW_WORDS)):
                heard += heard_folded[k]
                if len(heard) > limit and not pin:
                    break  # far longer than the row: no longer a reading of it
                if pin and not (
                    words[j][0] >= pin["start"] - 0.3 and words[k][1] <= pin["end"] + 0.3
                ):
                    if words[k][1] > pin["end"] + 0.3:
                        break
                    continue
                if not heard or not sounds[i]:
                    continue
                sm.set_seq1(heard)
                if not pin and sm.quick_ratio() < MIN_SIM:
                    continue
                sim = sm.ratio()
                if sim < MIN_SIM and not pin:
                    continue
                # sim × the row's length: a longer row matched well is worth more, and
                # swallowing extra words only lowers sim, so it never pays
                score = here + sim * len(sounds[i]) / 10 + (50.0 if pin else 0.0)
                if score > best[i + 1][k + 1]:
                    best[i + 1][k + 1], back[i + 1][k + 1] = score, ("row", j, round(sim, 2))

    # walk back from the best end state with every row placed
    j = max(range(m + 1), key=lambda x: best[n][x])
    placed, i = [None] * n, n
    while i > 0 or j > 0:
        step = back[i][j]
        if step is None:
            break
        if step[0] == "skip":
            j -= 1
        elif step[0] == "miss":
            i -= 1
        else:
            placed[i - 1] = (step[1], j - 1, step[2])
            i, j = i - 1, step[1]

    # interleave rows and the Uzbek talk between them
    lines, cursor = [], 0
    for r, spot in enumerate(placed):
        if spot is None:
            lines.append(
                {"kind": "ar", "row": r, "text": rows[r], "start": None, "end": None, "conf": 0.0}
            )
            continue
        first, last, sim = spot
        lines += _uz_lines(words[cursor:first])
        lines.append(
            {
                "kind": "ar",
                "row": r,
                "text": rows[r],
                "start": words[first][0],
                "end": words[last][1],
                "conf": round(sim, 2),
            }
        )
        cursor = last + 1
    lines += _uz_lines(words[cursor:])
    return _snap(lines, energy, pins)


def _uz_lines(words: Sequence[list]) -> list:
    """Uzbek talk as lines: split at pauses, or at the widest gap of a long run."""
    out, cur = [], []
    for w in words:
        if cur and (w[0] - cur[-1][1] >= UZ_SPLIT_PAUSE or w[1] - cur[0][0] > UZ_MAX_S):
            out.append(cur)
            cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return [
        {
            "kind": "uz",
            "text": re.sub(r"\s+", " ", " ".join(w[2] for w in ws)).strip(),
            "start": ws[0][0],
            "end": ws[-1][1],
            "conf": 1.0,
        }
        for ws in out
    ]


def _snap(lines: list, energy, pins: dict) -> list:
    """Each boundary into the quiet between two lines; a pinned row keeps its own
    edges and its neighbours are fitted to them."""
    timed = [x for x in lines if x["start"] is not None]
    pinned = set()
    for x in timed:
        pin = pins.get(x.get("row")) if x["kind"] == "ar" else None
        if pin:
            x["start"], x["end"], x["conf"] = pin["start"], pin["end"], 1.0
            pinned.add(id(x))
    for a, b in zip(timed, timed[1:]):
        if id(a) in pinned:
            b["start"] = max(b["start"], a["end"])
        elif id(b) in pinned:
            a["end"] = min(a["end"], b["start"])
        else:
            cut = _quietest(energy, a["end"], b["start"])
            a["end"], b["start"] = cut, cut
    for x in timed:
        x["start"], x["end"] = round(x["start"], 2), round(x["end"], 2)
    return lines


# --- files -------------------------------------------------------------------------


def _read(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as fp:
        return json.load(fp)


def _write(path, data) -> None:
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=1)
        fp.write("\n")


def align_lesson(n: int, overrides: dict) -> Optional[list]:
    transcript = _read(os.path.join(CACHE, "transcripts", "%03d.json" % n))
    if transcript is None:
        return None
    energy = None
    npy = os.path.join(CACHE, "energy", "%03d.npy" % n)
    if os.path.exists(npy):
        import numpy as np

        energy = np.load(npy).tolist()
    lesson_id = "ms-%03d" % n
    rows = [x.text for x in tajweed_lessons.audio_text(lesson_id) if x.kind == "ar"]
    pins = {int(k): v for k, v in overrides.get(lesson_id, {}).items()}
    return align(rows, words_of(transcript), energy, pins)


def report(table: dict, limit: int = 40) -> None:
    weak = [
        (x["conf"], lesson, i, x)
        for lesson, lines in sorted(table.items())
        for i, x in enumerate(lines)
        if x["kind"] == "ar" and x["conf"] < LOW_CONF
    ]
    weak.sort(key=lambda t: t[0])
    print("%d weak Arabic lines (conf < %.2f)" % (len(weak), LOW_CONF))
    for conf, lesson, i, x in weak[:limit]:
        when = (
            "%7.2f-%7.2f" % (x["start"], x["end"]) if x["start"] is not None else "   not heard   "
        )
        print("  %s #%-3d %s  %.2f  %s" % (lesson, i, when, conf, x["text"]))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("lessons", nargs="*", type=int, help="default: every transcribed lesson")
    ap.add_argument("--report", action="store_true", help="only list the weakest lines")
    args = ap.parse_args()

    data = _read(TIMINGS_PATH, {"version": VERSION, "lessons": {}})
    if args.report:
        report(data["lessons"])
        return 0
    overrides = _read(OVERRIDES_PATH, {})
    todo = args.lessons or [x.n for x in tajweed_lessons.audio_lessons()]
    done = 0
    for n in sorted(todo):
        lines = align_lesson(n, overrides)
        if lines is None:
            continue
        data["lessons"]["ms-%03d" % n] = lines
        ar = [x for x in lines if x["kind"] == "ar"]
        weak = sum(1 for x in ar if x["conf"] < LOW_CONF)
        print("%03d  %3d lines, %2d Arabic rows, %2d weak" % (n, len(lines), len(ar), weak))
        done += 1
    if not done:
        print("no transcripts in %s (set TAJWEED_CACHE to the unzipped Colab folder)" % CACHE)
        return 1
    data["lessons"] = dict(sorted(data["lessons"].items()))
    data["version"] = VERSION
    _write(TIMINGS_PATH, data)
    report(data["lessons"], limit=15)
    return 0


if __name__ == "__main__":
    sys.exit(main())
