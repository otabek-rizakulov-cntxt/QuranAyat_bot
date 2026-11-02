# Graph Report - QuranAyat_bot  (2026-11-02)

## Corpus Check
- 275 files · ~262,276 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 5116 nodes · 11798 edges · 328 communities (156 shown, 172 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1047 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b6d8018a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_plan
- link_token.py
- Phase 1 — Take `main.py` apart (pure moves) — *done*
- session.py
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
- infra/catalog.py
- Docker Compose.stress
- _png
- test_recall_check.py
- .get
- test_reciter_picker.py
- _plan_preview.py
- Recitation Checker Investigation
- hifz_progress.py
- fixture
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
- Ctx
- Dispatch
- PlanDaySpec
- PostgresProfileStore
- Inline Reciter Search Tests
- test_daily_feature.py
- MemoryStore
- os
- PostgresScheduleStore
- test_hifz_keyboard_snapshots.py
- Dispatch Order Tests
- taps
- Mini App Plan
- services/check.py
- IdentityStore
- surah_progress
- SendCtx
- weekly_board
- api/catalog.py
- reset_for_tests
- Hifz Seam Tests
- api/progress.py
- reader.py
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
- parse_quran_tafsir
- whatsapp_format.py
- _clip
- auth.py
- Store Contract Tests
- Multi Platform Plan: MultiPlatform Implementation Plan
- telegram
- _hifz
- Dependency rule (app -> bot -> services -> domain)
- test_whatsapp_router.py
- Hifz Seam Tests: TestRegistration
- handle_message
- Scheduler Tests: TestTransientFailuresAreRetried
- Store Contract Tests: TestPlans
- GraphClient
- TestStateStore
- _at
- week_bounds
- recall_check.py
- _seed_legacy_lang
- test_store_contract.py
- Hifz platform frozen string manifest
- PostgresPlanStore
- quran.py
- stats.py
- test_page_mode.py
- TestSchedule
- store/__init__.py
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- .get_next_ayah
- parse_ayah
- corpus
- refresh_streaks
- build_question
- _send_graph
- Quran
- 4. Navigation model
- TestHelpers
- Blue Green Ci: jobs
- Blue Green Ci: with
- build_grid
- test_navigation.py
- test_inline_range.py
- Mini App Plan: Separate quranayatminiapp Nextjs
- InMemoryScheduleStore
- Channel
- range_audio
- Phase 2 — DRY the duplicated patterns
- InMemoryGroupStore
- main.py
- parse_ayah_range
- MINI_APP_PLAN.md
- ScheduledSend
- TestRestartDeliversExactlyOnce
- test_export_web_content.py
- dispatch.py
- normalize_lang
- percentile_band
- juz_progress
- to_markup
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- split
- offset_keyboard
- Blue Green Ci: env
- test_channels_whatsapp.py
- TestProfiles
- graphify-autopush.sh
- Profile settings reset fix (fix/settings-persistence)
- MINI_APP_PLAN.md
- Settings Tests
- fetch_and_stitch
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
- test_channels_telegram.py
- Hifz Seam Tests: test_longest_prefix_wins
- .get_surah_length
- TestIdentity
- Claude
- WhatsApp
- re
- Hifz Seam Tests: TestDispatchCommand
- 8. Phased task breakdown
- .wa_user
- json
- features/leaderboard.py
- test_hifz_streak.py
- test_hifz_seam.py
- for_platform
- get_language
- as_command
- test_the_basmala_heading_is_not_part_of_the_question
- sweep_refs
- test_short_surahs_still_get_four_distinct_options
- _AnyDay
- PostgresDailyStore
- UserSettingsRow
- test_pick_ayah_accepts_anything_with_as_tuple
- Graph
- week_bounds
- TestDailyPost
- typing
- test_the_answer_is_not_findable_by_sorting_on_length
- test_sweep_produces_a_well_formed_question_everywhere
- test_options_are_distinct_even_ignoring_vowelling
- milestone_for
- test_prompt_is_never_offered_back_as_an_option
- test_correct_option_really_follows_the_prompt
- 11. Infrastructure, capacity and cost on paid Koyeb
- test_both_question_modes_show_up_in_the_sweep
- TestFiveAndSixTheBoard
- test_next_ayah_mode_answers_with_the_whole_short_ayah
- test_long_ayah_prompt_and_options_stay_button_sized
- test_next_ayah_prompt_is_truncated_and_says_so
- .test_sends_todays_ayah_and_queues_tomorrow
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
- _bytes_and_name
- reciter_label
- TestTransliteration
- _lock
- cache_key
- TestRegistration
- _legacy_lang_key
- _isolate_registries

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
- `5. Caching strategy` --references--> `MemoryStore`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/infra/redis_client.py
- `3. Target architecture` --references--> `TranslationRegistry`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/domain/quran.py
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
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

## Communities (328 total, 172 thin omitted)

### Community 0 - "build_plan"
Cohesion: 0.05
Nodes (21): _advance(), advancing(), auto_pace(), build_plan(), next_scheduled_date(), _validated_days(), juz_ref(), surah_ref() (+13 more)

### Community 1 - "link_token.py"
Cohesion: 0.12
Nodes (11): _b64(), InvalidLinkToken, issue(), _key(), redeem(), _secret(), _unb64(), exchange() (+3 more)

### Community 2 - "Phase 1 — Take `main.py` apart (pure moves) — *done*"
Cohesion: 0.08
Nodes (25): 5. API surface (`/api/v1`), Phase 2 — WhatsApp MVP (reader + daily ayat), 1. Why, 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 1 — Take `main.py` apart (pure moves) — *done*, Phase 2 — DRY the duplicated patterns — *done*, Phase 4 — Split infrastructure god-objects — *done* (+17 more)

### Community 3 - "session.py"
Cohesion: 0.14
Nodes (21): init_data_max_age(), auth_link(), auth_telegram(), AuthOut, LinkAuthIn, me(), _me(), MeOut (+13 more)

### Community 4 - "Wizard"
Cohesion: 0.06
Nodes (10): ctx(), Wizard, test_draft_is_written_with_that_ttl(), TestAccumulation, TestCancel, TestCoexistsWithTheReciterFlow, TestCorruptState, TestLifecycle (+2 more)

### Community 5 - "_plan_setup.py"
Cohesion: 0.07
Nodes (36): memorize(), on_tap(), plan_step(), _expired(), _ref_from_draft(), _ref_to_draft(), _know_by_heart(), _cancel_row() (+28 more)

### Community 6 - "features/profile.py"
Cohesion: 0.08
Nodes (25): patch_profile(), _cancel_keyboard(), _join_board(), name_step(), offset_from_callback(), on_profile_tap(), _plan_line(), profile_command() (+17 more)

### Community 7 - "next_due_utc"
Cohesion: 0.15
Nodes (8): _as_utc(), local_date(), local_now(), local_time(), next_due_utc(), TestLocalDate, TestNextDueUtc, _utc()

### Community 8 - "to_whatsapp"
Cohesion: 0.16
Nodes (3): to_whatsapp(), TestTags, TestWhatTheBotSends

### Community 9 - "_ctx"
Cohesion: 0.12
Nodes (10): _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join(), _Message, _sent(), _Settings (+2 more)

### Community 10 - "_ctx"
Cohesion: 0.09
Nodes (16): _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _Message, _profile_row(), _sent() (+8 more)

### Community 11 - "services/plans.py"
Cohesion: 0.06
Nodes (42): parse_ref_or_422(), ref_out(), active(), _build(), complete(), create(), DrillOut, lifecycle() (+34 more)

### Community 12 - "Store"
Cohesion: 0.08
Nodes (11): _CallbackQuery, _ctx(), _Message, _run_wizard(), _Settings, _tap(), TestDrill, TestEnqueueChain (+3 more)

### Community 13 - "render_streak_graph"
Cohesion: 0.14
Nodes (7): render(), draw_contribution_graph(), render_streak_graph(), _semaphore(), open_png(), TestRendering, TestRenderStreakGraph

### Community 14 - "test_whatsapp_config.py"
Cohesion: 0.31
Nodes (5): env(), test_any_missing_value_keeps_it_off(), test_off_by_default(), test_on_when_fully_configured(), test_the_flag_must_be_truthy()

### Community 15 - "UserSettings"
Cohesion: 0.19
Nodes (5): SettingsRow, UserSettings, TestDefaults, TestIndependence, TestRoundTrip

### Community 16 - "Context"
Cohesion: 0.14
Nodes (17): get_store(), _added_update(), _bot(), _ctx(), _member(), _run_setup_to_plan(), _Settings, TestAdded (+9 more)

### Community 17 - "test_store_selection.py"
Cohesion: 0.06
Nodes (16): health(), cache_backend(), store_backend(), database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries() (+8 more)

### Community 18 - "Refs"
Cohesion: 0.07
Nodes (11): _clean(), format_ref(), parse_range(), parse_reference(), TestSurahSpans, TestAcrossSurahs, TestFormatting, TestJuzAndPage (+3 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.06
Nodes (20): 6. Issues fixed in this refactor, link(), _code_key(), issue(), redeem(), too_many_tries(), _tries_key(), forget() (+12 more)

### Community 20 - "lifespan.py"
Cohesion: 0.04
Nodes (26): 3. Principles applied, _commands_for(), initialize(), lifespan(), _set_bot_commands(), _process_update(), telegram_webhook(), webhook_secret() (+18 more)

### Community 21 - "WhatsAppChannel"
Cohesion: 0.18
Nodes (4): _clip(), _resolve(), _split_choices(), WhatsAppChannel

### Community 22 - "InMemoryIdentityStore"
Cohesion: 0.12
Nodes (3): InMemoryIdentityStore, PostgresIdentityStore, _stored()

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "group.py"
Cohesion: 0.10
Nodes (17): bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), _enqueue_next_board(), _enqueue_next_group(), group_board_entries() (+9 more)

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.14
Nodes (14): 10. Found along the way (out of scope — behaviour changes), 2. Goals and non-goals, 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, 6. Ordering, risk, size, 7. Safety net, 8. Expected result, 9. Decisions and open questions (+6 more)

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
Cohesion: 0.09
Nodes (15): _CallbackQuery, _cmd(), _ctx(), _isolate_registries(), _Message, _run_wizard(), _save_plan(), _Settings (+7 more)

### Community 30 - "infra/catalog.py"
Cohesion: 0.07
Nodes (15): _search_reciters(), reciter_page_of(), reciter_search_keyboard(), source(), nav_labels(), audio_url(), find(), has_page_audio() (+7 more)

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 33 - "test_recall_check.py"
Cohesion: 0.15
Nodes (4): test_options_need_no_html_escaping_beyond_the_callers(), test_pick_ayah_is_deterministic_per_user_and_date(), test_pick_ayah_on_an_inverted_or_empty_span(), test_unknown_ayahs_are_rejected()

### Community 34 - ".get"
Cohesion: 0.06
Nodes (11): 12. Testing, 2. Current-state audit (what is hardcoded English), build_data(), get_default_query_results(), make_index(), parse_quran(), TranslationRegistry, TestCorpusIntegrity (+3 more)

### Community 35 - "test_reciter_picker.py"
Cohesion: 0.09
Nodes (7): reciter_set_confirmation(), data(), fake_bot(), TestCatalogKinds, TestCatalogOrder, TestKindWarnings, tg_bot()

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.09
Nodes (23): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 1. Terminology (so the report language is right), 2. What "correct" can mean — error taxonomy, 3.1 Commercial, 3.2 Open models and data, 3.3 Reference *text* per riwāyah (+15 more)

### Community 38 - "hifz_progress.py"
Cohesion: 0.08
Nodes (5): format_percent(), PageProgress, _Ratio, round_percent(), TestRounding

### Community 39 - "fixture"
Cohesion: 0.05
Nodes (32): create_app(), deliver_push(), _log(), data(), tg_bot(), data(), no_cdn(), _isolate_registries() (+24 more)

### Community 40 - "reciter_keyboard"
Cohesion: 0.19
Nodes (5): reciter_keyboard(), reciter_page_count(), _pager_row(), _reciter_buttons(), TestPagination

### Community 41 - "auth.py"
Cohesion: 0.10
Nodes (22): _b64url(), _b64url_decode(), decode_token(), _init_data_secret(), InvalidToken, issue_token(), jwt_secret(), require_user() (+14 more)

### Community 42 - "PostgresPlanStore"
Cohesion: 0.06
Nodes (4): InMemoryPlanStore, PlanDayRow, PlanRow, PlanStore

### Community 43 - "quran_page_progress"
Cohesion: 0.11
Nodes (4): juz_page_progress(), quran_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 44 - "test_hifz_cross_platform.py"
Cohesion: 0.22
Nodes (3): Telegram, test_a_week_on_whatsapp_matches_a_week_on_telegram(), _week()

### Community 45 - "Streaks"
Cohesion: 0.18
Nodes (3): record_session(), TestThreeTheStreak, TestRecordSession

### Community 46 - "Load Test"
Cohesion: 0.14
Nodes (13): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+5 more)

