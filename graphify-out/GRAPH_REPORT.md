# Graph Report - QuranAyat_bot  (2026-11-01)

## Corpus Check
- 241 files · ~217,240 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 4513 nodes · 10458 edges · 249 communities (144 shown, 105 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 983 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `56694fcc`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_plan
- Quran
- summarize
- services/plans.py
- Wizard
- Plan Setup
- auth.py
- localtime.py
- .reply
- Leaderboard
- _ctx
- Profile
- Store
- build_grid
- services/streaks.py
- User Settings
- Context
- Health
- Refs
- RedisSingleton
- typing
- Router
- IdentityStore
- Hifz Progress Cmd Tests
- Group
- Refactor — Implementation Plan
- TelegramChannel
- Hifz Streak Tests
- Hifz Platform
- Acceptance Tests
- Hifz Progress: quran_page_progress
- Docker Compose.stress
- test_inline_range.py
- test_recall_check.py
- TranslationRegistry
- Auth
- File
- Recitation Checker Investigation
- round_percent
- fetch_and_stitch
- test_miniapp_links.py
- Session
- Plans: PlanStore
- auto_pace
- SendCtx
- Streaks
- Load Test
- Multilingual Plan
- Text
- Schema
- Services
- Progress
- Dispatch
- reciter_keyboard
- advancing
- Inline Reciter Search Tests
- test_hifz_check.py
- Multi Platform Plan
- Refs: get_surah_length
- Hifz
- _hifz
- Dispatch Order Tests
- _message
- Mini App Plan
- surah_progress
- InMemoryGroupStore
- TestRestartDeliversExactlyOnce
- Profiles
- t
- api/plans.py
- reset_for_tests
- Hifz Seam Tests
- features/check.py
- quran.py
- Hifz Progress: juz_progress
- Tick
- Profiles: InMemoryProfileStore
- Bundle Translations
- Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd
- build_question
- Streaks: compute_streak
- Groups: PostgresGroupStore
- Sessions
- Scheduler Tests
- Layering Tests
- BismillahBot — Multilingual Support Plan
- Plan Builder: Portion
- verse_keyboard
- auth.py
- Store Contract Tests
- Multi Platform Plan: MultiPlatform Implementation Plan
- api/catalog.py
- Hifz platform frozen string manifest
- Profiles: ProfileRow
- parse_offset
- Hifz Seam Tests: TestRegistration
- test_media_cache_keys.py
- Scheduler Tests: TestTransientFailuresAreRetried
- Store Contract Tests: TestPlans
- .exists
- Plans: PlanDaySpec
- test_hifz_progress.py
- Refactor — Implementation Plan
- recall_check.py
- ._send_media
- test_store_contract.py
- Time Pickers
- hifz_progress.py
- bot/media.py
- _sent
- unittest_mock
- Store Contract Tests: TestSchedule
- store/__init__.py
- Safety net (characterisation tests, staging smoke, blue-green)
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- features/progress.py
- Export Web Content Tests
- reciter_set_confirmation
- _seed_legacy_lang
- .get_next_ayah
- streak.py
- InMemoryScheduleStore
- PostgresScheduleStore
- Mini App Plan: normalize_lang
- Blue Green Ci: jobs
- Blue Green Ci: with
- logging
- parse_ayah_range
- .is_cancel
- Mini App Plan: Separate quranayatminiapp Nextjs
- ScheduleStore
- Channel
- Media: range_audio
- _Ratio
- GroupStore
- Store Contract Tests: TestLeaderboard
- TestProfiles
- Business Logic: The hifz platform memorization
- InMemoryPlanStore
- week_bounds
- reader.py
- week_window
- 6. Phased task breakdown
- test_channels_telegram.py
- to_markup
- Hifz Seam Tests: test_hifz_seampy
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- Choice
- test_hifz_profile.py
- Blue Green Ci: env
- json
- _edited
- graphify-autopush.sh
- Page Mode Tests
- Scheduler Tests: _at
- Settings Tests
- Store Contract Tests: TestSessions
- Blue Green Ci: postgres
- Blue Green Ci: test
- Blue Green Ci: preflight
- for_platform
- services/streaks.py
- Hifz Seam Tests: TestPrefixNamespace
- Hifz Seam Tests: TestDispatchCallback
- TestAudioNeverFollowsLanguage
- percentile_band
- Blue Green Ci: smokegreen
- parse_quran
- export
- File Facade: search_performers
- Scheduler Tests: test_schedulerpy
- PageProgress
- Verse Card Tests
- BismillahBot README
- load_summary
- plan_builder.py
- GroupConfig
- Blue Green Ci: deploygreen
- Blue Green Ci: promote
- Profile settings reset fix (fix/settings-persistence)
- format_offset
- Hifz Seam Tests: test_longest_prefix_wins
- Scheduler Tests: TestRunScheduler
- TestSettings
- GroupPlanDayRow
- _parse_answer
- GroupMemberLink
- Claude
- _legacy_lang_key
- Hifz Seam Tests: TestDispatchCommand
- Hifz Group Tests: TestRegistration

## God Nodes (most connected - your core abstractions)
1. `get_store()` - 150 edges
2. `Quran` - 136 edges
3. `Ctx` - 127 edges
4. `t()` - 103 edges
5. `handle_update()` - 94 edges
6. `UserSettings` - 77 edges
7. `build_plan()` - 72 edges
8. `File` - 63 edges
9. `parse_reference()` - 59 edges
10. `Ref` - 55 edges

## Surprising Connections (you probably didn't know these)
- `The scheduler (`src/lib/scheduler.py`)` --references--> `idempotency_key()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/infra/scheduler/enqueue.py
- `5. Caching strategy` --references--> `MemoryStore`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/infra/redis_client.py
- `3. Target architecture` --references--> `TranslationRegistry`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/domain/quran.py
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `Phase 3 — Hifz parity` --references--> `build_plan()`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/domain/plan_builder.py

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

## Communities (249 total, 105 thin omitted)

### Community 0 - "build_plan"
Cohesion: 0.10
Nodes (7): build_plan(), surah_ref(), spans(), TestConsolidationDays, TestDayOfWeekFiltering, TestPurity, TestSmallAndAwkwardTargets

### Community 1 - "Quran"
Cohesion: 0.11
Nodes (4): _consolidations(), Quran, test_page_boundaries_match_the_bot(), TestDivisionsTileTheQuran

### Community 2 - "summarize"
Cohesion: 0.09
Nodes (4): Progress, summarize(), HifzInterval, TestSummarize

### Community 3 - "services/plans.py"
Cohesion: 0.10
Nodes (16): change_status(), complete_day(), day_position(), DrillResult, due_days(), enqueue_next(), owned_day(), preview() (+8 more)

### Community 4 - "Wizard"
Cohesion: 0.08
Nodes (7): Wizard, test_draft_is_written_with_that_ttl(), TestAccumulation, TestCorruptState, TestLifecycle, TestOneDraftPerUser, wiz()

### Community 5 - "Plan Setup"
Cohesion: 0.08
Nodes (41): Ctx, _begin_setup(), _is_group_admin(), on_group_tap(), setup_step(), _step_post_time(), _step_target(), _step_topic() (+33 more)

### Community 6 - "auth.py"
Cohesion: 0.15
Nodes (11): jwt_secret(), require_user(), answer(), AnswerIn, AnswerOut, make_token(), question(), QuestionOut (+3 more)

### Community 7 - "localtime.py"
Cohesion: 0.13
Nodes (9): _as_utc(), local_date(), local_now(), local_time(), next_due_utc(), to_utc(), TestLocalDate, TestNextDueUtc (+1 more)

### Community 8 - ".reply"
Cohesion: 0.09
Nodes (21): command, Routing rules (in `serve`), Phase 2 — DRY the duplicated patterns — *done*, handle_start_payload(), _join_board(), about(), app(), help_() (+13 more)

### Community 9 - "Leaderboard"
Cohesion: 0.09
Nodes (12): weekly_board(), _CallbackQuery, _ctx(), _earn(), _join(), _Message, _sent(), _Settings (+4 more)

### Community 10 - "_ctx"
Cohesion: 0.24
Nodes (4): _ctx(), _profile_row(), TestLeaderboardOptIn, _toast()

### Community 11 - "Profile"
Cohesion: 0.08
Nodes (23): _cancel_keyboard(), _join_board(), name_step(), offset_from_callback(), on_profile_tap(), _plan_line(), profile_command(), profile_view() (+15 more)

### Community 12 - "Store"
Cohesion: 0.08
Nodes (12): _CallbackQuery, _ctx(), _isolate_registries(), _Message, _run_wizard(), _Settings, _tap(), TestDrill (+4 more)

### Community 13 - "build_grid"
Cohesion: 0.07
Nodes (13): render(), build_grid(), _counts(), draw_contribution_graph(), Grid, level_for(), render_streak_graph(), _semaphore() (+5 more)

### Community 14 - "services/streaks.py"
Cohesion: 0.25
Nodes (4): refresh_streaks(), streak_summary(), user_today(), TestRefreshAndSummary

### Community 15 - "User Settings"
Cohesion: 0.17
Nodes (6): SettingsRow, UserSettings, TestDefaults, TestIndependence, TestKeyedByUserId, TestRoundTrip

### Community 16 - "Context"
Cohesion: 0.12
Nodes (20): ctx(), get_store(), _lock(), _added_update(), _bot(), _ctx(), _isolate_registries(), _member() (+12 more)

### Community 17 - "Health"
Cohesion: 0.06
Nodes (15): health(), store_backend(), database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries(), fresh_redis() (+7 more)

### Community 18 - "Refs"
Cohesion: 0.06
Nodes (15): _clean(), format_ref(), juz_ref(), page_ref(), parse_range(), parse_reference(), _validated(), plan_target() (+7 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.06
Nodes (16): 6. Issues fixed in this refactor, 11.1 Profile settings reset after a while — `fix/settings-persistence`, 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, get(), _key(), save(), expect() (+8 more)

### Community 20 - "typing"
Cohesion: 0.05
Nodes (22): create_app(), _commands_for(), initialize(), lifespan(), _set_bot_commands(), _process_update(), telegram_webhook(), webhook_secret() (+14 more)

### Community 21 - "Router"
Cohesion: 0.12
Nodes (13): Phase 3 — One router for everything — *done*, _on_text(), _cancel(), dispatch_callback(), dispatch_command(), dispatch_wizard(), handles(), handles_callback() (+5 more)

### Community 22 - "IdentityStore"
Cohesion: 0.07
Nodes (4): IdentityRow, IdentityStore, PostgresIdentityStore, _stored()

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "Group"
Cohesion: 0.12
Nodes (14): bot_username(), _chat_id(), _create_topic(), _deep_link(), _enqueue_next_board(), _enqueue_next_group(), group_board_entries(), on_my_chat_member() (+6 more)

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.15
Nodes (13): 10. Found along the way (out of scope — behaviour changes), 2. Goals and non-goals, 3. Principles applied, 6. Ordering, risk, size, 7. Safety net, 8. Expected result, 9. Decisions and open questions, Expected result metrics (§8) (+5 more)

### Community 26 - "TelegramChannel"
Cohesion: 0.14
Nodes (4): TelegramChannel, TestAnswerAndTyping, TestEditText, TestMedia

### Community 27 - "Hifz Streak Tests"
Cohesion: 0.11
Nodes (12): _caption(), _ctx(), _earn(), _isolate_registries(), _photo_message(), _Settings, _streak(), TestCallback (+4 more)

### Community 28 - "Hifz Platform"
Cohesion: 0.09
Nodes (20): Hifz Platform - Plan & Progress, Phase 1 acceptance criteria (tests/test_acceptance.py), Hifz change log, claim_due claimed_at clock bug, Hifz data model (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send, group_*), Phase 2 group cluster (J1-J6, forum topics), Workstream I: i18n & commands for 48 locales, Workstream C: interval merge-on-insert + derived percentages (+12 more)

### Community 29 - "Acceptance Tests"
Cohesion: 0.08
Nodes (15): _CallbackQuery, _cmd(), _ctx(), _isolate_registries(), _Message, _run_wizard(), _save_plan(), _Settings (+7 more)

### Community 30 - "Hifz Progress: quran_page_progress"
Cohesion: 0.11
Nodes (4): juz_page_progress(), quran_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 32 - "test_inline_range.py"
Cohesion: 0.06
Nodes (19): stitch(), send_page(), send_repeated_audio(), stitch(), download_combined_audio(), download_stitched_audio(), _buffer(), data() (+11 more)

### Community 33 - "test_recall_check.py"
Cohesion: 0.03
Nodes (31): _nfc(), sweep_refs(), swept(), test_a_different_date_gives_a_different_question(), test_both_question_modes_show_up_in_the_sweep(), test_correct_option_is_never_a_length_outlier(), test_correct_option_is_never_the_extreme_by_a_wide_ratio(), test_correct_option_really_follows_the_prompt() (+23 more)

### Community 34 - "TranslationRegistry"
Cohesion: 0.06
Nodes (11): build_data(), get_default_query_results(), parse_quran_tafsir(), TranslationRegistry, corpus(), preload_corpus(), TestCorpusIntegrity, TestAvailable (+3 more)

### Community 35 - "Auth"
Cohesion: 0.12
Nodes (23): _init_data_secret(), InvalidInitData, sign_init_data(), validate_init_data(), _auth(), _fields(), _jwt_secret(), test_added_field_is_rejected() (+15 more)

### Community 36 - "File"
Cohesion: 0.07
Nodes (6): File, TestAudioFilename, TestImageFilename, TestLegacyLanguageKey, TestStateStore, TestCoexistsWithTheReciterFlow

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.07
Nodes (29): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards (+21 more)

### Community 38 - "round_percent"
Cohesion: 0.19
Nodes (3): format_percent(), round_percent(), TestRounding

### Community 39 - "fetch_and_stitch"
Cohesion: 0.19
Nodes (6): stitch(), page_image_url(), fetch_and_stitch(), _fit_for_telegram(), _semaphore(), stitch_images()

### Community 40 - "test_miniapp_links.py"
Cohesion: 0.11
Nodes (17): page_keyboard(), app_button(), app_row(), app_url(), set_menu_button(), _app_command(), app_on(), data() (+9 more)

### Community 41 - "Session"
Cohesion: 0.11
Nodes (24): init_data_max_age(), auth_telegram(), AuthOut, me(), _me(), MeOut, patch_profile(), patch_settings() (+16 more)

### Community 42 - "Plans: PlanStore"
Cohesion: 0.07
Nodes (4): PlanDayRow, PlanRow, PlanStore, PostgresPlanStore

### Community 43 - "auto_pace"
Cohesion: 0.10
Nodes (7): _intersect(), _pages_of(), auto_pace(), clamp_to_quran(), contains(), TestContainsAndClamp, TestAutoPace

### Community 44 - "SendCtx"
Cohesion: 0.16
Nodes (5): 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, _send_plain_message(), SendCtx, TestDailyPost

### Community 45 - "Streaks"
Cohesion: 0.13
Nodes (4): record_session(), TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 46 - "Load Test"
Cohesion: 0.14
Nodes (12): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+4 more)

### Community 47 - "Multilingual Plan"
Cohesion: 0.17
Nodes (13): Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), Quran.from_file(path) refactor, setMyCommands per language, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+5 more)

### Community 48 - "Text"
Cohesion: 0.20
Nodes (7): reference(), _inline_query(), _of_type(), _results(), TestInlineArabicImage, TestRangeAudio, TestRangeText

### Community 49 - "Schema"
Cohesion: 0.11
Nodes (26): group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval, hifz_interval_user_surah_idx (+18 more)

### Community 50 - "Services"
Cohesion: 0.15
Nodes (20): client(), _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today() (+12 more)

### Community 51 - "Progress"
Cohesion: 0.15
Nodes (17): not_found(), forget(), ForgetIn, ForgetOut, _juz(), JuzRatio, progress(), ProgressOut (+9 more)

### Community 52 - "Dispatch"
Cohesion: 0.17
Nodes (19): handle_update(), _callback(), data(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index() (+11 more)

### Community 53 - "reciter_keyboard"
Cohesion: 0.07
Nodes (19): reciter_keyboard(), reciter_label(), reciter_page_count(), reciter_page_of(), reciter_catalog(), reciter_group(), _callback(), data() (+11 more)

### Community 54 - "advancing"
Cohesion: 0.10
Nodes (6): advancing(), assert_covers_target_once(), assert_well_formed(), TestAcrossTheWholeQuran, TestAlMulkAcceptance, TestCrossSurahTargets

### Community 55 - "Inline Reciter Search Tests"
Cohesion: 0.14
Nodes (19): _audio_result(), data(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter(), test_ayah_audio_dropped_without_public_base_url(), test_ayah_audio_uses_callers_reciter() (+11 more)

### Community 56 - "test_hifz_check.py"
Cohesion: 0.15
Nodes (8): _AnyDay, _ask(), _buttons(), _callback_query(), _ctx(), _Settings, TestCallbackDataDiscipline, TestCheckEntryPoint

### Community 57 - "Multi Platform Plan"
Cohesion: 0.16
Nodes (13): initData HMAC validation → short-lived JWT, Identity table (platform, external_id → user_id), Normalized Incoming event, Neutral message model rendering (HTML / WhatsApp markup), WhatsApp opt-in / STOP opt-out flow, Other platforms shortlist (Messenger, Viber, Discord, PWA, Signal), Multi-platform phased breakdown (Phases 0-6), Multi-platform risks (+5 more)

### Community 58 - "Refs: get_surah_length"
Cohesion: 0.11
Nodes (7): _span_length(), ayah_count(), surah_spans(), TestAyahCount, TestSurahMeta, test_short_surahs_still_get_four_distinct_options(), test_the_last_ayah_of_every_surah_produces_a_question()

### Community 59 - "Hifz"
Cohesion: 0.06
Nodes (10): _covers(), HifzStore, InMemoryHifzStore, _merge_span(), _normalize(), _overlaps(), PostgresHifzStore, _split_span() (+2 more)

### Community 60 - "_hifz"
Cohesion: 0.07
Nodes (10): _assert_invariant(), _ayahs(), _hifz(), _spans(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order(), TestAddInterval (+2 more)

### Community 61 - "Dispatch Order Tests"
Cohesion: 0.18
Nodes (17): _callback(), data(), fake_bot(), _message(), probe(), _sent_a_verse(), test_a_command_beats_a_pending_reciter_search(), test_a_command_escapes_a_wizard_without_ending_it() (+9 more)

### Community 62 - "_message"
Cohesion: 0.21
Nodes (4): _message(), TestJuzCommand, TestPageCommand, TestSajdaCommand

### Community 63 - "Mini App Plan"
Cohesion: 0.10
Nodes (21): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 6. Frontend structure (`quranayat-miniapp`), 7. Bot ↔ Mini App integration (+13 more)

### Community 65 - "surah_progress"
Cohesion: 0.14
Nodes (4): started_surahs(), surah_progress(), TestSpecAcceptance, TestSurahProgress

### Community 69 - "t"
Cohesion: 0.05
Nodes (25): 7. The keyboard & command localization challenge, Telegram command menu, main(), placeholders(), _days_keyboard(), _lang_keyboard(), _pace_keyboard(), button_action() (+17 more)

### Community 70 - "api/plans.py"
Cohesion: 0.10
Nodes (26): parse_ref_or_422(), ref_out(), RefOut, active(), _build(), complete(), create(), DrillOut (+18 more)

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 73 - "features/check.py"
Cohesion: 0.18
Nodes (7): _answer_data(), _ask(), check(), on_check(), _options_keyboard(), _question_text(), _score()

### Community 74 - "quran.py"
Cohesion: 0.05
Nodes (21): _on_callback(), _search_reciters(), answer_inline_query(), inline_audio_result(), inline_photo_results(), combined_audio_key(), range_audio_url(), resolve_settings() (+13 more)

### Community 75 - "Hifz Progress: juz_progress"
Cohesion: 0.16
Nodes (5): juz_progress(), JuzProgress, _spans(), started_juzs(), TestJuzProgress

### Community 76 - "Tick"
Cohesion: 0.07
Nodes (20): enqueue(), idempotency_key(), schedule_daily(), register_send_handler(), registered_kinds(), _same_origin(), decorate(), catch_up() (+12 more)

### Community 78 - "Bundle Translations"
Cohesion: 0.15
Nodes (8): _clean_state_store(), bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.11
Nodes (20): Audio catalog kinds, Repeat (memorization), Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES), Mini App feature parity map, Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points) (+12 more)

### Community 80 - "build_question"
Cohesion: 0.25
Nodes (6): _answer_data(), _asked(), _sessions(), _tap(), TestScoring, TestStaleButtons

### Community 81 - "Streaks: compute_streak"
Cohesion: 0.24
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 83 - "Sessions"
Cohesion: 0.06
Nodes (5): InMemorySessionStore, LeaderboardEntry, PostgresSessionStore, SessionRow, WeeklyBoard

### Community 84 - "Scheduler Tests"
Cohesion: 0.18
Nodes (4): _claimed_at(), _record(), TestCatchUp, TestTick

### Community 85 - "Layering Tests"
Cohesion: 0.14
Nodes (16): export(), languages(), main(), resolved_table(), _write(), _absolute_imports(), _sources(), test_known_violations_still_exist() (+8 more)

### Community 86 - "BismillahBot — Multilingual Support Plan"
Cohesion: 0.14
Nodes (14): 10. File-by-file change list, 11. Memory & performance (free-tier reality), 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 2. Current-state audit (what is hardcoded English), 3. Target architecture, 4. User language preference (+6 more)

### Community 87 - "Plan Builder: Portion"
Cohesion: 0.18
Nodes (5): Portion, match_portion(), portion_for(), portions_of(), TestPortionShape

### Community 88 - "verse_keyboard"
Cohesion: 0.14
Nodes (8): verse_keyboard(), mode_button(), _button(), data(), fake_bot(), TestLanguageFlags, TestVerseKeyboard, tg_bot()

### Community 89 - "auth.py"
Cohesion: 0.18
Nodes (12): _b64url(), _b64url_decode(), decode_token(), InvalidToken, issue_token(), _sign(), _unauthorized(), test_expired_token_is_rejected() (+4 more)

### Community 90 - "Store Contract Tests"
Cohesion: 0.11
Nodes (3): _spans(), TestHifzIntervalEdges, TestHifzIntervals

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.12
Nodes (17): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+9 more)

### Community 92 - "api/catalog.py"
Cohesion: 0.16
Nodes (10): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, ReaderPosition, Reciter, reciters() (+2 more)

### Community 93 - "Hifz platform frozen string manifest"
Cohesion: 0.13
Nodes (13): Translation Attributions, alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Hifz platform frozen string manifest, src/locales/en.py source of truth, Key conventions (btn_*, cmd_*) (+5 more)

### Community 94 - "Profiles: ProfileRow"
Cohesion: 0.06
Nodes (3): ProfileRow, ProfileStore, UserSettingsRow

### Community 95 - "parse_offset"
Cohesion: 0.15
Nodes (3): parse_offset(), TestParseOffset, TestPicker

### Community 97 - "test_media_cache_keys.py"
Cohesion: 0.15
Nodes (8): _bot(), _next_id(), send_audio(), send_photo(), no_cdn(), _source(), test_a_miss_caches_under_the_key_and_a_hit_replays_it(), test_a_rejected_cached_id_is_rebuilt_and_recached()

### Community 100 - ".exists"
Cohesion: 0.10
Nodes (7): put_position(), TestEveryParsedRefIsReal, TestExists, TestRandom, TestStructure, test_pick_ayah_handles_a_cross_surah_span(), test_the_whole_quran_is_a_valid_span()

### Community 102 - "test_hifz_progress.py"
Cohesion: 0.13
Nodes (4): quran_progress(), _at(), TestInputHandling, TestQuranProgress

### Community 103 - "Refactor — Implementation Plan"
Cohesion: 0.18
Nodes (10): tests/test_layering.py ratchet (KNOWN violations), Overlap with MULTI_PLATFORM_PLAN channel seam, Shared UTC offset picker (time_pickers.offset_keyboard), Decisions and open questions (§9), Found along the way (out-of-scope behaviour changes), Phase 0 — Guardrails (ruff, layering test, logging), Phase 5 — Fix the layering, Target layout (app/ bot/ services/ domain/ infra/) (+2 more)

### Community 104 - "recall_check.py"
Cohesion: 0.05
Nodes (33): _assemble(), _at_offset(), _ayah_text(), _basmala_prefix(), build_question(), _clean(), _continuation_question(), _date_key() (+25 more)

### Community 105 - "._send_media"
Cohesion: 0.15
Nodes (5): _build(), ignore_not_modified(), _send(), send_cached(), build()

### Community 107 - "Time Pickers"
Cohesion: 0.28
Nodes (7): offset_keyboard(), _grid(), test_a_label_prefix_changes_only_the_label(), test_cancel_data_adds_a_localized_cancel_row(), test_every_offset_is_offered_in_order_under_the_callers_prefix(), test_no_cancel_row_unless_asked(), test_rows_are_columns_wide()

### Community 108 - "hifz_progress.py"
Cohesion: 0.14
Nodes (7): _clip(), _covered(), _focus_surah(), _page_share(), ProgressSummary, _recency_key(), _surah_of()

### Community 109 - "bot/media.py"
Cohesion: 0.06
Nodes (26): 5. API surface (`/api/v1`), Phase 2 — WhatsApp MVP (reader + daily ayat), 1. Why, 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 1 — Take `main.py` apart (pure moves) — *done*, Phase 5 — Fix the layering — *done*, Phase 6 — Repository hygiene — *done* (+18 more)

### Community 110 - "_sent"
Cohesion: 0.19
Nodes (4): _callback_data(), _sent(), TestProfileCard, TestReminderTime

### Community 111 - "unittest_mock"
Cohesion: 0.12
Nodes (6): _stress_reset(), _stress_stats(), data(), fake_bot(), _no_network(), tg_bot()

### Community 113 - "store/__init__.py"
Cohesion: 0.10
Nodes (7): Caps, Incoming, SessionStore, MemoryState, _isolate_registries(), _isolate_registries(), TestCacheKey

### Community 114 - "Safety net (characterisation tests, staging smoke, blue-green)"
Cohesion: 0.14
Nodes (11): graphify knowledge graph (graphify-out/), CLAUDE.md graphify lookup rules, button_rows() row-packing helper, Copy-pasted patterns table (§1.3), GET / health with store and cache status (503), ignore_not_modified() context manager, Phase 2 — DRY the duplicated patterns, Phase 3 — One router for everything (+3 more)

### Community 115 - "Koyeb Capacity Report"
Cohesion: 0.25
Nodes (7): Koyeb free-tier capacity report, CPU-bound queueing failure mode (~24 msg/s ceiling), Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start), Neon managed Postgres, Capacity results 5-1000 concurrent (no errors, 70-91 MB), Stress environment (docker-compose.stress.yml, cpus 0.1, 512m), Synthetic traffic mix (scripts/stress/gen_updates.py)

### Community 116 - "Blue Green Ci"
Cohesion: 0.14
Nodes (13): concurrency, cancel-in-progress, group, env, PYTHON_DEFAULT, name, on, pull_request (+5 more)

### Community 117 - "Blue Green Ci: name"
Cohesion: 0.23
Nodes (14): steps, steps, steps, steps, steps, steps, steps, env (+6 more)

### Community 118 - "features/progress.py"
Cohesion: 0.09
Nodes (15): surah_name(), _translation_text(), forgot_command(), on_progress_tap(), progress_command(), progress_view(), _show(), _surah_line() (+7 more)

### Community 119 - "Export Web Content Tests"
Cohesion: 0.21
Nodes (7): _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah(), test_meta_surahs_and_sajdas(), test_tafsir_has_every_ayah()

### Community 120 - "reciter_set_confirmation"
Cohesion: 0.13
Nodes (6): Phase 4 — Split infrastructure god-objects — *done*, reciter_set_confirmation(), performers(), reciter_kind(), TestCatalogKinds, TestKindWarnings

### Community 121 - "_seed_legacy_lang"
Cohesion: 0.21
Nodes (3): _seed_legacy_lang(), TestInlineCaller, TestLegacyMigration

### Community 122 - ".get_next_ayah"
Cohesion: 0.22
Nodes (5): 4. Navigation model, Page images and page audio, Structural divisions (page / juz / sajda), Translation-only catalogue entries, TestNavigation

### Community 123 - "streak.py"
Cohesion: 0.22
Nodes (7): _caption(), _keyboard(), on_streak(), _send_graph(), streak(), cache_key(), StreakSummary

### Community 124 - "InMemoryScheduleStore"
Cohesion: 0.10
Nodes (3): InMemoryIdentityStore, InMemoryStore, InMemoryScheduleStore

### Community 125 - "PostgresScheduleStore"
Cohesion: 0.10
Nodes (4): PostgresStore, Store, PostgresScheduleStore, store()

### Community 126 - "Mini App Plan: normalize_lang"
Cohesion: 0.22
Nodes (6): 4.1 Flow, 4.2 Rules, 4.3 Transport, 4. Authentication, normalize_lang(), TestNormalizeLang

### Community 127 - "Blue Green Ci: jobs"
Cohesion: 0.15
Nodes (13): name, needs, runs-on, jobs, build, lint, rollback, name (+5 more)

### Community 128 - "Blue Green Ci: with"
Cohesion: 0.15
Nodes (13): with, cache, cache-dependency-path, cache-from, cache-to, context, if-no-files-found, load (+5 more)

### Community 130 - "parse_ayah_range"
Cohesion: 0.07
Nodes (20): 1. Overview, 2. Architecture, 3. Request lifecycle, 5. Caching strategy, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic, Local time (+12 more)

### Community 132 - "Mini App Plan: Separate quranayatminiapp Nextjs"
Cohesion: 0.22
Nodes (10): Page audio with stitched fallback, Page image stitching (lib/page_image.py), Structural divisions (page / juz / sajda from quran-data.xml), Uthmani text in Amiri Quran / KFGQPC font, Client-side playlist audio (no server stitching), Locale export to JSON (web_ keys, next-intl), Static immutable Quran JSON served from frontend CDN, Daily ayat cost model on WhatsApp (+2 more)

### Community 135 - "Media: range_audio"
Cohesion: 0.11
Nodes (6): range_audio(), content(), TestRangeAudioRoute, fake_download(), TestStitching, __init__()

### Community 140 - "Business Logic: The hifz platform memorization"
Cohesion: 0.10
Nodes (15): Central callback prefix allocation (hifz.PREFIXES), Future roadmap and prioritized backlog, The hifz platform (memorization companion), Inline query answering (all four representations, ranges), Navigation model ((surah, ayah, type) per chat_id), Pure plan builder (build_plan), Streak day ticks on completed session, Verse card (inline keyboard, edit in place) (+7 more)

### Community 143 - "reader.py"
Cohesion: 0.07
Nodes (22): _board_message(), leaderboard(), on_leaderboard(), juz(), page(), turn_page(), random_ayah(), read_text() (+14 more)

### Community 144 - "week_window"
Cohesion: 0.25
Nodes (3): user_week_window(), week_window(), TestWeekWindow

### Community 145 - "6. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 6. Phased task breakdown, Phase 0 — Prerequisites (no code), Phase 1 — Channel seam (this repo, no user-visible change), Phase 3 — Hifz on WhatsApp, Phase 4 — Recitation checker on WhatsApp, Phase 5 — Web access outside Telegram, Phase 6 — Later

### Community 146 - "test_channels_telegram.py"
Cohesion: 0.25
Nodes (3): bot(), cache(), TestChoice

### Community 147 - "to_markup"
Cohesion: 0.29
Nodes (3): to_button(), to_markup(), TestToMarkup

### Community 148 - "Hifz Seam Tests: test_hifz_seampy"
Cohesion: 0.18
Nodes (3): _isolate_registries(), _Settings, TestSchemaApplication

### Community 153 - "test_hifz_profile.py"
Cohesion: 0.21
Nodes (5): _CallbackQuery, _isolate_registries(), _Message, _Settings, _User

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 155 - "json"
Cohesion: 0.27
Nodes (5): build(), main_(), _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl()

### Community 156 - "_edited"
Cohesion: 0.22
Nodes (4): _buttons(), _edited(), TestCallbackDataDiscipline, TestTimezone

### Community 162 - "Blue Green Ci: postgres"
Cohesion: 0.22
Nodes (9): POSTGRES_DB, POSTGRES_HOST_AUTH_METHOD, POSTGRES_USER, env, image, options, ports, postgres (+1 more)

### Community 163 - "Blue Green Ci: test"
Cohesion: 0.22
Nodes (9): TEST_DATABASE_URL, test, python-version, fail-fast, matrix, env, name, runs-on (+1 more)

### Community 164 - "Blue Green Ci: preflight"
Cohesion: 0.22
Nodes (9): preflight, active, deploy_enabled, target, if, name, needs, outputs (+1 more)

### Community 166 - "services/streaks.py"
Cohesion: 0.10
Nodes (16): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut (+8 more)

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 172 - "parse_quran"
Cohesion: 0.22
Nodes (5): 7. Known limitations / tech debt, 12. Testing, 5. Content: multi-translation loading (memory-aware), Translation catalogue (initial set), parse_quran()

### Community 173 - "export"
Cohesion: 0.36
Nodes (6): build_meta(), export(), main(), _spans(), split_basmalah(), _write()

### Community 175 - "Scheduler Tests: test_schedulerpy"
Cohesion: 0.32
Nodes (3): _isolate_handlers(), state(), store()

### Community 178 - "BismillahBot README"
Cohesion: 0.15
Nodes (13): Four ayah representations (english, tafsir, arabic, audio), Known limitations / tech debt, Issues fixed in the refactor (12 bugs), Documentation, Documentation index (docs/README.md), Phase 6 — Repository hygiene, CI — Blue-Green pipeline, Running the tests locally (+5 more)

### Community 179 - "load_summary"
Cohesion: 0.33
Nodes (3): SurahProgress, load_summary(), TestLoadSummary

### Community 180 - "plan_builder.py"
Cohesion: 0.31
Nodes (3): _advance(), next_scheduled_date(), _validated_days()

### Community 182 - "Blue Green Ci: deploygreen"
Cohesion: 0.33
Nodes (6): environment, if, name, needs, runs-on, deploy-green

### Community 183 - "Blue Green Ci: promote"
Cohesion: 0.33
Nodes (6): promote, environment, if, name, needs, runs-on

### Community 184 - "Profile settings reset fix (fix/settings-persistence)"
Cohesion: 0.29
Nodes (8): ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable, lib/utils.File god class, Silent in-memory store fallback, Phase 4 — Split infrastructure god-objects, Profile settings reset fix (fix/settings-persistence), Typed frozen Settings (config/settings.py), conftest.py test environment (src on path, CWD pin, no Redis/network), Environment configuration (webhook, CDN base URLs, Redis)

## Knowledge Gaps
- **51 isolated node(s):** `button_rows() row-packing helper`, `ignore_not_modified() context manager`, `Found along the way (out-of-scope behaviour changes)`, `Phase 0 — Guardrails (ruff, layering test, logging)`, `ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1542 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **105 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `Context` to `summarize`, `auth.py`, `Leaderboard`, `_ctx`, `Store`, `build_grid`, `services/streaks.py`, `reader.py`, `User Settings`, `RedisSingleton`, `typing`, `Hifz Progress Cmd Tests`, `Hifz Streak Tests`, `Acceptance Tests`, `services/streaks.py`, `Session`, `SendCtx`, `Streaks`, `Services`, `Progress`, `Dispatch`, `load_summary`, `test_hifz_check.py`, `_hifz`, `surah_progress`, `api/plans.py`, `quran.py`, `Tick`, `build_question`, `api/catalog.py`, `test_hifz_progress.py`, `bot/media.py`, `_sent`, `store/__init__.py`, `InMemoryScheduleStore`, `PostgresScheduleStore`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `button_rows() row-packing helper`, `ignore_not_modified() context manager`, `Found along the way (out-of-scope behaviour changes)` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_plan` be split into smaller, more focused modules?**
  _Cohesion score 0.09936575052854123 - nodes in this community are weakly interconnected._
- **Why does `Quran` connect `Quran` to `build_plan`, `parse_ayah_range`, `summarize`, `services/plans.py`, `Plan Setup`, `Media: range_audio`, `Profile`, `reader.py`, `Refs`, `typing`, `Hifz Progress Cmd Tests`, `Hifz Progress: quran_page_progress`, `test_recall_check.py`, `TranslationRegistry`, `test_miniapp_links.py`, `auto_pace`, `parse_quran`, `export`, `Progress`, `plan_builder.py`, `advancing`, `Refs: get_surah_length`, `_parse_answer`, `_message`, `surah_progress`, `api/plans.py`, `features/check.py`, `quran.py`, `Hifz Progress: juz_progress`, `verse_keyboard`, `api/catalog.py`, `.exists`, `test_hifz_progress.py`, `recall_check.py`, `hifz_progress.py`, `bot/media.py`, `features/progress.py`, `Export Web Content Tests`, `.get_next_ayah`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `Quran` (e.g. with `Module responsibilities` and `build_meta()`) actually correct?**
  _`Quran` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `Quran` be split into smaller, more focused modules?**
  _Cohesion score 0.10574712643678161 - nodes in this community are weakly interconnected._