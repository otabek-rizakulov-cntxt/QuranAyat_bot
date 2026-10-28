# Graph Report - QuranAyat_bot  (2026-10-29)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 3421 nodes · 7417 edges · 219 communities (108 shown, 111 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 608 edges (avg confidence: 0.88)
- Token cost: 102,551 input · 13,314 output

## Graph Freshness
- Built from commit: `784b6c62`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Draft Wizard System
- Weekly Leaderboard
- App Initialization
- Setup Context Handler
- Profile Testing
- Recall Check Logic
- Time Timezone Handling
- Hifz Interval Testing
- Memorization Drilling
- User Settings Storage
- Profile Reminder Setup
- Reciter Picker
- Activity Contribution Graph
- Callback Dispatch System
- Group Management
- Memorize Feature Tests
- Quran Corpus Data
- Streak Tracking
- Progress Command
- Progress Data Models
- Inline Range Query
- File Media Storage
- Hifz Interval Storage
- Reference Parsing
- Plan Building Engine
- Configuration Setup
- Scheduler Queue Engine
- Profile Data Storage
- Mushaf Page Handling
- Reference Validation
- Stress Test Infrastructure
- State Management
- Check Answer Handling
- Context Building
- Check Command System
- Send Queue Handler
- Acceptance Testing
- Hifz Data Model
- Session Leaderboard Store
- Plan Days Portions
- Hifz Interval Edges
- Stress Testing App
- Queue Processing
- Plan Storage
- Session Logging
- Core Module Imports
- Audio Stitching
- Progress Command
- Recall Check Testing
- Database Schema
- Juz Page Progress
- Reciter Catalog
- Localization System
- Quran Reference Validation
- Reference Range Logic
- Daily Schedule Queue
- Hifz Store Interface
- Streak Computation
- Bot Architecture
- Audio Media Handling
- Surah Progress
- Store Initialization
- Keyboard Localization
- Juz Progress
- Quran Progress
- Postgres Store
- Load Testing
- Test Configuration
- Group Plan Storage
- Postgres Profile Storage
- Core Infrastructure
- Page Mode Testing
- Ayah Count Logic
- In-Memory Group Store
- Reference Parsing Tests
- Percentage Formatting
- Auto Pace Calculation
- Send Context
- In-Memory Profile Store
- Answer Scoring
- Handler Registration
- Plan Testing
- Plan Portion Data
- Juz Page References
- Plan Group Testing
- Streak Computation Logic
- Audio Fetching
- Internationalization System
- CI/CD Pipeline
- Postgres Plan Storage
- Schedule Testing
- Postgres Schedule Storage
- Workflow Steps
- CI Cache Build
- Reference Formatting
- In-Memory Schedule Store
- Verse Navigation
- Command Testing
- Utility Testing
- Progress Ratio
- Group Plan Management
- In-Memory Plan Storage
- Due-Queue Scheduler
- Command Registration
- Callback Dispatching
- Navigation Structure
- Leaderboard & Rankings
- User Profiles
- Translations & Tafsir
- Image Stitching
- Scheduler Loop
- Milestone Tracking
- Button Action Mapping
- Language Locales
- Hifz Seam Integration
- Request Context
- Bot Command Infrastructure
- Verse Navigation UI
- Deployment Configuration
- Message Sending Handler
- User Percentile Bands
- Translation Registry
- Wizard Workflows
- Audio Serving
- Image Composition
- Session Tracking
- Database Configuration
- Test CI Matrix
- Deployment Preflight
- Surah Progress
- Page Progress Tracking
- Group Configuration
- Language Normalization
- Health Check Endpoints
- Schedule Calculation
- Scheduler Testing
- User Settings
- Group Daily Planning
- Test Acceptance
- Workflow Environment
- Blue-Green Promotion
- Test Data Generation
- Workflow Triggers
- Schema Application
- Build Configuration
- Test Pool Reset
- Command Dispatching
- Handler Registration
- Group Membership
- Callback & Wizard Registration
- Command & Wizard Registration
- Text Normalization
- Test Fixtures
- Ayah References
- Quiz Answer Selection
- Text Comparison
- Quiz Validation
- Text Mode Handling
- Quiz Mode Coverage
- Short Ayah Handling
- Prompt Truncation
- Option Distraction
- Question Reproducibility
- Date Variation
- Randomness Isolation
- Answer Distribution
- Reference Formatting
- Text Escaping
- Parse Caching
- Answer Length Analysis
- Answer Value Analysis