### Community 47 - "Multilingual Plan"
Cohesion: 0.13
Nodes (17): Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), Quran.from_file(path) refactor, setMyCommands per language, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+9 more)

### Community 48 - "Text"
Cohesion: 0.22
Nodes (6): _inline_query(), _of_type(), _results(), TestInlineArabicImage, TestRangeAudio, TestRangeText

### Community 49 - "Schema"
Cohesion: 0.11
Nodes (27): daily_ayah_sub, group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval (+19 more)

### Community 50 - "Services"
Cohesion: 0.15
Nodes (19): _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today(), test_me_carries_plan_and_streak() (+11 more)

### Community 51 - "Ctx"
Cohesion: 0.06
Nodes (34): Phase 3 — One router for everything — *done*, Ctx, _on_text(), _begin_setup(), handle_start_payload(), _is_group_admin(), _join_board(), on_group_tap() (+26 more)

### Community 52 - "Dispatch"
Cohesion: 0.17
Nodes (19): handle_update(), _callback(), data(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index() (+11 more)

### Community 55 - "Inline Reciter Search Tests"
Cohesion: 0.14
Nodes (19): _audio_result(), data(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter(), test_ayah_audio_dropped_without_public_base_url(), test_ayah_audio_uses_callers_reciter() (+11 more)

### Community 56 - "test_daily_feature.py"
Cohesion: 0.18
Nodes (7): _buttons(), graph(), Graph, _message(), _tap(), TestTelegramSetup, _texts()

### Community 57 - "MemoryStore"
Cohesion: 0.12
Nodes (7): 11.1 Profile settings reset after a while — `fix/settings-persistence`, 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, DatabaseUnavailable, get_pool(), _lock(), MemoryStore

### Community 58 - "os"
Cohesion: 0.12
Nodes (17): build_meta(), export(), main(), _spans(), split_basmalah(), _write(), _absolute_imports(), _sources() (+9 more)

### Community 60 - "test_hifz_keyboard_snapshots.py"
Cohesion: 0.33
Nodes (6): _as_dict(), _ctx(), _Settings, _static_cases(), test_hifz_keyboards_match_their_snapshots(), _view_cases()

### Community 61 - "Dispatch Order Tests"
Cohesion: 0.18
Nodes (17): _callback(), data(), fake_bot(), _message(), probe(), _sent_a_verse(), test_a_command_beats_a_pending_reciter_search(), test_a_command_escapes_a_wizard_without_ending_it() (+9 more)

### Community 62 - "taps"
Cohesion: 0.17
Nodes (3): taps(), TestChoices, TestMedia

### Community 63 - "Mini App Plan"
Cohesion: 0.11
Nodes (18): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 4.1 Flow, 4.2 Rules (+10 more)

### Community 65 - "services/check.py"
Cohesion: 0.08
Nodes (15): _answer_data(), _ask(), check(), on_check(), _options_keyboard(), _parse_answer(), _question_text(), _score() (+7 more)

### Community 67 - "surah_progress"
Cohesion: 0.04
Nodes (15): Progress, ProgressSummary, quran_progress(), started_surahs(), summarize(), surah_progress(), SurahProgress, load_summary() (+7 more)

### Community 68 - "SendCtx"
Cohesion: 0.09
Nodes (11): _send_plain_message(), register_send_handler(), registered_kinds(), _same_origin(), send_handler(), decorate(), SendCtx, catch_up() (+3 more)

### Community 69 - "weekly_board"
Cohesion: 0.24
Nodes (3): weekly_board(), make_user(), TestWeeklyBoard

### Community 70 - "api/catalog.py"
Cohesion: 0.20
Nodes (10): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, put_position(), ReaderPosition, Reciter (+2 more)

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 73 - "api/progress.py"
Cohesion: 0.12
Nodes (18): not_found(), RefOut, surah_name(), forget(), ForgetIn, ForgetOut, _juz(), JuzRatio (+10 more)

### Community 74 - "reader.py"
Cohesion: 0.08
Nodes (22): juz(), page(), page_audio(), turn_page(), random_ayah(), read_text(), reader_position(), repeat() (+14 more)

### Community 75 - "parse_offset"
Cohesion: 0.09
Nodes (5): format_offset(), parse_offset(), TestFormatOffset, TestParseOffset, TestPicker

### Community 76 - "tick.py"
Cohesion: 0.18
Nodes (8): _deliver(), _is_stale(), _lock(), _release(), _resolve(), _tick(), TickResult, _utcnow()

### Community 78 - "bundle_translations.py"
Cohesion: 0.15
Nodes (8): _clean_state_store(), bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.13
Nodes (16): Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points), Error taxonomy L1-L5 (word, harakah, tajwid, riwayah mismatch, waqf), Evaluation plan (false-alarm gate < 2% per ayah), IqraEval 2025 shared task, Recitation checker phased roadmap (A-1 to E) (+8 more)

### Community 80 - "BismillahBot — Business Logic"
Cohesion: 0.11
Nodes (16): 1. Overview, 2. Architecture, 3. Request lifecycle, 5. Caching strategy, 7. Known limitations / tech debt, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic (+8 more)

### Community 81 - "Streaks: compute_streak"
Cohesion: 0.21
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 83 - "SessionStore"
Cohesion: 0.07
Nodes (5): InMemorySessionStore, LeaderboardEntry, PostgresSessionStore, SessionRow, SessionStore

### Community 84 - "Scheduler Tests"
Cohesion: 0.17
Nodes (4): _claimed_at(), _record(), TestCatchUp, TestTick

### Community 86 - "whatsapp_format.py"
Cohesion: 0.20
Nodes (3): _Converter, _render(), _wrap()

### Community 87 - "_clip"
Cohesion: 0.09
Nodes (14): _clip(), _covered(), _focus_surah(), _intersect(), _page_share(), _pages_of(), _recency_key(), _surah_of() (+6 more)

### Community 89 - "auth.py"
Cohesion: 0.12
Nodes (24): InvalidInitData, sign_init_data(), validate_init_data(), _auth(), _fields(), _jwt_secret(), test_added_field_is_rejected(), test_auth_drops_malformed_start_param() (+16 more)

### Community 90 - "Store Contract Tests"
Cohesion: 0.11
Nodes (3): _spans(), TestHifzIntervalEdges, TestHifzIntervals

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.08
Nodes (24): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+16 more)

