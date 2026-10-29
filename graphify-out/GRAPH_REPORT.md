# Graph Report - QuranAyat_bot  (2026-10-29)

## Corpus Check
- 173 files · ~200,066 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 3867 nodes · 8676 edges · 223 communities (116 shown, 107 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 751 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bb55ef69`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Wizard
- _ctx
- main.py
- memorize.py
- Profile Testing
- Recall Check Logic
- Time Timezone Handling
- Hifz Interval Testing
- api/progress.py
- User Settings Storage
- hifz/profile.py
- Reciter Picker
- streak_image.py
- Ctx
- Group Management
- Memorize Feature Tests
- .get
- test_hifz_streak.py
- Progress Command
- Progress Data Models
- Inline Range Query
- File
- Hifz Interval Storage
- Reference Parsing
- advancing
- Configuration Setup
- Scheduler Queue Engine
- Profile Data Storage
- .get_surah_length
- services/plans.py
- Stress Test Infrastructure
- Refactor — Implementation Plan
- test_hifz_check.py
- Context Building
- services/check.py
- tick
- Acceptance Testing
- Hifz Platform - Plan & Progress
- Session Leaderboard Store
- session.py
- Hifz Interval Edges
- test_verse_card.py
- Queue Processing
- Plan Storage
- Session Logging
- Core Module Imports
- test_page_mode.py
- streak.py
- test_recall_check.py
- Database Schema
- Juz Page Progress
- TestCatalogKinds
- locales/__init__.py
- .exists
- Ref
- .test_a_crash_between_send_and_mark_sent_is_the_known_window
- pytest
- Streak Computation
- BismillahBot Business Logic
- Page image stitching (lib/page_image.py)
- Surah Progress
- Store Initialization
- test_locales.py
- Juz Progress
- quran_progress
- t
- Load Testing
- Test Configuration
- PostgresGroupStore
- build_plan
- lib/utils.py File (state, file-id cache, media paths)
- catalog.py
- test_inline_reciter_search.py
- parse_quran_tafsir
- Reference Parsing Tests
- Percentage Formatting
- PostgresSessionStore
- Send Context
- In-Memory Profile Store
- PostgresProfileStore
- Handler Registration
- Plan Testing
- Plan Portion Data
- Recitation Checker — Investigation and Plan
- 5. Phases
- Streak Computation Logic
- Telegram Mini App — Implementation Plan
- build_grid
- CI/CD Pipeline
- PlanDaySpec
- Schedule Testing
- Postgres Schedule Storage
- Workflow Steps
- CI Cache Build
- pick_ayahs
- In-Memory Schedule Store
- api/check.py
- test_navigation.py
- Utility Testing
- Progress Ratio
- .get_next_ayah
- InMemoryPlanStore
- Due-Queue Scheduler
- TestSevenTheCommandsExist
- Callback Dispatching
- test_api_features.py
- Leaderboard & Rankings
- User Profiles
- Translations & Tafsir
- Image Stitching
- Scheduler Loop
- Milestone Tracking
- .page_range
- juz_ref
- Hifz Seam Integration
- Request Context
- Bot Command Infrastructure
- test_hifz_progress.py
- Deployment Configuration
- Message Sending Handler
- User Percentile Bands
- HifzInterval
- Wizard Workflows
- PostgresGroupStore
- Image Composition
- Session Tracking
- Database Configuration
- Test CI Matrix
- Deployment Preflight
- Surah Progress
- Page Progress Tracking
- Multi-Platform — Implementation Plan (WhatsApp first)
- auto_pace
- Health Check Endpoints
- Schedule Calculation
- Scheduler Testing
- User Settings
- _seed_legacy_lang
- Koyeb free-tier capacity report
- Workflow Environment
- Blue-Green Promotion
- TestTransliteration
- Workflow Triggers
- Schema Application
- Build Configuration
- Test Pool Reset
- Command Dispatching
- user_settings.py
- .preload
- stats.py
- TestRegistration
- 8. Phased task breakdown
- wizard
- unittest_mock
- check_locales.py
- button_action
- level_for
- json
- .available
- parametrize
- .search_performers
- test_export_web_content.py
- 4. Authentication
- BismillahBot Multilingual Support Plan
- _unprocessable
- normalize_lang
- BismillahBot README
- clamp_to_quran
- TestKindWarnings
- CLAUDE.md
- TestEveryParsedRefIsReal
- TestCatalogOrder
- TestRegistration

## God Nodes (most connected - your core abstractions)
1. `get_store()` - 144 edges
2. `Ctx` - 86 edges
3. `File` - 81 edges
4. `build_plan()` - 71 edges
5. `t()` - 71 edges
6. `UserSettings` - 68 edges
7. `parse_reference()` - 58 edges
8. `handle_update()` - 57 edges
9. `Ref` - 54 edges
10. `surah_ref()` - 48 edges

## Surprising Connections (you probably didn't know these)
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/hifz/__init__.py
- `Phase 3 — Hifz parity` --references--> `build_plan()`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/lib/plan_builder.py
- `In scope — feature parity map` --references--> `_download_stitched_audio()`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/main.py
- `2. Goals and non-goals` --references--> `handle_update()`  [INFERRED]
  docs/REFACTOR_PLAN.md → src/main.py
- `Phase 0 — Foundations` --references--> `require_user()`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/api/auth.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **512 MB free-tier memory budget shaping design** — multilingual_plan_koyeb_free_tier, multilingual_plan_translation_registry, business_logic_page_image_stitching, docs_hifz_platform_streaks, docs_koyeb_capacity_report_results [INFERRED 0.85]
- **Hifz daily push flow: plan builder -> scheduler due-queue -> drill delivery** — business_logic_plan_builder, business_logic_scheduler, business_logic_idempotency_key, docs_hifz_platform_plans_drills, docs_hifz_platform_scheduler [INFERRED 0.85]
- **Locale integrity enforcement across 48 locales** — scripts_check_locales, docs_hifz_strings_hard_rules, docs_hifz_platform_group_locales, readme_bot_commands, docs_translation_review_review_criteria [INFERRED 0.85]

## Communities (223 total, 107 thin omitted)

### Community 0 - "Wizard"
Cohesion: 0.06
Nodes (10): has_wizard(), Wizard, test_draft_is_written_with_that_ttl(), TestAccumulation, TestCancel, TestCoexistsWithTheReciterFlow, TestCorruptState, TestLifecycle (+2 more)

### Community 1 - "_ctx"
Cohesion: 0.07
Nodes (16): user_week_window(), week_window(), weekly_board(), _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join() (+8 more)

### Community 2 - "main.py"
Cohesion: 0.05
Nodes (51): close_pool(), app_button(), app_row(), app_url(), set_menu_button(), apply_schema(), build_data(), _commands_for() (+43 more)

### Community 3 - "memorize.py"
Cohesion: 0.09
Nodes (35): _after_days(), _ask_days(), _ask_pace(), _cancel_row(), _custom_days_keyboard(), _days_keyboard(), _expired(), _know_by_heart() (+27 more)

### Community 4 - "Profile Testing"
Cohesion: 0.08
Nodes (17): _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _isolate_registries(), _Message, _profile_row() (+9 more)

### Community 5 - "Recall Check Logic"
Cohesion: 0.08
Nodes (22): _assemble(), _ayah_text(), _basmala_prefix(), _clean(), _continuation_question(), corpus(), display_length(), _distinct() (+14 more)

### Community 6 - "Time Timezone Handling"
Cohesion: 0.06
Nodes (13): _as_utc(), format_offset(), local_date(), local_now(), local_time(), next_due_utc(), parse_offset(), TestFormatOffset (+5 more)

### Community 7 - "Hifz Interval Testing"
Cohesion: 0.07
Nodes (10): _assert_invariant(), _ayahs(), _hifz(), _spans(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order(), TestAddInterval (+2 more)

### Community 8 - "api/progress.py"
Cohesion: 0.15
Nodes (17): not_found(), surah_name(), forget(), ForgetIn, ForgetOut, _juz(), JuzRatio, progress() (+9 more)

### Community 9 - "User Settings Storage"
Cohesion: 0.15
Nodes (7): patch_settings(), UserSettings, _resolve_settings(), TestDefaults, TestIndependence, TestKeyedByUserId, TestRoundTrip

### Community 10 - "hifz/profile.py"
Cohesion: 0.07
Nodes (25): Phase 2 — DRY the duplicated patterns, patch_profile(), _cancel_keyboard(), _join_board(), name_step(), offset_from_callback(), offset_keyboard(), on_profile_tap() (+17 more)

### Community 11 - "Reciter Picker"
Cohesion: 0.07
Nodes (13): _callback(), data(), fake_bot(), _message(), _pager_row(), _reciter_buttons(), _tab_row(), TestAudioNeverFollowsLanguage (+5 more)

### Community 12 - "streak_image.py"
Cohesion: 0.15
Nodes (6): draw_contribution_graph(), render_streak_graph(), _semaphore(), open_png(), TestRendering, TestRenderStreakGraph

### Community 13 - "Ctx"
Cohesion: 0.05
Nodes (33): command, _answer_data(), _ask(), check(), on_check(), _options_keyboard(), _question_text(), _score() (+25 more)

### Community 14 - "Group Management"
Cohesion: 0.08
Nodes (25): _begin_setup(), bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), _enqueue_next_board(), _enqueue_next_group() (+17 more)

### Community 15 - "Memorize Feature Tests"
Cohesion: 0.09
Nodes (11): _CallbackQuery, _ctx(), _isolate_registries(), _Message, _run_wizard(), _Settings, _tap(), TestDrill (+3 more)

### Community 17 - "test_hifz_streak.py"
Cohesion: 0.11
Nodes (12): _caption(), _ctx(), _earn(), _isolate_registries(), _photo_message(), _Settings, _streak(), TestCallback (+4 more)

### Community 18 - "Progress Command"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 19 - "Progress Data Models"
Cohesion: 0.12
Nodes (4): Progress, summarize(), SurahProgress, TestSummarize

### Community 20 - "Inline Range Query"
Cohesion: 0.07
Nodes (15): content(), data(), fake_bot(), _inline_query(), _of_type(), public_url(), _results(), TestInlineArabicImage (+7 more)

### Community 21 - "File"
Cohesion: 0.04
Nodes (35): 1. Why, Phase 1 — Take `main.py` apart (pure moves), _post_portion(), push_group_day(), push_plan_day(), _send_drill(), _translation_text(), File (+27 more)

### Community 22 - "Hifz Interval Storage"
Cohesion: 0.08
Nodes (8): _covers(), _merge_span(), _normalize(), _overlaps(), PostgresHifzStore, _split_span(), _touches(), TestHelpers

### Community 23 - "Reference Parsing"
Cohesion: 0.09
Nodes (8): _clean(), parse_range(), parse_reference(), TestAcrossSurahs, TestFormatting, TestRejection, TestWholeSurah, TestWithinOneSurah

### Community 24 - "advancing"
Cohesion: 0.09
Nodes (7): advancing(), assert_covers_target_once(), assert_well_formed(), spans(), TestAlMulkAcceptance, TestCrossSurahTargets, TestSmallAndAwkwardTargets

### Community 25 - "Configuration Setup"
Cohesion: 0.09
Nodes (7): Environment, get_pool(), _lock(), MemoryStore, RedisSingleton, Bot, test_webhook_acks_before_initialization()

### Community 26 - "Scheduler Queue Engine"
Cohesion: 0.09
Nodes (11): catch_up(), _deliver(), idempotency_key(), _is_stale(), _release(), _resolve(), schedule_daily(), _tick() (+3 more)

### Community 28 - ".get_surah_length"
Cohesion: 0.13
Nodes (6): ayah_count(), TestAyahCount, sweep_refs(), swept(), test_short_surahs_still_get_four_distinct_options(), test_the_last_ayah_of_every_surah_produces_a_question()

### Community 29 - "services/plans.py"
Cohesion: 0.05
Nodes (45): parse_ref_or_422(), ref_out(), RefOut, active(), _build(), complete(), create(), DrillOut (+37 more)

### Community 30 - "Stress Test Infrastructure"
Cohesion: 0.06
Nodes (32): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+24 more)

### Community 31 - "Refactor — Implementation Plan"
Cohesion: 0.18
Nodes (10): 10. Found along the way (out of scope — behaviour changes), 2. Goals and non-goals, 3. Principles applied, 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, 6. Ordering, risk, size, 7. Safety net, 8. Expected result (+2 more)

### Community 32 - "test_hifz_check.py"
Cohesion: 0.10
Nodes (16): _parse_answer(), _answer_data(), _AnyDay, _ask(), _asked(), _buttons(), _callback_query(), _ctx() (+8 more)

### Community 33 - "Context Building"
Cohesion: 0.14
Nodes (14): _bot(), _ctx(), _isolate_registries(), _member(), _run_setup_to_plan(), _Settings, TestBoard, tap() (+6 more)

### Community 34 - "services/check.py"
Cohesion: 0.14
Nodes (8): build_question(), pick_ayah(), preload_corpus(), RecallQuestion, ask(), rebuild(), Score, score()

### Community 35 - "tick"
Cohesion: 0.07
Nodes (7): _lock(), registered_kinds(), send_handler(), tick(), TestRegistry, TestTheLoopSurvivesABadRow, TestTransientFailuresAreRetried

### Community 36 - "Acceptance Testing"
Cohesion: 0.12
Nodes (13): _CallbackQuery, _cmd(), _ctx(), _isolate_registries(), _Message, _run_wizard(), _save_plan(), _Settings (+5 more)

### Community 37 - "Hifz Platform - Plan & Progress"
Cohesion: 0.09
Nodes (24): Page audio (PageMp3s with stitch fallback), lib/plan_builder.build_plan (pure), Six hifz tables (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send), Repeat x3 memorization button, _download_stitched_audio, Repository store layer (src/lib/store/), Hifz Platform - Plan & Progress, Hifz data model (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send, group_*) (+16 more)

### Community 38 - "Session Leaderboard Store"
Cohesion: 0.10
Nodes (3): InMemorySessionStore, SessionRow, SessionStore

### Community 39 - "session.py"
Cohesion: 0.15
Nodes (18): init_data_max_age(), jwt_secret(), require_user(), auth_telegram(), AuthOut, me(), _me(), MeOut (+10 more)

### Community 40 - "Hifz Interval Edges"
Cohesion: 0.11
Nodes (3): _spans(), TestHifzIntervalEdges, TestHifzIntervals

### Community 41 - "test_verse_card.py"
Cohesion: 0.08
Nodes (9): _button(), _callback(), data(), fake_bot(), TestLanguageFlags, TestVerseCallbacks, TestVerseKeyboard, TestVerseText (+1 more)

### Community 42 - "Queue Processing"
Cohesion: 0.16
Nodes (7): enqueue(), _at(), _claimed_at(), _record(), TestCatchUp, TestIdempotentEnqueue, TestTick

### Community 43 - "Plan Storage"
Cohesion: 0.07
Nodes (4): PlanDayRow, PlanRow, PlanStore, PostgresPlanStore

### Community 44 - "Session Logging"
Cohesion: 0.12
Nodes (5): record_session(), SessionOutcome, TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 45 - "Core Module Imports"
Cohesion: 0.11
Nodes (6): WeeklyBoard, HifzStore, InMemoryHifzStore, InMemoryStore, LeaderboardEntry, MemoryState

### Community 46 - "test_page_mode.py"
Cohesion: 0.07
Nodes (15): main(), _buffer(), data(), fake_bot(), _stub_audio(), _stub_stitch(), stub(), TestPageAudio (+7 more)

### Community 47 - "streak.py"
Cohesion: 0.25
Nodes (5): _caption(), _send_graph(), cache_key(), StreakSummary, TestCacheKey

### Community 48 - "test_recall_check.py"
Cohesion: 0.03
Nodes (29): _nfc(), test_a_different_date_gives_a_different_question(), test_both_question_modes_show_up_in_the_sweep(), test_correct_option_is_never_a_length_outlier(), test_correct_option_is_never_the_extreme_by_a_wide_ratio(), test_correct_option_really_follows_the_prompt(), test_dates_and_iso_strings_are_interchangeable(), test_every_option_carries_the_same_word_count() (+21 more)

### Community 49 - "Database Schema"
Cohesion: 0.13
Nodes (23): group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval, hifz_interval_user_surah_idx (+15 more)

### Community 50 - "Juz Page Progress"
Cohesion: 0.11
Nodes (3): juz_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 52 - "locales/__init__.py"
Cohesion: 0.23
Nodes (5): get_language(), is_supported(), is_ui_language(), Language, TestLanguageLookup

### Community 53 - ".exists"
Cohesion: 0.12
Nodes (6): TestExists, TestRandom, TestStructure, TestSurahMeta, test_pick_ayah_handles_a_cross_surah_span(), test_the_whole_quran_is_a_valid_span()

### Community 54 - "Ref"
Cohesion: 0.06
Nodes (21): contains(), page_ref(), Ref, _validated(), _clip(), _covered(), _focus_surah(), _intersect() (+13 more)

### Community 56 - "pytest"
Cohesion: 0.09
Nodes (34): _b64url(), _b64url_decode(), decode_token(), _init_data_secret(), InvalidInitData, InvalidToken, issue_token(), _sign() (+26 more)

### Community 57 - "Streak Computation"
Cohesion: 0.17
Nodes (7): offset_of(), refresh_streaks(), streak_summary(), StreakCounts, user_offset(), user_today(), TestRefreshAndSummary

### Community 58 - "BismillahBot Business Logic"
Cohesion: 0.14
Nodes (16): BismillahBot Business Logic, Redis caching strategy (user state, file-ids, streak graph, wizard draft), Central callback prefixes hifz.PREFIXES, idempotency_key per (kind, target, local date), Inline query answering (all representations, ranges), Navigation model (surah, ayah, type) per chat_id, Issues fixed in refactor, Future roadmap (+8 more)

### Community 59 - "Page image stitching (lib/page_image.py)"
Cohesion: 0.29
Nodes (6): Page image stitching (lib/page_image.py), quran-data.xml, Structural divisions: page/juz/hizb/manzil/ruku/sajda from quran-data.xml, Workstream G: streaks & PNG contribution graph, everyayah.com CDN, Mushaf page reader (/page, /juz, /sajda)

### Community 60 - "Surah Progress"
Cohesion: 0.14
Nodes (4): started_surahs(), surah_progress(), TestSpecAcceptance, TestSurahProgress

### Community 61 - "Store Initialization"
Cohesion: 0.20
Nodes (5): get_store(), _lock(), TestFourProgress, _added_update(), TestAdded

### Community 62 - "test_locales.py"
Cohesion: 0.14
Nodes (4): missing_keys(), _placeholders(), TestGroupLocaleExemption, TestLocaleIntegrity

### Community 63 - "Juz Progress"
Cohesion: 0.16
Nodes (5): juz_progress(), JuzProgress, _spans(), started_juzs(), TestJuzProgress

### Community 65 - "t"
Cohesion: 0.10
Nodes (11): _drill_keyboard(), command_lines(), keyboard_rows(), _load_locales(), _module_name(), _reverse_button_map(), t(), welcome_text() (+3 more)

### Community 66 - "Load Testing"
Cohesion: 0.15
Nodes (11): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), _mem_to_mb(), _oom_killed() (+3 more)

### Community 67 - "Test Configuration"
Cohesion: 0.22
Nodes (7): bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 68 - "PostgresGroupStore"
Cohesion: 0.06
Nodes (6): GroupConfig, GroupMemberLink, GroupPlanDayRow, GroupPlanRow, GroupStore, InMemoryGroupStore

### Community 69 - "build_plan"
Cohesion: 0.13
Nodes (5): surah_ref(), build_plan(), TestConsolidationDays, TestDayOfWeekFiltering, TestPurity

### Community 70 - "lib/utils.py File (state, file-id cache, media paths)"
Cohesion: 0.40
Nodes (6): modules/bot.py Bot singleton, config/env.py Environment, lib/utils.py File (state, file-id cache, media paths), main.py serve loop / entrypoint, modules/quran.py Quran corpus engine, config/redis.py RedisSingleton

### Community 71 - "catalog.py"
Cohesion: 0.13
Nodes (13): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, put_position(), ReaderPosition, Reciter (+5 more)

### Community 72 - "test_inline_reciter_search.py"
Cohesion: 0.14
Nodes (19): _audio_result(), data(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter(), test_ayah_audio_dropped_without_public_base_url(), test_ayah_audio_uses_callers_reciter() (+11 more)

### Community 75 - "Percentage Formatting"
Cohesion: 0.19
Nodes (3): format_percent(), round_percent(), TestRounding

### Community 76 - "PostgresSessionStore"
Cohesion: 0.13
Nodes (3): PostgresStore, PostgresSessionStore, store()

### Community 77 - "Send Context"
Cohesion: 0.20
Nodes (3): _send_plain_message(), SendCtx, TestDailyPost

### Community 83 - "Recitation Checker — Investigation and Plan"
Cohesion: 0.07
Nodes (29): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards (+21 more)

### Community 84 - "5. Phases"
Cohesion: 0.20
Nodes (8): 5. Phases, Phase 0 — Guardrails (no code moves), Phase 3 — One router for everything, Phase 4 — Split infrastructure god-objects, Phase 5 — Fix the layering, Phase 6 — Repository hygiene, _range_audio_url(), _webhook_base_url()

### Community 85 - "Streak Computation Logic"
Cohesion: 0.23
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 86 - "Telegram Mini App — Implementation Plan"
Cohesion: 0.12
Nodes (15): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 5. API surface (`/api/v1`), 6. Frontend structure (`quranayat-miniapp`) (+7 more)

### Community 87 - "build_grid"
Cohesion: 0.18
Nodes (4): build_grid(), _counts(), Grid, TestGrid

### Community 88 - "CI/CD Pipeline"
Cohesion: 0.13
Nodes (14): concurrency, cancel-in-progress, group, env, PYTHON_DEFAULT, jobs, rollback, name (+6 more)

### Community 92 - "Workflow Steps"
Cohesion: 0.23
Nodes (13): steps, steps, steps, steps, steps, steps, env, id (+5 more)

### Community 93 - "CI Cache Build"
Cohesion: 0.15
Nodes (13): with, cache, cache-dependency-path, cache-from, cache-to, context, if-no-files-found, load (+5 more)

### Community 94 - "pick_ayahs"
Cohesion: 0.20
Nodes (5): _at_offset(), _date_key(), pick_ayahs(), _span_length(), _span_tuple()

### Community 96 - "api/check.py"
Cohesion: 0.16
Nodes (9): answer(), AnswerIn, AnswerOut, make_token(), question(), QuestionOut, read_token(), _secret() (+1 more)

### Community 97 - "test_navigation.py"
Cohesion: 0.12
Nodes (9): data(), fake_bot(), _message(), _no_network(), TestCommandArguments, TestJuzCommand, TestPageCommand, TestSajdaCommand (+1 more)

### Community 98 - "Utility Testing"
Cohesion: 0.12
Nodes (4): TestAudioFilename, TestImageFilename, TestLegacyLanguageKey, TestStateStore

### Community 105 - "test_api_features.py"
Cohesion: 0.14
Nodes (20): client(), _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today() (+12 more)

### Community 108 - "Translations & Tafsir"
Cohesion: 0.22
Nodes (8): alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Husary recitation (AUDIO_BASE_URL), Four ayah representations (english/tafsir/arabic/audio), Tafsir al-Jalalayn, Locale review tracking table (47 locales)

### Community 109 - "Image Stitching"
Cohesion: 0.25
Nodes (4): fetch_and_stitch(), _fit_for_telegram(), _semaphore(), stitch_images()

### Community 110 - "Scheduler Loop"
Cohesion: 0.25
Nodes (3): run_scheduler(), _wait(), TestRunScheduler

### Community 111 - "Milestone Tracking"
Cohesion: 0.25
Nodes (4): Milestone, milestone_for(), _milestone_key(), TestMilestones

### Community 112 - ".page_range"
Cohesion: 0.10
Nodes (3): Quran, test_page_boundaries_match_the_bot(), TestDivisionsTileTheQuran

### Community 113 - "juz_ref"
Cohesion: 0.15
Nodes (5): juz_ref(), to_day_specs(), TestSurahSpans, TestJuzAndPage, TestStorageShape

### Community 114 - "Hifz Seam Integration"
Cohesion: 0.18
Nodes (3): _isolate_registries(), _Settings, TestPrefixNamespace

### Community 118 - "Deployment Configuration"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 119 - "Message Sending Handler"
Cohesion: 0.20
Nodes (4): register_send_handler(), _same_origin(), decorate(), handler()

### Community 126 - "Database Configuration"
Cohesion: 0.22
Nodes (9): POSTGRES_DB, POSTGRES_HOST_AUTH_METHOD, POSTGRES_USER, env, image, options, ports, postgres (+1 more)

### Community 127 - "Test CI Matrix"
Cohesion: 0.22
Nodes (9): TEST_DATABASE_URL, test, python-version, fail-fast, matrix, env, name, runs-on (+1 more)

### Community 128 - "Deployment Preflight"
Cohesion: 0.22
Nodes (9): preflight, active, deploy_enabled, target, if, name, needs, outputs (+1 more)

### Community 129 - "Surah Progress"
Cohesion: 0.24
Nodes (3): load_summary(), ProgressSummary, TestLoadSummary

### Community 131 - "Multi-Platform — Implementation Plan (WhatsApp first)"
Cohesion: 0.08
Nodes (25): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+17 more)

### Community 133 - "Health Check Endpoints"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 134 - "Schedule Calculation"
Cohesion: 0.29
Nodes (3): _advance(), next_scheduled_date(), _validated_days()

### Community 135 - "Scheduler Testing"
Cohesion: 0.32
Nodes (3): _isolate_handlers(), state(), store()

### Community 137 - "_seed_legacy_lang"
Cohesion: 0.21
Nodes (3): _seed_legacy_lang(), TestInlineCaller, TestLegacyMigration

### Community 138 - "Koyeb free-tier capacity report"
Cohesion: 0.14
Nodes (14): In-process MemoryStore fallback, Phase 1 acceptance criteria (tests/test_acceptance.py), claim_due claimed_at clock bug, tests/test_store_contract.py (both storage legs, CI postgres:16), Koyeb free-tier capacity report, CPU-bound queueing failure mode (~24 msg/s ceiling), Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start), Capacity results 5-1000 concurrent (no errors, 70-91 MB) (+6 more)

### Community 139 - "Workflow Environment"
Cohesion: 0.33
Nodes (6): environment, if, name, needs, runs-on, deploy-green

### Community 140 - "Blue-Green Promotion"
Cohesion: 0.33
Nodes (6): promote, environment, if, name, needs, runs-on

### Community 142 - "Workflow Triggers"
Cohesion: 0.40
Nodes (5): on, pull_request, push, workflow_dispatch, branches

### Community 144 - "Build Configuration"
Cohesion: 0.50
Nodes (4): name, needs, runs-on, build

### Community 149 - "stats.py"
Cohesion: 0.18
Nodes (10): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut (+2 more)

### Community 151 - "8. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 8. Phased task breakdown, Phase 0 — Foundations, Phase 1 — Service-layer extraction (this repo, no UI change), Phase 2 — Reader parity (read-only, low risk, ships first), Phase 3 — Hifz parity, Phase 4 — Recitation checker UI (depends on the investigation's Phase A), Phase 5 — Later

### Community 152 - "wizard"
Cohesion: 0.33
Nodes (5): decorate(), decorate(), _same_origin(), wizard(), decorate()

### Community 154 - "check_locales.py"
Cohesion: 0.14
Nodes (12): Workstream I: i18n & commands for 48 locales, Hifz platform frozen string manifest, src/locales/en.py source of truth, 111 hifz string keys by workstream, Key conventions (btn_*, cmd_*), Wave process (feature agents, translation agents, reviewers), Review criteria (meaning, register, grammatical number, RTL, button length), BOT_COMMANDS single source of truth (+4 more)

### Community 157 - "json"
Cohesion: 0.10
Nodes (19): _clean_state_store(), export(), languages(), main(), resolved_table(), _write(), build(), main_() (+11 more)

### Community 161 - "test_export_web_content.py"
Cohesion: 0.14
Nodes (10): _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl(), _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah() (+2 more)

### Community 162 - "4. Authentication"
Cohesion: 0.50
Nodes (4): 4.1 Flow, 4.2 Rules, 4.3 Transport, 4. Authentication

### Community 163 - "BismillahBot Multilingual Support Plan"
Cohesion: 0.18
Nodes (12): Hifz risks, Neon managed Postgres, Stress environment (docker-compose.stress.yml, cpus 0.1, 512m), BismillahBot Multilingual Support Plan, Four multilingual dimensions (UI, translation, tafsir, audio), Koyeb free instance (512 MB, 0.1 vCPU), /language command + callback handler (setlang:), Per-user language preference (lang:{chat_id}, auto-detect) (+4 more)

### Community 167 - "BismillahBot README"
Cohesion: 0.20
Nodes (9): Translation Attributions, Audio catalog kinds (recitation/riwayah/translation), Reciter picker paging (recpage:), Translation-only catalogue entries / UI_LANGUAGES, BismillahBot README, GNU AGPL v3 license, Configuration env vars (TOKEN, REDIS_HOST_URL, AUDIO_BASE_URL, PHOTO_BASE_URL, PAGE_IMAGE_BASE_URL, WEBHOOK_URL), 48 languages with complete UI string tables (+1 more)

## Knowledge Gaps
- **26 isolated node(s):** `alquran.cloud API`, `Husary recitation (AUDIO_BASE_URL)`, `Tafsir al-Jalalayn`, `claim_due claimed_at clock bug`, `/streak and /leaderboard (opt-in boards)` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1340 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **107 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `Store Initialization` to `_ctx`, `main.py`, `Surah Progress`, `Profile Testing`, `Hifz Interval Testing`, `api/progress.py`, `User Settings Storage`, `hifz/profile.py`, `streak_image.py`, `Ctx`, `Memorize Feature Tests`, `test_hifz_streak.py`, `Progress Command`, `user_settings.py`, `Progress Data Models`, `stats.py`, `File`, `Configuration Setup`, `Scheduler Queue Engine`, `services/plans.py`, `test_hifz_check.py`, `Context Building`, `tick`, `Acceptance Testing`, `session.py`, `Session Logging`, `Core Module Imports`, `Streak Computation`, `Surah Progress`, `PostgresSessionStore`, `Send Context`, `api/check.py`, `Due-Queue Scheduler`, `test_api_features.py`, `test_hifz_progress.py`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `Ctx` (e.g. with `3. Architecture` and `Phase 1 — Channel seam (this repo, no user-visible change)`) actually correct?**
  _`Ctx` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `alquran.cloud API`, `Husary recitation (AUDIO_BASE_URL)`, `Tafsir al-Jalalayn` to the rest of the system?**
  _26 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Wizard` be split into smaller, more focused modules?**
  _Cohesion score 0.06298904538341157 - nodes in this community are weakly interconnected._
- **Why does `File` connect `File` to `Wizard`, `_ctx`, `main.py`, `Profile Testing`, `User Settings Storage`, `_seed_legacy_lang`, `Reciter Picker`, `Group Management`, `Memorize Feature Tests`, `test_hifz_streak.py`, `Progress Command`, `user_settings.py`, `Inline Range Query`, `Configuration Setup`, `Scheduler Queue Engine`, `json`, `.search_performers`, `test_hifz_check.py`, `Context Building`, `tick`, `Acceptance Testing`, `session.py`, `._lang_key`, `test_page_mode.py`, `TestCatalogKinds`, `catalog.py`, `Utility Testing`, `TestCatalogOrder`, `test_api_features.py`, `Request Context`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `File` (e.g. with `_clean_state_store()` and `get_position()`) actually correct?**
  _`File` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Should `_ctx` be split into smaller, more focused modules?**
  _Cohesion score 0.06641604010025062 - nodes in this community are weakly interconnected._