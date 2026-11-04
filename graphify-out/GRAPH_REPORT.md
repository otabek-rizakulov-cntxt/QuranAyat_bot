# Graph Report - QuranAyat_bot  (2026-11-04)

## Corpus Check
- 277 files · ~263,267 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 5065 nodes · 12150 edges · 293 communities (148 shown, 145 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 1156 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `982d0d0c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_plan
- link_token.py
- Phase 1 — Take `main.py` apart (pure moves) — *done*
- deliver_push
- Wizard
- Ctx
- features/profile.py
- .page_range
- to_whatsapp
- test_hifz_leaderboard.py
- _ctx
- services/plans.py
- _tap
- build_grid
- lifespan.py
- UserSettings
- Context
- test_store_selection.py
- Refs
- RedisSingleton
- lifespan.py
- WhatsAppChannel
- InMemoryIdentityStore
- Hifz Progress Cmd Tests
- group.py
- Refactor — Implementation Plan
- TelegramChannel
- Hifz Streak Tests
- Hifz Platform
- Acceptance Tests
- features/progress.py
- Docker Compose.stress
- _png
- test_recall_check.py
- .get
- reciter_set_confirmation
- _plan_preview.py
- Recitation Checker Investigation
- round_percent
- fixture
- to_markup
- services/check.py
- PostgresPlanStore
- surah_progress
- WhatsApp
- Streaks
- Load Test
- Keyboard localization challenge (reverse-map vs inline callback_data)
- Text
- Schema
- Services
- dispatch.py
- Dispatch
- PlanDaySpec
- PostgresProfileStore
- Inline Reciter Search Tests
- quran_page_progress
- api/progress.py
- os
- PostgresScheduleStore
- test_wizard.py
- Dispatch Order Tests
- Wizard
- Mini App Plan
- juz_progress
- store/__init__.py
- IdentityStore
- TestSummarize
- scheduler/__init__.py
- parse_offset
- InMemoryGroupStore
- reset_for_tests
- Hifz Seam Tests
- session.py
- Quran
- parse_offset
- tick.py
- Profiles: InMemoryProfileStore
- bundle_translations.py
- Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd
- BismillahBot — Business Logic
- juz_ref
- Groups: PostgresGroupStore
- SessionStore
- Scheduler Tests
- weekly_board
- whatsapp_format.py
- Ref
- .get
- auth.py
- Store Contract Tests
- Multi Platform Plan: MultiPlatform Implementation Plan
- dispatch.py
- _hifz
- Dependency rule (app -> bot -> services -> domain)
- handle_message
- Hifz Seam Tests: TestRegistration
- _seed_legacy_lang
- Scheduler Tests: TestTransientFailuresAreRetried
- Store Contract Tests: TestPlans
- GraphClient
- File
- _at
- stats.py
- recall_check.py
- InMemoryIdentityStore
- TestDaily
- button_action
- quran_progress
- infra/__init__.py
- week_window
- test_page_mode.py
- TestSchedule
- store/__init__.py
- Profile settings reset fix (fix/settings-persistence)
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- .get_next_ayah
- parse_ayah
- percentile_band
- _Ratio
- build_question
- _send_graph
- .exists
- plan_builder.py
- TestHelpers
- Blue Green Ci: jobs
- Blue Green Ci: with
- test_whatsapp_config.py
- test_navigation.py
- test_media_cache_keys.py
- Mini App Plan: Separate quranayatminiapp Nextjs
- InMemoryScheduleStore
- Channel
- range_audio
- features/check.py
- GroupStore
- main.py
- parse_ayah_range
- MINI_APP_PLAN.md
- ScheduledSend
- TestRestartDeliversExactlyOnce
- test_export_web_content.py
- t
- locales/__init__.py
- InMemoryPlanStore
- TestLeaderboard
- format_offset
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- split
- offset_keyboard
- Blue Green Ci: env
- test_channels_whatsapp.py
- TestProfiles
- graphify-autopush.sh
- IdentityRow
- MINI_APP_PLAN.md
- Settings Tests
- fetch_and_stitch
- Blue Green Ci: postgres
- Blue Green Ci: test
- Blue Green Ci: preflight
- GroupPlanDayRow
- ProfileStore
- Hifz Seam Tests: TestPrefixNamespace
- Hifz Seam Tests: TestDispatchCallback
- button_action
- Blue Green Ci: smokegreen
- BismillahBot — Multilingual Support Plan
- UserSettingsRow
- File Facade: search_performers
- test_keyboard_snapshots.py
- .is_cancel
- TestRunScheduler
- BismillahBot README
- Translation editions table (48 codes)
- Telegram
- ayah_for
- Blue Green Ci: deploygreen
- Blue Green Ci: promote
- test_the_basmala_heading_is_not_part_of_the_question
- TestVoiceNotes
- Hifz Seam Tests: test_longest_prefix_wins
- TestReaderPosition
- .get_surah_length
- test_pick_ayah_accepts_anything_with_as_tuple
- TestIdentity
- Claude
- test_the_answer_is_not_findable_by_sorting_on_length
- test_sweep_produces_a_well_formed_question_everywhere
- Hifz Seam Tests: TestDispatchCommand
- test_options_are_distinct_even_ignoring_vowelling
- .wa_user
- test_prompt_is_never_offered_back_as_an_option
- json
- pages.py
- test_correct_option_really_follows_the_prompt
- test_both_question_modes_show_up_in_the_sweep
- test_next_ayah_mode_answers_with_the_whole_short_ayah
- test_hifz_seam.py
- WhatsAppChannel
- TestSessions
- test_long_ayah_prompt_and_options_stay_button_sized
- export
- test_next_ayah_prompt_is_truncated_and_says_so
- PageProgress
- SurahProgress
- test_every_option_carries_the_same_word_count
- test_hifz_progress.py
- test_same_inputs_give_the_same_question
- test_a_different_date_gives_a_different_question
- week_bounds
- TestSettings
- get_store
- features/daily.py
- test_dates_and_iso_strings_are_interchangeable
- test_the_global_random_module_is_never_touched
- test_the_answer_does_not_always_land_in_the_same_slot
- milestone_for
- api/plans.py
- test_the_first_and_last_ayah_of_the_quran
- test_muqattaat_get_muqattaat_shaped_distractors
- test_no_option_carries_a_reference_suffix_or_a_bom
- test_options_need_no_html_escaping_beyond_the_callers
- test_pick_then_build_is_the_whole_check_flow
- test_preload_corpus_returns_the_same_cached_object
- swept
- test_correct_option_is_never_a_length_outlier
- test_correct_option_is_never_the_extreme_by_a_wide_ratio
- TestRegistration
- test_scheduler.py
- _callback
- Graph
- channels/whatsapp.py
- TestRegistration

## God Nodes (most connected - your core abstractions)
1. `get_store()` - 173 edges
2. `Ctx` - 145 edges
3. `Quran` - 139 edges
4. `t()` - 128 edges
5. `handle_update()` - 103 edges
6. `fixture()` - 84 edges
7. `UserSettings` - 81 edges
8. `build_plan()` - 72 edges
9. `File` - 64 edges
10. `Choice` - 62 edges

## Surprising Connections (you probably didn't know these)
- `2. Current-state audit (what is hardcoded English)` --references--> `build_data()`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/app/lifespan.py
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `The seam (`src/hifz/`)` --references--> `handle_update()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/bot/dispatch.py
- `Detection & selection flow` --references--> `handle_update()`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/bot/dispatch.py
- `2. Goals and non-goals` --references--> `handle_update()`  [INFERRED]
  docs/REFACTOR_PLAN.md → src/bot/dispatch.py

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

## Communities (293 total, 145 thin omitted)

### Community 0 - "build_plan"
Cohesion: 0.06
Nodes (14): advancing(), build_plan(), surah_ref(), assert_covers_target_once(), assert_well_formed(), spans(), TestAcrossTheWholeQuran, TestAlMulkAcceptance (+6 more)

### Community 1 - "link_token.py"
Cohesion: 0.11
Nodes (12): _b64(), InvalidLinkToken, issue(), _key(), redeem(), _secret(), _unb64(), configured() (+4 more)

### Community 2 - "Phase 1 — Take `main.py` apart (pure moves) — *done*"
Cohesion: 0.09
Nodes (21): 1. Why, 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 1 — Take `main.py` apart (pure moves) — *done*, Phase 2 — DRY the duplicated patterns — *done*, Phase 4 — Split infrastructure god-objects — *done* (+13 more)

### Community 3 - "deliver_push"
Cohesion: 0.14
Nodes (13): deliver_push(), _log(), ctx_for(), graph(), Graph, say_hi(), templates_allowed(), test_every_push_is_logged_for_cost_tracking() (+5 more)

### Community 4 - "Wizard"
Cohesion: 0.12
Nodes (3): TestAccumulation, TestLifecycle, TestOneDraftPerUser

### Community 5 - "Ctx"
Cohesion: 0.08
Nodes (40): Ctx, _ask(), on_check(), _question_text(), _score(), on_group_tap(), _save_group_plan(), setup_step() (+32 more)

### Community 6 - "features/profile.py"
Cohesion: 0.08
Nodes (26): patch_profile(), _cancel_keyboard(), _join_board(), name_step(), offset_from_callback(), on_profile_tap(), _plan_line(), profile_command() (+18 more)

### Community 7 - ".page_range"
Cohesion: 0.10
Nodes (3): _consolidations(), test_page_boundaries_match_the_bot(), TestDivisionsTileTheQuran

### Community 8 - "to_whatsapp"
Cohesion: 0.17
Nodes (3): to_whatsapp(), TestTags, TestWhatTheBotSends

### Community 9 - "test_hifz_leaderboard.py"
Cohesion: 0.12
Nodes (10): _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join(), _Message, _sent(), _Settings (+2 more)

### Community 10 - "_ctx"
Cohesion: 0.08
Nodes (17): _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _isolate_registries(), _Message, _profile_row() (+9 more)

### Community 11 - "services/plans.py"
Cohesion: 0.08
Nodes (24): active(), lifecycle(), _plan_out(), today(), change_status(), complete_day(), current_plan(), day_position() (+16 more)

### Community 12 - "_tap"
Cohesion: 0.13
Nodes (4): _run_wizard(), _tap(), TestDrill, TestEnqueueChain

### Community 13 - "build_grid"
Cohesion: 0.07
Nodes (13): render(), build_grid(), _counts(), draw_contribution_graph(), Grid, level_for(), render_streak_graph(), _semaphore() (+5 more)

### Community 14 - "lifespan.py"
Cohesion: 0.04
Nodes (36): _commands_for(), initialize(), _set_bot_commands(), answer_inline_query(), get_default_query_results(), inline_audio_result(), inline_photo_results(), combined_audio_key() (+28 more)

### Community 15 - "UserSettings"
Cohesion: 0.15
Nodes (7): _legacy_lang_key(), SettingsRow, UserSettings, TestDefaults, TestIndependence, TestKeyedByUserId, TestRoundTrip

### Community 16 - "Context"
Cohesion: 0.16
Nodes (13): _bot(), _ctx(), _member(), _run_setup_to_plan(), _Settings, TestBoard, tap(), TestBoardJoin (+5 more)

### Community 17 - "test_store_selection.py"
Cohesion: 0.06
Nodes (15): health(), cache_backend(), database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries(), fresh_redis() (+7 more)

### Community 18 - "Refs"
Cohesion: 0.07
Nodes (11): _clean(), format_ref(), parse_range(), parse_reference(), TestSurahSpans, TestAcrossSurahs, TestEveryParsedRefIsReal, TestFormatting (+3 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.05
Nodes (24): 5. Caching strategy, 6. Issues fixed in this refactor, 11.1 Profile settings reset after a while — `fix/settings-persistence`, 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, _code_key(), issue(), redeem() (+16 more)

### Community 20 - "lifespan.py"
Cohesion: 0.07
Nodes (15): 3. Principles applied, lifespan(), _process_update(), telegram_webhook(), webhook_secret(), _first_delivery(), messages_of(), _process() (+7 more)

### Community 21 - "WhatsAppChannel"
Cohesion: 0.15
Nodes (4): _bytes_and_name(), _resolve(), _split_choices(), TestMedia

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "group.py"
Cohesion: 0.10
Nodes (17): _begin_setup(), bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), _enqueue_next_board(), _enqueue_next_group() (+9 more)

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.09
Nodes (22): graphify knowledge graph (graphify-out/), CLAUDE.md graphify lookup rules, 10. Found along the way (out of scope — behaviour changes), 2. Goals and non-goals, 6. Ordering, risk, size, 7. Safety net, 8. Expected result, 9. Decisions and open questions (+14 more)

### Community 26 - "TelegramChannel"
Cohesion: 0.05
Nodes (14): _build(), ignore_not_modified(), _send(), send_cached(), TelegramChannel, build(), test_any_other_bad_request_propagates(), test_not_modified_is_swallowed() (+6 more)

### Community 27 - "Hifz Streak Tests"
Cohesion: 0.10
Nodes (14): cache_key(), _caption(), _ctx(), _earn(), _isolate_registries(), _photo_message(), _Settings, _streak() (+6 more)

### Community 28 - "Hifz Platform"
Cohesion: 0.07
Nodes (28): Hifz Platform - Plan & Progress, Phase 1 acceptance criteria (tests/test_acceptance.py), Hifz change log, claim_due claimed_at clock bug, Hifz data model (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send, group_*), Phase 2 group cluster (J1-J6, forum topics), Workstream I: i18n & commands for 48 locales, Workstream C: interval merge-on-insert + derived percentages (+20 more)

### Community 29 - "Acceptance Tests"
Cohesion: 0.12
Nodes (13): _CallbackQuery, _cmd(), _ctx(), _isolate_registries(), _Message, _run_wizard(), _save_plan(), _Settings (+5 more)

### Community 30 - "features/progress.py"
Cohesion: 0.09
Nodes (15): surah_name(), forgot_command(), on_progress_tap(), progress_command(), progress_view(), _show(), _surah_line(), button_rows() (+7 more)

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 33 - "test_recall_check.py"
Cohesion: 0.18
Nodes (3): test_pick_ayah_is_deterministic_per_user_and_date(), test_pick_ayah_on_an_inverted_or_empty_span(), test_unknown_ayahs_are_rejected()

### Community 34 - ".get"
Cohesion: 0.09
Nodes (8): 10. File-by-file change list, 3. Target architecture, What's covered, TranslationRegistry, TestCorpusIntegrity, TestAvailable, TestCaching, TestFallback

### Community 35 - "reciter_set_confirmation"
Cohesion: 0.15
Nodes (4): reciter_set_confirmation(), reciter_kind(), TestCatalogKinds, TestKindWarnings

### Community 36 - "_plan_preview.py"
Cohesion: 0.19
Nodes (3): _portion_label(), Portion, TestPortionShape

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.07
Nodes (29): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards (+21 more)

### Community 38 - "round_percent"
Cohesion: 0.19
Nodes (3): format_percent(), round_percent(), TestRounding

### Community 39 - "fixture"
Cohesion: 0.05
Nodes (33): create_app(), build_data(), signature(), make_index(), data(), data(), data(), data() (+25 more)

### Community 40 - "to_markup"
Cohesion: 0.05
Nodes (25): page_keyboard(), reciter_keyboard(), reciter_label(), reciter_page_count(), reciter_page_of(), reciter_search_keyboard(), to_markup(), reciter_catalog() (+17 more)

### Community 41 - "services/check.py"
Cohesion: 0.15
Nodes (7): pick_ayah(), preload_corpus(), ask(), default_span(), rebuild(), Score, score()

### Community 42 - "PostgresPlanStore"
Cohesion: 0.07
Nodes (4): PlanDayRow, PlanRow, PlanStore, PostgresPlanStore

### Community 43 - "surah_progress"
Cohesion: 0.14
Nodes (4): started_surahs(), surah_progress(), TestSpecAcceptance, TestSurahProgress

### Community 45 - "Streaks"
Cohesion: 0.13
Nodes (4): record_session(), TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 46 - "Load Test"
Cohesion: 0.10
Nodes (14): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+6 more)

