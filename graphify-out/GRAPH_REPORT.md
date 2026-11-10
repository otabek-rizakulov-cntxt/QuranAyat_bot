# Graph Report - QuranAyat_bot  (2026-11-10)

## Corpus Check
- 309 files · ~295,229 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 5588 nodes · 13500 edges · 296 communities (172 shown, 124 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1229 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c0f1984e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_plan
- link_token.py
- Quran
- deliver_push
- Wizard
- lifespan.py
- export.py
- streak.py
- to_whatsapp
- dispatch.py
- Ref
- InMemoryScheduleStore
- Wizard
- streak_image.py
- Choice
- UserSettings
- Context
- bot/media.py
- parse_reference
- RedisSingleton
- t
- WhatsAppChannel
- group.py
- Hifz Progress Cmd Tests
- services/plans.py
- Refactor — Implementation Plan
- TelegramChannel
- test_hifz_streak.py
- Hifz Platform - Plan & Progress
- Acceptance Tests
- html
- Docker Compose.stress
- _png
- test_recall_check.py
- stats.py
- infra/uz_audio.py
- _ctx
- Recitation Checker Investigation
- round_percent
- test_dispatch_order.py
- test_uz_audio_feature.py
- TranslationRegistry
- PostgresPlanStore
- to_markup
- handle_update
- Streaks
- asyncio
- Four multilingual dimensions (UI, translation, tafsir, audio)
- Phase 1 — Take `main.py` apart (pure moves) — *done*
- Schema
- Services
- test_tajweed_lessons.py
- features/check.py
- api/progress.py
- fixture
- InMemoryGroupStore
- deliver_quran
- whatsapp_setup.py
- os
- store/__init__.py
- surah_progress
- reciter_group
- .test_full_flow_queues_the_first_send
- Mini App Plan
- local_date
- .page_range
- IdentityStore
- summarize
- InMemoryStore
- features/daily.py
- PostgresScheduleStore
- parse_ayah_range
- Hifz Seam Tests
- session.py
- parse_offset
- InMemoryTajweedStore
- SendCtx
- quran_page_progress
- bundle_translations.py
- Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd
- json
- ._send_media
- Groups: PostgresGroupStore
- InMemorySessionStore
- Scheduler Tests
- routes/whatsapp.py
- PostgresProfileStore
- tajweed_lessons.py
- main.py
- test_api_auth.py
- Store Contract Tests
- Multi Platform Plan: MultiPlatform Implementation Plan
- test_inline_reciter_search.py
- _hifz
- PlanDaySpec
- test_whatsapp_router.py
- Hifz Seam Tests: TestRegistration
- test_hifz_check.py
- Scheduler Tests: TestTransientFailuresAreRetried
- _message
- GraphClient
- File
- _at
- api/uz_audio.py
- recall_check.py
- button_action
- test_tajweed_audio.py
- debug.py
- InMemoryIdentityStore
- asyncio
- BismillahBot — Business Logic
- handlers/settings.py
- TestSchedule
- offset_keyboard
- post
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- scheduler/__init__.py
- InMemoryProfileStore
- PostgresIdentityStore
- test_store_selection.py
- compute_streak
- Hifz platform frozen string manifest
- _align
- build_grid
- PostgresHifzStore
- Blue Green Ci: jobs
- Blue Green Ci: with
- Portion
- Store
- time
- weekly_board
- TestPlans
- Channel
- TestPickerFlow
- reciter_keyboard
- .get_next_ayah
- Tajweed (tajvid) section: plan
- re
- MINI_APP_PLAN.md
- sys
- TestRestartDeliversExactlyOnce
- parse_ayah
- test_hifz_leaderboard.py
- MINI_APP_PLAN.md
- keyboards/menu.py
- TestLeaderboard
- send_page
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- _FakePool
- MemoryStore
- Blue Green Ci: env
- test_channels_whatsapp.py
- TestProfiles
- graphify-autopush.sh
- test_settings.py
- Dependency rule (app -> bot -> services -> domain)
- uz_translit.py
- health
- Blue Green Ci: postgres
- Blue Green Ci: test
- Blue Green Ci: preflight
- make_whatsapp_avatar.py
- PostgresProfileStore
- Hifz Seam Tests: TestPrefixNamespace
- Hifz Seam Tests: TestDispatchCallback
- Profile settings reset fix (fix/settings-persistence)
- features/__init__.py
- Blue Green Ci: smokegreen
- test_miniapp_links.py
- FakeChannel
- test_webhook.py
- test_uz_audio_timings.py
- features/tajweed.py
- ayah_for
- BismillahBot README
- test_keyboard_snapshots.py
- week_window
- Graph
- Blue Green Ci: deploygreen
- Blue Green Ci: promote
- TestHifzIntervalEdges
- lang_hint
- Hifz Seam Tests: test_longest_prefix_wins
- percentile_band
- SendCtx
- .test_concatenates_the_ayahs_in_order
- .search_performers
- TestIdentity
- Claude
- WhatsAppChannel
- Hifz Seam Tests: TestDispatchCommand
- _callback
- .wa_user
- handle_message
- ignore_not_modified
- Graph
- week_bounds
- test_whatsapp_config.py
- exchange
- WhatsAppChannel
- TestSessions
- milestone_for
- export_web_content.py
- WhatsAppError
- level_for
- BismillahBot — Multilingual Support Plan
- Telegram
- reset_for_tests
- test_hifz_seam.py
- parse_quran_tafsir
- TestSettings
- UserSettingsRow
- PostgresDailyStore
- t
- probe
- for_platform
- graph
- TestRunScheduler
- .has_page_audio
- sessions
- TestDailyPost
- test_reciter_picker.py
- test_telegram_reader_shows_the_row_to_an_uzbek_user
- Separate quranayat-miniapp Next.js repo; API in this repo
- test_store_contract.py
- SendCtx
- TestRegistration
- domain/tajweed.py
- test_export_web_content.py
- WhatsApp

## God Nodes (most connected - your core abstractions)
1. `get_store()` - 178 edges
2. `Ctx` - 168 edges
3. `t()` - 150 edges
4. `Quran` - 143 edges
5. `handle_update()` - 103 edges
6. `fixture()` - 93 edges
7. `UserSettings` - 84 edges
8. `Choice` - 77 edges
9. `build_plan()` - 72 edges
10. `File` - 64 edges

## Surprising Connections (you probably didn't know these)
- `5. Caching strategy` --references--> `MemoryStore`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/infra/redis_client.py
- `3. Target architecture` --references--> `TranslationRegistry`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/domain/quran.py
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `Phase 3 — Hifz parity` --references--> `build_plan()`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/domain/plan_builder.py
- `2. Current-state audit (what is hardcoded English)` --references--> `build_data()`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/app/lifespan.py

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

## Communities (296 total, 124 thin omitted)

### Community 0 - "build_plan"
Cohesion: 0.05
Nodes (17): advancing(), auto_pace(), build_plan(), juz_ref(), surah_ref(), to_day_specs(), assert_well_formed(), spans() (+9 more)

### Community 1 - "link_token.py"
Cohesion: 0.19
Nodes (8): _b64(), InvalidLinkToken, issue(), _key(), redeem(), _secret(), _unb64(), TestToken

### Community 2 - "Quran"
Cohesion: 0.05
Nodes (20): random_ayah(), read_text(), _consolidations(), Quran, _span_length(), ayah_count(), TestSurahSpans, TestAyahCount (+12 more)

### Community 3 - "deliver_push"
Cohesion: 0.19
Nodes (10): deliver_push(), _log(), ctx_for(), say_hi(), test_every_push_is_logged_for_cost_tracking(), TestConsent, TestFreeMode, TestTelegram (+2 more)

### Community 4 - "Wizard"
Cohesion: 0.06
Nodes (9): Wizard, test_draft_is_written_with_that_ttl(), TestAccumulation, TestCancel, TestCoexistsWithTheReciterFlow, TestCorruptState, TestLifecycle, TestOneDraftPerUser (+1 more)

### Community 5 - "lifespan.py"
Cohesion: 0.05
Nodes (26): create_app(), _commands_for(), initialize(), lifespan(), _set_bot_commands(), get_default_query_results(), inline_photo_results(), range_audio_url() (+18 more)

### Community 6 - "export.py"
Cohesion: 0.14
Nodes (12): decode_16k(), mp3_path(), Mp3Info, probe(), to_float(), build_surah(), frames_of(), chunk_bounds() (+4 more)

### Community 7 - "streak.py"
Cohesion: 0.18
Nodes (8): _caption(), _keyboard(), on_streak(), _send_graph(), streak(), cache_key(), StreakSummary, TestCacheKey

### Community 8 - "to_whatsapp"
Cohesion: 0.08
Nodes (8): _Converter, _render(), split(), to_whatsapp(), _wrap(), TestSplit, TestTags, TestWhatTheBotSends

### Community 9 - "dispatch.py"
Cohesion: 0.09
Nodes (14): handle_incoming(), _incoming(), _on_callback(), _on_text(), _search_reciters(), answer_inline_query(), resolve_settings(), _now() (+6 more)

### Community 10 - "Ref"
Cohesion: 0.06
Nodes (19): _clip(), _covered(), _focus_surah(), _intersect(), _page_share(), _pages_of(), _recency_key(), _surah_of() (+11 more)

### Community 12 - "Wizard"
Cohesion: 0.08
Nodes (13): get_store(), _lock(), _CallbackQuery, _ctx(), _Message, _run_wizard(), _Settings, _tap() (+5 more)

### Community 13 - "streak_image.py"
Cohesion: 0.15
Nodes (7): render(), draw_contribution_graph(), render_streak_graph(), _semaphore(), open_png(), TestRendering, TestRenderStreakGraph

### Community 14 - "Choice"
Cohesion: 0.06
Nodes (48): Ctx, _begin_setup(), _is_group_admin(), _join_board(), on_group_tap(), _save_group_plan(), setup_step(), _step_post_time() (+40 more)

### Community 15 - "UserSettings"
Cohesion: 0.11
Nodes (9): patch_settings(), UserSettings, _seed_legacy_lang(), TestDefaults, TestIndependence, TestInlineCaller, TestKeyedByUserId, TestLegacyMigration (+1 more)

### Community 16 - "Context"
Cohesion: 0.13
Nodes (15): _added_update(), _bot(), _ctx(), _member(), _run_setup_to_plan(), _Settings, TestAdded, TestBoard (+7 more)

### Community 17 - "bot/media.py"
Cohesion: 0.07
Nodes (14): fetch_and_stitch(), _fit_for_telegram(), _semaphore(), stitch_images(), TestCodes, test_a_week_on_whatsapp_matches_a_week_on_telegram(), _week(), _bot() (+6 more)

### Community 18 - "parse_reference"
Cohesion: 0.06
Nodes (12): _clean(), format_ref(), page_ref(), parse_range(), parse_reference(), plan_target(), TestAcrossSurahs, TestFormatting (+4 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.06
Nodes (21): 6. Issues fixed in this refactor, _is_telegram_id(), link(), _code_key(), issue(), redeem(), too_many_tries(), _tries_key() (+13 more)

### Community 20 - "t"
Cohesion: 0.08
Nodes (22): memorize(), session(), _ref_from_draft(), _ref_to_draft(), _send_drill(), _start_drill(), _cancel_row(), _custom_days_keyboard() (+14 more)

### Community 21 - "WhatsAppChannel"
Cohesion: 0.15
Nodes (4): _bytes_and_name(), _resolve(), _split_choices(), TestMedia

### Community 22 - "group.py"
Cohesion: 0.06
Nodes (30): patch_profile(), bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), _enqueue_next_board(), _enqueue_next_group() (+22 more)

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.14
Nodes (12): _CallbackQuery, _ctx(), _edited(), _intervals(), _mark(), _Message, _progress(), _sent() (+4 more)

### Community 24 - "services/plans.py"
Cohesion: 0.06
Nodes (40): active(), _build(), complete(), create(), DrillOut, lifecycle(), _plan_out(), PlanCreateIn (+32 more)

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.08
Nodes (25): graphify knowledge graph (graphify-out/), CLAUDE.md graphify lookup rules, 10. Found along the way (out of scope — behaviour changes), 2. Goals and non-goals, 3. Principles applied, 6. Ordering, risk, size, 7. Safety net, 8. Expected result (+17 more)

### Community 26 - "TelegramChannel"
Cohesion: 0.08
Nodes (10): TelegramChannel, bot(), cache(), test_whatsapp_dressing_is_dropped(), TestAnswerAndTyping, TestChoice, TestEditChoices, TestEditText (+2 more)

### Community 27 - "test_hifz_streak.py"
Cohesion: 0.14
Nodes (11): _caption(), _ctx(), _earn(), _photo_message(), _Settings, _streak(), TestCallback, TestGraphCache (+3 more)

### Community 28 - "Hifz Platform - Plan & Progress"
Cohesion: 0.09
Nodes (20): Hifz Platform - Plan & Progress, Phase 1 acceptance criteria (tests/test_acceptance.py), Hifz change log, claim_due claimed_at clock bug, Hifz data model (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send, group_*), Phase 2 group cluster (J1-J6, forum topics), Workstream I: i18n & commands for 48 locales, Workstream C: interval merge-on-insert + derived percentages (+12 more)

### Community 29 - "Acceptance Tests"
Cohesion: 0.09
Nodes (15): _CallbackQuery, _cmd(), _ctx(), _isolate_registries(), _Message, _run_wizard(), _save_plan(), _Settings (+7 more)

### Community 30 - "html"
Cohesion: 0.18
Nodes (8): surah_name(), _translation_text(), forgot_command(), on_progress_tap(), progress_command(), progress_view(), _show(), _surah_line()

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 33 - "test_recall_check.py"
Cohesion: 0.03
Nodes (28): swept(), test_a_different_date_gives_a_different_question(), test_both_question_modes_show_up_in_the_sweep(), test_correct_option_is_never_a_length_outlier(), test_correct_option_is_never_the_extreme_by_a_wide_ratio(), test_correct_option_really_follows_the_prompt(), test_dates_and_iso_strings_are_interchangeable(), test_every_option_carries_the_same_word_count() (+20 more)

### Community 34 - "stats.py"
Cohesion: 0.35
Nodes (8): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut

### Community 35 - "infra/uz_audio.py"
Cohesion: 0.15
Nodes (11): byte_range(), part_key(), entry(), estimated(), Part, parts(), seconds(), size() (+3 more)

### Community 36 - "_ctx"
Cohesion: 0.08
Nodes (17): _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _isolate_registries(), _Message, _profile_row() (+9 more)

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.07
Nodes (29): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards (+21 more)

### Community 38 - "round_percent"
Cohesion: 0.08
Nodes (5): format_percent(), PageProgress, _Ratio, round_percent(), TestRounding

### Community 39 - "test_dispatch_order.py"
Cohesion: 0.24
Nodes (15): _callback(), fake_bot(), _message(), _sent_a_verse(), test_a_command_beats_a_pending_reciter_search(), test_a_command_escapes_a_wizard_without_ending_it(), test_a_pending_reciter_search_beats_a_wizard(), test_a_wizard_beats_the_reference_parser() (+7 more)

### Community 40 - "test_uz_audio_feature.py"
Cohesion: 0.10
Nodes (19): _baqarah(), _data(), _fatiha(), fetched(), _patch_client(), client(), table(), test_api_send_runs_the_bot_feature() (+11 more)

### Community 41 - "TranslationRegistry"
Cohesion: 0.08
Nodes (9): 12. Testing, parse_quran(), TranslationRegistry, TestCorpusIntegrity, _nfc(), test_the_basmala_heading_is_not_part_of_the_question(), TestAvailable, TestCaching (+1 more)

### Community 42 - "PostgresPlanStore"
Cohesion: 0.06
Nodes (4): PlanDayRow, PlanRow, PlanStore, PostgresPlanStore

### Community 43 - "to_markup"
Cohesion: 0.19
Nodes (5): verse_keyboard(), to_markup(), TestToMarkup, _button(), TestVerseKeyboard

### Community 44 - "handle_update"
Cohesion: 0.20
Nodes (7): reference(), _inline_query(), _of_type(), _results(), TestInlineArabicImage, TestRangeAudio, TestRangeText

### Community 45 - "Streaks"
Cohesion: 0.13
Nodes (4): record_session(), TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 47 - "Four multilingual dimensions (UI, translation, tafsir, audio)"
Cohesion: 0.13
Nodes (14): Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), Quran.from_file(path) refactor, setMyCommands per language, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+6 more)

