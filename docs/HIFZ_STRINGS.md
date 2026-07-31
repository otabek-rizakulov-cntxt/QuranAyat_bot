# Hifz platform — frozen string manifest

**Status:** frozen at Wave 0b · **Keys:** 111 new · **Source of truth:** `src/locales/en.py`
**Last updated:** 2026-07-31

---

## 0. How to use this document

This is the contract between three groups of people who never see each other's
work:

- **Wave 2 (feature agents)** — read this file instead of `en.py` to find the key
  you need. You are **forbidden from editing `en.py`**: if a key you need is
  missing, say so in your report rather than adding it, because 47 translations
  are generated from this list and a late key silently ships as English.
- **Wave 4 (translation agents)** — one agent per language group. Translate every
  key below into `src/locales/<code>.py`, keeping the placeholder names byte for
  byte identical to English.
- **Reviewers** — `venv/bin/python scripts/check_locales.py` enforces the two
  hard rules mechanically.

### Hard rules (enforced by `scripts/check_locales.py`)

1. **Placeholders must match English exactly.** `{name}` stays `{name}` in
   Georgian. Translate the sentence, never the brace.
2. **No empty strings.** A blank value fails the check; an untranslated key
   silently falls back to English, which is the exact failure mode this project
   exists to prevent.
3. **No HTML tags in any hifz key.** Only `welcome_intro`, `welcome_inline` and
   `about` are checked for balanced `<b>`, and an unbalanced tag makes Telegram
   reject the *entire* message. None of the strings below contain markup — keep
   it that way.
4. `/start` must advertise every command in `BOT_COMMANDS`. The list is
   generated, so this only breaks if a locale hard-codes its own command list.

### Conventions

- `btn_*` — an inline-keyboard button label. Keep it short: three or four words
  at most, or it wraps on a phone.
- `cmd_*` — a command description. Shown in Telegram's command menu and in the
  `/start` list. Sentence fragment, no trailing period.
- Everything else is message body text.
- Emoji in a value (`btn_know_by_heart`) is part of the string and must be kept.
- Dates, times, offsets, percentages and ayah references are formatted by code
  and passed in as placeholders — they are never translated.

---

## 1. Command descriptions (7)

Registered in `BOT_COMMANDS` (`src/locales/__init__.py`), which drives both the
Telegram command menu and the `/start` message.

| Key | Placeholders | Where it is used |
|---|---|---|
| `cmd_memorize` | — | `/memorize` in the command menu and `/start` |
| `cmd_progress` | — | `/progress` in the command menu and `/start` |
| `cmd_check` | — | `/check` in the command menu and `/start` |
| `cmd_forgot` | — | `/forgot` in the command menu and `/start` |
| `cmd_streak` | — | `/streak` in the command menu and `/start` |
| `cmd_leaderboard` | — | `/leaderboard` in the command menu and `/start` |
| `cmd_profile` | — | `/profile` in the command menu and `/start` |

## 2. Shared wizard controls (7)

Owned by the seam (`src/hifz/__init__.py`), used by every feature.

| Key | Placeholders | Where it is used |
|---|---|---|
| `wizard_cancelled` | — | `/cancel`, and any `cancel` typed inside a wizard |
| `wizard_nothing_to_cancel` | — | `/cancel` with no wizard in progress |
| `wizard_invalid_input` | — | a wizard step raised; the draft is dropped |
| `ref_invalid` | — | a typed reference that `hifz.refs.parse_reference` rejects |
| `btn_cancel` | — | the cancel button on any wizard keyboard |
| `btn_back` | — | the back button on any multi-step keyboard |
| `btn_confirm` | — | generic confirm on a wizard keyboard |

## 3. Days of the week (7)

| Key | Placeholders | Where it is used |
|---|---|---|
| `day_mon` … `day_sun` | — | the plan's custom-days picker (D1) and the streak grid header (G2) |

Short forms (3–4 characters). They sit side by side in one keyboard row, so a
long translation breaks the layout.

## 4. Profile — workstream B (30)

