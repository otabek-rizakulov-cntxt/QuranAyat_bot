# Hifz Platform — Plan & Progress

> Turning BismillahBot from a Qur'an **reader** into a Qur'an **memorization
> companion**: a user commits to a target (Al-Mulk, a juz, a range), the bot
> pushes a daily portion, tests recall, tracks what they have memorized as a
> percentage, and rewards consistency with streaks and leaderboards — privately
> in DM, and as a study circle in a supergroup topic.

**Status:** spec confirmed, implementation not started
**Last updated:** 2026-07-31

---

## 0. How to use this document

This is the single source of truth for the seven-feature hifz workstream. It is
both the **spec** (what to build and why) and the **tracker** (what is done).

- Every task carries a checkbox, an owner-facing description of *what should be
  done*, the **files it touches**, and a **done-when** line that is falsifiable.
- Update the checkbox and the status table in §3 as work lands. Do not delete
  completed items — this doubles as the build log.
- If a decision changes mid-build, amend §2 (Decisions) and note it in §9
  (Change log) rather than silently editing the task.
- Anything discovered that contradicts the spec is a **stop-and-ask**, not an
  improvisation.

---

## 1. Scope

Seven features were requested. They split cleanly into two clusters, and the
group cluster is roughly as much work as the personal one because it requires
lifting a ban that is currently hard-coded.

| # | Feature | Phase |
|---|---------|-------|
| 1 | Registration without phone number; leaderboard opt-in + display name | 1 |
| 2 | Daily streaks + activity graph (Duolingo-style motivation) | 1 |
| 3 | Weekly leaderboard | 1 |
| 4 | Memorization plans, repeat drills, recall check, progress % | 1 |
| 5 | Bot posts to a configured supergroup **topic** | 2 |
| 6 | Group posts carry image + audio + translation | 2 |
| 7 | Admin schedules which ayahs on which days | 2 |

**Phase 1 (build now)** — items 1–4, DM only. Ships an end-to-end usable product
and builds the scheduler that Phase 2 depends on.

**Phase 2 (designed now, built next)** — items 5–7. The data model below already
accounts for it so Phase 1 does not paint us into a corner, but no Phase 2 code
is written until Phase 1 ships.

### Explicitly out of scope

Phone/OTP auth · voice-verified recitation or ASR · tajweed feedback · payments ·
web dashboard · rendered PNG contribution graph (emoji grid instead) · tafsir
inside plans · `/hizb` `/manzil` `/ruku` commands · more than one active plan per
user · per-day editing of a group plan in v1 · migrating existing user history
(there is none to migrate).

---

## 2. Decisions

These were settled during grilling. Changing one of them is a spec change, not an
implementation detail.

| Area | Decision | Why |
|---|---|---|
| **Sequencing** | Personal (1–4) first, then group (5–7) | Group work needs the scheduler Phase 1 builds; shipping something usable sooner |
| **Streak rule** | A day ticks when a **session is completed** — a drill run through, or a passed recall check | Cannot be farmed by typing `/help`; makes streaks and memorization reinforce each other |
| **Drill entry** | Bot pushes a daily plan **and** the user can start a drill on demand | Push creates the habit; manual start respects the user who wants something else today |
| **Leaderboard metric** | Sessions completed this week; streak length breaks ties | Bot-measured, so nothing self-reported can inflate it |
| **Leaderboard scope** | Global board in DM; group-scoped weekly result posted in the group (Phase 2) | Scores are earned in DM, celebrated in the circle |
| **Book learners** | Earn sessions through the **recall check** — the bot tests them | It tests hifz, not app usage, so someone memorizing from a physical mushaf is a first-class citizen |
| **Marking hifz** | `✅ I know this by heart` after a drill, stored as ayah **intervals** | Every percentage is derived arithmetic — no counter can drift |
| **Group topic capture** | Bot **creates** the topic itself via `createForumTopic` | Bots cannot list forum topics and a forward strips the thread id; creating it means we own the id with zero failure modes |
| **Group plan shape** | Admin picks range + pace + days; bot splits across days and previews a calendar | One decision instead of thirty |
| **Time model** | Timezone + reminder time asked once, at first plan setup | Streak day boundary and pushes must be local; UTC would break streaks at 05:00 for a UTC+5 audience |
| **Scheduler** | In-process asyncio loop over a Postgres due-queue | No second service on a 512 MB free tier, no external dependency, restart-safe |
| **i18n** | Full 48 languages, validated by `scripts/check_locales.py` | Preserves the "no locale falls back to English" property the README advertises |