### Community 92 - "telegram"
Cohesion: 0.08
Nodes (18): _stress_reset(), _stress_stats(), set_menu_button(), _app_command(), app_on(), data(), test_app_command(), test_app_command_without_url() (+10 more)

### Community 93 - "_hifz"
Cohesion: 0.07
Nodes (10): _assert_invariant(), _ayahs(), _hifz(), _spans(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order(), TestAddInterval (+2 more)

### Community 94 - "Dependency rule (app -> bot -> services -> domain)"
Cohesion: 0.18
Nodes (10): tests/test_layering.py ratchet (KNOWN violations), Overlap with MULTI_PLATFORM_PLAN channel seam, Shared UTC offset picker (time_pickers.offset_keyboard), Decisions and open questions (§9), Found along the way (out-of-scope behaviour changes), Phase 0 — Guardrails (ruff, layering test, logging), Phase 5 — Fix the layering, Target layout (app/ bot/ services/ domain/ infra/) (+2 more)

### Community 95 - "test_whatsapp_router.py"
Cohesion: 0.17
Nodes (8): bodies(), fixture_message(), known_user(), tap(), TestBoundaries, TestFirstContact, TestReader, text()

### Community 97 - "handle_message"
Cohesion: 0.33
Nodes (7): _allowed_command(), handle_message(), _tap(), _due_rows(), TestWhatsApp, wa_tap(), wa_text()

### Community 101 - "TestStateStore"
Cohesion: 0.08
Nodes (7): image_url(), page_image_url(), File, TestAudioFilename, TestImageFilename, TestLegacyLanguageKey, TestStateStore

### Community 103 - "week_bounds"
Cohesion: 0.18
Nodes (5): user_week_window(), week_window(), WeeklyBoard, user_offset(), TestWeekWindow

### Community 104 - "recall_check.py"
Cohesion: 0.07
Nodes (25): _assemble(), _at_offset(), _ayah_text(), _continuation_question(), _date_key(), display_length(), _distinct(), _everything() (+17 more)

### Community 105 - "_seed_legacy_lang"
Cohesion: 0.18
Nodes (4): _seed_legacy_lang(), TestInlineCaller, TestKeyedByUserId, TestLegacyMigration

### Community 106 - "test_store_contract.py"
Cohesion: 0.05
Nodes (5): TestDaily, TestLeaderboard, TestReaderPosition, TestSessions, TestSettings

### Community 107 - "Hifz platform frozen string manifest"
Cohesion: 0.14
Nodes (12): alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Hifz platform frozen string manifest, src/locales/en.py source of truth, Key conventions (btn_*, cmd_*), Wave process (feature agents, translation agents, reviewers) (+4 more)

### Community 109 - "quran.py"
Cohesion: 0.11
Nodes (9): forgot_command(), on_progress_tap(), progress_command(), progress_view(), _show(), _surah_line(), _division_marks(), surah_spans() (+1 more)

### Community 110 - "stats.py"
Cohesion: 0.35
Nodes (8): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut

### Community 111 - "test_page_mode.py"
Cohesion: 0.08
Nodes (16): send_page(), send_page_audio(), send_repeated_audio(), _buffer(), data(), fake_bot(), _stub_audio(), _stub_stitch() (+8 more)

### Community 113 - "store/__init__.py"
Cohesion: 0.07
Nodes (8): DailyStore, DailySubRow, InMemoryDailyStore, InMemoryHifzStore, InMemoryStore, ScheduleStore, MemoryState, _isolate_registries()

### Community 115 - "Koyeb Capacity Report"
Cohesion: 0.25
Nodes (7): Koyeb free-tier capacity report, CPU-bound queueing failure mode (~24 msg/s ceiling), Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start), Neon managed Postgres, Capacity results 5-1000 concurrent (no errors, 70-91 MB), Stress environment (docker-compose.stress.yml, cpus 0.1, 512m), Synthetic traffic mix (scripts/stress/gen_updates.py)

