# Tajweed: next round (lesson text, lesson icons, reader colours, a better 3D model)

Status: **draft for the owner, 2026-11-23**. Nothing here is built yet. Follows
`TAJWEED_PLAN.md` (lessons, text tracking, practice) and `MAKHRAJ_3D_PLAN.md` (the 3D figure).

The owner's feedback this round:
- The text tracking misses lessons' Uzbek intros, and some lessons have no Arabic at all.
- The lesson list looks like empty checkboxes.
- The Quran reader should show tajweed colours, with a switch, linked to the lessons.
- The 3D figure should look better, made by us (no artist, no Blender).

## 1. Lesson text and timing

### 1.1 What is wrong (audit of `data/tajweed/muallimi_timings.json`)

The list in the app shows the foreword (ms-073) first, so **list position N is file
ms-(N−1)**. Lesson numbers aren't shown anywhere, which is how "55, 57, 61" were reported. §2
fixes that.

| Problem | Lessons (file ids) | Owner's report |
|---|---|---|
| No Arabic rows at all | 047–054, 058, 059, 060, 063, 066 (and 073, the foreword, which is fine) | "55 has no Arabic, only audio" = ms-054 Izhor; "61 has no Arabic" = ms-060 Tarqiqli ro |
| Letters spelled as Uzbek words instead of Arabic | ms-056 ("vov, nun, mim, yo") | "57: вов, нун, мим instead of و ن م" |
| Uzbek intro missing, the lesson starts on an Arabic row | 014, 024, 033, 037–040, 045, 046, 055, 062, 068–072 | "Fa harfi: first comes the Uzbek, then the Arabic; the timing misses it" = ms-014 |
| Rows with no timing (never highlighted) | 23 lessons, 1–7 rows each (worst: ms-062 with 7, ms-030 with 4) | |
| Text reconstructed from garbled transcripts | 013, 027, 029, 032, 035, 040, 059, 066, 073 | |
| Quran fragments in the examples not identified | ms-056/057 and the madd lessons | "57 had small parts of ayahs" |

**Root cause:**
- The Arabic rows were typed from the classic primer's exercises and matched to the audio by
  Whisper. Whisper hears Arabic badly in an Uzbek narration, so rows it couldn't place have no
  time.
- Where the primer's page wasn't known, the lesson got no Arabic at all.
- The lesson title the narrator reads first was sometimes merged into an Arabic row.

### 1.2 How to fix it

**Rule for every lesson:**
- It starts with an Uzbek row (the title the narrator reads).
- Uzbek and Arabic rows alternate in the order they're heard.
- Every row has a start time.

A test enforces this, so a broken lesson can't be exported again.

**Step 1: the Arabic text** (the authoritative source is the printed book).
- **A. The owner sends photos of the primer's pages** for the 14 lessons with no Arabic, and for
  ms-056 and ms-057. I type the rows from the photos (with harakat) and check each against the
  audio transcript. This is the most reliable option, and the owner only takes photos. *(Recommended.)*
- **B. Without the book,** I reconstruct the rows from the audio:
  - an Arabic speech-recognition pass on Colab's GPU (too heavy for this Mac);
  - Quran fragments looked up in `quran-uthmani.txt` by fuzzy match, so ayah pieces get the exact
    Uthmani spelling and a reference like "2:2".

  This is slower, and less certain for the drill words, which aren't Quran text.

**Step 2: the timing.** A reviewer-only **timing editor** in the Mini App (`?debug=1` on a
lesson):
- the lesson plays and the rows are listed;
- the reviewer taps "next row" as each one starts, with ±0.25 s nudges and a replay of the last 3
  seconds;
- **Save** sends the times to a reviewer-only endpoint, which stores them as an override on top of
  the generated file, like the makhraj clip edits.

That's about one listen per lesson, needs no heavy jobs, and the owner hears every result while
setting it. A script then folds the overrides back into `muallimi_timings.json` so they're in git.

**Step 3: verify.**
- The structure test (above).
- The owner marks each fixed lesson approved in the existing reviewer flow (`tj_draft`).
- Lessons stay visible while being fixed, since they're live already.

**Order of work:**
1. The 14 lessons with no Arabic, plus ms-056 and ms-057.
2. The 16 with missing intros. These are text-only edits: I add the missing title row, and the
   reviewer re-times it.
3. The 23 with untimed rows.
4. The 9 "unsure" ones.

## 2. Lesson icons in the list

The left badge is an empty circle until a lesson is done. It will instead show **what the lesson
is about**, in Arabic where possible, with a ✓ corner when done. The icons are generated from the
data, not drawn by hand:

| Lessons | Badge |
|---|---|
| Letters (ms-002…029) | The letter itself: ب, ت, ف … |
| Harakat, tanwin, sukun, shadda, madd (ms-030…053) | The mark on a dotted circle: ◌َ ◌ً ◌ْ ◌ّ ◌ٓ |
| Nun sakin rules (ms-054…058) | ن with the rule's colour from §3 (izhor, iqlob, idgʻom, ixfo) |
| Ro, Alloh, waqf and the rest | ر, ﷲ, a stop sign ۝, and so on |
| Foreword (ms-073) | A book icon |

