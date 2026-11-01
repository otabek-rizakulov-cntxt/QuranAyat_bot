# Graph Report - QuranAyat_bot  (2026-11-01)

## Corpus Check
- 240 files · ~215,678 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 4451 nodes · 10373 edges · 248 communities (139 shown, 109 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 990 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6068b31d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Plan Builder
- Quran
- summarize
- services/plans.py
- .start
- Plan Setup
- auth.py
- localtime.py
- Ctx
- Leaderboard
- Hifz Profile Tests
- Profile
- Store
- streak_image.py
- services/streaks.py
- User Settings
- Context
- Health
- Refs
- RedisSingleton
- typing
- Router
- button_rows
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
- Hifz Progress: round_percent
- pages.py
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
- reciter_keyboard
- services/check.py
- Inline Reciter Search Tests
- test_hifz_check.py
- Multi Platform Plan
- Refs: get_surah_length
- Hifz
- _hifz
- Dispatch Order Tests
- _message
- Mini App Plan
- PostgresSessionStore
- surah_progress
- InMemoryGroupStore
- TestRestartDeliversExactlyOnce
- Profiles
- t
- api/plans.py
- reset_for_tests
- Hifz Seam Tests
- features/check.py
- dispatch.py
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
- build_grid
- test_wizard.py
- Store Contract Tests
- Multi Platform Plan: MultiPlatform Implementation Plan
- locales/__init__.py
- Hifz platform frozen string manifest
- Profiles: ProfileRow
- parse_offset
- Hifz Seam Tests: TestRegistration
- _bot
- Scheduler Tests: TestTransientFailuresAreRetried
- Store Contract Tests: TestPlans
- Business Logic
- Plans: PlanDaySpec
- weekly_board
- Refactor — Implementation Plan
- recall_check.py
- ._send_media
- .get
- Time Pickers
- channels/telegram.py
- bot/media.py
- PostgresPlanStore
- build_data
- Store Contract Tests: TestSchedule
- store/__init__.py
- Safety net (characterisation tests, staging smoke, blue-green)
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- Progress: featuresprogresspy
- Export Web Content Tests
- reciter_set_confirmation
- _seed_legacy_lang
- 8. Phased task breakdown
- streak.py
- Schedule: InMemoryScheduleStore
- Schedule: PostgresScheduleStore
- Mini App Plan: normalize_lang
- Blue Green Ci: jobs
- Blue Green Ci: with
- corpus
- Parsing
- Wizard
- Mini App Plan: Separate quranayatminiapp Nextjs
- scheduler/__init__.py
- Channel
- Media: range_audio
- registry.py
- TestTransliteration
- Store Contract Tests: TestLeaderboard
- TestProfiles
- Business Logic: The hifz platform memorization
- TestCorpusIntegrity
- stats.py
- Parsing: parse_ayah
- week_window
- reciter
- test_channels_telegram.py
- to_markup
- Hifz Seam Tests: test_hifz_seampy
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- Choice
- TestBoard
- Blue Green Ci: env
- 11. Infrastructure, capacity and cost on paid Koyeb
- level_for
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
- test_bot_errors.py
- Blue Green Ci: smokegreen
- test_the_basmala_heading_is_not_part_of_the_question
- sweep_refs
- File Facade: search_performers
- Scheduler Tests: test_schedulerpy
- target_label
- Verse Card Tests
- BismillahBot README
- _isolate_registries
- TestRegistration
- test_pick_ayah_accepts_anything_with_as_tuple
- Blue Green Ci: deploygreen
- Blue Green Ci: promote
- _isolate_registries
- get_store
- Hifz Seam Tests: test_longest_prefix_wins
- Scheduler Tests: TestRunScheduler
- test_the_answer_is_not_findable_by_sorting_on_length
- test_options_are_distinct_even_ignoring_vowelling
- test_a_different_date_gives_a_different_question
- test_pick_then_build_is_the_whole_check_flow
- Claude
- Acceptance Tests: TestSevenTheCommandsExist
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
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `5. Caching strategy` --references--> `MemoryStore`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/infra/redis_client.py
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

## Communities (248 total, 109 thin omitted)

### Community 0 - "Plan Builder"
Cohesion: 0.05
Nodes (18): advancing(), auto_pace(), build_plan(), juz_ref(), surah_ref(), to_day_specs(), assert_covers_target_once(), assert_well_formed() (+10 more)

### Community 1 - "Quran"
Cohesion: 0.04
Nodes (19): 4. Navigation model, Page images and page audio, Structural divisions (page / juz / sajda), Translation-only catalogue entries, _advance(), _consolidations(), next_scheduled_date(), _validated_days() (+11 more)

### Community 2 - "summarize"
Cohesion: 0.08
Nodes (8): Progress, summarize(), SurahProgress, HifzInterval, load_summary(), _at(), TestLoadSummary, TestSummarize

### Community 3 - "services/plans.py"
Cohesion: 0.10
Nodes (17): today(), change_status(), complete_day(), current_plan(), day_position(), DrillResult, due_days(), enqueue_next() (+9 more)

### Community 5 - "Plan Setup"
Cohesion: 0.08
Nodes (38): on_group_tap(), memorize(), on_tap(), plan_step(), _expired(), _ref_from_draft(), _ref_to_draft(), _know_by_heart() (+30 more)

### Community 6 - "auth.py"
Cohesion: 0.13
Nodes (12): jwt_secret(), require_user(), _unauthorized(), answer(), AnswerIn, AnswerOut, make_token(), question() (+4 more)

### Community 7 - "localtime.py"
Cohesion: 0.13
Nodes (9): _as_utc(), local_date(), local_now(), local_time(), next_due_utc(), to_utc(), TestLocalDate, TestNextDueUtc (+1 more)

### Community 8 - "Ctx"
Cohesion: 0.11
Nodes (29): command, Routing rules (in `serve`), 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, Ctx, _join_board(), _board_message(), leaderboard() (+21 more)

### Community 9 - "Leaderboard"
Cohesion: 0.11
Nodes (10): _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join(), _Message, _sent(), _Settings (+2 more)

### Community 10 - "Hifz Profile Tests"
Cohesion: 0.08
Nodes (17): _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _isolate_registries(), _Message, _profile_row() (+9 more)

### Community 11 - "Profile"
Cohesion: 0.08
Nodes (22): patch_profile(), name_step(), offset_from_callback(), _plan_line(), profile_command(), profile_view(), reminder_keyboard(), reminder_step() (+14 more)

### Community 12 - "Store"
Cohesion: 0.10
Nodes (10): _CallbackQuery, _ctx(), _Message, _run_wizard(), _Settings, _tap(), TestDrill, TestEnqueueChain (+2 more)

### Community 13 - "streak_image.py"
Cohesion: 0.14
Nodes (7): render(), draw_contribution_graph(), render_streak_graph(), _semaphore(), open_png(), TestRendering, TestRenderStreakGraph

### Community 14 - "services/streaks.py"
Cohesion: 0.15
Nodes (8): offset_of(), StreakCounts, refresh_streaks(), SessionOutcome, streak_summary(), user_offset(), user_today(), TestRefreshAndSummary

### Community 15 - "User Settings"
Cohesion: 0.13
Nodes (9): patch_settings(), _unprocessable(), _legacy_lang_key(), SettingsRow, UserSettings, TestDefaults, TestIndependence, TestKeyedByUserId (+1 more)

### Community 16 - "Context"
Cohesion: 0.16
Nodes (15): ctx(), _bot(), _ctx(), _isolate_registries(), _member(), _run_setup_to_plan(), _Settings, tap() (+7 more)

### Community 17 - "Health"
Cohesion: 0.06
Nodes (15): health(), store_backend(), database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries(), fresh_redis() (+7 more)

### Community 18 - "Refs"
Cohesion: 0.07
Nodes (12): _clean(), format_ref(), page_ref(), parse_range(), parse_reference(), TestSurahSpans, TestAcrossSurahs, TestFormatting (+4 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.07
Nodes (15): 6. Issues fixed in this refactor, 11.1 Profile settings reset after a while — `fix/settings-persistence`, get(), _key(), save(), get(), expect(), _key() (+7 more)

### Community 20 - "typing"
Cohesion: 0.04
Nodes (25): create_app(), _commands_for(), initialize(), lifespan(), _set_bot_commands(), _process_update(), telegram_webhook(), webhook_secret() (+17 more)

### Community 21 - "Router"
Cohesion: 0.07
Nodes (23): 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 3 — One router for everything — *done*, Phase 5 — Fix the layering — *done*, Phase 6 — Repository hygiene — *done*, _on_callback(), _on_text(), decorate() (+15 more)

### Community 22 - "button_rows"
Cohesion: 0.14
Nodes (10): Phase 2 — DRY the duplicated patterns — *done*, language_keyboard(), language_picker(), translation_language_keyboard(), button_rows(), sajda_keyboard(), test_a_non_positive_width_is_one_per_row(), test_an_exact_fit_has_no_empty_trailing_row() (+2 more)

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "Group"
Cohesion: 0.09
Nodes (22): _begin_setup(), bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), _enqueue_next_board(), _enqueue_next_group() (+14 more)

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.13
Nodes (15): 10. Found along the way (out of scope — behaviour changes), 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, 2. Goals and non-goals, 3. Principles applied, 6. Ordering, risk, size, 7. Safety net, 8. Expected result (+7 more)

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
Cohesion: 0.13
Nodes (11): _CallbackQuery, _cmd(), _ctx(), _Message, _run_wizard(), _Settings, _tap(), TestFourProgress (+3 more)

### Community 30 - "Hifz Progress: quran_page_progress"
Cohesion: 0.11
Nodes (4): juz_page_progress(), quran_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 32 - "test_inline_range.py"
Cohesion: 0.04
Nodes (22): _stress_reset(), _stress_stats(), source(), stitch(), download_combined_audio(), download_stitched_audio(), has_page_audio(), page_audio_url() (+14 more)

### Community 33 - "test_recall_check.py"
Cohesion: 0.04
Nodes (22): test_both_question_modes_show_up_in_the_sweep(), test_correct_option_is_never_a_length_outlier(), test_correct_option_is_never_the_extreme_by_a_wide_ratio(), test_correct_option_really_follows_the_prompt(), test_dates_and_iso_strings_are_interchangeable(), test_every_option_carries_the_same_word_count(), test_long_ayah_prompt_and_options_stay_button_sized(), test_muqattaat_get_muqattaat_shaped_distractors() (+14 more)

### Community 34 - "TranslationRegistry"
Cohesion: 0.18
Nodes (5): 10. File-by-file change list, 3. Target architecture, TranslationRegistry, TestCaching, TestFallback

### Community 35 - "Auth"
Cohesion: 0.10
Nodes (32): _b64url(), _b64url_decode(), decode_token(), _init_data_secret(), InvalidInitData, InvalidToken, issue_token(), _sign() (+24 more)

### Community 36 - "File"
Cohesion: 0.08
Nodes (5): File, TestAudioFilename, TestImageFilename, TestLegacyLanguageKey, TestStateStore

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.09
Nodes (23): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 1. Terminology (so the report language is right), 2. What "correct" can mean — error taxonomy, 3.1 Commercial, 3.2 Open models and data, 3.3 Reference *text* per riwāyah (+15 more)

### Community 38 - "Hifz Progress: round_percent"
Cohesion: 0.08
Nodes (5): format_percent(), PageProgress, _Ratio, round_percent(), TestRounding

### Community 39 - "pages.py"
Cohesion: 0.10
Nodes (16): juz(), page(), reader_position(), send_page(), stitch(), as_int(), fetch_and_stitch(), _fit_for_telegram() (+8 more)

### Community 40 - "verse_keyboard"
Cohesion: 0.06
Nodes (26): page_keyboard(), verse_keyboard(), mode_button(), app_button(), app_row(), app_url(), set_menu_button(), nav_labels() (+18 more)

### Community 41 - "Session"
Cohesion: 0.16
Nodes (17): init_data_max_age(), auth_telegram(), AuthOut, me(), _me(), MeOut, PlanSummary, Profile (+9 more)

### Community 42 - "Plans: PlanStore"
Cohesion: 0.09
Nodes (3): PlanDayRow, PlanRow, PlanStore

### Community 43 - "Ref"
Cohesion: 0.08
Nodes (14): _clip(), _covered(), _focus_surah(), _intersect(), _page_share(), _pages_of(), ProgressSummary, _recency_key() (+6 more)

### Community 44 - "SendCtx"
Cohesion: 0.19
Nodes (3): _send_plain_message(), SendCtx, TestDailyPost

### Community 45 - "Streaks"
Cohesion: 0.18
Nodes (3): record_session(), TestThreeTheStreak, TestRecordSession

### Community 46 - "Load Test"
Cohesion: 0.13
Nodes (13): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+5 more)