| Key | Placeholders | Where it is used |
|---|---|---|
| `profile_title` | — | first line of `/profile` (B1) |
| `profile_name_set` | `{name}` | `/profile`, when a display name exists |
| `profile_name_unset` | — | `/profile`, when it does not |
| `profile_leaderboard_on` | — | `/profile`, opted in (B2) |
| `profile_leaderboard_off` | — | `/profile`, opted out |
| `profile_timezone_set` | `{offset}` | `/profile`; `{offset}` is `+05:00`, rendered after a literal "UTC" (B3) |
| `profile_timezone_unset` | — | `/profile`, no timezone captured yet |
| `profile_reminder_set` | `{time}` | `/profile`; `{time}` is 24-hour local, e.g. `07:30` |
| `profile_reminder_unset` | — | `/profile`, reminders off |
| `profile_plan_active` | `{target}` `{day}` `{total}` | `/profile`, active plan line; `{target}` is e.g. `Al-Mulk` |
| `profile_plan_none` | — | `/profile`, no plan line |
| `btn_edit_name` | — | `/profile` keyboard |
| `btn_join_board` | — | `/profile` keyboard, shown when opted out |
| `btn_leave_board` | — | `/profile` keyboard, shown when opted in |
| `btn_edit_timezone` | — | `/profile` keyboard |
| `btn_edit_reminder` | — | `/profile` keyboard |
| `name_prompt` | — | the display-name wizard step (B2) |
| `name_invalid` | `{min}` `{max}` | typed name outside 2–32 characters |
| `name_saved` | `{name}` | display name accepted |
| `board_joined` | — | leaderboard opt-in confirmed |
| `board_left` | — | leaderboard opt-out confirmed |
| `timezone_prompt` | — | above the UTC-offset picker (B3) |
| `timezone_saved` | `{offset}` | offset picked; rendered after a literal "UTC" |
| `reminder_prompt` | — | the reminder-time wizard step |
| `reminder_invalid` | — | typed time that does not parse |
| `reminder_saved` | `{time}` | reminder time accepted |
| `btn_reminder_off` | — | button on the reminder picker |
| `reminder_off` | — | confirmation that reminders were turned off |

## 5. Progress and `/forgot` — workstream C (8)

| Key | Placeholders | Where it is used |
|---|---|---|
| `progress_title` | — | first line of `/progress` (C3) |
| `progress_surah_line` | `{name}` `{done}` `{total}` `{pct}` | per-surah line; `{name}` is the surah name, `{done}`/`{total}` are ayah counts |
| `progress_juz_line` | `{n}` `{pct}` | per-juz line |
| `progress_quran_line` | `{pct}` | whole-Qur'an line |
| `progress_empty` | — | `/progress` with nothing marked |
| `forgot_usage` | — | bare `/forgot` with no argument |
| `forgot_done` | `{ref}` | a range unmarked; `{ref}` is e.g. `67:5-6` |
| `forgot_nothing` | — | `/forgot` on a range that was never marked |

## 6. Plans and drills — workstream D (32)

