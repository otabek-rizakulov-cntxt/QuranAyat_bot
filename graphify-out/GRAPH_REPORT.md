# Graph Report - QuranAyat_bot  (2026-11-02)

## Corpus Check
- 270 files · ~258,299 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 5011 nodes · 11539 edges · 289 communities (152 shown, 137 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1019 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fc00db3e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- advancing
- .page_range
- surah_progress
- build_plan
- Wizard
- _plan_setup.py
- features/profile.py
- next_due_utc
- to_whatsapp
- _ctx
- _ctx
- group.py
- Store
- render_streak_graph
- get_settings
- UserSettings
- Context
- test_store_selection.py
- Refs
- RedisSingleton
- lifespan.py
- WhatsAppChannel
- IdentityStore
- Hifz Progress Cmd Tests
- _save_group_plan
- Refactor — Implementation Plan
- TelegramChannel
- Hifz Streak Tests
- Hifz Platform
- Acceptance Tests
- bot/media.py
- Docker Compose.stress
- _png
- test_recall_check.py
- .get
- _options_keyboard
- _plan_preview.py
- Recitation Checker Investigation
- hifz_progress.py
- test_whatsapp_webhook.py
- to_markup
- Session
- PostgresPlanStore
- quran_page_progress
- test_hifz_cross_platform.py
- Streaks
- Load Test
- Multilingual Plan
- Text
- Schema
- Services
- auth.py
- Dispatch
- PlanDaySpec
- PostgresProfileStore
- Inline Reciter Search Tests
- test_hifz_check.py
- deliver_push
- os
- PostgresScheduleStore
- test_hifz_keyboard_snapshots.py
- Dispatch Order Tests
- .send_text
- Mini App Plan
- ask
- juz_progress
- summarize
- Ctx
- PostgresIdentityStore
- api/catalog.py
- postgres.py
- Hifz Seam Tests
- api/plans.py
- router.py
- InMemoryIdentityStore
- tick.py
- Profiles: InMemoryProfileStore
- Bundle Translations
- Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd
- BismillahBot — Business Logic
- Streaks: compute_streak
- Groups: PostgresGroupStore
- SessionStore
- Scheduler Tests
- sys
- InMemoryGroupStore
- Quran
- auth.py
- Store Contract Tests
- Multi Platform Plan: MultiPlatform Implementation Plan
- dispatch.py
- _hifz
- ProfileRow
- handle_message
- Hifz Seam Tests: TestRegistration
- test_hifz_progress.py
- Scheduler Tests: TestTransientFailuresAreRetried
- Store Contract Tests: TestPlans
- GraphClient
- TestStateStore
- _at
- week_bounds
- recall_check.py
- milestone_for
- test_store_contract.py
- test_daily_feature.py
- test_hifz_streak.py
- button_rows
- stats.py
- send_page
- TestSchedule
- store/__init__.py
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- .get_next_ayah
- parse_ayah_range
- ._load_performers
- test_navigation.py
- pick_ayahs
- streak.py
- .exists
- IdentityRow
- TestHelpers
- Blue Green Ci: jobs
- Blue Green Ci: with
- build_grid
- _message
- _focus_surah
- Mini App Plan: Separate quranayatminiapp Nextjs
- InMemoryScheduleStore
- Channel
- range_audio
- test_export_web_content.py
- GroupStore
- Store Contract Tests: TestLeaderboard
- test_hifz_intervals.py
- MINI_APP_PLAN.md
- re
- TestRestartDeliversExactlyOnce
- t
- locales/__init__.py
- normalize_lang
- juz_ref
- score
- Hifz Seam Tests: test_hifz_seampy
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- test_channels_telegram.py
- PostgresHifzStore
- Blue Green Ci: env
- test_channels_whatsapp.py
- TestProfiles
- graphify-autopush.sh
- .plan
- MINI_APP_PLAN.md
- Settings Tests
- Store Contract Tests: TestSessions
- Blue Green Ci: postgres
- Blue Green Ci: test
- Blue Green Ci: preflight
- ProfileStore
- Hifz Seam Tests: TestPrefixNamespace
- Hifz Seam Tests: TestDispatchCallback
- TestPickerFlow
- button_action
- Blue Green Ci: smokegreen
- TranslationRegistry
- File Facade: search_performers
- test_keyboard_snapshots.py
- TestRunScheduler
- BismillahBot README
- load_summary
- PostgresSessionStore
- Blue Green Ci: deploygreen
- Blue Green Ci: promote
- Choices
- TestHifzIntervalEdges
- Hifz Seam Tests: test_longest_prefix_wins
- .get_surah_length
- TestIdentity
- Claude
- json
- send_repeated_audio
- Hifz Seam Tests: TestDispatchCommand
- _Ratio
- offset_options
- Hifz Group Tests: TestRegistration
- answer_inline_query
- fetch_and_stitch
- test_draft_is_written_with_that_ttl
- quran_progress
- next_scheduled_date
- WhatsAppChannel
- PostgresDailyStore
- MemoryStore
- test_media_cache_keys.py
- GroupPlanDayRow
- .is_cancel
- TestDailyPost
- features/daily.py
- PageProgress
- infra/catalog.py
- auto_pace
- TestSettings
- GroupMemberLink
- bot/whatsapp.py
- Graph
- level_for
- Graph
- parametrize

## God Nodes (most connected - your core abstractions)
1. `get_store()` - 168 edges
2. `Ctx` - 129 edges
3. `t()` - 120 edges
4. `Quran` - 118 edges
5. `handle_update()` - 93 edges
6. `UserSettings` - 78 edges
7. `build_plan()` - 72 edges
8. `parse_reference()` - 59 edges
9. `TelegramChannel` - 58 edges
10. `Ref` - 57 edges

## Surprising Connections (you probably didn't know these)
- `5. Caching strategy` --references--> `MemoryStore`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/infra/redis_client.py
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `Prioritized backlog` --references--> `parse_ayah()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/domain/parsing.py
- `Translation-only catalogue entries` --references--> `normalize_lang()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/locales/languages.py
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

## Communities (289 total, 137 thin omitted)

### Community 0 - "advancing"
Cohesion: 0.09
Nodes (7): advancing(), assert_covers_target_once(), assert_well_formed(), spans(), TestAlMulkAcceptance, TestCrossSurahTargets, TestSmallAndAwkwardTargets

### Community 1 - ".page_range"
Cohesion: 0.13
Nodes (4): source(), stitch(), test_page_boundaries_match_the_bot(), TestDivisionsTileTheQuran

### Community 2 - "surah_progress"
Cohesion: 0.14
Nodes (4): started_surahs(), surah_progress(), TestSpecAcceptance, TestSurahProgress

### Community 3 - "build_plan"
Cohesion: 0.14
Nodes (5): build_plan(), surah_ref(), TestConsolidationDays, TestDayOfWeekFiltering, TestPurity

### Community 4 - "Wizard"
Cohesion: 0.08
Nodes (7): ctx(), Wizard, TestAccumulation, TestCorruptState, TestLifecycle, TestOneDraftPerUser, wiz()

### Community 5 - "_plan_setup.py"
Cohesion: 0.07
Nodes (38): _consented(), memorize(), on_tap(), plan_step(), _expired(), _ref_from_draft(), _ref_to_draft(), _start_drill() (+30 more)

### Community 6 - "features/profile.py"
Cohesion: 0.07
Nodes (21): _cancel_keyboard(), _join_board(), name_step(), offset_from_callback(), on_profile_tap(), _plan_line(), profile_command(), profile_view() (+13 more)

### Community 7 - "next_due_utc"
Cohesion: 0.07
Nodes (10): format_offset(), local_time(), next_due_utc(), parse_offset(), TestFormatOffset, TestLocalDate, TestNextDueUtc, TestParseOffset (+2 more)

### Community 8 - "to_whatsapp"
Cohesion: 0.06
Nodes (13): _Converter, _render(), split(), to_whatsapp(), _wrap(), env(), test_any_missing_value_keeps_it_off(), test_off_by_default() (+5 more)

### Community 9 - "_ctx"
Cohesion: 0.09
Nodes (13): weekly_board(), _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join(), _Message, _sent() (+5 more)

### Community 10 - "_ctx"
Cohesion: 0.09
Nodes (16): _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _Message, _profile_row(), _sent() (+8 more)

### Community 11 - "group.py"
Cohesion: 0.07
Nodes (26): _enqueue_next_board(), _enqueue_next_group(), group_board_entries(), post_board(), push_board(), push_group_day(), _as_utc(), local_date() (+18 more)

### Community 12 - "Store"
Cohesion: 0.09
Nodes (11): _CallbackQuery, _ctx(), _Message, _run_wizard(), _Settings, _tap(), TestDrill, TestEnqueueChain (+3 more)

### Community 13 - "render_streak_graph"
Cohesion: 0.14
Nodes (7): render(), draw_contribution_graph(), render_streak_graph(), _semaphore(), open_png(), TestRendering, TestRenderStreakGraph

### Community 14 - "get_settings"
Cohesion: 0.12
Nodes (10): Phase 5 — Fix the layering — *done*, app_button(), app_row(), app_url(), set_menu_button(), _flag(), get_settings(), Settings (+2 more)

### Community 15 - "UserSettings"
Cohesion: 0.10
Nodes (11): UserSettingsRow, _legacy_lang_key(), SettingsRow, UserSettings, _seed_legacy_lang(), TestDefaults, TestIndependence, TestInlineCaller (+3 more)

### Community 16 - "Context"
Cohesion: 0.12
Nodes (19): get_store(), _lock(), _added_update(), _bot(), _ctx(), _isolate_registries(), _member(), _run_setup_to_plan() (+11 more)

### Community 17 - "test_store_selection.py"
Cohesion: 0.06
Nodes (15): health(), store_backend(), database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries(), fresh_redis() (+7 more)

### Community 18 - "Refs"
Cohesion: 0.08
Nodes (9): _clean(), parse_range(), parse_reference(), TestSurahSpans, TestAcrossSurahs, TestFormatting, TestRejection, TestWholeSurah (+1 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.09
Nodes (11): 6. Issues fixed in this refactor, forget(), _key(), pick(), remember(), get(), _key(), save() (+3 more)

### Community 20 - "lifespan.py"
Cohesion: 0.04
Nodes (31): 2. Current-state audit (what is hardcoded English), Phase 1 — Take `main.py` apart (pure moves) — *done*, _stress_reset(), _stress_stats(), create_app(), build_data(), _commands_for(), initialize() (+23 more)

### Community 21 - "WhatsAppChannel"
Cohesion: 0.15
Nodes (4): _bytes_and_name(), _resolve(), _split_choices(), TestMedia

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "_save_group_plan"
Cohesion: 0.09
Nodes (18): _begin_setup(), bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), handle_start_payload(), _is_group_admin() (+10 more)

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.07
Nodes (31): graphify knowledge graph (graphify-out/), CLAUDE.md graphify lookup rules, 10. Found along the way (out of scope — behaviour changes), 2. Goals and non-goals, 3. Principles applied, 6. Ordering, risk, size, 7. Safety net, 8. Expected result (+23 more)

### Community 26 - "TelegramChannel"
Cohesion: 0.10
Nodes (6): TelegramChannel, TestAnswerAndTyping, TestEditChoices, TestEditText, TestMedia, TestSendText

### Community 27 - "Hifz Streak Tests"
Cohesion: 0.18
Nodes (6): _caption(), _earn(), _streak(), TestGraphCache, TestMilestones, TestStreakCard

### Community 28 - "Hifz Platform"
Cohesion: 0.07
Nodes (28): Hifz Platform - Plan & Progress, Phase 1 acceptance criteria (tests/test_acceptance.py), Hifz change log, claim_due claimed_at clock bug, Hifz data model (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send, group_*), Phase 2 group cluster (J1-J6, forum topics), Workstream I: i18n & commands for 48 locales, Workstream C: interval merge-on-insert + derived percentages (+20 more)

### Community 29 - "Acceptance Tests"
Cohesion: 0.09
Nodes (14): _CallbackQuery, _cmd(), _ctx(), _Message, _run_wizard(), _save_plan(), _Settings, _tap() (+6 more)

### Community 30 - "bot/media.py"
Cohesion: 0.05
Nodes (24): session(), _send_drill(), answer_inline_query(), inline_audio_result(), inline_photo_results(), combined_audio_key(), deliver_combined_audio(), deliver_quran() (+16 more)

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 33 - "test_recall_check.py"
Cohesion: 0.03
Nodes (29): _nfc(), test_a_different_date_gives_a_different_question(), test_both_question_modes_show_up_in_the_sweep(), test_correct_option_is_never_a_length_outlier(), test_correct_option_is_never_the_extreme_by_a_wide_ratio(), test_correct_option_really_follows_the_prompt(), test_dates_and_iso_strings_are_interchangeable(), test_every_option_carries_the_same_word_count() (+21 more)

### Community 34 - ".get"
Cohesion: 0.08
Nodes (5): TestCorpusIntegrity, TestAvailable, TestCaching, TestFallback, TestTransliteration

### Community 36 - "_plan_preview.py"
Cohesion: 0.13
Nodes (6): _portion_label(), _preview_text(), Portion, match_portion(), portion_for(), TestPortionShape

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.07
Nodes (29): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards (+21 more)

### Community 38 - "hifz_progress.py"
Cohesion: 0.19
Nodes (3): format_percent(), round_percent(), TestRounding

### Community 39 - "test_whatsapp_webhook.py"
Cohesion: 0.08
Nodes (17): signature(), _isolate_registries(), tg_bot(), _isolate_registries(), _isolate_registries(), app_on(), data(), client() (+9 more)

### Community 40 - "to_markup"
Cohesion: 0.07
Nodes (16): page_keyboard(), reciter_keyboard(), reciter_label(), reciter_page_count(), reciter_search_keyboard(), verse_keyboard(), mode_button(), to_button() (+8 more)

### Community 41 - "Session"
Cohesion: 0.13
Nodes (21): init_data_max_age(), auth_telegram(), AuthOut, me(), _me(), MeOut, patch_profile(), patch_settings() (+13 more)

### Community 42 - "PostgresPlanStore"
Cohesion: 0.05
Nodes (5): InMemoryPlanStore, PlanDayRow, PlanRow, PlanStore, PostgresPlanStore

### Community 43 - "quran_page_progress"
Cohesion: 0.11
Nodes (3): juz_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 44 - "test_hifz_cross_platform.py"
Cohesion: 0.15
Nodes (7): data(), no_cdn(), Telegram, test_a_week_on_whatsapp_matches_a_week_on_telegram(), test_without_consent_whatsapp_gets_no_reminders(), _week(), WhatsApp

### Community 45 - "Streaks"
Cohesion: 0.13
Nodes (4): record_session(), TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 46 - "Load Test"
Cohesion: 0.14
Nodes (13): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+5 more)