### Community 48 - "Phase 1 — Take `main.py` apart (pure moves) — *done*"
Cohesion: 0.08
Nodes (17): 1. Why, 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 1 — Take `main.py` apart (pure moves) — *done*, Phase 4 — Split infrastructure god-objects — *done*, Phase 5 — Fix the layering — *done*, Phase 6 — Repository hygiene — *done*, _post_portion() (+9 more)

### Community 49 - "Schema"
Cohesion: 0.10
Nodes (30): daily_ayah_sub, group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval (+22 more)

### Community 50 - "Services"
Cohesion: 0.15
Nodes (20): client(), _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today() (+12 more)

### Community 51 - "test_tajweed_lessons.py"
Cohesion: 0.19
Nodes (13): on_tajweed(), tajvid(), test_without_the_audio_base_url_there_is_nothing_yet(), _buttons(), _ctx(), reviewers(), test_bad_callbacks_are_only_acknowledged(), test_editing_a_lesson_sends_it_back_to_draft() (+5 more)

### Community 52 - "features/check.py"
Cohesion: 0.09
Nodes (15): _answer_data(), _ask(), check(), on_check(), _options_keyboard(), _parse_answer(), _question_text(), _score() (+7 more)

### Community 53 - "api/progress.py"
Cohesion: 0.08
Nodes (33): require_user(), answer(), AnswerIn, AnswerOut, make_token(), question(), QuestionOut, read_token() (+25 more)

