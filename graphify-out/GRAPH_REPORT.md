# Graph Report - QuranAyat_bot  (2026-11-01)

## Corpus Check
- 243 files · ~240,623 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 4564 nodes · 10531 edges · 284 communities (143 shown, 141 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 972 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6c28ef5b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_plan
- Quran
- summarize
- services/plans.py
- .start
- _plan_setup.py
- reciter.py
- localtime.py
- Ctx
- Leaderboard
- _ctx
- Profile
- Store
- render_streak_graph
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
- test_page_mode.py
- test_recall_check.py
- TranslationRegistry
- Auth
- File
- Recitation Checker Investigation
- round_percent
- ScheduledSend
- telegram
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
- api/plans.py
- Dispatch
- reciter_keyboard
- advancing
- Inline Reciter Search Tests
- test_hifz_check.py
- Wizard
- .get_surah_length
- Hifz
- _hifz
- Dispatch Order Tests
- _message
- Mini App Plan
- surah_progress
- InMemoryGroupStore
- TestRestartDeliversExactlyOnce
- get_store
- Quran
- _plan_out
- reset_for_tests
- Hifz Seam Tests
- features/check.py
- quran.py
- Hifz Progress: juz_progress
- tick.py
- Profiles: InMemoryProfileStore
- Bundle Translations
- Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd
- BismillahBot — Business Logic
- Streaks: compute_streak
- Groups: PostgresGroupStore
- services/leaderboard.py
- Scheduler Tests
- Layering Tests
- build_grid
- Plan Builder: Portion
- auth.py
- Store Contract Tests
- Multi Platform Plan: MultiPlatform Implementation Plan
- TestStateStore
- Translation editions table (48 codes)
- Profiles: ProfileRow
- parse_offset
- Hifz Seam Tests: TestRegistration
- _bot
- Scheduler Tests: TestTransientFailuresAreRetried
- Store Contract Tests: TestPlans
- .exists
- Plans: PlanDaySpec
- weekly_board
- Refactor — Implementation Plan
- recall_check.py
- ._send_media
- test_store_contract.py
- button_rows
- scheduler/__init__.py
- _plan_drill.py
- stats.py
- send_page
- Store Contract Tests: TestSchedule
- store/__init__.py
- Safety net (characterisation tests, staging smoke, blue-green)
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- features/progress.py
- Export Web Content Tests
- ._load_performers
- UserSettings
- 4. Navigation model
- streak.py
- InMemoryScheduleStore
- PostgresProfileStore
- Mini App Plan: normalize_lang
- Blue Green Ci: jobs
- Blue Green Ci: with
- send_repeated_audio
- test_navigation.py
- .is_cancel
- Mini App Plan: Separate quranayatminiapp Nextjs
- ScheduleStore
- Channel
- test_inline_range.py
- test_keyboard_snapshots.py
- GroupStore
- Store Contract Tests: TestLeaderboard
- TestProfiles
- Business Logic: The hifz platform memorization
- InMemorySessionStore
- week_bounds
- t
- PostgresSessionStore
- button_action
- test_channels_telegram.py
- Hifz Seam Tests: test_hifz_seampy
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- Choice
- .test_concatenates_the_ayahs_in_order
- Blue Green Ci: env
- TestHifzIntervalEdges
- test_wizard.py
- graphify-autopush.sh
- Page Mode Tests
- Scheduler Tests: _at
- Settings Tests
- Store Contract Tests: TestSessions
- Blue Green Ci: postgres
- Blue Green Ci: test
- Blue Green Ci: preflight
- TestLocaleIntegrity
- services/streaks.py
- Hifz Seam Tests: TestPrefixNamespace
- Hifz Seam Tests: TestDispatchCallback
- TestPickerFlow
- missing_keys
- Blue Green Ci: smokegreen
- TranslationRegistry
- _ctx
- File Facade: search_performers
- parse_ayah
- BUSINESS_LOGIC.md
- Verse Card Tests
- BismillahBot README
- 8. Phased task breakdown
- register_send_handler
- features/leaderboard.py
- Blue Green Ci: deploygreen
- Blue Green Ci: promote
- Profile settings reset fix (fix/settings-persistence)
- format_offset
- Hifz Seam Tests: test_longest_prefix_wins
- Scheduler Tests: TestRunScheduler
- test_store_contract.py
- GroupPlanDayRow
- UserSettingsRow
- GroupMemberLink
- Claude
- 11. Infrastructure, capacity and cost on paid Koyeb
- Hifz Seam Tests: TestDispatchCommand
- level_for
- test_the_basmala_heading_is_not_part_of_the_question
- sweep_refs
- Hifz Group Tests: TestRegistration
- test_short_surahs_still_get_four_distinct_options
- _AnyDay
- _isolate_registries
- test_pick_ayah_accepts_anything_with_as_tuple
- test_the_answer_is_not_findable_by_sorting_on_length
- test_sweep_produces_a_well_formed_question_everywhere
- test_options_are_distinct_even_ignoring_vowelling
- test_prompt_is_never_offered_back_as_an_option
- test_correct_option_really_follows_the_prompt
- test_both_question_modes_show_up_in_the_sweep
- test_next_ayah_mode_answers_with_the_whole_short_ayah
- test_long_ayah_prompt_and_options_stay_button_sized
- test_next_ayah_prompt_is_truncated_and_says_so
- test_every_option_carries_the_same_word_count
- test_same_inputs_give_the_same_question
- test_a_different_date_gives_a_different_question
- test_dates_and_iso_strings_are_interchangeable
- test_the_global_random_module_is_never_touched
- test_the_answer_does_not_always_land_in_the_same_slot
- test_the_first_and_last_ayah_of_the_quran
- test_muqattaat_get_muqattaat_shaped_distractors
- test_no_option_carries_a_reference_suffix_or_a_bom
- test_pick_then_build_is_the_whole_check_flow
- test_preload_corpus_returns_the_same_cached_object
- test_correct_option_is_never_a_length_outlier
- test_correct_option_is_never_the_extreme_by_a_wide_ratio

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
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `The seam (`src/hifz/`)` --references--> `handle_update()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/bot/dispatch.py
- `Detection & selection flow` --references--> `handle_update()`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/bot/dispatch.py
- `2. Goals and non-goals` --references--> `handle_update()`  [INFERRED]
  docs/REFACTOR_PLAN.md → src/bot/dispatch.py
- `8. Expected result` --references--> `handle_update()`  [INFERRED]
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

## Communities (284 total, 141 thin omitted)

### Community 0 - "build_plan"
Cohesion: 0.07
Nodes (13): _advance(), auto_pace(), build_plan(), next_scheduled_date(), _validated_days(), surah_ref(), to_day_specs(), TestAcrossTheWholeQuran (+5 more)

### Community 1 - "Quran"
Cohesion: 0.11
Nodes (5): source(), stitch(), page_audio_url(), page_image_url(), TestDivisionsTileTheQuran

### Community 2 - "summarize"
Cohesion: 0.08
Nodes (8): Progress, ProgressSummary, summarize(), SurahProgress, load_summary(), _at(), TestLoadSummary, TestSummarize

### Community 3 - "services/plans.py"
Cohesion: 0.10
Nodes (17): to_utc(), change_status(), complete_day(), current_plan(), day_position(), DrillResult, due_days(), enqueue_next() (+9 more)

### Community 5 - "_plan_setup.py"
Cohesion: 0.13
Nodes (16): memorize(), plan_step(), _ref_from_draft(), _ref_to_draft(), _cancel_row(), _custom_days_keyboard(), _days_keyboard(), _pace_keyboard() (+8 more)

### Community 6 - "reciter.py"
Cohesion: 0.13
Nodes (7): reciter_page_of(), reciter_set_confirmation(), reciter_catalog(), reciter_group(), reciter_kind(), TestCurrentReciter, TestKindWarnings

### Community 7 - "localtime.py"
Cohesion: 0.14
Nodes (8): _as_utc(), local_date(), local_now(), local_time(), next_due_utc(), TestLocalDate, TestNextDueUtc, _utc()

### Community 8 - "Ctx"
Cohesion: 0.10
Nodes (28): Ctx, _begin_setup(), _is_group_admin(), on_group_tap(), on_tap(), _expired(), _know_by_heart(), _lifecycle() (+20 more)

### Community 9 - "Leaderboard"
Cohesion: 0.12
Nodes (10): _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join(), _Message, _sent(), _Settings (+2 more)

### Community 10 - "_ctx"
Cohesion: 0.08
Nodes (17): _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _isolate_registries(), _Message, _profile_row() (+9 more)

### Community 11 - "Profile"
Cohesion: 0.10
Nodes (19): patch_profile(), offset_from_callback(), _plan_line(), profile_view(), reminder_keyboard(), reminder_step(), is_valid_offset(), normalize_offset() (+11 more)

### Community 12 - "Store"
Cohesion: 0.08
Nodes (12): _CallbackQuery, _ctx(), _isolate_registries(), _Message, _run_wizard(), _Settings, _tap(), TestDrill (+4 more)

### Community 13 - "render_streak_graph"
Cohesion: 0.14
Nodes (7): render(), draw_contribution_graph(), render_streak_graph(), _semaphore(), open_png(), TestRendering, TestRenderStreakGraph

### Community 14 - "services/streaks.py"
Cohesion: 0.25
Nodes (4): refresh_streaks(), streak_summary(), user_today(), TestRefreshAndSummary

### Community 15 - "User Settings"
Cohesion: 0.22
Nodes (4): _legacy_lang_key(), SettingsRow, TestIndependence, TestRoundTrip

### Community 16 - "Context"
Cohesion: 0.14
Nodes (15): _bot(), _ctx(), _isolate_registries(), _member(), _run_setup_to_plan(), _Settings, TestBoard, tap() (+7 more)

### Community 17 - "Health"
Cohesion: 0.07
Nodes (14): health(), database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries(), fresh_redis(), _Reachable (+6 more)

### Community 18 - "Refs"
Cohesion: 0.06
Nodes (14): _clean(), format_ref(), juz_ref(), parse_range(), parse_reference(), test_page_boundaries_match_the_bot(), TestSurahSpans, TestAcrossSurahs (+6 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.10
Nodes (10): 6. Issues fixed in this refactor, Module responsibilities, get(), _key(), save(), get(), _key(), take() (+2 more)

### Community 20 - "typing"
Cohesion: 0.04
Nodes (30): 11.1 Profile settings reset after a while — `fix/settings-persistence`, Phase 1 — Take `main.py` apart (pure moves) — *done*, create_app(), build_data(), _commands_for(), initialize(), lifespan(), _set_bot_commands() (+22 more)

### Community 21 - "Router"
Cohesion: 0.07
Nodes (18): Phase 3 — One router for everything — *done*, _on_callback(), _on_text(), ctx(), _search_reciters(), decorate(), dispatch_callback(), dispatch_command() (+10 more)

### Community 22 - "IdentityStore"
Cohesion: 0.06
Nodes (5): IdentityRow, IdentityStore, InMemoryIdentityStore, PostgresIdentityStore, _stored()

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "Group"
Cohesion: 0.09
Nodes (21): bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), _enqueue_next_board(), _enqueue_next_group(), group_board_entries() (+13 more)

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.13
Nodes (15): 10. Found along the way (out of scope — behaviour changes), 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, 2. Goals and non-goals, 3. Principles applied, 6. Ordering, risk, size, 7. Safety net, 8. Expected result (+7 more)

### Community 26 - "TelegramChannel"
Cohesion: 0.12
Nodes (5): TelegramChannel, TestAnswerAndTyping, TestEditChoices, TestEditText, TestMedia

### Community 27 - "Hifz Streak Tests"
Cohesion: 0.17
Nodes (7): _caption(), _earn(), _streak(), TestGraphCache, TestMilestones, TestStreakCard, TestWhatTicksADay

### Community 28 - "Hifz Platform"
Cohesion: 0.07
Nodes (29): Hifz Platform - Plan & Progress, Phase 1 acceptance criteria (tests/test_acceptance.py), Hifz change log, claim_due claimed_at clock bug, Hifz data model (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send, group_*), Phase 2 group cluster (J1-J6, forum topics), Workstream I: i18n & commands for 48 locales, Workstream C: interval merge-on-insert + derived percentages (+21 more)

### Community 29 - "Acceptance Tests"
Cohesion: 0.10
Nodes (14): _CallbackQuery, _cmd(), _ctx(), _isolate_registries(), _Message, _run_wizard(), _save_plan(), _Settings (+6 more)

### Community 30 - "Hifz Progress: quran_page_progress"
Cohesion: 0.09
Nodes (5): juz_page_progress(), PageProgress, quran_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 32 - "test_page_mode.py"
Cohesion: 0.13
Nodes (7): deliver_page_audio(), send_page_audio(), data(), fake_bot(), TestPageAudio, TestStitchedAudioAcrossSurahs, tg_bot()

### Community 33 - "test_recall_check.py"
Cohesion: 0.15
Nodes (4): test_options_need_no_html_escaping_beyond_the_callers(), test_pick_ayah_is_deterministic_per_user_and_date(), test_pick_ayah_on_an_inverted_or_empty_span(), test_unknown_ayahs_are_rejected()

### Community 34 - "TranslationRegistry"
Cohesion: 0.08
Nodes (5): TestCorpusIntegrity, TestAvailable, TestCaching, TestFallback, TestTransliteration

### Community 35 - "Auth"
Cohesion: 0.12
Nodes (23): _init_data_secret(), InvalidInitData, sign_init_data(), validate_init_data(), _auth(), _fields(), _jwt_secret(), test_added_field_is_rejected() (+15 more)

### Community 36 - "File"
Cohesion: 0.12
Nodes (3): File, TestLegacyLanguageKey, TestCoexistsWithTheReciterFlow

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.09
Nodes (23): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 1. Terminology (so the report language is right), 2. What "correct" can mean — error taxonomy, 3.1 Commercial, 3.2 Open models and data, 3.3 Reference *text* per riwāyah (+15 more)

### Community 38 - "round_percent"
Cohesion: 0.10
Nodes (4): format_percent(), _Ratio, round_percent(), TestRounding

### Community 39 - "ScheduledSend"
Cohesion: 0.12
Nodes (4): enqueue(), idempotency_key(), schedule_daily(), ScheduledSend

### Community 40 - "telegram"
Cohesion: 0.04
Nodes (32): _stress_reset(), _stress_stats(), page_keyboard(), verse_keyboard(), app_choice_row(), app_url(), set_menu_button(), to_button() (+24 more)

### Community 41 - "Session"
Cohesion: 0.14
Nodes (18): init_data_max_age(), auth_telegram(), AuthOut, me(), _me(), MeOut, patch_settings(), PlanSummary (+10 more)

### Community 42 - "Plans: PlanStore"
Cohesion: 0.06
Nodes (4): InMemoryPlanStore, PlanDayRow, PlanRow, PlanStore

### Community 43 - "Ref"
Cohesion: 0.08
Nodes (15): _clip(), _covered(), _focus_surah(), _intersect(), _page_share(), _pages_of(), _recency_key(), _surah_of() (+7 more)

### Community 45 - "Streaks"
Cohesion: 0.13
Nodes (4): record_session(), TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 46 - "Load Test"
Cohesion: 0.14
Nodes (12): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+4 more)

### Community 47 - "Multilingual Plan"
Cohesion: 0.19
Nodes (12): Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), Quran.from_file(path) refactor, setMyCommands per language, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+4 more)

### Community 48 - "Text"
Cohesion: 0.22
Nodes (6): _inline_query(), _of_type(), _results(), TestInlineArabicImage, TestRangeAudio, TestRangeText

### Community 49 - "Schema"
Cohesion: 0.11
Nodes (26): group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval, hifz_interval_user_surah_idx (+18 more)

### Community 50 - "Services"
Cohesion: 0.14
Nodes (20): client(), _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today() (+12 more)

### Community 51 - "api/plans.py"
Cohesion: 0.06
Nodes (44): jwt_secret(), require_user(), answer(), AnswerIn, AnswerOut, make_token(), question(), QuestionOut (+36 more)

### Community 52 - "Dispatch"
Cohesion: 0.16
Nodes (18): _callback(), data(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index(), test_inline_query_valid_ayah_returns_all_four_views() (+10 more)

### Community 53 - "reciter_keyboard"
Cohesion: 0.13
Nodes (8): reciter_keyboard(), reciter_label(), reciter_page_count(), reciter_search_keyboard(), _pager_row(), _reciter_buttons(), TestLabels, TestPagination

### Community 54 - "advancing"
Cohesion: 0.09
Nodes (7): advancing(), assert_covers_target_once(), assert_well_formed(), spans(), TestAlMulkAcceptance, TestCrossSurahTargets, TestSmallAndAwkwardTargets

### Community 55 - "Inline Reciter Search Tests"
Cohesion: 0.14
Nodes (21): handle_update(), _incoming(), _audio_result(), data(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter() (+13 more)

### Community 56 - "test_hifz_check.py"
Cohesion: 0.13
Nodes (13): _answer_data(), _ask(), _asked(), _buttons(), _callback_query(), _ctx(), _sessions(), _Settings (+5 more)

### Community 58 - ".get_surah_length"
Cohesion: 0.13
Nodes (4): _neighbours(), ayah_count(), TestAyahCount, TestNavigation

### Community 59 - "Hifz"
Cohesion: 0.07
Nodes (10): _covers(), HifzStore, InMemoryHifzStore, _merge_span(), _normalize(), _overlaps(), PostgresHifzStore, _split_span() (+2 more)

### Community 60 - "_hifz"
Cohesion: 0.06
Nodes (11): HifzInterval, _assert_invariant(), _ayahs(), _hifz(), _spans(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order() (+3 more)

### Community 61 - "Dispatch Order Tests"
Cohesion: 0.18
Nodes (17): _callback(), data(), fake_bot(), _message(), probe(), _sent_a_verse(), test_a_command_beats_a_pending_reciter_search(), test_a_command_escapes_a_wizard_without_ending_it() (+9 more)

### Community 62 - "_message"
Cohesion: 0.17
Nodes (3): _message(), TestPageCommand, TestSajdaCommand

### Community 63 - "Mini App Plan"
Cohesion: 0.14
Nodes (14): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 6. Frontend structure (`quranayat-miniapp`), 7. Bot ↔ Mini App integration (+6 more)

### Community 65 - "surah_progress"
Cohesion: 0.11
Nodes (5): started_surahs(), surah_progress(), TestInputHandling, TestSpecAcceptance, TestSurahProgress

### Community 68 - "get_store"
Cohesion: 0.16
Nodes (6): get_store(), _lock(), TestFourProgress, _added_update(), TestAdded, TestDailyPost

### Community 69 - "Quran"
Cohesion: 0.06
Nodes (15): nav_labels(), page_caption(), _division_marks(), get_translation(), parse_quran_tafsir(), Quran, _load_locales(), missing_locales() (+7 more)

### Community 70 - "_plan_out"
Cohesion: 0.16
Nodes (9): active(), create(), lifecycle(), _plan_out(), PlanOut, today(), plan_ref(), portions_of() (+1 more)

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 73 - "features/check.py"
Cohesion: 0.08
Nodes (15): _answer_data(), _ask(), check(), on_check(), _options_keyboard(), _parse_answer(), _question_text(), _score() (+7 more)

### Community 74 - "quran.py"
Cohesion: 0.05
Nodes (27): handle_incoming(), random_ayah(), read_text(), repeat(), _send_verse(), verse_card(), answer_inline_query(), inline_audio_result() (+19 more)

### Community 75 - "Hifz Progress: juz_progress"
Cohesion: 0.11
Nodes (7): juz_progress(), JuzProgress, quran_progress(), _spans(), started_juzs(), TestJuzProgress, TestQuranProgress

### Community 76 - "tick.py"
Cohesion: 0.18
Nodes (8): _deliver(), _is_stale(), _lock(), _release(), _resolve(), _tick(), TickResult, _utcnow()

### Community 78 - "Bundle Translations"
Cohesion: 0.13
Nodes (14): bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file(), export() (+6 more)

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.13
Nodes (16): Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points), Error taxonomy L1-L5 (word, harakah, tajwid, riwayah mismatch, waqf), Evaluation plan (false-alarm gate < 2% per ayah), IqraEval 2025 shared task, Recitation checker phased roadmap (A-1 to E) (+8 more)

### Community 80 - "BismillahBot — Business Logic"
Cohesion: 0.11
Nodes (14): 1. Overview, 2. Architecture, 3. Request lifecycle, 5. Caching strategy, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic, Local time (+6 more)

### Community 81 - "Streaks: compute_streak"
Cohesion: 0.24
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 83 - "services/leaderboard.py"
Cohesion: 0.08
Nodes (7): LeaderboardEntry, SessionRow, user_week_window(), week_window(), WeeklyBoard, user_offset(), TestWeekWindow

### Community 84 - "Scheduler Tests"
Cohesion: 0.17
Nodes (4): _claimed_at(), _record(), TestCatchUp, TestTick

### Community 85 - "Layering Tests"
Cohesion: 0.10
Nodes (18): _clean_state_store(), build_meta(), export(), main(), _spans(), split_basmalah(), _write(), _absolute_imports() (+10 more)

### Community 86 - "build_grid"
Cohesion: 0.18
Nodes (4): build_grid(), _counts(), Grid, TestGrid

### Community 87 - "Plan Builder: Portion"
Cohesion: 0.17
Nodes (4): Portion, match_portion(), portion_for(), TestPortionShape

### Community 89 - "auth.py"
Cohesion: 0.18
Nodes (12): _b64url(), _b64url_decode(), decode_token(), InvalidToken, issue_token(), _sign(), _unauthorized(), test_expired_token_is_rejected() (+4 more)

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.08
Nodes (24): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+16 more)

### Community 92 - "TestStateStore"
Cohesion: 0.12
Nodes (3): TestAudioFilename, TestImageFilename, TestStateStore

### Community 93 - "Translation editions table (48 codes)"
Cohesion: 0.29
Nodes (6): Translation Attributions, alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Locale review tracking table (47 locales)

### Community 95 - "parse_offset"
Cohesion: 0.15
Nodes (3): parse_offset(), TestParseOffset, TestPicker

### Community 97 - "_bot"
Cohesion: 0.38
Nodes (5): _bot(), _next_id(), send_audio(), send_photo(), test_a_rejected_cached_id_is_rebuilt_and_recached()

### Community 100 - ".exists"
Cohesion: 0.08
Nodes (16): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, put_position(), ReaderPosition, Reciter (+8 more)

### Community 102 - "weekly_board"
Cohesion: 0.28
Nodes (3): weekly_board(), make_user(), TestWeeklyBoard

### Community 103 - "Refactor — Implementation Plan"
Cohesion: 0.22
Nodes (8): tests/test_layering.py ratchet (KNOWN violations), Overlap with MULTI_PLATFORM_PLAN channel seam, Decisions and open questions (§9), Phase 0 — Guardrails (ruff, layering test, logging), Phase 5 — Fix the layering, Target layout (app/ bot/ services/ domain/ infra/), Timezone picker by country (feat/timezone-by-country), Memorizing (hifz): /memorize, /check, /progress, /streak, /leaderboard, /profile

### Community 104 - "recall_check.py"
Cohesion: 0.06
Nodes (28): _assemble(), _at_offset(), _ayah_text(), _basmala_prefix(), build_question(), _clean(), _continuation_question(), corpus() (+20 more)

### Community 105 - "._send_media"
Cohesion: 0.15
Nodes (3): _build(), ignore_not_modified(), build()

### Community 107 - "button_rows"
Cohesion: 0.14
Nodes (13): button_rows(), offset_keyboard(), offset_options(), test_a_non_positive_width_is_one_per_row(), test_an_exact_fit_has_no_empty_trailing_row(), test_nothing_in_nothing_out(), test_packs_in_order_with_a_short_last_row(), _grid() (+5 more)

### Community 108 - "scheduler/__init__.py"
Cohesion: 0.22
Nodes (5): registered_kinds(), catch_up(), run_scheduler(), _wait(), tick()

### Community 109 - "_plan_drill.py"
Cohesion: 0.07
Nodes (23): 1. Why, 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 2 — DRY the duplicated patterns — *done*, Phase 5 — Fix the layering — *done*, Phase 6 — Repository hygiene — *done*, _post_portion(), push_group_day() (+15 more)

### Community 110 - "stats.py"
Cohesion: 0.35
Nodes (8): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut

### Community 111 - "send_page"
Cohesion: 0.29
Nodes (7): send_page(), _buffer(), _stub_stitch(), stub(), TestPageCard, capture(), counting()

### Community 113 - "store/__init__.py"
Cohesion: 0.08
Nodes (9): Caps, Incoming, store_backend(), SessionStore, MemoryState, _isolate_registries(), _isolate_handlers(), state() (+1 more)

### Community 114 - "Safety net (characterisation tests, staging smoke, blue-green)"
Cohesion: 0.12
Nodes (13): graphify knowledge graph (graphify-out/), CLAUDE.md graphify lookup rules, button_rows() row-packing helper, Copy-pasted patterns table (§1.3), GET / health with store and cache status (503), ignore_not_modified() context manager, Shared UTC offset picker (time_pickers.offset_keyboard), Found along the way (out-of-scope behaviour changes) (+5 more)

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
Cohesion: 0.18
Nodes (8): forgot_command(), on_progress_tap(), progress_command(), progress_view(), _show(), _surah_line(), surah_spans(), unmark()

### Community 119 - "Export Web Content Tests"
Cohesion: 0.14
Nodes (10): _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl(), _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah() (+2 more)

### Community 120 - "._load_performers"
Cohesion: 0.15
Nodes (3): Phase 4 — Split infrastructure god-objects — *done*, TestCatalogKinds, TestCatalogOrder

### Community 121 - "UserSettings"
Cohesion: 0.13
Nodes (6): UserSettings, _seed_legacy_lang(), TestDefaults, TestInlineCaller, TestKeyedByUserId, TestLegacyMigration

### Community 122 - "4. Navigation model"
Cohesion: 0.29
Nodes (8): 4. Navigation model, Audio catalog kinds, Page images and page audio, Repeat (memorization), Structural divisions (page / juz / sajda), Translation-only catalogue entries, Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES), Mini App feature parity map

### Community 123 - "streak.py"
Cohesion: 0.14
Nodes (10): _caption(), _keyboard(), on_streak(), _send_graph(), streak(), cache_key(), _send(), send_cached() (+2 more)

### Community 125 - "PostgresProfileStore"
Cohesion: 0.05
Nodes (5): PostgresStore, PostgresPlanStore, PostgresProfileStore, PostgresScheduleStore, store()

### Community 126 - "Mini App Plan: normalize_lang"
Cohesion: 0.22
Nodes (6): 4.1 Flow, 4.2 Rules, 4.3 Transport, 4. Authentication, normalize_lang(), TestNormalizeLang

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
Cohesion: 0.11
Nodes (8): parse_ayah_range(), data(), fake_bot(), _no_network(), TestCommandArguments, TestJuzCommand, tg_bot(), TestParseAyahRange

### Community 132 - "Mini App Plan: Separate quranayatminiapp Nextjs"
Cohesion: 0.16
Nodes (12): Inline query answering (all four representations, ranges), Navigation model ((surah, ayah, type) per chat_id), Page audio with stitched fallback, Page image stitching (lib/page_image.py), Structural divisions (page / juz / sajda from quran-data.xml), Uthmani text in Amiri Quran / KFGQPC font, Client-side playlist audio (no server stitching), Locale export to JSON (web_ keys, next-intl) (+4 more)

### Community 135 - "test_inline_range.py"
Cohesion: 0.06
Nodes (16): range_audio(), stitch(), download_combined_audio(), download_stitched_audio(), fetch_and_stitch(), _fit_for_telegram(), _semaphore(), stitch_images() (+8 more)

### Community 136 - "test_keyboard_snapshots.py"
Cohesion: 0.25
Nodes (5): _as_dict(), _keyboards(), _render(), _search_markup(), test_keyboards_match_their_snapshots()

### Community 137 - "GroupStore"
Cohesion: 0.12
Nodes (3): GroupConfig, GroupPlanRow, GroupStore

### Community 140 - "Business Logic: The hifz platform memorization"
Cohesion: 0.09
Nodes (25): Central callback prefix allocation (hifz.PREFIXES), Future roadmap and prioritized backlog, The hifz platform (memorization companion), Pure plan builder (build_plan), Streak day ticks on completed session, /api/v1 REST surface, Bot ↔ Mini App integration (menu button, startapp, /app), initData HMAC validation → short-lived JWT (+17 more)

### Community 143 - "t"
Cohesion: 0.06
Nodes (40): command, Routing rules (in `serve`), 5. API surface (`/api/v1`), Phase 2 — WhatsApp MVP (reader + daily ayat), 7. The keyboard & command localization challenge, Telegram command menu, 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering (+32 more)

### Community 145 - "button_action"
Cohesion: 0.27
Nodes (3): button_action(), _reverse_button_map(), TestButtonAction

### Community 146 - "test_channels_telegram.py"
Cohesion: 0.15
Nodes (5): for_platform(), bot(), cache(), TestChoice, TestForPlatform

### Community 148 - "Hifz Seam Tests: test_hifz_seampy"
Cohesion: 0.18
Nodes (3): _isolate_registries(), _Settings, TestSchemaApplication

### Community 152 - "Choice"
Cohesion: 0.25
Nodes (3): mode_button(), Choice, TestSendText

### Community 153 - ".test_concatenates_the_ayahs_in_order"
Cohesion: 0.18
Nodes (4): content(), fake_download(), TestStitching, __init__()

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 156 - "test_wizard.py"
Cohesion: 0.18
Nodes (3): test_draft_is_written_with_that_ttl(), TestOneDraftPerUser, wiz()

### Community 162 - "Blue Green Ci: postgres"
Cohesion: 0.22
Nodes (9): POSTGRES_DB, POSTGRES_HOST_AUTH_METHOD, POSTGRES_USER, env, image, options, ports, postgres (+1 more)

### Community 163 - "Blue Green Ci: test"
Cohesion: 0.22
Nodes (9): TEST_DATABASE_URL, test, python-version, fail-fast, matrix, env, name, runs-on (+1 more)

### Community 164 - "Blue Green Ci: preflight"
Cohesion: 0.22
Nodes (9): preflight, active, deploy_enabled, target, if, name, needs, outputs (+1 more)

### Community 165 - "TestLocaleIntegrity"
Cohesion: 0.20
Nodes (3): keyboard_rows(), _placeholders(), TestLocaleIntegrity

### Community 166 - "services/streaks.py"
Cohesion: 0.11
Nodes (9): Milestone, milestone_for(), _milestone_key(), offset_of(), percentile_band(), StreakCounts, SessionOutcome, TestMilestones (+1 more)

### Community 169 - "TestPickerFlow"
Cohesion: 0.17
Nodes (5): _callback(), _message(), _tab_row(), TestAudioNeverFollowsLanguage, TestPickerFlow

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 172 - "TranslationRegistry"
Cohesion: 0.12
Nodes (9): 7. Known limitations / tech debt, 10. File-by-file change list, 12. Testing, 3. Target architecture, 5. Content: multi-translation loading (memory-aware), Translation catalogue (initial set), What's covered, parse_quran() (+1 more)

### Community 173 - "_ctx"
Cohesion: 0.24
Nodes (4): _ctx(), _photo_message(), _Settings, TestCallback

### Community 176 - "BUSINESS_LOGIC.md"
Cohesion: 0.29
Nodes (4): Four ayah representations (english, tafsir, arabic, audio), Known limitations / tech debt, Issues fixed in the refactor (12 bugs), Verse card (inline keyboard, edit in place)

### Community 178 - "BismillahBot README"
Cohesion: 0.09
Nodes (23): 11. Memory & performance (free-tier reality), 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 2. Current-state audit (what is hardcoded English), 4. User language preference, 6. UI internationalization (i18n), 8. Tafsir & audio (later dimensions) (+15 more)

### Community 179 - "8. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 8. Phased task breakdown, Phase 0 — Foundations, Phase 1 — Service-layer extraction (this repo, no UI change), Phase 2 — Reader parity (read-only, low risk, ships first), Phase 3 — Hifz parity, Phase 4 — Recitation checker UI (depends on the investigation's Phase A), Phase 5 — Later

### Community 180 - "register_send_handler"
Cohesion: 0.29
Nodes (3): register_send_handler(), _same_origin(), decorate()

### Community 181 - "features/leaderboard.py"
Cohesion: 0.38
Nodes (3): _board_message(), leaderboard(), on_leaderboard()

### Community 182 - "Blue Green Ci: deploygreen"
Cohesion: 0.33
Nodes (6): environment, if, name, needs, runs-on, deploy-green

### Community 183 - "Blue Green Ci: promote"
Cohesion: 0.33
Nodes (6): promote, environment, if, name, needs, runs-on

### Community 184 - "Profile settings reset fix (fix/settings-persistence)"
Cohesion: 0.29
Nodes (8): ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable, lib/utils.File god class, Silent in-memory store fallback, Phase 4 — Split infrastructure god-objects, Profile settings reset fix (fix/settings-persistence), Typed frozen Settings (config/settings.py), conftest.py test environment (src on path, CWD pin, no Redis/network), Environment configuration (webhook, CDN base URLs, Redis)

### Community 193 - "11. Infrastructure, capacity and cost on paid Koyeb"
Cohesion: 0.33
Nodes (6): 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards, 11. Infrastructure, capacity and cost on paid Koyeb

## Knowledge Gaps
- **51 isolated node(s):** `Found along the way (out-of-scope behaviour changes)`, `Phase 0 — Guardrails (ruff, layering test, logging)`, `button_rows() row-packing helper`, `ignore_not_modified() context manager`, `CLAUDE.md graphify lookup rules` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1574 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **141 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `get_store` to `summarize`, `ScheduleStore`, `Leaderboard`, `_ctx`, `Profile`, `Store`, `render_streak_graph`, `services/streaks.py`, `t`, `Context`, `User Settings`, `RedisSingleton`, `typing`, `Hifz Progress Cmd Tests`, `Hifz Streak Tests`, `Acceptance Tests`, `services/streaks.py`, `Session`, `Streaks`, `Services`, `api/plans.py`, `Inline Reciter Search Tests`, `test_hifz_check.py`, `_hifz`, `surah_progress`, `_plan_out`, `quran.py`, `tick.py`, `services/leaderboard.py`, `weekly_board`, `scheduler/__init__.py`, `stats.py`, `store/__init__.py`, `InMemoryScheduleStore`, `PostgresProfileStore`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Found along the way (out-of-scope behaviour changes)`, `Phase 0 — Guardrails (ruff, layering test, logging)`, `button_rows() row-packing helper` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_plan` be split into smaller, more focused modules?**
  _Cohesion score 0.06554019457245264 - nodes in this community are weakly interconnected._
- **Why does `Quran` connect `Quran` to `build_plan`, `Quran`, `summarize`, `services/plans.py`, `test_navigation.py`, `test_inline_range.py`, `Profile`, `t`, `Refs`, `RedisSingleton`, `typing`, `Hifz Progress Cmd Tests`, `Hifz Progress: quran_page_progress`, `TranslationRegistry`, `Ref`, `TranslationRegistry`, `api/plans.py`, `advancing`, `.get_surah_length`, `_message`, `surah_progress`, `_plan_out`, `sweep_refs`, `test_short_surahs_still_get_four_distinct_options`, `features/check.py`, `quran.py`, `Hifz Progress: juz_progress`, `Layering Tests`, `.exists`, `recall_check.py`, `_plan_drill.py`, `features/progress.py`, `Export Web Content Tests`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Ctx` (e.g. with `3. Architecture` and `4.1 Overlap with `MULTI_PLATFORM_PLAN.md``) actually correct?**
  _`Ctx` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Should `Quran` be split into smaller, more focused modules?**
  _Cohesion score 0.11462450592885376 - nodes in this community are weakly interconnected._