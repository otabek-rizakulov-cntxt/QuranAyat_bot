# Makhraj: animated 3D tongue positions (tajweed P5): plan

> Status: **proposal, revised 2026-11-17** after the owner's second round of answers (§1). Every
> decision is made; nothing is built yet. This replaces the 2D SVG idea in [TAJWEED_PLAN.md](TAJWEED_PLAN.md) §7 and makes P5 (§14)
> concrete. It also takes in the owner's audio latency complaint (§9), which ships first on its
> own branch.

## 0. Goal

The Mini App shows **one letter at a time**, as its own 3D view:
- a 3D head that the user can turn **all the way round (360°)**;
- the head animates from rest into that letter's articulation: the tongue moves to its contact
  point, the lips and jaw take their shape, and the soft palate rises or lowers;
- the contact area glows, and the airflow is drawn up to the point where the sound is made;
- **◀ ▶** (or a swipe) goes to the previous or next letter in alphabet order, morphing from one
  pose to the next.

It must stay smooth on slow phones (§6) and must not make the app's audio any slower (§9).

## 1. Decisions

| # | Question | Decision | Status |
|---|---|---|---|
| D1 | Where the model comes from | **We create it ourselves**, rendered with three.js in the browser. The main model is **built in JS** (procedural). Our own Blender-made GLB is optional later, through the same rig (§4.1). No bought or third-party models. | ✅ owner, 2026-11-17 |
| D2 | View | **Full 360° rotation** (drag to orbit, pinch to zoom, double tap to reset). The skin is semi-transparent, so the tongue is visible from any angle (§4.3). | ✅ owner |
| D3 | Layout | **Letter by letter**: one letter per screen, with its own pose, text and navigation. The makhraj group is shown as a label. | ✅ owner |
| D4 | Rendering library | Plain **`three`** core + `OrbitControls` (+ `GLTFLoader` only if our own GLB is used), dynamically imported. No React bindings. | recommended |
| D5 | Sound | **The letter's own line from its Muallimi soniy lesson** (e.g. «قَ ـقِـ ـقُ»), cut from the lesson audio we already have using the P2 timings, with hand-set times where those are weak (§2.1). It plays in step with the animation. | ✅ owner |
| D6 | Bot | **Only a 🦷 Maxraj (3D) WebApp button** on the letter lessons. No images or videos in the chat. | ✅ owner |
| D7 | Visibility | **Testers first:** only the user ids in the existing reviewers setting see the screen until a release setting is switched on (§3). After that everyone sees it. | ✅ owner |
| D8 | Teacher review | **None for now.** No approval step and no content hash for the makhraj data. Teacher accounts (teachers registering and managing their students) are a future feature and will cover this then. | ✅ owner |
| D9 | Number of makhraj | **17** (jawf 1, throat 3, tongue 10, lips 2, nose 1), as the `maxraj-kirish` lesson already says. | recommended |

## 2. Letters, makhraj and poses

Letter by letter, in alphabet order: ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي (28),
then **madd** (ا و ي as long vowels, i.e. jawf) and **ghunna** (khayshum) as two extra screens:
30 screens in all. Each letter points to one of the 17 makhraj; letters that share a makhraj
share its pose, adjusted by the letter's own layers (heavy, rounded lips, nasal).