### Community 54 - "fixture"
Cohesion: 0.06
Nodes (34): _clean_state_store(), build_data(), make_index(), data(), _jwt_secret(), data(), data(), data() (+26 more)

### Community 55 - "InMemoryGroupStore"
Cohesion: 0.06
Nodes (6): GroupConfig, GroupMemberLink, GroupPlanDayRow, GroupPlanRow, GroupStore, InMemoryGroupStore

### Community 56 - "deliver_quran"
Cohesion: 0.08
Nodes (16): inline_audio_result(), combined_audio_key(), deliver_combined_audio(), stitch(), deliver_quran(), deliver_repeated_audio(), stitch(), ref_key() (+8 more)

### Community 57 - "whatsapp_setup.py"
Cohesion: 0.15
Nodes (12): automation(), _bot_api(), Graph, main(), profile(), _show(), status(), telegram() (+4 more)

### Community 58 - "os"
Cohesion: 0.11
Nodes (18): export(), languages(), main(), resolved_table(), _write(), build(), main_(), _absolute_imports() (+10 more)

### Community 59 - "store/__init__.py"
Cohesion: 0.14
Nodes (6): Milestone, offset_of(), StreakCounts, MemoryState, user_offset(), state()

### Community 60 - "surah_progress"
Cohesion: 0.11
Nodes (7): juz_progress(), JuzProgress, quran_progress(), _spans(), started_juzs(), TestJuzProgress, TestQuranProgress

