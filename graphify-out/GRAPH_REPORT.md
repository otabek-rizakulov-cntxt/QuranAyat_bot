# Graph Report - QuranAyat_bot  (2026-11-02)

## Corpus Check
- 272 files · ~259,441 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 5055 nodes · 11634 edges · 318 communities (151 shown, 167 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 991 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `10433a72`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_plan
- link_token.py
- language.py
- SendCtx
- Wizard
- _plan_setup.py
- features/profile.py
- next_due_utc
- to_whatsapp
- _ctx
- _ctx
- services/plans.py
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
- t
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
- Phase 1 — Take `main.py` apart (pure moves) — *done*
- _plan_preview.py
- Recitation Checker Investigation
- hifz_progress.py
- test_whatsapp_webhook.py
- to_markup
- session.py
- PostgresPlanStore
- quran_page_progress
- test_hifz_cross_platform.py
- Streaks
- Load Test
- Multilingual Plan
- Text
- Schema
- Services
- api/progress.py
- Dispatch
- PlanDaySpec
- PostgresProfileStore
- Inline Reciter Search Tests
- test_hifz_check.py
- deliver_push
- test_service_layer.py
- PostgresScheduleStore
- test_hifz_keyboard_snapshots.py
- Dispatch Order Tests
- taps
- Mini App Plan
- services/check.py
- check_locales.py
- hifz_progress.py
- features/leaderboard.py
- weekly_board
- api/catalog.py
- reset_for_tests
- Hifz Seam Tests
- Ref
- router.py
- Phase 2 — DRY the duplicated patterns
- tick.py
- Profiles: InMemoryProfileStore
- os
- Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd
- BismillahBot — Business Logic
- Streaks: compute_streak
- Groups: PostgresGroupStore
- SessionStore
- Scheduler Tests
- export
- whatsapp_format.py
- _clip
- auth.py
- Store Contract Tests
- Multi Platform Plan: MultiPlatform Implementation Plan
- dispatch.py
- _hifz
- Dependency rule (app -> bot -> services -> domain)
- handle_message
- Hifz Seam Tests: TestRegistration
- InMemoryPlanStore
- Scheduler Tests: TestTransientFailuresAreRetried
- Store Contract Tests: TestPlans
- GraphClient
- TestStateStore
- _at
- week_bounds
- recall_check.py
- services/streaks.py
- test_store_contract.py
- test_daily_feature.py
- welcome_text
- button_rows
- stats.py
- send_page
- TestSchedule
- store/__init__.py
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- .get_next_ayah
- parse_ayah
- ._load_performers
- refresh_streaks
- button_action
- streak.py
- Quran
- 4. Navigation model
- TestHelpers
- Blue Green Ci: jobs
- Blue Green Ci: with
- build_grid
- test_navigation.py
- test_page_mode.py
- Mini App Plan: Separate quranayatminiapp Nextjs
- InMemoryScheduleStore
- Channel
- range_audio
- download_stitched_audio
- InMemoryGroupStore
- Store Contract Tests: TestLeaderboard
- parse_ayah_range
- MINI_APP_PLAN.md
- re
- TestRestartDeliversExactlyOnce
- Ctx
- locales/__init__.py
- normalize_lang
- percentile_band
- .test_full_flow_queues_the_first_send
- TestDispatchWizard
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- split
- test_layering.py
- Blue Green Ci: env
- test_channels_whatsapp.py
- TestProfiles
- graphify-autopush.sh
- Profile settings reset fix (fix/settings-persistence)
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
- unittest_mock
- TestRunScheduler
- BismillahBot README
- page_keyboard
- ayah_for
- Blue Green Ci: deploygreen
- Blue Green Ci: promote
- Choices
- TestHifzIntervalEdges
- Hifz Seam Tests: test_longest_prefix_wins
- .get_surah_length
- TestIdentity
- Claude
- WhatsApp
- send_repeated_audio
- Hifz Seam Tests: TestDispatchCommand
- 8. Phased task breakdown
- offset_options
- send_page_audio
- Translation editions table (48 codes)
- Testing & CI
- 11. Infrastructure, capacity and cost on paid Koyeb
- TestTransport
- .test_sends_todays_ayah_and_queues_tomorrow
- graph
- test_the_basmala_heading_is_not_part_of_the_question
- sweep_refs
- test_short_surahs_still_get_four_distinct_options
- _AnyDay
- PostgresDailyStore
- _isolate_registries
- test_pick_ayah_accepts_anything_with_as_tuple
- test_media_cache_keys.py
- Incoming
- get_store
- features/daily.py
- test_the_answer_is_not_findable_by_sorting_on_length
- test_sweep_produces_a_well_formed_question_everywhere
- test_options_are_distinct_even_ignoring_vowelling
- reciter_set_confirmation
- test_prompt_is_never_offered_back_as_an_option
- test_correct_option_really_follows_the_prompt
- TestSettings
- test_both_question_modes_show_up_in_the_sweep
- bot/whatsapp.py
- test_next_ayah_mode_answers_with_the_whole_short_ayah
- test_long_ayah_prompt_and_options_stay_button_sized
- test_next_ayah_prompt_is_truncated_and_says_so
- Graph
- test_every_option_carries_the_same_word_count
- level_for
- Graph
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
1. `get_store()` - 168 edges
2. `Ctx` - 129 edges
3. `t()` - 120 edges
4. `Quran` - 118 edges
5. `handle_update()` - 93 edges
6. `UserSettings` - 79 edges
7. `build_plan()` - 72 edges
8. `parse_reference()` - 59 edges
9. `TelegramChannel` - 58 edges
10. `Ref` - 57 edges

## Surprising Connections (you probably didn't know these)
- `3. Target architecture` --references--> `TranslationRegistry`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/domain/quran.py
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `Prioritized backlog` --references--> `parse_ayah()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/domain/parsing.py
- `Translation-only catalogue entries` --references--> `normalize_lang()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/locales/languages.py
- `Translation catalogue (initial set)` --references--> `parse_quran()`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/domain/quran.py

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

## Communities (318 total, 167 thin omitted)

### Community 0 - "build_plan"
Cohesion: 0.04
Nodes (21): _advance(), advancing(), auto_pace(), build_plan(), next_scheduled_date(), _validated_days(), juz_ref(), surah_ref() (+13 more)

### Community 1 - "link_token.py"
Cohesion: 0.10
Nodes (13): _b64url_decode(), _b64(), InvalidLinkToken, issue(), _key(), redeem(), _secret(), _unb64() (+5 more)

### Community 2 - "language.py"
Cohesion: 0.09
Nodes (8): Phase 2 — DRY the duplicated patterns — *done*, language_keyboard(), language_picker(), translation_language_keyboard(), missing_locales(), TestAvailable, TestTransliteration, TestLanguageFlags

### Community 3 - "SendCtx"
Cohesion: 0.11
Nodes (6): _send_plain_message(), register_send_handler(), registered_kinds(), _same_origin(), decorate(), SendCtx

### Community 4 - "Wizard"
Cohesion: 0.06
Nodes (10): ctx(), Wizard, test_draft_is_written_with_that_ttl(), TestAccumulation, TestCancel, TestCoexistsWithTheReciterFlow, TestCorruptState, TestLifecycle (+2 more)

### Community 5 - "_plan_setup.py"
Cohesion: 0.06
Nodes (40): memorize(), on_tap(), plan_step(), _expired(), _ref_from_draft(), _ref_to_draft(), _know_by_heart(), _send_drill() (+32 more)

### Community 6 - "features/profile.py"
Cohesion: 0.07
Nodes (28): create(), patch_profile(), _profile(), _cancel_keyboard(), _join_board(), name_step(), offset_from_callback(), on_profile_tap() (+20 more)

### Community 7 - "next_due_utc"
Cohesion: 0.06
Nodes (14): _as_utc(), format_offset(), local_date(), local_now(), local_time(), next_due_utc(), parse_offset(), to_utc() (+6 more)

### Community 8 - "to_whatsapp"
Cohesion: 0.16
Nodes (3): to_whatsapp(), TestTags, TestWhatTheBotSends

### Community 9 - "_ctx"
Cohesion: 0.12
Nodes (10): _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join(), _Message, _sent(), _Settings (+2 more)

### Community 10 - "_ctx"
Cohesion: 0.08
Nodes (17): _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _isolate_registries(), _Message, _profile_row() (+9 more)

### Community 11 - "services/plans.py"
Cohesion: 0.08
Nodes (24): active(), lifecycle(), _plan_out(), today(), change_status(), complete_day(), current_plan(), day_position() (+16 more)

### Community 12 - "Store"
Cohesion: 0.09
Nodes (11): _CallbackQuery, _ctx(), _Message, _run_wizard(), _Settings, _tap(), TestDrill, TestEnqueueChain (+3 more)

### Community 13 - "render_streak_graph"
Cohesion: 0.13
Nodes (8): render(), draw_contribution_graph(), render_streak_graph(), _semaphore(), open_png(), TestCacheKey, TestRendering, TestRenderStreakGraph

### Community 14 - "get_settings"
Cohesion: 0.09
Nodes (12): _flag(), get_settings(), Settings, DatabaseUnavailable, get_pool(), _lock(), create_bot(), env() (+4 more)

### Community 15 - "UserSettings"
Cohesion: 0.10
Nodes (13): patch_settings(), _unprocessable(), resolve_settings(), _legacy_lang_key(), SettingsRow, UserSettings, _seed_legacy_lang(), TestDefaults (+5 more)

### Community 16 - "Context"
Cohesion: 0.12
Nodes (16): _bot(), _ctx(), _isolate_registries(), _member(), _run_setup_to_plan(), _Settings, TestBoard, tap() (+8 more)

### Community 17 - "test_store_selection.py"
Cohesion: 0.07
Nodes (15): health(), store_backend(), database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries(), fresh_redis() (+7 more)

### Community 18 - "Refs"
Cohesion: 0.07
Nodes (11): _clean(), format_ref(), parse_range(), parse_reference(), TestSurahSpans, TestAcrossSurahs, TestFormatting, TestJuzAndPage (+3 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.09
Nodes (11): 6. Issues fixed in this refactor, forget(), _key(), pick(), remember(), get(), _key(), save() (+3 more)

### Community 20 - "lifespan.py"
Cohesion: 0.05
Nodes (22): _commands_for(), initialize(), lifespan(), _set_bot_commands(), _process_update(), telegram_webhook(), webhook_secret(), _first_delivery() (+14 more)

### Community 21 - "WhatsAppChannel"
Cohesion: 0.16
Nodes (5): _bytes_and_name(), _clip(), _resolve(), _split_choices(), WhatsAppChannel

### Community 22 - "IdentityStore"
Cohesion: 0.06
Nodes (5): IdentityRow, IdentityStore, InMemoryIdentityStore, PostgresIdentityStore, _stored()

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "t"
Cohesion: 0.08
Nodes (21): 7. The keyboard & command localization challenge, Telegram command menu, bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), _enqueue_next_board() (+13 more)

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.15
Nodes (13): 10. Found along the way (out of scope — behaviour changes), 2. Goals and non-goals, 3. Principles applied, 6. Ordering, risk, size, 7. Safety net, 8. Expected result, 9. Decisions and open questions, Expected result metrics (§8) (+5 more)

### Community 26 - "TelegramChannel"
Cohesion: 0.10
Nodes (6): TelegramChannel, TestAnswerAndTyping, TestEditChoices, TestEditText, TestMedia, TestSendText

### Community 27 - "Hifz Streak Tests"
Cohesion: 0.11
Nodes (13): cache_key(), _caption(), _ctx(), _earn(), _isolate_registries(), _photo_message(), _Settings, _streak() (+5 more)

### Community 28 - "Hifz Platform"
Cohesion: 0.12
Nodes (17): Hifz Platform - Plan & Progress, Phase 1 acceptance criteria (tests/test_acceptance.py), Hifz change log, claim_due claimed_at clock bug, Hifz data model (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send, group_*), Phase 2 group cluster (J1-J6, forum topics), Workstream C: interval merge-on-insert + derived percentages, Workstream H: weekly leaderboard (+9 more)

### Community 29 - "Acceptance Tests"
Cohesion: 0.15
Nodes (12): _CallbackQuery, _cmd(), _ctx(), _isolate_registries(), _Message, _run_wizard(), _Settings, _tap() (+4 more)

### Community 30 - "bot/media.py"
Cohesion: 0.06
Nodes (21): Phase 4 — Split infrastructure god-objects — *done*, answer_inline_query(), inline_audio_result(), inline_photo_results(), combined_audio_key(), deliver_combined_audio(), deliver_quran(), range_audio_url() (+13 more)

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 33 - "test_recall_check.py"
Cohesion: 0.15
Nodes (4): test_options_need_no_html_escaping_beyond_the_callers(), test_pick_ayah_is_deterministic_per_user_and_date(), test_pick_ayah_on_an_inverted_or_empty_span(), test_unknown_ayahs_are_rejected()

### Community 34 - ".get"
Cohesion: 0.09
Nodes (8): 12. Testing, What's covered, get_default_query_results(), parse_quran(), TranslationRegistry, TestCorpusIntegrity, TestCaching, TestFallback

### Community 35 - "Phase 1 — Take `main.py` apart (pure moves) — *done*"
Cohesion: 0.15
Nodes (12): 1. Why, 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 1 — Take `main.py` apart (pure moves) — *done*, Phase 5 — Fix the layering — *done*, Phase 6 — Repository hygiene — *done*, _post_portion(), push_group_day() (+4 more)

### Community 36 - "_plan_preview.py"
Cohesion: 0.19
Nodes (3): _portion_label(), Portion, TestPortionShape

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.09
Nodes (23): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 1. Terminology (so the report language is right), 2. What "correct" can mean — error taxonomy, 3.1 Commercial, 3.2 Open models and data, 3.3 Reference *text* per riwāyah (+15 more)

### Community 38 - "hifz_progress.py"
Cohesion: 0.10
Nodes (4): format_percent(), _Ratio, round_percent(), TestRounding

### Community 39 - "test_whatsapp_webhook.py"
Cohesion: 0.11
Nodes (13): create_app(), _isolate_registries(), store(), client(), data(), client(), fixture(), handled() (+5 more)

### Community 40 - "to_markup"
Cohesion: 0.09
Nodes (13): reciter_keyboard(), reciter_label(), reciter_page_count(), verse_keyboard(), to_button(), to_markup(), TestToMarkup, _pager_row() (+5 more)

### Community 41 - "session.py"
Cohesion: 0.12
Nodes (24): _b64url(), init_data_max_age(), issue_token(), jwt_secret(), require_user(), _sign(), _unauthorized(), auth_link() (+16 more)

### Community 42 - "PostgresPlanStore"
Cohesion: 0.07
Nodes (4): PlanDayRow, PlanRow, PlanStore, PostgresPlanStore

### Community 43 - "quran_page_progress"
Cohesion: 0.09
Nodes (5): juz_page_progress(), PageProgress, quran_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 44 - "test_hifz_cross_platform.py"
Cohesion: 0.10
Nodes (8): _error(), WhatsAppError, WindowClosed, data(), no_cdn(), Telegram, test_a_week_on_whatsapp_matches_a_week_on_telegram(), _week()

### Community 45 - "Streaks"
Cohesion: 0.13
Nodes (4): record_session(), TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 46 - "Load Test"
Cohesion: 0.09
Nodes (17): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+9 more)

