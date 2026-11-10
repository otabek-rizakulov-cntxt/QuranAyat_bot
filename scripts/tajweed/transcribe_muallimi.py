"""Transcribe the 73 Muallimi soniy lessons with word timestamps (docs/TAJWEED_PLAN.md P2).

    python -m scripts.tajweed.transcribe_muallimi [N ...] [--force]

Runs on Colab (scripts/tajweed/colab_muallimi.ipynb), never on the Mac: Whisper
large-v3-turbo on a GPU. For each lesson it downloads the mp3 from the public URL
in data/tajweed/audio_list.txt (or TAJWEED_AUDIO_BASE_URL when R2 is live), then
writes into the cache (TAJWEED_CACHE, default ~/.cache/quranayat/muallimi):

    transcripts/NNN.json  Whisper segments + words, seconds from the file start
    energy/NNN.npy        RMS level in dB per 20 ms hop, for the pause detector

The audio stays on the machine's temporary disk; only these files come back.
Long lessons (30 is 11 min) are cut into ~10-minute chunks inside a pause, with
the same `chunk_bounds` as the Uzbek translation audio.
"""

import argparse
import json
import os
import re
import sys
import time

import numpy as np

from scripts.uz_audio.transcribe import chunk_bounds, energy_db

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUDIO_LIST = os.path.join(REPO, "data", "tajweed", "audio_list.txt")
CACHE = os.path.expanduser(os.environ.get("TAJWEED_CACHE", "~/.cache/quranayat/muallimi"))
MP3_DIR = os.path.join(CACHE, "mp3")
TRANSCRIPT_DIR = os.path.join(CACHE, "transcripts")
ENERGY_DIR = os.path.join(CACHE, "energy")
SR = 16000
MODEL = os.environ.get("TAJWEED_WHISPER_MODEL", "large-v3-turbo")
HEADERS = {"User-Agent": "Mozilla/5.0"}


def sources() -> dict:
    """Lesson number -> mp3 URL."""
    base = os.environ.get("TAJWEED_AUDIO_BASE_URL", "").strip()
    out = {}
    with open(AUDIO_LIST, encoding="utf-8") as fp:
        for line in fp:
            m = re.match(r"^(\d{3})\s+(\S+)$", line.strip())
            if m:
                n = int(m.group(1))
                out[n] = base.rstrip("/") + "/%03d.mp3" % n if base else m.group(2)
    return out


def fetch(n: int, url: str) -> str:
    import requests

    path = os.path.join(MP3_DIR, "%03d.mp3" % n)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path
    os.makedirs(MP3_DIR, exist_ok=True)
    for attempt in range(5):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=120)
            resp.raise_for_status()
            with open(path + ".part", "wb") as fp:
                fp.write(resp.content)
            os.replace(path + ".part", path)
            return path
        except requests.RequestException:
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("lesson %d: download failed" % n)


def decode_16k(path: str) -> np.ndarray:
    """Mono int16 at 16 kHz (PyAV). Lessons are at most ~11 min, so a list is fine;
    unlike the translation audio these files carry ID3 tags and padded frames."""
    import av

    parts = []
    with av.open(path) as container:
        resampler = av.AudioResampler(format="s16", layout="mono", rate=SR)
        for frame in container.decode(audio=0):
            parts += [c.to_ndarray().reshape(-1) for c in resampler.resample(frame)]
        parts += [c.to_ndarray().reshape(-1) for c in resampler.resample(None)]
    return np.concatenate(parts).astype(np.int16)


def transcribe(model, n: int, path: str) -> None:
    samples = decode_16k(path)
    energy = energy_db(samples)
    segments = []
    for a, b in chunk_bounds(energy, len(samples) / SR):
        chunk = samples[int(a * SR) : int(b * SR)].astype(np.float32) / 32768.0
        result, _ = model.transcribe(
            chunk,
            language="uz",
            word_timestamps=True,
            condition_on_previous_text=False,  # one bad segment must not snowball
            vad_filter=False,  # pauses are our signal; keep every one
        )
        segments += [
            {
                "start": round(a + s.start, 2),
                "end": round(a + s.end, 2),
                "text": s.text.strip(),
                "words": [
                    [round(a + w.start, 2), round(a + w.end, 2), w.word.strip()]
                    for w in (s.words or [])
                ],
            }
            for s in result
        ]
    os.makedirs(ENERGY_DIR, exist_ok=True)
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
    np.save(os.path.join(ENERGY_DIR, "%03d.npy" % n), energy)
    with open(os.path.join(TRANSCRIPT_DIR, "%03d.json" % n), "w", encoding="utf-8") as fp:
        json.dump(
            {
                "lesson": n,
                "model": MODEL,
                "duration": round(len(samples) / SR, 2),
                "segments": segments,
            },
            fp,
            ensure_ascii=False,
        )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("lessons", nargs="*", type=int, help="default: all 73")
    ap.add_argument("--force", action="store_true", help="redo lessons already transcribed")
    ap.add_argument("--device", default="cuda")
    args = ap.parse_args()

    from faster_whisper import WhisperModel

    model = WhisperModel(
        MODEL, device=args.device, compute_type="float16" if args.device == "cuda" else "int8"
    )
    urls = sources()
    failed = []
    for n in args.lessons or sorted(urls):
        out = os.path.join(TRANSCRIPT_DIR, "%03d.json" % n)
        if os.path.exists(out) and not args.force:
            continue
        started = time.time()
        try:
            transcribe(model, n, fetch(n, urls[n]))
            print("%03d done in %.0fs" % (n, time.time() - started), flush=True)
        except Exception as err:  # keep going: one bad file shouldn't stop the batch
            failed.append(n)
            print("%03d FAILED: %s" % (n, err), file=sys.stderr, flush=True)
    done = len([f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith(".json")])
    print("%d of %d lessons transcribed; failed: %s" % (done, len(urls), failed or "none"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
