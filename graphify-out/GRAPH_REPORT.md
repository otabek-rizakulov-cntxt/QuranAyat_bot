# Graph Report - QuranAyat_bot  (2026-11-01)

## Corpus Check
- 236 files · ~212,989 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 4361 nodes · 10210 edges · 241 communities (140 shown, 101 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 984 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7ba08524`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Plan Builder
- Quran
- summarize
- services/plans.py
- Wizard Store
- Plan Setup
- auth.py
- localtime.py
- reader.py
- Leaderboard
- Hifz Profile Tests
- Profile
- Store
- Streak Image
- t
- User Settings
- Context
- Health
- Refs
- Redis Client
- store/__init__.py
- Router
- locales/__init__.py
- Hifz Progress Cmd Tests
- Group
- send_cached
- reciter_keyboard
- Hifz Streak Tests
- Hifz Platform
- Acceptance Tests
- Hifz Progress: quran_page_progress
- Docker Compose.stress
- Media: test_page_modepy
- test_recall_check.py
- Quran: TranslationRegistry
- Auth
- File
- Recitation Checker Investigation
- Hifz Progress: round_percent
- fetch_and_stitch
- verse_keyboard
- Session
- Plans: PlanStore
- Ref
- SendCtx
- Streaks
- Load Test
- Multilingual Plan
- Text
- Schema
- Services
- Progress
- Dispatch
- File Facade: test_reciter_pickerpy
- ScheduleStore
- Inline Reciter Search Tests
- test_hifz_check.py
- Multi Platform Plan
- Refs: get_surah_length
- Hifz
- _hifz
- Dispatch Order Tests
- Navigation Tests
- Mini App Plan
- Run App
- surah_progress
- Groups
- TestRestartDeliversExactlyOnce
- Profiles
- Locales
- api/plans.py
- postgres.py
- Hifz Seam Tests
- reciter_catalog
- bot/media.py
- Hifz Progress: juz_progress
- Tick
- Profiles: InMemoryProfileStore
- Bundle Translations
- Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd
- Quran: exists
- Streaks: compute_streak
- Groups: PostgresGroupStore
- Sessions
- Scheduler Tests
- Layering Tests
- BismillahBot — Multilingual Support Plan
- Plan Builder: Portion
- Groups: InMemoryGroupStore
- UserSettingsRow
- Store Contract Tests
- Multi Platform Plan: MultiPlatform Implementation Plan
- Catalog: get_position
- check_locales.py
- Profiles: ProfileRow
- parse_offset
- Hifz Seam Tests: TestRegistration
- Media Cache Keys Tests
- Scheduler Tests: TestTransientFailuresAreRetried
- Store Contract Tests: TestPlans
- Business Logic
- Plans: PlanDaySpec
- InMemoryStore
- Refactor — Implementation Plan
- recall_check.py
- Auth: time
- reciter.py
- Time Pickers
- info.py
- 1. Why
- asyncio
- reciter_label
- Store Contract Tests: TestSchedule
- store/__init__.py
- Safety net (characterisation tests, staging smoke, blue-green)
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- Progress: featuresprogresspy
- Export Web Content Tests
- reciter_kind
- _seed_legacy_lang
- 8. Phased task breakdown
- streak.py
- Schedule: InMemoryScheduleStore
- Schedule: PostgresScheduleStore
- Mini App Plan: normalize_lang
- Blue Green Ci: jobs
- Blue Green Ci: with
- test_reciter_picker.py
- Parsing
- run_app.py
- Mini App Plan: Separate quranayatminiapp Nextjs
- Enqueue
- save_plan
- Media: range_audio
- Quran: get_next_ayah
- format_offset
- Store Contract Tests: TestLeaderboard
- Store Contract Tests: TestProfiles
- Business Logic: The hifz platform memorization
- Export Openapi
- stats.py
- Parsing: parse_ayah
- week_bounds
- 6. Phased task breakdown
- pending_input.py
- test_inline_range.py
- Hifz Seam Tests: test_hifz_seampy
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- Translation editions table (48 codes)
- Caching strategy (Redis user state, file_id, wizard draft)
- Blue Green Ci: env
- 5. Content: multi-translation loading (memory-aware)
- Runner
- graphify-autopush.sh
- Page Mode Tests
- Scheduler Tests: _at
- Settings Tests
- Store Contract Tests: TestSessions
- Blue Green Ci: postgres
- Blue Green Ci: test
- Blue Green Ci: preflight
- Export Web Content
- services/streaks.py
- Hifz Seam Tests: TestPrefixNamespace
- Hifz Seam Tests: TestDispatchCallback
- _legacy_lang_key
- Blue Green Ci: smokegreen
- Reciter: reciter_set_confirmation
- File Facade: search_performers
- Scheduler Tests: test_schedulerpy
- Store Contract Tests: TestSettings
- Verse Card Tests
- BismillahBot README
- Groups: GroupPlanDayRow
- Blue Green Ci: deploygreen
- Blue Green Ci: promote
- get_store
- Hifz Seam Tests: test_longest_prefix_wins
- Scheduler Tests: TestRunScheduler
- Store Contract Tests: test_store_contractpy
- Claude
- Acceptance Tests: TestSevenTheCommandsExist
- Hifz Seam Tests: TestDispatchCommand
- Groups: GroupMemberLink
- Hifz Group Tests: TestRegistration

## God Nodes (most connected - your core abstractions)
1. `get_store()` - 150 edges
2. `Quran` - 138 edges
3. `Ctx` - 127 edges
4. `t()` - 103 edges
5. `handle_update()` - 94 edges
6. `UserSettings` - 77 edges
7. `build_plan()` - 72 edges
8. `File` - 63 edges
9. `parse_reference()` - 59 edges
10. `Ref` - 55 edges

## Surprising Connections (you probably didn't know these)
- `5. Caching strategy` --references--> `MemoryStore`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/infra/redis_client.py
- `3. Target architecture` --references--> `TranslationRegistry`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/domain/quran.py
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `Phase 3 — Hifz parity` --references--> `build_plan()`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/domain/plan_builder.py
- `Translation-only catalogue entries` --references--> `normalize_lang()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/locales/languages.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Hifz platform design principles (derived state, pure builder, idempotent scheduler, local time)** — docs_business_logic_derived_intervals, docs_business_logic_pure_plan_builder, docs_business_logic_scheduler_claim_send_mark, docs_business_logic_local_time_utc_offset [EXTRACTED 1.00]
- **Recitation check pipeline (recite flow → worker → ASR → alignment → report)** — docs_recitation_checker_investigation_recite_flow, docs_recitation_checker_investigation_checker_worker, docs_recitation_checker_investigation_quran_asr_tiny, docs_recitation_checker_investigation_alignment, docs_recitation_checker_investigation_report_json [EXTRACTED 1.00]
- **DRY helpers replacing copy-pasted patterns** — docs_refactor_plan_send_cached, docs_refactor_plan_button_rows, docs_refactor_plan_offset_picker, docs_refactor_plan_ignore_not_modified, docs_refactor_plan_spawn [EXTRACTED 1.00]
- **Refactor phases 0-6 sequence** — docs_refactor_plan_phase_0_guardrails, docs_refactor_plan_phase_1_split_main, docs_refactor_plan_phase_2_dry, docs_refactor_plan_phase_3_router, docs_refactor_plan_phase_4_infra, docs_refactor_plan_phase_5_layering, docs_refactor_plan_phase_6_hygiene [EXTRACTED 1.00]
- **Settings persistence fail-loudly fix** — docs_refactor_plan_settings_persistence_fix, docs_refactor_plan_in_memory_store_fallback, docs_refactor_plan_allow_memory_store, docs_refactor_plan_health_endpoint [EXTRACTED 1.00]
- **Thin adapters over a single Python business-logic layer (bot, Mini App API, WhatsApp channel)** — docs_mini_app_plan_service_layer, docs_mini_app_plan_api_v1_surface, docs_multi_platform_plan_channel_interface, docs_business_logic_repository_store [INFERRED 0.85]
- **Locale integrity enforcement across 48 locales** — scripts_check_locales, docs_hifz_strings_hard_rules, docs_hifz_platform_group_locales, docs_translation_review_review_criteria [INFERRED 0.85]

## Communities (241 total, 101 thin omitted)

### Community 0 - "Plan Builder"
Cohesion: 0.05
Nodes (17): advancing(), auto_pace(), build_plan(), surah_ref(), to_day_specs(), assert_covers_target_once(), assert_well_formed(), spans() (+9 more)

### Community 1 - "Quran"
Cohesion: 0.08
Nodes (7): stitch(), page_caption(), _consolidations(), Quran, page_image_url(), test_page_boundaries_match_the_bot(), TestDivisionsTileTheQuran

### Community 2 - "summarize"
Cohesion: 0.07
Nodes (8): Progress, summarize(), SurahProgress, HifzInterval, load_summary(), _at(), TestLoadSummary, TestSummarize

### Community 3 - "services/plans.py"
Cohesion: 0.10
Nodes (19): active(), _plan_out(), today(), change_status(), complete_day(), current_plan(), day_position(), DrillResult (+11 more)

### Community 4 - "Wizard Store"
Cohesion: 0.06
Nodes (9): Wizard, test_draft_is_written_with_that_ttl(), TestAccumulation, TestCancel, TestCoexistsWithTheReciterFlow, TestCorruptState, TestLifecycle, TestOneDraftPerUser (+1 more)

### Community 5 - "Plan Setup"
Cohesion: 0.12
Nodes (30): Ctx, _begin_setup(), _join_board(), memorize(), on_tap(), plan_step(), _expired(), _ref_from_draft() (+22 more)

### Community 6 - "auth.py"
Cohesion: 0.11
Nodes (15): jwt_secret(), require_user(), answer(), AnswerIn, AnswerOut, make_token(), question(), QuestionOut (+7 more)

### Community 7 - "localtime.py"
Cohesion: 0.13
Nodes (9): _as_utc(), local_date(), local_now(), local_time(), next_due_utc(), to_utc(), TestLocalDate, TestNextDueUtc (+1 more)

### Community 8 - "reader.py"
Cohesion: 0.07
Nodes (27): command, 5. API surface (`/api/v1`), Phase 2 — WhatsApp MVP (reader + daily ayat), ignore_not_modified(), _board_message(), leaderboard(), on_leaderboard(), juz() (+19 more)

### Community 9 - "Leaderboard"
Cohesion: 0.07
Nodes (16): user_week_window(), week_window(), weekly_board(), _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join() (+8 more)

### Community 10 - "Hifz Profile Tests"
Cohesion: 0.08
Nodes (17): _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _isolate_registries(), _Message, _profile_row() (+9 more)

### Community 11 - "Profile"
Cohesion: 0.04
Nodes (40): patch_profile(), _answer_data(), _ask(), check(), on_check(), _options_keyboard(), _parse_answer(), _question_text() (+32 more)

### Community 12 - "Store"
Cohesion: 0.08
Nodes (12): _CallbackQuery, _ctx(), _isolate_registries(), _Message, _run_wizard(), _Settings, _tap(), TestDrill (+4 more)

### Community 13 - "Streak Image"
Cohesion: 0.07
Nodes (13): render(), build_grid(), _counts(), draw_contribution_graph(), Grid, level_for(), render_streak_graph(), _semaphore() (+5 more)

### Community 14 - "t"
Cohesion: 0.09
Nodes (19): 7. The keyboard & command localization challenge, Telegram command menu, _send_drill(), _translation_text(), _cancel_row(), _custom_days_keyboard(), _days_keyboard(), _drill_keyboard() (+11 more)

### Community 15 - "User Settings"
Cohesion: 0.17
Nodes (6): SettingsRow, UserSettings, TestDefaults, TestIndependence, TestKeyedByUserId, TestRoundTrip

### Community 16 - "Context"
Cohesion: 0.14
Nodes (16): ctx(), _bot(), _ctx(), _isolate_registries(), _member(), _run_setup_to_plan(), _Settings, TestBoard (+8 more)

### Community 17 - "Health"
Cohesion: 0.06
Nodes (16): health(), cache_backend(), store_backend(), database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries() (+8 more)

### Community 18 - "Refs"
Cohesion: 0.05
Nodes (17): clamp_to_quran(), _clean(), format_ref(), juz_ref(), page_ref(), parse_range(), parse_reference(), _validated() (+9 more)

### Community 19 - "Redis Client"
Cohesion: 0.08
Nodes (8): 6. Issues fixed in this refactor, get(), _key(), save(), get(), save(), CacheUnavailable, RedisSingleton

### Community 20 - "store/__init__.py"
Cohesion: 0.07
Nodes (17): Phase 1 — Take `main.py` apart (pure moves) — *done*, create_app(), build_data(), _commands_for(), initialize(), lifespan(), _set_bot_commands(), _process_update() (+9 more)

### Community 21 - "Router"
Cohesion: 0.07
Nodes (21): 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 3 — One router for everything — *done*, Phase 5 — Fix the layering — *done*, Phase 6 — Repository hygiene — *done*, _on_callback(), _on_text(), decorate() (+13 more)

### Community 22 - "locales/__init__.py"
Cohesion: 0.05
Nodes (24): Phase 2 — DRY the duplicated patterns — *done*, _search_reciters(), set_translation_language(), set_ui_language(), language_keyboard(), language_picker(), translation_language_keyboard(), button_rows() (+16 more)

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "Group"
Cohesion: 0.09
Nodes (19): bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), group_board_entries(), handle_start_payload(), _is_group_admin() (+11 more)

