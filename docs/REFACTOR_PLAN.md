# Refactor — Implementation Plan

> Break `src/main.py` (1,512 lines) into small single-purpose modules, give every
> layer one direction of dependency, remove the copy-pasted patterns, and tidy the
> repository root — **without changing a single user-visible behaviour.** Every
> step is a pure move or a mechanical extraction, gated by the existing suite.

**Status:** §11.1 shipped (PR #26). Phase 0 done on `refactor/phase-0-guardrails`. §9
records the decisions taken; questions 2, 3 and 7 are still open.
§11 holds two user-reported problems (settings resetting; a country-based
timezone picker). They change behaviour, so they ship as separate `fix/` and
`feat/` work, but they're tracked here because they touch the same modules.
**Last updated:** 2026-10-29
**Baseline:** `pytest` → 1846 passed, 100 skipped (Postgres leg) in ~8 s. Every PR
below must end on the same numbers or higher.
**Verified against:** the graphify code graph at commit `bb55ef6` (3865 nodes,
8647 edges) — `GRAPH_REPORT.md`, `graphify query` and `graphify affected` on every
symbol this plan moves, cross-checked against the source.

---

## 1. Why

The codebase is in better shape than its biggest file suggests. `services/`,
`lib/store/` and the `hifz/` feature seam are already well-factored, documented and
covered. The problems are concentrated, and the plan targets those spots and leaves the rest alone:

1. **`src/main.py` does nine jobs.** These are FastAPI app wiring, startup/shutdown, the webhook
   route, a public media route, Telegram media sending + file-id caching, CDN audio
   stitching, ayah-reference parsing, six keyboard builders, inline-query answering
   and a 410-line `handle_update` with ~30 `if`/`elif` branches routing commands,
   callbacks and free text by hand.
2. **The dependency graph has a hidden cycle and several inversions.** These are workarounds, not design choices:
   - `hifz/memorize.py` and `hifz/group.py` import from `main` (`send_quran`,
     `send_combined_audio`, `get_translation`, `REPEAT_COUNT`, `MAX_RANGE_AYAHS`).
     A static scan finds no import cycle: `main` imports only the `hifz` package,
     and the feature modules that import `main` back are loaded lazily by
     `pkgutil`. At runtime the loop is real (`main → hifz → memorize → main`).
     It only works because discovery is deferred, and `hifz/__init__.py`'s header
     says so. The feature code that depends on `main` is `push_plan_day`,
     `_start_drill` and `_send_drill` (memorize), plus `push_group_day` →
     `_post_portion` (group).
   - `lib/` (`plan_builder`, `hifz_progress`) and `services/` import `hifz.refs`.
     The low-level layers depend on the Telegram-handler package because a pure
     domain type (`Ref`) lives in it.
   - 18 function-local imports exist (12 in `hifz/group.py` alone), mostly to dodge
     those cycles.
3. **The same patterns are copy-pasted in many places.**

   | Pattern | Copies | Where |
   |---|---|---|
   | "send cached file_id, else upload and cache it" | 5 | `send_file`, `send_combined_audio`, `send_page`, `send_page_audio`, `send_repeated_audio` |
   | chunk buttons into rows of N | 10 | `main.py` ×5 (both language keyboards, reciter, sajda, search results); `hifz/memorize.py:222,231`; `hifz/profile.py:109`; `hifz/group.py:527`; `hifz/progress.py:94` |
   | UTC-offset picker keyboard | 3 | `profile.offset_keyboard` (public, already takes `prefix` + `columns`), `memorize._offset_keyboard`, `group._offset_keyboard` |
   | `except BadRequest: if "not modified" not in …: raise` | 3 | `main.py`, `hifz/__init__.py` |
   | `create_task` + `_background_tasks.add` + `discard` | 3 | `main.py` |
   | `language_keyboard` vs `translation_language_keyboard` | 2 | identical except list + callback prefix |
   | per-update settings unpacking `ui_lang, translation_lang, reciter = …` | 3 | `handle_update` |

   The offset pickers are a leftover. `memorize.py:212-216` says to delete its
   private keyboards and call `profile`'s "when Wave 2A lands its public helpers".
   Wave 2A has landed, so that cleanup was never done. (The two *reminder*
   keyboards aren't duplicates, though: see §10.)

4. **`lib/utils.File` is a god class.** It holds the Redis file-id cache, reader nav state,
   the legacy language key, the awaiting-input flag, the performers catalog,
   reciter search and every CDN URL builder. It also *inherits* from
   `Environment` just to call `get_env`.
   - **How far it reaches:** 13 `src/` modules and 31 test files use it, and
     every `hifz` handler receives it through `Ctx.file`. The graph ranks it the
     third most-connected node, bridging more than 30 communities.
   - **Leaked private access:** `File._load_performers` is called from outside
     the class 3 times.
5. **`lib/` is a junk drawer.** Pure domain logic (`plan_builder`, `recall_check`,
   `localtime`, `streaks`), infrastructure (`store`, `scheduler`, `page_image`,
   `streak_image`) and Telegram UI (`miniapp.app_row`) sit side by side. The name
   says nothing about which is which. `modules/` has the same problem: it holds the
   Quran domain *and* the Telegram `Bot` singleton.
6. **There's no consistent hygiene.**
   - 15 files use 2-space indentation and the rest use 4 (`config/*`,
     `lib/store/*`, `lib/utils.py`, `hifz/group.py`, …).
   - There's no formatter, linter or `pyproject.toml`.
   - Logging is 56 `print()` calls; there's no `logging`.
   - FastAPI's deprecated `@app.on_event` is still in use.
   - Config is read through stringly-typed `Environment.get_env("…")` keys.
7. **The repository root is cluttered.**
   - Runtime corpora (`quran-data.xml`, `en.ahmedraza`, `Al_Jalalain_Eng.txt`,
     `translations/`) sit at the root. They're listed in `.gitignore` yet tracked,
     so the ignore lines are dead and misleading.
   - A 3 MB source PDF is tracked, as is `.DS_Store`.
   - Three planning docs (`BUSINESS_LOGIC.md`, `MULTILINGUAL_PLAN.md`,
     `TESTING.md`) live at the root while the rest live in `docs/`.
   - The Dockerfile's `pip install -U python-dotenv` silently overrides the pinned
     version.

## 2. Goals and non-goals

**Goals**
- No source file over ~300 lines; no function over ~60 lines.
- `main.py` becomes app wiring only (< 60 lines).
- Dependencies point one way (§4). No module imports `main`. No function-local
  import exists to dodge a cycle.
- Each pattern in the §1.3 table has exactly one implementation.
- The core reader uses the same decorator registry the `hifz` features already
  use. Adding a command means adding a handler, not editing `handle_update`.
- One formatter/linter config, enforced in CI; `logging` instead of `print`.

**Non-goals**
- **No behaviour change.** Callback-data strings, cache keys, Redis/Postgres
  schemas, message text, the HTTP API and the Mini App contract stay
  byte-identical. A cache-key typo would silently invalidate every cached file_id.
- No new frameworks: no DI container, no ORM, no abstract base class per module.
  KISS beats ceremony. The existing `Protocol`/dataclass style is the ceiling.
- Locale tables (`src/locales/*.py`) stay as they are; they're data, and 48 files
  of the same shape is correct.
- `services/` and `lib/store/` internals aren't redesigned, only relocated.
- The multi-platform (WhatsApp) adapter in `docs/MULTI_PLATFORM_PLAN.md` isn't
  built here. This plan only makes that work cheaper (§4, §4.1).

## 3. Principles applied

| Principle | Concretely, in this repo |
|---|---|
| **Single responsibility** | One module per job: keyboards, media sending, parsing, routing, app wiring. |
| **DRY** | §1.3 patterns become `send_cached()`, `button_rows()`, `ignore_not_modified()`, `spawn()`. |
| **KISS** | Plain functions and dataclasses; no class where a function does. |
| **Dependency rule** | Presentation → services → domain; infrastructure is injected or called downward, never upward (§4). |
| **Open/closed via registry** | Commands/callbacks register with decorators (the existing `hifz` seam, generalised), so the router never grows. |
| **Command pattern** | Each command/callback is a small handler object behind a uniform `(ctx) -> None` signature. |
| **Facade** | `main.py` keeps re-exporting moved names for exactly one phase so tests migrate in a separate, reviewable PR. |
| **Strangler fig** | Move one slice at a time behind the old names; delete the shim only when nothing references it. |

## 4. Target layout and layering

```
src/
  main.py                    # ~40 lines: `app = create_app()`
  app/                       # HTTP process (FastAPI)
    factory.py               # create_app(): routers, CORS, lifespan
    lifespan.py              # startup steps (was _initialize), shutdown
    state.py                 # AppState(bot, data) — replaces module globals
    tasks.py                 # spawn(): background tasks with strong refs
    routes/
      webhook.py             # POST /webhook (secret header, not the token in the path)
      media.py               # GET /media/range.mp3
      health.py              # GET /
  bot/                       # Telegram presentation layer
    router.py                # @command / @callback / @wizard registry (from hifz/__init__)
    context.py               # Ctx (from hifz/__init__), built once per update
    dispatch.py              # handle_update: route by update type → router
    errors.py                # ignore_not_modified()
    keyboards/
      rows.py                # button_rows(buttons, cols) — the one row-packing loop
      verse.py page.py reciter.py language.py sajda.py
      time_pickers.py        # offset_keyboard, reminder_keyboard (from hifz/profile.py)
    text.py                  # reference(), ref_key(), nav_labels(), page_caption(), verse_text()
    media.py                 # send_cached() + send_quran/page/page_audio/repeat/range
    inline.py                # inline-query answering (articles, audio, photos)
    handlers/                # core reader, registered like hifz features
      info.py                # /start /help /about /index /app
      reader.py              # vc: vr: rep:, button actions, typed references, /random
      pages.py               # /page /juz /sajda, pg: pga:
      settings.py            # /language /translation, setlang: settranslang: showlang
      reciters.py            # /reciter, recgrp: setreciter: reciter_search
      membership.py          # my_chat_member → group feature
    features/                # was src/hifz/ (memorize, group, check, progress, …)
  services/                  # unchanged role: use-cases, no telegram import
  domain/                    # pure Python, no I/O, no telegram
    quran.py                 # Quran, divisions, TranslationRegistry (from modules/)
    refs.py                  # Ref & friends (from hifz/refs.py)
    parsing.py               # parse_ayah, parse_ayah_range, as_int
    plan_builder.py recall_check.py localtime.py hifz_progress.py
    streaks.py leaderboard.py   # the pure computation halves
  infra/                     # I/O adapters
    store/                   # from lib/store (repositories, schema)
    redis.py postgres.py     # from config/
    media_cache.py           # file-id cache          ┐
    nav_state.py             # reader position         │ the four halves
    pending_input.py         # awaiting-input flag     │ of File, split
    catalog.py               # performers.json, search, CDN URL builders ┘
    audio.py                 # download_stitched_audio (from main)
    page_image.py streak_image.py wizard_store.py scheduler.py
    telegram.py              # Bot client factory (from modules/bot.py)
  config/
    settings.py              # typed, frozen Settings, read once
    logging.py               # logging setup
  locales/                   # unchanged
  resources/                 # performers.json, schema.sql (from common/)
data/                        # runtime corpora, moved out of the repo root
  quran-data.xml  en.ahmedraza  al_jalalain_en.txt  translations/*.txt
```

**Dependency rule.** An import may only point down this list:

```
app  →  bot  →  services  →  domain
  ↘       ↘        ↘
          infra  ─────────→  domain        config ← everyone
```

- `domain` imports nothing from the project except `config` constants.
- `services` never imports `telegram`. The repo already has this rule in
  `tests/test_service_layer.py`; it's extended to the full table above.
- `bot` and `app` are the only places that know Telegram or FastAPI exist. A
  future `whatsapp/` adapter sits beside `bot/` and reuses everything below it,
  which is exactly the seam `MULTI_PLATFORM_PLAN.md` needs.

Enforcement is an extension of `test_service_layer.py` (an AST walk over imports
per package) rather than a new dependency like `import-linter`.

### 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`

That plan's Phase 1 ("Channel seam") rewrites the same code this plan moves:

- **P1.3** normalises `main.handle_update` to `Incoming`, swaps `hifz.Ctx.bot` for a
  `channel`, and routes the scheduler's `SendCtx` through `Channel`.
- **P1.1** wraps every `send_*` behind `channels/telegram.py`.

Doing both plans at once means rewriting the same functions twice and resolving
merge conflicts in `main.py`. **Sequence them instead:** finish this plan's
Phases 0–3 first. Then the channel seam lands on small, known targets:

- `Channel` wraps `bot/media.py`;
- `Incoming` normalisation lives in `bot/dispatch.py`;
- `Ctx` is defined once, in `bot/context.py`.

Phases 4–6 don't conflict with the channel seam, so they can run before or after it.
`MULTI_PLATFORM_PLAN.md` §P1 should then be updated to name those modules instead of
`main.handle_update`.

## 5. Phases

Each numbered step is one PR on its own branch, merged only on green CI. Moves
and edits are never mixed in one commit, so `git log --follow` and review diffs
stay readable.

### Phase 0 — Guardrails (no code moves) — *done*

- **0.1 Tooling.**
  - Add `pyproject.toml` with `ruff` (lint + format) and a minimal rule set
    (`E`, `F`, `I`, `B`, `UP`, `SIM`).
  - Run one mass format commit to normalise 2-space → 4-space. Put its hash in
    `.git-blame-ignore-revs`.
  - Add a `ruff check` + `ruff format --check` step to `.github/workflows`.
- **0.2 Layering test.** `tests/test_layering.py` checks import direction between
  today's packages. The 13 violations that exist now are listed in `KNOWN`, each
  with the step that removes it. It works as a ratchet rather than `xfail`: a new
  violation fails, and so does a listed one that has been fixed, so the list
  only shrinks. Each refactor step deletes its entries.
- **0.3 Logging.** Add `config/logging.py` and replace all 56 `print()` calls
  with module loggers at the right levels (`INIT ERROR` → `logger.exception`).
  Output stays on stdout, so the platform logs are unchanged.

*Done when:* CI runs lint + format; zero `print(` in `src/`.

*As shipped:*
- Ruff ignores style-only rules: `%`-formatting, typing-syntax upgrades and a
  few others, each with its reason in `pyproject.toml`.
- Ruff's undefined-name check found a real `NameError` in the group setup
  wizard, fixed in its own commit.
- Logging keeps httpx/httpcore at WARNING, because Bot API URLs contain the
  bot token.

### Phase 1 — Take `main.py` apart (pure moves) — *done*

`main.py` keeps `from bot.… import *`-style re-exports of every moved name until
step 1.6. Tests patch ~40 `main.*` attributes (73 references to
`main.handle_update` alone), so they keep passing untouched until then.

- **1.1 Parsing → `domain/parsing.py`.** `parse_ayah`, `parse_ayah_range`, `_as_int`.
- **1.2 Text + keyboards → `bot/text.py`, `bot/keyboards/*`.**
  - Move `_reference`, `_ref_key`, `_nav_labels`, `_page_caption` and
    `build_verse_text`.
  - Move the five keyboard builders and the reciter-picker helpers
    (`reciter_label`, `reciter_page_count`, `reciter_page_of`,
    `reciter_set_confirmation`).
- **1.3 Media → `infra/audio.py` + `bot/media.py`.**
  - `_download_stitched_audio` / `_download_combined_audio` go to `infra/audio.py`.
  - Every `send_*` function goes to `bot/media.py`, along with the constants
    `MAX_RANGE_AYAHS` and `REPEAT_COUNT`.
  - **This is the step that breaks the `hifz → main` runtime cycle.** Repoint
    `hifz/memorize.py` (module-level import, used by `push_plan_day`,
    `_start_drill`, `_send_drill`) and `hifz/group.py` (function-local import in
    `_post_portion`) to `bot.media`, and drop the local imports.
  - `get_translation` goes to `domain/quran.py` next to `TranslationRegistry`,
    not to `bot/`. It isn't Telegram-specific, and `services` will need it once
    the channel seam lands.
- **1.4 Inline mode → `bot/inline.py`.** `_inline_audio_result`,
  `_inline_photo_results`, `get_default_query_results`, plus the inline branch of
  `handle_update` as `answer_inline_query(bot, data, update)`.
- **1.5 App wiring → `app/`.**
  - The FastAPI app, CORS and the three routes move into `app/routes/`.
  - `_initialize` is split into named startup steps in `app/lifespan.py`.
  - `@app.on_event` becomes a `lifespan` context manager.
  - The module globals `bot` / `data` become an `AppState` on `app.state`.
- **1.6 Retarget tests, delete the shim.** A mechanical `sed` from `main.X` to
  the new module paths in `tests/`, reviewed as one PR. Then delete the
  re-exports from `main.py`.

*Done when:* `main.py` < 60 lines; `grep -r "from main import" src` is empty.

*As shipped* (`refactor/phase-1-split-main`):
- `main.py` is 40 lines, down from 1,512.
- `handle_update` moved unchanged to `bot/dispatch.py` in 1.5. Leaving it in
  `main.py` until Phase 3 would have broken the line count above, so Phase 3
  rewrites it there instead.
- 2.5 (`spawn`) was pulled forward into 1.5, since the three task sites were
  moving anyway.
- `@app.on_event` became a `lifespan` handler; the suite now runs with no
  deprecation warnings.
- `get_translation` lives in `modules/quran.py` until Phase 5 moves the
  module to `domain/`.
- The re-export shim only worked for *reading* names. Tests that patched a
  function through `main` had to move in the step that moved the function
  (1.3), because a patch on `main` no longer reaches the caller.

### Phase 2 — DRY the duplicated patterns — *done*

- **2.1 `send_cached(bot, key, kind, build_source, **kwargs)`** in `bot/media.py`.
  It tries the cached file_id, falls back to building and uploading, then stores
  the new id. The five senders become ~10 lines each. Cache keys are passed in
  verbatim; a test asserts every key string is unchanged.
- **2.2 `button_rows(buttons, cols)`** in `bot/keyboards/rows.py`, used at all
  10 chunking sites in `main.py` and `hifz/`. (It isn't called `grid`/`build_grid`:
  that name already belongs to the streak heatmap in `lib/streak_image.py`.)
  `language_keyboard` and `translation_language_keyboard` collapse to one
  `language_picker(languages, callback_prefix)`.
- **2.3 One offset picker.** Move `profile.offset_keyboard` (already
  parameterised by `prefix` and `columns`; it reads the same `OFFSET_CHOICES` list
  as the others) to `bot/keyboards/time_pickers.py`, along with
  `reminder_keyboard`.
  - Delete `memorize._offset_keyboard`, as its own comment asks, and call the
    shared one with `prefix="hm:tz:"`.
  - Leave `memorize._reminder_keyboard` alone: it isn't a copy (see §10).
  - Delete `group._offset_keyboard` and call the shared one with
    `prefix="gr:tz:"`.
  - **Check the label difference first:** memorize prints `"UTC+05:00"`, while
    profile and group print `"+05:00"`. Keep it with a `label_prefix` argument,
    or treat dropping it as a deliberate, separately reviewed copy change.
- **2.4 `ignore_not_modified()`** context manager in `bot/errors.py`, applied to
  all six sites.
- **2.5 `spawn(coro)`** in `app/tasks.py`, applied to all three background-task
  sites. *(Done in 1.5.)*
- **2.6 (optional, behaviour-adjacent) Group portion image.** `group._post_portion`
  re-downloads and re-stitches the portion image on every daily post, for every
  group. It skips the file_id cache that `send_page` uses for the same kind of
  stitched image. Routing it through `send_cached` with a
  `portion:<surah>:<start>-<end>` key changes no message content, but it adds a
  new cache key. Ship it as its own PR or skip it.

*Done when:* each §1.3 row has one implementation; senders have a table-driven
test over their cache keys.

*As shipped* (`refactor/phase-2-dry`):
- `tests/test_media_cache_keys.py` pinned every sender's Redis key before the
  merge.
- There were six cache-or-upload copies, not five: `/streak`'s graph was one
  too. All six now go through `send_cached`, which also logs a rejected cached
  id for every sender.
- Row-chunking (8 sites; the other 2 were the private offset pickers) goes
  through `button_rows`. The two language keyboards are now one
  `language_picker`.
- The three offset pickers are one, and all three grids were checked
  identical to before. `reminder_keyboard` stayed in `profile.py`: it has a
  single caller, and memorize's preset picker is a different interaction
  (§10), not a copy.
- There were three "not modified" sites, not six (the count included
  comments).
- 2.6 (caching the group portion image) was skipped. It's optional and adds
  a cache key.
- The "settings unpacking ×3" row is left to Phase 3, where `Ctx` replaces it.

### Phase 3 — One router for everything — *done*

- **3.1 Promote the seam.** Move `Ctx`, the decorators and the dispatchers from
  `hifz/__init__.py` to `bot/router.py` and `bot/context.py`. `hifz/__init__.py`
  re-exports them, so feature modules don't change in this PR.
- **3.2 Register the core reader.** Rewrite `handle_update`'s command chain and
  callback chain as decorated handlers in `bot/handlers/*.py` (§4). Then
  `bot/dispatch.py` becomes:
  1. `my_chat_member` → membership
  2. inline query → `bot.inline`
  3. callback query → `router.dispatch_callback`
  4. text message, in this order:
     1. command → `router.dispatch_command`
     2. pending input
     3. active wizard
     4. button action
     5. reference

  That order is the one `handle_update` encodes today, comments included. It's
  load-bearing: a command must always escape a wizard.
- **3.3 Reciter search as a wizard.** The ad-hoc `awaiting_input == "reciter_search"`
  branch becomes a `@wizard("reciter_search")`, which retires the separate
  awaiting-input mechanism.
- **3.4 Prefix table.** Move the reserved reader prefixes out of the comment in
  `hifz.PREFIXES` and into the table itself. Have the registry reject a duplicate
  prefix at load time instead of by convention.

*Done when:* `handle_update` is under 40 lines; adding a command touches one file.

*As shipped* (`refactor/phase-3-router`):
- `tests/test_dispatch_order.py` pinned the text-message order before the
  rewrite.
- `handle_update` is ~20 lines, plus `_on_callback` and `_on_text` (~60
  together), down from ~460. The reader's 12 commands and 11 prefixes live
  in `bot/handlers/`.
- **3.3 skipped on purpose.** Making reciter search a wizard would change
  three behaviours the order tests pin:
  - wizards are one per user, so tapping "Search reciter" mid-`/memorize`
    would destroy that draft;
  - any command clears a pending search, but commands deliberately don't end
    wizards;
  - the prompt would live 30 minutes instead of 2.

  The pending-input flag stays.
- 3.4: instead of a longer table, the router enforces the namespace. It
  rejects a callback prefix that overlaps another module's.
- The reader's callbacks now get the router's error handling (logged and
  acknowledged on failure, no endless spinner).
- The "settings unpacking ×3" row from §1.3 is gone: handlers read
  `ctx.ui_lang` / `ctx.reciter`.
- Found and fixed on the way: scheduled pushes queued their follow-up from
  the wall clock, not the tick's time, which made one acceptance test fail
  between 02:00 and 19:00 UTC (the test user's reminder time to local midnight).

### Phase 4 — Split infrastructure god-objects

- **4.1 Split `File`** into `media_cache`, `nav_state`, `pending_input` (until 3.3
  retires it) and `catalog` (§4).
  - Each takes its Redis connection in `__init__` instead of inheriting
    `Environment`.
  - The legacy-language migration helpers stay with `user_settings`, their only
    caller.
  - **`File` stays as a thin facade** that delegates to the four new classes.
    It's used in 13 `src/` modules and 31 test files, and every `hifz` handler
    reads it through `Ctx.file`, so a big-bang rename would be the largest diff
    in the plan. Callers migrate one module per PR; the facade is deleted when
    `graphify affected` on `File` shows no callers.
  - `File._load_performers` becomes a public `catalog.performers()`. Three
    outside callers currently reach into the private method.
- **4.2 Typed settings.** `config/settings.py` exposes one frozen dataclass, built
  once from the environment at startup.
  - `Environment.get_env("…")` string lookups are replaced by attribute access, so
    a typo becomes an `AttributeError` at import instead of a `KeyError` at
    runtime.
  - `_webhook_base_url()` becomes a computed field.
- **4.3 Bot client.** `modules/bot.py`'s singleton becomes
  `infra/telegram.create_bot(settings)`, held on `AppState` and passed via `Ctx`.

### Phase 5 — Fix the layering

- **5.1 Domain package.**
  - Move `hifz/refs.py` → `domain/refs.py` (removes every `lib`/`services` →
    `hifz` import).
  - Move `modules/quran.py` → `domain/quran.py`.
  - Move the pure modules of `lib/` → `domain/`.
- **5.2 Infra package.** `lib/store`, `scheduler`, `page_image`, `streak_image`
  and `wizard` move to `infra/`; `config/redis.py` and `config/postgres.py` move
  to `infra/`. Where a `lib` module mixes pure computation with a store read
  (`streaks`, `leaderboard`), split it: the pure half goes to `domain`, and the
  store-reading half becomes a `services` function.
- **5.3 Features.** Move `hifz/*` → `bot/features/`, and `lib/miniapp.py`'s
  `app_row` → `bot/keyboards/`. Delete `lib/` and `modules/`.
- **5.4 Turn the layering test's `xfail`s into hard failures.**

### Phase 6 — Repository hygiene

- **6.1 Corpora → `data/`.** Resolve them relative to the package, never the
  CWD, so `conftest.py`'s `os.chdir` and the Dockerfile's comment about it can
  go. Delete the dead `.gitignore` lines for files that are tracked.
- **6.2 Untrack junk.** `git rm --cached .DS_Store`. Ask before removing
  `Al_Jalalain_Eng.pdf` (§9): it's the provenance of the tafsir text, but it
  isn't read at runtime.
- **6.3 Docs.** Move `BUSINESS_LOGIC.md`, `MULTILINGUAL_PLAN.md` and `TESTING.md`
  into `docs/`, add a `docs/README.md` index, and fix the links.
- **6.4 Image.**
  - Drop the `pip install -U python-dotenv` override.
  - Pin a current Python 3.10 patch, or 3.12 after a test run.
  - Add `docs/`, `graphify-out/` and `scripts/` to `.dockerignore`.
- **6.5 Tests mirror source.** Regroup `tests/` into `tests/{domain,services,bot,app,infra}/`
  as a pure move.

## 6. Ordering, risk, size

| Phase | Risk | Size | Unblocks |
|---|---|---|---|
| 0 Guardrails | low | S | everything (formatter first, or every later diff is noise) |
| 1 Split main | low (pure moves behind a shim) | M | 2, 3, multi-platform |
| 2 DRY | **medium**: cache keys | S | — |
| 3 Router | **medium**: dispatch order | M | adding features cheaply |
| 4 Infra split | low | S–M | 5 |
| 5 Layering | low (moves) but wide | M | — |
| 6 Hygiene | low | S | — |

Phases 0 → 1 → 2 are the high-value core and stand alone. 3–6 can stop at any
phase boundary and leave the tree in a consistent state.

## 7. Safety net

- The 1846-test suite is the contract. No test is deleted or weakened; tests only
  change their import paths (1.6, 6.5).
- **New characterisation tests, written *before* the phase that touches the
  code:**
  - every Redis cache-key string (Phase 2);
  - every `callback_data` prefix → handler mapping;
  - the dispatch order "command beats pending input beats wizard beats reference"
    (Phase 3).
- `graphify affected "<node>"` before each move, `graphify update .` after, per
  `CLAUDE.md`.
- A manual smoke on a staging bot after Phases 1, 3 and 5: `/start`, a typed
  reference, a range, every verse-card button, `/page`, `/reciter` + search,
  inline query, `/memorize` wizard, a group daily post.
- Deploys stay on the existing blue-green workflow; any phase reverts as one
  merge commit.

## 8. Expected result

| Metric | Now | After |
|---|---|---|
| `main.py` lines | 1,512 | < 60 |
| Largest source file | 1,512 | ~300 (`bot/features/memorize.py`, split further if still over) |
| Imports of `main` from `src/` | 2 | 0 |
| Upward imports (`lib`/`services` → `hifz`) | 6 | 0 |
| Function-local imports | 18 | 0 (except deliberate lazy loads, commented) |
| `print()` calls | 56 | 0 |
| Indentation styles | 2 | 1 (enforced) |
| Copies of cache-or-upload | 5 | 1 |
| Copies of row-chunking | 10 | 1 |
| Offset pickers | 3 | 1 |
| Places to edit to add a command | 2 (chain + menu) | 1 handler (+ locale key) |

## 9. Decisions and open questions

Decided 2026-10-29:
- **Order:** §11.1 first, then Phase 0. *(Q6: Phases 0–3 land before the
  channel seam.)*
- **Q1:** layout as in §4, with `hifz/` → `bot/features/`.
- **Q4:** ruff for both lint and format.
- **Q5:** one PR per phase, with one commit per numbered step.

Still open:

1. **Package names.** Is `app/ bot/ domain/ infra/ services/` acceptable, or do you want
   `hifz/` kept as a top-level name rather than `bot/features/`? (It's in commit
   history, docs and test names.)
2. **Python version.** Should we stay on 3.10 or move to 3.12 in Phase 6? 3.12 is faster
   and has better error messages; it needs one full-suite run plus a Pillow/asyncpg check.
3. **The tafsir PDF.** Should we untrack `Al_Jalalain_Eng.pdf`? `ATTRIBUTIONS.md` could
   link its source instead.
4. **Formatter choice.** Should we use `ruff format` (proposed; one tool for lint + format)
   or `black`?
5. **Delivery.** Should each step be its own PR, or one PR per phase? Per-step PRs are
   easier to review; per-phase PRs mean fewer merges.
6. **Order against multi-platform.** Should this plan's Phases 0–3 land before the
   WhatsApp channel seam (§4.1, recommended), or should the channel seam go first?
7. **Timezone model.** For the country picker, should we label the existing offsets
   (§11.2 option A) or move to IANA zones (option B, recommended)?

## 10. Found along the way (out of scope — behaviour changes)

These came up while verifying the plan. They're real, but fixing them changes what
users see, so they don't belong in a pure refactor. Each should be its own `fix/` PR.

- **Group setup keyboards are English-only.** `hifz/group.py:516-519` builds the
  days buttons with `t("group_btn_daily", "en")` / `t(…, "en")` instead of the
  admin's UI language.
- **The memorize offset picker labels differ** from the other two pickers:
  `"UTC+05:00"` vs `"+05:00"` (see 2.3). Pick one on purpose.
- **Two reminder-time interactions disagree.**
  - `/profile` asks the user to *type* the time, and its docstring argues
    deliberately against presets.
  - `/memorize` offers six preset buttons (`05:00` … `21:00`).

  This is a UX decision to settle, not code to merge.

## 11. User-reported problems

These change behaviour, so they're out of scope for the pure refactor. Each is
its own branch and PR. §11.1 is a bug and should ship **before** Phase 0: a
refactor on top of a store that silently loses data would only hide it.

### 11.1 Profile settings reset after a while — `fix/settings-persistence`

**Symptom.** After some time, a user's settings go back to the defaults:
interface language, translation language, reciter, timezone and reminder. So
does their reading position.

**Root cause: confirmed 2026-10-29 (cause 1).** The connection URL was stored
as a Koyeb **Secret**, but the service's environment never referenced it. A Koyeb
Secret is only visible to a service when an environment variable points at it.
So the app saw the URL as unset and ran on the in-memory store, losing everything
on each restart and redeploy.

- **Operational fix (no code):** add the environment variable(s) on the service
  that reference the existing Secrets, for the database and for Redis. Redeploy,
  then check the boot log no longer contains `falling back to in-memory`.
- **Code fix (below):** still needed. Without it, the next missing reference
  fails the same silent way.

**Possible causes** (cause 1 is confirmed; 2–4 are still real gaps that the code
fix closes):

1. **The settings store silently falls back to memory.** `config/postgres.get_pool()`
   returns `None` in two cases: when the database URL isn't configured, and when
   the server can't be reached at boot. `lib/store.get_store()` then builds an
   `InMemoryStore` for the life of the process. All profile, plan, progress and
   session rows live in that process's RAM. They're lost on every restart:
   every deploy, every push to `main` (the Koyeb service rebuilds from it),
   every crash, every time the free instance is recycled.
   - The only signal is one `WARNING` line in the boot log. The bot keeps working,
     so the problem looks like "settings reset after a while", not "database down".
2. **One failed connection at boot disables the database until the next restart.**
   `get_pool()` sets `_pool_resolved = True` even when `create_pool` raises, and
   it never retries. A serverless Postgres waking from auto-suspend (the code
   comments mention Neon) or a short network blip at boot is enough to switch
   the whole process to memory, even though the database is fine a second later.
3. **Redis has the same fallback.** `config/redis.RedisSingleton` falls back to
   `MemoryStore` when no Redis URL is configured or Redis is unreachable. Redis
   holds the reading position, wizard drafts and the media file-id cache. As of
   my July deployment notes, the Redis URL had not been set on Koyeb.
4. **The reading position expires by design.** `File.save_user` stores
   `(surah, ayah, type)` with a 2-day TTL. Even with Redis working, someone who
   doesn't open the bot for two days starts again at 1:1. If "settings" includes
   "where I was reading", this alone explains it.

**Diagnose first.** This takes one look at the logs, no code:

- Search the Koyeb runtime logs for `falling back to in-memory`. The text is the
  same for both stores, and the line says which store fell back and why
  (unset vs. unreachable).
- Confirm the database and Redis URLs are configured on the service. Check that
  they're set; don't paste them anywhere.

**Fix.**

- **Fail loudly by default.** *(done on `fix/settings-persistence`)*
  - The in-memory stores are refused unless `ALLOW_MEMORY_STORE=1` is set.
    Tests, the local `.env` and the stress stack set it; production doesn't.
  - Without the flag, a missing or unreachable database raises
    `DatabaseUnavailable`, and Redis raises `CacheUnavailable`, instead of
    degrading. That covers both the forgotten Secret reference and an outage.
- **Retry instead of caching failure.** *(done)*
  - Postgres retries 4 times with backoff and caches nothing on failure, so the
    next call reconnects.
  - Redis, whose client is synchronous, waits 30 s after a failed connect before
    trying again, so a Redis outage doesn't stall every update for the 5 s
    connect timeout.
- **Expose the state.** *(done)* `GET /` returns
  `{"status", "store", "cache"}`, where `store` is postgres/memory/unavailable/pending
  and `cache` is redis/memory/unavailable/pending. It answers **503** when either is
  unavailable; `pending` (still booting) stays 200. Redis connects at boot, so this
  is accurate straight after startup.
  - **Koyeb must use an HTTP health check on `GET /`** for a 503 to fail the
    deploy. A TCP check only sees that the port is open.
- **Make the reading position durable.** *(done)* Move `(surah, ayah, type)` from the
  2-day Redis key to a column on `user_profile`. Postgres already holds every
  other per-user setting. Redis stays for what's truly temporary: the file-id
  cache, wizard drafts and the pending-input flag.
- **Tests.**
  - A unit test that `get_pool()` retries after a first failure.
  - A test that production mode refuses to start on the in-memory store.
  - A store-contract test that the reading position survives a fresh
    `get_store()`.

**Relation to the refactor.** Phase 4.2 (typed settings) is where the
deploy-mode flag naturally lives. Phase 4.1 moves `nav_state` out of `File`. If
this fix lands first, `nav_state` simply moves to `infra/store/` instead of
`infra/nav_state.py`.

### 11.2 Timezone picker by country — `feat/timezone-by-country`

**Request.** The timezone picker shows bare offsets (`+05:00`, `−03:00`, …). Show
country names instead, the way most apps' dropdowns do: "🇺🇿 Uzbekistan
(UTC+05:00)". This applies in `/profile`, the `/memorize` wizard, group setup and
the Mini App.

**Today's design, and why.** Timezones are stored as a fixed UTC offset string
(`user_profile.timezone = '+05:00'`). `lib/localtime.py` and `schema.sql` record
this as a deliberate, approved trade-off:

- no `tzdata` dependency;
- no daylight-saving logic;
- a 34-button picker with nothing to translate.

The known cost is that users in DST countries drift by an hour twice a year
until they pick again. Ten modules read the offset: `localtime`, `streaks`,
`leaderboard`, `store/profiles`, `services/profile`, `services/plans`, the three
`hifz` features, and `api/session`.

**Option A: label the offsets (small, keeps the model).**
- Keep storing `+05:00`.
- Each picker button gets a few example countries: `+05:00 · Uzbekistan,
  Pakistan, Maldives`.
- A static `offset → [country codes]` table drives the labels, with country
  names localized per UI language and flags from the ISO code.
- No schema change, no scheduler change.
- **Limitation:** countries that use daylight saving belong to two offsets a
  year (UK `+00:00` / `+01:00`, Morocco, most of Europe and North America). They
  can only be listed under one, so the label is wrong half the year, and the
  drift problem stays.

**Option B: country → IANA zone (recommended).** This is what the request
actually describes.
- **Picker:**
  - Step 1 is the country: a paged, localized list, plus typed search
    ("uzb", "Ташкент").
  - Step 2 is the zone, shown only for multi-zone countries (US, Russia,
    Brazil, Australia, Kazakhstan, Indonesia, …). Its labels are city +
    current offset: "Almaty (UTC+05:00)".
  - Most users get a single tap, because most countries have one zone.
- **Storage:**
  - Add `user_profile.tz_name` (`'Asia/Tashkent'`).
  - Keep `timezone` as a fallback for rows not yet migrated.
  - Backfill existing rows lazily: the next time a user opens the picker, it
    preselects a country whose current offset matches their saved one.
- **One read path:**
  - `localtime.user_offset(profile, at)` returns the offset in effect at time
    `at`, via `zoneinfo.ZoneInfo(tz_name)`, falling back to the stored fixed
    offset.
  - The ten consumers call that function instead of parsing `timezone`, so the
    blast radius is one helper plus call-site edits.
  - The scheduler computes each next due time with the offset at *that* moment,
    so reminders follow DST automatically.
- **Data:**
  - `zoneinfo` is in the standard library. Add the `tzdata` pip package so slim
    images and Windows dev machines have the zone database.
  - The country → zones map comes from `zone1970.tab` / `zone.tab`, which ships
    with `tzdata`.
  - Localized country names for 48 UI languages come from CLDR. Either use
    `babel` (adds ~30 MB of locale data) or, lighter, generate a JSON of names
    per language once with a script in `scripts/` and commit it, like the
    translations bundle.
- **Mini App:** `Intl.DateTimeFormat().resolvedOptions().timeZone` gives the
  browser's IANA zone directly. The app can preselect it and ask the user to
  confirm. The bot has no equivalent, since Telegram doesn't share the user's
  timezone.
- **Callback size:** `callback_data` is capped at 64 bytes. Country codes (`uz`)
  and zone indexes fit easily; full zone names like
  `America/Argentina/ComodRivadavia` don't, so the buttons carry an index into
  the country's zone list.
- **Tests:**
  - DST transitions for streak day boundaries and the weekly leaderboard
    window. A Sunday-night DST change must not drop or double-count a day.
  - The 64-byte callback cap.
  - Localized country names present for every UI language (extend
    `scripts/check_locales.py`).

**Picking the option** is open question 7. Option B reverses a recorded design
decision, so it should also update the comments in `lib/localtime.py` and
`schema.sql`, plus the spec in `docs/HIFZ_PLATFORM.md`.

**Relation to the refactor.** Phase 2.3 merges the three offset pickers into
`bot/keyboards/time_pickers.py`. Do that first, and this feature changes one
picker instead of three.