### Community 47 - "Multilingual Plan"
Cohesion: 0.19
Nodes (12): Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), Quran.from_file(path) refactor, setMyCommands per language, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+4 more)

### Community 48 - "Text"
Cohesion: 0.22
Nodes (6): _inline_query(), _of_type(), _results(), TestInlineArabicImage, TestRangeAudio, TestRangeText

### Community 49 - "Schema"
Cohesion: 0.12
Nodes (24): group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval, hifz_interval_user_surah_idx (+16 more)

### Community 50 - "Services"
Cohesion: 0.15
Nodes (19): _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today(), test_me_carries_plan_and_streak() (+11 more)

### Community 51 - "Progress"
Cohesion: 0.15
Nodes (17): not_found(), surah_name(), forget(), ForgetIn, ForgetOut, _juz(), JuzRatio, progress() (+9 more)

### Community 52 - "Dispatch"
Cohesion: 0.17
Nodes (19): handle_update(), _callback(), data(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index() (+11 more)

### Community 53 - "reciter_keyboard"
Cohesion: 0.11
Nodes (10): reciter_keyboard(), reciter_page_count(), reciter_group(), _callback(), _message(), _pager_row(), _reciter_buttons(), _tab_row() (+2 more)

### Community 54 - "services/check.py"
Cohesion: 0.14
Nodes (7): preload_corpus(), RecallQuestion, ask(), default_span(), rebuild(), Score, score()

### Community 55 - "Inline Reciter Search Tests"
Cohesion: 0.14
Nodes (19): _audio_result(), data(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter(), test_ayah_audio_dropped_without_public_base_url(), test_ayah_audio_uses_callers_reciter() (+11 more)

### Community 56 - "test_hifz_check.py"
Cohesion: 0.16
Nodes (9): _AnyDay, _ask(), _asked(), _buttons(), _callback_query(), _ctx(), _Settings, TestCallbackDataDiscipline (+1 more)

### Community 57 - "Multi Platform Plan"
Cohesion: 0.18
Nodes (12): Pure plan builder (build_plan), /api/v1 REST surface, initData HMAC validation → short-lived JWT, OpenAPI → TypeScript client pipeline, Recall check integrity (signed question_token), Mini App risks, Other platforms shortlist (Messenger, Viber, Discord, PWA, Signal), Multi-platform phased breakdown (Phases 0-6) (+4 more)

### Community 58 - "Refs: get_surah_length"
Cohesion: 0.18
Nodes (4): ayah_count(), TestAyahCount, test_short_surahs_still_get_four_distinct_options(), test_the_last_ayah_of_every_surah_produces_a_question()

### Community 59 - "Hifz"
Cohesion: 0.08
Nodes (8): _covers(), _merge_span(), _normalize(), _overlaps(), PostgresHifzStore, _split_span(), _touches(), TestHelpers

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
Cohesion: 0.11
Nodes (19): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 4.1 Flow, 4.2 Rules (+11 more)

### Community 64 - "PostgresSessionStore"
Cohesion: 0.13
Nodes (3): PostgresStore, PostgresSessionStore, store()

### Community 65 - "surah_progress"
Cohesion: 0.11
Nodes (5): started_surahs(), surah_progress(), TestInputHandling, TestSpecAcceptance, TestSurahProgress

### Community 66 - "InMemoryGroupStore"
Cohesion: 0.06
Nodes (6): GroupConfig, GroupMemberLink, GroupPlanDayRow, GroupPlanRow, GroupStore, InMemoryGroupStore

### Community 69 - "t"
Cohesion: 0.06
Nodes (17): main(), placeholders(), button_action(), command_lines(), keyboard_rows(), missing_keys(), missing_locales(), _reverse_button_map() (+9 more)

### Community 70 - "api/plans.py"
Cohesion: 0.13
Nodes (21): parse_ref_or_422(), ref_out(), RefOut, active(), _build(), complete(), create(), DrillOut (+13 more)

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 73 - "features/check.py"
Cohesion: 0.15
Nodes (8): _answer_data(), _ask(), check(), on_check(), _options_keyboard(), _parse_answer(), _question_text(), _score()

### Community 74 - "dispatch.py"
Cohesion: 0.07
Nodes (13): _search_reciters(), answer_inline_query(), inline_audio_result(), reciter_label(), combined_audio_key(), range_audio_url(), resolve_settings(), ref_key() (+5 more)

### Community 75 - "Hifz Progress: juz_progress"
Cohesion: 0.11
Nodes (7): juz_progress(), JuzProgress, quran_progress(), _spans(), started_juzs(), TestJuzProgress, TestQuranProgress

### Community 76 - "Tick"
Cohesion: 0.13
Nodes (12): catch_up(), run_scheduler(), _wait(), _deliver(), _is_stale(), _lock(), _release(), _resolve() (+4 more)

### Community 78 - "Bundle Translations"
Cohesion: 0.10
Nodes (10): _clean_state_store(), bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file() (+2 more)

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.10
Nodes (22): Audio catalog kinds, Page audio with stitched fallback, Repeat (memorization), Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES), Client-side playlist audio (no server stitching), Mini App feature parity map, Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5) (+14 more)