### Community 61 - "reciter_group"
Cohesion: 0.39
Nodes (3): reciter_page_of(), reciter_group(), TestCurrentReciter

### Community 62 - ".test_full_flow_queues_the_first_send"
Cohesion: 0.22
Nodes (8): _buttons(), _message(), _send_ctx(), _tap(), TestTelegramDelivery, TestTelegramSetup, _texts(), tg_bot()

### Community 63 - "Mini App Plan"
Cohesion: 0.08
Nodes (25): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 4.1 Flow, 4.2 Rules (+17 more)

### Community 64 - "local_date"
Cohesion: 0.14
Nodes (8): _as_utc(), local_date(), local_now(), local_time(), next_due_utc(), TestLocalDate, TestNextDueUtc, _utc()

### Community 65 - ".page_range"
Cohesion: 0.10
Nodes (9): juz(), page(), reader_position(), deliver_page(), source(), stitch(), page_caption(), test_page_boundaries_match_the_bot() (+1 more)

### Community 67 - "summarize"
Cohesion: 0.05
Nodes (13): Progress, ProgressSummary, started_surahs(), summarize(), surah_progress(), SurahProgress, load_summary(), _at() (+5 more)

### Community 68 - "InMemoryStore"
Cohesion: 0.08
Nodes (8): InMemoryDailyStore, InMemoryStore, InMemoryPlanStore, store(), store(), store(), store(), store()

### Community 69 - "features/daily.py"
Cohesion: 0.12
Nodes (18): _ask_time(), daily(), _enable(), _hhmm(), _offset(), on_tap(), _parse_time(), session() (+10 more)

### Community 70 - "PostgresScheduleStore"
Cohesion: 0.10
Nodes (3): PostgresStore, PostgresScheduleStore, PostgresSessionStore

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 73 - "session.py"
Cohesion: 0.15
Nodes (20): init_data_max_age(), jwt_secret(), auth_link(), auth_telegram(), AuthOut, LinkAuthIn, me(), _me() (+12 more)

### Community 74 - "parse_offset"
Cohesion: 0.10
Nodes (5): format_offset(), parse_offset(), TestFormatOffset, TestParseOffset, TestPicker

### Community 75 - "InMemoryTajweedStore"
Cohesion: 0.09
Nodes (4): ApprovalRow, InMemoryTajweedStore, PostgresTajweedStore, TajweedStore

### Community 76 - "SendCtx"
Cohesion: 0.13
Nodes (12): catch_up(), run_scheduler(), _wait(), _deliver(), _is_stale(), _lock(), _release(), _resolve() (+4 more)

### Community 77 - "quran_page_progress"
Cohesion: 0.11
Nodes (4): juz_page_progress(), quran_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 78 - "bundle_translations.py"
Cohesion: 0.22
Nodes (7): bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.12
Nodes (18): Audio catalog kinds, Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES), Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points), Error taxonomy L1-L5 (word, harakah, tajwid, riwayah mismatch, waqf), Evaluation plan (false-alarm gate < 2% per ayah) (+10 more)

### Community 80 - "json"
Cohesion: 0.13
Nodes (11): _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl(), _as_dict(), _ctx(), _Settings, _static_cases(), test_hifz_keyboards_match_their_snapshots() (+3 more)

### Community 81 - "._send_media"
Cohesion: 0.15
Nodes (4): _build(), _send(), send_cached(), build()

### Community 83 - "InMemorySessionStore"
Cohesion: 0.09
Nodes (5): InMemorySessionStore, LeaderboardEntry, SessionRow, SessionStore, WeeklyBoard