### Community 25 - "send_cached"
Cohesion: 0.11
Nodes (10): 3. Principles applied, _send(), send_cached(), send_file(), source(), send_page_audio(), source(), has_page_audio() (+2 more)

### Community 26 - "reciter_keyboard"
Cohesion: 0.24
Nodes (4): reciter_keyboard(), reciter_page_count(), _pager_row(), TestPagination

### Community 27 - "Hifz Streak Tests"
Cohesion: 0.10
Nodes (13): cache_key(), _caption(), _ctx(), _earn(), _photo_message(), _Settings, _streak(), TestCallback (+5 more)

### Community 28 - "Hifz Platform"
Cohesion: 0.09
Nodes (20): Hifz Platform - Plan & Progress, Phase 1 acceptance criteria (tests/test_acceptance.py), Hifz change log, claim_due claimed_at clock bug, Hifz data model (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send, group_*), Phase 2 group cluster (J1-J6, forum topics), Workstream I: i18n & commands for 48 locales, Workstream C: interval merge-on-insert + derived percentages (+12 more)

### Community 29 - "Acceptance Tests"
Cohesion: 0.12
Nodes (13): _CallbackQuery, _cmd(), _ctx(), _isolate_registries(), _Message, _run_wizard(), _save_plan(), _Settings (+5 more)

