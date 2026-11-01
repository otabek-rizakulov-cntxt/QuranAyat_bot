# Graph Report - QuranAyat_bot  (2026-11-02)

## Corpus Check
- 246 files · ~241,948 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 4617 nodes · 10625 edges · 255 communities (140 shown, 115 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 978 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `891535cf`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_plan
- .page_range
- summarize
- services/plans.py
- Wizard
- _plan_setup.py
- infra/catalog.py
- next_due_utc
- to_whatsapp
- Leaderboard
- _ctx
- Profile
- Store
- render_streak_graph
- t
- UserSettings
- Context
- Health
- Refs
- RedisSingleton
- typing
- wizard
- IdentityStore
- Hifz Progress Cmd Tests
- Group
- Refactor — Implementation Plan
- TelegramChannel
- Hifz Streak Tests
- Hifz Platform
- Acceptance Tests
- get_settings
- Docker Compose.stress
- test_page_mode.py
- test_recall_check.py
- .get
- services/check.py
- File
- Recitation Checker Investigation
- round_percent
- features/check.py
- to_markup
- Session
- Plans: PlanStore
- Ref
- Choice
- Streaks
- Load Test
- Multilingual Plan
- Text
- Schema
- Services
- api/check.py
- Dispatch
- reciter_keyboard
- api/progress.py
- Inline Reciter Search Tests
- test_hifz_check.py
- PlanDaySpec
- juz_ref
- Hifz
- _hifz
- Dispatch Order Tests
- logging.py
- Mini App Plan
- surah_progress
- InMemoryGroupStore
- InMemoryIdentityStore
- get_store
- Quran
- InMemoryHifzStore
- reset_for_tests
- Hifz Seam Tests
- api/plans.py
- t
- PostgresPlanStore
- tick.py
- Profiles: InMemoryProfileStore
- Bundle Translations
- Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd
- BismillahBot — Business Logic
- Streaks: compute_streak
- Groups: PostgresGroupStore
- InMemorySessionStore
- Scheduler Tests
- Layering Tests
- build_grid
- Portion
- auth.py
- Store Contract Tests
- Multi Platform Plan: MultiPlatform Implementation Plan
- text.py
- TestAddInterval
- Profiles: ProfileRow
- test_channels_telegram.py
- Hifz Seam Tests: TestRegistration
- test_media_cache_keys.py
- Scheduler Tests: TestTransientFailuresAreRetried
- Store Contract Tests: TestPlans
- api/catalog.py
- MemoryStore
- weekly_board
- Refactor — Implementation Plan
- recall_check.py
- ._send_media
- test_store_contract.py
- inline.py
- test_hifz_streak.py
- quran.py
- stats.py
- send_page
- Store Contract Tests: TestSchedule
- store/__init__.py
- Safety net (characterisation tests, staging smoke, blue-green)
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- services/leaderboard.py
- parse_ayah_range
- ._load_performers
- corpus
- test_hifz_intervals.py
- streak.py
- InMemoryScheduleStore
- PostgresProfileStore
- unittest_mock
- Blue Green Ci: jobs
- Blue Green Ci: with
- send_repeated_audio
- test_navigation.py
- _at
- Mini App Plan: Separate quranayatminiapp Nextjs
- ScheduleStore
- Channel
- range_audio
- json
- GroupStore
- Store Contract Tests: TestLeaderboard
- TestProfiles
- Business Logic: The hifz platform memorization
- export
- TestRestartDeliversExactlyOnce
- t
- get_language
- PostgresHifzStore
- PostgresScheduleStore
- Hifz Seam Tests: test_hifz_seampy
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- test_miniapp_links.py
- reciter_set_confirmation
- Blue Green Ci: env
- Translation editions table (48 codes)
- level_for
- graphify-autopush.sh
- Page Mode Tests
- MINI_APP_PLAN.md
- Settings Tests
- Store Contract Tests: TestSessions
- Blue Green Ci: postgres
- Blue Green Ci: test
- Blue Green Ci: preflight
- check_locales.py
- services/streaks.py
- Hifz Seam Tests: TestPrefixNamespace
- Hifz Seam Tests: TestDispatchCallback
- TestPickerFlow
- button_action
- Blue Green Ci: smokegreen
- TranslationRegistry
- parse_quran_tafsir
- File Facade: search_performers
- parse_ayah
- BUSINESS_LOGIC.md
- TestRunScheduler
- BismillahBot README
- 8. Phased task breakdown
- _options_keyboard
- cache_key
- Blue Green Ci: deploygreen
- Blue Green Ci: promote
- TestReaderPosition
- Hifz Seam Tests: test_longest_prefix_wins
- test_scheduler.py
- TestSettings
- GroupPlanDayRow
- Claude
- Hifz Seam Tests: TestDispatchCommand
- Hifz Group Tests: TestRegistration
- bot/media.py
- miniapp.py
- test_export_web_content.py
- reciter.py
- .has_page_audio

## God Nodes (most connected - your core abstractions)
1. `get_store()` - 151 edges
2. `Ctx` - 130 edges
3. `Quran` - 124 edges
4. `t()` - 104 edges
5. `handle_update()` - 95 edges
6. `UserSettings` - 74 edges
7. `build_plan()` - 72 edges
8. `parse_reference()` - 59 edges
9. `File` - 57 edges
10. `TelegramChannel` - 56 edges

## Surprising Connections (you probably didn't know these)
- `5. Caching strategy` --references--> `MemoryStore`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/infra/redis_client.py
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `Phase 3 — Hifz parity` --references--> `build_plan()`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/domain/plan_builder.py
- `Translation-only catalogue entries` --references--> `normalize_lang()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/locales/languages.py
- `Prioritized backlog` --references--> `parse_ayah()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/domain/parsing.py

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

## Communities (255 total, 115 thin omitted)

### Community 0 - "build_plan"
Cohesion: 0.06
Nodes (15): _advance(), auto_pace(), build_plan(), next_scheduled_date(), _validated_days(), surah_ref(), to_day_specs(), spans() (+7 more)

### Community 2 - "summarize"
Cohesion: 0.09
Nodes (6): Progress, ProgressSummary, summarize(), SurahProgress, HifzInterval, TestSummarize

### Community 3 - "services/plans.py"
Cohesion: 0.12
Nodes (14): change_status(), complete_day(), day_position(), DrillResult, due_days(), enqueue_next(), owned_day(), preview() (+6 more)

### Community 4 - "Wizard"
Cohesion: 0.06
Nodes (9): Wizard, test_draft_is_written_with_that_ttl(), TestAccumulation, TestCancel, TestCoexistsWithTheReciterFlow, TestCorruptState, TestLifecycle, TestOneDraftPerUser (+1 more)

### Community 5 - "_plan_setup.py"
Cohesion: 0.12
Nodes (25): memorize(), on_tap(), plan_step(), _expired(), _ref_from_draft(), _ref_to_draft(), _know_by_heart(), _start_drill() (+17 more)

### Community 6 - "infra/catalog.py"
Cohesion: 0.12
Nodes (7): source(), audio_url(), find(), has_page_audio(), image_url(), page_audio_url(), page_image_url()

### Community 7 - "next_due_utc"
Cohesion: 0.07
Nodes (10): format_offset(), local_time(), next_due_utc(), parse_offset(), TestFormatOffset, TestLocalDate, TestNextDueUtc, TestParseOffset (+2 more)

### Community 8 - "to_whatsapp"
Cohesion: 0.07
Nodes (8): _Converter, _render(), split(), to_whatsapp(), _wrap(), TestSplit, TestTags, TestWhatTheBotSends

### Community 9 - "Leaderboard"
Cohesion: 0.12
Nodes (10): _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join(), _Message, _sent(), _Settings (+2 more)

### Community 10 - "_ctx"
Cohesion: 0.08
Nodes (17): _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _isolate_registries(), _Message, _profile_row() (+9 more)

### Community 11 - "Profile"
Cohesion: 0.08
Nodes (25): patch_profile(), _cancel_keyboard(), _join_board(), name_step(), offset_from_callback(), on_profile_tap(), _plan_line(), profile_view() (+17 more)

### Community 12 - "Store"
Cohesion: 0.08
Nodes (12): _CallbackQuery, _ctx(), _isolate_registries(), _Message, _run_wizard(), _Settings, _tap(), TestDrill (+4 more)

### Community 13 - "render_streak_graph"
Cohesion: 0.14
Nodes (7): render(), draw_contribution_graph(), render_streak_graph(), _semaphore(), open_png(), TestRendering, TestRenderStreakGraph

### Community 14 - "t"
Cohesion: 0.10
Nodes (17): 7. The keyboard & command localization challenge, Telegram command menu, _send_drill(), _cancel_row(), _custom_days_keyboard(), _days_keyboard(), _drill_keyboard(), _pace_keyboard() (+9 more)

### Community 15 - "UserSettings"
Cohesion: 0.06
Nodes (21): 4.1 Flow, 4.2 Rules, 4.3 Transport, 4. Authentication, patch_settings(), _unprocessable(), resolve_settings(), UserSettingsRow (+13 more)

### Community 16 - "Context"
Cohesion: 0.14
Nodes (15): _bot(), _ctx(), _isolate_registries(), _member(), _run_setup_to_plan(), _Settings, TestBoard, tap() (+7 more)

### Community 17 - "Health"
Cohesion: 0.06
Nodes (16): health(), cache_backend(), store_backend(), database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries() (+8 more)

### Community 18 - "Refs"
Cohesion: 0.06
Nodes (14): clamp_to_quran(), _clean(), contains(), format_ref(), parse_range(), parse_reference(), TestSurahSpans, TestAcrossSurahs (+6 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.10
Nodes (8): get(), _key(), save(), get(), expect(), _key(), take(), RedisSingleton

### Community 20 - "typing"
Cohesion: 0.06
Nodes (16): create_app(), _commands_for(), initialize(), lifespan(), _set_bot_commands(), _process_update(), telegram_webhook(), webhook_secret() (+8 more)

### Community 21 - "wizard"
Cohesion: 0.15
Nodes (11): 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 4 — Split infrastructure god-objects — *done*, Phase 5 — Fix the layering — *done*, Phase 6 — Repository hygiene — *done*, app_row(), decorate(), decorate() (+3 more)

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "Group"
Cohesion: 0.07
Nodes (30): 5.2 Telegram message (bot), 1. Why, Phase 1 — Take `main.py` apart (pure moves) — *done*, ctx(), bot_username(), _chat_id(), _create_topic(), _days_keyboard() (+22 more)

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.13
Nodes (15): 10. Found along the way (out of scope — behaviour changes), 2. Goals and non-goals, 3. Principles applied, 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, 6. Ordering, risk, size, 7. Safety net, 8. Expected result (+7 more)

### Community 26 - "TelegramChannel"
Cohesion: 0.10
Nodes (6): TelegramChannel, TestAnswerAndTyping, TestEditChoices, TestEditText, TestMedia, TestSendText

### Community 27 - "Hifz Streak Tests"
Cohesion: 0.18
Nodes (6): _caption(), _earn(), _streak(), TestGraphCache, TestMilestones, TestStreakCard

### Community 28 - "Hifz Platform"
Cohesion: 0.09
Nodes (20): Hifz Platform - Plan & Progress, Phase 1 acceptance criteria (tests/test_acceptance.py), Hifz change log, claim_due claimed_at clock bug, Hifz data model (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send, group_*), Phase 2 group cluster (J1-J6, forum topics), Workstream I: i18n & commands for 48 locales, Workstream C: interval merge-on-insert + derived percentages (+12 more)

### Community 29 - "Acceptance Tests"
Cohesion: 0.08
Nodes (15): _CallbackQuery, _cmd(), _ctx(), _isolate_registries(), _Message, _run_wizard(), _save_plan(), _Settings (+7 more)

### Community 30 - "get_settings"
Cohesion: 0.10
Nodes (12): _flag(), get_settings(), Settings, DatabaseUnavailable, get_pool(), _lock(), create_bot(), env() (+4 more)

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 32 - "test_page_mode.py"
Cohesion: 0.24
Nodes (4): data(), fake_bot(), TestStitchedAudioAcrossSurahs, tg_bot()

### Community 33 - "test_recall_check.py"
Cohesion: 0.03
Nodes (28): _nfc(), swept(), test_a_different_date_gives_a_different_question(), test_both_question_modes_show_up_in_the_sweep(), test_correct_option_is_never_a_length_outlier(), test_correct_option_is_never_the_extreme_by_a_wide_ratio(), test_correct_option_really_follows_the_prompt(), test_dates_and_iso_strings_are_interchangeable() (+20 more)

### Community 34 - ".get"
Cohesion: 0.10
Nodes (5): get_default_query_results(), TestCorpusIntegrity, TestAvailable, TestCaching, TestFallback

### Community 35 - "services/check.py"
Cohesion: 0.12
Nodes (8): pick_ayah(), preload_corpus(), RecallQuestion, ask(), default_span(), rebuild(), Score, score()

### Community 36 - "File"
Cohesion: 0.08
Nodes (6): File, save(), TestAudioFilename, TestImageFilename, TestLegacyLanguageKey, TestStateStore

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.07
Nodes (28): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards (+20 more)

### Community 38 - "round_percent"
Cohesion: 0.08
Nodes (5): format_percent(), PageProgress, _Ratio, round_percent(), TestRounding

### Community 39 - "features/check.py"
Cohesion: 0.15
Nodes (8): _ask(), on_check(), _parse_answer(), _question_text(), _score(), _translation_text(), progress_view(), _surah_line()

### Community 40 - "to_markup"
Cohesion: 0.19
Nodes (5): verse_keyboard(), to_markup(), TestToMarkup, _button(), TestVerseKeyboard

### Community 41 - "Session"
Cohesion: 0.14
Nodes (19): init_data_max_age(), jwt_secret(), require_user(), auth_telegram(), AuthOut, me(), _me(), MeOut (+11 more)

### Community 42 - "Plans: PlanStore"
Cohesion: 0.06
Nodes (4): InMemoryPlanStore, PlanDayRow, PlanRow, PlanStore

### Community 43 - "Ref"
Cohesion: 0.05
Nodes (17): _clip(), _covered(), _focus_surah(), _intersect(), juz_page_progress(), juz_progress(), JuzProgress, _page_share() (+9 more)

### Community 44 - "Choice"
Cohesion: 0.15
Nodes (6): page_keyboard(), mode_button(), app_choice_row(), Choice, to_button(), TestPageKeyboard

### Community 45 - "Streaks"
Cohesion: 0.13
Nodes (4): record_session(), TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 46 - "Load Test"
Cohesion: 0.15
Nodes (12): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+4 more)

### Community 47 - "Multilingual Plan"
Cohesion: 0.19
Nodes (12): Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), Quran.from_file(path) refactor, setMyCommands per language, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+4 more)

