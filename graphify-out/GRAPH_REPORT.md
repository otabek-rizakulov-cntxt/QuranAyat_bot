# Graph Report - QuranAyat_bot  (2026-11-01)

## Corpus Check
- 245 files · ~241,726 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 4607 nodes · 10605 edges · 295 communities (145 shown, 150 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 973 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0b8cfd49`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_plan
- .page_range
- summarize
- enqueue_next
- .start
- _plan_setup.py
- infra/catalog.py
- localtime.py
- to_whatsapp
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
- PageProgress
- Docker Compose.stress
- test_page_mode.py
- test_recall_check.py
- TranslationRegistry
- Auth
- File
- Recitation Checker Investigation
- round_percent
- ScheduledSend
- to_markup
- Session
- Plans: PlanStore
- Ref
- _send_plain_message
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
- Wizard
- .get_surah_length
- Hifz
- _hifz
- Dispatch Order Tests
- logging
- Mini App Plan
- surah_progress
- InMemoryGroupStore
- InMemoryIdentityStore
- get_store
- Quran
- _plan_out
- reset_for_tests
- Hifz Seam Tests
- api/plans.py
- t
- Hifz Progress: juz_progress
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
- services/plans.py
- auth.py
- Store Contract Tests
- Multi Platform Plan: MultiPlatform Implementation Plan
- unittest_mock
- TestAddInterval
- Profiles: ProfileRow
- parse_offset
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
- offset_keyboard
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
- services/leaderboard.py
- Export Web Content Tests
- ._load_performers
- _seed_legacy_lang
- test_hifz_intervals.py
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
- range_audio
- test_keyboard_snapshots.py
- GroupStore
- Store Contract Tests: TestLeaderboard
- TestProfiles
- Business Logic: The hifz platform memorization
- PostgresStore
- week_bounds
- t
- get_language
- PostgresHifzStore
- PostgresScheduleStore
- Hifz Seam Tests: test_hifz_seampy
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- test_miniapp_links.py
- .test_concatenates_the_ayahs_in_order
- Blue Green Ci: env
- TestHifzIntervalEdges
- test_wizard.py
- graphify-autopush.sh
- Page Mode Tests
- MINI_APP_PLAN.md
- Settings Tests
- Store Contract Tests: TestSessions
- Blue Green Ci: postgres
- Blue Green Ci: test
- Blue Green Ci: preflight
- check_locales.py
- domain/streaks.py
- Hifz Seam Tests: TestPrefixNamespace
- Hifz Seam Tests: TestDispatchCallback
- TestPickerFlow
- button_action
- Blue Green Ci: smokegreen
- BismillahBot — Multilingual Support Plan
- load_summary
- File Facade: search_performers
- parse_ayah_range
- BUSINESS_LOGIC.md
- Verse Card Tests
- BismillahBot README
- 8. Phased task breakdown
- register_send_handler
- json
- Blue Green Ci: deploygreen
- Blue Green Ci: promote
- _Ratio
- format_offset
- Hifz Seam Tests: test_longest_prefix_wins
- test_scheduler.py
- test_store_contract.py
- GroupPlanDayRow
- ProfileStore
- GroupMemberLink
- Claude
- 11. Infrastructure, capacity and cost on paid Koyeb
- Hifz Seam Tests: TestDispatchCommand
- PostgresIdentityStore
- test_the_basmala_heading_is_not_part_of_the_question
- sweep_refs
- Hifz Group Tests: TestRegistration
- user_settings.py
- percentile_band
- fetch_and_stitch
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
- miniapp.py
- GroupConfig
- test_export_web_content.py
- test_inline_range.py
- 6. Phased task breakdown
- reciter_page_of
- .has_page_audio
- require_user
- TestSevenTheCommandsExist
- TestRegistration
- test_options_need_no_html_escaping_beyond_the_callers

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
- `3. Target architecture` --references--> `TranslationRegistry`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/domain/quran.py
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `5. Caching strategy` --references--> `MemoryStore`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/infra/redis_client.py
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

## Communities (295 total, 150 thin omitted)

### Community 0 - "build_plan"
Cohesion: 0.05
Nodes (15): advancing(), auto_pace(), build_plan(), surah_ref(), assert_covers_target_once(), assert_well_formed(), spans(), TestAcrossTheWholeQuran (+7 more)

### Community 1 - ".page_range"
Cohesion: 0.07
Nodes (8): 4. Navigation model, Page images and page audio, Structural divisions (page / juz / sajda), Translation-only catalogue entries, _consolidations(), test_page_boundaries_match_the_bot(), TestDivisionsTileTheQuran, TestNavigation

### Community 2 - "summarize"
Cohesion: 0.08
Nodes (5): Progress, summarize(), HifzInterval, _at(), TestSummarize

### Community 3 - "enqueue_next"
Cohesion: 0.19
Nodes (8): complete_day(), DrillResult, due_days(), enqueue_next(), owned_day(), profile_offset(), user_local_today(), utcnow()

### Community 5 - "_plan_setup.py"
Cohesion: 0.09
Nodes (33): _score(), on_group_tap(), memorize(), on_tap(), plan_step(), _expired(), _ref_from_draft(), _ref_to_draft() (+25 more)

### Community 6 - "infra/catalog.py"
Cohesion: 0.07
Nodes (13): reciter_set_confirmation(), audio_url(), find(), has_page_audio(), image_url(), page_audio_url(), page_image_url(), performer_name() (+5 more)

### Community 7 - "localtime.py"
Cohesion: 0.11
Nodes (11): _enqueue_next_board(), _enqueue_next_group(), _as_utc(), local_date(), local_now(), local_time(), next_due_utc(), to_utc() (+3 more)

### Community 8 - "to_whatsapp"
Cohesion: 0.07
Nodes (8): _Converter, _render(), split(), to_whatsapp(), _wrap(), TestSplit, TestTags, TestWhatTheBotSends

### Community 9 - "Leaderboard"
Cohesion: 0.12
Nodes (10): _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join(), _Message, _sent(), _Settings (+2 more)

### Community 10 - "_ctx"
Cohesion: 0.06
Nodes (19): PlanDaySpec, _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _isolate_registries(), _Message (+11 more)

### Community 11 - "Profile"
Cohesion: 0.07
Nodes (27): patch_profile(), _profile(), _cancel_keyboard(), _join_board(), name_step(), offset_from_callback(), on_profile_tap(), _plan_line() (+19 more)

### Community 12 - "Store"
Cohesion: 0.09
Nodes (11): _CallbackQuery, _ctx(), _isolate_registries(), _Message, _run_wizard(), _Settings, _tap(), TestDrill (+3 more)

### Community 13 - "render_streak_graph"
Cohesion: 0.11
Nodes (9): render(), draw_contribution_graph(), Grid, render_streak_graph(), _semaphore(), open_png(), TestCacheKey, TestRendering (+1 more)

### Community 14 - "services/streaks.py"
Cohesion: 0.20
Nodes (5): StreakCounts, refresh_streaks(), SessionOutcome, streak_summary(), TestRefreshAndSummary

### Community 15 - "User Settings"
Cohesion: 0.18
Nodes (5): UserSettings, TestDefaults, TestIndependence, TestKeyedByUserId, TestRoundTrip

### Community 16 - "Context"
Cohesion: 0.14
Nodes (15): _bot(), _ctx(), _isolate_registries(), _member(), _run_setup_to_plan(), _Settings, TestBoard, tap() (+7 more)

### Community 17 - "Health"
Cohesion: 0.06
Nodes (15): health(), store_backend(), database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries(), fresh_redis() (+7 more)

### Community 18 - "Refs"
Cohesion: 0.06
Nodes (14): clamp_to_quran(), _clean(), format_ref(), juz_ref(), parse_range(), parse_reference(), TestSurahSpans, TestAcrossSurahs (+6 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.09
Nodes (7): 6. Issues fixed in this refactor, get(), _key(), save(), get(), CacheUnavailable, RedisSingleton

### Community 20 - "typing"
Cohesion: 0.06
Nodes (20): Phase 1 — Take `main.py` apart (pure moves) — *done*, create_app(), _commands_for(), initialize(), lifespan(), _set_bot_commands(), _process_update(), telegram_webhook() (+12 more)

### Community 21 - "Router"
Cohesion: 0.08
Nodes (19): Phase 3 — One router for everything — *done*, _on_callback(), decorate(), _cancel(), command(), decorate(), dispatch_callback(), dispatch_command() (+11 more)

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "Group"
Cohesion: 0.09
Nodes (20): _begin_setup(), bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), group_board_entries(), handle_start_payload() (+12 more)

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.15
Nodes (13): 10. Found along the way (out of scope — behaviour changes), 2. Goals and non-goals, 3. Principles applied, 6. Ordering, risk, size, 7. Safety net, 8. Expected result, 9. Decisions and open questions, Expected result metrics (§8) (+5 more)

### Community 26 - "TelegramChannel"
Cohesion: 0.07
Nodes (11): for_platform(), TelegramChannel, bot(), cache(), TestAnswerAndTyping, TestChoice, TestEditChoices, TestEditText (+3 more)

### Community 27 - "Hifz Streak Tests"
Cohesion: 0.11
Nodes (13): cache_key(), _caption(), _ctx(), _earn(), _isolate_registries(), _photo_message(), _Settings, _streak() (+5 more)

### Community 28 - "Hifz Platform"
Cohesion: 0.09
Nodes (20): Hifz Platform - Plan & Progress, Phase 1 acceptance criteria (tests/test_acceptance.py), Hifz change log, claim_due claimed_at clock bug, Hifz data model (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send, group_*), Phase 2 group cluster (J1-J6, forum topics), Workstream I: i18n & commands for 48 locales, Workstream C: interval merge-on-insert + derived percentages (+12 more)

### Community 29 - "Acceptance Tests"
Cohesion: 0.11
Nodes (13): _CallbackQuery, _cmd(), _ctx(), _isolate_registries(), _Message, _run_wizard(), _save_plan(), _Settings (+5 more)

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 32 - "test_page_mode.py"
Cohesion: 0.24
Nodes (4): data(), fake_bot(), TestStitchedAudioAcrossSurahs, tg_bot()

### Community 33 - "test_recall_check.py"
Cohesion: 0.18
Nodes (3): test_pick_ayah_is_deterministic_per_user_and_date(), test_pick_ayah_on_an_inverted_or_empty_span(), test_unknown_ayahs_are_rejected()

### Community 34 - "TranslationRegistry"
Cohesion: 0.06
Nodes (12): 12. Testing, 5. Content: multi-translation loading (memory-aware), Translation catalogue (initial set), build_data(), make_index(), parse_quran(), TranslationRegistry, TestCorpusIntegrity (+4 more)

### Community 35 - "Auth"
Cohesion: 0.18
Nodes (15): _init_data_secret(), InvalidInitData, sign_init_data(), validate_init_data(), _fields(), test_added_field_is_rejected(), test_auth_rejects_tampered_init_data(), test_duplicate_field_is_rejected() (+7 more)

### Community 36 - "File"
Cohesion: 0.08
Nodes (6): File, TestAudioFilename, TestImageFilename, TestLegacyLanguageKey, TestStateStore, TestCoexistsWithTheReciterFlow

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.09
Nodes (22): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 1. Terminology (so the report language is right), 2. What "correct" can mean — error taxonomy, 3.1 Commercial, 3.2 Open models and data, 3.3 Reference *text* per riwāyah (+14 more)

### Community 38 - "round_percent"
Cohesion: 0.21
Nodes (3): format_percent(), round_percent(), TestRounding

### Community 39 - "ScheduledSend"
Cohesion: 0.23
Nodes (5): enqueue(), idempotency_key(), schedule_daily(), registered_kinds(), ScheduledSend

### Community 40 - "to_markup"
Cohesion: 0.10
Nodes (11): page_keyboard(), verse_keyboard(), mode_button(), app_choice_row(), Choice, to_button(), to_markup(), TestToMarkup (+3 more)

### Community 41 - "Session"
Cohesion: 0.14
Nodes (18): init_data_max_age(), auth_telegram(), AuthOut, me(), _me(), MeOut, patch_settings(), PlanSummary (+10 more)

### Community 42 - "Plans: PlanStore"
Cohesion: 0.05
Nodes (5): InMemoryPlanStore, PlanDayRow, PlanRow, PlanStore, PostgresPlanStore

### Community 43 - "Ref"
Cohesion: 0.05
Nodes (19): _clip(), _covered(), _focus_surah(), _intersect(), juz_page_progress(), _page_share(), _pages_of(), quran_page_progress() (+11 more)

### Community 45 - "Streaks"
Cohesion: 0.13
Nodes (4): record_session(), TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 46 - "Load Test"
Cohesion: 0.10
Nodes (15): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+7 more)

### Community 47 - "Multilingual Plan"
Cohesion: 0.19
Nodes (12): Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), Quran.from_file(path) refactor, setMyCommands per language, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+4 more)

### Community 48 - "Text"
Cohesion: 0.20
Nodes (7): reference(), _inline_query(), _of_type(), _results(), TestInlineArabicImage, TestRangeAudio, TestRangeText

### Community 49 - "Schema"
Cohesion: 0.11
Nodes (26): group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval, hifz_interval_user_surah_idx (+18 more)

### Community 50 - "Services"
Cohesion: 0.15
Nodes (19): _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today(), test_me_carries_plan_and_streak() (+11 more)

### Community 51 - "api/check.py"
Cohesion: 0.13
Nodes (13): jwt_secret(), answer(), AnswerIn, AnswerOut, make_token(), question(), QuestionOut, read_token() (+5 more)

### Community 52 - "Dispatch"
Cohesion: 0.17
Nodes (19): handle_update(), _callback(), data(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index() (+11 more)

### Community 53 - "reciter_keyboard"
Cohesion: 0.12
Nodes (9): reciter_keyboard(), reciter_label(), reciter_page_count(), reciter_search_keyboard(), reciter_group(), _pager_row(), _reciter_buttons(), TestLabels (+1 more)

### Community 54 - "api/progress.py"
Cohesion: 0.18
Nodes (16): not_found(), forget(), ForgetIn, ForgetOut, _juz(), JuzRatio, progress(), ProgressOut (+8 more)

### Community 55 - "Inline Reciter Search Tests"
Cohesion: 0.14
Nodes (19): _audio_result(), data(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter(), test_ayah_audio_dropped_without_public_base_url(), test_ayah_audio_uses_callers_reciter() (+11 more)

### Community 56 - "test_hifz_check.py"
Cohesion: 0.10
Nodes (16): user_today(), _answer_data(), _AnyDay, _ask(), _asked(), _buttons(), _callback_query(), _ctx() (+8 more)

### Community 58 - ".get_surah_length"
Cohesion: 0.10
Nodes (7): quran_progress(), ayah_count(), TestQuranProgress, TestAyahCount, sweep_refs(), test_short_surahs_still_get_four_distinct_options(), test_the_last_ayah_of_every_surah_produces_a_question()

### Community 59 - "Hifz"
Cohesion: 0.10
Nodes (7): _covers(), InMemoryHifzStore, _merge_span(), _overlaps(), _split_span(), _touches(), TestHelpers

### Community 60 - "_hifz"
Cohesion: 0.17
Nodes (3): _hifz(), _spans(), TestRemoveRange

### Community 61 - "Dispatch Order Tests"
Cohesion: 0.16
Nodes (18): Wizard, _callback(), data(), fake_bot(), _message(), probe(), _sent_a_verse(), test_a_command_beats_a_pending_reciter_search() (+10 more)

### Community 62 - "logging"
Cohesion: 0.12
Nodes (4): setup_logging(), test_http_client_request_urls_are_never_logged(), test_the_secret_does_not_reveal_the_token(), test_webhook_acks_before_initialization()

### Community 63 - "Mini App Plan"
Cohesion: 0.11
Nodes (18): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 4.1 Flow, 4.2 Rules (+10 more)

### Community 65 - "surah_progress"
Cohesion: 0.11
Nodes (5): started_surahs(), surah_progress(), TestInputHandling, TestSpecAcceptance, TestSurahProgress

### Community 67 - "InMemoryIdentityStore"
Cohesion: 0.10
Nodes (3): InMemoryIdentityStore, InMemoryStore, TestRestartDeliversExactlyOnce

### Community 68 - "get_store"
Cohesion: 0.16
Nodes (6): get_store(), _lock(), TestFourProgress, _added_update(), TestAdded, TestDailyPost

### Community 69 - "Quran"
Cohesion: 0.04
Nodes (26): surah_name(), _parse_answer(), answer_inline_query(), inline_audio_result(), inline_photo_results(), combined_audio_key(), deliver_page_audio(), source() (+18 more)

### Community 70 - "_plan_out"
Cohesion: 0.23
Nodes (7): active(), lifecycle(), _plan_out(), PlanOut, today(), change_status(), current_plan()

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 73 - "api/plans.py"
Cohesion: 0.19
Nodes (14): _build(), complete(), create(), DrillOut, PlanCreateIn, PlanDayOut, PlanSettingsIn, _portion_out() (+6 more)

### Community 74 - "t"
Cohesion: 0.05
Nodes (35): 7. The keyboard & command localization challenge, Telegram command menu, handle_incoming(), _incoming(), _on_text(), _search_reciters(), juz(), page() (+27 more)

### Community 75 - "Hifz Progress: juz_progress"
Cohesion: 0.18
Nodes (4): juz_progress(), JuzProgress, started_juzs(), TestJuzProgress

### Community 76 - "tick.py"
Cohesion: 0.13
Nodes (10): SendCtx, _deliver(), _is_stale(), _lock(), _release(), _resolve(), tick(), _tick() (+2 more)

### Community 78 - "Bundle Translations"
Cohesion: 0.15
Nodes (8): _clean_state_store(), bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.13
Nodes (16): Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points), Error taxonomy L1-L5 (word, harakah, tajwid, riwayah mismatch, waqf), Evaluation plan (false-alarm gate < 2% per ayah), IqraEval 2025 shared task, Recitation checker phased roadmap (A-1 to E) (+8 more)

### Community 80 - "BismillahBot — Business Logic"
Cohesion: 0.12
Nodes (15): 1. Overview, 2. Architecture, 3. Request lifecycle, 5. Caching strategy, 7. Known limitations / tech debt, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic (+7 more)

### Community 81 - "Streaks: compute_streak"
Cohesion: 0.21
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 83 - "InMemorySessionStore"
Cohesion: 0.07
Nodes (5): InMemorySessionStore, LeaderboardEntry, PostgresSessionStore, SessionRow, SessionStore

### Community 84 - "Scheduler Tests"
Cohesion: 0.14
Nodes (6): _at(), _claimed_at(), _record(), TestCatchUp, TestIdempotentEnqueue, TestTick

### Community 85 - "Layering Tests"
Cohesion: 0.12
Nodes (17): build_meta(), export(), main(), _spans(), split_basmalah(), _write(), _absolute_imports(), _sources() (+9 more)

### Community 86 - "build_grid"
Cohesion: 0.14
Nodes (5): build_grid(), _counts(), level_for(), TestGrid, TestLevels

### Community 87 - "services/plans.py"
Cohesion: 0.08
Nodes (13): Portion, day_position(), match_portion(), plan_ref(), portion_for(), portions_of(), preview(), save_plan() (+5 more)

### Community 89 - "auth.py"
Cohesion: 0.13
Nodes (19): _b64url(), _b64url_decode(), decode_token(), InvalidToken, issue_token(), _sign(), _auth(), _jwt_secret() (+11 more)

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.12
Nodes (17): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+9 more)

### Community 92 - "unittest_mock"
Cohesion: 0.11
Nodes (6): _stress_reset(), _stress_stats(), data(), fake_bot(), TestVerseText, tg_bot()

### Community 95 - "parse_offset"
Cohesion: 0.15
Nodes (3): parse_offset(), TestParseOffset, TestPicker

### Community 97 - "test_media_cache_keys.py"
Cohesion: 0.17
Nodes (8): _bot(), _next_id(), send_audio(), send_photo(), no_cdn(), _source(), test_a_miss_caches_under_the_key_and_a_hit_replays_it(), test_a_rejected_cached_id_is_rebuilt_and_recached()

### Community 100 - "api/catalog.py"
Cohesion: 0.20
Nodes (10): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, put_position(), ReaderPosition, Reciter (+2 more)

### Community 101 - "MemoryStore"
Cohesion: 0.13
Nodes (7): 11.1 Profile settings reset after a while — `fix/settings-persistence`, 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, DatabaseUnavailable, get_pool(), _lock(), MemoryStore

### Community 102 - "weekly_board"
Cohesion: 0.28
Nodes (3): weekly_board(), make_user(), TestWeeklyBoard

### Community 103 - "Refactor — Implementation Plan"
Cohesion: 0.13
Nodes (14): button_rows() row-packing helper, Copy-pasted patterns table (§1.3), ignore_not_modified() context manager, tests/test_layering.py ratchet (KNOWN violations), Overlap with MULTI_PLATFORM_PLAN channel seam, Shared UTC offset picker (time_pickers.offset_keyboard), Decisions and open questions (§9), Found along the way (out-of-scope behaviour changes) (+6 more)

### Community 104 - "recall_check.py"
Cohesion: 0.04
Nodes (38): _answer_data(), _options_keyboard(), _assemble(), _at_offset(), _ayah_text(), _basmala_prefix(), build_question(), _clean() (+30 more)

### Community 105 - "._send_media"
Cohesion: 0.12
Nodes (5): _build(), ignore_not_modified(), _send(), send_cached(), build()

### Community 107 - "offset_keyboard"
Cohesion: 0.35
Nodes (7): offset_keyboard(), _grid(), test_a_label_prefix_changes_only_the_label(), test_cancel_data_adds_a_localized_cancel_row(), test_every_offset_is_offered_in_order_under_the_callers_prefix(), test_no_cancel_row_unless_asked(), test_rows_are_columns_wide()

### Community 108 - "scheduler/__init__.py"
Cohesion: 0.29
Nodes (3): catch_up(), run_scheduler(), _wait()

### Community 109 - "_plan_drill.py"
Cohesion: 0.05
Nodes (31): 5.2 Telegram message (bot), 1. Why, 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 2 — DRY the duplicated patterns — *done*, Phase 4 — Split infrastructure god-objects — *done*, Phase 5 — Fix the layering — *done*, Phase 6 — Repository hygiene — *done* (+23 more)

### Community 110 - "stats.py"
Cohesion: 0.31
Nodes (8): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut

### Community 111 - "send_page"
Cohesion: 0.29
Nodes (7): send_page(), _buffer(), _stub_stitch(), stub(), TestPageCard, capture(), counting()

### Community 113 - "store/__init__.py"
Cohesion: 0.10
Nodes (7): Caps, Incoming, _advance(), next_scheduled_date(), _validated_days(), HifzStore, MemoryState

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
Cohesion: 0.18
Nodes (5): user_week_window(), week_window(), WeeklyBoard, user_offset(), TestWeekWindow

### Community 119 - "Export Web Content Tests"
Cohesion: 0.22
Nodes (3): _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl()

### Community 121 - "_seed_legacy_lang"
Cohesion: 0.21
Nodes (3): _seed_legacy_lang(), TestInlineCaller, TestLegacyMigration

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
Cohesion: 0.12
Nodes (9): data(), fake_bot(), _message(), _no_network(), TestCommandArguments, TestJuzCommand, TestPageCommand, TestSajdaCommand (+1 more)

### Community 132 - "Mini App Plan: Separate quranayatminiapp Nextjs"
Cohesion: 0.12
Nodes (16): Audio catalog kinds, Inline query answering (all four representations, ranges), Navigation model ((surah, ayah, type) per chat_id), Page audio with stitched fallback, Page image stitching (lib/page_image.py), Repeat (memorization), Structural divisions (page / juz / sajda from quran-data.xml), Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES) (+8 more)

### Community 136 - "test_keyboard_snapshots.py"
Cohesion: 0.25
Nodes (5): _as_dict(), _keyboards(), _render(), _search_markup(), test_keyboards_match_their_snapshots()

### Community 140 - "Business Logic: The hifz platform memorization"
Cohesion: 0.13
Nodes (13): Central callback prefix allocation (hifz.PREFIXES), The hifz platform (memorization companion), Pure plan builder (build_plan), Streak day ticks on completed session, Bot ↔ Mini App integration (menu button, startapp, /app), Identity table (platform, external_id → user_id), Normalized Incoming event, Neutral message model rendering (HTML / WhatsApp markup) (+5 more)

### Community 141 - "PostgresStore"
Cohesion: 0.14
Nodes (3): PostgresStore, Store, store()

### Community 143 - "t"
Cohesion: 0.06
Nodes (38): command, Routing rules (in `serve`), 5. API surface (`/api/v1`), Phase 2 — WhatsApp MVP (reader + daily ayat), 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, Ctx, _ask() (+30 more)

### Community 144 - "get_language"
Cohesion: 0.17
Nodes (6): get_language(), is_supported(), is_ui_language(), Language, TestLanguageLookup, TestLanguageFlags

### Community 148 - "Hifz Seam Tests: test_hifz_seampy"
Cohesion: 0.18
Nodes (3): _isolate_registries(), _Settings, TestSchemaApplication

### Community 152 - "test_miniapp_links.py"
Cohesion: 0.24
Nodes (9): _app_command(), app_on(), data(), test_app_command(), test_app_command_without_url(), test_cards_and_drill_link_to_their_screens(), test_inline_messages_never_get_a_web_app_button(), test_off_by_default() (+1 more)

### Community 153 - ".test_concatenates_the_ayahs_in_order"
Cohesion: 0.18
Nodes (4): content(), fake_download(), TestStitching, __init__()

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 159 - "MINI_APP_PLAN.md"
Cohesion: 0.19
Nodes (11): /api/v1 REST surface, initData HMAC validation → short-lived JWT, OpenAPI → TypeScript client pipeline, Recall check integrity (signed question_token), Mini App risks, Other platforms shortlist (Messenger, Viber, Discord, PWA, Signal), Multi-platform phased breakdown (Phases 0-6), Multi-platform risks (+3 more)

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
Cohesion: 0.11
Nodes (13): Hifz platform frozen string manifest, src/locales/en.py source of truth, Key conventions (btn_*, cmd_*), Wave process (feature agents, translation agents, reviewers), Native-speaker review - hifz platform strings, Locale review tracking table (47 locales), Review process steps, Review criteria (meaning, register, grammatical number, RTL, button length) (+5 more)

### Community 166 - "domain/streaks.py"
Cohesion: 0.19
Nodes (5): Milestone, milestone_for(), _milestone_key(), offset_of(), TestMilestones

### Community 169 - "TestPickerFlow"
Cohesion: 0.14
Nodes (8): _callback(), data(), fake_bot(), _message(), _tab_row(), TestAudioNeverFollowsLanguage, TestPickerFlow, tg_bot()

### Community 170 - "button_action"
Cohesion: 0.11
Nodes (6): button_action(), missing_keys(), _placeholders(), TestButtonAction, TestGroupLocaleExemption, TestLocaleIntegrity

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 172 - "BismillahBot — Multilingual Support Plan"
Cohesion: 0.14
Nodes (14): 10. File-by-file change list, 11. Memory & performance (free-tier reality), 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 2. Current-state audit (what is hardcoded English), 3. Target architecture, 4. User language preference (+6 more)

### Community 173 - "load_summary"
Cohesion: 0.21
Nodes (4): ProgressSummary, SurahProgress, load_summary(), TestLoadSummary

### Community 175 - "parse_ayah_range"
Cohesion: 0.12
Nodes (5): parse_ayah(), parse_ayah_range(), parse_quran_tafsir(), TestParseAyah, TestParseAyahRange

### Community 176 - "BUSINESS_LOGIC.md"
Cohesion: 0.25
Nodes (5): Four ayah representations (english, tafsir, arabic, audio), Future roadmap and prioritized backlog, Known limitations / tech debt, Issues fixed in the refactor (12 bugs), Verse card (inline keyboard, edit in place)

### Community 178 - "BismillahBot README"
Cohesion: 0.12
Nodes (17): Translation Attributions, alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Documentation, Documentation index (docs/README.md), Phase 6 — Repository hygiene (+9 more)

### Community 179 - "8. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 8. Phased task breakdown, Phase 0 — Foundations, Phase 1 — Service-layer extraction (this repo, no UI change), Phase 2 — Reader parity (read-only, low risk, ships first), Phase 3 — Hifz parity, Phase 4 — Recitation checker UI (depends on the investigation's Phase A), Phase 5 — Later

### Community 180 - "register_send_handler"
Cohesion: 0.33
Nodes (3): register_send_handler(), _same_origin(), decorate()

### Community 181 - "json"
Cohesion: 0.27
Nodes (7): export(), languages(), main(), resolved_table(), _write(), build(), main_()

### Community 182 - "Blue Green Ci: deploygreen"
Cohesion: 0.33
Nodes (6): environment, if, name, needs, runs-on, deploy-green

### Community 183 - "Blue Green Ci: promote"
Cohesion: 0.33
Nodes (6): promote, environment, if, name, needs, runs-on

### Community 187 - "test_scheduler.py"
Cohesion: 0.16
Nodes (4): _isolate_handlers(), state(), store(), TestRunScheduler

### Community 193 - "11. Infrastructure, capacity and cost on paid Koyeb"
Cohesion: 0.33
Nodes (6): 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards, 11. Infrastructure, capacity and cost on paid Koyeb

### Community 200 - "user_settings.py"
Cohesion: 0.20
Nodes (4): resolve_settings(), UserSettingsRow, _legacy_lang_key(), SettingsRow

### Community 205 - "fetch_and_stitch"
Cohesion: 0.29
Nodes (4): fetch_and_stitch(), _fit_for_telegram(), _semaphore(), stitch_images()

### Community 284 - "miniapp.py"
Cohesion: 0.28
Nodes (5): app_button(), app_url(), set_menu_button(), test_menu_button(), test_menu_button_off_without_url()

### Community 286 - "test_export_web_content.py"
Cohesion: 0.39
Nodes (7): _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah(), test_meta_surahs_and_sajdas(), test_tafsir_has_every_ayah()

### Community 287 - "test_inline_range.py"
Cohesion: 0.36
Nodes (4): data(), fake_bot(), public_url(), tg_bot()

### Community 288 - "6. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 6. Phased task breakdown, Phase 0 — Prerequisites (no code), Phase 1 — Channel seam (this repo, no user-visible change), Phase 3 — Hifz on WhatsApp, Phase 4 — Recitation checker on WhatsApp, Phase 5 — Web access outside Telegram, Phase 6 — Later

## Knowledge Gaps
- **51 isolated node(s):** `Phase 0 — Guardrails (ruff, layering test, logging)`, `button_rows() row-packing helper`, `ignore_not_modified() context manager`, `Found along the way (out-of-scope behaviour changes)`, `CLAUDE.md graphify lookup rules` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1582 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **150 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `get_store` to `summarize`, `Leaderboard`, `_ctx`, `Profile`, `Store`, `render_streak_graph`, `PostgresStore`, `services/streaks.py`, `Context`, `User Settings`, `RedisSingleton`, `typing`, `Hifz Progress Cmd Tests`, `Hifz Streak Tests`, `Acceptance Tests`, `Session`, `Streaks`, `load_summary`, `Services`, `api/check.py`, `Dispatch`, `api/progress.py`, `test_hifz_check.py`, `_hifz`, `surah_progress`, `InMemoryIdentityStore`, `_plan_out`, `user_settings.py`, `api/plans.py`, `t`, `tick.py`, `TestAddInterval`, `MemoryStore`, `weekly_board`, `stats.py`, `store/__init__.py`, `services/leaderboard.py`?**
  _High betweenness centrality (0.122) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Phase 0 — Guardrails (ruff, layering test, logging)`, `button_rows() row-packing helper`, `ignore_not_modified() context manager` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_plan` be split into smaller, more focused modules?**
  _Cohesion score 0.05389876880984952 - nodes in this community are weakly interconnected._
- **Why does `Quran` connect `Quran` to `build_plan`, `.page_range`, `summarize`, `test_navigation.py`, `range_audio`, `Profile`, `t`, `Refs`, `typing`, `Hifz Progress Cmd Tests`, `test_export_web_content.py`, `TranslationRegistry`, `Ref`, `api/progress.py`, `.get_surah_length`, `surah_progress`, `t`, `Hifz Progress: juz_progress`, `BismillahBot — Business Logic`, `Layering Tests`, `services/plans.py`, `api/catalog.py`, `recall_check.py`, `_plan_drill.py`, `store/__init__.py`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Ctx` (e.g. with `3. Architecture` and `4.1 Overlap with `MULTI_PLATFORM_PLAN.md``) actually correct?**
  _`Ctx` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Should `.page_range` be split into smaller, more focused modules?**
  _Cohesion score 0.07200929152148665 - nodes in this community are weakly interconnected._