### Community 47 - "Multilingual Plan"
Cohesion: 0.19
Nodes (12): Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), Quran.from_file(path) refactor, setMyCommands per language, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+4 more)

### Community 48 - "Text"
Cohesion: 0.15
Nodes (11): reference(), data(), fake_bot(), _inline_query(), _of_type(), public_url(), _results(), TestInlineArabicImage (+3 more)

### Community 49 - "Schema"
Cohesion: 0.11
Nodes (27): daily_ayah_sub, group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval (+19 more)

### Community 50 - "Services"
Cohesion: 0.15
Nodes (19): _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today(), test_me_carries_plan_and_streak() (+11 more)

### Community 51 - "api/progress.py"
Cohesion: 0.20
Nodes (15): forget(), ForgetIn, ForgetOut, _juz(), JuzRatio, progress(), ProgressOut, Ratio (+7 more)

### Community 52 - "Dispatch"
Cohesion: 0.16
Nodes (18): _callback(), data(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index(), test_inline_query_valid_ayah_returns_all_four_views() (+10 more)

### Community 55 - "Inline Reciter Search Tests"
Cohesion: 0.10
Nodes (24): handle_incoming(), handle_update(), _incoming(), _audio_result(), data(), fake_bot(), _inline_callback(), _inline_query() (+16 more)

### Community 56 - "test_hifz_check.py"
Cohesion: 0.13
Nodes (14): build_question(), _answer_data(), _ask(), _asked(), _buttons(), _callback_query(), _ctx(), _sessions() (+6 more)

### Community 57 - "deliver_push"
Cohesion: 0.23
Nodes (9): deliver_push(), _log(), ctx_for(), say_hi(), test_every_push_is_logged_for_cost_tracking(), TestConsent, TestTelegram, TestWhatsApp (+1 more)

### Community 58 - "test_service_layer.py"
Cohesion: 0.33
Nodes (5): _imported_modules(), _py_files(), test_api_holds_no_sql(), test_guards_see_files(), test_services_never_import_telegram()

### Community 60 - "test_hifz_keyboard_snapshots.py"
Cohesion: 0.26
Nodes (6): _as_dict(), _ctx(), _Settings, _static_cases(), test_hifz_keyboards_match_their_snapshots(), _view_cases()

### Community 61 - "Dispatch Order Tests"
Cohesion: 0.18
Nodes (17): _callback(), data(), fake_bot(), _message(), probe(), _sent_a_verse(), test_a_command_beats_a_pending_reciter_search(), test_a_command_escapes_a_wizard_without_ending_it() (+9 more)

### Community 62 - "taps"
Cohesion: 0.15
Nodes (4): taps(), TestChoices, TestMedia, TestNumberedMenuLifetime

### Community 63 - "Mini App Plan"
Cohesion: 0.11
Nodes (18): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 4.1 Flow, 4.2 Rules (+10 more)

### Community 65 - "services/check.py"
Cohesion: 0.10
Nodes (11): _parse_answer(), _question_text(), _score(), pick_ayah(), preload_corpus(), RecallQuestion, ask(), default_span() (+3 more)

### Community 66 - "check_locales.py"
Cohesion: 0.15
Nodes (12): Workstream I: i18n & commands for 48 locales, Workstream G: streaks & PNG contribution graph, Hifz platform frozen string manifest, src/locales/en.py source of truth, 111 hifz string keys by workstream, Key conventions (btn_*, cmd_*), Wave process (feature agents, translation agents, reviewers), Native-speaker review - hifz platform strings (+4 more)

### Community 67 - "hifz_progress.py"
Cohesion: 0.04
Nodes (22): _focus_surah(), juz_progress(), JuzProgress, Progress, ProgressSummary, quran_progress(), _recency_key(), _spans() (+14 more)

### Community 68 - "features/leaderboard.py"
Cohesion: 0.38
Nodes (3): _board_message(), leaderboard(), on_leaderboard()

### Community 69 - "weekly_board"
Cohesion: 0.28
Nodes (3): weekly_board(), make_user(), TestWeeklyBoard

### Community 70 - "api/catalog.py"
Cohesion: 0.20
Nodes (10): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, put_position(), ReaderPosition, Reciter (+2 more)

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.29
Nodes (3): _ctx(), _Settings, TestCtx

### Community 73 - "Ref"
Cohesion: 0.08
Nodes (29): answer(), AnswerIn, AnswerOut, make_token(), question(), QuestionOut, read_token(), _secret() (+21 more)

### Community 74 - "router.py"
Cohesion: 0.05
Nodes (41): 5. API surface (`/api/v1`), Phase 3 — One router for everything — *done*, _on_text(), juz(), page(), page_audio(), turn_page(), random_ayah() (+33 more)

### Community 75 - "Phase 2 — DRY the duplicated patterns"
Cohesion: 0.14
Nodes (11): graphify knowledge graph (graphify-out/), CLAUDE.md graphify lookup rules, button_rows() row-packing helper, Copy-pasted patterns table (§1.3), GET / health with store and cache status (503), ignore_not_modified() context manager, Phase 2 — DRY the duplicated patterns, Phase 3 — One router for everything (+3 more)

### Community 76 - "tick.py"
Cohesion: 0.07
Nodes (16): enqueue(), idempotency_key(), schedule_daily(), catch_up(), run_scheduler(), _wait(), _deliver(), _is_stale() (+8 more)

### Community 78 - "os"
Cohesion: 0.06
Nodes (18): bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file(), export() (+10 more)

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.13
Nodes (16): Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points), Error taxonomy L1-L5 (word, harakah, tajwid, riwayah mismatch, waqf), Evaluation plan (false-alarm gate < 2% per ayah), IqraEval 2025 shared task, Recitation checker phased roadmap (A-1 to E) (+8 more)