| # | Makhraj id | Region | Letters | Pose | Glow |
|---|---|---|---|---|---|
| 1 | `jawf` | jawf | madd ا و ي | Tongue at rest and low, mouth open, no contact point | The whole cavity, faintly |
| 2 | `halq-aqsa` | throat | ء ه | Constriction at the deepest part of the throat | Lower throat |
| 3 | `halq-wasat` | throat | ع ح | The tongue root draws back and narrows the middle of the pharynx | Middle throat |
| 4 | `halq-adna` | throat | غ خ | The back of the tongue rises towards the uvula | Upper throat and uvula |
| 5 | `lisan-aqsa` | tongue | ق | The farthest back of the tongue touches the soft palate | Soft palate, back |
| 6 | `lisan-aqsa-2` | tongue | ك | Like ق, a little forward and lower | Soft palate, front |
| 7 | `lisan-wasat` | tongue | ج ش ي | The middle of the tongue rises to the hard palate | Hard palate, middle |
| 8 | `hafa` | tongue | ض | One or both sides of the tongue touch the upper molars | Upper molars, side |
| 9 | `lam` | tongue | ل | The front edges of the tongue, up to the tip, touch the gums from the premolars to the incisors | Front gum ridge, wide |
| 10 | `nun` | tongue | ن | The tip, slightly below where ل touches | Gum ridge, one point |
| 11 | `ra` | tongue | ر | Close to ن; the tip and a little of the top of the tongue | Just behind the ن point |
| 12 | `nit` | tongue | ت د ط | The tip touches the roots of the upper front teeth | Roots of the upper incisors |
| 13 | `asala` | tongue | ص س ز | The tip is close to the front teeth, leaving a narrow whistling gap | The gap behind the incisors |
| 14 | `lisa` | tongue | ث ذ ظ | The tip touches the edges of the upper front teeth | Edges of the upper incisors |
| 15 | `shafa-fa` | lips | ف | The inner lower lip touches the edges of the upper front teeth | Lower lip and upper incisors |
| 16 | `shafatan` | lips | ب م و | ب and م: the lips close. و: the lips round and don't close | Both lips |
| 17 | `khayshum` | nose | ghunna | The soft palate lowers, the air goes through the nose, and the ن or م contact is held | Nasal cavity |

Letter layers on top of the makhraj pose:
- **`heavy`** (ص ض ط ظ غ خ ق): the back of the tongue also rises;
- **`round`** (و);
- **`nasal`** (م ن, slightly).

So ت, د and ط share a makhraj, but ط visibly differs.

### 2.1 The sound for each letter (D5)

Every letter lesson (`ms-002` to `ms-029`) opens with the letter and its three vowels, so the
clip is that lesson's **first timed Arabic row**: its start and end in the lesson MP3. The
player already plays a span of a file (`Track.start`/`end`), so no new audio files are needed.

- **Timings checked on 2026-11-17:**
  - 22 of the 28 letters have a clean first row of about 3–8 s.
  - **ن ف ش ط خ** have rows under 1.5 s (badly placed).
  - **غ**'s first timed row is a word row, not the letter.
  - Rows with confidence under 0.6 (ز ن ه ش ط خ ع د) should also be checked by ear.
- **Fix:** `makhraj.json` may set `"clip": [start, end]` for any letter, which overrides the
  timings. The debug panel (§4.5) has a player with nudge buttons (±0.1 s) to find it, and
  **Copy JSON**. A test fails if a letter's clip is shorter than 1.5 s or longer than 12 s.
- **Madd and ghunna screens:** a hand-set `clip` from lesson 30 (madd letters) and from the
  ghunna lesson.
- **No lesson audio:** when `audio_base` isn't set, the screen has no 🔊 and the animation still
  plays.