### Community 47 - "Keyboard localization challenge (reverse-map vs inline callback_data)"
Cohesion: 0.25
Nodes (4): locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), setMyCommands per language, Phase 3 — One router for everything

### Community 48 - "Text"
Cohesion: 0.23
Nodes (6): _inline_query(), _of_type(), _results(), TestInlineArabicImage, TestRangeAudio, TestRangeText

### Community 49 - "Schema"
Cohesion: 0.11
Nodes (27): daily_ayah_sub, group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval (+19 more)

### Community 50 - "Services"
Cohesion: 0.15
Nodes (20): client(), _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today() (+12 more)

### Community 51 - "dispatch.py"
Cohesion: 0.06
Nodes (28): Phase 3 — One router for everything — *done*, handle_incoming(), _incoming(), _on_callback(), _on_text(), _search_reciters(), _board_message(), leaderboard() (+20 more)

### Community 52 - "Dispatch"
Cohesion: 0.22
Nodes (16): handle_update(), _callback(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index(), test_inline_query_valid_ayah_returns_all_four_views(), test_language_shows_inline_keyboard() (+8 more)

### Community 55 - "Inline Reciter Search Tests"
Cohesion: 0.15
Nodes (18): _audio_result(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter(), test_ayah_audio_dropped_without_public_base_url(), test_ayah_audio_uses_callers_reciter(), test_ayah_query_is_personal_and_briefly_cached() (+10 more)

### Community 56 - "quran_page_progress"
Cohesion: 0.11
Nodes (4): juz_page_progress(), quran_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 57 - "api/progress.py"
Cohesion: 0.20
Nodes (15): forget(), ForgetIn, ForgetOut, _juz(), JuzRatio, progress(), ProgressOut, Ratio (+7 more)

### Community 58 - "os"
Cohesion: 0.10
Nodes (22): main(), placeholders(), export(), languages(), main(), resolved_table(), _write(), _modules() (+14 more)

### Community 60 - "test_wizard.py"
Cohesion: 0.14
Nodes (3): test_draft_is_written_with_that_ttl(), TestCoexistsWithTheReciterFlow, wiz()

### Community 61 - "Dispatch Order Tests"
Cohesion: 0.19
Nodes (16): _callback(), fake_bot(), _message(), probe(), _sent_a_verse(), test_a_command_beats_a_pending_reciter_search(), test_a_command_escapes_a_wizard_without_ending_it(), test_a_pending_reciter_search_beats_a_wizard() (+8 more)

### Community 62 - "Wizard"
Cohesion: 0.18
Nodes (7): Wizard, _CallbackQuery, _ctx(), _Message, _Settings, TestWizard, _type()

### Community 63 - "Mini App Plan"
Cohesion: 0.08
Nodes (25): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 4.1 Flow, 4.2 Rules (+17 more)

### Community 64 - "juz_progress"
Cohesion: 0.16
Nodes (5): juz_progress(), JuzProgress, _spans(), started_juzs(), TestJuzProgress

### Community 65 - "store/__init__.py"
Cohesion: 0.09
Nodes (8): Milestone, offset_of(), StreakCounts, HifzStore, store_backend(), MemoryState, SessionOutcome, user_offset()

### Community 67 - "TestSummarize"
Cohesion: 0.10
Nodes (4): Progress, ProgressSummary, summarize(), TestSummarize

### Community 68 - "scheduler/__init__.py"
Cohesion: 0.13
Nodes (6): _send_plain_message(), register_send_handler(), registered_kinds(), _same_origin(), decorate(), SendCtx

### Community 69 - "parse_offset"
Cohesion: 0.15
Nodes (3): parse_offset(), TestParseOffset, TestPicker

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 73 - "session.py"
Cohesion: 0.13
Nodes (22): init_data_max_age(), jwt_secret(), auth_link(), auth_telegram(), AuthOut, LinkAuthIn, me(), _me() (+14 more)

### Community 74 - "Quran"
Cohesion: 0.11
Nodes (14): session(), random_ayah(), read_text(), reader_position(), repeat(), _send_verse(), verse_card(), verse_keyboard() (+6 more)

### Community 75 - "parse_offset"
Cohesion: 0.12
Nodes (9): _as_utc(), local_date(), local_now(), local_time(), next_due_utc(), to_utc(), TestLocalDate, TestNextDueUtc (+1 more)

### Community 76 - "tick.py"
Cohesion: 0.13
Nodes (12): catch_up(), run_scheduler(), _wait(), _deliver(), _is_stale(), _lock(), _release(), _resolve() (+4 more)

### Community 78 - "bundle_translations.py"
Cohesion: 0.16
Nodes (8): _clean_state_store(), bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.12
Nodes (18): Audio catalog kinds, Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES), Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points), Error taxonomy L1-L5 (word, harakah, tajwid, riwayah mismatch, waqf), Evaluation plan (false-alarm gate < 2% per ayah) (+10 more)