## God Nodes (most connected - your core abstractions)
1. `get_store()` - 120 edges
2. `Ctx` - 82 edges
3. `File` - 73 edges
4. `build_plan()` - 69 edges
5. `t()` - 67 edges
6. `UserSettings` - 62 edges
7. `parse_reference()` - 55 edges
8. `handle_update()` - 50 edges
9. `surah_ref()` - 48 edges
10. `enqueue()` - 46 edges

## Surprising Connections (you probably didn't know these)
- `Workstream A: repository layer replacing FakePostgresPool` --semantically_similar_to--> `Repository store layer (src/lib/store/)`  [INFERRED] [semantically similar]
  docs/HIFZ_PLATFORM.md → BUSINESS_LOGIC.md
- `Telegram API mocked via AsyncMock(spec=telegram.Bot)` --semantically_similar_to--> `conftest.py (in-memory store, AsyncMock bot)`  [INFERRED] [semantically similar]
  docs/KOYEB_CAPACITY_REPORT.md → TESTING.md
- `TestOneSetUpAPlan` --uses--> `Wizard`  [INFERRED]
  tests/test_acceptance.py → src/lib/wizard.py
- `TestWizard` --uses--> `Wizard`  [INFERRED]
  tests/test_hifz_memorize.py → src/lib/wizard.py
- `TestCoexistsWithTheReciterFlow` --uses--> `File`  [INFERRED]
  tests/test_wizard.py → src/lib/utils.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **512 MB free-tier memory budget shaping design** — multilingual_plan_koyeb_free_tier, multilingual_plan_translation_registry, business_logic_page_image_stitching, docs_hifz_platform_streaks, docs_koyeb_capacity_report_results [INFERRED 0.85]
- **Hifz daily push flow: plan builder -> scheduler due-queue -> drill delivery** — business_logic_plan_builder, business_logic_scheduler, business_logic_idempotency_key, docs_hifz_platform_plans_drills, docs_hifz_platform_scheduler [INFERRED 0.85]
- **Locale integrity enforcement across 48 locales** — scripts_check_locales, docs_hifz_strings_hard_rules, docs_hifz_platform_group_locales, readme_bot_commands, docs_translation_review_review_criteria [INFERRED 0.85]

## Communities (219 total, 111 thin omitted)

### Community 0 - "Draft Wizard System"
Cohesion: 0.06
Nodes (10): has_wizard(), Wizard, test_draft_is_written_with_that_ttl(), TestAccumulation, TestCancel, TestCoexistsWithTheReciterFlow, TestCorruptState, TestLifecycle (+2 more)

### Community 1 - "Weekly Leaderboard"
Cohesion: 0.05
Nodes (21): user_week_window(), week_window(), weekly_board(), WeeklyBoard, week_bounds(), offset_of(), user_offset(), _CallbackQuery (+13 more)

### Community 2 - "App Initialization"
Cohesion: 0.06
Nodes (46): close_pool(), apply_schema(), _commands_for(), _initialize(), on_shutdown(), on_startup(), _range_audio_url(), _set_bot_commands() (+38 more)

### Community 3 - "Setup Context Handler"
Cohesion: 0.11
Nodes (30): on_group_tap(), setup_step(), _step_post_time(), _step_target(), _step_topic(), _cancel(), Ctx, dispatch_wizard() (+22 more)

### Community 4 - "Profile Testing"
Cohesion: 0.08
Nodes (17): _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _isolate_registries(), _Message, _profile_row() (+9 more)

### Community 5 - "Recall Check Logic"
Cohesion: 0.06
Nodes (27): _assemble(), _at_offset(), _ayah_text(), _basmala_prefix(), _clean(), _continuation_question(), _date_key(), display_length() (+19 more)

### Community 6 - "Time Timezone Handling"
Cohesion: 0.06
Nodes (12): _as_utc(), format_offset(), local_now(), local_time(), next_due_utc(), parse_offset(), TestFormatOffset, TestLocalDate (+4 more)