| Key | Placeholders | Where it is used |
|---|---|---|
| `memorize_choose_target` | — | step 1 of `/memorize` (D1) |
| `btn_target_surah` | — | target chooser |
| `btn_target_juz` | — | target chooser |
| `btn_target_range` | — | target chooser |
| `memorize_surah_prompt` | — | after picking "a surah" |
| `memorize_juz_prompt` | — | after picking "a juz" |
| `memorize_range_prompt` | — | after picking "a range" |
| `memorize_choose_pace` | — | step 2 of `/memorize` |
| `btn_pace_auto` | — | pace chooser; lets the generator decide |
| `memorize_pace_prompt` | — | after choosing an explicit pace |
| `memorize_pace_invalid` | `{min}` `{max}` | typed pace out of range |
| `memorize_choose_days` | — | step 3 of `/memorize` |
| `btn_days_daily` | — | days chooser |
| `btn_days_weekdays` | — | days chooser |
| `btn_days_custom` | — | days chooser |
| `memorize_days_prompt` | — | the custom day-picker keyboard |
| `memorize_preview_title` | `{days}` `{start}` `{end}` | preview header; `{start}`/`{end}` are dates |
| `memorize_preview_row` | `{date}` `{ref}` | one row of the preview calendar |
| `btn_confirm_plan` | — | saves the plan |
| `plan_saved` | `{first_date}` | plan written; first portion date |
| `plan_exists` | — | `/memorize` with a plan already active (assumption 3) |
| `btn_pause_plan` | — | plan lifecycle (D5) |
| `btn_resume_plan` | — | plan lifecycle |
| `btn_abandon_plan` | — | plan lifecycle |
| `plan_paused` | — | confirmation |
| `plan_resumed` | — | confirmation |
| `plan_abandoned` | — | confirmation |
| `plan_complete` | `{target}` | final day completed |
| `drill_title` | `{ref}` `{day}` `{total}` | header of a pushed or manual drill (D3) |
| `drill_none_today` | — | manual drill start on a non-study day |
| `btn_start_drill` | — | starts today's portion on demand |
| `btn_know_by_heart` | — | ends the drill and writes the interval (D4). Keep the ✅ |
| `know_confirmed` | `{ref}` `{pct}` | interval written; `{pct}` is the new surah percentage |
| `know_already` | — | the same portion tapped twice |

## 7. Recall check — workstream E (6)

| Key | Placeholders | Where it is used |
|---|---|---|
| `check_question` | — | above the ayah opening and the four options (E2) |
| `check_usage` | — | bare `/check` with no argument (E3) |
| `check_correct` | — | right answer |
| `check_wrong` | `{correct}` | wrong answer; `{correct}` is the correct continuation |
| `check_already_today` | — | a pass when today's session was already earned |
| `btn_check_start` | — | starts a check from another screen |

## 8. Streaks — workstream G (9)

| Key | Placeholders | Where it is used |
|---|---|---|
| `streak_title` | — | first line of `/streak` (G2) |
| `streak_current` | `{n}` | current streak in days |
| `streak_longest` | `{n}` | longest streak in days |
| `streak_none` | — | `/streak` with no sessions yet |
| `streak_graph_caption` | — | under the 12-week emoji grid |
| `streak_milestone_7` | — | shown at exactly 7 days (G3) |
| `streak_milestone_30` | — | shown at 30 days |
| `streak_milestone_100` | — | shown at 100 days |
| `streak_milestone_365` | — | shown at 365 days |

No percentile / "top X% of users" string exists by design (assumption 2) — do
not invent one.

## 9. Leaderboard — workstream H (5)

| Key | Placeholders | Where it is used |
|---|---|---|
| `leaderboard_title` | — | first line of `/leaderboard` (H2) |
| `leaderboard_row` | `{rank}` `{name}` `{sessions}` | one board row |
| `leaderboard_you_row` | `{rank}` `{sessions}` | the caller's own row, always shown |
| `leaderboard_empty` | — | nobody has a session this week |
| `leaderboard_not_opted_in` | — | the caller is opted out (B2) |

---

## 10. Count check

| Section | Keys |
|---|---|
| 1 · Commands | 7 |
| 2 · Shared wizard controls | 7 |
| 3 · Days of the week | 7 |
| 4 · Profile | 28 |
| 5 · Progress and `/forgot` | 8 |
| 6 · Plans and drills | 34 |
| 7 · Recall check | 6 |
| 8 · Streaks | 9 |
| 9 · Leaderboard | 5 |
| **Total** | **111** |

Verify against the code with:

```bash
venv/bin/python - <<'PY'
import subprocess, sys
sys.path.insert(0, "src")
old = subprocess.run(["git", "show", "HEAD:src/locales/en.py"],
                     capture_output=True, text=True).stdout
ns = {}; exec(compile(old, "old", "exec"), ns)
import locales.en as en
print(len(set(en.strings) - set(ns["strings"])), "new keys")
PY
```

`tests/test_locales.py` fails with **47 `test_no_missing_keys` failures** until
Wave 4 lands — one per non-English interface language. That red is the intended
signal that translation work is outstanding; it must not be silenced by copying
English into the other tables.