### Community 30 - "Hifz Progress: quran_page_progress"
Cohesion: 0.10
Nodes (4): juz_page_progress(), quran_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 32 - "Media: test_page_modepy"
Cohesion: 0.10
Nodes (14): send_page(), send_repeated_audio(), stitch(), _buffer(), data(), fake_bot(), _stub_audio(), _stub_stitch() (+6 more)

### Community 33 - "test_recall_check.py"
Cohesion: 0.03
Nodes (31): _nfc(), sweep_refs(), swept(), test_a_different_date_gives_a_different_question(), test_both_question_modes_show_up_in_the_sweep(), test_correct_option_is_never_a_length_outlier(), test_correct_option_is_never_the_extreme_by_a_wide_ratio(), test_correct_option_really_follows_the_prompt() (+23 more)

### Community 34 - "Quran: TranslationRegistry"
Cohesion: 0.07
Nodes (8): 12. Testing, parse_quran(), TranslationRegistry, TestCorpusIntegrity, TestAvailable, TestCaching, TestFallback, TestTransliteration

### Community 35 - "Auth"
Cohesion: 0.12
Nodes (23): InvalidInitData, sign_init_data(), validate_init_data(), _auth(), _fields(), _jwt_secret(), test_added_field_is_rejected(), test_auth_drops_malformed_start_param() (+15 more)