### Community 116 - "Blue Green Ci"
Cohesion: 0.14
Nodes (13): concurrency, cancel-in-progress, group, env, PYTHON_DEFAULT, name, on, pull_request (+5 more)

### Community 117 - "Blue Green Ci: name"
Cohesion: 0.23
Nodes (14): steps, steps, steps, steps, steps, steps, steps, env (+6 more)

### Community 120 - "corpus"
Cohesion: 0.33
Nodes (3): _basmala_prefix(), _clean(), corpus()

### Community 121 - "refresh_streaks"
Cohesion: 0.19
Nodes (6): StreakCounts, refresh_streaks(), SessionOutcome, streak_summary(), user_today(), TestRefreshAndSummary

### Community 122 - "build_question"
Cohesion: 0.12
Nodes (14): build_question(), _answer_data(), _ask(), _asked(), _buttons(), _callback_query(), _ctx(), _sessions() (+6 more)

### Community 123 - "_send_graph"
Cohesion: 0.21
Nodes (6): _caption(), _keyboard(), on_streak(), _send_graph(), streak(), StreakSummary

### Community 124 - "Quran"
Cohesion: 0.06
Nodes (11): _consolidations(), Quran, test_page_boundaries_match_the_bot(), TestEveryParsedRefIsReal, TestDivisionsTileTheQuran, TestExists, TestRandom, TestStructure (+3 more)