The list also gets the lesson number in small grey text (`12`), so feedback like "lesson 55" maps
to one lesson. The owner chooses between the Arabic badge, the number in the badge, or both
(question 1, §6).

## 3. Tajweed colours in the Quran reader

**What the reader shows:**
- A switch, **Tajweed ranglari**, in the reader's settings sheet. Off by default; it's remembered.
- When on, the ayah text is drawn with each rule's span coloured. A small legend lists the colours.
- **Tapping a coloured span** opens a sheet with:
  - the rule's name and a one-line explanation;
  - the ayah piece;
  - a button **Darsni ochish** (open the lesson), which goes to the lesson that teaches the rule
    (rule → lesson, below).

**"Uzbek only":** the lessons exist only in Uzbek (Latin and Cyrillic), so:
- the link button shows for `uz` and `uz-Cyrl` only;
- the colours and legend show for everyone, *or* for Uzbek only (question 3).

**Data:**
- The colours come from `data/tajweed.json` (cpfair/quran-tajweed, CC BY 4.0, already in the repo).
  It indexes the **Uthmani** text (`quran-uthmani.txt`), but the reader shows `ar.txt`, which has a
  different spelling, so the indexes don't line up.
- **Fix:** with colours on, the reader shows the Uthmani text for that surah.
  `export_web_content.py` writes `public/content/tajweed/text/NNN.json` per surah (ayah text plus
  rule spans, about 5 MB in total, loaded lazily one surah at a time).
- **Credit:** the licence requires a line in the About page.

**Rule → lesson map:** built from the rules track's `rules` and the audio track's map
(`tajweed_practice.rules_for`):

| Rule(s) | Lesson |
|---|---|
| ghunna | ms-056 |
| iqlab | ms-055 |
| idgʻom with / without ghunna | ms-056 / ms-057 |
| ixfo | ms-058 |
| lam shamsiyya | ms-042 |
| hamzat wasl | ms-044 |
| madd | ms-047…053 |
| qalqala | the rules-track lesson |

A test checks that every rule maps to a lesson that exists.

**Mushaf page view:** the same switch later. It's skipped in the first version because its line
layout uses the printed page's glyphs.

**Bot:** Telegram can't colour text, so there's no change in chat. The existing marked examples
stay.

## 4. A better 3D head, made by us

There's no artist or Blender, and no buying. The figure stays procedural, but it moves from
outlines swept in the browser to a **sculpted mesh generated by a script** and shipped as a small
GLB file. The tongue, jaw, lips and velum keep their live rig, because the poses drive them.

1. **Shapes as signed-distance fields (SDFs):** smooth blends of simple solids. This is how
   procedural sculpting works without a sculpting tool:
   - the skull and face from the existing profiles;
   - cheeks, nose and ears;
   - teeth with crowns and roots;
   - the gums and the palate's ridges (rugae).
2. **A node script meshes the SDFs** (marching cubes, offline, one time), smooths them, and bakes
   ambient occlusion and a subtle skin and mucosa texture into vertex colours. It's exported with
   three.js's GLTFExporter, Draco-compressed, at about 300–600 KB.
   - Runs on the Mac in minutes at about 500 MB RAM; within limits, but checked first.
3. **The viewer loads the GLB**, replacing the swept skin, teeth and palate, and keeps the current
   rig for the moving parts. The low tier keeps today's procedural figure as a fallback.
4. **Side-by-side screenshots for the owner** before it replaces anything, the same way the
   cutaway was chosen.

It stays a teaching figure. Fine detail like pores or veins isn't realistic to generate this way.

## 5. 3D smoothness (done on `feat/makhraj-polish`, to be tested on devices)

- **No orbit damping.** The head used to trail the finger by a few frames, which feels like lag
  even at 60 fps.
- **Quality drops last for the session only.** The automatic quality drop used to be stored for
  good, so one janky moment left a fast phone at 30 fps forever. Old stored drops are cleared.
- **A Quality button** (Auto / High / Medium / Low) under the figure.
- **An fps readout** on the figure with `?debug=1`. The owner tests on the iPhone 15 Pro Max and the
  XS and reports the numbers. If it still isn't smooth at 60 fps, the next suspects are the
  Telegram WebView's frame pacing and the page's own animations during a letter change.

## 6. Questions for the owner

1. **Lesson badges:** the Arabic letter or mark, the lesson number, or both?
2. **Primer pages:** can you photograph the pages for the 14 lessons with no Arabic, plus ms-056
   and ms-057? (§1.2 option A.)
3. **Reader colours:** for everyone, or Uzbek readers only? The lesson link is Uzbek only either way.
4. **Colours on by default** for Uzbek readers, or off until switched on?
5. **The 3D model (§4):** start now, or after the lesson text?