### Community 80 - "BismillahBot — Business Logic"
Cohesion: 0.08
Nodes (18): 1. Overview, 2. Architecture, 3. Request lifecycle, 5. Caching strategy, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic, Local time (+10 more)

### Community 81 - "Streaks: compute_streak"
Cohesion: 0.24
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 83 - "SessionStore"
Cohesion: 0.07
Nodes (6): InMemorySessionStore, LeaderboardEntry, PostgresSessionStore, SessionRow, SessionStore, WeeklyBoard

### Community 84 - "Scheduler Tests"
Cohesion: 0.17
Nodes (4): _claimed_at(), _record(), TestCatchUp, TestTick

### Community 85 - "export"
Cohesion: 0.27
Nodes (6): build_meta(), export(), main(), _spans(), split_basmalah(), _write()

### Community 86 - "whatsapp_format.py"
Cohesion: 0.20
Nodes (3): _Converter, _render(), _wrap()

### Community 87 - "_clip"
Cohesion: 0.12
Nodes (8): _clip(), _covered(), _intersect(), _page_share(), _pages_of(), clamp_to_quran(), contains(), TestContainsAndClamp

### Community 89 - "auth.py"
Cohesion: 0.10
Nodes (30): decode_token(), _init_data_secret(), InvalidInitData, InvalidToken, sign_init_data(), validate_init_data(), _auth(), _fields() (+22 more)

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.08
Nodes (24): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+16 more)

