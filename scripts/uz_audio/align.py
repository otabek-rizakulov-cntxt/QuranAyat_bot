"""Stage 2: turn a surah's transcript + pause profile into ayah boundaries.

    python3 -m scripts.uz_audio.align [SURAH ...]

Reads the cache written by `transcribe` and the hand fixes in
data/uz_audio_overrides.json; writes align/NNN.json into the cache:

    {"surah": 2, "intro_end": 41.3,
     "ayahs": [{"start": 41.3, "end": 55.0, "conf": 0.91,
                "pause": 0.84, "sim": 0.47, "text": "...whisper text..."}, ...]}

How (docs/MULTILINGUAL_PLAN.md §8.1.9): Whisper segments, split again at long
in-segment silences, are the units. A dynamic programme assigns consecutive units
to [intro, ayah 1 … ayah N], scoring how much each unit's text resembles its
ayah's reference translation (a different translation, so it guides rather than
anchors), how long the pause before each ayah is, and how well each ayah's length
fits the surah's speaking rate. Each boundary is then placed inside the quiet
stretch just before the next ayah's speech starts.
"""

import argparse
import math
import os
import re
import unicodedata

import numpy as np

from scripts.uz_audio.common import (
    AYAH_COUNTS,
    CACHE,
    ENERGY_DIR,
    OVERRIDES_PATH,
    TRANSCRIPT_DIR,
    load_reference,
    read_json,
    write_json,
)

ALIGN_DIR = os.path.join(CACHE, "align")
HOP_S = 0.02  # energy resolution
QUIET_DB = 10.0  # above the surah's noise floor (10th percentile) still counts as quiet
MIN_PAUSE = 0.2
LEAD_IN = 0.2  # cut this long before the next ayah's speech onset
SPLIT_GAP = 0.45  # split a Whisper segment where two words are this far apart
MIN_AYAH_S = 0.8  # no ayah clip shorter than this (export's gate uses the same floor)
# Fallback for a surah where those units are fewer than its ayahs: split wherever the
# audio has a pause this long near a word boundary. Word times smear real pauses
# (faster-whisper put 1:3 and 1:4, ~1 s apart, in one segment with no gap between the
# words). Only a fallback: finer units give the search more room to misplace a cut.
SPLIT_PAUSE = 0.3
MIN_VOICED = 0.3  # seconds of non-quiet audio a split-off piece must contain
BLIP = 6  # hops (0.12 s)  # split a Whisper segment where two words are this far apart

# --- text normalisation ----------------------------------------------------------

_ARABIC = {
    "ا": "a",
    "أ": "a",
    "إ": "i",
    "آ": "a",
    "ب": "b",
    "پ": "p",
    "ت": "t",
    "ث": "s",
    "ج": "j",
    "چ": "ch",
    "ح": "h",
    "خ": "x",
    "د": "d",
    "ذ": "z",
    "ر": "r",
    "ز": "z",
    "ژ": "j",
    "س": "s",
    "ش": "sh",
    "ص": "s",
    "ض": "z",
    "ط": "t",
    "ظ": "z",
    "ع": "",
    "غ": "g",
    "ف": "f",
    "ق": "q",
    "ک": "k",
    "ك": "k",
    "گ": "g",
    "ل": "l",
    "م": "m",
    "ن": "n",
    "و": "v",
    "ه": "h",
    "ة": "h",
    "ی": "y",
    "ي": "y",
    "ى": "y",
    "ئ": "y",
    "ؤ": "v",
    "ء": "",
}
_CYRILLIC = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "ғ": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "j",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "қ": "q",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "ў": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "x",
    "ҳ": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "ъ": "",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}
_LATIN = {"ə": "a", "ş": "sh", "ç": "ch", "ı": "i", "ğ": "g", "ñ": "n", "ß": "s"}
# Consonant skeleton: Whisper's Uzbek vowels and x/h, q/k, w/v are unreliable.
_FOLD = str.maketrans({"x": "h", "q": "k", "w": "v", "c": "s", "j": "y"})


def strip_notes(text: str) -> str:
    """Drop the bracketed tafsir notes in uz.txt; the narration doesn't read them.

    Innermost pairs first (notes nest), then anything after an unclosed "(" and
    before a stray ")"."""
    prev = None
    while prev != text:
        prev, text = text, re.sub(r"\([^()]*\)", " ", text)
    text = text.split("(")[0]
    return text.rsplit(")", 1)[-1]


def skeleton(text: str) -> str:
    text = text.lower()
    out = []
    for ch in text:
        ch = _ARABIC.get(ch) or _CYRILLIC.get(ch) or _LATIN.get(ch) or ch
        out.append(ch)
    text = unicodedata.normalize("NFKD", "".join(out))
    text = "".join(c for c in text if c.isascii() and c.isalpha())
    text = text.replace("sh", "s").replace("ch", "s").translate(_FOLD)
    return re.sub(r"[aeiouy]", "", text)