### Community 80 - "build_question"
Cohesion: 0.25
Nodes (6): build_question(), _answer_data(), _sessions(), _tap(), TestScoring, TestStaleButtons

### Community 81 - "Streaks: compute_streak"
Cohesion: 0.21
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 83 - "Sessions"
Cohesion: 0.09
Nodes (5): InMemorySessionStore, LeaderboardEntry, SessionRow, SessionStore, WeeklyBoard

### Community 84 - "Scheduler Tests"
Cohesion: 0.17
Nodes (4): _claimed_at(), _record(), TestCatchUp, TestTick

### Community 85 - "Layering Tests"
Cohesion: 0.09
Nodes (24): export(), languages(), main(), resolved_table(), _write(), build(), main_(), build_meta() (+16 more)

### Community 86 - "BismillahBot — Multilingual Support Plan"
Cohesion: 0.09
Nodes (19): 7. Known limitations / tech debt, 11. Memory & performance (free-tier reality), 12. Testing, 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 2. Current-state audit (what is hardcoded English), 4. User language preference (+11 more)

### Community 87 - "Plan Builder: Portion"
Cohesion: 0.13
Nodes (7): _portion_label(), _preview_text(), Portion, match_portion(), portion_for(), portions_of(), TestPortionShape

### Community 88 - "build_grid"
Cohesion: 0.18
Nodes (4): build_grid(), _counts(), Grid, TestGrid