### Community 125 - "4. Navigation model"
Cohesion: 0.22
Nodes (10): 4. Navigation model, Audio catalog kinds, Page audio with stitched fallback, Page images and page audio, Repeat (memorization), Structural divisions (page / juz / sajda), Translation-only catalogue entries, Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES) (+2 more)

### Community 126 - "TestHelpers"
Cohesion: 0.06
Nodes (10): _covers(), HifzInterval, HifzStore, _merge_span(), _normalize(), _overlaps(), PostgresHifzStore, _split_span() (+2 more)

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
Cohesion: 0.12
Nodes (9): data(), fake_bot(), _message(), _no_network(), TestCommandArguments, TestJuzCommand, TestPageCommand, TestSajdaCommand (+1 more)

### Community 131 - "test_inline_range.py"
Cohesion: 0.08
Nodes (14): download_combined_audio(), download_stitched_audio(), data(), fake_bot(), public_url(), tg_bot(), _bot(), _next_id() (+6 more)

### Community 132 - "Mini App Plan: Separate quranayatminiapp Nextjs"
Cohesion: 0.14
Nodes (11): Inline query answering (all four representations, ranges), Navigation model ((surah, ayah, type) per chat_id), Page image stitching (lib/page_image.py), Structural divisions (page / juz / sajda from quran-data.xml), Verse card (inline keyboard, edit in place), Uthmani text in Amiri Quran / KFGQPC font, Locale export to JSON (web_ keys, next-intl), Static immutable Quran JSON served from frontend CDN (+3 more)