### Community 47 - "Multilingual Plan"
Cohesion: 0.14
Nodes (13): Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), Quran.from_file(path) refactor, setMyCommands per language, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+5 more)

### Community 48 - "Text"
Cohesion: 0.22
Nodes (6): _inline_query(), _of_type(), _results(), TestInlineArabicImage, TestRangeAudio, TestRangeText

### Community 49 - "Schema"
Cohesion: 0.11
Nodes (27): daily_ayah_sub, group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval (+19 more)

### Community 50 - "Services"
Cohesion: 0.15
Nodes (19): _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today(), test_me_carries_plan_and_streak() (+11 more)

### Community 51 - "auth.py"
Cohesion: 0.07
Nodes (28): jwt_secret(), require_user(), answer(), AnswerIn, AnswerOut, make_token(), question(), QuestionOut (+20 more)

### Community 52 - "Dispatch"
Cohesion: 0.16
Nodes (18): _callback(), data(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index(), test_inline_query_valid_ayah_returns_all_four_views() (+10 more)

### Community 55 - "Inline Reciter Search Tests"
Cohesion: 0.12
Nodes (22): handle_update(), _audio_result(), data(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter(), test_ayah_audio_dropped_without_public_base_url() (+14 more)

### Community 56 - "test_hifz_check.py"
Cohesion: 0.06
Nodes (22): _parse_answer(), percentile_band(), refresh_streaks(), streak_summary(), user_today(), _answer_data(), _AnyDay, _ask() (+14 more)

### Community 57 - "deliver_push"
Cohesion: 0.23
Nodes (9): deliver_push(), _log(), ctx_for(), say_hi(), test_every_push_is_logged_for_cost_tracking(), TestConsent, TestTelegram, TestWhatsApp (+1 more)

### Community 58 - "os"
Cohesion: 0.19
Nodes (11): _absolute_imports(), _sources(), test_known_violations_still_exist(), test_no_new_violations(), test_the_scan_sees_every_package(), _violations(), _imported_modules(), _py_files() (+3 more)

### Community 60 - "test_hifz_keyboard_snapshots.py"
Cohesion: 0.26
Nodes (6): _as_dict(), _ctx(), _Settings, _static_cases(), test_hifz_keyboards_match_their_snapshots(), _view_cases()

### Community 61 - "Dispatch Order Tests"
Cohesion: 0.18
Nodes (17): _callback(), data(), fake_bot(), _message(), probe(), _sent_a_verse(), test_a_command_beats_a_pending_reciter_search(), test_a_command_escapes_a_wizard_without_ending_it() (+9 more)

### Community 62 - ".send_text"
Cohesion: 0.16
Nodes (5): taps(), TestChoices, TestNumberedMenuLifetime, TestText, TestTransport

### Community 63 - "Mini App Plan"
Cohesion: 0.08
Nodes (25): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 4.1 Flow, 4.2 Rules (+17 more)

### Community 65 - "ask"
Cohesion: 0.17
Nodes (6): _basmala_prefix(), _clean(), corpus(), pick_ayah(), preload_corpus(), ask()

### Community 66 - "juz_progress"
Cohesion: 0.16
Nodes (5): juz_progress(), JuzProgress, _spans(), started_juzs(), TestJuzProgress

### Community 67 - "summarize"
Cohesion: 0.10
Nodes (4): Progress, ProgressSummary, summarize(), TestSummarize

### Community 68 - "Ctx"
Cohesion: 0.08
Nodes (23): 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, Ctx, _ask(), check(), on_check(), _question_text(), _score() (+15 more)

### Community 70 - "api/catalog.py"
Cohesion: 0.20
Nodes (10): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, put_position(), ReaderPosition, Reciter (+2 more)

### Community 71 - "postgres.py"
Cohesion: 0.25
Nodes (4): get_pool(), _lock(), reset_for_tests(), reset_for_tests()

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 73 - "api/plans.py"
Cohesion: 0.10
Nodes (25): ref_out(), RefOut, active(), _build(), complete(), create(), DrillOut, lifecycle() (+17 more)

### Community 74 - "router.py"
Cohesion: 0.09
Nodes (21): Phase 3 — One router for everything — *done*, _on_callback(), _on_text(), callback(), decorate(), _cancel(), command(), decorate() (+13 more)

### Community 76 - "tick.py"
Cohesion: 0.04
Nodes (24): enqueue(), idempotency_key(), schedule_daily(), _send_plain_message(), register_send_handler(), registered_kinds(), _same_origin(), send_handler() (+16 more)

### Community 78 - "Bundle Translations"
Cohesion: 0.22
Nodes (7): bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.12
Nodes (18): Audio catalog kinds, Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES), Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points), Error taxonomy L1-L5 (word, harakah, tajwid, riwayah mismatch, waqf), Evaluation plan (false-alarm gate < 2% per ayah) (+10 more)