### Community 7 - "Hifz Interval Testing"
Cohesion: 0.07
Nodes (10): _assert_invariant(), _ayahs(), _hifz(), _spans(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order(), TestAddInterval (+2 more)

### Community 8 - "Memorization Drilling"
Cohesion: 0.07
Nodes (29): _post_portion(), _ask_pace(), _cancel_row(), _custom_days_keyboard(), _day_position(), _days_keyboard(), _drill_keyboard(), memorize() (+21 more)

### Community 9 - "User Settings Storage"
Cohesion: 0.11
Nodes (10): SettingsRow, UserSettings, _resolve_settings(), _seed_legacy_lang(), TestDefaults, TestIndependence, TestInlineCaller, TestKeyedByUserId (+2 more)

### Community 10 - "Profile Reminder Setup"
Cohesion: 0.08
Nodes (22): wizard(), _cancel_keyboard(), format_reminder_time(), name_step(), next_push_utc(), offset_from_callback(), offset_keyboard(), on_profile_tap() (+14 more)

### Community 11 - "Reciter Picker"
Cohesion: 0.06
Nodes (13): _callback(), data(), fake_bot(), _message(), _pager_row(), _reciter_buttons(), _tab_row(), TestCurrentReciter (+5 more)

### Community 12 - "Activity Contribution Graph"
Cohesion: 0.07
Nodes (12): build_grid(), _counts(), draw_contribution_graph(), Grid, level_for(), render_streak_graph(), _semaphore(), open_png() (+4 more)

### Community 13 - "Callback Dispatch System"
Cohesion: 0.07
Nodes (22): callback(), decorate(), command(), decorate(), dispatch_callback(), dispatch_command(), handles(), handles_callback() (+14 more)

### Community 14 - "Group Management"
Cohesion: 0.06
Nodes (26): _begin_setup(), bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), _enqueue_next_board(), _enqueue_next_group() (+18 more)

### Community 15 - "Memorize Feature Tests"
Cohesion: 0.09
Nodes (11): _CallbackQuery, _ctx(), _isolate_registries(), _Message, _run_wizard(), _Settings, _tap(), TestDrill (+3 more)

### Community 16 - "Quran Corpus Data"
Cohesion: 0.07
Nodes (8): corpus(), build_data(), get_default_query_results(), Quran, TranslationRegistry, TestCorpusIntegrity, test_the_basmala_heading_is_not_part_of_the_question(), TestCaching

### Community 17 - "Streak Tracking"
Cohesion: 0.10
Nodes (14): cache_key(), _caption(), _ctx(), _earn(), _isolate_registries(), _photo_message(), _Settings, _streak() (+6 more)

### Community 18 - "Progress Command"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 19 - "Progress Data Models"
Cohesion: 0.07
Nodes (5): Progress, ProgressSummary, summarize(), HifzInterval, TestSummarize

### Community 20 - "Inline Range Query"
Cohesion: 0.11
Nodes (11): data(), fake_bot(), _inline_query(), _of_type(), public_url(), _results(), TestInlineArabicImage, TestRangeAudio (+3 more)

### Community 21 - "File Media Storage"
Cohesion: 0.08
Nodes (10): File, _combined_audio_key(), _inline_audio_result(), _inline_photo_results(), reciter_kind(), reciter_set_confirmation(), _ref_key(), send_file() (+2 more)

### Community 22 - "Hifz Interval Storage"
Cohesion: 0.08
Nodes (8): _covers(), _merge_span(), _normalize(), _overlaps(), PostgresHifzStore, _split_span(), _touches(), TestHelpers

### Community 23 - "Reference Parsing"
Cohesion: 0.08
Nodes (10): _clean(), parse_range(), parse_reference(), parse_ayah(), parse_ayah_range(), TestSurahSpans, TestAcrossSurahs, TestRejection (+2 more)

### Community 24 - "Plan Building Engine"
Cohesion: 0.12
Nodes (6): surah_ref(), build_plan(), TestConsolidationDays, TestDayOfWeekFiltering, TestPurity, TestStorageShape

### Community 25 - "Configuration Setup"
Cohesion: 0.09
Nodes (7): Environment, get_pool(), _lock(), MemoryStore, RedisSingleton, Bot, test_webhook_acks_before_initialization()

### Community 26 - "Scheduler Queue Engine"
Cohesion: 0.09
Nodes (11): catch_up(), _deliver(), idempotency_key(), _is_stale(), _lock(), _release(), _resolve(), _tick() (+3 more)