### Community 48 - "Text"
Cohesion: 0.15
Nodes (11): reference(), data(), fake_bot(), _inline_query(), _of_type(), public_url(), _results(), TestInlineArabicImage (+3 more)

### Community 49 - "Schema"
Cohesion: 0.11
Nodes (26): group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval, hifz_interval_user_surah_idx (+18 more)

### Community 50 - "Services"
Cohesion: 0.15
Nodes (20): client(), _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today() (+12 more)

### Community 51 - "api/check.py"
Cohesion: 0.14
Nodes (12): answer(), AnswerIn, AnswerOut, make_token(), question(), QuestionOut, read_token(), _secret() (+4 more)

### Community 52 - "Dispatch"
Cohesion: 0.13
Nodes (21): handle_update(), _callback(), data(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index() (+13 more)

### Community 53 - "reciter_keyboard"
Cohesion: 0.14
Nodes (8): reciter_keyboard(), reciter_label(), reciter_page_count(), reciter_search_keyboard(), _pager_row(), _reciter_buttons(), TestLabels, TestPagination

### Community 54 - "api/progress.py"
Cohesion: 0.17
Nodes (16): not_found(), forget(), ForgetIn, ForgetOut, _juz(), JuzRatio, progress(), ProgressOut (+8 more)

### Community 55 - "Inline Reciter Search Tests"
Cohesion: 0.14
Nodes (19): _audio_result(), data(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter(), test_ayah_audio_dropped_without_public_base_url(), test_ayah_audio_uses_callers_reciter() (+11 more)

### Community 56 - "test_hifz_check.py"
Cohesion: 0.06
Nodes (21): percentile_band(), refresh_streaks(), streak_summary(), user_today(), _answer_data(), _AnyDay, _ask(), _asked() (+13 more)

### Community 58 - "juz_ref"
Cohesion: 0.09
Nodes (7): advancing(), juz_ref(), page_ref(), assert_covers_target_once(), assert_well_formed(), TestAlMulkAcceptance, TestCrossSurahTargets

### Community 59 - "Hifz"
Cohesion: 0.13
Nodes (6): _covers(), _merge_span(), _overlaps(), _split_span(), _touches(), TestHelpers

### Community 61 - "Dispatch Order Tests"
Cohesion: 0.18
Nodes (17): _callback(), data(), fake_bot(), _message(), probe(), _sent_a_verse(), test_a_command_beats_a_pending_reciter_search(), test_a_command_escapes_a_wizard_without_ending_it() (+9 more)

### Community 63 - "Mini App Plan"
Cohesion: 0.14
Nodes (14): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 6. Frontend structure (`quranayat-miniapp`), 7. Bot ↔ Mini App integration (+6 more)

### Community 65 - "surah_progress"
Cohesion: 0.07
Nodes (8): quran_progress(), started_surahs(), surah_progress(), _at(), TestInputHandling, TestQuranProgress, TestSpecAcceptance, TestSurahProgress

### Community 67 - "InMemoryIdentityStore"
Cohesion: 0.11
Nodes (3): InMemoryIdentityStore, InMemoryStore, Store

### Community 68 - "get_store"
Cohesion: 0.16
Nodes (7): get_store(), _lock(), load_summary(), _added_update(), TestAdded, TestDailyPost, TestLoadSummary

### Community 69 - "Quran"
Cohesion: 0.04
Nodes (25): 4. Navigation model, Page images and page audio, Structural divisions (page / juz / sajda), Translation-only catalogue entries, _consolidations(), Quran, _at_offset(), ayah_count() (+17 more)

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 73 - "api/plans.py"
Cohesion: 0.11
Nodes (23): parse_ref_or_422(), active(), _build(), complete(), create(), DrillOut, lifecycle(), _plan_out() (+15 more)

### Community 74 - "t"
Cohesion: 0.05
Nodes (35): Phase 3 — One router for everything — *done*, handle_incoming(), _incoming(), _on_callback(), _on_text(), _search_reciters(), juz(), page() (+27 more)

### Community 76 - "tick.py"
Cohesion: 0.06
Nodes (22): enqueue(), idempotency_key(), schedule_daily(), _send_plain_message(), register_send_handler(), registered_kinds(), _same_origin(), decorate() (+14 more)

### Community 78 - "Bundle Translations"
Cohesion: 0.15
Nodes (8): _clean_state_store(), bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.11
Nodes (19): Audio catalog kinds, Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES), Mini App feature parity map, Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points), Error taxonomy L1-L5 (word, harakah, tajwid, riwayah mismatch, waqf) (+11 more)