### Community 80 - "BismillahBot — Business Logic"
Cohesion: 0.12
Nodes (15): 1. Overview, 2. Architecture, 3. Request lifecycle, 5. Caching strategy, 7. Known limitations / tech debt, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic (+7 more)

### Community 81 - "Streaks: compute_streak"
Cohesion: 0.24
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 83 - "SessionStore"
Cohesion: 0.10
Nodes (3): InMemorySessionStore, SessionRow, SessionStore

### Community 84 - "Scheduler Tests"
Cohesion: 0.17
Nodes (4): _claimed_at(), _record(), TestCatchUp, TestTick

### Community 85 - "sys"
Cohesion: 0.12
Nodes (9): _clean_state_store(), build_meta(), export(), main(), _spans(), split_basmalah(), _write(), setup_logging() (+1 more)

### Community 87 - "Quran"
Cohesion: 0.05
Nodes (26): surah_name(), _know_by_heart(), _translation_text(), progress_view(), _surah_line(), _clip(), _covered(), _intersect() (+18 more)

### Community 89 - "auth.py"
Cohesion: 0.08
Nodes (37): _b64url(), _b64url_decode(), decode_token(), _init_data_secret(), InvalidInitData, InvalidToken, issue_token(), _sign() (+29 more)

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.08
Nodes (24): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+16 more)