### Community 89 - "test_wizard.py"
Cohesion: 0.13
Nodes (3): test_draft_is_written_with_that_ttl(), TestCoexistsWithTheReciterFlow, wiz()

### Community 90 - "Store Contract Tests"
Cohesion: 0.11
Nodes (3): _spans(), TestHifzIntervalEdges, TestHifzIntervals

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.12
Nodes (17): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+9 more)

### Community 92 - "locales/__init__.py"
Cohesion: 0.07
Nodes (18): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, put_position(), ReaderPosition, Reciter (+10 more)

### Community 93 - "Hifz platform frozen string manifest"
Cohesion: 0.13
Nodes (13): Translation Attributions, alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Hifz platform frozen string manifest, src/locales/en.py source of truth, Key conventions (btn_*, cmd_*) (+5 more)

### Community 94 - "Profiles: ProfileRow"
Cohesion: 0.06
Nodes (3): ProfileRow, ProfileStore, UserSettingsRow

### Community 95 - "parse_offset"
Cohesion: 0.10
Nodes (5): format_offset(), parse_offset(), TestFormatOffset, TestParseOffset, TestPicker

### Community 97 - "_bot"
Cohesion: 0.38
Nodes (5): _bot(), _next_id(), send_audio(), send_photo(), test_a_rejected_cached_id_is_rebuilt_and_recached()