### Assumptions (flagged — override if wrong)

1. **Activity graph is an emoji grid, not a rendered PNG.** Pillow is already a
   dependency, but per-user image rendering on a 512 MB instance that also
   stitches mushaf pages is a real memory risk. PNG is a later nice-to-have.
2. **No "top 2% of users" line until there is a real distribution.** With a small
   user base that number is meaningless or embarrassing. Fixed milestone copy
   (7 / 30 / 100 / 365 days) until ≥200 users have a streak, then the real
   percentile computed weekly.
3. **One active plan per user.** Multi-plan concurrency is a v2 concern.
4. **Group posts use one admin-chosen translation language**, not per-member — a
   group message can only be in one language.
5. **Recall-check distractors** are drawn from the same surah where possible,
   falling back to neighbouring ayahs, filtered to a similar length so option
   length is not a tell.
6. **`REDIS_HOST_URL` stays unset.** Nothing here depends on Redis; all new state
   is Postgres.

---

## 3. Progress at a glance

| Workstream | Tasks | Done | Status |
|---|---|---|---|
| A — Storage foundation | 4 | 0 | ⬜ not started |
| B — Profile & registration (item 1) | 3 | 0 | ⬜ not started |
| C — Hifz progress (item 4a) | 3 | 0 | ⬜ not started |
| D — Plans & drills (item 4b) | 5 | 0 | ⬜ not started |
| E — Recall check (item 4c) | 3 | 0 | ⬜ not started |
| F — Scheduler | 3 | 0 | ⬜ not started |
| G — Streaks & graph (item 2) | 3 | 0 | ⬜ not started |
| H — Leaderboard (item 3) | 2 | 0 | ⬜ not started |
| I — i18n & commands | 3 | 0 | ⬜ not started |
| J — Group cluster (items 5–7) | 6 | 0 | ⬜ Phase 2 |

Legend: ⬜ not started · 🟨 in progress · ✅ done · ⛔ blocked

---

## 4. Phase 1 — task breakdown

### Workstream A — Storage foundation

The existing `FakePostgresPool` (`src/config/postgres.py`) pattern-matches four
hard-coded query strings and raises `ValueError` on anything else. Phase 1 adds
roughly 25 query shapes. Growing that fake is untenable, so the abstraction moves
up a level: repositories, not faked SQL.

- [ ] **A1 — Introduce a repository layer.**
  Create `src/lib/store/` with one module per aggregate (`profiles.py`,
  `hifz.py`, `plans.py`, `sessions.py`, `schedule.py`). Each exposes async
  methods, never raw SQL, to callers. Provide two implementations behind the same
  interface: asyncpg-backed and in-memory.
  *Files:* `src/lib/store/*`, `src/config/postgres.py`
  *Done when:* no caller outside `src/lib/store/` contains a SQL string.

- [ ] **A2 — Retire the SQL-shaped fake.**
  Replace `FakePostgresPool` with the in-memory repository implementation, chosen
  when `DATABASE_URL` is unset — same dev/test convenience, no SQL pretence. Keep
  the existing startup warning.
  *Files:* `src/config/postgres.py`, `conftest.py`
  *Done when:* `pytest` passes with `DATABASE_URL` unset and no query-string
  matching remains.

- [ ] **A3 — Move `UserSettings` behind the repository.**
  Behaviour-preserving refactor: `src/lib/user_settings.py` keeps its public
  surface (`get`, `set_ui_lang`, `set_translation_lang`, `set_reciter`) including
  the legacy-Redis migration in `_ensure_row`.
  *Files:* `src/lib/user_settings.py`, `src/lib/store/profiles.py`
  *Done when:* `tests/test_user_settings.py` passes unmodified.

- [ ] **A4 — Extend the schema.**
  Append the new tables to `src/common/schema.sql`, still `CREATE TABLE IF NOT
  EXISTS`, still applied idempotently at boot from `_initialize()`. No migration
  framework — consistent with what is there.
  *Files:* `src/common/schema.sql`
  *Done when:* a fresh Postgres and an existing one both boot clean.