### Community 80 - "BismillahBot — Business Logic"
Cohesion: 0.12
Nodes (15): 1. Overview, 2. Architecture, 3. Request lifecycle, 5. Caching strategy, 7. Known limitations / tech debt, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic (+7 more)

### Community 81 - "Streaks: compute_streak"
Cohesion: 0.24
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 83 - "InMemorySessionStore"
Cohesion: 0.07
Nodes (6): InMemorySessionStore, LeaderboardEntry, PostgresSessionStore, SessionRow, SessionStore, WeeklyBoard

### Community 84 - "Scheduler Tests"
Cohesion: 0.17
Nodes (4): _claimed_at(), _record(), TestCatchUp, TestTick

### Community 85 - "Layering Tests"
Cohesion: 0.14
Nodes (16): export(), languages(), main(), resolved_table(), _write(), _absolute_imports(), _sources(), test_known_violations_still_exist() (+8 more)

### Community 86 - "build_grid"
Cohesion: 0.18
Nodes (4): build_grid(), _counts(), Grid, TestGrid

### Community 87 - "Portion"
Cohesion: 0.13
Nodes (7): _portion_label(), _preview_text(), Portion, match_portion(), portion_for(), portions_of(), TestPortionShape

### Community 89 - "auth.py"
Cohesion: 0.08
Nodes (37): _b64url(), _b64url_decode(), decode_token(), _init_data_secret(), InvalidInitData, InvalidToken, issue_token(), _sign() (+29 more)

