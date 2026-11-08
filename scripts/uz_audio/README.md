# Uzbek translation audio — timing tool

Produces `data/uz_audio_timings.json`: where every ayah starts and ends inside the
newbooks.uz surah mp3s (`https://newbooks.uz/audio/t1/NNN.mp3`), so the bot and
the Mini App can play or send any single ayah or range. Design and decisions:
`docs/MULTILINGUAL_PLAN.md` §8.1.

Runs **offline on a Mac with Apple Silicon**, never on the server. The mp3s are
cached in `~/.cache/quranayat/uz_audio/` (override with `UZ_AUDIO_CACHE`) and are
never committed. Only the timing table and the overrides file enter the repo.

## Setup (once)

```bash
uv venv ~/.venvs/uz-audio && uv pip install --python ~/.venvs/uz-audio/bin/python \
    -r scripts/uz_audio/requirements.txt
alias uzpy=~/.venvs/uz-audio/bin/python      # run every command below from the repo root
```

Whisper large-v3-turbo needs about 3 GB free RAM. On an 8 GB Mac, close the
browser and other heavy apps first. Under memory pressure macOS kills the
process without a traceback, and it just disappears.

## Transcribing on Colab (preferred)

Transcribing 33.8 h of audio is too heavy for an 8 GB Mac: it swaps and gets killed. So run stage 1
on a free Colab GPU with `scripts/uz_audio/colab_transcribe.ipynb`:

1. Open colab.research.google.com → *File → Upload notebook* and pick the `.ipynb` (or open it from
   GitHub once the branch is pushed).
2. Set *Runtime → Change runtime type → T4 GPU*, then *Run all*.
3. Section 4 compares large-v3, large-v3-turbo (the default, best on timing) and an Uzbek fine-tune on the approved al-Baqarah
   cuts. Set `MODEL` to the winner, then run sections 5–7.
4. Colab downloads the mp3s itself (to its temporary disk, never Drive). Results are saved to
   `MyDrive/quranayat_uz_audio/` after every surah, so after a disconnect you just *Run all* again.
5. Section 7 downloads `uz_audio_colab.zip` (a few MB). On the Mac:

```bash
unzip -o ~/Downloads/uz_audio_colab.zip -d ~/.cache/quranayat/uz_audio
python3 -m scripts.uz_audio.align && python3 -m scripts.uz_audio.export   # seconds, low memory
```

Align was tuned on large-v3-turbo output. After switching models, check that `debug show 2:284`
still matches the approved cuts (the CI test `test_baqarah_matches_the_cuts_approved_by_ear` does
this too).

## Pipeline

```bash
# 0. fetch: 114 files, ~1.6 GB, resumable
mkdir -p ~/.cache/quranayat/uz_audio/mp3 && cd ~/.cache/quranayat/uz_audio/mp3 && \
  for n in $(seq -f %03g 1 114); do curl -s -C - -o $n.mp3 https://newbooks.uz/audio/t1/$n.mp3; done; cd -

uzpy -m scripts.uz_audio.transcribe        # 1. ~5 h for all 33.8 h of audio; skips done surahs
uzpy -m scripts.uz_audio.align             # 2. seconds; re-run freely
uzpy -m scripts.uz_audio.export            # 3. writes data/uz_audio_timings.json
venv/bin/python -m pytest tests/test_uz_audio_timings.py
```

- `transcribe S…` / `align S…` take surah numbers, and `--force` redoes a transcript.
- `export` prints every surah's status and low-confidence count, plus any hard problem (prefixed `!`).

## Format and the download formula

Every file is constant-bitrate MPEG-1 Layer III at 32 kHz, but the bitrate
differs per file (Fatiha 320, 21 surahs 128, the rest 96 kbps). One frame is
1152 samples (36 ms) and `4.5 × kbps` bytes. The table stores frame indices:

```
ayah a            = ayahs[a-1] = [start_frame, end_frame, confidence]   (end exclusive)
bytes for a..b    = Range: bytes=<ayahs[a-1][0] * frame_bytes>-<ayahs[b-1][1] * frame_bytes - 1>
seconds           = frame * 1152 / sample_rate
```

Example: 2:284 is `bytes=108409104-108808703`, which is 9034.1–9067.4 s.

## Fixing a wrong timing

```bash
uzpy -m scripts.uz_audio.debug report            # every surah: status, weakest boundary
uzpy -m scripts.uz_audio.debug report 2          # al-Baqarah's 30 weakest boundaries
uzpy -m scripts.uz_audio.debug show 2:255        # times, bytes, heard text vs reference, words and pauses at each cut
uzpy -m scripts.uz_audio.debug clip 2:255 --pad 3   # audio-samples/2-255_pad3.mp3 with 3 s of context
uzpy -m scripts.uz_audio.debug clip 2:255 --server  # exactly what the bot sends (Range from newbooks.uz)
uzpy -m scripts.uz_audio.debug set 2:255 start 1234.5   # or: nudge 2:255 end -0.4
uzpy -m scripts.uz_audio.align 2 && uzpy -m scripts.uz_audio.export
uzpy -m scripts.uz_audio.debug verify 2 "listened 2:1-20, 2:250-286"   # marks the surah verified
```

- Overrides live in `data/uz_audio_overrides.json`, in seconds. They act as hard pins when aligning, so the ayahs around a fix re-fit to it.
- If a whole stretch is shifted, fix the first wrong boundary. One missed cut usually explains everything after it.
- Clips are cached in Telegram under keys that include the surah's timing version. A re-export therefore makes the bot cut fresh clips by itself (`debug purge` lists the stale keys).
- `debug smoke` checks against the live server that every surah still has the same size and that boundaries land on MPEG frames. Run it if users report garbled audio: it means the upstream file changed and the surah needs re-timing.
- `audio-samples/` is excluded locally via `.git/info/exclude`; never commit audio.