### Community 92 - "dispatch.py"
Cohesion: 0.09
Nodes (14): _app_command(), test_app_command(), test_app_command_without_url(), test_cards_and_drill_link_to_their_screens(), test_inline_messages_never_get_a_web_app_button(), test_off_by_default(), _web_apps(), data() (+6 more)

### Community 93 - "_hifz"
Cohesion: 0.11
Nodes (4): _hifz(), _spans(), TestAddInterval, TestRemoveRange

### Community 95 - "handle_message"
Cohesion: 0.19
Nodes (9): handle_message(), bodies(), fixture_message(), known_user(), tap(), TestBoundaries, TestFirstContact, TestReader (+1 more)

### Community 100 - "GraphClient"
Cohesion: 0.10
Nodes (3): GraphClient, graph(), Graph

### Community 101 - "TestStateStore"
Cohesion: 0.05
Nodes (13): _search_reciters(), page_audio_url(), page_image_url(), File, save(), expect(), _key(), take() (+5 more)

### Community 103 - "week_bounds"
Cohesion: 0.25
Nodes (3): user_week_window(), week_window(), TestWeekWindow

### Community 104 - "recall_check.py"
Cohesion: 0.08
Nodes (22): _assemble(), _ayah_text(), build_question(), _continuation_question(), _date_key(), display_length(), _distinct(), _everything() (+14 more)

