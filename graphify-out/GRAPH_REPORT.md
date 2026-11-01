# Graph Report - QuranAyat_bot  (2026-11-02)

## Corpus Check
- 266 files · ~252,493 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 4952 nodes · 11551 edges · 307 communities (168 shown, 139 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1076 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2f27033f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- advancing
- Quran
- surah_progress
- build_plan
- .start
- _plan_setup.py
- features/profile.py
- next_due_utc
- to_whatsapp
- _ctx
- _ctx
- group.py
- Store
- render_streak_graph
- test_miniapp_links.py
- UserSettings
- Context
- test_store_selection.py
- Refs
- RedisSingleton
- lifespan.py
- WhatsAppChannel
- InMemoryIdentityStore
- Hifz Progress Cmd Tests
- on_my_chat_member
- Refactor — Implementation Plan
- TelegramChannel
- Hifz Streak Tests
- Hifz Platform
- Acceptance Tests
- dispatch.py
- Docker Compose.stress
- test_page_mode.py
- test_recall_check.py
- .get
- _options_keyboard
- expect
- Recitation Checker Investigation
- hifz_progress.py
- test_whatsapp_webhook.py
- to_markup
- Session
- PostgresPlanStore
- quran_page_progress
- page_keyboard
- Streaks
- Load Test
- Multilingual Plan
- Text
- Schema
- Services
- auth.py
- Dispatch
- reciter_keyboard
- PostgresProfileStore
- Inline Reciter Search Tests
- test_hifz_check.py
- deliver_push
- os
- InMemoryDailyStore
- SendCtx
- Dispatch Order Tests
- .send_text
- Mini App Plan
- Wizard
- juz_progress
- summarize
- features/daily.py
- reader.py
- api/catalog.py
- reset_for_tests
- Hifz Seam Tests
- api/plans.py
- router.py
- command
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
- Ref
- auth.py
- Store Contract Tests
- Multi Platform Plan: MultiPlatform Implementation Plan
- test_verse_card.py
- _hifz
- ProfileRow
- handle_message
- Hifz Seam Tests: TestRegistration
- no_cdn
- Scheduler Tests: TestTransientFailuresAreRetried
- Store Contract Tests: TestPlans
- GraphClient
- TestStateStore
- welcome_text
- week_bounds
- recall_check.py
- weekly_board
- test_store_contract.py
- handle_message
- test_hifz_streak.py
- pages.py
- stats.py
- send_page
- TestSchedule
- store/__init__.py
- features/progress.py
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- .get_next_ayah
- parse_ayah
- ._load_performers
- Profile settings reset fix (fix/settings-persistence)
- whatsapp_format.py
- streak.py
- .exists
- UserSettingsRow
- TestHelpers
- Blue Green Ci: jobs
- Blue Green Ci: with
- build_grid
- test_navigation.py
- _clip
- Mini App Plan: Separate quranayatminiapp Nextjs
- InMemoryScheduleStore
- Channel
- range_audio
- test_export_web_content.py
- GroupStore
- Store Contract Tests: TestLeaderboard
- test_hifz_intervals.py
- MINI_APP_PLAN.md
- export
- TestRestartDeliversExactlyOnce
- t
- locales/__init__.py
- normalize_lang
- juz_ref
- Hifz platform frozen string manifest
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
- Phase 2 — DRY the duplicated patterns
- MINI_APP_PLAN.md
- Settings Tests
- Store Contract Tests: TestSessions
- Blue Green Ci: postgres
- Blue Green Ci: test
- Blue Green Ci: preflight
- TestTransliteration
- ProfileStore
- Hifz Seam Tests: TestPrefixNamespace
- Hifz Seam Tests: TestDispatchCallback
- TestPickerFlow
- button_action
- Blue Green Ci: smokegreen
- BismillahBot — Multilingual Support Plan
- File Facade: search_performers
- test_keyboard_snapshots.py
- reciter_label
- TestRunScheduler
- BismillahBot README
- load_summary
- InMemorySessionStore
- PostgresSessionStore
- Blue Green Ci: deploygreen
- Blue Green Ci: promote
- Choices
- TestHifzIntervalEdges
- Hifz Seam Tests: test_longest_prefix_wins
- HifzStore
- ayah_count
- Dependency rule (app -> bot -> services -> domain)
- _save_plan
- TestIdentity
- Claude
- json
- send_repeated_audio
- Hifz Seam Tests: TestDispatchCommand
- _Ratio
- offset_options
- test_export_locales_json.py
- Hifz Group Tests: TestRegistration
- answer_inline_query
- split
- fetch_and_stitch
- test_wizard.py
- send_page_audio
- button_action
- quran_progress
- next_scheduled_date
- parse_ayah_range
- test_whatsapp_config.py
- WhatsAppChannel
- PostgresDailyStore
- .test_full_flow_queues_the_first_send
- MemoryStore
- _bot
- GroupPlanDayRow
- .is_cancel
- get_store
- ayah_for
- test_webhook.py
- TestRegistration
- PageProgress
- performers
- GroupConfig
- auto_pace
- TestSettings
- _plan_keyboards.py
- GroupMemberLink
- as_command
- get
- get_language
- reciter_set_confirmation
- Graph
- check_locales.py
- level_for
- Graph
- .test_sends_todays_ayah_and_queues_tomorrow
- parametrize
- register_send_handler
- test_bot_errors.py
- _create_topic

## God Nodes (most connected - your core abstractions)
1. `get_store()` - 164 edges
2. `Ctx` - 137 edges
3. `Quran` - 123 edges
4. `t()` - 120 edges
5. `handle_update()` - 95 edges
6. `UserSettings` - 78 edges
7. `build_plan()` - 72 edges
8. `parse_reference()` - 59 edges
9. `File` - 57 edges
10. `TelegramChannel` - 56 edges

## Surprising Connections (you probably didn't know these)
- `The scheduler (`src/lib/scheduler.py`)` --references--> `idempotency_key()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/infra/scheduler/enqueue.py
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `3. Target architecture` --references--> `TranslationRegistry`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/domain/quran.py
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

## Communities (307 total, 139 thin omitted)

### Community 0 - "advancing"
Cohesion: 0.09
Nodes (7): advancing(), assert_covers_target_once(), assert_well_formed(), spans(), TestAlMulkAcceptance, TestCrossSurahTargets, TestSmallAndAwkwardTargets

### Community 1 - "Quran"
Cohesion: 0.06
Nodes (13): _consolidations(), Quran, _at_offset(), _everything(), _same_surah(), _span_length(), plan_target(), test_page_boundaries_match_the_bot() (+5 more)

### Community 2 - "surah_progress"
Cohesion: 0.09
Nodes (6): started_surahs(), surah_progress(), _at(), TestInputHandling, TestSpecAcceptance, TestSurahProgress

### Community 3 - "build_plan"
Cohesion: 0.12
Nodes (5): build_plan(), surah_ref(), TestConsolidationDays, TestDayOfWeekFiltering, TestPurity

### Community 5 - "_plan_setup.py"
Cohesion: 0.08
Nodes (40): Ctx, _ask(), check(), on_check(), _question_text(), _score(), _begin_setup(), _is_group_admin() (+32 more)

### Community 6 - "features/profile.py"
Cohesion: 0.09
Nodes (19): _cancel_keyboard(), _join_board(), name_step(), offset_from_callback(), on_profile_tap(), _plan_line(), profile_command(), profile_view() (+11 more)

### Community 7 - "next_due_utc"
Cohesion: 0.07
Nodes (11): format_offset(), local_now(), local_time(), next_due_utc(), parse_offset(), TestFormatOffset, TestLocalDate, TestNextDueUtc (+3 more)

### Community 8 - "to_whatsapp"
Cohesion: 0.15
Nodes (4): to_whatsapp(), test_any_missing_value_keeps_it_off(), TestTags, TestWhatTheBotSends

### Community 9 - "_ctx"
Cohesion: 0.12
Nodes (10): _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join(), _Message, _sent(), _Settings (+2 more)

### Community 10 - "_ctx"
Cohesion: 0.06
Nodes (19): PlanDaySpec, _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _isolate_registries(), _Message (+11 more)

### Community 11 - "group.py"
Cohesion: 0.07
Nodes (25): _enqueue_next_board(), _enqueue_next_group(), group_board_entries(), post_board(), push_board(), push_group_day(), _as_utc(), local_date() (+17 more)

### Community 12 - "Store"
Cohesion: 0.09
Nodes (11): _CallbackQuery, _ctx(), _isolate_registries(), _Message, _run_wizard(), _Settings, _tap(), TestDrill (+3 more)

### Community 13 - "render_streak_graph"
Cohesion: 0.14
Nodes (7): render(), draw_contribution_graph(), render_streak_graph(), _semaphore(), open_png(), TestRendering, TestRenderStreakGraph

### Community 14 - "test_miniapp_links.py"
Cohesion: 0.16
Nodes (13): app_url(), set_menu_button(), _app_command(), app_on(), data(), test_app_command(), test_app_command_without_url(), test_cards_and_drill_link_to_their_screens() (+5 more)

### Community 15 - "UserSettings"
Cohesion: 0.11
Nodes (11): patch_settings(), _legacy_lang_key(), SettingsRow, UserSettings, _seed_legacy_lang(), TestDefaults, TestIndependence, TestInlineCaller (+3 more)

### Community 16 - "Context"
Cohesion: 0.17
Nodes (14): _bot(), _ctx(), _isolate_registries(), _member(), _run_setup_to_plan(), _Settings, tap(), TestBoardJoin (+6 more)

### Community 17 - "test_store_selection.py"
Cohesion: 0.06
Nodes (15): health(), CacheUnavailable, database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries(), fresh_redis() (+7 more)

### Community 18 - "Refs"
Cohesion: 0.08
Nodes (9): _clean(), parse_range(), parse_reference(), TestSurahSpans, TestAcrossSurahs, TestFormatting, TestRejection, TestWholeSurah (+1 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.14
Nodes (6): 6. Issues fixed in this refactor, _key(), pick(), remember(), get(), RedisSingleton

### Community 20 - "lifespan.py"
Cohesion: 0.04
Nodes (28): Phase 4 — Split infrastructure god-objects — *done*, _stress_reset(), _stress_stats(), create_app(), _commands_for(), initialize(), lifespan(), _set_bot_commands() (+20 more)

### Community 21 - "WhatsAppChannel"
Cohesion: 0.14
Nodes (5): _bytes_and_name(), _clip(), _resolve(), _split_choices(), TestMedia

### Community 22 - "InMemoryIdentityStore"
Cohesion: 0.06
Nodes (5): IdentityRow, IdentityStore, InMemoryIdentityStore, PostgresIdentityStore, _stored()

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "on_my_chat_member"
Cohesion: 0.40
Nodes (3): bot_username(), _deep_link(), on_my_chat_member()

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.15
Nodes (13): 10. Found along the way (out of scope — behaviour changes), 2. Goals and non-goals, 3. Principles applied, 6. Ordering, risk, size, 7. Safety net, 8. Expected result, 9. Decisions and open questions, Expected result metrics (§8) (+5 more)

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
Cohesion: 0.13
Nodes (11): _CallbackQuery, _cmd(), _ctx(), _Message, _run_wizard(), _Settings, _tap(), TestFourProgress (+3 more)

### Community 30 - "dispatch.py"
Cohesion: 0.04
Nodes (16): inline_audio_result(), combined_audio_key(), range_audio_url(), ref_key(), Caps, WindowClosed, _flag(), get_settings() (+8 more)

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 32 - "test_page_mode.py"
Cohesion: 0.14
Nodes (6): data(), fake_bot(), _png(), TestStitchedAudioAcrossSurahs, TestStitching, tg_bot()

### Community 33 - "test_recall_check.py"
Cohesion: 0.03
Nodes (30): _nfc(), swept(), test_a_different_date_gives_a_different_question(), test_both_question_modes_show_up_in_the_sweep(), test_correct_option_is_never_a_length_outlier(), test_correct_option_is_never_the_extreme_by_a_wide_ratio(), test_correct_option_really_follows_the_prompt(), test_dates_and_iso_strings_are_interchangeable() (+22 more)

### Community 34 - ".get"
Cohesion: 0.08
Nodes (7): 12. Testing, parse_quran(), TranslationRegistry, TestCorpusIntegrity, TestAvailable, TestCaching, TestFallback

### Community 36 - "expect"
Cohesion: 0.21
Nodes (4): expect(), _key(), take(), TestCoexistsWithTheReciterFlow

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.07
Nodes (29): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards (+21 more)

### Community 38 - "hifz_progress.py"
Cohesion: 0.13
Nodes (6): _focus_surah(), format_percent(), _recency_key(), round_percent(), _surah_of(), TestRounding

### Community 39 - "test_whatsapp_webhook.py"
Cohesion: 0.10
Nodes (14): 2. Current-state audit (what is hardcoded English), build_data(), data(), tg_bot(), client(), data(), client(), fixture() (+6 more)

### Community 40 - "to_markup"
Cohesion: 0.17
Nodes (5): to_button(), to_markup(), TestToMarkup, _button(), TestVerseKeyboard

### Community 41 - "Session"
Cohesion: 0.10
Nodes (23): init_data_max_age(), auth_telegram(), AuthOut, me(), _me(), MeOut, patch_profile(), PlanSummary (+15 more)

### Community 42 - "PostgresPlanStore"
Cohesion: 0.05
Nodes (5): InMemoryPlanStore, PlanDayRow, PlanRow, PlanStore, PostgresPlanStore

### Community 43 - "quran_page_progress"
Cohesion: 0.10
Nodes (7): _covered(), juz_page_progress(), _page_share(), quran_page_progress(), page_ref(), TestPageProgress, _whole_quran_spans()

### Community 45 - "Streaks"
Cohesion: 0.13
Nodes (4): record_session(), TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 46 - "Load Test"
Cohesion: 0.14
Nodes (12): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+4 more)

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
Nodes (20): client(), _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today() (+12 more)

### Community 51 - "auth.py"
Cohesion: 0.07
Nodes (34): _b64url(), _b64url_decode(), jwt_secret(), require_user(), _sign(), _unauthorized(), answer(), AnswerIn (+26 more)

### Community 52 - "Dispatch"
Cohesion: 0.16
Nodes (18): _callback(), data(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index(), test_inline_query_valid_ayah_returns_all_four_views() (+10 more)

### Community 53 - "reciter_keyboard"
Cohesion: 0.21
Nodes (5): reciter_keyboard(), reciter_page_count(), _pager_row(), _reciter_buttons(), TestPagination

### Community 55 - "Inline Reciter Search Tests"
Cohesion: 0.12
Nodes (22): handle_update(), _audio_result(), data(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter(), test_ayah_audio_dropped_without_public_base_url() (+14 more)

### Community 56 - "test_hifz_check.py"
Cohesion: 0.05
Nodes (25): _parse_answer(), milestone_for(), _milestone_key(), percentile_band(), refresh_streaks(), streak_summary(), user_today(), _answer_data() (+17 more)

### Community 57 - "deliver_push"
Cohesion: 0.16
Nodes (11): deliver_push(), _log(), ctx_for(), graph(), Graph, say_hi(), test_every_push_is_logged_for_cost_tracking(), TestConsent (+3 more)

### Community 58 - "os"
Cohesion: 0.19
Nodes (11): _absolute_imports(), _sources(), test_known_violations_still_exist(), test_no_new_violations(), test_the_scan_sees_every_package(), _violations(), _imported_modules(), _py_files() (+3 more)

### Community 59 - "InMemoryDailyStore"
Cohesion: 0.15
Nodes (3): DailyStore, DailySubRow, InMemoryDailyStore

### Community 60 - "SendCtx"
Cohesion: 0.14
Nodes (5): ctx(), _send_plain_message(), decorate(), SendCtx, _deliver()

### Community 61 - "Dispatch Order Tests"
Cohesion: 0.18
Nodes (17): _callback(), data(), fake_bot(), _message(), probe(), _sent_a_verse(), test_a_command_beats_a_pending_reciter_search(), test_a_command_escapes_a_wizard_without_ending_it() (+9 more)

### Community 62 - ".send_text"
Cohesion: 0.21
Nodes (4): taps(), TestChoices, TestText, TestTransport

### Community 63 - "Mini App Plan"
Cohesion: 0.08
Nodes (25): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 4.1 Flow, 4.2 Rules (+17 more)

### Community 65 - "Wizard"
Cohesion: 0.19
Nodes (3): Wizard, TestCorruptState, TestLifecycle

### Community 66 - "juz_progress"
Cohesion: 0.16
Nodes (5): juz_progress(), JuzProgress, _spans(), started_juzs(), TestJuzProgress

### Community 67 - "summarize"
Cohesion: 0.11
Nodes (3): Progress, summarize(), TestSummarize

### Community 68 - "features/daily.py"
Cohesion: 0.13
Nodes (16): _ask_time(), daily(), _enable(), _hhmm(), _offset(), on_tap(), _parse_time(), push_daily() (+8 more)

### Community 69 - "reader.py"
Cohesion: 0.11
Nodes (14): random_ayah(), read_text(), reader_position(), repeat(), _send_verse(), verse_card(), verse_keyboard(), deliver_combined_audio() (+6 more)

### Community 70 - "api/catalog.py"
Cohesion: 0.15
Nodes (10): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, put_position(), ReaderPosition, Reciter (+2 more)

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 73 - "api/plans.py"
Cohesion: 0.09
Nodes (26): active(), _build(), complete(), create(), DrillOut, lifecycle(), _plan_out(), PlanCreateIn (+18 more)

### Community 74 - "router.py"
Cohesion: 0.09
Nodes (19): Phase 3 — One router for everything — *done*, _on_callback(), _on_text(), decorate(), _cancel(), command(), decorate(), dispatch_callback() (+11 more)

### Community 75 - "command"
Cohesion: 0.11
Nodes (16): command, Routing rules (in `serve`), 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, _chat_id(), handle_start_payload(), _board_message(), leaderboard() (+8 more)

### Community 76 - "tick.py"
Cohesion: 0.09
Nodes (16): enqueue(), idempotency_key(), schedule_daily(), registered_kinds(), catch_up(), run_scheduler(), _wait(), _is_stale() (+8 more)

### Community 78 - "Bundle Translations"
Cohesion: 0.22
Nodes (7): bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.12
Nodes (18): Audio catalog kinds, Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES), Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points), Error taxonomy L1-L5 (word, harakah, tajwid, riwayah mismatch, waqf), Evaluation plan (false-alarm gate < 2% per ayah) (+10 more)

### Community 80 - "BismillahBot — Business Logic"
Cohesion: 0.11
Nodes (16): 1. Overview, 2. Architecture, 3. Request lifecycle, 7. Known limitations / tech debt, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic, Local time (+8 more)

### Community 81 - "Streaks: compute_streak"
Cohesion: 0.24
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 83 - "SessionStore"
Cohesion: 0.13
Nodes (4): LeaderboardEntry, SessionRow, SessionStore, WeeklyBoard

### Community 84 - "Scheduler Tests"
Cohesion: 0.14
Nodes (6): _at(), _claimed_at(), _record(), TestCatchUp, TestIdempotentEnqueue, TestTick

### Community 85 - "sys"
Cohesion: 0.14
Nodes (3): _clean_state_store(), setup_logging(), test_http_client_request_urls_are_never_logged()

### Community 87 - "Ref"
Cohesion: 0.06
Nodes (18): 1. Why, Phase 1 — Take `main.py` apart (pure moves) — *done*, _post_portion(), push_plan_day(), _send_drill(), _translation_text(), _portion_label(), _preview_text() (+10 more)

### Community 89 - "auth.py"
Cohesion: 0.11
Nodes (29): decode_token(), _init_data_secret(), InvalidInitData, InvalidToken, issue_token(), sign_init_data(), validate_init_data(), _auth() (+21 more)

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.08
Nodes (24): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+16 more)

### Community 92 - "test_verse_card.py"
Cohesion: 0.18
Nodes (5): data(), fake_bot(), TestLanguageFlags, TestVerseText, tg_bot()

### Community 93 - "_hifz"
Cohesion: 0.11
Nodes (4): _hifz(), _spans(), TestAddInterval, TestRemoveRange

### Community 95 - "handle_message"
Cohesion: 0.16
Nodes (8): bodies(), fixture_message(), known_user(), tap(), TestBoundaries, TestFirstContact, TestReader, text()

### Community 100 - "GraphClient"
Cohesion: 0.11
Nodes (3): _error(), GraphClient, WhatsAppError

### Community 101 - "TestStateStore"
Cohesion: 0.08
Nodes (7): page_audio_url(), page_image_url(), File, TestAudioFilename, TestImageFilename, TestLegacyLanguageKey, TestStateStore

### Community 102 - "welcome_text"
Cohesion: 0.18
Nodes (4): command_lines(), welcome_text(), TestSevenTheCommandsExist, TestWelcomeText

### Community 103 - "week_bounds"
Cohesion: 0.14
Nodes (5): week_bounds(), user_week_window(), week_window(), TestWeekWindow, TestWeekBounds

### Community 104 - "recall_check.py"
Cohesion: 0.05
Nodes (32): _assemble(), _ayah_text(), _basmala_prefix(), build_question(), _clean(), _continuation_question(), corpus(), _date_key() (+24 more)

### Community 105 - "weekly_board"
Cohesion: 0.28
Nodes (3): weekly_board(), make_user(), TestWeeklyBoard

### Community 107 - "handle_message"
Cohesion: 0.23
Nodes (9): _allowed_command(), handle_message(), _now(), opt_out(), _tap(), _due_rows(), TestWhatsApp, wa_tap() (+1 more)

### Community 108 - "test_hifz_streak.py"
Cohesion: 0.20
Nodes (6): _ctx(), _isolate_registries(), _photo_message(), _Settings, TestCallback, TestWhatTicksADay

### Community 109 - "pages.py"
Cohesion: 0.08
Nodes (19): _search_reciters(), juz(), page(), page_audio(), sajda(), turn_page(), reciter_search_keyboard(), button_rows() (+11 more)

### Community 110 - "stats.py"
Cohesion: 0.27
Nodes (8): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut

### Community 111 - "send_page"
Cohesion: 0.29
Nodes (7): send_page(), _buffer(), _stub_stitch(), stub(), TestPageCard, capture(), counting()

### Community 113 - "store/__init__.py"
Cohesion: 0.09
Nodes (9): Incoming, Milestone, offset_of(), StreakCounts, MemoryState, SessionOutcome, user_offset(), _isolate_registries() (+1 more)

### Community 114 - "features/progress.py"
Cohesion: 0.10
Nodes (11): surah_name(), forgot_command(), on_progress_tap(), progress_command(), progress_view(), _show(), _surah_line(), build_verse_text() (+3 more)

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

### Community 120 - "._load_performers"
Cohesion: 0.13
Nodes (5): data(), fake_bot(), TestCatalogKinds, TestCatalogOrder, tg_bot()

### Community 121 - "Profile settings reset fix (fix/settings-persistence)"
Cohesion: 0.29
Nodes (8): ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable, lib/utils.File god class, Silent in-memory store fallback, Phase 4 — Split infrastructure god-objects, Profile settings reset fix (fix/settings-persistence), Typed frozen Settings (config/settings.py), conftest.py test environment (src on path, CWD pin, no Redis/network), Environment configuration (webhook, CDN base URLs, Redis)

### Community 122 - "whatsapp_format.py"
Cohesion: 0.20
Nodes (3): _Converter, _render(), _wrap()

### Community 123 - "streak.py"
Cohesion: 0.14
Nodes (10): _caption(), _keyboard(), on_streak(), _send_graph(), streak(), cache_key(), _send(), send_cached() (+2 more)

### Community 124 - ".exists"
Cohesion: 0.12
Nodes (6): TestEveryParsedRefIsReal, TestExists, TestRandom, TestStructure, test_pick_ayah_handles_a_cross_surah_span(), test_the_whole_quran_is_a_valid_span()

### Community 126 - "TestHelpers"
Cohesion: 0.10
Nodes (7): _covers(), InMemoryHifzStore, _merge_span(), _overlaps(), _split_span(), _touches(), TestHelpers

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

### Community 131 - "_clip"
Cohesion: 0.15
Nodes (6): _clip(), _intersect(), _pages_of(), clamp_to_quran(), contains(), TestContainsAndClamp

### Community 132 - "Mini App Plan: Separate quranayatminiapp Nextjs"
Cohesion: 0.12
Nodes (15): Inline query answering (all four representations, ranges), Navigation model ((surah, ayah, type) per chat_id), Page audio with stitched fallback, Page image stitching (lib/page_image.py), Repeat (memorization), Structural divisions (page / juz / sajda from quran-data.xml), Verse card (inline keyboard, edit in place), Uthmani text in Amiri Quran / KFGQPC font (+7 more)

### Community 133 - "InMemoryScheduleStore"
Cohesion: 0.06
Nodes (3): InMemoryScheduleStore, PostgresScheduleStore, ScheduleStore

### Community 135 - "range_audio"
Cohesion: 0.09
Nodes (8): range_audio(), download_combined_audio(), download_stitched_audio(), content(), TestRangeAudioRoute, fake_download(), TestStitching, __init__()

### Community 136 - "test_export_web_content.py"
Cohesion: 0.39
Nodes (7): _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah(), test_meta_surahs_and_sajdas(), test_tafsir_has_every_ayah()

### Community 139 - "test_hifz_intervals.py"
Cohesion: 0.19
Nodes (6): _assert_invariant(), _ayahs(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order(), TestEveryRelativePosition

### Community 140 - "MINI_APP_PLAN.md"
Cohesion: 0.13
Nodes (13): Central callback prefix allocation (hifz.PREFIXES), Future roadmap and prioritized backlog, The hifz platform (memorization companion), Streak day ticks on completed session, Bot ↔ Mini App integration (menu button, startapp, /app), Identity table (platform, external_id → user_id), Normalized Incoming event, Neutral message model rendering (HTML / WhatsApp markup) (+5 more)

### Community 141 - "export"
Cohesion: 0.18
Nodes (7): build_meta(), export(), main(), _spans(), split_basmalah(), _write(), parse_quran_tafsir()

### Community 142 - "TestRestartDeliversExactlyOnce"
Cohesion: 0.11
Nodes (5): InMemoryStore, store(), _isolate_handlers(), store(), TestRestartDeliversExactlyOnce

### Community 143 - "t"
Cohesion: 0.09
Nodes (23): 5. API surface (`/api/v1`), Phase 2 — WhatsApp MVP (reader + daily ayat), 7. The keyboard & command localization challenge, Telegram command menu, Phase 2 — DRY the duplicated patterns — *done*, _days_keyboard(), _lang_keyboard(), _pace_keyboard() (+15 more)

### Community 144 - "locales/__init__.py"
Cohesion: 0.19
Nodes (5): _load_locales(), _module_name(), is_supported(), is_ui_language(), Language

### Community 146 - "juz_ref"
Cohesion: 0.18
Nodes (4): juz_ref(), to_day_specs(), TestJuzAndPage, TestStorageShape

### Community 147 - "Hifz platform frozen string manifest"
Cohesion: 0.14
Nodes (12): alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Hifz platform frozen string manifest, src/locales/en.py source of truth, Key conventions (btn_*, cmd_*), Wave process (feature agents, translation agents, reviewers) (+4 more)

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
Cohesion: 0.22
Nodes (4): cache(), channel(), graph(), Graph

### Community 158 - "Phase 2 — DRY the duplicated patterns"
Cohesion: 0.14
Nodes (11): graphify knowledge graph (graphify-out/), CLAUDE.md graphify lookup rules, button_rows() row-packing helper, Copy-pasted patterns table (§1.3), GET / health with store and cache status (503), ignore_not_modified() context manager, Phase 2 — DRY the duplicated patterns, Phase 3 — One router for everything (+3 more)

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

### Community 165 - "TestTransliteration"
Cohesion: 0.18
Nodes (3): missing_locales(), TestCatalogue, TestTransliteration

### Community 169 - "TestPickerFlow"
Cohesion: 0.16
Nodes (5): _callback(), _message(), _tab_row(), TestAudioNeverFollowsLanguage, TestPickerFlow

### Community 170 - "button_action"
Cohesion: 0.14
Nodes (4): missing_keys(), _placeholders(), TestGroupLocaleExemption, TestLocaleIntegrity

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 172 - "BismillahBot — Multilingual Support Plan"
Cohesion: 0.13
Nodes (15): 10. File-by-file change list, 11. Memory & performance (free-tier reality), 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 3. Target architecture, 4. User language preference, 6. UI internationalization (i18n) (+7 more)

### Community 175 - "test_keyboard_snapshots.py"
Cohesion: 0.25
Nodes (5): _as_dict(), _keyboards(), _render(), _search_markup(), test_keyboards_match_their_snapshots()

### Community 176 - "reciter_label"
Cohesion: 0.21
Nodes (4): reciter_label(), reciter_page_of(), TestCurrentReciter, TestLabels

### Community 178 - "BismillahBot README"
Cohesion: 0.21
Nodes (9): Translation Attributions, Four ayah representations (english, tafsir, arabic, audio), Known limitations / tech debt, Issues fixed in the refactor (12 bugs), Documentation, BismillahBot README, Inline mode (@BismillahBot ref/range/reciter), Mushaf page reader (/page, /juz, /sajda) (+1 more)

### Community 179 - "load_summary"
Cohesion: 0.21
Nodes (4): ProgressSummary, SurahProgress, load_summary(), TestLoadSummary

### Community 182 - "Blue Green Ci: deploygreen"
Cohesion: 0.33
Nodes (6): environment, if, name, needs, runs-on, deploy-green

### Community 183 - "Blue Green Ci: promote"
Cohesion: 0.33
Nodes (6): promote, environment, if, name, needs, runs-on

### Community 184 - "Choices"
Cohesion: 0.15
Nodes (3): _build(), ignore_not_modified(), build()

### Community 189 - "Dependency rule (app -> bot -> services -> domain)"
Cohesion: 0.18
Nodes (10): tests/test_layering.py ratchet (KNOWN violations), Overlap with MULTI_PLATFORM_PLAN channel seam, Shared UTC offset picker (time_pickers.offset_keyboard), Decisions and open questions (§9), Found along the way (out-of-scope behaviour changes), Phase 0 — Guardrails (ruff, layering test, logging), Phase 5 — Fix the layering, Target layout (app/ bot/ services/ domain/ infra/) (+2 more)

### Community 193 - "json"
Cohesion: 0.27
Nodes (7): export(), languages(), main(), resolved_table(), _write(), build(), main_()

### Community 194 - "send_repeated_audio"
Cohesion: 0.26
Nodes (3): send_repeated_audio(), _stub_audio(), TestRepeatForMemorization

### Community 197 - "offset_options"
Cohesion: 0.20
Nodes (9): offset_choices(), offset_keyboard(), offset_options(), _grid(), test_a_label_prefix_changes_only_the_label(), test_cancel_data_adds_a_localized_cancel_row(), test_every_offset_is_offered_in_order_under_the_callers_prefix(), test_no_cancel_row_unless_asked() (+1 more)

### Community 198 - "test_export_locales_json.py"
Cohesion: 0.22
Nodes (3): _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl()

### Community 200 - "answer_inline_query"
Cohesion: 0.18
Nodes (4): handle_incoming(), _incoming(), answer_inline_query(), resolve_settings()

### Community 205 - "fetch_and_stitch"
Cohesion: 0.29
Nodes (4): fetch_and_stitch(), _fit_for_telegram(), _semaphore(), stitch_images()

### Community 206 - "test_wizard.py"
Cohesion: 0.18
Nodes (3): test_draft_is_written_with_that_ttl(), TestOneDraftPerUser, wiz()

### Community 207 - "send_page_audio"
Cohesion: 0.24
Nodes (4): send_page_audio(), find(), has_page_audio(), TestPageAudio

### Community 208 - "button_action"
Cohesion: 0.27
Nodes (3): button_action(), _reverse_button_map(), TestButtonAction

### Community 210 - "next_scheduled_date"
Cohesion: 0.29
Nodes (3): _advance(), next_scheduled_date(), _validated_days()

### Community 212 - "test_whatsapp_config.py"
Cohesion: 0.38
Nodes (4): env(), test_off_by_default(), test_on_when_fully_configured(), test_the_flag_must_be_truthy()

### Community 214 - "PostgresDailyStore"
Cohesion: 0.13
Nodes (4): PostgresDailyStore, PostgresStore, Store, store()

### Community 215 - ".test_full_flow_queues_the_first_send"
Cohesion: 0.38
Nodes (5): _buttons(), _message(), _tap(), TestTelegramSetup, _texts()

### Community 216 - "MemoryStore"
Cohesion: 0.14
Nodes (6): 5. Caching strategy, 11.1 Profile settings reset after a while — `fix/settings-persistence`, 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, DatabaseUnavailable, MemoryStore

### Community 266 - "_bot"
Cohesion: 0.24
Nodes (7): _bot(), _next_id(), send_audio(), send_photo(), _source(), test_a_miss_caches_under_the_key_and_a_hit_replays_it(), test_a_rejected_cached_id_is_rebuilt_and_recached()

### Community 269 - "get_store"
Cohesion: 0.17
Nodes (6): get_store(), _lock(), _added_update(), TestAdded, TestBoard, TestDailyPost

### Community 270 - "ayah_for"
Cohesion: 0.25
Nodes (4): ayah_for(), test_every_entry_is_a_real_ayah(), test_nothing_repeats_within_one_cycle(), test_same_date_same_ayah()

### Community 275 - "performers"
Cohesion: 0.28
Nodes (4): performers(), reciter_catalog(), reciter_group(), reciter_kind()

### Community 284 - "_plan_keyboards.py"
Cohesion: 0.16
Nodes (14): 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 5 — Fix the layering — *done*, Phase 6 — Repository hygiene — *done*, _cancel_row(), _custom_days_keyboard(), _days_keyboard(), _drill_keyboard() (+6 more)

### Community 286 - "as_command"
Cohesion: 0.29
Nodes (3): as_command(), lang_hint(), TestKeywords

### Community 287 - "get"
Cohesion: 0.29
Nodes (3): get(), _key(), save()

### Community 291 - "check_locales.py"
Cohesion: 0.40
Nodes (3): main(), placeholders(), keyboard_rows()

## Knowledge Gaps
- **51 isolated node(s):** `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres`, `Capacity results 5-1000 concurrent (no errors, 70-91 MB)`, `ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1679 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **139 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `get_store` to `surah_progress`, `_ctx`, `_ctx`, `test_hifz_intervals.py`, `Store`, `render_streak_graph`, `TestRestartDeliversExactlyOnce`, `t`, `Context`, `UserSettings`, `RedisSingleton`, `lifespan.py`, `Hifz Progress Cmd Tests`, `Hifz Streak Tests`, `Acceptance Tests`, `dispatch.py`, `.test_sends_todays_ayah_and_queues_tomorrow`, `Session`, `Streaks`, `Services`, `auth.py`, `load_summary`, `Inline Reciter Search Tests`, `test_hifz_check.py`, `_save_plan`, `summarize`, `reader.py`, `answer_inline_query`, `api/plans.py`, `tick.py`, `PostgresDailyStore`, `.test_full_flow_queues_the_first_send`, `MemoryStore`, `_hifz`, `handle_message`, `weekly_board`, `handle_message`, `stats.py`, `store/__init__.py`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `advancing` be split into smaller, more focused modules?**
  _Cohesion score 0.08819345661450925 - nodes in this community are weakly interconnected._
- **Why does `Ctx` connect `_plan_setup.py` to `features/daily.py`, `reader.py`, `features/profile.py`, `router.py`, `command`, `group.py`, `pages.py`, `t`, `Context`, `features/progress.py`, `lifespan.py`, `Ref`, `TelegramChannel`, `streak.py`, `dispatch.py`, `Mini App Plan`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Ctx` (e.g. with `3. Architecture` and `4.1 Overlap with `MULTI_PLATFORM_PLAN.md``) actually correct?**
  _`Ctx` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Should `Quran` be split into smaller, more focused modules?**
  _Cohesion score 0.05858585858585859 - nodes in this community are weakly interconnected._