### Community 92 - "dispatch.py"
Cohesion: 0.10
Nodes (19): app_button(), app_link(), app_url(), set_menu_button(), _app_command(), app_on(), data(), test_app_command() (+11 more)

### Community 93 - "_hifz"
Cohesion: 0.06
Nodes (11): HifzInterval, _assert_invariant(), _ayahs(), _hifz(), _spans(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order() (+3 more)

### Community 94 - "Dependency rule (app -> bot -> services -> domain)"
Cohesion: 0.18
Nodes (10): tests/test_layering.py ratchet (KNOWN violations), Overlap with MULTI_PLATFORM_PLAN channel seam, Shared UTC offset picker (time_pickers.offset_keyboard), Decisions and open questions (§9), Found along the way (out-of-scope behaviour changes), Phase 0 — Guardrails (ruff, layering test, logging), Phase 5 — Fix the layering, Target layout (app/ bot/ services/ domain/ infra/) (+2 more)

### Community 95 - "handle_message"
Cohesion: 0.19
Nodes (9): handle_message(), bodies(), fixture_message(), known_user(), tap(), TestBoundaries, TestFirstContact, TestReader (+1 more)

### Community 101 - "TestStateStore"
Cohesion: 0.05
Nodes (11): _clean_state_store(), _on_callback(), page_audio_url(), page_image_url(), File, _key(), take(), TestAudioFilename (+3 more)

### Community 103 - "week_bounds"
Cohesion: 0.25
Nodes (3): user_week_window(), week_window(), TestWeekWindow

### Community 104 - "recall_check.py"
Cohesion: 0.08
Nodes (22): _assemble(), _ayah_text(), _basmala_prefix(), _clean(), _continuation_question(), corpus(), display_length(), _distinct() (+14 more)

### Community 105 - "services/streaks.py"
Cohesion: 0.09
Nodes (14): _answer_data(), _ask(), check(), on_check(), _options_keyboard(), Milestone, milestone_for(), _milestone_key() (+6 more)

### Community 107 - "test_daily_feature.py"
Cohesion: 0.34
Nodes (5): _due_rows(), TestWhatsApp, tg_bot(), wa_tap(), wa_text()

### Community 108 - "welcome_text"
Cohesion: 0.18
Nodes (4): command_lines(), welcome_text(), TestSevenTheCommandsExist, TestWelcomeText

### Community 109 - "button_rows"
Cohesion: 0.08
Nodes (15): _search_reciters(), forgot_command(), on_progress_tap(), progress_view(), _show(), _surah_line(), reciter_search_keyboard(), button_rows() (+7 more)

### Community 110 - "stats.py"
Cohesion: 0.18
Nodes (10): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut (+2 more)

### Community 111 - "send_page"
Cohesion: 0.29
Nodes (7): send_page(), _buffer(), _stub_stitch(), stub(), TestPageCard, capture(), counting()

### Community 113 - "store/__init__.py"
Cohesion: 0.07
Nodes (10): DailyStore, InMemoryDailyStore, HifzStore, InMemoryHifzStore, InMemoryStore, Store, MemoryState, _isolate_handlers() (+2 more)

### Community 115 - "Koyeb Capacity Report"
Cohesion: 0.25
Nodes (7): Koyeb free-tier capacity report, CPU-bound queueing failure mode (~24 msg/s ceiling), Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start), Neon managed Postgres, Capacity results 5-1000 concurrent (no errors, 70-91 MB), Stress environment (docker-compose.stress.yml, cpus 0.1, 512m), Synthetic traffic mix (scripts/stress/gen_updates.py)

