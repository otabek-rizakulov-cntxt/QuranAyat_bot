#!/usr/bin/env python3
"""Re-encode the Muallimi soniy lessons for fast playback (docs/MAKHRAJ_3D_PLAN.md §9).

    python3 scripts/tajweed/encode_speech.py
    python3 scripts/tajweed/muallimi.py          # then refresh the manifest

The downloads (data/tajweed/downloads/, 192 kbps stereo, 134 MB) are narration, so
64 kbps mono CBR keeps them clear at about a third of the size: a phone buffers enough
to start playing about three times sooner. Output: data/tajweed/encoded/NNN.mp3
(gitignored), uploaded under the `v2/` key prefix by upload_r2.py so the old files,
cached as immutable, are never overwritten.

CBR with a Xing header, 44.1 kHz (MPEG-1 Layer III, which muallimi.py's frame walker
reads), no ID3 tags, so the bytes depend only on the audio. Light: one ffmpeg at a
time, ~50 MB RAM, a minute or two for all 73. Files already encoded are skipped.
The ffmpeg binary is $FFMPEG, else `ffmpeg` on the PATH.
"""

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOWNLOADS = os.path.join(ROOT, "data", "tajweed", "downloads")
ENCODED = os.path.join(ROOT, "data", "tajweed", "encoded")
BITRATE = "64k"


def encode(src: str, dst: str) -> None:
    tmp = dst + ".tmp.mp3"
    subprocess.run(
        [
            os.environ.get("FFMPEG") or "ffmpeg",
            "-nostdin",
            "-loglevel",
            "error",
            "-y",
            "-i",
            src,
            "-map",
            "0:a:0",
            "-map_metadata",
            "-1",
            "-ac",
            "1",
            "-ar",
            "44100",
            "-codec:a",
            "libmp3lame",
            "-b:a",
            BITRATE,
            "-write_xing",
            "1",
            "-id3v2_version",
            "0",
            "-write_id3v1",
            "0",
            tmp,
        ],
        check=True,
    )
    os.replace(tmp, dst)


def main() -> int:
    os.makedirs(ENCODED, exist_ok=True)
    done = 0
    for name in sorted(os.listdir(DOWNLOADS)):
        m = re.match(r"^(\d{3})_.+\.mp3$", name)
        if not m:
            continue
        dst = os.path.join(ENCODED, "%s.mp3" % m.group(1))
        if os.path.exists(dst):
            continue
        encode(os.path.join(DOWNLOADS, name), dst)
        done += 1
    before = sum(os.path.getsize(os.path.join(DOWNLOADS, f)) for f in os.listdir(DOWNLOADS))
    after = sum(os.path.getsize(os.path.join(ENCODED, f)) for f in os.listdir(ENCODED))
    print("%d encoded; %.1f MB -> %.1f MB in %s" % (done, before / 1e6, after / 1e6, ENCODED))
    return 0


if __name__ == "__main__":
    sys.exit(main())