### Community 100 - "Business Logic"
Cohesion: 0.15
Nodes (13): 1. Overview, 2. Architecture, 3. Request lifecycle, 5. Caching strategy, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic, Local time (+5 more)

### Community 102 - "weekly_board"
Cohesion: 0.28
Nodes (3): weekly_board(), make_user(), TestWeeklyBoard

### Community 103 - "Refactor — Implementation Plan"
Cohesion: 0.13
Nodes (14): button_rows() row-packing helper, Copy-pasted patterns table (§1.3), ignore_not_modified() context manager, tests/test_layering.py ratchet (KNOWN violations), Overlap with MULTI_PLATFORM_PLAN channel seam, Shared UTC offset picker (time_pickers.offset_keyboard), Decisions and open questions (§9), Found along the way (out-of-scope behaviour changes) (+6 more)

### Community 104 - "recall_check.py"
Cohesion: 0.08
Nodes (21): _assemble(), _at_offset(), _continuation_question(), _date_key(), display_length(), _distinct(), _everything(), _gather() (+13 more)

### Community 107 - "Time Pickers"
Cohesion: 0.35
Nodes (7): offset_keyboard(), _grid(), test_a_label_prefix_changes_only_the_label(), test_cancel_data_adds_a_localized_cancel_row(), test_every_offset_is_offered_in_order_under_the_callers_prefix(), test_no_cancel_row_unless_asked(), test_rows_are_columns_wide()