### Community 27 - "Profile Data Storage"
Cohesion: 0.07
Nodes (3): ProfileRow, ProfileStore, UserSettingsRow

### Community 28 - "Mushaf Page Handling"
Cohesion: 0.08
Nodes (5): _page_caption(), page_keyboard(), send_page(), send_page_audio(), TestDivisionsTileTheQuran

### Community 29 - "Reference Validation"
Cohesion: 0.08
Nodes (8): clamp_to_quran(), _validated(), _consolidations(), _division_marks(), make_index(), parse_quran(), parse_quran_tafsir(), TestContainsAndClamp

### Community 30 - "Stress Test Infrastructure"
Cohesion: 0.06
Nodes (32): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+24 more)

### Community 31 - "State Management"
Cohesion: 0.07
Nodes (14): _as_int(), handle_update(), language_keyboard(), _nav_labels(), _process_update(), reciter_catalog(), reciter_group(), reciter_keyboard() (+6 more)

### Community 32 - "Check Answer Handling"
Cohesion: 0.12
Nodes (11): _parse_answer(), _AnyDay, _ask(), _asked(), _buttons(), _callback_query(), _ctx(), _isolate_registries() (+3 more)

### Community 33 - "Context Building"
Cohesion: 0.16
Nodes (13): _bot(), _ctx(), _isolate_registries(), _member(), _run_setup_to_plan(), _Settings, tap(), TestBoardJoin (+5 more)

### Community 34 - "Check Command System"
Cohesion: 0.10
Nodes (11): _answer_data(), _ask(), check(), _default_span(), on_check(), _options_keyboard(), _question_text(), _score() (+3 more)

### Community 35 - "Send Queue Handler"
Cohesion: 0.08
Nodes (3): send_handler(), TestTheLoopSurvivesABadRow, TestTransientFailuresAreRetried

### Community 36 - "Acceptance Testing"
Cohesion: 0.11
Nodes (13): _CallbackQuery, _cmd(), _ctx(), _isolate_registries(), _Message, _run_wizard(), _save_plan(), _Settings (+5 more)

### Community 37 - "Hifz Data Model"
Cohesion: 0.08
Nodes (25): Page audio (PageMp3s with stitch fallback), lib/plan_builder.build_plan (pure), Six hifz tables (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send), modules/quran.py Quran corpus engine, Repeat x3 memorization button, _download_stitched_audio, Repository store layer (src/lib/store/), Hifz Platform - Plan & Progress (+17 more)

### Community 38 - "Session Leaderboard Store"
Cohesion: 0.10
Nodes (4): InMemorySessionStore, LeaderboardEntry, SessionRow, SessionStore

### Community 39 - "Plan Days Portions"
Cohesion: 0.11
Nodes (6): advancing(), assert_covers_target_once(), assert_well_formed(), spans(), TestAlMulkAcceptance, TestSmallAndAwkwardTargets

### Community 40 - "Hifz Interval Edges"
Cohesion: 0.11
Nodes (3): _spans(), TestHifzIntervalEdges, TestHifzIntervals

### Community 41 - "Stress Testing App"
Cohesion: 0.09
Nodes (8): _stress_reset(), _stress_stats(), _callback(), data(), fake_bot(), TestVerseCallbacks, TestVerseText, tg_bot()

### Community 42 - "Queue Processing"
Cohesion: 0.17
Nodes (7): enqueue(), tick(), _claimed_at(), _record(), TestCatchUp, TestRegistry, TestTick

### Community 43 - "Plan Storage"
Cohesion: 0.09
Nodes (3): PlanDayRow, PlanRow, PlanStore

### Community 44 - "Session Logging"
Cohesion: 0.12
Nodes (5): record_session(), SessionOutcome, TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 46 - "Audio Stitching"
Cohesion: 0.14
Nodes (9): main(), _buffer(), _stub_audio(), _stub_stitch(), stub(), TestPageCard, capture(), counting() (+1 more)

### Community 47 - "Progress Command"
Cohesion: 0.12
Nodes (12): command, _ref_from_draft(), _target_kind(), forgot_command(), on_progress_tap(), progress_command(), progress_view(), _show() (+4 more)