### Community 116 - "Blue Green Ci"
Cohesion: 0.14
Nodes (13): concurrency, cancel-in-progress, group, env, PYTHON_DEFAULT, name, on, pull_request (+5 more)

### Community 117 - "Blue Green Ci: name"
Cohesion: 0.23
Nodes (14): steps, steps, steps, steps, steps, steps, steps, env (+6 more)

### Community 120 - "._load_performers"
Cohesion: 0.10
Nodes (7): reciter_page_of(), data(), fake_bot(), TestCatalogKinds, TestCatalogOrder, TestCurrentReciter, tg_bot()

### Community 122 - "button_action"
Cohesion: 0.27
Nodes (3): button_action(), _reverse_button_map(), TestButtonAction

### Community 123 - "streak.py"
Cohesion: 0.23
Nodes (7): _caption(), _keyboard(), on_streak(), _send_graph(), streak(), streak_summary(), StreakSummary

### Community 124 - "Quran"
Cohesion: 0.05
Nodes (14): surah_name(), _consolidations(), Quran, page_ref(), surah_spans(), test_page_boundaries_match_the_bot(), TestEveryParsedRefIsReal, TestDivisionsTileTheQuran (+6 more)

### Community 125 - "4. Navigation model"
Cohesion: 0.22
Nodes (10): 4. Navigation model, Audio catalog kinds, Page audio with stitched fallback, Page images and page audio, Repeat (memorization), Structural divisions (page / juz / sajda), Translation-only catalogue entries, Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES) (+2 more)