### Community 108 - "channels/telegram.py"
Cohesion: 0.17
Nodes (4): Caps, Incoming, ignore_not_modified(), _send()

### Community 109 - "bot/media.py"
Cohesion: 0.07
Nodes (26): 1. Why, Phase 1 — Take `main.py` apart (pure moves) — *done*, _post_portion(), push_group_day(), push_plan_day(), _send_drill(), _translation_text(), random_ayah() (+18 more)

### Community 111 - "build_data"
Cohesion: 0.18
Nodes (7): build_data(), get_default_query_results(), make_index(), data(), fake_bot(), _no_network(), tg_bot()

### Community 113 - "store/__init__.py"
Cohesion: 0.06
Nodes (7): HifzStore, InMemoryHifzStore, InMemoryStore, Store, InMemoryPlanStore, MemoryState, _isolate_registries()

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
Cohesion: 0.18
Nodes (8): forgot_command(), on_progress_tap(), progress_command(), progress_view(), _show(), _surah_line(), surah_spans(), unmark()

### Community 119 - "Export Web Content Tests"
Cohesion: 0.14
Nodes (10): _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl(), _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah() (+2 more)

### Community 120 - "reciter_set_confirmation"
Cohesion: 0.10
Nodes (8): Phase 4 — Split infrastructure god-objects — *done*, reciter_set_confirmation(), performers(), reciter_catalog(), reciter_kind(), TestCatalogKinds, TestCatalogOrder, TestKindWarnings

### Community 121 - "_seed_legacy_lang"
Cohesion: 0.19
Nodes (3): _seed_legacy_lang(), TestInlineCaller, TestLegacyMigration