### Community 90 - "Store Contract Tests"
Cohesion: 0.11
Nodes (3): _spans(), TestHifzIntervalEdges, TestHifzIntervals

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.08
Nodes (24): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+16 more)

### Community 92 - "text.py"
Cohesion: 0.14
Nodes (4): data(), fake_bot(), TestVerseText, tg_bot()

### Community 95 - "test_channels_telegram.py"
Cohesion: 0.16
Nodes (5): for_platform(), bot(), cache(), TestChoice, TestForPlatform

### Community 97 - "test_media_cache_keys.py"
Cohesion: 0.15
Nodes (8): _bot(), _next_id(), send_audio(), send_photo(), no_cdn(), _source(), test_a_miss_caches_under_the_key_and_a_hit_replays_it(), test_a_rejected_cached_id_is_rebuilt_and_recached()

### Community 100 - "api/catalog.py"
Cohesion: 0.20
Nodes (10): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, put_position(), ReaderPosition, Reciter (+2 more)

### Community 101 - "MemoryStore"
Cohesion: 0.12
Nodes (6): 6. Issues fixed in this refactor, 11.1 Profile settings reset after a while — `fix/settings-persistence`, 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, CacheUnavailable, MemoryStore

### Community 102 - "weekly_board"
Cohesion: 0.28
Nodes (3): weekly_board(), make_user(), TestWeeklyBoard