### Community 80 - "BismillahBot — Business Logic"
Cohesion: 0.12
Nodes (14): 1. Overview, 2. Architecture, 3. Request lifecycle, 7. Known limitations / tech debt, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic, Local time (+6 more)

### Community 81 - "juz_ref"
Cohesion: 0.17
Nodes (5): juz_ref(), page_ref(), to_day_specs(), TestJuzAndPage, TestStorageShape

### Community 83 - "SessionStore"
Cohesion: 0.07
Nodes (6): InMemorySessionStore, LeaderboardEntry, PostgresSessionStore, SessionRow, SessionStore, WeeklyBoard

### Community 84 - "Scheduler Tests"
Cohesion: 0.17
Nodes (4): _claimed_at(), _record(), TestCatchUp, TestTick

### Community 85 - "weekly_board"
Cohesion: 0.28
Nodes (3): weekly_board(), make_user(), TestWeeklyBoard

### Community 86 - "whatsapp_format.py"
Cohesion: 0.20
Nodes (3): _Converter, _render(), _wrap()

### Community 87 - "Ref"
Cohesion: 0.09
Nodes (14): _clip(), _covered(), _focus_surah(), _intersect(), _page_share(), _pages_of(), _recency_key(), _surah_of() (+6 more)

### Community 89 - "auth.py"
Cohesion: 0.11
Nodes (32): _b64url(), _b64url_decode(), decode_token(), _init_data_secret(), InvalidInitData, InvalidToken, issue_token(), _sign() (+24 more)