### Community 84 - "Scheduler Tests"
Cohesion: 0.17
Nodes (4): _claimed_at(), _record(), TestCatchUp, TestTick

### Community 85 - "routes/whatsapp.py"
Cohesion: 0.12
Nodes (10): _process_update(), telegram_webhook(), _first_delivery(), messages_of(), _process(), receive(), signature(), verify() (+2 more)

### Community 87 - "tajweed_lessons.py"
Cohesion: 0.18
Nodes (18): _listen(), _unit(), _unit_track(), audio_lesson(), audio_lessons(), audio_units(), audio_url(), AudioLesson (+10 more)

### Community 88 - "main.py"
Cohesion: 0.11
Nodes (3): privacy(), setup_logging(), test_http_client_request_urls_are_never_logged()

### Community 89 - "test_api_auth.py"
Cohesion: 0.17
Nodes (20): _init_data_secret(), InvalidInitData, sign_init_data(), validate_init_data(), _auth(), _fields(), test_added_field_is_rejected(), test_auth_drops_malformed_start_param() (+12 more)

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.08
Nodes (24): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+16 more)

### Community 92 - "test_inline_reciter_search.py"
Cohesion: 0.10
Nodes (36): handle_update(), _callback(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index(), test_inline_query_valid_ayah_returns_all_four_views() (+28 more)

### Community 93 - "_hifz"
Cohesion: 0.07
Nodes (10): _assert_invariant(), _ayahs(), _hifz(), _spans(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order(), TestAddInterval (+2 more)

### Community 95 - "test_whatsapp_router.py"
Cohesion: 0.19
Nodes (8): bodies(), fixture_message(), known_user(), rows(), tap(), TestBoundaries, TestMenu, TestStarters

### Community 97 - "test_hifz_check.py"
Cohesion: 0.08
Nodes (18): refresh_streaks(), streak_summary(), user_today(), _answer_data(), _AnyDay, _ask(), _asked(), _buttons() (+10 more)

### Community 99 - "_message"
Cohesion: 0.11
Nodes (9): data(), fake_bot(), _message(), _no_network(), TestCommandArguments, TestJuzCommand, TestPageCommand, TestSajdaCommand (+1 more)

### Community 101 - "File"
Cohesion: 0.10
Nodes (5): File, TestAudioFilename, TestImageFilename, TestLegacyLanguageKey, TestStateStore

### Community 103 - "api/uz_audio.py"
Cohesion: 0.29
Nodes (6): send(), SendIn, SendOut, available(), send_to_user(), valid_clip()

### Community 104 - "recall_check.py"
Cohesion: 0.06
Nodes (28): _assemble(), _at_offset(), _ayah_text(), _basmala_prefix(), build_question(), _clean(), _continuation_question(), corpus() (+20 more)

### Community 105 - "button_action"
Cohesion: 0.07
Nodes (12): main(), button_action(), keyboard_rows(), missing_keys(), missing_locales(), welcome_text(), _placeholders(), TestButtonAction (+4 more)

### Community 106 - "test_tajweed_audio.py"
Cohesion: 0.15
Nodes (15): _buttons(), client(), _ctx(), env(), _labels(), _login(), test_api_refuses_unknown_and_draft_lessons(), test_api_state_and_done() (+7 more)

### Community 107 - "debug.py"
Cohesion: 0.27
Nodes (16): quiet_mask(), cmd_clip(), cmd_nudge(), cmd_purge(), cmd_report(), cmd_set(), cmd_show(), cmd_smoke() (+8 more)

### Community 109 - "asyncio"
Cohesion: 0.10
Nodes (14): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+6 more)

### Community 110 - "BismillahBot — Business Logic"
Cohesion: 0.11
Nodes (17): 1. Overview, 2. Architecture, 3. Request lifecycle, 5. Caching strategy, 7. Known limitations / tech debt, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic (+9 more)

### Community 111 - "handlers/settings.py"
Cohesion: 0.09
Nodes (16): 7. The keyboard & command localization challenge, Telegram command menu, Phase 2 — DRY the duplicated patterns — *done*, language(), set_translation_language(), set_ui_language(), show_languages(), translation() (+8 more)

### Community 113 - "offset_keyboard"
Cohesion: 0.28
Nodes (8): offset_keyboard(), offset_options(), _grid(), test_a_label_prefix_changes_only_the_label(), test_cancel_data_adds_a_localized_cancel_row(), test_every_offset_is_offered_in_order_under_the_callers_prefix(), test_no_cancel_row_unless_asked(), test_rows_are_columns_wide()

### Community 114 - "post"
Cohesion: 0.11
Nodes (7): client(), handled(), post(), test_not_mounted_unless_configured(), TestDelivery, TestHandshake, TestSignature

### Community 115 - "Koyeb Capacity Report"
Cohesion: 0.25
Nodes (7): Koyeb free-tier capacity report, CPU-bound queueing failure mode (~24 msg/s ceiling), Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start), Neon managed Postgres, Capacity results 5-1000 concurrent (no errors, 70-91 MB), Stress environment (docker-compose.stress.yml, cpus 0.1, 512m), Synthetic traffic mix (scripts/stress/gen_updates.py)

### Community 116 - "Blue Green Ci"
Cohesion: 0.14
Nodes (13): concurrency, cancel-in-progress, group, env, PYTHON_DEFAULT, name, on, pull_request (+5 more)

### Community 117 - "Blue Green Ci: name"
Cohesion: 0.23
Nodes (14): steps, steps, steps, steps, steps, steps, steps, env (+6 more)

### Community 118 - "scheduler/__init__.py"
Cohesion: 0.09
Nodes (7): enqueue(), idempotency_key(), schedule_daily(), register_send_handler(), registered_kinds(), _same_origin(), ScheduledSend

### Community 121 - "test_store_selection.py"
Cohesion: 0.13
Nodes (8): database_url(), fast_retries(), fresh_redis(), _Reachable, strict(), TestStrictByDefault, from_url(), _Unreachable