### Community 105 - "milestone_for"
Cohesion: 0.33
Nodes (3): milestone_for(), _milestone_key(), TestMilestones

### Community 107 - "test_daily_feature.py"
Cohesion: 0.19
Nodes (11): _buttons(), _due_rows(), _message(), _send_ctx(), _tap(), TestTelegramDelivery, TestTelegramSetup, TestWhatsApp (+3 more)

### Community 108 - "test_hifz_streak.py"
Cohesion: 0.22
Nodes (6): _ctx(), _isolate_registries(), _photo_message(), _Settings, TestCallback, TestWhatTicksADay

### Community 109 - "button_rows"
Cohesion: 0.21
Nodes (6): button_rows(), sajda_keyboard(), test_a_non_positive_width_is_one_per_row(), test_an_exact_fit_has_no_empty_trailing_row(), test_nothing_in_nothing_out(), test_packs_in_order_with_a_short_last_row()

### Community 110 - "stats.py"
Cohesion: 0.18
Nodes (10): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut (+2 more)

### Community 111 - "send_page"
Cohesion: 0.29
Nodes (7): send_page(), _buffer(), _stub_stitch(), stub(), TestPageCard, capture(), counting()

### Community 113 - "store/__init__.py"
Cohesion: 0.05
Nodes (17): Milestone, offset_of(), StreakCounts, DailyStore, DailySubRow, InMemoryDailyStore, HifzStore, InMemoryHifzStore (+9 more)

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
Cohesion: 0.20
Nodes (5): 4. Navigation model, Page images and page audio, Structural divisions (page / juz / sajda), Translation-only catalogue entries, TestNavigation