### Community 90 - "Store Contract Tests"
Cohesion: 0.11
Nodes (3): _spans(), TestHifzIntervalEdges, TestHifzIntervals

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.08
Nodes (24): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+16 more)

### Community 92 - "dispatch.py"
Cohesion: 0.07
Nodes (18): set_menu_button(), to_button(), TestCodes, bot(), cache(), TestChoice, tg_bot(), _app_command() (+10 more)

### Community 93 - "_hifz"
Cohesion: 0.06
Nodes (11): HifzInterval, _assert_invariant(), _ayahs(), _hifz(), _spans(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order() (+3 more)

### Community 94 - "Dependency rule (app -> bot -> services -> domain)"
Cohesion: 0.22
Nodes (8): tests/test_layering.py ratchet (KNOWN violations), Overlap with MULTI_PLATFORM_PLAN channel seam, Decisions and open questions (§9), Phase 0 — Guardrails (ruff, layering test, logging), Phase 5 — Fix the layering, Target layout (app/ bot/ services/ domain/ infra/), Timezone picker by country (feat/timezone-by-country), Memorizing (hifz): /memorize, /check, /progress, /streak, /leaderboard, /profile

### Community 95 - "handle_message"
Cohesion: 0.06
Nodes (30): _allowed_command(), as_command(), handle_message(), lang_hint(), _tap(), _buttons(), _due_rows(), graph() (+22 more)

### Community 97 - "_seed_legacy_lang"
Cohesion: 0.19
Nodes (3): _seed_legacy_lang(), TestInlineCaller, TestLegacyMigration

### Community 101 - "File"
Cohesion: 0.08
Nodes (6): File, TestAudioNeverFollowsLanguage, TestAudioFilename, TestImageFilename, TestLegacyLanguageKey, TestStateStore

### Community 103 - "stats.py"
Cohesion: 0.35
Nodes (8): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut

### Community 104 - "recall_check.py"
Cohesion: 0.06
Nodes (27): _assemble(), _ayah_text(), _basmala_prefix(), build_question(), _clean(), _continuation_question(), corpus(), _date_key() (+19 more)

### Community 107 - "button_action"
Cohesion: 0.27
Nodes (3): button_action(), _reverse_button_map(), TestButtonAction

### Community 109 - "infra/__init__.py"
Cohesion: 0.08
Nodes (10): download_combined_audio(), download_stitched_audio(), content(), fake_bot(), public_url(), fake_download(), TestStitching, __init__() (+2 more)

### Community 110 - "week_window"
Cohesion: 0.25
Nodes (3): user_week_window(), week_window(), TestWeekWindow

### Community 111 - "test_page_mode.py"
Cohesion: 0.09
Nodes (13): send_page(), send_repeated_audio(), _buffer(), fake_bot(), _stub_audio(), _stub_stitch(), stub(), TestPageAudio (+5 more)

### Community 113 - "store/__init__.py"
Cohesion: 0.06
Nodes (10): DailyStore, DailySubRow, InMemoryDailyStore, PostgresDailyStore, InMemoryStore, PostgresStore, Store, store() (+2 more)

### Community 114 - "Profile settings reset fix (fix/settings-persistence)"
Cohesion: 0.22
Nodes (10): ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable, lib/utils.File god class, GET / health with store and cache status (503), Silent in-memory store fallback, Phase 4 — Split infrastructure god-objects, Profile settings reset fix (fix/settings-persistence), Typed frozen Settings (config/settings.py), Blue-Green CI pipeline (blue-green-ci.yml) (+2 more)

### Community 115 - "Koyeb Capacity Report"
Cohesion: 0.25
Nodes (7): Koyeb free-tier capacity report, CPU-bound queueing failure mode (~24 msg/s ceiling), Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start), Neon managed Postgres, Capacity results 5-1000 concurrent (no errors, 70-91 MB), Stress environment (docker-compose.stress.yml, cpus 0.1, 512m), Synthetic traffic mix (scripts/stress/gen_updates.py)