### Community 36 - "File"
Cohesion: 0.08
Nodes (6): File, TestAudioNeverFollowsLanguage, TestAudioFilename, TestImageFilename, TestLegacyLanguageKey, TestStateStore

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.07
Nodes (28): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards (+20 more)

### Community 38 - "Hifz Progress: round_percent"
Cohesion: 0.08
Nodes (5): format_percent(), PageProgress, _Ratio, round_percent(), TestRounding

### Community 39 - "fetch_and_stitch"
Cohesion: 0.29
Nodes (4): fetch_and_stitch(), _fit_for_telegram(), _semaphore(), stitch_images()

### Community 40 - "verse_keyboard"
Cohesion: 0.08
Nodes (19): page_keyboard(), verse_keyboard(), mode_button(), app_url(), set_menu_button(), _app_command(), app_on(), data() (+11 more)

### Community 41 - "Session"
Cohesion: 0.12
Nodes (20): init_data_max_age(), auth_telegram(), AuthOut, me(), _me(), MeOut, patch_settings(), PlanSummary (+12 more)

### Community 42 - "Plans: PlanStore"
Cohesion: 0.07
Nodes (4): PlanDayRow, PlanRow, PlanStore, PostgresPlanStore

### Community 43 - "Ref"
Cohesion: 0.10
Nodes (11): _clip(), _covered(), _focus_surah(), _intersect(), _page_share(), _pages_of(), ProgressSummary, _recency_key() (+3 more)

### Community 44 - "SendCtx"
Cohesion: 0.13
Nodes (7): push_plan_day(), _send_plain_message(), register_send_handler(), _same_origin(), send_handler(), decorate(), SendCtx

### Community 45 - "Streaks"
Cohesion: 0.13
Nodes (4): record_session(), TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 46 - "Load Test"
Cohesion: 0.12
Nodes (14): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+6 more)

### Community 47 - "Multilingual Plan"
Cohesion: 0.17
Nodes (13): Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), Quran.from_file(path) refactor, setMyCommands per language, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+5 more)

### Community 48 - "Text"
Cohesion: 0.20
Nodes (7): reference(), _inline_query(), _of_type(), _results(), TestInlineArabicImage, TestRangeAudio, TestRangeText

### Community 49 - "Schema"
Cohesion: 0.12
Nodes (24): group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval, hifz_interval_user_surah_idx (+16 more)

### Community 50 - "Services"
Cohesion: 0.18
Nodes (18): _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today(), test_me_carries_plan_and_streak(), test_opted_out_user_is_absent_from_the_board() (+10 more)

### Community 51 - "Progress"
Cohesion: 0.18
Nodes (16): not_found(), forget(), ForgetIn, ForgetOut, _juz(), JuzRatio, progress(), ProgressOut (+8 more)