### Community 119 - "parse_ayah_range"
Cohesion: 0.13
Nodes (5): parse_ayah(), parse_ayah_range(), TestCommandArguments, TestParseAyah, TestParseAyahRange

### Community 120 - "._load_performers"
Cohesion: 0.12
Nodes (7): 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 4 — Split infrastructure god-objects — *done*, Phase 6 — Repository hygiene — *done*, send_quran(), TestCatalogKinds, TestCatalogOrder

### Community 121 - "test_navigation.py"
Cohesion: 0.31
Nodes (4): data(), fake_bot(), _no_network(), tg_bot()

### Community 122 - "pick_ayahs"
Cohesion: 0.25
Nodes (4): _at_offset(), pick_ayahs(), _span_length(), _span_tuple()

### Community 123 - "streak.py"
Cohesion: 0.18
Nodes (8): _caption(), _keyboard(), on_streak(), _send_graph(), streak(), cache_key(), StreakSummary, TestCacheKey

### Community 124 - ".exists"
Cohesion: 0.10
Nodes (7): TestEveryParsedRefIsReal, TestExists, TestRandom, TestStructure, TestSurahMeta, test_pick_ayah_handles_a_cross_surah_span(), test_the_whole_quran_is_a_valid_span()

### Community 126 - "TestHelpers"
Cohesion: 0.08
Nodes (7): _covers(), HifzInterval, _merge_span(), _overlaps(), _split_span(), _touches(), TestHelpers

### Community 127 - "Blue Green Ci: jobs"
Cohesion: 0.15
Nodes (13): name, needs, runs-on, jobs, build, lint, rollback, name (+5 more)

### Community 128 - "Blue Green Ci: with"
Cohesion: 0.15
Nodes (13): with, cache, cache-dependency-path, cache-from, cache-to, context, if-no-files-found, load (+5 more)

### Community 129 - "build_grid"
Cohesion: 0.18
Nodes (4): build_grid(), _counts(), Grid, TestGrid

### Community 130 - "_message"
Cohesion: 0.23
Nodes (4): _message(), TestJuzCommand, TestPageCommand, TestSajdaCommand

### Community 131 - "_focus_surah"
Cohesion: 0.33
Nodes (3): _focus_surah(), _recency_key(), _surah_of()

### Community 132 - "Mini App Plan: Separate quranayatminiapp Nextjs"
Cohesion: 0.12
Nodes (15): Inline query answering (all four representations, ranges), Navigation model ((surah, ayah, type) per chat_id), Page audio with stitched fallback, Page image stitching (lib/page_image.py), Repeat (memorization), Structural divisions (page / juz / sajda from quran-data.xml), Verse card (inline keyboard, edit in place), Uthmani text in Amiri Quran / KFGQPC font (+7 more)

### Community 135 - "range_audio"
Cohesion: 0.08
Nodes (9): range_audio(), stitch(), download_combined_audio(), download_stitched_audio(), content(), TestRangeAudioRoute, fake_download(), TestStitching (+1 more)

### Community 136 - "test_export_web_content.py"
Cohesion: 0.21
Nodes (7): _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah(), test_meta_surahs_and_sajdas(), test_tafsir_has_every_ayah()

### Community 137 - "GroupStore"
Cohesion: 0.12
Nodes (3): GroupConfig, GroupPlanRow, GroupStore