### Community 116 - "Blue Green Ci"
Cohesion: 0.14
Nodes (13): concurrency, cancel-in-progress, group, env, PYTHON_DEFAULT, name, on, pull_request (+5 more)

### Community 117 - "Blue Green Ci: name"
Cohesion: 0.23
Nodes (14): steps, steps, steps, steps, steps, steps, steps, env (+6 more)

### Community 118 - ".get_next_ayah"
Cohesion: 0.22
Nodes (5): 4. Navigation model, Page images and page audio, Structural divisions (page / juz / sajda), Translation-only catalogue entries, TestNavigation

### Community 122 - "build_question"
Cohesion: 0.06
Nodes (23): _parse_answer(), compute_streak(), refresh_streaks(), streak_summary(), user_today(), _answer_data(), _AnyDay, _ask() (+15 more)

### Community 123 - "_send_graph"
Cohesion: 0.26
Nodes (6): _caption(), _keyboard(), on_streak(), _send_graph(), streak(), StreakSummary

### Community 124 - ".exists"
Cohesion: 0.09
Nodes (10): get_position(), put_position(), ReaderPosition, test_every_entry_is_a_real_ayah(), TestExists, TestRandom, TestStructure, TestSurahMeta (+2 more)

### Community 125 - "plan_builder.py"
Cohesion: 0.31
Nodes (3): _advance(), next_scheduled_date(), _validated_days()