### Community 48 - "Recall Check Testing"
Cohesion: 0.09
Nodes (9): test_dates_and_iso_strings_are_interchangeable(), test_long_ayah_prompt_and_options_stay_button_sized(), test_muqattaat_get_muqattaat_shaped_distractors(), test_pick_ayah_is_deterministic_per_user_and_date(), test_pick_ayah_on_an_inverted_or_empty_span(), test_pick_then_build_is_the_whole_check_flow(), test_sweep_produces_a_well_formed_question_everywhere(), test_the_first_and_last_ayah_of_the_quran() (+1 more)

### Community 49 - "Database Schema"
Cohesion: 0.13
Nodes (23): group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval, hifz_interval_user_surah_idx (+15 more)

### Community 50 - "Juz Page Progress"
Cohesion: 0.13
Nodes (4): juz_page_progress(), quran_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 51 - "Reciter Catalog"
Cohesion: 0.11
Nodes (3): TestCatalogKinds, TestCatalogOrder, TestSearch

### Community 52 - "Localization System"
Cohesion: 0.12
Nodes (8): _load_locales(), _module_name(), get_language(), is_supported(), is_ui_language(), Language, TestLanguageLookup, TestLanguageFlags

### Community 53 - "Quran Reference Validation"
Cohesion: 0.10
Nodes (7): TestEveryParsedRefIsReal, TestExists, TestRandom, TestStructure, TestSurahMeta, test_pick_ayah_handles_a_cross_surah_span(), test_the_whole_quran_is_a_valid_span()

### Community 54 - "Reference Range Logic"
Cohesion: 0.14
Nodes (9): contains(), _clip(), _covered(), _focus_surah(), _intersect(), _page_share(), _pages_of(), _recency_key() (+1 more)

### Community 55 - "Daily Schedule Queue"
Cohesion: 0.15
Nodes (4): schedule_daily(), _at(), TestIdempotentEnqueue, TestRestartDeliversExactlyOnce

### Community 56 - "Hifz Store Interface"
Cohesion: 0.10
Nodes (4): HifzStore, InMemoryHifzStore, InMemoryStore, Store

### Community 57 - "Streak Computation"
Cohesion: 0.19
Nodes (6): refresh_streaks(), streak_summary(), StreakCounts, StreakSummary, user_today(), TestRefreshAndSummary

### Community 58 - "Bot Architecture"
Cohesion: 0.11
Nodes (19): BismillahBot Business Logic, Redis caching strategy (user state, file-ids, streak graph, wizard draft), Central callback prefixes hifz.PREFIXES, idempotency_key per (kind, target, local date), Inline query answering (all representations, ranges), In-process MemoryStore fallback, Navigation model (surah, ayah, type) per chat_id, Reciter picker paging (recpage:) (+11 more)

### Community 59 - "Audio Media Handling"
Cohesion: 0.11
Nodes (17): Audio catalog kinds (recitation/riwayah/translation), Page image stitching (lib/page_image.py), quran-data.xml, Structural divisions: page/juz/hizb/manzil/ruku/sajda from quran-data.xml, Workstream G: streaks & PNG contribution graph, Koyeb free-tier capacity report, CPU-bound queueing failure mode (~24 msg/s ceiling), Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start) (+9 more)

### Community 60 - "Surah Progress"
Cohesion: 0.14
Nodes (4): started_surahs(), surah_progress(), TestSpecAcceptance, TestSurahProgress

### Community 61 - "Store Initialization"
Cohesion: 0.17
Nodes (6): get_store(), _lock(), TestFourProgress, _added_update(), TestAdded, TestBoard

### Community 62 - "Keyboard Localization"
Cohesion: 0.12
Nodes (5): keyboard_rows(), missing_keys(), _placeholders(), TestGroupLocaleExemption, TestLocaleIntegrity

### Community 63 - "Juz Progress"
Cohesion: 0.16
Nodes (5): juz_progress(), JuzProgress, _spans(), started_juzs(), TestJuzProgress

### Community 64 - "Quran Progress"
Cohesion: 0.13
Nodes (4): quran_progress(), _at(), TestInputHandling, TestQuranProgress

### Community 65 - "Postgres Store"
Cohesion: 0.13
Nodes (3): PostgresStore, PostgresSessionStore, store()