### Community 122 - "compute_streak"
Cohesion: 0.24
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 123 - "Hifz platform frozen string manifest"
Cohesion: 0.22
Nodes (8): Hifz platform frozen string manifest, src/locales/en.py source of truth, Key conventions (btn_*, cmd_*), Wave process (feature agents, translation agents, reviewers), Native-speaker review - hifz platform strings, Locale review tracking table (47 locales), Review process steps, Review criteria (meaning, register, grammatical number, RTL, button length)

### Community 124 - "_align"
Cohesion: 0.10
Nodes (18): align(), _align(), containment(), load_pins(), main(), onset_cut(), quiet_runs(), skeleton() (+10 more)

### Community 125 - "build_grid"
Cohesion: 0.18
Nodes (4): build_grid(), _counts(), Grid, TestGrid

### Community 126 - "PostgresHifzStore"
Cohesion: 0.06
Nodes (11): _covers(), HifzInterval, HifzStore, InMemoryHifzStore, _merge_span(), _normalize(), _overlaps(), PostgresHifzStore (+3 more)

### Community 127 - "Blue Green Ci: jobs"
Cohesion: 0.15
Nodes (13): name, needs, runs-on, jobs, build, lint, rollback, name (+5 more)

### Community 128 - "Blue Green Ci: with"
Cohesion: 0.15
Nodes (13): with, cache, cache-dependency-path, cache-from, cache-to, context, if-no-files-found, load (+5 more)

### Community 131 - "time"
Cohesion: 0.18
Nodes (12): _b64url(), _b64url_decode(), decode_token(), InvalidToken, issue_token(), _sign(), _unauthorized(), test_expired_token_is_rejected() (+4 more)

### Community 132 - "weekly_board"
Cohesion: 0.28
Nodes (3): weekly_board(), make_user(), TestWeeklyBoard

### Community 135 - "TestPickerFlow"
Cohesion: 0.16
Nodes (5): _callback(), _message(), _tab_row(), TestAudioNeverFollowsLanguage, TestPickerFlow

### Community 136 - "reciter_keyboard"
Cohesion: 0.15
Nodes (7): reciter_keyboard(), reciter_label(), reciter_page_count(), _pager_row(), _reciter_buttons(), TestLabels, TestPagination

### Community 137 - ".get_next_ayah"
Cohesion: 0.18
Nodes (6): 4. Navigation model, Page images and page audio, Structural divisions (page / juz / sajda), Translation-only catalogue entries, assert_covers_target_once(), TestNavigation

### Community 138 - "Tajweed (tajvid) section: plan"
Cohesion: 0.12
Nodes (15): 10. Phases, 11. Testing, 12. Attribution, 13. Open questions, 14. Revision 2026-11-10: the audio track, progress, phases P1–P5, 1. Decisions (2026-11-09), 2. Data: where the rules come from, 3. Curriculum (v1, ~24 lessons) (+7 more)

### Community 139 - "re"
Cohesion: 0.21
Nodes (8): placeholders(), duration(), _id3_size(), main(), _modules(), test_nothing_builds_telegram_markup_by_hand_outside_those_modules(), test_only_group_code_reads_the_telegram_client(), test_only_telegram_only_modules_import_telegram()

### Community 140 - "MINI_APP_PLAN.md"
Cohesion: 0.13
Nodes (13): Central callback prefix allocation (hifz.PREFIXES), Future roadmap and prioritized backlog, The hifz platform (memorization companion), Streak day ticks on completed session, Bot ↔ Mini App integration (menu button, startapp, /app), Identity table (platform, external_id → user_id), Normalized Incoming event, Neutral message model rendering (HTML / WhatsApp markup) (+5 more)

### Community 141 - "sys"
Cohesion: 0.26
Nodes (8): main(), score(), _env(), _lessons(), _local(), main(), upload(), verify()

### Community 144 - "test_hifz_leaderboard.py"
Cohesion: 0.12
Nodes (10): _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join(), _Message, _sent(), _Settings (+2 more)

### Community 145 - "MINI_APP_PLAN.md"
Cohesion: 0.18
Nodes (12): Pure plan builder (build_plan), /api/v1 REST surface, initData HMAC validation → short-lived JWT, OpenAPI → TypeScript client pipeline, Recall check integrity (signed question_token), Mini App risks, Other platforms shortlist (Messenger, Viber, Discord, PWA, Signal), Multi-platform phased breakdown (Phases 0-6) (+4 more)

### Community 146 - "keyboards/menu.py"
Cohesion: 0.15
Nodes (15): command, Routing rules (in `serve`), about(), app(), help_(), index(), start(), _welcome() (+7 more)

### Community 148 - "send_page"
Cohesion: 0.14
Nodes (10): send_page(), send_repeated_audio(), _buffer(), _stub_audio(), _stub_stitch(), stub(), TestPageCard, capture() (+2 more)

### Community 152 - "_FakePool"
Cohesion: 0.23
Nodes (4): _failing_create_pool(), create_pool(), _FakePool, TestUnreachableDatabase

### Community 153 - "MemoryStore"
Cohesion: 0.15
Nodes (5): 11.1 Profile settings reset after a while — `fix/settings-persistence`, 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, DatabaseUnavailable, MemoryStore

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 155 - "test_channels_whatsapp.py"
Cohesion: 0.13
Nodes (6): taps(), TestChoices, TestDressing, TestNumberedMenuLifetime, TestText, TestTransport

### Community 159 - "Dependency rule (app -> bot -> services -> domain)"
Cohesion: 0.22
Nodes (8): tests/test_layering.py ratchet (KNOWN violations), Overlap with MULTI_PLATFORM_PLAN channel seam, Decisions and open questions (§9), Phase 0 — Guardrails (ruff, layering test, logging), Phase 5 — Fix the layering, Target layout (app/ bot/ services/ domain/ infra/), Timezone picker by country (feat/timezone-by-country), Memorizing (hifz): /memorize, /check, /progress, /streak, /leaderboard, /profile