### Community 52 - "Dispatch"
Cohesion: 0.17
Nodes (19): handle_update(), _callback(), data(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index() (+11 more)

### Community 53 - "File Facade: test_reciter_pickerpy"
Cohesion: 0.18
Nodes (5): _callback(), _message(), _reciter_buttons(), _tab_row(), TestPickerFlow

### Community 55 - "Inline Reciter Search Tests"
Cohesion: 0.14
Nodes (19): _audio_result(), data(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter(), test_ayah_audio_dropped_without_public_base_url(), test_ayah_audio_uses_callers_reciter() (+11 more)

### Community 56 - "test_hifz_check.py"
Cohesion: 0.06
Nodes (21): percentile_band(), refresh_streaks(), streak_summary(), user_today(), _answer_data(), _AnyDay, _ask(), _asked() (+13 more)

### Community 57 - "Multi Platform Plan"
Cohesion: 0.13
Nodes (17): /api/v1 REST surface, initData HMAC validation → short-lived JWT, OpenAPI → TypeScript client pipeline, Recall check integrity (signed question_token), Mini App risks, Identity table (platform, external_id → user_id), Normalized Incoming event, Neutral message model rendering (HTML / WhatsApp markup) (+9 more)

### Community 58 - "Refs: get_surah_length"
Cohesion: 0.18
Nodes (4): ayah_count(), TestAyahCount, test_short_surahs_still_get_four_distinct_options(), test_the_last_ayah_of_every_surah_produces_a_question()

### Community 59 - "Hifz"
Cohesion: 0.06
Nodes (10): _covers(), HifzStore, InMemoryHifzStore, _merge_span(), _normalize(), _overlaps(), PostgresHifzStore, _split_span() (+2 more)

### Community 60 - "_hifz"
Cohesion: 0.07
Nodes (10): _assert_invariant(), _ayahs(), _hifz(), _spans(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order(), TestAddInterval (+2 more)

### Community 61 - "Dispatch Order Tests"
Cohesion: 0.18
Nodes (17): _callback(), data(), fake_bot(), _message(), probe(), _sent_a_verse(), test_a_command_beats_a_pending_reciter_search(), test_a_command_escapes_a_wizard_without_ending_it() (+9 more)

### Community 62 - "Navigation Tests"
Cohesion: 0.12
Nodes (9): data(), fake_bot(), _message(), _no_network(), TestCommandArguments, TestJuzCommand, TestPageCommand, TestSajdaCommand (+1 more)

### Community 63 - "Mini App Plan"
Cohesion: 0.14
Nodes (14): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 6. Frontend structure (`quranayat-miniapp`), 7. Bot ↔ Mini App integration (+6 more)

### Community 64 - "Run App"
Cohesion: 0.12
Nodes (4): setup_logging(), test_http_client_request_urls_are_never_logged(), test_the_secret_does_not_reveal_the_token(), test_webhook_acks_before_initialization()

### Community 65 - "surah_progress"
Cohesion: 0.11
Nodes (5): started_surahs(), surah_progress(), TestInputHandling, TestSpecAcceptance, TestSurahProgress

### Community 66 - "Groups"
Cohesion: 0.12
Nodes (3): GroupConfig, GroupPlanRow, GroupStore

### Community 69 - "Locales"
Cohesion: 0.09
Nodes (7): button_action(), missing_keys(), _placeholders(), TestButtonAction, TestGroupLocaleExemption, TestLanguageLookup, TestLocaleIntegrity

### Community 70 - "api/plans.py"
Cohesion: 0.17
Nodes (16): _build(), complete(), create(), DrillOut, lifecycle(), PlanCreateIn, PlanDayOut, PlanOut (+8 more)

### Community 71 - "postgres.py"
Cohesion: 0.10
Nodes (10): 11.1 Profile settings reset after a while — `fix/settings-persistence`, 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, close_pool(), DatabaseUnavailable, get_pool(), _lock(), reset_for_tests() (+2 more)

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 74 - "bot/media.py"
Cohesion: 0.08
Nodes (18): Phase 4 — Split infrastructure god-objects — *done*, answer_inline_query(), inline_audio_result(), inline_photo_results(), combined_audio_key(), range_audio_url(), send_quran(), resolve_settings() (+10 more)

### Community 75 - "Hifz Progress: juz_progress"
Cohesion: 0.11
Nodes (7): juz_progress(), JuzProgress, quran_progress(), _spans(), started_juzs(), TestJuzProgress, TestQuranProgress

### Community 76 - "Tick"
Cohesion: 0.10
Nodes (10): _deliver(), _is_stale(), _lock(), _release(), _resolve(), tick(), _tick(), TickResult (+2 more)

### Community 78 - "Bundle Translations"
Cohesion: 0.15
Nodes (8): _clean_state_store(), bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.11
Nodes (20): Audio catalog kinds, Repeat (memorization), Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES), Mini App feature parity map, Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points) (+12 more)

### Community 80 - "Quran: exists"
Cohesion: 0.12
Nodes (6): TestExists, TestRandom, TestStructure, TestSurahMeta, test_pick_ayah_handles_a_cross_surah_span(), test_the_whole_quran_is_a_valid_span()

### Community 81 - "Streaks: compute_streak"
Cohesion: 0.24
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 83 - "Sessions"
Cohesion: 0.07
Nodes (6): InMemorySessionStore, LeaderboardEntry, PostgresSessionStore, SessionRow, SessionStore, WeeklyBoard

### Community 84 - "Scheduler Tests"
Cohesion: 0.17
Nodes (4): _claimed_at(), _record(), TestCatchUp, TestTick

### Community 85 - "Layering Tests"
Cohesion: 0.14
Nodes (16): export(), languages(), main(), resolved_table(), _write(), _absolute_imports(), _sources(), test_known_violations_still_exist() (+8 more)

### Community 86 - "BismillahBot — Multilingual Support Plan"
Cohesion: 0.13
Nodes (14): 10. File-by-file change list, 11. Memory & performance (free-tier reality), 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 2. Current-state audit (what is hardcoded English), 3. Target architecture, 4. User language preference (+6 more)

### Community 87 - "Plan Builder: Portion"
Cohesion: 0.12
Nodes (5): _advance(), next_scheduled_date(), Portion, _validated_days(), TestPortionShape

### Community 90 - "Store Contract Tests"
Cohesion: 0.11
Nodes (3): _spans(), TestHifzIntervalEdges, TestHifzIntervals

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.12
Nodes (17): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+9 more)