### Community 126 - "TestHelpers"
Cohesion: 0.08
Nodes (8): _covers(), _merge_span(), _normalize(), _overlaps(), PostgresHifzStore, _split_span(), _touches(), TestHelpers

### Community 127 - "Blue Green Ci: jobs"
Cohesion: 0.15
Nodes (13): name, needs, runs-on, jobs, build, lint, rollback, name (+5 more)

### Community 128 - "Blue Green Ci: with"
Cohesion: 0.15
Nodes (13): with, cache, cache-dependency-path, cache-from, cache-to, context, if-no-files-found, load (+5 more)

### Community 129 - "build_grid"
Cohesion: 0.18
Nodes (4): build_grid(), _counts(), Grid, TestGrid

### Community 130 - "test_navigation.py"
Cohesion: 0.10
Nodes (12): 2. Current-state audit (what is hardcoded English), build_data(), data(), data(), fake_bot(), _message(), _no_network(), TestCommandArguments (+4 more)

### Community 131 - "test_page_mode.py"
Cohesion: 0.24
Nodes (4): data(), fake_bot(), TestStitchedAudioAcrossSurahs, tg_bot()

### Community 132 - "Mini App Plan: Separate quranayatminiapp Nextjs"
Cohesion: 0.14
Nodes (11): Inline query answering (all four representations, ranges), Navigation model ((surah, ayah, type) per chat_id), Page image stitching (lib/page_image.py), Structural divisions (page / juz / sajda from quran-data.xml), Verse card (inline keyboard, edit in place), Uthmani text in Amiri Quran / KFGQPC font, Locale export to JSON (web_ keys, next-intl), Static immutable Quran JSON served from frontend CDN (+3 more)

### Community 134 - "Channel"
Cohesion: 0.10
Nodes (5): Caps, Channel, for_platform(), TestForPlatform, TestTheRest