### Community 126 - "TestHelpers"
Cohesion: 0.07
Nodes (9): _covers(), InMemoryHifzStore, _merge_span(), _normalize(), _overlaps(), PostgresHifzStore, _split_span(), _touches() (+1 more)

### Community 127 - "Blue Green Ci: jobs"
Cohesion: 0.15
Nodes (13): name, needs, runs-on, jobs, build, lint, rollback, name (+5 more)

### Community 128 - "Blue Green Ci: with"
Cohesion: 0.15
Nodes (13): with, cache, cache-dependency-path, cache-from, cache-to, context, if-no-files-found, load (+5 more)

### Community 129 - "test_whatsapp_config.py"
Cohesion: 0.31
Nodes (5): env(), test_any_missing_value_keeps_it_off(), test_off_by_default(), test_on_when_fully_configured(), test_the_flag_must_be_truthy()

### Community 130 - "test_navigation.py"
Cohesion: 0.23
Nodes (4): _message(), TestJuzCommand, TestPageCommand, TestSajdaCommand

### Community 131 - "test_media_cache_keys.py"
Cohesion: 0.18
Nodes (8): _bot(), _next_id(), send_audio(), send_photo(), no_cdn(), _source(), test_a_miss_caches_under_the_key_and_a_hit_replays_it(), test_a_rejected_cached_id_is_rebuilt_and_recached()

### Community 132 - "Mini App Plan: Separate quranayatminiapp Nextjs"
Cohesion: 0.12
Nodes (15): Inline query answering (all four representations, ranges), Navigation model ((surah, ayah, type) per chat_id), Page audio with stitched fallback, Page image stitching (lib/page_image.py), Repeat (memorization), Structural divisions (page / juz / sajda from quran-data.xml), Verse card (inline keyboard, edit in place), Uthmani text in Amiri Quran / KFGQPC font (+7 more)

### Community 136 - "features/check.py"
Cohesion: 0.29
Nodes (3): _answer_data(), check(), _options_keyboard()

### Community 137 - "GroupStore"
Cohesion: 0.10
Nodes (4): GroupConfig, GroupMemberLink, GroupPlanRow, GroupStore

### Community 138 - "main.py"
Cohesion: 0.10
Nodes (3): privacy(), setup_logging(), test_http_client_request_urls_are_never_logged()