### Community 122 - "8. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 8. Phased task breakdown, Phase 0 — Foundations, Phase 1 — Service-layer extraction (this repo, no UI change), Phase 2 — Reader parity (read-only, low risk, ships first), Phase 3 — Hifz parity, Phase 4 — Recitation checker UI (depends on the investigation's Phase A), Phase 5 — Later

### Community 123 - "streak.py"
Cohesion: 0.21
Nodes (7): _caption(), _keyboard(), _send_graph(), streak(), cache_key(), StreakSummary, TestCacheKey

### Community 127 - "Blue Green Ci: jobs"
Cohesion: 0.15
Nodes (13): name, needs, runs-on, jobs, build, lint, rollback, name (+5 more)

### Community 128 - "Blue Green Ci: with"
Cohesion: 0.15
Nodes (13): with, cache, cache-dependency-path, cache-from, cache-to, context, if-no-files-found, load (+5 more)

### Community 129 - "corpus"
Cohesion: 0.15
Nodes (7): _ayah_text(), _basmala_prefix(), _clean(), corpus(), _option_from(), _whole_ayah_option(), _words()

### Community 130 - "Parsing"
Cohesion: 0.19
Nodes (3): parse_ayah_range(), TestCommandArguments, TestParseAyahRange

### Community 132 - "Mini App Plan: Separate quranayatminiapp Nextjs"
Cohesion: 0.14
Nodes (11): Inline query answering (all four representations, ranges), Navigation model ((surah, ayah, type) per chat_id), Page image stitching (lib/page_image.py), Structural divisions (page / juz / sajda from quran-data.xml), Verse card (inline keyboard, edit in place), Uthmani text in Amiri Quran / KFGQPC font, Locale export to JSON (web_ keys, next-intl), Static immutable Quran JSON served from frontend CDN (+3 more)

### Community 133 - "scheduler/__init__.py"
Cohesion: 0.08
Nodes (6): The scheduler (`src/lib/scheduler.py`), enqueue(), idempotency_key(), schedule_daily(), ScheduledSend, ScheduleStore

### Community 135 - "Media: range_audio"
Cohesion: 0.11
Nodes (6): range_audio(), content(), TestRangeAudioRoute, fake_download(), TestStitching, __init__()

### Community 136 - "registry.py"
Cohesion: 0.18
Nodes (5): register_send_handler(), registered_kinds(), _same_origin(), send_handler(), decorate()

### Community 139 - "TestProfiles"
Cohesion: 0.08
Nodes (3): TestProfiles, TestReaderPosition, TestSettings

### Community 140 - "Business Logic: The hifz platform memorization"
Cohesion: 0.13
Nodes (13): Central callback prefix allocation (hifz.PREFIXES), Future roadmap and prioritized backlog, The hifz platform (memorization companion), Streak day ticks on completed session, Bot ↔ Mini App integration (menu button, startapp, /app), Identity table (platform, external_id → user_id), Normalized Incoming event, Neutral message model rendering (HTML / WhatsApp markup) (+5 more)

### Community 142 - "stats.py"
Cohesion: 0.18
Nodes (10): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut (+2 more)

### Community 143 - "Parsing: parse_ayah"
Cohesion: 0.21
Nodes (3): parse_ayah(), parse_quran_tafsir(), TestParseAyah

### Community 144 - "week_window"
Cohesion: 0.29
Nodes (3): user_week_window(), week_window(), TestWeekWindow

### Community 145 - "reciter"
Cohesion: 0.15
Nodes (11): 6. Phased task breakdown, Phase 0 — Prerequisites (no code), Phase 1 — Channel seam (this repo, no user-visible change), Phase 2 — WhatsApp MVP (reader + daily ayat), Phase 3 — Hifz on WhatsApp, Phase 4 — Recitation checker on WhatsApp, Phase 5 — Web access outside Telegram, Phase 6 — Later (+3 more)

### Community 146 - "test_channels_telegram.py"
Cohesion: 0.25
Nodes (3): bot(), cache(), TestChoice

### Community 147 - "to_markup"
Cohesion: 0.29
Nodes (3): to_button(), to_markup(), TestToMarkup