### Community 92 - "Catalog: get_position"
Cohesion: 0.20
Nodes (10): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, put_position(), ReaderPosition, Reciter (+2 more)

### Community 93 - "check_locales.py"
Cohesion: 0.12
Nodes (12): Hifz platform frozen string manifest, src/locales/en.py source of truth, Key conventions (btn_*, cmd_*), Wave process (feature agents, translation agents, reviewers), Native-speaker review - hifz platform strings, Review process steps, Review criteria (meaning, register, grammatical number, RTL, button length), main() (+4 more)

### Community 95 - "parse_offset"
Cohesion: 0.15
Nodes (3): parse_offset(), TestParseOffset, TestPicker

### Community 97 - "Media Cache Keys Tests"
Cohesion: 0.15
Nodes (8): _bot(), _next_id(), send_audio(), send_photo(), no_cdn(), _source(), test_a_miss_caches_under_the_key_and_a_hit_replays_it(), test_a_rejected_cached_id_is_rebuilt_and_recached()

### Community 100 - "Business Logic"
Cohesion: 0.15
Nodes (13): 1. Overview, 2. Architecture, 3. Request lifecycle, 5. Caching strategy, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic, Local time (+5 more)

### Community 103 - "Refactor — Implementation Plan"
Cohesion: 0.07
Nodes (28): 10. Found along the way (out of scope — behaviour changes), 2. Goals and non-goals, 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, 6. Ordering, risk, size, 7. Safety net, 8. Expected result, 9. Decisions and open questions (+20 more)

### Community 104 - "recall_check.py"
Cohesion: 0.05
Nodes (36): _assemble(), _at_offset(), _ayah_text(), _basmala_prefix(), build_question(), _clean(), _continuation_question(), corpus() (+28 more)

### Community 105 - "Auth: time"
Cohesion: 0.18
Nodes (13): _b64url(), _b64url_decode(), decode_token(), _init_data_secret(), InvalidToken, issue_token(), _sign(), _unauthorized() (+5 more)

### Community 106 - "reciter.py"
Cohesion: 0.22
Nodes (3): reciter_page_of(), reciter_group(), TestCurrentReciter

### Community 107 - "Time Pickers"
Cohesion: 0.33
Nodes (7): offset_options(), _grid(), test_a_label_prefix_changes_only_the_label(), test_cancel_data_adds_a_localized_cancel_row(), test_every_offset_is_offered_in_order_under_the_callers_prefix(), test_no_cancel_row_unless_asked(), test_rows_are_columns_wide()

### Community 108 - "info.py"
Cohesion: 0.15
Nodes (10): Routing rules (in `serve`), about(), app(), help_(), index(), start(), _welcome(), command_lines() (+2 more)

### Community 109 - "1. Why"
Cohesion: 0.15
Nodes (9): 5.2 Telegram message (bot), 1. Why, _post_portion(), push_group_day(), send_combined_audio(), stitch(), build_verse_text(), get_translation() (+1 more)

### Community 110 - "asyncio"
Cohesion: 0.18
Nodes (3): download_combined_audio(), download_stitched_audio(), TestStitchedAudioAcrossSurahs

### Community 114 - "Safety net (characterisation tests, staging smoke, blue-green)"
Cohesion: 0.12
Nodes (15): graphify knowledge graph (graphify-out/), CLAUDE.md graphify lookup rules, ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable, lib/utils.File god class, GET / health with store and cache status (503), Silent in-memory store fallback, Phase 3 — One router for everything, Phase 4 — Split infrastructure god-objects (+7 more)

### Community 115 - "Koyeb Capacity Report"
Cohesion: 0.25
Nodes (7): Koyeb free-tier capacity report, CPU-bound queueing failure mode (~24 msg/s ceiling), Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start), Neon managed Postgres, Capacity results 5-1000 concurrent (no errors, 70-91 MB), Stress environment (docker-compose.stress.yml, cpus 0.1, 512m), Synthetic traffic mix (scripts/stress/gen_updates.py)

### Community 116 - "Blue Green Ci"
Cohesion: 0.14
Nodes (13): concurrency, cancel-in-progress, group, env, PYTHON_DEFAULT, name, on, pull_request (+5 more)

### Community 117 - "Blue Green Ci: name"
Cohesion: 0.23
Nodes (14): steps, steps, steps, steps, steps, steps, steps, env (+6 more)

### Community 118 - "Progress: featuresprogresspy"
Cohesion: 0.24
Nodes (6): forgot_command(), on_progress_tap(), progress_command(), _show(), surah_spans(), unmark()