### Community 139 - "parse_ayah_range"
Cohesion: 0.23
Nodes (3): parse_ayah_range(), TestCommandArguments, TestParseAyahRange

### Community 140 - "MINI_APP_PLAN.md"
Cohesion: 0.13
Nodes (13): Central callback prefix allocation (hifz.PREFIXES), Future roadmap and prioritized backlog, The hifz platform (memorization companion), Streak day ticks on completed session, Bot ↔ Mini App integration (menu button, startapp, /app), Identity table (platform, external_id → user_id), Normalized Incoming event, Neutral message model rendering (HTML / WhatsApp markup) (+5 more)

### Community 141 - "ScheduledSend"
Cohesion: 0.12
Nodes (4): enqueue(), idempotency_key(), schedule_daily(), ScheduledSend

### Community 143 - "test_export_web_content.py"
Cohesion: 0.21
Nodes (7): _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah(), test_meta_surahs_and_sajdas(), test_tafsir_has_every_ayah()

### Community 144 - "t"
Cohesion: 0.09
Nodes (19): _ref_from_draft(), _ref_to_draft(), _send_drill(), _translation_text(), _cancel_row(), _custom_days_keyboard(), _days_keyboard(), _drill_keyboard() (+11 more)

### Community 145 - "locales/__init__.py"
Cohesion: 0.05
Nodes (20): _lang(), LanguageOut, languages(), LanguagesOut, Reciter, reciters(), RecitersOut, nav_labels() (+12 more)

### Community 153 - "offset_keyboard"
Cohesion: 0.35
Nodes (7): offset_keyboard(), _grid(), test_a_label_prefix_changes_only_the_label(), test_cancel_data_adds_a_localized_cancel_row(), test_every_offset_is_offered_in_order_under_the_callers_prefix(), test_no_cancel_row_unless_asked(), test_rows_are_columns_wide()

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 155 - "test_channels_whatsapp.py"
Cohesion: 0.14
Nodes (7): cache(), channel(), taps(), TestChoices, TestNumberedMenuLifetime, TestText, TestTransport

### Community 159 - "MINI_APP_PLAN.md"
Cohesion: 0.18
Nodes (12): Pure plan builder (build_plan), /api/v1 REST surface, initData HMAC validation → short-lived JWT, OpenAPI → TypeScript client pipeline, Recall check integrity (signed question_token), Mini App risks, Other platforms shortlist (Messenger, Viber, Discord, PWA, Signal), Multi-platform phased breakdown (Phases 0-6) (+4 more)

### Community 161 - "fetch_and_stitch"
Cohesion: 0.15
Nodes (8): stitch(), deliver_page(), stitch(), page_image_url(), fetch_and_stitch(), _fit_for_telegram(), _semaphore(), stitch_images()

### Community 162 - "Blue Green Ci: postgres"
Cohesion: 0.22
Nodes (9): POSTGRES_DB, POSTGRES_HOST_AUTH_METHOD, POSTGRES_USER, env, image, options, ports, postgres (+1 more)

### Community 163 - "Blue Green Ci: test"
Cohesion: 0.22
Nodes (9): TEST_DATABASE_URL, test, python-version, fail-fast, matrix, env, name, runs-on (+1 more)

### Community 164 - "Blue Green Ci: preflight"
Cohesion: 0.22
Nodes (9): preflight, active, deploy_enabled, target, if, name, needs, outputs (+1 more)

### Community 170 - "button_action"
Cohesion: 0.07
Nodes (10): command_lines(), keyboard_rows(), missing_keys(), welcome_text(), TestSevenTheCommandsExist, _placeholders(), TestCatalogue, TestGroupLocaleExemption (+2 more)

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 172 - "BismillahBot — Multilingual Support Plan"
Cohesion: 0.12
Nodes (16): 11. Memory & performance (free-tier reality), 12. Testing, 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 2. Current-state audit (what is hardcoded English), 4. User language preference, 5. Content: multi-translation loading (memory-aware) (+8 more)

### Community 175 - "test_keyboard_snapshots.py"
Cohesion: 0.23
Nodes (5): _as_dict(), _keyboards(), _render(), _search_markup(), test_keyboards_match_their_snapshots()

### Community 178 - "BismillahBot README"
Cohesion: 0.10
Nodes (23): Four ayah representations (english, tafsir, arabic, audio), Known limitations / tech debt, Issues fixed in the refactor (12 bugs), Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), Quran.from_file(path) refactor, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+15 more)

### Community 179 - "Translation editions table (48 codes)"
Cohesion: 0.33
Nodes (5): Translation Attributions, alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes)

### Community 181 - "ayah_for"
Cohesion: 0.29
Nodes (3): ayah_for(), test_nothing_repeats_within_one_cycle(), test_same_date_same_ayah()

### Community 182 - "Blue Green Ci: deploygreen"
Cohesion: 0.33
Nodes (6): environment, if, name, needs, runs-on, deploy-green

### Community 183 - "Blue Green Ci: promote"
Cohesion: 0.33
Nodes (6): promote, environment, if, name, needs, runs-on