### Community 148 - "Hifz Seam Tests: test_hifz_seampy"
Cohesion: 0.18
Nodes (3): _isolate_registries(), _Settings, TestSchemaApplication

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 155 - "11. Infrastructure, capacity and cost on paid Koyeb"
Cohesion: 0.33
Nodes (6): 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards, 11. Infrastructure, capacity and cost on paid Koyeb

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
Cohesion: 0.13
Nodes (6): Milestone, milestone_for(), _milestone_key(), percentile_band(), TestMilestones, TestPercentile

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 175 - "Scheduler Tests: test_schedulerpy"
Cohesion: 0.32
Nodes (3): _isolate_handlers(), state(), store()

### Community 178 - "BismillahBot README"
Cohesion: 0.13
Nodes (15): Four ayah representations (english, tafsir, arabic, audio), Known limitations / tech debt, Issues fixed in the refactor (12 bugs), Documentation, Documentation index (docs/README.md), Phase 6 — Repository hygiene, CI — Blue-Green pipeline, Running the tests locally (+7 more)

### Community 182 - "Blue Green Ci: deploygreen"
Cohesion: 0.33
Nodes (6): environment, if, name, needs, runs-on, deploy-green

### Community 183 - "Blue Green Ci: promote"
Cohesion: 0.33
Nodes (6): promote, environment, if, name, needs, runs-on

### Community 185 - "get_store"
Cohesion: 0.12
Nodes (7): get_store(), _lock(), _save_plan(), TestFiveAndSixTheBoard, TestTwoTheDailyPush, _added_update(), TestAdded

## Knowledge Gaps
- **51 isolated node(s):** `button_rows() row-packing helper`, `Expected result metrics (§8)`, `ignore_not_modified() context manager`, `Found along the way (out-of-scope behaviour changes)`, `Phase 0 — Guardrails (ruff, layering test, logging)` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1514 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **109 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `get_store` to `summarize`, `services/plans.py`, `auth.py`, `Leaderboard`, `Hifz Profile Tests`, `Profile`, `Store`, `streak_image.py`, `stats.py`, `services/streaks.py`, `Context`, `User Settings`, `RedisSingleton`, `typing`, `Hifz Progress Cmd Tests`, `TestBoard`, `Hifz Streak Tests`, `Acceptance Tests`, `Session`, `SendCtx`, `Streaks`, `Services`, `Progress`, `Dispatch`, `test_hifz_check.py`, `_hifz`, `PostgresSessionStore`, `surah_progress`, `api/plans.py`, `dispatch.py`, `Tick`, `build_question`, `weekly_board`, `bot/media.py`, `store/__init__.py`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `button_rows() row-packing helper`, `Expected result metrics (§8)`, `ignore_not_modified() context manager` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Plan Builder` be split into smaller, more focused modules?**
  _Cohesion score 0.05078929306794784 - nodes in this community are weakly interconnected._
- **Why does `Quran` connect `Quran` to `Plan Builder`, `corpus`, `summarize`, `services/plans.py`, `Plan Setup`, `Media: range_audio`, `Ctx`, `Profile`, `TestCorpusIntegrity`, `Refs`, `typing`, `button_rows`, `Hifz Progress Cmd Tests`, `Hifz Progress: quran_page_progress`, `TranslationRegistry`, `pages.py`, `verse_keyboard`, `Ref`, `sweep_refs`, `target_label`, `Progress`, `services/check.py`, `Refs: get_surah_length`, `_message`, `surah_progress`, `features/check.py`, `dispatch.py`, `Hifz Progress: juz_progress`, `build_question`, `Layering Tests`, `BismillahBot — Multilingual Support Plan`, `locales/__init__.py`, `Business Logic`, `recall_check.py`, `bot/media.py`, `build_data`, `Progress: featuresprogresspy`, `Export Web Content Tests`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `Quran` (e.g. with `Module responsibilities` and `build_meta()`) actually correct?**
  _`Quran` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `Quran` be split into smaller, more focused modules?**
  _Cohesion score 0.041292041292041295 - nodes in this community are weakly interconnected._