- **Sync:** the pose reaches its contact as the clip starts, holds while it plays (the hold
  stretches to the clip's length), and then returns to rest. Tapping 🔊 or switching letters
  plays it; nothing autoplays (iOS needs a tap).

### Pose data

```json
{
  "makhraj": [
    {
      "id": "lisan-aqsa", "region": "tongue", "name_uz": "Til orqasi va yumshoq tanglay",
      "body_uz": "…", "contact": "velum-back", "airflow": "oral",
      "pose": {
        "tongue": [[0.12, 0.30], [0.30, 0.42], [0.52, 0.58], [0.70, 0.66], [0.86, 0.52]],
        "tongue_side": 0, "jaw": 0.25, "lips_close": 0, "lips_round": 0.1,
        "lip_to_teeth": 0, "velum": 0, "pharynx": 0, "heavy": 0
      }
    }
  ],
  "letters": [
    { "letter": "ق", "name_uz": "Qof", "makhraj": "lisan-aqsa", "layers": { "heavy": 1 }, "lesson": "ms-015",
      "clip": null }
  ]
}
```

- **`tongue`:** five points along the tongue's midline, from tip to root.
- **Other controls:** all 0..1.
- **`airflow`:** `oral`, `nasal`, `hiss` or `none`.

The data says *where the tongue is*. It doesn't depend on which model draws it (§4.1).

## 3. Data and the bot side (single source)

| File | What |
|---|---|
| `data/tajweed/makhraj.json` (new) | The 17 makhraj and the 30 letter screens above, hand-written and reviewed in diffs. |
| `src/domain/tajweed_makhraj.py` (new) | Load and validate it; `for_letter()`; letter lesson ↔ letter (`ms-002`..`ms-029` via `tajweed_practice.LETTERS`); `clip(letter)` (the override, else the lesson's first timed Arabic row). |
| `src/config/settings.py` | A new non-secret **release flag** (off by default), plus `.env.example`. Off: only reviewers see the makhraj screen and its buttons. On: everyone does. |
| `src/services/tajweed.py`, `src/api/tajweed.py` | `makhraj_visible(user_id)` = flag on, or the user is a reviewer. `GET /tajweed` adds `makhraj: bool`, which the Mini App uses to show or hide the screen and its entry points. |
| `scripts/export_web_content.py` | Adds `makhraj` (with each letter's resolved clip) to `public/content/tajweed/{uz,uz-Cyrl}.json` (Cyrillic through `to_cyrillic`). |
| `src/bot/features/tajweed.py` | The 🦷 WebApp button on the letter lessons and the `maxraj-*` lessons → `…/learn/makhraj/<n>`, only when `makhraj_visible` and the Mini App URL is set. |
| `locales/*` | `tj_makhraj_*` keys. |

## 4. The 3D figure (Mini App)

### 4.1 One rig interface, two possible models

```ts
interface MakhrajRig {
  root: THREE.Object3D;                 // added to the scene
  apply(pose: Pose): void;              // set the tongue, lips, jaw, velum and pharynx; cheap enough to run every frame
  zone(id: ContactId): THREE.Vector3;   // where to put the glow and end the airflow
  dispose(): void;
}
```

Everything else (the poses, the animation, the sound, the screens and the tuning panel) talks
only to this interface.

- **`ProceduralRig` (JS), the one we build first and ship:**
  - Each organ's midline outline (palate, soft palate, teeth, lips, jaw, pharynx, nasal cavity,
    larynx) is defined as control points and extruded with a bevel. The head shell is a loft
    surface.
  - The tongue is a mesh lofted along a Catmull-Rom curve through the 5 pose points, with an
    elliptical cross-section; `tongue_side` lifts the edges. Its vertex buffer is updated in
    place.
  - The outlines are drawn by us from general anatomy knowledge (nothing traced from Noqta or
    any other source), so the whole model is ours. It loads no extra files. It looks clean and
    diagram-like.
- **`GltfRig`, optional later:**
  - Our own model made in Blender, with morph targets (shape keys) for the tongue, jaw, lips and
    velum, mapped to the same pose controls through a small `models/<name>.map.json`.
  - Only if the procedural look isn't good enough after P5c. Same budget: under 30k triangles,
    ≤ 1.5 MB GLB after `gltf-transform optimize` (meshopt + quantization).

### 4.2 Animation

`pose.ts` holds a pure `lerpPose(a, b, t)` with easing. Opening a letter goes:

1. rest → pose (350 ms);
2. hold for 900 ms while the glow pulses and the airflow runs;
3. back to rest (300 ms);
4. loop, or **⏸** to hold the pose.

- **Speed:** 1× or **🐢 0.5×**.
- **◀ ▶:** morphs directly from the current pose.
- **Reduced motion** (`prefers-reduced-motion`): jumps to the pose, with no loop and no
  particles.

### 4.3 360° viewing

- **Controls:** `OrbitControls` with no angle limits, damping on, zoom clamped (so you can't fly
  inside or lose the head), panning off, and double tap to reset to the side view.
- **Skin:** a semi-transparent shell (Fresnel-style edge shading, so the outline stays readable).
  The tongue, teeth, palate and airway are opaque inside it, so the articulation is visible from
  the front, the side and the back without a cut that only works from one side.
- **"Kesim" (cut) toggle:** a clipping plane at the midline for the textbook side view.
- **Touch:** dragging the canvas orbits; only a swipe *outside* the canvas (on the letter strip)
  changes letters. `touch-action: none` applies on the canvas only, so the page still scrolls
  and Telegram's swipe-to-close isn't hijacked. When the screen opens it calls the existing
  Telegram SDK's `disableVerticalSwipes()` and restores it on leaving.

### 4.4 The screen: `app/learn/makhraj/[n]/page.tsx`

- **Top:** the canvas, square and `width: 100%`, with a fixed aspect-ratio box before the chunk
  loads (no layout shift and no horizontal overflow: see the iPhone XS report).
- **Under it:**
  - the letter, large, with its name (Qof);
  - the makhraj label (*Til orqasi va yumshoq tanglay*, "the back of the tongue and the soft
    palate");
  - two or three lines of text;
  - ▶/⏸, 🐢, Kesim, and a ↺ button that resets the view.
- **Bottom:**
  - ◀ ▶ and a scrollable strip of the 30 letters to jump to any of them;
  - 🔊 plays the letter's Muallimi line (§2.1) in step with the animation, and a "🎧 Dars"
    (lesson) link opens the full lesson.
- **Entry points:** a "Maxrajlar" card on the Learn hub (opens ا), a 🦷 button on letter lessons
  2–29 and the `maxraj-*` lessons, and deep links from the bot. All are hidden unless
  `GET /tajweed` says `makhraj: true` (D7).
- **Rendering on one canvas:** one WebGL context for the whole screen, reused when the letter
  changes. Only the pose changes; nothing is rebuilt.

### 4.5 Pose-tuning panel (reviewer + `?debug=1` only)

- **Controls:** sliders for every control and drag handles on the tongue points; for the
  sound, the clip's start and end with ±0.1 s nudges and a replay button.
- **Copy JSON:** puts the pose on the clipboard for `makhraj.json`.
- **Loading:** lazy and never loaded for normal users.

## 5. Loading strategy

- **Code:** `three` and the rig load only on the makhraj screen, through
  `next/dynamic({ ssr: false })`. The JS budget is ≤ 180 KB gz, and no other page grows.
- **Model (GltfRig only):**
  - served from the app's own static files (`public/models/`, CDN-cached, immutable hash name);
  - prefetched while the user is on a letter lesson page;
  - stays cached between letters.

The screen shows the letter and its text **immediately**, then the 3D view when it's ready;
it's never a blank wait.

## 6. Slow devices: quality tiers

The tier is picked once per device and stored in `localStorage`. It can be overridden in the
screen's ⋯ menu.

| Tier | Detected by | Settings |
|---|---|---|
| **High** | WebGL 2, `hardwareConcurrency ≥ 6`, and a 1 s warm-up averaging under 12 ms per frame | DPR ≤ 2, antialias via MSAA, airflow particles, 60 fps |
| **Medium** | WebGL 2, warm-up under 25 ms per frame | DPR 1.5, no MSAA (FXAA off as well), simplified airflow (a tube instead of particles), 60 fps cap |
| **Low** | WebGL 1 only, `deviceMemory ≤ 2`, or a warm-up over 25 ms | DPR 1, half the tongue segments, no particles, an opaque skin with the cut on by default (no transparency sorting), 30 fps cap |
| **None** | No WebGL, or context creation fails or is lost twice | No canvas: the letter, its text and a 2D still (`public/makhraj/<id>.webp`, rendered once from the same rig, §11) |

These apply to every tier:
- **Render on demand:** frames are drawn only while animating or orbiting, never when idle.
- **Pausing:** stops when the tab is hidden (`visibilitychange`) and when the canvas scrolls
  out of view (`IntersectionObserver`).
- **Cleanup:** disposes everything on unmount and handles `webglcontextlost`.
- **Downgrading:** a running frame-time monitor drops one tier (it never goes back up within a
  session) if 30 frames in a row take over 33 ms.
- **Targets:** smooth on an iPhone XS (A12) and on a ~2019 budget Android (Mali-G52 class).

## 7. Correctness

- **Wording:** the text is split from the existing `maxraj-*` lessons and written fresh in plain
  Uzbek.
- **Checking:** there's no teacher approval for now (D8). The owner and the testers check all 30
  screens while the release flag is off (D7) and turn it on when satisfied.
- **Points to look at closely:** ض with one side of the tongue or both; ي and و as madd versus
  not madd; how ghunna is shown. These are kept as `note` fields in the JSON, ready for the
  future teacher accounts.

## 8. Testing

- **pytest:**
  - each of the 28 letters maps to exactly one makhraj, and the region counts are 1/3/10/2/1;
  - poses are complete and within range, with 5 tongue points;
  - every `contact` and `airflow` value is known;
  - Cyrillic covers every text, and the export contains `makhraj`;
  - every letter has a clip of 1.5–12 s inside its lesson's duration;
  - visibility: flag off means reviewers only, flag on means everyone (API, bot button);
  - the bot button shows on the right lessons only.
- **Mini App:**
  - `typecheck` and `lint`;
  - tests for `lerpPose`, the tongue builder (stable vertex count, no NaN) and tier selection;
  - the 375 px overflow harness on `/learn/makhraj/*`.
- **Manual:**
  - all 30 screens in light and dark mode, each with its sound in step;
  - 360° drag and the cut toggle;
  - reduced motion;
  - WebGL off (tier None);
  - forcing Low;
  - Telegram on an iPhone XS and on a budget Android: frame rate, no horizontal scroll, and
    Telegram's swipe still works outside the canvas.

## 9. Audio playback latency (first, its own branch: `fix/audio-latency`)

**The complaint:** pressing play sometimes takes **2–5 s** before sound.

**What we know (2026-11-17):**
- **Ayah audio** comes from everyayah.com behind BunnyCDN. It's cached (`max-age` ≈ 300 days)
  and supports ranges, and its first byte arrives in about 0.4 s from here. The edge seen was in
  Germany, so it could be slower from Uzbekistan.
- **Tajweed lesson audio** is on the R2 bucket's `r2.dev` URL. Cloudflare rate-limits that URL,
  doesn't cache it at the edge, and documents it as not meant for production. The files are
  192 kbps MP3s, up to 15.6 MB.
- **The player** (`lib/audio/player.tsx`) uses one `<audio>` element:
  - it sets `src` and calls `play()` at once, with no "loading" state shown;
  - preloading the next track uses a separate throwaway `new Audio()`, and iOS WebKit doesn't
    reliably share that buffer with the playing element, so the preload is often wasted;
  - nothing starts connecting to the audio host before the first tap;
  - several screens build their URL from `reciters.data`, which is an API call, so a tap before
    it returns does nothing until it does.

**Plan, measured first:**

1. **Measure.** Add a small timer in the player: tap → `playing`, with the host, whether the
   file was cached (`performance.getEntriesByName`), the device and the network type. Send it as
   a single beacon to a new `POST /api/v1/metrics/audio` (aggregated per host and phone model,
   no personal data). Collect for a few days to get real p50 and p95 numbers per host.
2. **Lesson audio:**
   - move it from `r2.dev` to a **custom domain on R2** with a Cache Rule (edge cached, immutable).
     The owner has a domain (2026-11-17). The owner's steps, done in Cloudflare:
     1. the domain's DNS is on Cloudflare;
     2. R2 → the bucket → Settings → Custom Domains → add a subdomain (for example `audio.`);
     3. Caching → Cache Rules → cache everything on that host, edge TTL 1 year;
     4. set the lesson audio base URL on Koyeb to the new host, and turn `r2.dev` access off.

     The code needs no change for this, since the base URL is already a setting.
   - **re-encode** the narration to **64 kbps mono** CBR MP3 (speech: about a third of the size,
     so it buffers about 3× faster). That's 73 files and about 92 min, a light ffmpeg job
     (seconds per file, under 200 MB RAM), checked against `vm.swapusage` first;
   - re-upload with `upload_r2.py` (new sha256 values, the same keys under a `v2/` prefix);
   - P2 timings stay valid because the duration doesn't change, and we verify that with
     `--verify`.
3. **Player:**
   - **double-buffer:** two `<audio>` elements. The next track is loaded (`load()`) in the idle
     one, and `next` swaps them, so a preload actually gets used, including on iOS;
   - **a loading state:** a spinner from `waiting`/`loadstart` until `playing`, so a slow start
     at least shows something;
   - **warm-up:** `<link rel="preconnect">` to the audio hosts in the root layout, and on
     screens with audio, `preload="metadata"` of the first likely track (the lesson's file, the
     first ayah of the open surah) when the page opens, before the tap;
   - **no wait on the API:** the reciter list and the audio base are cached (`localStorage` with
     revalidate), so the URL is known at once on the next visit.
4. **Ayah audio, only if the numbers say so:** if everyayah's p95 from users is still high,
   mirror the default reciters' files into R2 behind the custom domain, and point
   `AUDIO_BASE_URL` at it (the URL layout stays the same). For one reciter that's about 6,236
   files and roughly 0.5–1 GB, done as a remote job, not on this Mac.
5. **Re-measure** with the beacon, aiming for a p95 tap → sound under 1 s on 4G.

Steps 1–3 are code plus a one-off re-encode; step 4 is optional. This branch ships before P5, and
P5's screen uses the same player.

## 10. Phases

| Step | Branch | Deliverable |
|---|---|---|
| **A0** | `fix/audio-latency` (both repos) | §9 steps 1–3: the beacon, the double-buffered player, the loading state, preconnect and preload, the cached reciter list; the 64 kbps re-encode; the owner moves the lesson audio to the custom domain. |
| **P5a: data** | `feat/tajweed-makhraj` | `makhraj.json` (poses as first drafts), clip resolution, the domain module, export, the release flag and `makhraj` in `GET /tajweed`, locales, tests. |
| **P5b: the figure** | ″ | The rig interface and `ProceduralRig`; `lerpPose`, the animation synced to the clip, glow and airflow; quality tiers; the WebGL fallback. |
| **P5c: screens** | ″ | `/learn/makhraj/[n]` letter by letter, 360° controls, the cut toggle, the letter strip, 🔊, the entry points behind the flag, the debug panel (poses and clips). |
| **P5d: bot** | ″ | The 🦷 WebApp button. |
| **P5e: tuning** | ″ | Tuning the 30 poses and the 6+ weak clips, tests on the iPhone XS and a budget Android, the 2D stills for tier None; then the owner turns the flag on. |

## 11. Machine and cost notes

- **Light (fine on this Mac):** the 64 kbps re-encode (73 files, one at a time).
- **Tier-None stills:** 30 headless-browser screenshots of the same rig. That's light, about
  500 MB of RAM for a minute, checked against swap first.
- **Remote, not here:** any ayah mirroring (GBs).
- **Mini App `next build`:** check `vm.swapusage` before running it, as before.

## 12. Later

- Teacher accounts (teachers register and manage their students) will take over checking and
  approving this content.
- Our own Blender GLB (`GltfRig`) if the procedural look needs more realism.
- Storing learners' own recordings: not now (owner, 2026-11-17).
- Sifat (the letters' qualities) as layers on the same rig.
- The figure on the back of the `L:<letter>` spaced-repetition cards.

## 13. Owner's answers (2026-11-17)

| Question | Answer |
|---|---|
| Sound | The letter's Muallimi line (D5, §2.1). |
| Images in the bot | None; only the WebApp button (D6). |
| Visibility | Testers first, then a release setting turns it on for everyone (D7). |
| Teacher review | Skipped for now; future teacher accounts will cover it (D8). |
| Learners' audio | Not stored now; maybe in the future. |
| R2 custom domain | Yes, the owner has a domain (§9). |
| 3D models | Created by us, not bought (D1). |

Nothing is open. The next step is A0 (`fix/audio-latency`), then P5a.