#### Data model

```
user_profile
  telegram_user_id   BIGINT PK
  display_name       TEXT NULL          -- @username, or user-supplied
  leaderboard_opt_in BOOLEAN  DEFAULT false
  timezone           TEXT NULL          -- IANA name or fixed UTC offset
  reminder_time      TIME NULL          -- local
  current_streak     INT DEFAULT 0      -- denormalized for cheap reads
  longest_streak     INT DEFAULT 0
  created_at, updated_at TIMESTAMPTZ

hifz_interval                            -- what the user knows by heart
  id BIGSERIAL PK
  user_id  BIGINT
  surah    INT
  start_ayah INT
  end_ayah   INT                         -- merged on insert; never overlapping
  marked_at TIMESTAMPTZ

plan                                     -- one active per user (assumption 3)
  id BIGSERIAL PK
  user_id BIGINT
  target_kind TEXT                       -- 'surah' | 'juz' | 'range'
  start_surah, start_ayah, end_surah, end_ayah INT
  pace INT                               -- ayahs per day (0 = auto)
  days_of_week SMALLINT[]                -- 1=Mon … 7=Sun
  status TEXT                            -- 'active' | 'paused' | 'complete'
  created_at TIMESTAMPTZ

plan_day                                 -- materialized daily portions
  id BIGSERIAL PK
  plan_id BIGINT
  scheduled_date DATE                    -- local to the user
  surah, start_ayah, end_ayah INT
  state TEXT                             -- 'pending' | 'sent' | 'completed'

session_log                              -- the streak & leaderboard substrate
  id BIGSERIAL PK
  user_id BIGINT
  local_date DATE                        -- user-local, decides the streak day
  kind TEXT                              -- 'drill' | 'recall_check'
  surah, start_ayah, end_ayah INT
  occurred_at TIMESTAMPTZ

scheduled_send                           -- the due-queue
  id BIGSERIAL PK
  kind TEXT                              -- 'plan_day' | 'weekly_board' | 'group_post'
  target_chat_id BIGINT
  thread_id INT NULL                     -- forum topic (Phase 2)
  due_at TIMESTAMPTZ
  payload JSONB
  state TEXT                             -- 'pending' | 'claimed' | 'sent' | 'failed'
  idempotency_key TEXT UNIQUE            -- (kind, target, local_date)
  claimed_at TIMESTAMPTZ NULL

-- Phase 2
group_config      chat_id PK, thread_id, admin_user_id, translation_lang,
                  reciter, timezone, post_time, days_of_week, content_flags, status
group_plan        same shape as `plan`, keyed by chat_id
group_plan_day    same shape as `plan_day`
group_member_link user_id, chat_id, linked_at   -- consent to appear on that board
```

---

### Workstream B — Profile & registration (item 1)

No phone number is involved anywhere, and none is being added. Registration
already happens implicitly: `UserSettings._ensure_row` creates a row keyed on
`telegram_user_id` at first contact. What is new is **identity for the
leaderboard**.

- [ ] **B1 — `/profile` command.**
  Shows display name, leaderboard status, timezone, reminder time, current plan.
  Inline buttons to change each.
  *Files:* `src/main.py`, `src/locales/*`
  *Done when:* `/profile` renders for a user who has never used any other feature.

- [ ] **B2 — Leaderboard opt-in flow.**
  Default **off**. On opt-in: if the user has a Telegram `@username`, adopt it as
  the display name; if not, prompt for one (2–32 chars, HTML-escaped via the
  existing `html.escape` path, uniqueness not required). Opt-out removes them
  from every board immediately.
  *Files:* `src/main.py`, `src/lib/store/profiles.py`
  *Done when:* a user with no username can opt in, and an opted-out user never
  appears in any board query.

- [ ] **B3 — Timezone & reminder time capture.**
  Asked **once**, during first plan setup (workstream D), not as a separate
  onboarding wall. Short UTC-offset picker; stored on `user_profile`. `/profile`
  can change it later.
  *Files:* `src/main.py`, `src/lib/store/profiles.py`
  *Done when:* changing the timezone shifts the next scheduled push accordingly.