def trigrams(s: str) -> set:
    return {s[i : i + 3] for i in range(len(s) - 2)}


def containment(unit: set, ref: set) -> float:
    return len(unit & ref) / len(unit) if unit else 0.0


# --- audio helpers ----------------------------------------------------------------


def quiet_mask(energy: np.ndarray) -> np.ndarray:
    """Quiet hops, with blips shorter than BLIP (a click, a breath) filled in so
    they don't split one pause into two."""
    quiet = energy < np.percentile(energy, 10) + QUIET_DB
    loud = np.flatnonzero(~quiet)
    if len(loud):
        # a loud run of <= BLIP hops between two quiet hops counts as quiet
        edges = np.flatnonzero(np.diff(loud) > 1)
        starts = np.concatenate([[loud[0]], loud[edges + 1]])
        ends = np.concatenate([loud[edges], [loud[-1]]])
        for a, b in zip(starts, ends):
            if b - a + 1 <= BLIP and a > 0 and b + 1 < len(quiet):
                quiet[a : b + 1] = True
    return quiet


def quiet_runs(quiet: np.ndarray, a: float, b: float):
    """Quiet stretches ≥ MIN_PAUSE inside [a, b] seconds, as (start, end) seconds."""
    i, j = max(0, int(a / HOP_S)), min(len(quiet), int(b / HOP_S) + 1)
    runs, k = [], i
    while k < j:
        if quiet[k]:
            m = k
            while m < j and quiet[m]:
                m += 1
            if (m - k) * HOP_S >= MIN_PAUSE:
                runs.append((k * HOP_S, m * HOP_S))
            k = m
        else:
            k += 1
    return runs


# --- units ------------------------------------------------------------------------


def voiced(quiet: np.ndarray, a: float, b: float) -> float:
    """Seconds of non-quiet audio in [a, b]."""
    i, j = max(0, int(a / HOP_S)), min(len(quiet), int(b / HOP_S))
    return float((~quiet[i:j]).sum()) * HOP_S if j > i else 0.0


def units_from(transcript: dict, quiet: np.ndarray, fine: bool = False) -> list:
    """Whisper segments, split where a long quiet gap separates two words.

    `fine`: split at every real pause between words instead (see SPLIT_PAUSE)."""
    units = []
    for seg in transcript["segments"]:
        words = seg["words"] or [[seg["start"], seg["end"], seg["text"]]]
        cur = [words[0]]
        for prev, w in zip(words, words[1:]):
            if fine:
                near = quiet_runs(quiet, prev[1] - 0.3, w[0] + 0.3)
                # ...unless the piece before is barely spoken: a word Whisper smeared over
                # the pause (1:3's "O" sat on the pause before it) stays with what follows.
                split = any(b - a >= SPLIT_PAUSE for a, b in near) and (
                    voiced(quiet, cur[0][0], prev[1]) >= MIN_VOICED
                )
            else:
                split = w[0] - prev[1] >= SPLIT_GAP and bool(quiet_runs(quiet, prev[1], w[0]))
            if split:
                units.append(cur)
                cur = []
            cur.append(w)
        units.append(cur)
    out = []
    for ws in units:
        text = " ".join(w[2] for w in ws)
        out.append(
            {
                "start": ws[0][0],
                "end": ws[-1][1],
                "first_word_end": ws[0][1],
                "text": text,
                "tri": trigrams(skeleton(text)),
            }
        )
    return out


def onset_cut(quiet: np.ndarray, prev_end: float, next_start: float, next_word_end: float):
    """Where to cut between two units, and how long the pause there is.

    Measured on al-Fatiha and al-Baqarah 283-286: Whisper's segment start is never
    later than the real speech onset, but can be up to ~1.4 s early. So the onset
    lies in [next_start, end of the unit's first word], and the cut goes in the
    first quiet run that ends inside that window, LEAD_IN before speech resumes.
    Taking the *first* such run matters: a later one would cut off a short first
    word ("Hamd." in 1:2 is 0.8 s and is followed by its own pause)."""
    runs = quiet_runs(quiet, prev_end - 0.5, next_word_end + 0.4)
    near = [r for r in runs if next_start - 0.25 <= r[1] <= next_word_end + 0.3]
    if near:
        a, b = min(near, key=lambda r: r[1])
    elif runs:
        a, b = max(runs, key=lambda r: (r[1] - r[0]) - 0.3 * abs(r[1] - next_start))
    else:
        return max(prev_end, next_start - LEAD_IN), 0.0
    return max(a, b - LEAD_IN), b - a


# --- dynamic programme ------------------------------------------------------------