### Community 103 - "Refactor — Implementation Plan"
Cohesion: 0.13
Nodes (14): button_rows() row-packing helper, Copy-pasted patterns table (§1.3), ignore_not_modified() context manager, tests/test_layering.py ratchet (KNOWN violations), Overlap with MULTI_PLATFORM_PLAN channel seam, Shared UTC offset picker (time_pickers.offset_keyboard), Decisions and open questions (§9), Found along the way (out-of-scope behaviour changes) (+6 more)

### Community 104 - "recall_check.py"
Cohesion: 0.08
Nodes (21): _assemble(), build_question(), _continuation_question(), _date_key(), display_length(), _distinct(), _everything(), _gather() (+13 more)

### Community 105 - "._send_media"
Cohesion: 0.12
Nodes (5): _build(), ignore_not_modified(), _send(), send_cached(), build()

### Community 107 - "inline.py"
Cohesion: 0.21
Nodes (6): answer_inline_query(), inline_audio_result(), inline_photo_results(), combined_audio_key(), range_audio_url(), ref_key()

### Community 108 - "test_hifz_streak.py"
Cohesion: 0.20
Nodes (6): _ctx(), _isolate_registries(), _photo_message(), _Settings, TestCallback, TestWhatTicksADay

### Community 109 - "quran.py"
Cohesion: 0.08
Nodes (18): Phase 2 — DRY the duplicated patterns — *done*, language_keyboard(), language_picker(), translation_language_keyboard(), button_rows(), sajda_keyboard(), offset_keyboard(), _division_marks() (+10 more)