### Community 139 - "test_hifz_intervals.py"
Cohesion: 0.23
Nodes (6): _assert_invariant(), _ayahs(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order(), TestEveryRelativePosition

### Community 140 - "MINI_APP_PLAN.md"
Cohesion: 0.13
Nodes (13): Central callback prefix allocation (hifz.PREFIXES), Future roadmap and prioritized backlog, The hifz platform (memorization companion), Streak day ticks on completed session, Bot ↔ Mini App integration (menu button, startapp, /app), Identity table (platform, external_id → user_id), Normalized Incoming event, Neutral message model rendering (HTML / WhatsApp markup) (+5 more)

### Community 141 - "re"
Cohesion: 0.23
Nodes (5): parse_quran_tafsir(), _modules(), test_nothing_builds_telegram_markup_by_hand_outside_those_modules(), test_only_group_code_reads_the_telegram_client(), test_only_telegram_only_modules_import_telegram()

### Community 142 - "TestRestartDeliversExactlyOnce"
Cohesion: 0.14
Nodes (3): InMemoryStore, store(), TestRestartDeliversExactlyOnce

### Community 143 - "t"
Cohesion: 0.05
Nodes (40): command, Routing rules (in `serve`), 5. API surface (`/api/v1`), Phase 2 — WhatsApp MVP (reader + daily ayat), 7. The keyboard & command localization challenge, Telegram command menu, about(), app() (+32 more)

### Community 144 - "locales/__init__.py"
Cohesion: 0.08
Nodes (16): 1. Why, Phase 2 — DRY the duplicated patterns — *done*, _post_portion(), set_translation_language(), set_ui_language(), language_keyboard(), language_picker(), translation_language_keyboard() (+8 more)

### Community 145 - "normalize_lang"
Cohesion: 0.10
Nodes (19): Documentation index (docs/README.md), ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable, lib/utils.File god class, GET / health with store and cache status (503), Silent in-memory store fallback, Phase 4 — Split infrastructure god-objects, Phase 6 — Repository hygiene, Profile settings reset fix (fix/settings-persistence) (+11 more)

### Community 146 - "juz_ref"
Cohesion: 0.16
Nodes (4): juz_ref(), to_day_specs(), TestJuzAndPage, TestStorageShape

### Community 148 - "Hifz Seam Tests: test_hifz_seampy"
Cohesion: 0.18
Nodes (3): _isolate_registries(), _Settings, TestSchemaApplication

### Community 152 - "test_channels_telegram.py"
Cohesion: 0.16
Nodes (5): for_platform(), bot(), cache(), TestChoice, TestForPlatform

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 155 - "test_channels_whatsapp.py"
Cohesion: 0.18
Nodes (4): cache(), channel(), graph(), Graph

### Community 159 - "MINI_APP_PLAN.md"
Cohesion: 0.18
Nodes (12): Pure plan builder (build_plan), /api/v1 REST surface, initData HMAC validation → short-lived JWT, OpenAPI → TypeScript client pipeline, Recall check integrity (signed question_token), Mini App risks, Other platforms shortlist (Messenger, Viber, Discord, PWA, Signal), Multi-platform phased breakdown (Phases 0-6) (+4 more)

### Community 162 - "Blue Green Ci: postgres"
Cohesion: 0.22
Nodes (9): POSTGRES_DB, POSTGRES_HOST_AUTH_METHOD, POSTGRES_USER, env, image, options, ports, postgres (+1 more)

### Community 163 - "Blue Green Ci: test"
Cohesion: 0.22
Nodes (9): TEST_DATABASE_URL, test, python-version, fail-fast, matrix, env, name, runs-on (+1 more)

### Community 164 - "Blue Green Ci: preflight"
Cohesion: 0.22
Nodes (9): preflight, active, deploy_enabled, target, if, name, needs, outputs (+1 more)

### Community 169 - "TestPickerFlow"
Cohesion: 0.16
Nodes (6): _callback(), _message(), _reciter_buttons(), _tab_row(), TestAudioNeverFollowsLanguage, TestPickerFlow

### Community 170 - "button_action"
Cohesion: 0.07
Nodes (12): main(), placeholders(), button_action(), keyboard_rows(), missing_keys(), missing_locales(), _reverse_button_map(), _placeholders() (+4 more)

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 172 - "TranslationRegistry"
Cohesion: 0.09
Nodes (18): 10. File-by-file change list, 11. Memory & performance (free-tier reality), 12. Testing, 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 3. Target architecture, 4. User language preference (+10 more)

### Community 175 - "test_keyboard_snapshots.py"
Cohesion: 0.25
Nodes (5): _as_dict(), _keyboards(), _render(), _search_markup(), test_keyboards_match_their_snapshots()

### Community 178 - "BismillahBot README"
Cohesion: 0.13
Nodes (13): Translation Attributions, alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Four ayah representations (english, tafsir, arabic, audio), Known limitations / tech debt, Issues fixed in the refactor (12 bugs) (+5 more)

### Community 179 - "load_summary"
Cohesion: 0.33
Nodes (3): SurahProgress, load_summary(), TestLoadSummary

### Community 182 - "Blue Green Ci: deploygreen"
Cohesion: 0.33
Nodes (6): environment, if, name, needs, runs-on, deploy-green

### Community 183 - "Blue Green Ci: promote"
Cohesion: 0.33
Nodes (6): promote, environment, if, name, needs, runs-on

### Community 184 - "Choices"
Cohesion: 0.12
Nodes (5): _build(), ignore_not_modified(), _send(), send_cached(), build()

### Community 188 - ".get_surah_length"
Cohesion: 0.13
Nodes (6): ayah_count(), TestAyahCount, sweep_refs(), swept(), test_short_surahs_still_get_four_distinct_options(), test_the_last_ayah_of_every_surah_produces_a_question()

### Community 193 - "json"
Cohesion: 0.18
Nodes (10): export(), languages(), main(), resolved_table(), _write(), build(), main_(), _load() (+2 more)

### Community 194 - "send_repeated_audio"
Cohesion: 0.26
Nodes (3): send_repeated_audio(), _stub_audio(), TestRepeatForMemorization

### Community 197 - "offset_options"
Cohesion: 0.28
Nodes (8): offset_keyboard(), offset_options(), _grid(), test_a_label_prefix_changes_only_the_label(), test_cancel_data_adds_a_localized_cancel_row(), test_every_offset_is_offered_in_order_under_the_callers_prefix(), test_no_cancel_row_unless_asked(), test_rows_are_columns_wide()

### Community 200 - "answer_inline_query"
Cohesion: 0.22
Nodes (3): handle_incoming(), _incoming(), resolve_settings()

### Community 205 - "fetch_and_stitch"
Cohesion: 0.29
Nodes (4): fetch_and_stitch(), _fit_for_telegram(), _semaphore(), stitch_images()

### Community 210 - "next_scheduled_date"
Cohesion: 0.29
Nodes (3): _advance(), next_scheduled_date(), _validated_days()

### Community 213 - "WhatsAppChannel"
Cohesion: 0.14
Nodes (3): _clip(), WhatsAppChannel, TestTheRest

### Community 214 - "PostgresDailyStore"
Cohesion: 0.20
Nodes (3): PostgresDailyStore, PostgresStore, store()

### Community 216 - "MemoryStore"
Cohesion: 0.15
Nodes (5): 11.1 Profile settings reset after a while — `fix/settings-persistence`, 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, DatabaseUnavailable, MemoryStore

### Community 266 - "test_media_cache_keys.py"
Cohesion: 0.11
Nodes (11): send_page_audio(), has_page_audio(), _bot(), _next_id(), send_audio(), send_photo(), no_cdn(), _source() (+3 more)

### Community 270 - "features/daily.py"
Cohesion: 0.06
Nodes (15): push_daily(), _template_text(), push_plan_day(), build_verse_text(), Caps, Incoming, _error(), WhatsAppError (+7 more)

### Community 275 - "infra/catalog.py"
Cohesion: 0.09
Nodes (11): reciter_page_of(), reciter_set_confirmation(), audio_url(), find(), performers(), search(), reciter_catalog(), reciter_group() (+3 more)

### Community 286 - "bot/whatsapp.py"
Cohesion: 0.15
Nodes (7): _allowed_command(), as_command(), lang_hint(), _now(), opt_out(), _tap(), TestKeywords

## Knowledge Gaps
- **51 isolated node(s):** `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres`, `Capacity results 5-1000 concurrent (no errors, 70-91 MB)`, `ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1701 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **137 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `Context` to `surah_progress`, `_ctx`, `_ctx`, `Store`, `render_streak_graph`, `TestRestartDeliversExactlyOnce`, `t`, `UserSettings`, `TestDailyPost`, `RedisSingleton`, `lifespan.py`, `Hifz Progress Cmd Tests`, `Hifz Streak Tests`, `Acceptance Tests`, `bot/whatsapp.py`, `Session`, `test_hifz_cross_platform.py`, `Streaks`, `Services`, `auth.py`, `load_summary`, `Inline Reciter Search Tests`, `test_hifz_check.py`, `test_hifz_keyboard_snapshots.py`, `summarize`, `postgres.py`, `answer_inline_query`, `api/plans.py`, `tick.py`, `PostgresDailyStore`, `MemoryStore`, `dispatch.py`, `_hifz`, `handle_message`, `test_hifz_progress.py`, `TestStateStore`, `test_daily_feature.py`, `stats.py`, `store/__init__.py`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 44 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 44 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `advancing` be split into smaller, more focused modules?**
  _Cohesion score 0.09309309309309309 - nodes in this community are weakly interconnected._
- **Why does `Quran` connect `Quran` to `advancing`, `.page_range`, `surah_progress`, `build_plan`, `_message`, `range_audio`, `test_export_web_content.py`, `group.py`, `re`, `features/daily.py`, `t`, `juz_ref`, `Refs`, `lifespan.py`, `auto_pace`, `Hifz Progress Cmd Tests`, `bot/media.py`, `.get`, `quran_page_progress`, `TranslationRegistry`, `auth.py`, `.get_surah_length`, `ask`, `juz_progress`, `summarize`, `api/catalog.py`, `BismillahBot — Business Logic`, `quran_progress`, `sys`, `recall_check.py`, `store/__init__.py`, `.get_next_ayah`, `pick_ayahs`, `.exists`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Ctx` (e.g. with `3. Architecture` and `4.1 Overlap with `MULTI_PLATFORM_PLAN.md``) actually correct?**
  _`Ctx` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Should `.page_range` be split into smaller, more focused modules?**
  _Cohesion score 0.13043478260869565 - nodes in this community are weakly interconnected._