def align(surah: int, ref: dict, transcript: dict, energy: np.ndarray, pins: dict) -> dict:
    """Ayah boundaries for one surah; retries with finer units if there are too few."""
    try:
        return _align(surah, ref, transcript, energy, pins, fine=False)
    except RuntimeError:
        result = _align(surah, ref, transcript, energy, pins, fine=True)
        result["fine_units"] = True  # worth a listen: see SPLIT_PAUSE
        return result


def _align(
    surah: int, ref: dict, transcript: dict, energy: np.ndarray, pins: dict, fine: bool
) -> dict:
    n = AYAH_COUNTS[surah - 1]
    quiet = quiet_mask(energy)
    units = units_from(transcript, quiet, fine)
    U = len(units)
    ref_sk = [skeleton(strip_notes(ref[(surah, a)])) for a in range(1, n + 1)]
    ref_tri = [trigrams(sk) for sk in ref_sk]
    ref_len = np.array([max(1, len(sk)) for sk in ref_sk], float)
    pause_before = [0.0] + [
        onset_cut(quiet, units[u - 1]["end"], units[u]["start"], units[u]["first_word_end"])[1]
        for u in range(1, U)
    ]

    def dice(u0: int, u1: int, k: int) -> float:
        seg = set().union(*(units[u]["tri"] for u in range(u0, u1))) if u1 > u0 else set()
        total = len(seg) + len(ref_tri[k])
        return 2 * len(seg & ref_tri[k]) / total if total else 0.0

    # Hard constraints from overrides: an ayah pinned to start at t must start at
    # the unit nearest t.
    pinned_unit = {}
    for (s, a), t in pins.items():
        if s == surah and 1 <= a <= n:
            pinned_unit[a - 1] = min(range(U), key=lambda u: abs(units[u]["start"] - t))

    # The intro (surah name, where it was revealed, how many ayahs, …) always ends
    # with the basmala. In al-Fatiha the basmala *is* ayah 1; elsewhere ayah 1 is
    # the unit after it. At-Tawbah has none, so the intro end is left to the search.
    first, last = units[0]["start"], units[-1]["end"]
    basmala = trigrams(skeleton(strip_notes(ref[(1, 1)])))
    window = max(240.0, 0.25 * (last - first))
    anchor = next(
        (
            u
            for u in range(U)
            if units[u]["start"] - first <= window and containment(units[u]["tri"], basmala) >= 0.5
        ),
        None,
    )
    first_unit = None if anchor is None else (anchor if surah == 1 else anchor + 1)
    # A "basmala" that leaves fewer units than ayahs is a false match late in the
    # surah (84: the real one was misheard, a phrase at unit 57 of 66 matched).
    if first_unit is not None and U - first_unit < n:
        first_unit = None
    if 0 not in pinned_unit and first_unit is not None and surah != 9:
        intro_starts = [first_unit]
    else:
        intro_starts = [u for u in range(U) if units[u]["start"] - first <= window]

    starts_s = np.array([x["start"] for x in units])

    def search(rate: float, body_start: float) -> list:
        """Best start unit per ayah (plus U at the end) for a given speaking rate."""
        cum = np.concatenate([[0.0], np.cumsum(ref_len)]) / ref_len.sum()
        span = last - body_start
        slack = max(90.0, 0.2 * span)
        NEG = -1e18
        # best[k][u]: ayah k (0-based) starts at unit u; value = score of ayahs < k.
        best = np.full((n + 1, U + 1), NEG)
        back = np.zeros((n + 1, U + 1), dtype=np.int32)
        for u in intro_starts:
            best[0][u] = 0.0  # units before u are the intro
        for k in range(n):
            expect = rate * ref_len[k]
            ref_set = ref_tri[k]
            lo_u, hi_u = np.searchsorted(
                starts_s, [body_start + cum[k] * span - slack, body_start + cum[k] * span + slack]
            )
            if k == 0:
                lo_u, hi_u = 0, U
            for u in range(lo_u, min(U, hi_u + 1)):
                if best[k][u] == NEG:
                    continue
                if k in pinned_unit and pinned_unit[k] != u:
                    continue
                seg, inter = set(), 0
                for v in range(u + 1, U + 1):  # ayah k covers units u..v-1
                    new = units[v - 1]["tri"] - seg
                    inter += len(new & ref_set)
                    seg |= new
                    dur = units[v - 1]["end"] - units[u]["start"]
                    if dur > 4 * expect + 20:
                        break
                    if (k == n - 1) != (v == U):
                        continue  # only the last ayah may (and must) run to the end
                    d = 2 * inter / (len(seg) + len(ref_set)) if seg or ref_set else 0.0
                    score = 3.0 * d - 0.5 * abs(math.log(max(dur, 0.3) / max(expect, 0.3)))
                    if v < U:
                        score += 0.5 * min(pause_before[v], 1.0)
                    total = best[k][u] + score
                    if total > best[k + 1][v]:
                        best[k + 1][v] = total
                        back[k + 1][v] = u
        if best[n][U] == NEG:
            raise RuntimeError("no alignment found (too few units?)")
        starts = [0] * (n + 1)
        starts[n] = U
        for k in range(n, 0, -1):
            starts[k - 1] = int(back[k][starts[k]])
        return starts

    # Two passes: the first guesses the pace from everything after the intro
    # window, the second re-measures it from where the ayahs actually start.
    def pace(u0: int) -> float:
        return sum(x["end"] - x["start"] for x in units[u0:]) / ref_len.sum()

    u_body = intro_starts[0]
    starts = search(pace(u_body), units[u_body]["start"])
    starts = search(pace(starts[0]), units[starts[0]]["start"])

    ayahs = []
    for k in range(n):
        u0, u1 = starts[k], starts[k + 1]
        if u0 == 0:
            cut, pause = max(0.0, units[0]["start"] - LEAD_IN), 1.0
        else:
            cut, pause = onset_cut(
                quiet, units[u0 - 1]["end"], units[u0]["start"], units[u0]["first_word_end"]
            )
        if k in pinned_unit and (surah, k + 1) in pins:
            cut, pause = pins[(surah, k + 1)], 9.9
        ayahs.append(
            {
                "start": round(cut, 3),
                "pause": round(pause, 2),
                "sim": round(dice(u0, u1, k), 3),
                "text": " | ".join(units[u]["text"] for u in range(u0, u1)),
            }
        )
    # Two neighbouring cuts can land in the same pause (10:27 came out 0 s long).
    # Keep every ayah at least MIN_AYAH_S long; such an ayah keeps its low confidence.
    for k in range(1, n):
        floor = ayahs[k - 1]["start"] + MIN_AYAH_S + 0.05  # margin for frame rounding
        if ayahs[k]["start"] < floor:
            ayahs[k]["start"] = round(floor, 3)
            ayahs[k]["pause"] = 0.0
    end_unit = units[U - 1]
    tail = quiet_runs(quiet, end_unit["end"], end_unit["end"] + 2.0)
    last_end = tail[0][0] + 0.15 if tail else end_unit["end"] + 0.3
    duration = len(energy) * HOP_S
    for k, a in enumerate(ayahs):
        a["end"] = ayahs[k + 1]["start"] if k + 1 < n else round(min(last_end, duration), 3)
        # Confidence: a clear pause at the start, and text that resembles the ayah.
        a["conf"] = round(min(1.0, a["pause"] / 0.6) * min(1.0, 0.3 + a["sim"] * 1.5), 3)
    return {
        "surah": surah,
        "intro_end": ayahs[0]["start"],
        "rate": round(pace(starts[0]), 4),
        "units": U,
        "ayahs": ayahs,
    }


