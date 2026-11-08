"""Shared bits of the Uzbek translation audio timing tool (docs/MULTILINGUAL_PLAN.md §8.1).

Offline only: this runs on a laptop or Colab, never on the server. The mp3s are
downloaded into a local cache outside the repo and never committed; the only
output that enters the repo is data/uz_audio_timings.json.
"""

import json
import os
from dataclasses import dataclass

SOURCE_URL = "https://newbooks.uz/audio/t1/%03d.mp3"
PAGE_URL = "https://newbooks.uz/ms.php?t=%03d"

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TIMINGS_PATH = os.path.join(REPO, "data", "uz_audio_timings.json")
OVERRIDES_PATH = os.path.join(REPO, "data", "uz_audio_overrides.json")
REFERENCE_PATH = os.path.join(REPO, "data", "translations", "uz.txt")

CACHE = os.path.expanduser(os.environ.get("UZ_AUDIO_CACHE", "~/.cache/quranayat/uz_audio"))
MP3_DIR = os.path.join(CACHE, "mp3")
TRANSCRIPT_DIR = os.path.join(CACHE, "transcripts")
ENERGY_DIR = os.path.join(CACHE, "energy")

# MPEG-1 Layer III tables (the only kind newbooks.uz serves).
_BITRATES = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320]
_SAMPLE_RATES = [44100, 48000, 32000]
SAMPLES_PER_FRAME = 1152

AYAH_COUNTS = [
    7,
    286,
    200,
    176,
    120,
    165,
    206,
    75,
    129,
    109,
    123,
    111,
    43,
    52,
    99,
    128,
    111,
    110,
    98,
    135,
    112,
    78,
    118,
    64,
    77,
    227,
    93,
    88,
    69,
    60,
    34,
    30,
    73,
    54,
    45,
    83,
    182,
    88,
    75,
    85,
    54,
    53,
    89,
    59,
    37,
    35,
    38,
    29,
    18,
    45,
    60,
    49,
    62,
    55,
    78,
    96,
    29,
    22,
    24,
    13,
    14,
    11,
    11,
    18,
    12,
    12,
    30,
    52,
    52,
    44,
    28,
    28,
    20,
    56,
    40,
    31,
    50,
    40,
    46,
    42,
    29,
    19,
    36,
    25,
    22,
    17,
    19,
    26,
    30,
    20,
    15,
    21,
    11,
    8,
    8,
    19,
    5,
    8,
    8,
    11,
    11,
    8,
    3,
    9,
    5,
    4,
    7,
    3,
    6,
    3,
    5,
    4,
    5,
    6,
]


def mp3_path(surah: int) -> str:
    return os.path.join(MP3_DIR, "%03d.mp3" % surah)


@dataclass
class Mp3Info:
    """What a newbooks.uz file looks like: constant bitrate, no padding, no tags.

    `frame_bytes` × frame index is the exact byte offset of that frame, which is
    the whole download formula (§8.1.1)."""

    kbps: int
    sample_rate: int
    frame_bytes: int
    frames: int
    size: int
    first_frame: int  # byte offset of the first frame header (0 for every file so far)

    @property
    def frame_seconds(self) -> float:
        return SAMPLES_PER_FRAME / self.sample_rate

    @property
    def duration(self) -> float:
        return self.frames * self.frame_seconds


def probe(path: str) -> Mp3Info:
    """Walk every frame header and prove the file is constant-bitrate without padding.

    Raises ValueError on anything else, because the byte formula would then be
    wrong for that surah."""
    with open(path, "rb") as fp:
        data = fp.read()
    i, first, frames, shape = 0, None, 0, None
    while i < len(data) - 4:
        if data[i] == 0xFF and (data[i + 1] & 0xFE) == 0xFA:
            b, s, pad = data[i + 2] >> 4, (data[i + 2] >> 2) & 3, (data[i + 2] >> 1) & 1
            if 0 < b < 15 and s < 3:
                size = 144 * _BITRATES[b] * 1000 // _SAMPLE_RATES[s] + pad
                if first is None:
                    first, shape = i, (b, s, pad)
                elif (b, s, pad) != shape:
                    raise ValueError("%s: frame %d differs from the first frame" % (path, frames))
                frames += 1
                i += size
                continue
        if first is not None:
            raise ValueError("%s: lost frame sync at byte %d" % (path, i))
        i += 1
    if first is None:
        raise ValueError("%s: no MPEG audio frames" % path)
    b, s, pad = shape
    return Mp3Info(
        kbps=_BITRATES[b],
        sample_rate=_SAMPLE_RATES[s],
        frame_bytes=144 * _BITRATES[b] * 1000 // _SAMPLE_RATES[s] + pad,
        frames=frames,
        size=len(data),
        first_frame=first,
    )


def decode_16k(path: str):
    """The mp3 as mono int16 at 16 kHz, the rate Whisper expects (PyAV, no ffmpeg CLI).

    int16 into a pre-sized array: al-Baqarah (2 h 33 m) is ~290 MB this way, where
    decoding to a list of float chunks and concatenating peaked near 2 GB and got
    the process killed on an 8 GB machine. Callers convert one chunk at a time."""
    import av
    import numpy as np

    info = probe(path)
    out = np.zeros(int(info.duration * 16000) + 16000, dtype=np.int16)
    n = 0
    with av.open(path) as container:
        resampler = av.AudioResampler(format="s16", layout="mono", rate=16000)
        frames = container.decode(audio=0)
        for frame in frames:
            for chunk in resampler.resample(frame):
                data = chunk.to_ndarray().reshape(-1)
                out[n : n + len(data)] = data[: len(out) - n]
                n += len(data)
        for chunk in resampler.resample(None):
            data = chunk.to_ndarray().reshape(-1)
            out[n : n + len(data)] = data[: len(out) - n]
            n += len(data)
    return out[: min(n, len(out))]


def to_float(samples):
    """int16 samples -> float32 in [-1, 1), the form Whisper takes."""
    import numpy as np

    return samples.astype(np.float32) / 32768.0


def load_reference() -> dict:
    """The bundled Uzbek Latin translation, `{(surah, ayah): text}`."""
    ref = {}
    with open(REFERENCE_PATH, encoding="utf-8") as fp:
        for line in fp:
            parts = line.rstrip("\n").split("|", 2)
            if len(parts) == 3 and parts[0].isdigit():
                ref[(int(parts[0]), int(parts[1]))] = parts[2]
    return ref


def read_json(path: str, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as fp:
        return json.load(fp)


def write_json(path: str, data, **kwargs) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, **kwargs)
        fp.write("\n")
    os.replace(tmp, path)