### Community 160 - "uz_translit.py"
Cohesion: 0.21
Nodes (7): _case(), to_cyrillic(), to_latin(), _word_to_cyr(), test_cyrillic_titles_round_trip(), test_cyrillic_is_real_cyrillic_and_round_trips(), test_transliteration_cases()

### Community 161 - "health"
Cohesion: 0.24
Nodes (3): health(), store_backend(), TestHealthReportsTheStores

### Community 162 - "Blue Green Ci: postgres"
Cohesion: 0.22
Nodes (9): POSTGRES_DB, POSTGRES_HOST_AUTH_METHOD, POSTGRES_USER, env, image, options, ports, postgres (+1 more)

### Community 163 - "Blue Green Ci: test"
Cohesion: 0.22
Nodes (9): TEST_DATABASE_URL, test, python-version, fail-fast, matrix, env, name, runs-on (+1 more)

### Community 164 - "Blue Green Ci: preflight"
Cohesion: 0.22
Nodes (9): preflight, active, deploy_enabled, target, if, name, needs, outputs (+1 more)

### Community 169 - "Profile settings reset fix (fix/settings-persistence)"
Cohesion: 0.18
Nodes (14): Documentation index (docs/README.md), ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable, GET / health with store and cache status (503), Silent in-memory store fallback, Phase 6 — Repository hygiene, Profile settings reset fix (fix/settings-persistence), Typed frozen Settings (config/settings.py), Blue-Green CI pipeline (blue-green-ci.yml) (+6 more)

### Community 170 - "features/__init__.py"
Cohesion: 0.07
Nodes (23): Phase 3 — One router for everything — *done*, _board_message(), leaderboard(), on_leaderboard(), turn_page(), callback(), decorate(), _cancel() (+15 more)

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 172 - "test_miniapp_links.py"
Cohesion: 0.16
Nodes (11): page_keyboard(), _app_command(), app_on(), data(), test_app_command(), test_app_command_without_url(), test_cards_and_drill_link_to_their_screens(), test_inline_messages_never_get_a_web_app_button() (+3 more)

### Community 173 - "FakeChannel"
Cohesion: 0.12
Nodes (12): build(), send_surah(), build(), surah_key(), fetch(), url(), FakeChannel, test_big_surah_goes_in_parts() (+4 more)

### Community 174 - "test_webhook.py"
Cohesion: 0.22
Nodes (4): webhook_secret(), test_startup_registers_the_webhook_without_the_token(), test_the_secret_does_not_reveal_the_token(), test_webhook_acks_before_initialization()

### Community 175 - "test_uz_audio_timings.py"
Cohesion: 0.13
Nodes (9): Fixing a wrong timing, Format and the download formula, Pipeline, Setup (once), Transcribing on Colab (preferred), Uzbek translation audio — timing tool, reset_for_tests(), real_table() (+1 more)

### Community 176 - "features/tajweed.py"
Cohesion: 0.11
Nodes (21): state(), _done_row(), _duration(), _lesson(), _mark_done(), _nav_row(), _play(), _review() (+13 more)

### Community 177 - "ayah_for"
Cohesion: 0.22
Nodes (4): ayah_for(), test_every_entry_is_a_real_ayah(), test_nothing_repeats_within_one_cycle(), test_same_date_same_ayah()

### Community 178 - "BismillahBot README"
Cohesion: 0.13
Nodes (13): Translation Attributions, alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Four ayah representations (english, tafsir, arabic, audio), Known limitations / tech debt, Issues fixed in the refactor (12 bugs) (+5 more)

### Community 179 - "test_keyboard_snapshots.py"
Cohesion: 0.23
Nodes (5): _as_dict(), _keyboards(), _render(), _search_markup(), test_keyboards_match_their_snapshots()

### Community 180 - "week_window"
Cohesion: 0.25
Nodes (3): user_week_window(), week_window(), TestWeekWindow

### Community 182 - "Blue Green Ci: deploygreen"
Cohesion: 0.33
Nodes (6): environment, if, name, needs, runs-on, deploy-green

### Community 183 - "Blue Green Ci: promote"
Cohesion: 0.33
Nodes (6): promote, environment, if, name, needs, runs-on

### Community 185 - "lang_hint"
Cohesion: 0.18
Nodes (3): lang_hint(), TestKeywords, TestUsernames

### Community 188 - "SendCtx"
Cohesion: 0.10
Nodes (14): Phase 1 — Channel seam (this repo, no user-visible change), 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, push_daily(), _template_text(), _consented(), push_plan_day(), _send_plain_message() (+6 more)

### Community 189 - ".test_concatenates_the_ayahs_in_order"
Cohesion: 0.20
Nodes (4): content(), fake_download(), TestStitching, __init__()

### Community 193 - "WhatsAppChannel"
Cohesion: 0.13
Nodes (4): _clip(), WhatsAppChannel, interactive(), TestTheRest

### Community 197 - ".wa_user"
Cohesion: 0.36
Nodes (4): apps(), Apps, _code(), TestLinking

### Community 198 - "handle_message"
Cohesion: 0.16
Nodes (8): _allowed_command(), as_command(), handle_message(), _tap(), TestFirstContact, stitch(), TestReader, text()

### Community 199 - "ignore_not_modified"
Cohesion: 0.31
Nodes (4): ignore_not_modified(), test_any_other_bad_request_propagates(), test_not_modified_is_swallowed(), test_other_errors_propagate()

### Community 205 - "test_whatsapp_config.py"
Cohesion: 0.31
Nodes (5): env(), test_any_missing_value_keeps_it_off(), test_off_by_default(), test_on_when_fully_configured(), test_the_flag_must_be_truthy()