def load_pins() -> dict:
    """Override starts/ends as hard pins: {(surah, ayah): start_seconds}."""
    pins = {}
    for key, val in (read_json(OVERRIDES_PATH, {}) or {}).items():
        if ":" not in key or not isinstance(val, dict):
            continue
        s, a = (int(x) for x in key.split(":"))
        if "start" in val:
            pins[(s, a)] = float(val["start"])
        if "end" in val and a < AYAH_COUNTS[s - 1]:
            pins[(s, a + 1)] = float(val["end"])
    return pins


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("surahs", nargs="*", type=int, help="default: every transcribed surah")
    args = ap.parse_args()
    ref, pins = load_reference(), load_pins()
    failed = []
    for surah in args.surahs or range(1, 115):
        tpath = os.path.join(TRANSCRIPT_DIR, "%03d.json" % surah)
        if not os.path.exists(tpath):
            if args.surahs:
                print("%03d  not transcribed yet" % surah)
            continue
        energy = np.load(os.path.join(ENERGY_DIR, "%03d.npy" % surah))
        transcript = read_json(tpath)
        try:
            result = align(surah, ref, transcript, energy, pins)
        except RuntimeError as err:  # one surah must not stop the other 113
            print("%03d  FAILED: %s" % (surah, err), flush=True)
            failed.append(surah)
            continue
        result["mp3"] = transcript.get("mp3")  # frame facts, for export without the mp3
        write_json(os.path.join(ALIGN_DIR, "%03d.json" % surah), result, indent=1)
        confs = [a["conf"] for a in result["ayahs"]]
        print(
            "%03d  %3d ayahs  intro %6.1fs  min conf %.2f  low(<0.5) %d"
            % (surah, len(confs), result["intro_end"], min(confs), sum(c < 0.5 for c in confs)),
            flush=True,
        )

    if failed:
        print("failed: %s (export leaves them out; see debug report)" % failed)


if __name__ == "__main__":
    main()