### Community 135 - "range_audio"
Cohesion: 0.06
Nodes (16): range_audio(), _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl(), content(), _count(), _load(), test_arabic_has_every_ayah() (+8 more)

### Community 136 - "download_stitched_audio"
Cohesion: 0.24
Nodes (5): stitch(), deliver_repeated_audio(), stitch(), download_combined_audio(), download_stitched_audio()

### Community 137 - "InMemoryGroupStore"
Cohesion: 0.06
Nodes (6): GroupConfig, GroupMemberLink, GroupPlanDayRow, GroupPlanRow, GroupStore, InMemoryGroupStore

### Community 140 - "MINI_APP_PLAN.md"
Cohesion: 0.20
Nodes (8): Central callback prefix allocation (hifz.PREFIXES), Future roadmap and prioritized backlog, The hifz platform (memorization companion), Pure plan builder (build_plan), Streak day ticks on completed session, Bot ↔ Mini App integration (menu button, startapp, /app), recitation_job table and user_profile.riwayah, /recite flow (voice note → recitation_job → report)

### Community 141 - "re"
Cohesion: 0.29
Nodes (5): parse_quran_tafsir(), _modules(), test_nothing_builds_telegram_markup_by_hand_outside_those_modules(), test_only_group_code_reads_the_telegram_client(), test_only_telegram_only_modules_import_telegram()

### Community 143 - "Ctx"
Cohesion: 0.09
Nodes (28): command, Routing rules (in `serve`), Phase 2 — WhatsApp MVP (reader + daily ayat), 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, Ctx, _begin_setup(), handle_start_payload() (+20 more)

### Community 144 - "locales/__init__.py"
Cohesion: 0.09
Nodes (10): nav_labels(), _division_marks(), make_index(), _load_locales(), _module_name(), get_language(), is_supported(), is_ui_language() (+2 more)

### Community 147 - ".test_full_flow_queues_the_first_send"
Cohesion: 0.38
Nodes (5): _buttons(), _message(), _tap(), TestTelegramSetup, _texts()

### Community 153 - "test_layering.py"
Cohesion: 0.36
Nodes (6): _absolute_imports(), _sources(), test_known_violations_still_exist(), test_no_new_violations(), test_the_scan_sees_every_package(), _violations()

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 155 - "test_channels_whatsapp.py"
Cohesion: 0.08
Nodes (8): bot(), cache(), TestChoice, cache(), graph(), Graph, TestText, TestVoiceNotes

### Community 158 - "Profile settings reset fix (fix/settings-persistence)"
Cohesion: 0.29
Nodes (8): ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable, lib/utils.File god class, Silent in-memory store fallback, Phase 4 — Split infrastructure god-objects, Profile settings reset fix (fix/settings-persistence), Typed frozen Settings (config/settings.py), conftest.py test environment (src on path, CWD pin, no Redis/network), Environment configuration (webhook, CDN base URLs, Redis)

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

### Community 166 - "ProfileStore"
Cohesion: 0.06
Nodes (3): ProfileRow, ProfileStore, UserSettingsRow

### Community 169 - "TestPickerFlow"
Cohesion: 0.17
Nodes (5): _callback(), _message(), _tab_row(), TestAudioNeverFollowsLanguage, TestPickerFlow

### Community 170 - "button_action"
Cohesion: 0.11
Nodes (6): keyboard_rows(), missing_keys(), _placeholders(), TestCatalogue, TestGroupLocaleExemption, TestLocaleIntegrity

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 172 - "TranslationRegistry"
Cohesion: 0.11
Nodes (16): 7. Known limitations / tech debt, 10. File-by-file change list, 11. Memory & performance (free-tier reality), 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 3. Target architecture, 4. User language preference (+8 more)

### Community 175 - "unittest_mock"
Cohesion: 0.11
Nodes (7): _isolate_registries(), TestSchemaApplication, _as_dict(), _keyboards(), _render(), _search_markup(), test_keyboards_match_their_snapshots()

### Community 178 - "BismillahBot README"
Cohesion: 0.21
Nodes (9): Translation Attributions, Four ayah representations (english, tafsir, arabic, audio), Known limitations / tech debt, Issues fixed in the refactor (12 bugs), Documentation, BismillahBot README, Inline mode (@BismillahBot ref/range/reciter), Mushaf page reader (/page, /juz, /sajda) (+1 more)

### Community 181 - "ayah_for"
Cohesion: 0.29
Nodes (4): ayah_for(), test_every_entry_is_a_real_ayah(), test_nothing_repeats_within_one_cycle(), test_same_date_same_ayah()

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
Nodes (7): _at_offset(), _date_key(), pick_ayahs(), _span_length(), _span_tuple(), ayah_count(), TestAyahCount

### Community 194 - "send_repeated_audio"
Cohesion: 0.26
Nodes (3): send_repeated_audio(), _stub_audio(), TestRepeatForMemorization