### Community 135 - "range_audio"
Cohesion: 0.11
Nodes (6): range_audio(), content(), TestRangeAudioRoute, fake_download(), TestStitching, __init__()

### Community 136 - "Phase 2 — DRY the duplicated patterns"
Cohesion: 0.14
Nodes (11): graphify knowledge graph (graphify-out/), CLAUDE.md graphify lookup rules, button_rows() row-packing helper, Copy-pasted patterns table (§1.3), GET / health with store and cache status (503), ignore_not_modified() context manager, Phase 2 — DRY the duplicated patterns, Phase 3 — One router for everything (+3 more)

### Community 137 - "InMemoryGroupStore"
Cohesion: 0.06
Nodes (6): GroupConfig, GroupMemberLink, GroupPlanDayRow, GroupPlanRow, GroupStore, InMemoryGroupStore

### Community 140 - "MINI_APP_PLAN.md"
Cohesion: 0.20
Nodes (8): Central callback prefix allocation (hifz.PREFIXES), Future roadmap and prioritized backlog, The hifz platform (memorization companion), Pure plan builder (build_plan), Streak day ticks on completed session, Bot ↔ Mini App integration (menu button, startapp, /app), recitation_job table and user_profile.riwayah, /recite flow (voice note → recitation_job → report)

### Community 141 - "ScheduledSend"
Cohesion: 0.11
Nodes (5): The scheduler (`src/lib/scheduler.py`), enqueue(), idempotency_key(), schedule_daily(), ScheduledSend