### Community 66 - "Load Testing"
Cohesion: 0.20
Nodes (9): batch(), _container_alive(), _docker_stats(), _fire_one(), _mem_to_mb(), _oom_killed(), _pctile(), run_tier() (+1 more)

### Community 67 - "Test Configuration"
Cohesion: 0.15
Nodes (8): _clean_state_store(), bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 70 - "Core Infrastructure"
Cohesion: 0.13
Nodes (17): modules/bot.py Bot singleton, config/env.py Environment, lib/utils.py File (state, file-id cache, media paths), main.py serve loop / entrypoint, Inline verse card (edit in place), Hifz risks, Neon managed Postgres, Stress environment (docker-compose.stress.yml, cpus 0.1, 512m) (+9 more)

### Community 71 - "Page Mode Testing"
Cohesion: 0.12
Nodes (6): data(), fake_bot(), TestPageAudio, TestPageKeyboard, TestStitchedAudioAcrossSurahs, tg_bot()

### Community 72 - "Ayah Count Logic"
Cohesion: 0.16
Nodes (5): ayah_count(), TestAyahCount, sweep_refs(), test_short_surahs_still_get_four_distinct_options(), test_the_last_ayah_of_every_surah_produces_a_question()

### Community 75 - "Percentage Formatting"
Cohesion: 0.19
Nodes (3): format_percent(), round_percent(), TestRounding

### Community 76 - "Auto Pace Calculation"
Cohesion: 0.16
Nodes (3): auto_pace(), TestAcrossTheWholeQuran, TestAutoPace

### Community 77 - "Send Context"
Cohesion: 0.20
Nodes (3): _send_plain_message(), SendCtx, TestDailyPost

### Community 79 - "Answer Scoring"
Cohesion: 0.26
Nodes (5): _answer_data(), _sessions(), _tap(), TestScoring, TestStaleButtons

### Community 82 - "Plan Portion Data"
Cohesion: 0.19
Nodes (3): _portion_label(), Portion, TestPortionShape

### Community 83 - "Juz Page References"
Cohesion: 0.19
Nodes (4): juz_ref(), page_ref(), TestJuzAndPage, TestCrossSurahTargets

### Community 85 - "Streak Computation Logic"
Cohesion: 0.27
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 86 - "Audio Fetching"
Cohesion: 0.13
Nodes (5): _download_combined_audio(), _download_stitched_audio(), health(), range_audio(), TestAudioNeverFollowsLanguage

### Community 87 - "Internationalization System"
Cohesion: 0.18
Nodes (12): Translation-only catalogue entries / UI_LANGUAGES, Workstream I: i18n & commands for 48 locales, Hifz platform frozen string manifest, src/locales/en.py source of truth, 111 hifz string keys by workstream, Key conventions (btn_*, cmd_*), Wave process (feature agents, translation agents, reviewers), Review criteria (meaning, register, grammatical number, RTL, button length) (+4 more)

### Community 88 - "CI/CD Pipeline"
Cohesion: 0.13
Nodes (14): concurrency, cancel-in-progress, group, env, PYTHON_DEFAULT, jobs, rollback, name (+6 more)

### Community 92 - "Workflow Steps"
Cohesion: 0.23
Nodes (13): steps, steps, steps, steps, steps, steps, env, id (+5 more)

### Community 93 - "CI Cache Build"
Cohesion: 0.15
Nodes (13): with, cache, cache-dependency-path, cache-from, cache-to, context, if-no-files-found, load (+5 more)

### Community 96 - "Verse Navigation"
Cohesion: 0.24
Nodes (3): verse_keyboard(), mode_button(), TestNavigation

### Community 97 - "Command Testing"
Cohesion: 0.21
Nodes (4): _message(), TestJuzCommand, TestPageCommand, TestSajdaCommand

### Community 98 - "Utility Testing"
Cohesion: 0.15
Nodes (3): TestAudioFilename, TestImageFilename, TestStateStore

### Community 103 - "Command Registration"
Cohesion: 0.18
Nodes (4): command_lines(), welcome_text(), TestSevenTheCommandsExist, TestWelcomeText

### Community 105 - "Navigation Structure"
Cohesion: 0.21
Nodes (5): data(), fake_bot(), _no_network(), TestCommandArguments, tg_bot()