### Community 196 - "8. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 8. Phased task breakdown, Phase 0 — Foundations, Phase 1 — Service-layer extraction (this repo, no UI change), Phase 2 — Reader parity (read-only, low risk, ships first), Phase 3 — Hifz parity, Phase 4 — Recitation checker UI (depends on the investigation's Phase A), Phase 5 — Later

### Community 197 - "offset_options"
Cohesion: 0.22
Nodes (8): offset_choices(), offset_keyboard(), _grid(), test_a_label_prefix_changes_only_the_label(), test_cancel_data_adds_a_localized_cancel_row(), test_every_offset_is_offered_in_order_under_the_callers_prefix(), test_no_cancel_row_unless_asked(), test_rows_are_columns_wide()

### Community 200 - "Translation editions table (48 codes)"
Cohesion: 0.33
Nodes (5): alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Locale review tracking table (47 locales)

### Community 205 - "Testing & CI"
Cohesion: 0.40
Nodes (6): Documentation index (docs/README.md), Phase 6 — Repository hygiene, CI — Blue-Green pipeline, Running the tests locally, Testing & CI, scripts/check_locales.py locale integrity check

### Community 206 - "11. Infrastructure, capacity and cost on paid Koyeb"
Cohesion: 0.33
Nodes (6): 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards, 11. Infrastructure, capacity and cost on paid Koyeb

### Community 214 - "PostgresDailyStore"
Cohesion: 0.10
Nodes (4): DailySubRow, PostgresDailyStore, PostgresStore, store()

### Community 266 - "test_media_cache_keys.py"
Cohesion: 0.15
Nodes (8): _bot(), _next_id(), send_audio(), send_photo(), no_cdn(), _source(), test_a_miss_caches_under_the_key_and_a_hit_replays_it(), test_a_rejected_cached_id_is_rebuilt_and_recached()

### Community 269 - "get_store"
Cohesion: 0.10
Nodes (8): get_store(), _lock(), _save_plan(), TestTwoTheDailyPush, _added_update(), TestAdded, TestDailyPost, TestSpecAcceptance

### Community 270 - "features/daily.py"
Cohesion: 0.15
Nodes (16): _ask_time(), daily(), _enable(), _hhmm(), _offset(), on_tap(), _parse_time(), push_daily() (+8 more)

### Community 286 - "bot/whatsapp.py"
Cohesion: 0.14
Nodes (7): _allowed_command(), as_command(), lang_hint(), _now(), opt_out(), _tap(), TestKeywords

## Knowledge Gaps
- **51 isolated node(s):** `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres`, `Capacity results 5-1000 concurrent (no errors, 70-91 MB)`, `Verse card (inline keyboard, edit in place)` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1726 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **167 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `get_store` to `features/profile.py`, `_ctx`, `_ctx`, `services/plans.py`, `Store`, `render_streak_graph`, `get_settings`, `UserSettings`, `Context`, `RedisSingleton`, `lifespan.py`, `.test_full_flow_queues_the_first_send`, `Hifz Progress Cmd Tests`, `Hifz Streak Tests`, `Acceptance Tests`, `bot/media.py`, `bot/whatsapp.py`, `session.py`, `test_hifz_cross_platform.py`, `Streaks`, `Services`, `api/progress.py`, `Inline Reciter Search Tests`, `test_hifz_check.py`, `test_hifz_keyboard_snapshots.py`, `WhatsApp`, `hifz_progress.py`, `weekly_board`, `Ref`, `router.py`, `tick.py`, `BismillahBot — Business Logic`, `.test_sends_todays_ayah_and_queues_tomorrow`, `PostgresDailyStore`, `_hifz`, `handle_message`, `TestStateStore`, `services/streaks.py`, `test_daily_feature.py`, `stats.py`, `store/__init__.py`, `refresh_streaks`, `streak.py`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Are the 44 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 44 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_plan` be split into smaller, more focused modules?**
  _Cohesion score 0.04487179487179487 - nodes in this community are weakly interconnected._
- **Why does `Quran` connect `Quran` to `build_plan`, `test_navigation.py`, `_plan_setup.py`, `features/profile.py`, `range_audio`, `services/plans.py`, `locales/__init__.py`, `Refs`, `lifespan.py`, `Hifz Progress Cmd Tests`, `bot/media.py`, `.get`, `Phase 1 — Take `main.py` apart (pure moves) — *done*`, `quran_page_progress`, `TranslationRegistry`, `api/progress.py`, `test_hifz_check.py`, `.get_surah_length`, `services/check.py`, `hifz_progress.py`, `api/catalog.py`, `Ref`, `router.py`, `BismillahBot — Business Logic`, `sweep_refs`, `test_short_surahs_still_get_four_distinct_options`, `export`, `_clip`, `recall_check.py`, `services/streaks.py`, `button_rows`, `.get_next_ayah`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `Ctx` (e.g. with `3. Architecture` and `4.1 Overlap with `MULTI_PLATFORM_PLAN.md``) actually correct?**
  _`Ctx` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Should `link_token.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10476190476190476 - nodes in this community are weakly interconnected._