### Community 143 - "test_export_web_content.py"
Cohesion: 0.21
Nodes (7): _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah(), test_meta_surahs_and_sajdas(), test_tafsir_has_every_ayah()

### Community 144 - "dispatch.py"
Cohesion: 0.07
Nodes (19): handle_incoming(), _incoming(), _on_callback(), answer_inline_query(), inline_audio_result(), inline_photo_results(), combined_audio_key(), deliver_page_audio() (+11 more)

### Community 145 - "normalize_lang"
Cohesion: 0.18
Nodes (5): is_supported(), is_ui_language(), Language, normalize_lang(), TestNormalizeLang

### Community 147 - "juz_progress"
Cohesion: 0.16
Nodes (5): juz_progress(), JuzProgress, _spans(), started_juzs(), TestJuzProgress

### Community 148 - "to_markup"
Cohesion: 0.19
Nodes (5): verse_keyboard(), to_markup(), TestToMarkup, _button(), TestVerseKeyboard

### Community 153 - "offset_keyboard"
Cohesion: 0.35
Nodes (7): offset_keyboard(), _grid(), test_a_label_prefix_changes_only_the_label(), test_cancel_data_adds_a_localized_cancel_row(), test_every_offset_is_offered_in_order_under_the_callers_prefix(), test_no_cancel_row_unless_asked(), test_rows_are_columns_wide()

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 155 - "test_channels_whatsapp.py"
Cohesion: 0.08
Nodes (8): cache(), channel(), graph(), Graph, TestNumberedMenuLifetime, TestText, TestTransport, TestVoiceNotes

### Community 158 - "Profile settings reset fix (fix/settings-persistence)"
Cohesion: 0.29
Nodes (8): ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable, lib/utils.File god class, Silent in-memory store fallback, Phase 4 — Split infrastructure god-objects, Profile settings reset fix (fix/settings-persistence), Typed frozen Settings (config/settings.py), conftest.py test environment (src on path, CWD pin, no Redis/network), Environment configuration (webhook, CDN base URLs, Redis)

### Community 159 - "MINI_APP_PLAN.md"
Cohesion: 0.13
Nodes (17): /api/v1 REST surface, initData HMAC validation → short-lived JWT, OpenAPI → TypeScript client pipeline, Recall check integrity (signed question_token), Mini App risks, Identity table (platform, external_id → user_id), Normalized Incoming event, Neutral message model rendering (HTML / WhatsApp markup) (+9 more)

### Community 161 - "fetch_and_stitch"
Cohesion: 0.29
Nodes (4): fetch_and_stitch(), _fit_for_telegram(), _semaphore(), stitch_images()

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
Cohesion: 0.17
Nodes (5): _callback(), _message(), _tab_row(), TestAudioNeverFollowsLanguage, TestPickerFlow

### Community 170 - "button_action"
Cohesion: 0.04
Nodes (31): command, Routing rules (in `serve`), 7. The keyboard & command localization challenge, Telegram command menu, main(), placeholders(), about(), app() (+23 more)

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 172 - "TranslationRegistry"
Cohesion: 0.13
Nodes (15): 10. File-by-file change list, 11. Memory & performance (free-tier reality), 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 3. Target architecture, 4. User language preference, 6. UI internationalization (i18n) (+7 more)

### Community 175 - "test_keyboard_snapshots.py"
Cohesion: 0.25
Nodes (5): _as_dict(), _keyboards(), _render(), _search_markup(), test_keyboards_match_their_snapshots()

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

### Community 185 - "test_channels_telegram.py"
Cohesion: 0.25
Nodes (3): bot(), cache(), TestChoice

### Community 194 - "re"
Cohesion: 0.57
Nodes (4): _modules(), test_nothing_builds_telegram_markup_by_hand_outside_those_modules(), test_only_group_code_reads_the_telegram_client(), test_only_telegram_only_modules_import_telegram()

### Community 196 - "8. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 8. Phased task breakdown, Phase 0 — Foundations, Phase 1 — Service-layer extraction (this repo, no UI change), Phase 2 — Reader parity (read-only, low risk, ships first), Phase 3 — Hifz parity, Phase 4 — Recitation checker UI (depends on the investigation's Phase A), Phase 5 — Later