### Community 110 - "stats.py"
Cohesion: 0.18
Nodes (10): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut (+2 more)

### Community 111 - "send_page"
Cohesion: 0.29
Nodes (7): send_page(), _buffer(), _stub_stitch(), stub(), TestPageCard, capture(), counting()

### Community 113 - "store/__init__.py"
Cohesion: 0.13
Nodes (3): Caps, Incoming, MemoryState

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

### Community 118 - "services/leaderboard.py"
Cohesion: 0.25
Nodes (3): user_week_window(), week_window(), TestWeekWindow

### Community 119 - "parse_ayah_range"
Cohesion: 0.23
Nodes (3): parse_ayah_range(), TestCommandArguments, TestParseAyahRange

### Community 121 - "corpus"
Cohesion: 0.18
Nodes (6): _ayah_text(), _basmala_prefix(), _clean(), corpus(), _option_from(), _whole_ayah_option()

### Community 122 - "test_hifz_intervals.py"
Cohesion: 0.23
Nodes (6): _assert_invariant(), _ayahs(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order(), TestEveryRelativePosition

### Community 123 - "streak.py"
Cohesion: 0.26
Nodes (6): _caption(), _keyboard(), on_streak(), _send_graph(), streak(), StreakSummary

### Community 127 - "Blue Green Ci: jobs"
Cohesion: 0.15
Nodes (13): name, needs, runs-on, jobs, build, lint, rollback, name (+5 more)

### Community 128 - "Blue Green Ci: with"
Cohesion: 0.15
Nodes (13): with, cache, cache-dependency-path, cache-from, cache-to, context, if-no-files-found, load (+5 more)

### Community 129 - "send_repeated_audio"
Cohesion: 0.26
Nodes (3): send_repeated_audio(), _stub_audio(), TestRepeatForMemorization

### Community 130 - "test_navigation.py"
Cohesion: 0.13
Nodes (8): data(), fake_bot(), _message(), _no_network(), TestJuzCommand, TestPageCommand, TestSajdaCommand, tg_bot()

### Community 132 - "Mini App Plan: Separate quranayatminiapp Nextjs"
Cohesion: 0.15
Nodes (13): Inline query answering (all four representations, ranges), Navigation model ((surah, ayah, type) per chat_id), Page audio with stitched fallback, Page image stitching (lib/page_image.py), Repeat (memorization), Structural divisions (page / juz / sajda from quran-data.xml), Uthmani text in Amiri Quran / KFGQPC font, Client-side playlist audio (no server stitching) (+5 more)

### Community 135 - "range_audio"
Cohesion: 0.11
Nodes (6): range_audio(), content(), TestRangeAudioRoute, fake_download(), TestStitching, __init__()

### Community 136 - "json"
Cohesion: 0.13
Nodes (10): build(), main_(), _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl(), _as_dict(), _keyboards(), _render() (+2 more)

### Community 137 - "GroupStore"
Cohesion: 0.10
Nodes (4): GroupConfig, GroupMemberLink, GroupPlanRow, GroupStore

### Community 140 - "Business Logic: The hifz platform memorization"
Cohesion: 0.22
Nodes (7): Central callback prefix allocation (hifz.PREFIXES), The hifz platform (memorization companion), Pure plan builder (build_plan), Streak day ticks on completed session, Bot ↔ Mini App integration (menu button, startapp, /app), recitation_job table and user_profile.riwayah, /recite flow (voice note → recitation_job → report)

### Community 141 - "export"
Cohesion: 0.36
Nodes (6): build_meta(), export(), main(), _spans(), split_basmalah(), _write()

### Community 143 - "t"
Cohesion: 0.07
Nodes (37): command, Routing rules (in `serve`), 5. API surface (`/api/v1`), Phase 2 — WhatsApp MVP (reader + daily ayat), Ctx, check(), _begin_setup(), handle_start_payload() (+29 more)

### Community 144 - "get_language"
Cohesion: 0.11
Nodes (6): nav_labels(), get_language(), is_supported(), TestLanguageLookup, TestTransliteration, TestLanguageFlags

### Community 146 - "PostgresScheduleStore"
Cohesion: 0.09
Nodes (5): PostgresIdentityStore, _stored(), PostgresStore, PostgresScheduleStore, store()

### Community 148 - "Hifz Seam Tests: test_hifz_seampy"
Cohesion: 0.18
Nodes (3): _isolate_registries(), _Settings, TestSchemaApplication

### Community 152 - "test_miniapp_links.py"
Cohesion: 0.24
Nodes (9): _app_command(), app_on(), data(), test_app_command(), test_app_command_without_url(), test_cards_and_drill_link_to_their_screens(), test_inline_messages_never_get_a_web_app_button(), test_off_by_default() (+1 more)

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 155 - "Translation editions table (48 codes)"
Cohesion: 0.33
Nodes (5): alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Locale review tracking table (47 locales)

### Community 159 - "MINI_APP_PLAN.md"
Cohesion: 0.13
Nodes (17): /api/v1 REST surface, initData HMAC validation → short-lived JWT, OpenAPI → TypeScript client pipeline, Recall check integrity (signed question_token), Mini App risks, Identity table (platform, external_id → user_id), Normalized Incoming event, Neutral message model rendering (HTML / WhatsApp markup) (+9 more)

### Community 162 - "Blue Green Ci: postgres"
Cohesion: 0.22
Nodes (9): POSTGRES_DB, POSTGRES_HOST_AUTH_METHOD, POSTGRES_USER, env, image, options, ports, postgres (+1 more)

### Community 163 - "Blue Green Ci: test"
Cohesion: 0.22
Nodes (9): TEST_DATABASE_URL, test, python-version, fail-fast, matrix, env, name, runs-on (+1 more)

### Community 164 - "Blue Green Ci: preflight"
Cohesion: 0.22
Nodes (9): preflight, active, deploy_enabled, target, if, name, needs, outputs (+1 more)

### Community 165 - "check_locales.py"
Cohesion: 0.12
Nodes (12): Hifz platform frozen string manifest, src/locales/en.py source of truth, Key conventions (btn_*, cmd_*), Wave process (feature agents, translation agents, reviewers), Native-speaker review - hifz platform strings, Review process steps, Review criteria (meaning, register, grammatical number, RTL, button length), main() (+4 more)

### Community 166 - "services/streaks.py"
Cohesion: 0.11
Nodes (11): _as_utc(), local_date(), local_now(), Milestone, milestone_for(), _milestone_key(), offset_of(), StreakCounts (+3 more)

### Community 169 - "TestPickerFlow"
Cohesion: 0.13
Nodes (8): _callback(), data(), fake_bot(), _message(), _tab_row(), TestAudioNeverFollowsLanguage, TestPickerFlow, tg_bot()

### Community 170 - "button_action"
Cohesion: 0.11
Nodes (6): button_action(), missing_keys(), _placeholders(), TestButtonAction, TestGroupLocaleExemption, TestLocaleIntegrity

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 172 - "TranslationRegistry"
Cohesion: 0.09
Nodes (20): 10. File-by-file change list, 11. Memory & performance (free-tier reality), 12. Testing, 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 2. Current-state audit (what is hardcoded English), 3. Target architecture (+12 more)

### Community 176 - "BUSINESS_LOGIC.md"
Cohesion: 0.25
Nodes (5): Four ayah representations (english, tafsir, arabic, audio), Future roadmap and prioritized backlog, Known limitations / tech debt, Issues fixed in the refactor (12 bugs), Verse card (inline keyboard, edit in place)

### Community 178 - "BismillahBot README"
Cohesion: 0.16
Nodes (13): Translation Attributions, Documentation, Documentation index (docs/README.md), Phase 6 — Repository hygiene, CI — Blue-Green pipeline, Running the tests locally, Testing & CI, What's covered (+5 more)

### Community 179 - "8. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 8. Phased task breakdown, Phase 0 — Foundations, Phase 1 — Service-layer extraction (this repo, no UI change), Phase 2 — Reader parity (read-only, low risk, ships first), Phase 3 — Hifz parity, Phase 4 — Recitation checker UI (depends on the investigation's Phase A), Phase 5 — Later

### Community 182 - "Blue Green Ci: deploygreen"
Cohesion: 0.33
Nodes (6): environment, if, name, needs, runs-on, deploy-green

### Community 183 - "Blue Green Ci: promote"
Cohesion: 0.33
Nodes (6): promote, environment, if, name, needs, runs-on

### Community 187 - "test_scheduler.py"
Cohesion: 0.32
Nodes (3): _isolate_handlers(), state(), store()

### Community 205 - "bot/media.py"
Cohesion: 0.08
Nodes (13): deliver_combined_audio(), stitch(), deliver_page_audio(), deliver_repeated_audio(), stitch(), page_caption(), download_combined_audio(), download_stitched_audio() (+5 more)

### Community 284 - "miniapp.py"
Cohesion: 0.28
Nodes (5): app_button(), app_url(), set_menu_button(), test_menu_button(), test_menu_button_off_without_url()

### Community 286 - "test_export_web_content.py"
Cohesion: 0.21
Nodes (7): _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah(), test_meta_surahs_and_sajdas(), test_tafsir_has_every_ayah()

### Community 289 - "reciter.py"
Cohesion: 0.18
Nodes (6): reciter_page_of(), performers(), reciter_catalog(), reciter_group(), reciter_kind(), TestCurrentReciter

## Knowledge Gaps
- **51 isolated node(s):** `button_rows() row-packing helper`, `ignore_not_modified() context manager`, `Found along the way (out-of-scope behaviour changes)`, `Phase 0 — Guardrails (ruff, layering test, logging)`, `ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1584 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **115 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `get_store` to `summarize`, `Leaderboard`, `_ctx`, `Profile`, `Store`, `render_streak_graph`, `UserSettings`, `Context`, `PostgresScheduleStore`, `RedisSingleton`, `typing`, `Hifz Progress Cmd Tests`, `Hifz Streak Tests`, `Acceptance Tests`, `get_settings`, `File`, `services/streaks.py`, `Session`, `Streaks`, `Services`, `api/check.py`, `Dispatch`, `api/progress.py`, `test_hifz_check.py`, `_hifz`, `surah_progress`, `InMemoryIdentityStore`, `api/plans.py`, `t`, `tick.py`, `TestAddInterval`, `MemoryStore`, `weekly_board`, `stats.py`, `store/__init__.py`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `button_rows() row-packing helper`, `ignore_not_modified() context manager`, `Found along the way (out-of-scope behaviour changes)` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_plan` be split into smaller, more focused modules?**
  _Cohesion score 0.058018018018018015 - nodes in this community are weakly interconnected._
- **Why does `Quran` connect `Quran` to `build_plan`, `.page_range`, `summarize`, `services/plans.py`, `test_navigation.py`, `range_audio`, `Profile`, `export`, `t`, `t`, `Refs`, `typing`, `Hifz Progress Cmd Tests`, `Group`, `test_export_web_content.py`, `.get`, `services/check.py`, `features/check.py`, `Ref`, `TranslationRegistry`, `parse_quran_tafsir`, `api/check.py`, `api/progress.py`, `juz_ref`, `surah_progress`, `api/plans.py`, `t`, `bot/media.py`, `BismillahBot — Business Logic`, `text.py`, `api/catalog.py`, `recall_check.py`, `inline.py`, `quran.py`, `corpus`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Ctx` (e.g. with `3. Architecture` and `4.1 Overlap with `MULTI_PLATFORM_PLAN.md``) actually correct?**
  _`Ctx` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Should `.page_range` be split into smaller, more focused modules?**
  _Cohesion score 0.12857142857142856 - nodes in this community are weakly interconnected._