### Community 188 - ".get_surah_length"
Cohesion: 0.11
Nodes (8): _at_offset(), _span_length(), ayah_count(), plan_target(), TestAyahCount, sweep_refs(), test_short_surahs_still_get_four_distinct_options(), test_the_last_ayah_of_every_surah_produces_a_question()

### Community 197 - ".wa_user"
Cohesion: 0.36
Nodes (4): apps(), Apps, _code(), TestLinking

### Community 199 - "json"
Cohesion: 0.16
Nodes (11): build(), main_(), _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl(), _as_dict(), _ctx(), _Settings (+3 more)

### Community 200 - "pages.py"
Cohesion: 0.07
Nodes (29): command, Routing rules (in `serve`), 5. API surface (`/api/v1`), Phase 2 — WhatsApp MVP (reader + daily ayat), 7. The keyboard & command localization challenge, Telegram command menu, _is_telegram_id(), link() (+21 more)

### Community 206 - "test_hifz_seam.py"
Cohesion: 0.20
Nodes (3): _isolate_registries(), _Settings, TestSchemaApplication

### Community 207 - "WhatsAppChannel"
Cohesion: 0.11
Nodes (5): for_platform(), _clip(), WhatsAppChannel, TestForPlatform, TestTheRest

### Community 210 - "export"
Cohesion: 0.18
Nodes (7): build_meta(), export(), main(), _spans(), split_basmalah(), _write(), parse_quran_tafsir()

### Community 213 - "SurahProgress"
Cohesion: 0.33
Nodes (3): SurahProgress, load_summary(), TestLoadSummary

### Community 269 - "get_store"
Cohesion: 0.15
Nodes (6): get_store(), _lock(), TestFourProgress, _added_update(), TestAdded, TestDailyPost

### Community 270 - "features/daily.py"
Cohesion: 0.14
Nodes (16): ctx(), _ask_time(), daily(), _enable(), _hhmm(), _offset(), on_tap(), _parse_time() (+8 more)

### Community 275 - "milestone_for"
Cohesion: 0.33
Nodes (3): milestone_for(), _milestone_key(), TestMilestones

### Community 276 - "api/plans.py"
Cohesion: 0.08
Nodes (30): require_user(), _unauthorized(), answer(), AnswerIn, AnswerOut, make_token(), question(), QuestionOut (+22 more)

### Community 318 - "channels/whatsapp.py"
Cohesion: 0.09
Nodes (10): _now(), opt_out(), Caps, Incoming, _error(), WhatsAppError, WindowClosed, no_cdn() (+2 more)

## Knowledge Gaps
- **51 isolated node(s):** `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres`, `Capacity results 5-1000 concurrent (no errors, 70-91 MB)`, `Verse card (inline keyboard, edit in place)` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1691 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **145 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `get_store` to `features/profile.py`, `test_hifz_leaderboard.py`, `_ctx`, `services/plans.py`, `_tap`, `build_grid`, `lifespan.py`, `UserSettings`, `Context`, `RedisSingleton`, `api/plans.py`, `Hifz Progress Cmd Tests`, `Hifz Streak Tests`, `Acceptance Tests`, `surah_progress`, `WhatsApp`, `Streaks`, `Services`, `dispatch.py`, `Dispatch`, `api/progress.py`, `channels/whatsapp.py`, `store/__init__.py`, `TestSummarize`, `.wa_user`, `json`, `session.py`, `Quran`, `tick.py`, `weekly_board`, `SurahProgress`, `test_hifz_progress.py`, `dispatch.py`, `_hifz`, `handle_message`, `stats.py`, `store/__init__.py`, `build_question`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_plan` be split into smaller, more focused modules?**
  _Cohesion score 0.05600722673893405 - nodes in this community are weakly interconnected._
- **Why does `Quran` connect `Quran` to `build_plan`, `Phase 1 — Take `main.py` apart (pure moves) — *done*`, `test_navigation.py`, `features/profile.py`, `range_audio`, `features/check.py`, `.page_range`, `services/plans.py`, `lifespan.py`, `test_export_web_content.py`, `t`, `locales/__init__.py`, `Refs`, `api/plans.py`, `Hifz Progress Cmd Tests`, `features/progress.py`, `fetch_and_stitch`, `.get`, `fixture`, `to_markup`, `services/check.py`, `surah_progress`, `quran_page_progress`, `api/progress.py`, `.get_surah_length`, `juz_progress`, `TestSummarize`, `pages.py`, `BismillahBot — Business Logic`, `juz_ref`, `export`, `Ref`, `recall_check.py`, `quran_progress`, `infra/__init__.py`, `.get_next_ayah`, `build_question`, `.exists`, `plan_builder.py`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 40 inferred relationships involving `Ctx` (e.g. with `3. Architecture` and `4.1 Overlap with `MULTI_PLATFORM_PLAN.md``) actually correct?**
  _`Ctx` has 40 INFERRED edges - model-reasoned connections that need verification._
- **Should `link_token.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10588235294117647 - nodes in this community are weakly interconnected._