---

### Workstream C — Hifz progress (item 4a)

- [ ] **C1 — Interval store with merge-on-insert.**
  Marking 67:1–8 then 67:5–10 must yield a single 67:1–10 interval, never two
  overlapping rows. Adjacent intervals coalesce.
  *Files:* `src/lib/store/hifz.py`
  *Done when:* the merge is covered by unit tests including adjacency,
  containment, and partial overlap.

- [ ] **C2 — Derived percentages.**
  Surah %, juz %, and whole-Qur'an % computed from intervals against
  `Quran.surah_lengths` and `Quran.juz_range` — both already exist in
  `src/modules/quran.py`. Nothing is stored as a counter.
  *Files:* `src/lib/hifz_progress.py`
  *Done when:* 67:1–8 reports Al-Mulk 27%, and re-marking 67:5–10 reports 33%.

- [ ] **C3 — `/progress` and `/forgot`.**
  `/progress` renders the motivation line ("Al-Mulk 8/30 · 27% · juz 29 4% ·
  Qur'an 0.4%"). `/forgot <ref>` unmarks a range, splitting intervals as needed.
  *Files:* `src/main.py`, `src/locales/*`
  *Done when:* `/forgot 67:5-6` splits 67:1–10 into 67:1–4 and 67:7–10.

---

### Workstream D — Plans & drills (item 4b)

The progression you described — repeat a **range**, then the **page**, then the
**whole surah** — is the plan generator's job, not the user's.

- [ ] **D1 — `/memorize` setup wizard.**
  Target (surah / juz / range) → pace (auto or explicit ayahs-per-day) → days of
  week → reminder time + timezone (B3). Ends with a **preview calendar** before
  anything is saved.
  *Files:* `src/main.py`, `src/lib/store/plans.py`, `src/locales/*`
  *Done when:* the preview matches what is later pushed, day for day.

- [ ] **D2 — Plan generator.**
  Splits the target across the chosen days, respecting ayah boundaries and never
  splitting mid-ayah. Widens the drill unit as portions are marked known: range →
  mushaf page (`Quran.page_range`) → whole surah.
  *Files:* `src/lib/plan_builder.py`
  *Done when:* Al-Mulk over weekdays produces 15 days ending exactly at 67:30,
  with a consolidation day at each page and surah boundary.

- [ ] **D3 — Drill delivery.**
  A pushed or manually started portion sends the Arabic image, the audio, the
  translation, and the drill controls. Reuses `send_quran`, `send_combined_audio`
  and the existing `🔁 Repeat ×3` button in `verse_keyboard`.
  *Files:* `src/main.py`
  *Done when:* a multi-ayah portion sends one stitched audio, not N files.

- [ ] **D4 — `✅ I know this by heart`.**
  Ends the drill; writes the interval (C1) and logs a `drill` session (G1) in one
  transaction so a streak can never tick without progress being recorded.
  *Files:* `src/main.py`, `src/lib/store/sessions.py`
  *Done when:* tapping it twice on the same portion does not double-log.

- [ ] **D5 — Plan lifecycle.**
  Pause, resume, abandon, and completion. Completing the final day sends a
  completion message and marks the plan `complete`.
  *Files:* `src/main.py`, `src/lib/store/plans.py`
  *Done when:* a paused plan produces no pushes and resumes without re-sending
  days already completed.

---

### Workstream E — Recall check (item 4c)

This is what makes the leaderboard fair to people memorizing from a **physical
mushaf**. It tests hifz, not app usage.

`translations/ar.txt` is the full vocalized Arabic text, 6236 ayahs, already
bundled and loadable through the existing `TranslationRegistry` — no new corpus
is needed.

- [ ] **E1 — Question builder.**
  Given an ayah, show its opening and offer four continuations: the correct one
  plus three distractors drawn from the same surah where possible, falling back
  to neighbouring ayahs, filtered to a similar length so option length is not a
  tell (assumption 5). Deterministic per (user, ayah, date) so a retry is not a
  reroll.
  *Files:* `src/lib/recall_check.py`
  *Done when:* no generated question has a correct option that is the longest or
  shortest by a wide margin, asserted over a sample of all 114 surahs.

- [ ] **E2 — Quiz delivery and scoring.**
  Inline-keyboard answer, immediate feedback, at most one earned session per day
  from recall checks. A pass logs a `recall_check` session.
  *Files:* `src/main.py`, `src/lib/store/sessions.py`
  *Done when:* a user with no plan at all can pass a check and earn the day.

- [ ] **E3 — `/check` entry point.**
  Lets a book learner test themselves on any surah or range on demand, not only
  on a plan portion.
  *Files:* `src/main.py`, `src/locales/*`
  *Done when:* `/check 67` produces a question from Al-Mulk.

---

### Workstream F — Scheduler

The app currently only wakes on webhooks. Everything timed depends on this, so it
lands before G and H.

- [ ] **F1 — Due-queue loop.**
  A background asyncio task started from `_initialize()` in `src/main.py`,
  alongside the existing corpora load. Polls `scheduled_send` every 60 s and
  claims due rows with `SELECT … FOR UPDATE SKIP LOCKED`.
  *Files:* `src/lib/scheduler.py`, `src/main.py`
  *Done when:* the loop survives an exception in one send without dying.

- [ ] **F2 — Idempotent enqueue.**
  Unique `idempotency_key` per `(kind, target, local_date)` so a restart, a
  double boot, or a retry cannot double-send.
  *Files:* `src/lib/store/schedule.py`
  *Done when:* enqueuing the same key twice inserts one row and raises nothing.

- [ ] **F3 — Catch-up on boot.**
  A window missed while the instance was restarting fires on next boot if it is
  still same-day-relevant; stale rows are dropped rather than delivered at 3 a.m.
  *Files:* `src/lib/scheduler.py`
  *Done when:* restarting the app between enqueue and due time still delivers
  exactly once.

---

### Workstream G — Streaks & activity graph (item 2)

- [ ] **G1 — Session logging + streak computation.**
  Streak = consecutive distinct `local_date` values in `session_log`. Recomputed
  on each session; `current_streak` / `longest_streak` denormalized onto
  `user_profile` for cheap reads.
  *Files:* `src/lib/store/sessions.py`, `src/lib/streaks.py`
  *Done when:* two sessions on the same local date tick the streak once, and a
  session at 23:59 followed by one at 00:01 local ticks it twice.

- [ ] **G2 — `/streak` with a 12-week grid.**
  Emoji grid (⬜🟩🟩⬛), which every Telegram client renders identically at zero
  render cost (assumption 1). Shows current streak, longest, and milestone copy.
  *Files:* `src/main.py`, `src/lib/streaks.py`, `src/locales/*`
  *Done when:* the grid aligns in a monospace block on both mobile and desktop.

- [ ] **G3 — Motivation copy.**
  Fixed milestones at 7 / 30 / 100 / 365 days. The "top X% of users" line stays
  dark until ≥200 users have a streak, then uses the real distribution computed
  weekly (assumption 2).
  *Files:* `src/lib/streaks.py`, `src/locales/*`
  *Done when:* with a small user base, no percentile claim is ever rendered.

---

### Workstream H — Leaderboard (item 3)

- [ ] **H1 — Weekly aggregation.**
  Sessions completed Mon 00:00 → Sun 23:59 **in the user's timezone**, ties
  broken by streak length. Opted-in users only.
  *Files:* `src/lib/leaderboard.py`, `src/lib/store/sessions.py`
  *Done when:* an opted-out user is absent from the query result, not merely
  hidden in rendering.

- [ ] **H2 — `/leaderboard` in DM.**
  Global board, the user's own rank always shown even when outside the top N.
  *Files:* `src/main.py`, `src/locales/*`
  *Done when:* a user ranked 400th sees rows 1–10 plus their own row.

---

### Workstream I — i18n & commands

- [ ] **I1 — New commands registered.**
  `/memorize`, `/progress`, `/streak`, `/leaderboard`, `/profile`, `/check`,
  `/forgot` added to `BOT_COMMANDS` in `src/locales/__init__.py` — the single
  source of truth for both the `/start` message and Telegram's command menu, so
  all 48 languages surface them at once.
  *Files:* `src/locales/__init__.py`
  *Done when:* `/start` lists every new command in every locale.

- [ ] **I2 — String tables for 48 locales.**
  Roughly 40–60 new keys across `src/locales/*.py`. No locale falls back to
  English — the property the README advertises.
  *Files:* `src/locales/*.py`
  *Done when:* `python3 scripts/check_locales.py` passes.

- [ ] **I3 — Docs.**
  Update `README.md` (user-facing feature description) and `BUSINESS_LOGIC.md`
  (§4 navigation model, §5 caching, and the roadmap in §8, which already lists
  "daily ayah subscriptions" as backlog item 4).
  *Files:* `README.md`, `BUSINESS_LOGIC.md`
  *Done when:* a new contributor can find the hifz flow from the README.

---

## 5. Phase 2 — group cluster (items 5–7)

Designed, not built. Listed so the Phase 1 data model stays honest.

- [ ] **J1 — Lift the group ban selectively.** `src/main.py:1136` currently
  returns on `chat_id < 0`. It becomes a check against configured chats, so the
  bot still ignores every group it was not deliberately set up in.
- [ ] **J2 — Admin onboarding in DM.** Admin adds the bot; a `my_chat_member`
  update tells us who added it; the bot DMs them the wizard.
- [ ] **J3 — Bot-created topic.** The admin names a topic in DM and the bot calls
  `createForumTopic`, so we own the `message_thread_id` outright — bots cannot
  list forum topics, and forwarding a message out of one strips the thread id.
- [ ] **J4 — Group plan wizard.** Range + pace + days + post time, with a preview
  calendar, reusing the Phase 1 plan generator against `group_plan`.
- [ ] **J5 — Daily group post (item 6).** Image + audio + translation in the
  group's admin-chosen language (assumption 4), posted to the bound topic through
  the Phase 1 scheduler.
- [ ] **J6 — Group weekly board.** Same aggregation as H1, scoped to members who
  opted in and linked via a `?start=g<chat_id>` deep link, with membership
  verified by `getChatMember` at render time.

---

## 6. Risks

| Risk | Mitigation |
|---|---|
| 512 MB free Koyeb instance already stitches mushaf pages; adding a scheduler and per-user renders could OOM | Emoji grid instead of PNG (assumption 1); scheduler holds no corpus state; bounded concurrency as `lib/page_image.py` already does |
| `translations/ar.txt` orthography may not match the rendered ayah images exactly | Recall check quotes the text file consistently for both prompt and options, so any mismatch is invisible within a question |
| ~2,500 machine-translated strings across 48 locales, in languages neither of us reads | `scripts/check_locales.py` validates placeholders, HTML balance and button round-trip; nuance remains a known limitation |
| Self-marked hifz is honour-system even though the leaderboard is not | Progress % and the board are deliberately decoupled — the board ranks sessions, never claimed ayahs |
| One in-process scheduler means one instance only | Already true of the app; `FOR UPDATE SKIP LOCKED` means a second instance would be correct, just unnecessary |

---

## 7. Done when (Phase 1 acceptance)

- A user runs `/memorize`, picks Al-Mulk, a pace and a reminder time, and sees a
  day-by-day preview before saving.
- At their local reminder time the next day the bot pushes that day's portion
  unprompted — verified by restarting the app between scheduling and firing, with
  no duplicate send.
- Completing that drill and passing the recall check ticks the streak **once**;
  `/streak` shows `1` and a 12-week grid.
- Marking 67:1–8 memorized makes `/progress` report Al-Mulk 27%; re-marking
  67:5–10 reports 33% (intervals merge, no double count).
- An opted-in user appears in `/leaderboard`; opting out removes them within one
  command.
- A user who never runs a drill but passes a recall check still earns the session
  and appears on the board.
- `pytest` passes, including new tests for interval merging, streak boundary at
  local midnight, scheduler idempotency, and quiz-distractor selection.
- `python3 scripts/check_locales.py` passes with all 48 locales complete.

---

## 8. Open questions

- [ ] Confirm **assumption 1** — emoji activity grid rather than a rendered PNG
  contribution graph.
- [ ] Confirm **assumption 2** — hold back the "top 2% of users" line until there
  are ≥200 users with a streak.

---

## 9. Change log

| Date | Change |
|---|---|
| 2026-07-31 | Document created; spec settled across three rounds of grilling. Phase 1 = items 1–4, Phase 2 = items 5–7. |