### Community 108 - "Translations & Tafsir"
Cohesion: 0.18
Nodes (9): Translation Attributions, alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Husary recitation (AUDIO_BASE_URL), Four ayah representations (english/tafsir/arabic/audio), Tafsir al-Jalalayn (+1 more)

### Community 109 - "Image Stitching"
Cohesion: 0.25
Nodes (4): fetch_and_stitch(), _fit_for_telegram(), _semaphore(), stitch_images()

### Community 110 - "Scheduler Loop"
Cohesion: 0.25
Nodes (3): run_scheduler(), _wait(), TestRunScheduler

### Community 111 - "Milestone Tracking"
Cohesion: 0.25
Nodes (4): Milestone, milestone_for(), _milestone_key(), TestMilestones

### Community 112 - "Button Action Mapping"
Cohesion: 0.27
Nodes (3): button_action(), _reverse_button_map(), TestButtonAction

### Community 113 - "Language Locales"
Cohesion: 0.18
Nodes (3): missing_locales(), TestCatalogue, TestTransliteration

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
Cohesion: 0.33
Nodes (3): load_summary(), SurahProgress, TestLoadSummary

### Community 133 - "Health Check Endpoints"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 134 - "Schedule Calculation"
Cohesion: 0.29
Nodes (3): _advance(), next_scheduled_date(), _validated_days()

### Community 135 - "Scheduler Testing"
Cohesion: 0.32
Nodes (3): _isolate_handlers(), state(), store()

### Community 138 - "Test Acceptance"
Cohesion: 0.33
Nodes (6): Phase 1 acceptance criteria (tests/test_acceptance.py), claim_due claimed_at clock bug, tests/test_store_contract.py (both storage legs, CI postgres:16), Testing & CI, Blue-Green CI pipeline (blue-green-ci.yml), Test suite (parsing, quran, translations, locales, utils, webhook, handle_update)

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

## Knowledge Gaps
- **26 isolated node(s):** `alquran.cloud API`, `Husary recitation (AUDIO_BASE_URL)`, `Tafsir al-Jalalayn`, `claim_due claimed_at clock bug`, `UserSettings (src/lib/user_settings.py)` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1190 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **111 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `Store Initialization` to `Weekly Leaderboard`, `App Initialization`, `Surah Progress`, `Profile Testing`, `Hifz Interval Testing`, `User Settings Storage`, `Activity Contribution Graph`, `Callback Dispatch System`, `Memorize Feature Tests`, `Streak Tracking`, `Progress Command`, `Progress Data Models`, `Configuration Setup`, `Scheduler Queue Engine`, `State Management`, `Check Answer Handling`, `Context Building`, `Acceptance Testing`, `Queue Processing`, `Session Logging`, `Core Module Imports`, `Hifz Store Interface`, `Streak Computation`, `Surah Progress`, `Quran Progress`, `Postgres Store`, `Send Context`, `Answer Scoring`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Are the 37 inferred relationships involving `File` (e.g. with `_clean_state_store()` and `_tick()`) actually correct?**
  _`File` has 37 INFERRED edges - model-reasoned connections that need verification._
- **What connects `alquran.cloud API`, `Husary recitation (AUDIO_BASE_URL)`, `Tafsir al-Jalalayn` to the rest of the system?**
  _26 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Draft Wizard System` be split into smaller, more focused modules?**
  _Cohesion score 0.056150600454397924 - nodes in this community are weakly interconnected._
- **Why does `File` connect `File Media Storage` to `Draft Wizard System`, `Weekly Leaderboard`, `App Initialization`, `Profile Testing`, `Memorization Drilling`, `User Settings Storage`, `Group Management`, `Memorize Feature Tests`, `Streak Tracking`, `Progress Command`, `Inline Range Query`, `Configuration Setup`, `Scheduler Queue Engine`, `Mushaf Page Handling`, `State Management`, `Check Answer Handling`, `Context Building`, `Acceptance Testing`, `Queue Processing`, `Core Module Imports`, `Audio Stitching`, `Reciter Catalog`, `Test Configuration`, `Page Mode Testing`, `Audio Fetching`, `Utility Testing`, `Request Context`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `build_plan()` (e.g. with `Ref` and `.count()`) actually correct?**
  _`build_plan()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Should `Weekly Leaderboard` be split into smaller, more focused modules?**
  _Cohesion score 0.05009009009009009 - nodes in this community are weakly interconnected._