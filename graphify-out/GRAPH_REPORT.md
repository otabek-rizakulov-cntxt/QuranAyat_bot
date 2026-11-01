# Graph Report - QuranAyat_bot  (2026-11-02)

## Corpus Check
- 275 files · ~261,567 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 5107 nodes · 11771 edges · 327 communities (157 shown, 170 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1018 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dd97e502`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_plan
- link_token.py
- language_keyboard
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
- test_whatsapp_config.py
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
- test_reciter_picker.py
- Docker Compose.stress
- _png
- test_recall_check.py
- .get
- summarize
- _plan_preview.py
- Recitation Checker Investigation
- hifz_progress.py
- test_whatsapp_webhook.py
- reciter_keyboard
- auth.py
- PostgresPlanStore
- quran_page_progress
- test_hifz_cross_platform.py
- Streaks
- Load Test
- Multilingual Plan
- Text
- Schema
- Services
- router.py
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
- taps
- Mini App Plan
- services/check.py
- IdentityStore
- surah_progress
- scheduler/__init__.py
- weekly_board
- api/catalog.py
- reset_for_tests
- Hifz Seam Tests
- api/progress.py
- Ctx
- parse_offset
- tick.py
- Profiles: InMemoryProfileStore
- bundle_translations.py
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
- features/check.py
- test_store_contract.py
- .exists
- api/plans.py
- Quran
- stats.py
- send_page
- TestSchedule
- store/__init__.py
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- .get_next_ayah
- parse_ayah
- recall_check.py
- refresh_streaks
- _ask
- streak.py
- .page_range
- 4. Navigation model
- TestHelpers
- Blue Green Ci: jobs
- Blue Green Ci: with
- build_grid
- test_navigation.py
- bot/media.py
- Mini App Plan: Separate quranayatminiapp Nextjs
- InMemoryScheduleStore
- Channel
- range_audio
- reader.py
- InMemoryGroupStore
- Store Contract Tests: TestLeaderboard
- parse_ayah_range
- MINI_APP_PLAN.md
- ScheduleStore
- TestRestartDeliversExactlyOnce
- test_export_web_content.py
- locales/__init__.py
- normalize_lang
- percentile_band
- juz_progress
- to_markup
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- split
- link.py
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
- test_keyboard_snapshots.py
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
- .wa_user
- json
- TestBoard
- test_hifz_streak.py
- test_hifz_seam.py
- for_platform
- get_language
- graph
- test_the_basmala_heading_is_not_part_of_the_question
- sweep_refs
- test_short_surahs_still_get_four_distinct_options
- _AnyDay
- PostgresDailyStore
- _isolate_registries
- test_pick_ayah_accepts_anything_with_as_tuple
- test_media_cache_keys.py
- week_bounds
- get_store
- typing
- test_the_answer_is_not_findable_by_sorting_on_length
- test_sweep_produces_a_well_formed_question_everywhere
- test_options_are_distinct_even_ignoring_vowelling
- milestone_for
- test_prompt_is_never_offered_back_as_an_option
- test_correct_option_really_follows_the_prompt
- TestSettings
- test_both_question_modes_show_up_in_the_sweep
- _message
- test_next_ayah_mode_answers_with_the_whole_short_ayah
- test_long_ayah_prompt_and_options_stay_button_sized
- test_next_ayah_prompt_is_truncated_and_says_so
- MULTI_PLATFORM_PLAN.md
- test_every_option_carries_the_same_word_count
- level_for
- test_scheduler.py
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
- _callback
- 6. Phased task breakdown
- reciter_label
- TestTransliteration
- Identity table (platform, external_id → user_id)
- cache_key
- Routing rules in serve (inline, commands, type words, callbacks)
- TestRegistration
- TestRegistration

## God Nodes (most connected - your core abstractions)
1. `get_store()` - 173 edges
2. `Ctx` - 131 edges
3. `t()` - 128 edges
4. `Quran` - 118 edges
5. `handle_update()` - 93 edges
6. `UserSettings` - 79 edges
7. `build_plan()` - 72 edges
8. `parse_reference()` - 59 edges
9. `TelegramChannel` - 58 edges
10. `Ref` - 57 edges

## Surprising Connections (you probably didn't know these)
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `3. Target architecture` --references--> `TranslationRegistry`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/domain/quran.py
- `5. Caching strategy` --references--> `MemoryStore`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/infra/redis_client.py
- `Phase 3 — Hifz parity` --references--> `build_plan()`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/domain/plan_builder.py
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

## Communities (327 total, 170 thin omitted)

### Community 0 - "build_plan"
Cohesion: 0.05
Nodes (21): _advance(), advancing(), auto_pace(), build_plan(), next_scheduled_date(), _validated_days(), juz_ref(), surah_ref() (+13 more)

### Community 1 - "link_token.py"
Cohesion: 0.12
Nodes (10): _b64(), InvalidLinkToken, issue(), _key(), redeem(), _secret(), exchange(), test_whatsapp_app_sends_a_working_sign_in_link() (+2 more)

### Community 2 - "language_keyboard"
Cohesion: 0.19
Nodes (9): 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 2 — DRY the duplicated patterns — *done*, Phase 5 — Fix the layering — *done*, Phase 6 — Repository hygiene — *done*, language_keyboard(), language_picker(), translation_language_keyboard() (+1 more)

### Community 4 - "Wizard"
Cohesion: 0.07
Nodes (9): ctx(), Wizard, test_draft_is_written_with_that_ttl(), TestAccumulation, TestCancel, TestCorruptState, TestLifecycle, TestOneDraftPerUser (+1 more)

### Community 5 - "_plan_setup.py"
Cohesion: 0.07
Nodes (39): memorize(), on_tap(), plan_step(), _expired(), _ref_from_draft(), _ref_to_draft(), _know_by_heart(), _send_drill() (+31 more)

### Community 6 - "features/profile.py"
Cohesion: 0.07
Nodes (26): create(), _profile(), _cancel_keyboard(), _join_board(), name_step(), offset_from_callback(), on_profile_tap(), _plan_line() (+18 more)

### Community 7 - "next_due_utc"
Cohesion: 0.14
Nodes (8): _as_utc(), local_date(), local_now(), local_time(), next_due_utc(), TestLocalDate, TestNextDueUtc, _utc()

### Community 8 - "to_whatsapp"
Cohesion: 0.17
Nodes (3): to_whatsapp(), TestTags, TestWhatTheBotSends

### Community 9 - "_ctx"
Cohesion: 0.16
Nodes (7): _CallbackQuery, _ctx(), _isolate_registries(), _Message, _sent(), _Settings, TestDispatch

### Community 10 - "_ctx"
Cohesion: 0.08
Nodes (17): _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _isolate_registries(), _Message, _profile_row() (+9 more)

### Community 11 - "services/plans.py"
Cohesion: 0.08
Nodes (23): active(), _plan_out(), today(), change_status(), complete_day(), current_plan(), day_position(), DrillResult (+15 more)

### Community 12 - "Store"
Cohesion: 0.10
Nodes (10): _CallbackQuery, _ctx(), _Message, _run_wizard(), _Settings, _tap(), TestDrill, TestEnqueueChain (+2 more)

### Community 13 - "render_streak_graph"
Cohesion: 0.14
Nodes (7): render(), draw_contribution_graph(), render_streak_graph(), _semaphore(), open_png(), TestRendering, TestRenderStreakGraph

### Community 14 - "test_whatsapp_config.py"
Cohesion: 0.31
Nodes (5): env(), test_any_missing_value_keeps_it_off(), test_off_by_default(), test_on_when_fully_configured(), test_the_flag_must_be_truthy()

### Community 15 - "UserSettings"
Cohesion: 0.05
Nodes (40): init_data_max_age(), auth_link(), auth_telegram(), AuthOut, LinkAuthIn, me(), _me(), MeOut (+32 more)

### Community 16 - "Context"
Cohesion: 0.14
Nodes (15): _bot(), _ctx(), _isolate_registries(), _member(), _run_setup_to_plan(), _Settings, TestBoard, tap() (+7 more)

### Community 17 - "test_store_selection.py"
Cohesion: 0.07
Nodes (15): health(), store_backend(), database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries(), fresh_redis() (+7 more)

### Community 18 - "Refs"
Cohesion: 0.07
Nodes (11): _clean(), format_ref(), parse_range(), parse_reference(), TestSurahSpans, TestAcrossSurahs, TestFormatting, TestJuzAndPage (+3 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.05
Nodes (17): 6. Issues fixed in this refactor, 11.1 Profile settings reset after a while — `fix/settings-persistence`, 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, forget(), _key(), pick(), remember() (+9 more)

### Community 20 - "lifespan.py"
Cohesion: 0.04
Nodes (35): create_app(), _commands_for(), initialize(), lifespan(), _set_bot_commands(), _process_update(), telegram_webhook(), webhook_secret() (+27 more)

### Community 21 - "WhatsAppChannel"
Cohesion: 0.16
Nodes (5): _bytes_and_name(), _clip(), _resolve(), _split_choices(), WhatsAppChannel

### Community 22 - "InMemoryIdentityStore"
Cohesion: 0.12
Nodes (3): InMemoryIdentityStore, PostgresIdentityStore, _stored()

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "group.py"
Cohesion: 0.06
Nodes (30): 1. Why, _begin_setup(), bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), _enqueue_next_board() (+22 more)

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.09
Nodes (23): graphify knowledge graph (graphify-out/), CLAUDE.md graphify lookup rules, 10. Found along the way (out of scope — behaviour changes), 2. Goals and non-goals, 3. Principles applied, 6. Ordering, risk, size, 7. Safety net, 8. Expected result (+15 more)

### Community 26 - "TelegramChannel"
Cohesion: 0.10
Nodes (6): TelegramChannel, TestAnswerAndTyping, TestEditChoices, TestEditText, TestMedia, TestSendText

### Community 27 - "Hifz Streak Tests"
Cohesion: 0.18
Nodes (6): _caption(), _earn(), _streak(), TestGraphCache, TestMilestones, TestStreakCard

### Community 28 - "Hifz Platform"
Cohesion: 0.07
Nodes (27): Hifz Platform - Plan & Progress, Phase 1 acceptance criteria (tests/test_acceptance.py), Hifz change log, claim_due claimed_at clock bug, Hifz data model (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send, group_*), Phase 2 group cluster (J1-J6, forum topics), Workstream I: i18n & commands for 48 locales, Workstream C: interval merge-on-insert + derived percentages (+19 more)

### Community 29 - "Acceptance Tests"
Cohesion: 0.09
Nodes (14): _CallbackQuery, _cmd(), _ctx(), _isolate_registries(), _Message, _run_wizard(), _save_plan(), _Settings (+6 more)

### Community 30 - "test_reciter_picker.py"
Cohesion: 0.05
Nodes (21): Phase 4 — Split infrastructure god-objects — *done*, _search_reciters(), reciter_page_of(), reciter_search_keyboard(), reciter_set_confirmation(), send_quran(), audio_url(), find() (+13 more)

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 33 - "test_recall_check.py"
Cohesion: 0.15
Nodes (4): test_options_need_no_html_escaping_beyond_the_callers(), test_pick_ayah_is_deterministic_per_user_and_date(), test_pick_ayah_on_an_inverted_or_empty_span(), test_unknown_ayahs_are_rejected()

### Community 34 - ".get"
Cohesion: 0.08
Nodes (7): 12. Testing, parse_quran(), TranslationRegistry, TestCorpusIntegrity, TestAvailable, TestCaching, TestFallback

### Community 35 - "summarize"
Cohesion: 0.09
Nodes (5): Progress, summarize(), SurahProgress, HifzInterval, TestSummarize

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.07
Nodes (29): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards (+21 more)

### Community 38 - "hifz_progress.py"
Cohesion: 0.08
Nodes (5): format_percent(), PageProgress, _Ratio, round_percent(), TestRounding

### Community 39 - "test_whatsapp_webhook.py"
Cohesion: 0.08
Nodes (18): signature(), tg_bot(), _isolate_registries(), _isolate_registries(), configured(), app_on(), data(), store() (+10 more)

### Community 40 - "reciter_keyboard"
Cohesion: 0.19
Nodes (5): reciter_keyboard(), reciter_page_count(), _pager_row(), _reciter_buttons(), TestPagination

### Community 41 - "auth.py"
Cohesion: 0.20
Nodes (13): _b64url(), _b64url_decode(), decode_token(), InvalidToken, issue_token(), _sign(), _unauthorized(), _unb64() (+5 more)

### Community 42 - "PostgresPlanStore"
Cohesion: 0.07
Nodes (4): PlanDayRow, PlanRow, PlanStore, PostgresPlanStore

### Community 43 - "quran_page_progress"
Cohesion: 0.11
Nodes (4): juz_page_progress(), quran_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 44 - "test_hifz_cross_platform.py"
Cohesion: 0.09
Nodes (7): _stress_reset(), _stress_stats(), data(), no_cdn(), Telegram, test_a_week_on_whatsapp_matches_a_week_on_telegram(), _week()

### Community 45 - "Streaks"
Cohesion: 0.14
Nodes (4): record_session(), TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 46 - "Load Test"
Cohesion: 0.14
Nodes (12): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+4 more)

### Community 47 - "Multilingual Plan"
Cohesion: 0.14
Nodes (13): Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), Quran.from_file(path) refactor, setMyCommands per language, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+5 more)

### Community 48 - "Text"
Cohesion: 0.20
Nodes (7): reference(), _inline_query(), _of_type(), _results(), TestInlineArabicImage, TestRangeAudio, TestRangeText

### Community 49 - "Schema"
Cohesion: 0.11
Nodes (27): daily_ayah_sub, group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval (+19 more)

### Community 50 - "Services"
Cohesion: 0.15
Nodes (20): client(), _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today() (+12 more)

### Community 51 - "router.py"
Cohesion: 0.10
Nodes (16): Phase 3 — One router for everything — *done*, _on_text(), decorate(), decorate(), dispatch_callback(), dispatch_command(), handles(), handles_callback() (+8 more)

### Community 52 - "Dispatch"
Cohesion: 0.17
Nodes (19): handle_update(), _callback(), data(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index() (+11 more)

### Community 55 - "Inline Reciter Search Tests"
Cohesion: 0.14
Nodes (19): _audio_result(), data(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter(), test_ayah_audio_dropped_without_public_base_url(), test_ayah_audio_uses_callers_reciter() (+11 more)

### Community 56 - "test_hifz_check.py"
Cohesion: 0.23
Nodes (6): _answer_data(), _asked(), _sessions(), _tap(), TestScoring, TestStaleButtons

### Community 57 - "deliver_push"
Cohesion: 0.23
Nodes (9): deliver_push(), _log(), ctx_for(), say_hi(), test_every_push_is_logged_for_cost_tracking(), TestConsent, TestTelegram, TestWhatsApp (+1 more)

### Community 58 - "os"
Cohesion: 0.14
Nodes (15): _modules(), test_nothing_builds_telegram_markup_by_hand_outside_those_modules(), test_only_group_code_reads_the_telegram_client(), test_only_telegram_only_modules_import_telegram(), _absolute_imports(), _sources(), test_known_violations_still_exist(), test_no_new_violations() (+7 more)

### Community 60 - "test_hifz_keyboard_snapshots.py"
Cohesion: 0.33
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
Cohesion: 0.13
Nodes (9): build_question(), pick_ayah(), preload_corpus(), RecallQuestion, ask(), default_span(), rebuild(), Score (+1 more)

### Community 67 - "surah_progress"
Cohesion: 0.07
Nodes (8): quran_progress(), started_surahs(), surah_progress(), _at(), TestInputHandling, TestQuranProgress, TestSpecAcceptance, TestSurahProgress

### Community 68 - "scheduler/__init__.py"
Cohesion: 0.12
Nodes (9): enqueue(), idempotency_key(), schedule_daily(), register_send_handler(), registered_kinds(), _same_origin(), send_handler(), decorate() (+1 more)

### Community 69 - "weekly_board"
Cohesion: 0.28
Nodes (3): weekly_board(), make_user(), TestWeeklyBoard

### Community 70 - "api/catalog.py"
Cohesion: 0.20
Nodes (10): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, put_position(), ReaderPosition, Reciter (+2 more)

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 73 - "api/progress.py"
Cohesion: 0.08
Nodes (29): jwt_secret(), require_user(), answer(), AnswerIn, AnswerOut, make_token(), question(), QuestionOut (+21 more)

### Community 74 - "Ctx"
Cohesion: 0.06
Nodes (43): command, Routing rules (in `serve`), 5. API surface (`/api/v1`), Phase 2 — WhatsApp MVP (reader + daily ayat), 7. The keyboard & command localization challenge, Telegram command menu, 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering (+35 more)

### Community 75 - "parse_offset"
Cohesion: 0.10
Nodes (5): format_offset(), parse_offset(), TestFormatOffset, TestParseOffset, TestPicker

### Community 76 - "tick.py"
Cohesion: 0.13
Nodes (12): catch_up(), run_scheduler(), _wait(), _deliver(), _is_stale(), _lock(), _release(), _resolve() (+4 more)

### Community 78 - "bundle_translations.py"
Cohesion: 0.13
Nodes (8): _clean_state_store(), bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.13
Nodes (16): Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points), Error taxonomy L1-L5 (word, harakah, tajwid, riwayah mismatch, waqf), Evaluation plan (false-alarm gate < 2% per ayah), IqraEval 2025 shared task, Recitation checker phased roadmap (A-1 to E) (+8 more)

### Community 80 - "BismillahBot — Business Logic"
Cohesion: 0.11
Nodes (17): 1. Overview, 2. Architecture, 3. Request lifecycle, 5. Caching strategy, 7. Known limitations / tech debt, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic (+9 more)

### Community 81 - "Streaks: compute_streak"
Cohesion: 0.21
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 83 - "SessionStore"
Cohesion: 0.07
Nodes (5): InMemorySessionStore, LeaderboardEntry, PostgresSessionStore, SessionRow, SessionStore

### Community 84 - "Scheduler Tests"
Cohesion: 0.17
Nodes (4): _claimed_at(), _record(), TestCatchUp, TestTick

### Community 85 - "export"
Cohesion: 0.18
Nodes (7): build_meta(), export(), main(), _spans(), split_basmalah(), _write(), parse_quran_tafsir()

### Community 86 - "whatsapp_format.py"
Cohesion: 0.20
Nodes (3): _Converter, _render(), _wrap()

### Community 87 - "_clip"
Cohesion: 0.09
Nodes (14): _clip(), _covered(), _focus_surah(), _intersect(), _page_share(), _pages_of(), _recency_key(), _surah_of() (+6 more)

### Community 89 - "auth.py"
Cohesion: 0.12
Nodes (23): _init_data_secret(), InvalidInitData, sign_init_data(), validate_init_data(), _auth(), _fields(), _jwt_secret(), test_added_field_is_rejected() (+15 more)

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.12
Nodes (17): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+9 more)

### Community 92 - "dispatch.py"
Cohesion: 0.07
Nodes (21): handle_incoming(), _incoming(), _on_callback(), app_button(), app_link(), app_url(), set_menu_button(), to_button() (+13 more)

### Community 93 - "_hifz"
Cohesion: 0.07
Nodes (10): _assert_invariant(), _ayahs(), _hifz(), _spans(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order(), TestAddInterval (+2 more)

### Community 94 - "Dependency rule (app -> bot -> services -> domain)"
Cohesion: 0.18
Nodes (10): tests/test_layering.py ratchet (KNOWN violations), Overlap with MULTI_PLATFORM_PLAN channel seam, Shared UTC offset picker (time_pickers.offset_keyboard), Decisions and open questions (§9), Found along the way (out-of-scope behaviour changes), Phase 0 — Guardrails (ruff, layering test, logging), Phase 5 — Fix the layering, Target layout (app/ bot/ services/ domain/ infra/) (+2 more)

### Community 95 - "handle_message"
Cohesion: 0.06
Nodes (29): _allowed_command(), as_command(), handle_message(), lang_hint(), _tap(), _buttons(), _due_rows(), graph() (+21 more)

### Community 101 - "TestStateStore"
Cohesion: 0.06
Nodes (9): image_url(), page_audio_url(), page_image_url(), File, TestAudioFilename, TestImageFilename, TestLegacyLanguageKey, TestStateStore (+1 more)

### Community 103 - "week_bounds"
Cohesion: 0.16
Nodes (5): user_week_window(), week_window(), WeeklyBoard, user_offset(), TestWeekWindow

### Community 104 - "recall_check.py"
Cohesion: 0.10
Nodes (14): _assemble(), _continuation_question(), display_length(), _distinct(), _everything(), _gather(), is_similar_length(), _key() (+6 more)

### Community 105 - "features/check.py"
Cohesion: 0.18
Nodes (7): _answer_data(), _ask(), check(), on_check(), _options_keyboard(), _question_text(), _score()

### Community 107 - ".exists"
Cohesion: 0.08
Nodes (8): TestEveryParsedRefIsReal, TestSajdaCommand, TestExists, TestRandom, TestStructure, TestSurahMeta, test_pick_ayah_handles_a_cross_surah_span(), test_the_whole_quran_is_a_valid_span()

### Community 108 - "api/plans.py"
Cohesion: 0.15
Nodes (16): RefOut, _build(), complete(), DrillOut, lifecycle(), PlanCreateIn, PlanDayOut, PlanOut (+8 more)

### Community 109 - "Quran"
Cohesion: 0.06
Nodes (19): Phase 1 — Take `main.py` apart (pure moves) — *done*, surah_name(), _translation_text(), forgot_command(), on_progress_tap(), progress_command(), progress_view(), _show() (+11 more)

### Community 110 - "stats.py"
Cohesion: 0.35
Nodes (8): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut

### Community 111 - "send_page"
Cohesion: 0.29
Nodes (7): send_page(), _buffer(), _stub_stitch(), stub(), TestPageCard, capture(), counting()

### Community 113 - "store/__init__.py"
Cohesion: 0.08
Nodes (8): DailyStore, DailySubRow, InMemoryDailyStore, HifzStore, InMemoryHifzStore, InMemoryStore, Store, MemoryState

### Community 115 - "Koyeb Capacity Report"
Cohesion: 0.25
Nodes (7): Koyeb free-tier capacity report, CPU-bound queueing failure mode (~24 msg/s ceiling), Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start), Neon managed Postgres, Capacity results 5-1000 concurrent (no errors, 70-91 MB), Stress environment (docker-compose.stress.yml, cpus 0.1, 512m), Synthetic traffic mix (scripts/stress/gen_updates.py)

### Community 116 - "Blue Green Ci"
Cohesion: 0.14
Nodes (13): concurrency, cancel-in-progress, group, env, PYTHON_DEFAULT, name, on, pull_request (+5 more)

### Community 117 - "Blue Green Ci: name"
Cohesion: 0.23
Nodes (14): steps, steps, steps, steps, steps, steps, steps, env (+6 more)

### Community 120 - "recall_check.py"
Cohesion: 0.12
Nodes (12): _at_offset(), _ayah_text(), _basmala_prefix(), _clean(), corpus(), _date_key(), _option_from(), pick_ayahs() (+4 more)

### Community 121 - "refresh_streaks"
Cohesion: 0.25
Nodes (4): refresh_streaks(), streak_summary(), user_today(), TestRefreshAndSummary

### Community 122 - "_ask"
Cohesion: 0.15
Nodes (8): _parse_answer(), _ask(), _buttons(), _callback_query(), _ctx(), _Settings, TestCallbackDataDiscipline, TestCheckEntryPoint

### Community 123 - "streak.py"
Cohesion: 0.14
Nodes (10): _caption(), _keyboard(), on_streak(), _send_graph(), streak(), Milestone, offset_of(), StreakCounts (+2 more)

### Community 125 - "4. Navigation model"
Cohesion: 0.29
Nodes (8): 4. Navigation model, Audio catalog kinds, Page images and page audio, Repeat (memorization), Structural divisions (page / juz / sajda), Translation-only catalogue entries, Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES), Mini App feature parity map

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
Cohesion: 0.16
Nodes (8): 2. Current-state audit (what is hardcoded English), build_data(), make_index(), data(), data(), fake_bot(), _no_network(), tg_bot()

### Community 131 - "bot/media.py"
Cohesion: 0.06
Nodes (17): stitch(), deliver_repeated_audio(), stitch(), download_combined_audio(), download_stitched_audio(), fetch_and_stitch(), _fit_for_telegram(), _semaphore() (+9 more)

### Community 132 - "Mini App Plan: Separate quranayatminiapp Nextjs"
Cohesion: 0.22
Nodes (10): Page audio with stitched fallback, Page image stitching (lib/page_image.py), Structural divisions (page / juz / sajda from quran-data.xml), Uthmani text in Amiri Quran / KFGQPC font, Client-side playlist audio (no server stitching), Locale export to JSON (web_ keys, next-intl), Static immutable Quran JSON served from frontend CDN, Daily ayat cost model on WhatsApp (+2 more)

### Community 135 - "range_audio"
Cohesion: 0.11
Nodes (6): range_audio(), content(), TestRangeAudioRoute, fake_download(), TestStitching, __init__()

### Community 136 - "reader.py"
Cohesion: 0.15
Nodes (10): session(), random_ayah(), read_text(), reader_position(), _send_verse(), verse_card(), deliver_combined_audio(), deliver_quran() (+2 more)

### Community 137 - "InMemoryGroupStore"
Cohesion: 0.06
Nodes (6): GroupConfig, GroupMemberLink, GroupPlanDayRow, GroupPlanRow, GroupStore, InMemoryGroupStore

### Community 139 - "parse_ayah_range"
Cohesion: 0.23
Nodes (3): parse_ayah_range(), TestCommandArguments, TestParseAyahRange

### Community 140 - "MINI_APP_PLAN.md"
Cohesion: 0.22
Nodes (7): Central callback prefix allocation (hifz.PREFIXES), Future roadmap and prioritized backlog, The hifz platform (memorization companion), Pure plan builder (build_plan), Streak day ticks on completed session, recitation_job table and user_profile.riwayah, /recite flow (voice note → recitation_job → report)

### Community 143 - "test_export_web_content.py"
Cohesion: 0.14
Nodes (10): _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl(), _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah() (+2 more)

### Community 144 - "locales/__init__.py"
Cohesion: 0.06
Nodes (12): resolve_settings(), _now(), opt_out(), setup_logging(), _load_locales(), _module_name(), data(), TestCodes (+4 more)

### Community 145 - "normalize_lang"
Cohesion: 0.18
Nodes (5): is_supported(), is_ui_language(), Language, normalize_lang(), TestNormalizeLang

### Community 147 - "juz_progress"
Cohesion: 0.16
Nodes (5): juz_progress(), JuzProgress, _spans(), started_juzs(), TestJuzProgress

### Community 148 - "to_markup"
Cohesion: 0.19
Nodes (5): verse_keyboard(), to_markup(), TestToMarkup, _button(), TestVerseKeyboard

### Community 153 - "link.py"
Cohesion: 0.23
Nodes (8): _is_telegram_id(), link(), unlink(), _code_key(), issue(), redeem(), too_many_tries(), _tries_key()

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 155 - "test_channels_whatsapp.py"
Cohesion: 0.09
Nodes (7): cache(), channel(), graph(), Graph, TestText, TestTransport, TestVoiceNotes

### Community 158 - "Profile settings reset fix (fix/settings-persistence)"
Cohesion: 0.29
Nodes (8): ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable, lib/utils.File god class, Silent in-memory store fallback, Phase 4 — Split infrastructure god-objects, Profile settings reset fix (fix/settings-persistence), Typed frozen Settings (config/settings.py), conftest.py test environment (src on path, CWD pin, no Redis/network), Environment configuration (webhook, CDN base URLs, Redis)

### Community 159 - "MINI_APP_PLAN.md"
Cohesion: 0.21
Nodes (7): Navigation model ((surah, ayah, type) per chat_id), /api/v1 REST surface, Bot ↔ Mini App integration (menu button, startapp, /app), OpenAPI → TypeScript client pipeline, Recall check integrity (signed question_token), Mini App risks, Neutral message model rendering (HTML / WhatsApp markup)

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
Cohesion: 0.05
Nodes (16): main(), placeholders(), button_action(), command_lines(), keyboard_rows(), missing_keys(), missing_locales(), _reverse_button_map() (+8 more)

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 172 - "TranslationRegistry"
Cohesion: 0.11
Nodes (20): 10. File-by-file change list, 11. Memory & performance (free-tier reality), 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 3. Target architecture, 4. User language preference, 6. UI internationalization (i18n) (+12 more)

### Community 175 - "test_keyboard_snapshots.py"
Cohesion: 0.25
Nodes (5): _as_dict(), _keyboards(), _render(), _search_markup(), test_keyboards_match_their_snapshots()

### Community 178 - "BismillahBot README"
Cohesion: 0.12
Nodes (14): Translation Attributions, alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Four ayah representations (english, tafsir, arabic, audio), Known limitations / tech debt, Issues fixed in the refactor (12 bugs) (+6 more)

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
Cohesion: 0.23
Nodes (3): _consolidations(), ayah_count(), TestAyahCount

### Community 194 - "send_repeated_audio"
Cohesion: 0.26
Nodes (3): send_repeated_audio(), _stub_audio(), TestRepeatForMemorization

### Community 196 - "8. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 8. Phased task breakdown, Phase 0 — Foundations, Phase 1 — Service-layer extraction (this repo, no UI change), Phase 2 — Reader parity (read-only, low risk, ships first), Phase 3 — Hifz parity, Phase 4 — Recitation checker UI (depends on the investigation's Phase A), Phase 5 — Later

### Community 197 - ".wa_user"
Cohesion: 0.36
Nodes (4): apps(), Apps, _code(), TestLinking

### Community 199 - "json"
Cohesion: 0.27
Nodes (7): export(), languages(), main(), resolved_table(), _write(), build(), main_()

### Community 200 - "TestBoard"
Cohesion: 0.29
Nodes (3): _earn(), _join(), TestBoard

### Community 205 - "test_hifz_streak.py"
Cohesion: 0.24
Nodes (5): _ctx(), _photo_message(), _Settings, TestCallback, TestWhatTicksADay

### Community 206 - "test_hifz_seam.py"
Cohesion: 0.18
Nodes (3): _isolate_registries(), _Settings, TestSchemaApplication

### Community 207 - "for_platform"
Cohesion: 0.22
Nodes (3): for_platform(), TestForPlatform, TestTheRest

### Community 208 - "get_language"
Cohesion: 0.22
Nodes (3): get_language(), TestLanguageLookup, TestLanguageFlags

### Community 214 - "PostgresDailyStore"
Cohesion: 0.23
Nodes (3): PostgresDailyStore, PostgresStore, store()

### Community 266 - "test_media_cache_keys.py"
Cohesion: 0.11
Nodes (11): send_page_audio(), has_page_audio(), _bot(), _next_id(), send_audio(), send_photo(), no_cdn(), _source() (+3 more)

### Community 269 - "get_store"
Cohesion: 0.14
Nodes (6): get_store(), _lock(), _added_update(), TestAdded, TestDailyPost, TestLoadSummary

### Community 270 - "typing"
Cohesion: 0.05
Nodes (29): _ask_time(), daily(), _enable(), _hhmm(), _offset(), on_tap(), _parse_time(), push_daily() (+21 more)

### Community 275 - "milestone_for"
Cohesion: 0.33
Nodes (3): milestone_for(), _milestone_key(), TestMilestones

### Community 286 - "_message"
Cohesion: 0.33
Nodes (3): _message(), TestJuzCommand, TestPageCommand

### Community 290 - "MULTI_PLATFORM_PLAN.md"
Cohesion: 0.29
Nodes (7): initData HMAC validation → short-lived JWT, Other platforms shortlist (Messenger, Viber, Discord, PWA, Signal), Multi-platform phased breakdown (Phases 0-6), Multi-platform risks, Signed magic link for web access outside Telegram, Meta WhatsApp Cloud API (direct, no BSP), WhatsApp webhook (X-Hub-Signature-256, ack-then-process)

### Community 293 - "test_scheduler.py"
Cohesion: 0.32
Nodes (3): _isolate_handlers(), state(), store()

### Community 318 - "6. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 6. Phased task breakdown, Phase 0 — Prerequisites (no code), Phase 1 — Channel seam (this repo, no user-visible change), Phase 3 — Hifz on WhatsApp, Phase 4 — Recitation checker on WhatsApp, Phase 5 — Web access outside Telegram, Phase 6 — Later

### Community 321 - "Identity table (platform, external_id → user_id)"
Cohesion: 0.50
Nodes (5): Identity table (platform, external_id → user_id), Normalized Incoming event, WhatsApp opt-in / STOP opt-out flow, WhatsApp constraints (24-h window, templates, pricing, opt-in), Window-aware scheduler (session message vs template)

## Knowledge Gaps
- **51 isolated node(s):** `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres`, `Capacity results 5-1000 concurrent (no errors, 70-91 MB)`, `Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES)` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1742 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **170 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `get_store` to `features/profile.py`, `reader.py`, `_ctx`, `_ctx`, `services/plans.py`, `Store`, `render_streak_graph`, `UserSettings`, `Context`, `locales/__init__.py`, `RedisSingleton`, `lifespan.py`, `Hifz Progress Cmd Tests`, `Hifz Streak Tests`, `Acceptance Tests`, `summarize`, `test_hifz_cross_platform.py`, `Streaks`, `Services`, `Dispatch`, `test_hifz_check.py`, `test_hifz_keyboard_snapshots.py`, `WhatsApp`, `surah_progress`, `weekly_board`, `.wa_user`, `TestBoard`, `api/progress.py`, `Ctx`, `tick.py`, `PostgresDailyStore`, `dispatch.py`, `_hifz`, `handle_message`, `week_bounds`, `api/plans.py`, `stats.py`, `store/__init__.py`, `refresh_streaks`, `_ask`, `streak.py`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Are the 49 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 49 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_plan` be split into smaller, more focused modules?**
  _Cohesion score 0.04606891300209404 - nodes in this community are weakly interconnected._
- **Why does `Quran` connect `Quran` to `build_plan`, `bot/media.py`, `_plan_setup.py`, `features/profile.py`, `range_audio`, `reader.py`, `services/plans.py`, `test_export_web_content.py`, `Refs`, `juz_progress`, `lifespan.py`, `Hifz Progress Cmd Tests`, `_message`, `.get`, `summarize`, `quran_page_progress`, `.get_surah_length`, `services/check.py`, `surah_progress`, `api/catalog.py`, `api/progress.py`, `Ctx`, `BismillahBot — Business Logic`, `sweep_refs`, `test_short_surahs_still_get_four_distinct_options`, `export`, `_clip`, `recall_check.py`, `features/check.py`, `.exists`, `.get_next_ayah`, `recall_check.py`, `.page_range`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `Ctx` (e.g. with `3. Architecture` and `4.1 Overlap with `MULTI_PLATFORM_PLAN.md``) actually correct?**
  _`Ctx` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Should `link_token.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12258064516129032 - nodes in this community are weakly interconnected._