### Community 197 - ".wa_user"
Cohesion: 0.17
Nodes (6): apps(), Apps, _code(), data(), TestCodes, TestLinking

### Community 199 - "json"
Cohesion: 0.18
Nodes (10): export(), languages(), main(), resolved_table(), _write(), build(), main_(), _load() (+2 more)

### Community 200 - "features/leaderboard.py"
Cohesion: 0.38
Nodes (3): _board_message(), leaderboard(), on_leaderboard()

### Community 205 - "test_hifz_streak.py"
Cohesion: 0.22
Nodes (6): _ctx(), _isolate_registries(), _photo_message(), _Settings, TestCallback, TestWhatTicksADay

### Community 206 - "test_hifz_seam.py"
Cohesion: 0.18
Nodes (3): _isolate_registries(), _Settings, TestSchemaApplication

### Community 207 - "for_platform"
Cohesion: 0.22
Nodes (3): for_platform(), TestForPlatform, TestTheRest

### Community 208 - "get_language"
Cohesion: 0.22
Nodes (3): get_language(), TestLanguageLookup, TestLanguageFlags

### Community 209 - "as_command"
Cohesion: 0.29
Nodes (3): as_command(), lang_hint(), TestKeywords

### Community 214 - "PostgresDailyStore"
Cohesion: 0.14
Nodes (4): PostgresDailyStore, PostgresStore, Store, store()

### Community 270 - "typing"
Cohesion: 0.05
Nodes (32): _ask_time(), daily(), _enable(), _hhmm(), _offset(), on_tap(), _parse_time(), push_daily() (+24 more)

### Community 275 - "milestone_for"
Cohesion: 0.19
Nodes (5): Milestone, milestone_for(), _milestone_key(), offset_of(), TestMilestones

### Community 278 - "11. Infrastructure, capacity and cost on paid Koyeb"
Cohesion: 0.33
Nodes (6): 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards, 11. Infrastructure, capacity and cost on paid Koyeb

### Community 293 - "test_scheduler.py"
Cohesion: 0.32
Nodes (3): _isolate_handlers(), state(), store()

## Knowledge Gaps
- **51 isolated node(s):** `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres`, `Capacity results 5-1000 concurrent (no errors, 70-91 MB)`, `Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES)` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1744 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **172 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `Context` to `session.py`, `features/profile.py`, `_ctx`, `_ctx`, `services/plans.py`, `Store`, `render_streak_graph`, `TestDailyPost`, `UserSettings`, `dispatch.py`, `RedisSingleton`, `lifespan.py`, `Hifz Progress Cmd Tests`, `Hifz Streak Tests`, `Acceptance Tests`, `TestFiveAndSixTheBoard`, `.test_sends_todays_ayah_and_queues_tomorrow`, `auth.py`, `test_hifz_cross_platform.py`, `Streaks`, `Services`, `Dispatch`, `test_daily_feature.py`, `MemoryStore`, `test_hifz_keyboard_snapshots.py`, `_lock`, `WhatsApp`, `.apply_schema`, `SendCtx`, `weekly_board`, `.wa_user`, `surah_progress`, `api/progress.py`, `reader.py`, `tick.py`, `PostgresDailyStore`, `_hifz`, `test_whatsapp_router.py`, `handle_message`, `week_bounds`, `stats.py`, `store/__init__.py`, `refresh_streaks`, `build_question`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Are the 57 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 57 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_plan` be split into smaller, more focused modules?**
  _Cohesion score 0.04606891300209404 - nodes in this community are weakly interconnected._
- **Why does `Quran` connect `Quran` to `build_plan`, `test_navigation.py`, `_plan_setup.py`, `features/profile.py`, `range_audio`, `services/plans.py`, `typing`, `test_export_web_content.py`, `dispatch.py`, `Refs`, `juz_progress`, `lifespan.py`, `Hifz Progress Cmd Tests`, `.get`, `quran_page_progress`, `os`, `.get_surah_length`, `services/check.py`, `surah_progress`, `api/catalog.py`, `api/progress.py`, `reader.py`, `BismillahBot — Business Logic`, `sweep_refs`, `test_short_surahs_still_get_four_distinct_options`, `_clip`, `recall_check.py`, `quran.py`, `.get_next_ayah`, `corpus`, `build_question`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `Ctx` (e.g. with `3. Architecture` and `4.1 Overlap with `MULTI_PLATFORM_PLAN.md``) actually correct?**
  _`Ctx` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Should `link_token.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11895161290322581 - nodes in this community are weakly interconnected._