### Community 119 - "Export Web Content Tests"
Cohesion: 0.21
Nodes (7): _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah(), test_meta_surahs_and_sajdas(), test_tafsir_has_every_ayah()

### Community 121 - "_seed_legacy_lang"
Cohesion: 0.21
Nodes (3): _seed_legacy_lang(), TestInlineCaller, TestLegacyMigration

### Community 122 - "8. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 8. Phased task breakdown, Phase 0 — Foundations, Phase 1 — Service-layer extraction (this repo, no UI change), Phase 2 — Reader parity (read-only, low risk, ships first), Phase 3 — Hifz parity, Phase 4 — Recitation checker UI (depends on the investigation's Phase A), Phase 5 — Later

### Community 123 - "streak.py"
Cohesion: 0.26
Nodes (6): _caption(), _keyboard(), on_streak(), _send_graph(), streak(), StreakSummary

### Community 125 - "Schedule: PostgresScheduleStore"
Cohesion: 0.13
Nodes (3): PostgresStore, PostgresScheduleStore, store()

### Community 126 - "Mini App Plan: normalize_lang"
Cohesion: 0.22
Nodes (6): 4.1 Flow, 4.2 Rules, 4.3 Transport, 4. Authentication, normalize_lang(), TestNormalizeLang

### Community 127 - "Blue Green Ci: jobs"
Cohesion: 0.15
Nodes (13): name, needs, runs-on, jobs, build, lint, rollback, name (+5 more)

### Community 128 - "Blue Green Ci: with"
Cohesion: 0.15
Nodes (13): with, cache, cache-dependency-path, cache-from, cache-to, context, if-no-files-found, load (+5 more)

### Community 129 - "test_reciter_picker.py"
Cohesion: 0.47
Nodes (3): data(), fake_bot(), tg_bot()

### Community 130 - "Parsing"
Cohesion: 0.16
Nodes (3): parse_ayah_range(), parse_quran_tafsir(), TestParseAyahRange

### Community 132 - "Mini App Plan: Separate quranayatminiapp Nextjs"
Cohesion: 0.22
Nodes (10): Page audio with stitched fallback, Page image stitching (lib/page_image.py), Structural divisions (page / juz / sajda from quran-data.xml), Uthmani text in Amiri Quran / KFGQPC font, Client-side playlist audio (no server stitching), Locale export to JSON (web_ keys, next-intl), Static immutable Quran JSON served from frontend CDN, Daily ayat cost model on WhatsApp (+2 more)

### Community 133 - "Enqueue"
Cohesion: 0.21
Nodes (5): The scheduler (`src/lib/scheduler.py`), enqueue(), idempotency_key(), schedule_daily(), registered_kinds()

### Community 134 - "save_plan"
Cohesion: 0.25
Nodes (4): preview(), save_plan(), SavedPlan, target_kind()

### Community 135 - "Media: range_audio"
Cohesion: 0.17
Nodes (5): range_audio(), content(), TestRangeAudioRoute, fake_download(), __init__()

### Community 136 - "Quran: get_next_ayah"
Cohesion: 0.22
Nodes (5): 4. Navigation model, Page images and page audio, Structural divisions (page / juz / sajda), Translation-only catalogue entries, TestNavigation

### Community 140 - "Business Logic: The hifz platform memorization"
Cohesion: 0.20
Nodes (8): Central callback prefix allocation (hifz.PREFIXES), Future roadmap and prioritized backlog, The hifz platform (memorization companion), Pure plan builder (build_plan), Streak day ticks on completed session, Bot ↔ Mini App integration (menu button, startapp, /app), recitation_job table and user_profile.riwayah, /recite flow (voice note → recitation_job → report)

### Community 141 - "Export Openapi"
Cohesion: 0.27
Nodes (5): build(), main_(), _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl()

### Community 142 - "stats.py"
Cohesion: 0.35
Nodes (8): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut

### Community 145 - "6. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 6. Phased task breakdown, Phase 0 — Prerequisites (no code), Phase 1 — Channel seam (this repo, no user-visible change), Phase 3 — Hifz on WhatsApp, Phase 4 — Recitation checker on WhatsApp, Phase 5 — Web access outside Telegram, Phase 6 — Later

### Community 146 - "pending_input.py"
Cohesion: 0.38
Nodes (3): expect(), _key(), take()

### Community 147 - "test_inline_range.py"
Cohesion: 0.16
Nodes (5): data(), fake_bot(), public_url(), TestStitching, tg_bot()

### Community 148 - "Hifz Seam Tests: test_hifz_seampy"
Cohesion: 0.18
Nodes (3): _isolate_registries(), _Settings, TestSchemaApplication

### Community 152 - "Translation editions table (48 codes)"
Cohesion: 0.33
Nodes (5): alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Locale review tracking table (47 locales)

### Community 153 - "Caching strategy (Redis user state, file_id, wizard draft)"
Cohesion: 0.33
Nodes (3): Inline query answering (all four representations, ranges), Navigation model ((surah, ayah, type) per chat_id), Verse card (inline keyboard, edit in place)

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 155 - "5. Content: multi-translation loading (memory-aware)"
Cohesion: 0.40
Nodes (3): 7. Known limitations / tech debt, 5. Content: multi-translation loading (memory-aware), Translation catalogue (initial set)