### Community 206 - "exchange"
Cohesion: 0.22
Nodes (3): exchange(), test_whatsapp_app_sends_a_working_sign_in_link(), TestExchange

### Community 207 - "WhatsAppChannel"
Cohesion: 0.12
Nodes (7): ctx(), cache(), channel(), graph(), Graph, test_a_bsuid_is_addressed_as_recipient(), TestVoiceNotes

### Community 209 - "milestone_for"
Cohesion: 0.33
Nodes (3): milestone_for(), _milestone_key(), TestMilestones

### Community 210 - "export_web_content.py"
Cohesion: 0.20
Nodes (8): build_meta(), export(), main(), _spans(), split_basmalah(), tajweed_doc(), uz_audio_doc(), _write()

### Community 211 - "WhatsAppError"
Cohesion: 0.29
Nodes (3): _error(), WhatsAppError, WindowClosed

### Community 213 - "BismillahBot — Multilingual Support Plan"
Cohesion: 0.14
Nodes (14): 10. File-by-file change list, 11. Memory & performance (free-tier reality), 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 2. Current-state audit (what is hardcoded English), 3. Target architecture, 4. User language preference (+6 more)

### Community 216 - "test_hifz_seam.py"
Cohesion: 0.20
Nodes (3): _isolate_registries(), _Settings, TestSchemaApplication

### Community 270 - "PostgresDailyStore"
Cohesion: 0.16
Nodes (3): DailyStore, DailySubRow, PostgresDailyStore

### Community 271 - "t"
Cohesion: 0.04
Nodes (32): 5. API surface (`/api/v1`), on_uz_audio(), parse(), page_audio(), sajda(), reciter(), sajda_keyboard(), uz_audio_row() (+24 more)

### Community 282 - "test_reciter_picker.py"
Cohesion: 0.12
Nodes (13): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, put_position(), ReaderPosition, Reciter (+5 more)

### Community 289 - "Separate quranayat-miniapp Next.js repo; API in this repo"
Cohesion: 0.12
Nodes (15): Inline query answering (all four representations, ranges), Navigation model ((surah, ayah, type) per chat_id), Page audio with stitched fallback, Page image stitching (lib/page_image.py), Repeat (memorization), Structural divisions (page / juz / sajda from quran-data.xml), Verse card (inline keyboard, edit in place), Uthmani text in Amiri Quran / KFGQPC font (+7 more)

### Community 294 - "test_store_contract.py"
Cohesion: 0.08
Nodes (5): TestDaily, TestReaderPosition, TestSenderIds, TestTajweedApprovals, TestTajweedProgress

### Community 295 - "SendCtx"
Cohesion: 0.51
Nodes (4): _due_rows(), TestWhatsApp, wa_tap(), wa_text()

### Community 317 - "domain/tajweed.py"
Cohesion: 0.19
Nodes (6): examples(), _load(), marked_html(), Rule, spans(), text()

### Community 332 - "test_export_web_content.py"
Cohesion: 0.21
Nodes (7): _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah(), test_meta_surahs_and_sajdas(), test_tafsir_has_every_ayah()

## Knowledge Gaps
- **51 isolated node(s):** `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres`, `Capacity results 5-1000 concurrent (no errors, 70-91 MB)`, `src/locales/en.py source of truth` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1875 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **124 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `Wizard` to `Store`, `weekly_board`, `lifespan.py`, `dispatch.py`, `streak_image.py`, `t`, `Context`, `bot/media.py`, `UserSettings`, `RedisSingleton`, `test_hifz_leaderboard.py`, `group.py`, `Hifz Progress Cmd Tests`, `services/plans.py`, `MemoryStore`, `TestDailyPost`, `test_hifz_streak.py`, `Acceptance Tests`, `stats.py`, `_ctx`, `SendCtx`, `Streaks`, `features/tajweed.py`, `Services`, `api/progress.py`, `deliver_quran`, `lang_hint`, `store/__init__.py`, `.test_full_flow_queues_the_first_send`, `summarize`, `InMemoryStore`, `.wa_user`, `handle_message`, `PostgresScheduleStore`, `session.py`, `SendCtx`, `WhatsApp`, `json`, `test_inline_reciter_search.py`, `_hifz`, `test_whatsapp_router.py`, `test_hifz_check.py`, `test_tajweed_audio.py`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_plan` be split into smaller, more focused modules?**
  _Cohesion score 0.053194333066025126 - nodes in this community are weakly interconnected._
- **Why does `Quran` connect `Quran` to `build_plan`, `lifespan.py`, `dispatch.py`, `Ref`, `parse_quran_tafsir`, `.get_next_ayah`, `Choice`, `t`, `bot/media.py`, `parse_reference`, `t`, `group.py`, `Hifz Progress Cmd Tests`, `services/plans.py`, `test_reciter_picker.py`, `html`, `TranslationRegistry`, `features/__init__.py`, `to_markup`, `test_miniapp_links.py`, `FakeChannel`, `asyncio`, `Phase 1 — Take `main.py` apart (pure moves) — *done*`, `ayah_for`, `features/check.py`, `api/progress.py`, `fixture`, `surah_progress`, `.page_range`, `summarize`, `test_export_web_content.py`, `quran_page_progress`, `_message`, `api/uz_audio.py`, `recall_check.py`, `BismillahBot — Business Logic`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Are the 44 inferred relationships involving `Ctx` (e.g. with `3. Architecture` and `4.1 Overlap with `MULTI_PLATFORM_PLAN.md``) actually correct?**
  _`Ctx` has 44 INFERRED edges - model-reasoned connections that need verification._
- **Should `Quran` be split into smaller, more focused modules?**
  _Cohesion score 0.05076679005817028 - nodes in this community are weakly interconnected._