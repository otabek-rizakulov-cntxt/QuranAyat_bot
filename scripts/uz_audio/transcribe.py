"""Stage 1: transcribe each surah with word timestamps and record its pause profile.

    python3 -m scripts.uz_audio.transcribe [SURAH ...] [--force] [--wait]

Writes, per surah, into the local cache (never the repo):
    transcripts/NNN.json  Whisper segments + words, times in seconds from file start,
                          and the mp3's frame facts (`mp3`: kbps, frame_bytes, frames, size)
    energy/NNN.npy        RMS level in dB per 20 ms hop, for the pause detector

Needs Apple Silicon + `pip install -r scripts/uz_audio/requirements.txt`
(mlx-whisper). Already-done surahs are skipped unless --force. With --wait it
polls for mp3s that are still downloading (a file is ready once its size matches
the server's Content-Length).
"""

import argparse
import dataclasses
import os
import sys
import time
import urllib.request

import numpy as np

from scripts.uz_audio.common import (
    ENERGY_DIR,
    SOURCE_URL,
    TRANSCRIPT_DIR,
    decode_16k,
    mp3_path,
    probe,
    to_float,
    write_json,
)

# Full-precision turbo. The 4-bit "-q4" build uses less memory but moved the 1:3
# cut by 2 s (its word times are coarser), so it is only a fallback.
MODEL = os.environ.get("UZ_AUDIO_MODEL", "mlx-community/whisper-large-v3-turbo")
HOP = 320  # 20 ms at 16 kHz
SR = 16000
# Long surahs are transcribed in chunks: a 2.5 h file in one call exhausts an 8 GB
# M1 and macOS kills the process without a traceback. Each chunk ends inside the
# quietest stretch near the target length, so no word is split.
CHUNK_S = 600
CHUNK_SEARCH_S = 30


def remote_size(surah: int) -> int:
    req = urllib.request.Request(
        SOURCE_URL % surah, method="HEAD", headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return int(resp.headers["Content-Length"])


def energy_db(x: np.ndarray) -> np.ndarray:
    """RMS level per 20 ms hop, in dB of full scale, from int16 samples (in blocks,
    so a long surah never exists as one big float array)."""
    n = len(x) // HOP
    out = np.empty(n, dtype=np.float32)
    block = 50_000  # hops (~17 min)
    for i in range(0, n, block):
        j = min(n, i + block)
        frames = to_float(x[i * HOP : j * HOP]).reshape(j - i, HOP)
        out[i:j] = 20 * np.log10(np.sqrt((frames**2).mean(axis=1)) + 1e-9)
    return out


def chunk_bounds(energy: np.ndarray, total_s: float) -> list:
    """[(start_s, end_s), …] covering the audio, each cut at a quiet point."""
    hop_s = HOP / SR
    bounds, start = [], 0.0
    while total_s - start > CHUNK_S + CHUNK_SEARCH_S:
        lo = int((start + CHUNK_S - CHUNK_SEARCH_S) / hop_s)
        hi = int((start + CHUNK_S + CHUNK_SEARCH_S) / hop_s)
        # quietest 0.5 s window in the search range
        window = 25
        smooth = np.convolve(energy[lo:hi], np.ones(window) / window, mode="valid")
        cut = (lo + int(np.argmin(smooth)) + window // 2) * hop_s
        bounds.append((start, cut))
        start = cut
    bounds.append((start, total_s))
    return bounds


def transcribe(surah: int) -> None:
    import mlx_whisper

    path = mp3_path(surah)
    info = probe(path)
    audio = decode_16k(path)
    os.makedirs(ENERGY_DIR, exist_ok=True)
    energy = energy_db(audio)
    started = time.time()
    segments = []
    for a, b in chunk_bounds(energy, len(audio) / SR):
        result = mlx_whisper.transcribe(
            to_float(audio[int(a * SR) : int(b * SR)]),
            path_or_hf_repo=MODEL,
            language="uz",
            word_timestamps=True,
            condition_on_previous_text=False,  # stops one bad segment from snowballing
        )
        segments += [
            {
                "start": round(a + s["start"], 2),
                "end": round(a + s["end"], 2),
                "text": s["text"].strip(),
                "words": [
                    [round(a + w["start"], 2), round(a + w["end"], 2), w["word"].strip()]
                    for w in s.get("words", [])
                ],
            }
            for s in result["segments"]
        ]
        print("    %03d  chunk %.0f-%.0fs done" % (surah, a, b), flush=True)
    np.save(os.path.join(ENERGY_DIR, "%03d.npy" % surah), energy)
    del audio
    write_json(
        os.path.join(TRANSCRIPT_DIR, "%03d.json" % surah),
        {
            "surah": surah,
            "model": MODEL,
            "duration": info.duration,
            "mp3": dataclasses.asdict(info),  # lets export run without the mp3 (e.g. on Colab)
            "segments": segments,
        },
    )
    print(
        "%03d  %6.0fs audio  %5.0fs work  %d segments"
        % (surah, info.duration, time.time() - started, len(segments)),
        flush=True,
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("surahs", nargs="*", type=int, help="default: all 114")
    ap.add_argument("--force", action="store_true", help="redo surahs already transcribed")
    ap.add_argument("--wait", action="store_true", help="wait for mp3s still downloading")
    args = ap.parse_args()

    for surah in args.surahs or range(1, 115):
        out = os.path.join(TRANSCRIPT_DIR, "%03d.json" % surah)
        if os.path.exists(out) and not args.force:
            continue
        path = mp3_path(surah)
        if args.wait:
            expected = remote_size(surah)
            while not os.path.exists(path) or os.path.getsize(path) < expected:
                time.sleep(15)
        elif not os.path.exists(path):
            print("%03d  missing mp3 (run fetch first)" % surah, file=sys.stderr)
            continue
        try:
            transcribe(surah)
        except Exception as err:  # keep going: one bad file shouldn't stop the batch
            print("%03d  FAILED: %s" % (surah, err), file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