### Community 156 - "Runner"
Cohesion: 0.29
Nodes (3): catch_up(), run_scheduler(), _wait()

### Community 162 - "Blue Green Ci: postgres"
Cohesion: 0.22
Nodes (9): POSTGRES_DB, POSTGRES_HOST_AUTH_METHOD, POSTGRES_USER, env, image, options, ports, postgres (+1 more)

### Community 163 - "Blue Green Ci: test"
Cohesion: 0.22
Nodes (9): TEST_DATABASE_URL, test, python-version, fail-fast, matrix, env, name, runs-on (+1 more)

### Community 164 - "Blue Green Ci: preflight"
Cohesion: 0.22
Nodes (9): preflight, active, deploy_enabled, target, if, name, needs, outputs (+1 more)

### Community 165 - "Export Web Content"
Cohesion: 0.36
Nodes (6): build_meta(), export(), main(), _spans(), split_basmalah(), _write()

### Community 166 - "services/streaks.py"
Cohesion: 0.15
Nodes (8): Milestone, milestone_for(), _milestone_key(), offset_of(), StreakCounts, SessionOutcome, user_offset(), TestMilestones

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 175 - "Scheduler Tests: test_schedulerpy"
Cohesion: 0.28
Nodes (3): _isolate_handlers(), state(), store()

### Community 178 - "BismillahBot README"
Cohesion: 0.15
Nodes (15): Translation Attributions, Four ayah representations (english, tafsir, arabic, audio), Known limitations / tech debt, Issues fixed in the refactor (12 bugs), Documentation, Documentation index (docs/README.md), Phase 6 — Repository hygiene, CI — Blue-Green pipeline (+7 more)

### Community 182 - "Blue Green Ci: deploygreen"
Cohesion: 0.33
Nodes (6): environment, if, name, needs, runs-on, deploy-green

### Community 183 - "Blue Green Ci: promote"
Cohesion: 0.33
Nodes (6): promote, environment, if, name, needs, runs-on

### Community 185 - "get_store"
Cohesion: 0.15
Nodes (6): get_store(), _lock(), TestFourProgress, _added_update(), TestAdded, TestDailyPost

## Knowledge Gaps
- **51 isolated node(s):** `Expected result metrics (§8)`, `spawn() background tasks with strong refs`, `button_rows() row-packing helper`, `ignore_not_modified() context manager`, `Found along the way (out-of-scope behaviour changes)` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1490 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **101 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `get_store` to `summarize`, `services/plans.py`, `auth.py`, `reader.py`, `Leaderboard`, `Hifz Profile Tests`, `Profile`, `Store`, `Streak Image`, `stats.py`, `User Settings`, `Context`, `Redis Client`, `store/__init__.py`, `locales/__init__.py`, `Hifz Progress Cmd Tests`, `Hifz Streak Tests`, `Acceptance Tests`, `services/streaks.py`, `Session`, `Streaks`, `Services`, `Progress`, `Dispatch`, `ScheduleStore`, `test_hifz_check.py`, `_hifz`, `surah_progress`, `api/plans.py`, `postgres.py`, `Tick`, `InMemoryStore`, `store/__init__.py`, `Schedule: PostgresScheduleStore`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Expected result metrics (§8)`, `spawn() background tasks with strong refs`, `button_rows() row-packing helper` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Plan Builder` be split into smaller, more focused modules?**
  _Cohesion score 0.05030525030525031 - nodes in this community are weakly interconnected._
- **Why does `Quran` connect `Quran` to `Plan Builder`, `summarize`, `Parsing`, `services/plans.py`, `auth.py`, `Media: range_audio`, `reader.py`, `Quran: get_next_ayah`, `Profile`, `t`, `Refs`, `store/__init__.py`, `locales/__init__.py`, `Hifz Progress Cmd Tests`, `send_cached`, `5. Content: multi-translation loading (memory-aware)`, `Hifz Progress: quran_page_progress`, `Media: test_page_modepy`, `test_recall_check.py`, `Quran: TranslationRegistry`, `Export Web Content`, `verse_keyboard`, `Ref`, `Progress`, `Refs: get_surah_length`, `Navigation Tests`, `surah_progress`, `bot/media.py`, `Hifz Progress: juz_progress`, `Quran: exists`, `Plan Builder: Portion`, `Catalog: get_position`, `Business Logic`, `recall_check.py`, `1. Why`, `asyncio`, `Progress: featuresprogresspy`, `Export Web Content Tests`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 90 inferred relationships involving `Quran` (e.g. with `Module responsibilities` and `build_meta()`) actually correct?**
  _`Quran` has 90 INFERRED edges - model-reasoned connections that need verification._
- **Should `Quran` be split into smaller, more focused modules?**
  _Cohesion score 0.08408408408408409 - nodes in this community are weakly interconnected._