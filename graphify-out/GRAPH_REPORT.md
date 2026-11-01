# Graph Report - QuranAyat_bot  (2026-11-02)

## Corpus Check
- 249 files · ~244,733 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 4721 nodes · 10872 edges · 282 communities (164 shown, 118 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1029 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `01fd3443`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_plan
- Quran
- summarize
- services/streaks.py
- Wizard
- _plan_setup.py
- _clip
- local_date
- to_whatsapp
- Leaderboard
- _ctx
- typing
- Store
- render_streak_graph
- t
- UserSettings
- Context
- Health
- Refs
- RedisSingleton
- typing
- WhatsAppChannel
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
- hifz_progress.py
- features/check.py
- to_markup
- Session
- Plans: PlanStore
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
- api/progress.py
- Inline Reciter Search Tests
- test_hifz_check.py
- PlanDaySpec
- juz_ref
- PostgresHifzStore
- SendCtx
- Dispatch Order Tests
- Choice
- Mini App Plan
- surah_progress
- juz_progress
- InMemoryIdentityStore
- get_store
- .exists
- test_hifz_progress.py
- reset_for_tests
- Hifz Seam Tests
- api/plans.py
- router.py
- parse_offset
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
- _hifz
- Profiles: ProfileRow
- test_channels_telegram.py
- Hifz Seam Tests: TestRegistration
- test_media_cache_keys.py
- Scheduler Tests: TestTransientFailuresAreRetried
- Store Contract Tests: TestPlans
- GraphClient
- TestStateStore
- command
- Refactor — Implementation Plan
- recall_check.py
- ._send_media
- auto_pace
- juz_ref
- test_hifz_streak.py
- pages.py
- stats.py
- send_page
- test_store_contract.py
- store/__init__.py
- Phase 2 — DRY the duplicated patterns
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- .get_next_ayah
- parse_ayah_range
- ._load_performers
- Testing & CI
- whatsapp_format.py
- streak.py
- InMemoryScheduleStore
- user_settings.py
- unittest_mock
- Blue Green Ci: jobs
- Blue Green Ci: with
- send_repeated_audio
- test_navigation.py
- _at
- Mini App Plan: Separate quranayatminiapp Nextjs
- ScheduledSend
- Channel
- range_audio
- json
- InMemoryGroupStore
- Store Contract Tests: TestLeaderboard
- _seed_legacy_lang
- Business Logic: The hifz platform memorization
- export
- TestRestartDeliversExactlyOnce
- callback
- get_language
- normalize_lang
- PostgresScheduleStore
- Hifz Seam Tests: test_hifz_seampy
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- test_miniapp_links.py
- reciter_set_confirmation
- Blue Green Ci: env
- test_channels_whatsapp.py
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
- domain/streaks.py
- Hifz Seam Tests: TestPrefixNamespace
- Hifz Seam Tests: TestDispatchCallback
- TestPickerFlow
- button_action
- Blue Green Ci: smokegreen
- TranslationRegistry
- whatsapp.py
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
- Choices
- _Ratio
- Hifz Seam Tests: test_longest_prefix_wins
- test_scheduler.py
- ayah_count
- InMemoryPlanStore
- test_webhook.py
- .send_text
- Claude
- load_summary
- Hifz Seam Tests: TestDispatchCommand
- .test_concatenates_the_ayahs_in_order
- offset_options
- percentile_band
- Hifz Group Tests: TestRegistration
- audio.py
- split
- fetch_and_stitch
- PageProgress
- week_bounds
- media_cache.py
- format_offset
- next_scheduled_date
- _callback
- test_whatsapp_config.py
- TestTheRest
- for_platform
- to_day_specs
- TestMedia
- .test_a_stale_button_does_not_mis_score_todays_question
- TestSevenTheCommandsExist
- TestCatalogOrder
- 4. User language preference
- _AnyDay
- _isolate_registries
- TestRegistration
- miniapp.py
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
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `Phase 3 — Hifz parity` --references--> `build_plan()`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/domain/plan_builder.py
- `Translation-only catalogue entries` --references--> `normalize_lang()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/locales/languages.py
- `Prioritized backlog` --references--> `parse_ayah()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/domain/parsing.py
- `The seam (`src/hifz/`)` --references--> `handle_update()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/bot/dispatch.py

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

## Communities (282 total, 118 thin omitted)

### Community 0 - "build_plan"
Cohesion: 0.13
Nodes (5): build_plan(), surah_ref(), TestConsolidationDays, TestDayOfWeekFiltering, TestPurity

### Community 1 - "Quran"
Cohesion: 0.08
Nodes (9): _consolidations(), Quran, _at_offset(), _span_length(), test_page_boundaries_match_the_bot(), TestDivisionsTileTheQuran, sweep_refs(), test_short_surahs_still_get_four_distinct_options() (+1 more)

### Community 2 - "summarize"
Cohesion: 0.12
Nodes (4): Progress, summarize(), SurahProgress, TestSummarize

### Community 3 - "services/streaks.py"
Cohesion: 0.14
Nodes (9): offset_of(), StreakCounts, refresh_streaks(), SessionOutcome, streak_summary(), StreakSummary, user_offset(), user_today() (+1 more)

### Community 4 - "Wizard"
Cohesion: 0.07
Nodes (9): ctx(), Wizard, test_draft_is_written_with_that_ttl(), TestAccumulation, TestCancel, TestCorruptState, TestLifecycle, TestOneDraftPerUser (+1 more)

### Community 5 - "_plan_setup.py"
Cohesion: 0.07
Nodes (46): Ctx, _begin_setup(), _is_group_admin(), _join_board(), on_group_tap(), setup_step(), _step_post_time(), _step_target() (+38 more)

### Community 6 - "_clip"
Cohesion: 0.11
Nodes (8): _clip(), _covered(), _intersect(), _page_share(), _pages_of(), clamp_to_quran(), contains(), TestContainsAndClamp

### Community 7 - "local_date"
Cohesion: 0.14
Nodes (8): _as_utc(), local_date(), local_now(), local_time(), next_due_utc(), TestLocalDate, TestNextDueUtc, _utc()

### Community 8 - "to_whatsapp"
Cohesion: 0.16
Nodes (3): to_whatsapp(), TestTags, TestWhatTheBotSends

### Community 9 - "Leaderboard"
Cohesion: 0.07
Nodes (16): user_week_window(), week_window(), weekly_board(), _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join() (+8 more)

### Community 10 - "_ctx"
Cohesion: 0.08
Nodes (17): _buttons(), _callback_data(), _CallbackQuery, _ctx(), _edited(), _isolate_registries(), _Message, _profile_row() (+9 more)

### Community 11 - "typing"
Cohesion: 0.04
Nodes (44): today(), offset_from_callback(), _plan_line(), profile_view(), reminder_keyboard(), telegram_username(), forgot_command(), on_progress_tap() (+36 more)

### Community 12 - "Store"
Cohesion: 0.09
Nodes (11): _CallbackQuery, _ctx(), _isolate_registries(), _Message, _run_wizard(), _Settings, _tap(), TestDrill (+3 more)

### Community 13 - "render_streak_graph"
Cohesion: 0.16
Nodes (6): render(), draw_contribution_graph(), render_streak_graph(), open_png(), TestRendering, TestRenderStreakGraph

### Community 14 - "t"
Cohesion: 0.04
Nodes (43): 5.2 Telegram message (bot), Phase 1 — Take `main.py` apart (pure moves) — *done*, _search_reciters(), _send_drill(), _translation_text(), _cancel_row(), _custom_days_keyboard(), _days_keyboard() (+35 more)

### Community 15 - "UserSettings"
Cohesion: 0.18
Nodes (5): UserSettings, TestDefaults, TestIndependence, TestKeyedByUserId, TestRoundTrip

### Community 16 - "Context"
Cohesion: 0.14
Nodes (15): _bot(), _ctx(), _isolate_registries(), _member(), _run_setup_to_plan(), _Settings, TestBoard, tap() (+7 more)

### Community 17 - "Health"
Cohesion: 0.06
Nodes (15): health(), store_backend(), database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries(), fresh_redis() (+7 more)

### Community 18 - "Refs"
Cohesion: 0.08
Nodes (9): _clean(), parse_range(), parse_reference(), TestSurahSpans, TestAcrossSurahs, TestFormatting, TestRejection, TestWholeSurah (+1 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.10
Nodes (10): 6. Issues fixed in this refactor, _key(), pick(), remember(), get(), expect(), _key(), take() (+2 more)

### Community 20 - "typing"
Cohesion: 0.07
Nodes (14): 3. Principles applied, create_app(), _commands_for(), initialize(), lifespan(), _set_bot_commands(), AppState, spawn() (+6 more)

### Community 21 - "WhatsAppChannel"
Cohesion: 0.21
Nodes (4): _clip(), _resolve(), _split_choices(), WhatsAppChannel

### Community 22 - "IdentityStore"
Cohesion: 0.07
Nodes (4): IdentityRow, IdentityStore, PostgresIdentityStore, _stored()

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "Group"
Cohesion: 0.08
Nodes (21): bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), _enqueue_next_board(), _enqueue_next_group(), group_board_entries() (+13 more)

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.11
Nodes (18): 10. Found along the way (out of scope — behaviour changes), 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, 2. Goals and non-goals, 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, 6. Ordering, risk, size, 7. Safety net (+10 more)

### Community 26 - "TelegramChannel"
Cohesion: 0.12
Nodes (5): TelegramChannel, TestAnswerAndTyping, TestEditChoices, TestEditText, TestSendText

### Community 27 - "Hifz Streak Tests"
Cohesion: 0.24
Nodes (5): _caption(), _earn(), _streak(), TestMilestones, TestStreakCard

### Community 28 - "Hifz Platform"
Cohesion: 0.09
Nodes (20): Hifz Platform - Plan & Progress, Phase 1 acceptance criteria (tests/test_acceptance.py), Hifz change log, claim_due claimed_at clock bug, Hifz data model (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send, group_*), Phase 2 group cluster (J1-J6, forum topics), Workstream I: i18n & commands for 48 locales, Workstream C: interval merge-on-insert + derived percentages (+12 more)

### Community 29 - "Acceptance Tests"
Cohesion: 0.11
Nodes (13): _CallbackQuery, _cmd(), _ctx(), _isolate_registries(), _Message, _run_wizard(), _save_plan(), _Settings (+5 more)

### Community 30 - "get_settings"
Cohesion: 0.07
Nodes (18): answer_inline_query(), inline_audio_result(), inline_photo_results(), combined_audio_key(), source(), range_audio_url(), ref_key(), _flag() (+10 more)

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 32 - "test_page_mode.py"
Cohesion: 0.24
Nodes (4): data(), fake_bot(), TestStitchedAudioAcrossSurahs, tg_bot()

### Community 33 - "test_recall_check.py"
Cohesion: 0.03
Nodes (30): _nfc(), swept(), test_a_different_date_gives_a_different_question(), test_both_question_modes_show_up_in_the_sweep(), test_correct_option_is_never_a_length_outlier(), test_correct_option_is_never_the_extreme_by_a_wide_ratio(), test_correct_option_really_follows_the_prompt(), test_dates_and_iso_strings_are_interchangeable() (+22 more)

### Community 34 - ".get"
Cohesion: 0.08
Nodes (6): get_default_query_results(), TestCorpusIntegrity, TestAvailable, TestCaching, TestFallback, TestTransliteration

### Community 35 - "services/check.py"
Cohesion: 0.15
Nodes (7): pick_ayah(), preload_corpus(), ask(), default_span(), rebuild(), Score, score()

### Community 36 - "File"
Cohesion: 0.09
Nodes (7): stitch(), page_image_url(), File, TestAudioFilename, TestImageFilename, TestLegacyLanguageKey, TestCoexistsWithTheReciterFlow

### Community 37 - "Recitation Checker Investigation"
Cohesion: 0.07
Nodes (28): 0.1 Decision (2026-10-27), 0. Bottom line up front, 10. Phased roadmap, 11.1 Relevant Koyeb prices, 11.2 Assumptions, 11.3 Capacity by scenario, 11.4 Monthly cost, 11.5 Cost guards (+20 more)

### Community 38 - "hifz_progress.py"
Cohesion: 0.13
Nodes (6): _focus_surah(), format_percent(), _recency_key(), round_percent(), _surah_of(), TestRounding

### Community 39 - "features/check.py"
Cohesion: 0.23
Nodes (6): _ask(), check(), on_check(), _parse_answer(), _question_text(), _score()

### Community 40 - "to_markup"
Cohesion: 0.16
Nodes (7): verse_keyboard(), mode_button(), to_button(), to_markup(), TestToMarkup, _button(), TestVerseKeyboard

### Community 41 - "Session"
Cohesion: 0.13
Nodes (21): init_data_max_age(), auth_telegram(), AuthOut, me(), _me(), MeOut, patch_profile(), patch_settings() (+13 more)

### Community 42 - "Plans: PlanStore"
Cohesion: 0.07
Nodes (4): PlanDayRow, PlanRow, PlanStore, PostgresPlanStore

### Community 43 - "quran_page_progress"
Cohesion: 0.11
Nodes (4): juz_page_progress(), quran_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 45 - "Streaks"
Cohesion: 0.13
Nodes (4): record_session(), TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 46 - "Load Test"
Cohesion: 0.14
Nodes (13): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+5 more)

### Community 47 - "Multilingual Plan"
Cohesion: 0.17
Nodes (13): Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), Quran.from_file(path) refactor, setMyCommands per language, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+5 more)

### Community 48 - "Text"
Cohesion: 0.20
Nodes (7): reference(), _inline_query(), _of_type(), _results(), TestInlineArabicImage, TestRangeAudio, TestRangeText

### Community 49 - "Schema"
Cohesion: 0.11
Nodes (26): group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval, hifz_interval_user_surah_idx (+18 more)

### Community 50 - "Services"
Cohesion: 0.14
Nodes (19): _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today(), test_me_carries_plan_and_streak() (+11 more)

### Community 51 - "auth.py"
Cohesion: 0.06
Nodes (29): _b64url_decode(), jwt_secret(), require_user(), _unauthorized(), get_position(), _lang(), LanguageOut, languages() (+21 more)

### Community 52 - "Dispatch"
Cohesion: 0.16
Nodes (18): _callback(), data(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index(), test_inline_query_valid_ayah_returns_all_four_views() (+10 more)

### Community 53 - "reciter_keyboard"
Cohesion: 0.16
Nodes (6): reciter_keyboard(), reciter_label(), reciter_page_count(), _pager_row(), TestLabels, TestPagination

### Community 54 - "api/progress.py"
Cohesion: 0.18
Nodes (16): not_found(), forget(), ForgetIn, ForgetOut, _juz(), JuzRatio, progress(), ProgressOut (+8 more)

### Community 55 - "Inline Reciter Search Tests"
Cohesion: 0.15
Nodes (20): handle_update(), _audio_result(), data(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter(), test_ayah_audio_dropped_without_public_base_url() (+12 more)

### Community 56 - "test_hifz_check.py"
Cohesion: 0.15
Nodes (12): _answer_data(), _ask(), _asked(), _buttons(), _callback_query(), _ctx(), _sessions(), _Settings (+4 more)

### Community 58 - "juz_ref"
Cohesion: 0.11
Nodes (6): advancing(), assert_covers_target_once(), assert_well_formed(), spans(), TestAlMulkAcceptance, TestSmallAndAwkwardTargets

### Community 59 - "PostgresHifzStore"
Cohesion: 0.07
Nodes (9): _covers(), InMemoryHifzStore, _merge_span(), _normalize(), _overlaps(), PostgresHifzStore, _split_span(), _touches() (+1 more)

### Community 60 - "SendCtx"
Cohesion: 0.12
Nodes (5): register_send_handler(), registered_kinds(), _same_origin(), decorate(), SendCtx

### Community 61 - "Dispatch Order Tests"
Cohesion: 0.18
Nodes (17): _callback(), data(), fake_bot(), _message(), probe(), _sent_a_verse(), test_a_command_beats_a_pending_reciter_search(), test_a_command_escapes_a_wizard_without_ending_it() (+9 more)

### Community 62 - "Choice"
Cohesion: 0.19
Nodes (4): Choice, taps(), TestChoices, TestMedia

### Community 63 - "Mini App Plan"
Cohesion: 0.14
Nodes (14): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 6. Frontend structure (`quranayat-miniapp`), 7. Bot ↔ Mini App integration (+6 more)

### Community 65 - "surah_progress"
Cohesion: 0.14
Nodes (4): started_surahs(), surah_progress(), TestSpecAcceptance, TestSurahProgress

### Community 66 - "juz_progress"
Cohesion: 0.16
Nodes (5): juz_progress(), JuzProgress, _spans(), started_juzs(), TestJuzProgress

### Community 67 - "InMemoryIdentityStore"
Cohesion: 0.11
Nodes (3): InMemoryIdentityStore, InMemoryStore, Store

### Community 68 - "get_store"
Cohesion: 0.16
Nodes (6): get_store(), _lock(), TestFourProgress, _added_update(), TestAdded, TestDailyPost

### Community 69 - ".exists"
Cohesion: 0.10
Nodes (7): TestEveryParsedRefIsReal, TestExists, TestRandom, TestStructure, TestSurahMeta, test_pick_ayah_handles_a_cross_surah_span(), test_the_whole_quran_is_a_valid_span()

### Community 70 - "test_hifz_progress.py"
Cohesion: 0.13
Nodes (4): quran_progress(), _at(), TestInputHandling, TestQuranProgress

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 73 - "api/plans.py"
Cohesion: 0.14
Nodes (19): active(), _build(), complete(), create(), DrillOut, lifecycle(), _plan_out(), PlanCreateIn (+11 more)

### Community 74 - "router.py"
Cohesion: 0.08
Nodes (20): Phase 3 — One router for everything — *done*, handle_incoming(), _incoming(), _on_callback(), _on_text(), decorate(), command(), decorate() (+12 more)

### Community 75 - "parse_offset"
Cohesion: 0.15
Nodes (3): parse_offset(), TestParseOffset, TestPicker

### Community 76 - "tick.py"
Cohesion: 0.13
Nodes (12): catch_up(), run_scheduler(), _wait(), _deliver(), _is_stale(), _lock(), _release(), _resolve() (+4 more)

### Community 78 - "Bundle Translations"
Cohesion: 0.22
Nodes (7): bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.11
Nodes (19): Audio catalog kinds, Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES), Mini App feature parity map, Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points), Error taxonomy L1-L5 (word, harakah, tajwid, riwayah mismatch, waqf) (+11 more)

### Community 80 - "BismillahBot — Business Logic"
Cohesion: 0.10
Nodes (15): 1. Overview, 2. Architecture, 3. Request lifecycle, 5. Caching strategy, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic, Local time (+7 more)

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
Cohesion: 0.08
Nodes (19): _clean_state_store(), export(), languages(), main(), resolved_table(), _write(), setup_logging(), _absolute_imports() (+11 more)

### Community 86 - "build_grid"
Cohesion: 0.16
Nodes (5): build_grid(), _counts(), Grid, _semaphore(), TestGrid

### Community 87 - "Portion"
Cohesion: 0.18
Nodes (5): Portion, match_portion(), portion_for(), portions_of(), TestPortionShape

### Community 89 - "auth.py"
Cohesion: 0.09
Nodes (33): _b64url(), decode_token(), _init_data_secret(), InvalidInitData, InvalidToken, issue_token(), _sign(), sign_init_data() (+25 more)

### Community 90 - "Store Contract Tests"
Cohesion: 0.11
Nodes (3): _spans(), TestHifzIntervalEdges, TestHifzIntervals

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.08
Nodes (24): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+16 more)

### Community 92 - "text.py"
Cohesion: 0.18
Nodes (5): data(), fake_bot(), TestLanguageFlags, TestVerseText, tg_bot()

### Community 93 - "_hifz"
Cohesion: 0.06
Nodes (11): HifzInterval, _assert_invariant(), _ayahs(), _hifz(), _spans(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order() (+3 more)

### Community 94 - "Profiles: ProfileRow"
Cohesion: 0.05
Nodes (3): PostgresProfileStore, ProfileRow, ProfileStore

### Community 95 - "test_channels_telegram.py"
Cohesion: 0.25
Nodes (3): bot(), cache(), TestChoice

### Community 97 - "test_media_cache_keys.py"
Cohesion: 0.15
Nodes (8): _bot(), _next_id(), send_audio(), send_photo(), no_cdn(), _source(), test_a_miss_caches_under_the_key_and_a_hit_replays_it(), test_a_rejected_cached_id_is_rebuilt_and_recached()

### Community 101 - "TestStateStore"
Cohesion: 0.15
Nodes (3): 11.1 Profile settings reset after a while — `fix/settings-persistence`, DatabaseUnavailable, TestStateStore

### Community 102 - "command"
Cohesion: 0.18
Nodes (11): command, Routing rules (in `serve`), about(), app(), help_(), index(), start(), _welcome() (+3 more)

### Community 103 - "Refactor — Implementation Plan"
Cohesion: 0.22
Nodes (8): tests/test_layering.py ratchet (KNOWN violations), Overlap with MULTI_PLATFORM_PLAN channel seam, Decisions and open questions (§9), Phase 0 — Guardrails (ruff, layering test, logging), Phase 5 — Fix the layering, Target layout (app/ bot/ services/ domain/ infra/), Timezone picker by country (feat/timezone-by-country), Memorizing (hifz): /memorize, /check, /progress, /streak, /leaderboard, /profile

### Community 104 - "recall_check.py"
Cohesion: 0.06
Nodes (27): _assemble(), _ayah_text(), _basmala_prefix(), build_question(), _clean(), _continuation_question(), corpus(), _date_key() (+19 more)

### Community 105 - "._send_media"
Cohesion: 0.22
Nodes (4): _build(), _send(), send_cached(), build()

### Community 106 - "auto_pace"
Cohesion: 0.16
Nodes (3): auto_pace(), TestAcrossTheWholeQuran, TestAutoPace

### Community 107 - "juz_ref"
Cohesion: 0.18
Nodes (4): juz_ref(), page_ref(), TestJuzAndPage, TestCrossSurahTargets

### Community 108 - "test_hifz_streak.py"
Cohesion: 0.18
Nodes (6): _ctx(), _isolate_registries(), _photo_message(), _Settings, TestCallback, TestWhatTicksADay

### Community 109 - "pages.py"
Cohesion: 0.11
Nodes (13): juz(), page(), sajda(), turn_page(), reader_position(), button_rows(), sajda_keyboard(), deliver_page() (+5 more)

### Community 110 - "stats.py"
Cohesion: 0.35
Nodes (8): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut

### Community 111 - "send_page"
Cohesion: 0.29
Nodes (7): send_page(), _buffer(), _stub_stitch(), stub(), TestPageCard, capture(), counting()

### Community 112 - "test_store_contract.py"
Cohesion: 0.04
Nodes (5): TestIdentity, TestProfiles, TestReaderPosition, TestSchedule, TestSettings

### Community 113 - "store/__init__.py"
Cohesion: 0.12
Nodes (3): HifzStore, ScheduleStore, MemoryState

### Community 114 - "Phase 2 — DRY the duplicated patterns"
Cohesion: 0.14
Nodes (11): graphify knowledge graph (graphify-out/), CLAUDE.md graphify lookup rules, button_rows() row-packing helper, Copy-pasted patterns table (§1.3), ignore_not_modified() context manager, Shared UTC offset picker (time_pickers.offset_keyboard), Found along the way (out-of-scope behaviour changes), Phase 2 — DRY the duplicated patterns (+3 more)

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

### Community 119 - "parse_ayah_range"
Cohesion: 0.23
Nodes (3): parse_ayah_range(), TestCommandArguments, TestParseAyahRange

### Community 120 - "._load_performers"
Cohesion: 0.15
Nodes (6): 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 4 — Split infrastructure god-objects — *done*, Phase 6 — Repository hygiene — *done*, performers(), TestCatalogKinds

### Community 121 - "Testing & CI"
Cohesion: 0.18
Nodes (14): Documentation index (docs/README.md), ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable, GET / health with store and cache status (503), Silent in-memory store fallback, Phase 6 — Repository hygiene, Profile settings reset fix (fix/settings-persistence), Typed frozen Settings (config/settings.py), Blue-Green CI pipeline (blue-green-ci.yml) (+6 more)

### Community 122 - "whatsapp_format.py"
Cohesion: 0.20
Nodes (3): _Converter, _render(), _wrap()

### Community 123 - "streak.py"
Cohesion: 0.15
Nodes (6): _caption(), _keyboard(), on_streak(), _send_graph(), streak(), offset_keyboard()

### Community 125 - "user_settings.py"
Cohesion: 0.14
Nodes (4): resolve_settings(), UserSettingsRow, _legacy_lang_key(), SettingsRow

### Community 126 - "unittest_mock"
Cohesion: 0.13
Nodes (6): _stress_reset(), _stress_stats(), data(), fake_bot(), public_url(), tg_bot()

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

### Community 133 - "ScheduledSend"
Cohesion: 0.12
Nodes (4): enqueue(), idempotency_key(), schedule_daily(), ScheduledSend

### Community 136 - "json"
Cohesion: 0.08
Nodes (17): build(), main_(), _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl(), _count(), _load(), test_arabic_has_every_ayah() (+9 more)

### Community 137 - "InMemoryGroupStore"
Cohesion: 0.06
Nodes (6): GroupConfig, GroupMemberLink, GroupPlanDayRow, GroupPlanRow, GroupStore, InMemoryGroupStore

### Community 139 - "_seed_legacy_lang"
Cohesion: 0.20
Nodes (3): _seed_legacy_lang(), TestInlineCaller, TestLegacyMigration

### Community 140 - "Business Logic: The hifz platform memorization"
Cohesion: 0.22
Nodes (7): Central callback prefix allocation (hifz.PREFIXES), The hifz platform (memorization companion), Pure plan builder (build_plan), Streak day ticks on completed session, Bot ↔ Mini App integration (menu button, startapp, /app), recitation_job table and user_profile.riwayah, /recite flow (voice note → recitation_job → report)

### Community 141 - "export"
Cohesion: 0.18
Nodes (7): build_meta(), export(), main(), _spans(), split_basmalah(), _write(), parse_quran_tafsir()

### Community 143 - "callback"
Cohesion: 0.09
Nodes (21): 5. API surface (`/api/v1`), Phase 2 — WhatsApp MVP (reader + daily ayat), 7. The keyboard & command localization challenge, Telegram command menu, 1. Why, Phase 2 — DRY the duplicated patterns — *done*, _board_message(), leaderboard() (+13 more)

### Community 144 - "get_language"
Cohesion: 0.23
Nodes (5): get_language(), is_supported(), is_ui_language(), Language, TestLanguageLookup

### Community 145 - "normalize_lang"
Cohesion: 0.22
Nodes (6): 4.1 Flow, 4.2 Rules, 4.3 Transport, 4. Authentication, normalize_lang(), TestNormalizeLang

### Community 146 - "PostgresScheduleStore"
Cohesion: 0.13
Nodes (3): PostgresStore, PostgresScheduleStore, store()

### Community 148 - "Hifz Seam Tests: test_hifz_seampy"
Cohesion: 0.18
Nodes (3): _isolate_registries(), _Settings, TestSchemaApplication

### Community 152 - "test_miniapp_links.py"
Cohesion: 0.20
Nodes (11): _app_command(), app_on(), data(), test_app_command(), test_app_command_without_url(), test_cards_and_drill_link_to_their_screens(), test_inline_messages_never_get_a_web_app_button(), test_menu_button() (+3 more)

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 155 - "test_channels_whatsapp.py"
Cohesion: 0.20
Nodes (4): cache(), channel(), graph(), Graph

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

### Community 166 - "domain/streaks.py"
Cohesion: 0.23
Nodes (4): Milestone, milestone_for(), _milestone_key(), TestMilestones

### Community 169 - "TestPickerFlow"
Cohesion: 0.13
Nodes (9): _callback(), data(), fake_bot(), _message(), _reciter_buttons(), _tab_row(), TestAudioNeverFollowsLanguage, TestPickerFlow (+1 more)

### Community 170 - "button_action"
Cohesion: 0.10
Nodes (6): button_action(), missing_keys(), _placeholders(), TestButtonAction, TestGroupLocaleExemption, TestLocaleIntegrity

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 172 - "TranslationRegistry"
Cohesion: 0.09
Nodes (18): 7. Known limitations / tech debt, 10. File-by-file change list, 11. Memory & performance (free-tier reality), 12. Testing, 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 2. Current-state audit (what is hardcoded English) (+10 more)

### Community 173 - "whatsapp.py"
Cohesion: 0.20
Nodes (4): _bytes_and_name(), _error(), WhatsAppError, WindowClosed

### Community 176 - "BUSINESS_LOGIC.md"
Cohesion: 0.25
Nodes (5): Four ayah representations (english, tafsir, arabic, audio), Future roadmap and prioritized backlog, Known limitations / tech debt, Issues fixed in the refactor (12 bugs), Verse card (inline keyboard, edit in place)

### Community 178 - "BismillahBot README"
Cohesion: 0.15
Nodes (11): Translation Attributions, alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Documentation, Locale review tracking table (47 locales), BismillahBot README (+3 more)

### Community 179 - "8. Phased task breakdown"
Cohesion: 0.29
Nodes (7): 8. Phased task breakdown, Phase 0 — Foundations, Phase 1 — Service-layer extraction (this repo, no UI change), Phase 2 — Reader parity (read-only, low risk, ships first), Phase 3 — Hifz parity, Phase 4 — Recitation checker UI (depends on the investigation's Phase A), Phase 5 — Later

### Community 181 - "cache_key"
Cohesion: 0.25
Nodes (3): cache_key(), TestGraphCache, TestCacheKey

### Community 182 - "Blue Green Ci: deploygreen"
Cohesion: 0.33
Nodes (6): environment, if, name, needs, runs-on, deploy-green

### Community 183 - "Blue Green Ci: promote"
Cohesion: 0.33
Nodes (6): promote, environment, if, name, needs, runs-on

### Community 187 - "test_scheduler.py"
Cohesion: 0.32
Nodes (3): _isolate_handlers(), state(), store()

### Community 190 - "test_webhook.py"
Cohesion: 0.20
Nodes (3): webhook_secret(), test_the_secret_does_not_reveal_the_token(), test_webhook_acks_before_initialization()

### Community 193 - "load_summary"
Cohesion: 0.24
Nodes (3): ProgressSummary, load_summary(), TestLoadSummary

### Community 196 - ".test_concatenates_the_ayahs_in_order"
Cohesion: 0.18
Nodes (4): content(), fake_download(), TestStitching, __init__()

### Community 197 - "offset_options"
Cohesion: 0.33
Nodes (7): offset_options(), _grid(), test_a_label_prefix_changes_only_the_label(), test_cancel_data_adds_a_localized_cancel_row(), test_every_offset_is_offered_in_order_under_the_callers_prefix(), test_no_cancel_row_unless_asked(), test_rows_are_columns_wide()

### Community 200 - "audio.py"
Cohesion: 0.28
Nodes (3): stitch(), download_combined_audio(), download_stitched_audio()

### Community 205 - "fetch_and_stitch"
Cohesion: 0.25
Nodes (4): fetch_and_stitch(), _fit_for_telegram(), _semaphore(), stitch_images()

### Community 208 - "media_cache.py"
Cohesion: 0.28
Nodes (3): get(), _key(), save()

### Community 210 - "next_scheduled_date"
Cohesion: 0.29
Nodes (3): _advance(), next_scheduled_date(), _validated_days()

### Community 212 - "test_whatsapp_config.py"
Cohesion: 0.36
Nodes (5): env(), test_any_missing_value_keeps_it_off(), test_off_by_default(), test_on_when_fully_configured(), test_the_flag_must_be_truthy()

### Community 269 - "4. User language preference"
Cohesion: 0.67
Nodes (3): 4. User language preference, Detection & selection flow, Storage

### Community 284 - "miniapp.py"
Cohesion: 0.21
Nodes (6): Phase 5 — Fix the layering — *done*, app_button(), app_choice_row(), app_row(), app_url(), set_menu_button()

### Community 289 - "reciter.py"
Cohesion: 0.19
Nodes (5): reciter_page_of(), reciter_catalog(), reciter_group(), reciter_kind(), TestCurrentReciter

## Knowledge Gaps
- **51 isolated node(s):** `button_rows() row-packing helper`, `ignore_not_modified() context manager`, `Found along the way (out-of-scope behaviour changes)`, `Phase 0 — Guardrails (ruff, layering test, logging)`, `ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1613 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **118 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `get_store` to `summarize`, `services/streaks.py`, `Leaderboard`, `_ctx`, `typing`, `Store`, `render_streak_graph`, `t`, `UserSettings`, `Context`, `PostgresScheduleStore`, `RedisSingleton`, `typing`, `Hifz Progress Cmd Tests`, `Hifz Streak Tests`, `Acceptance Tests`, `get_settings`, `Session`, `Streaks`, `Services`, `auth.py`, `api/progress.py`, `Inline Reciter Search Tests`, `test_hifz_check.py`, `load_summary`, `surah_progress`, `InMemoryIdentityStore`, `test_hifz_progress.py`, `api/plans.py`, `router.py`, `tick.py`, `build_grid`, `_hifz`, `TestStateStore`, `stats.py`, `store/__init__.py`, `user_settings.py`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `button_rows() row-packing helper`, `ignore_not_modified() context manager`, `Found along the way (out-of-scope behaviour changes)` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_plan` be split into smaller, more focused modules?**
  _Cohesion score 0.13306451612903225 - nodes in this community are weakly interconnected._
- **Why does `Quran` connect `Quran` to `build_plan`, `summarize`, `test_navigation.py`, `_clip`, `range_audio`, `json`, `typing`, `export`, `t`, `Refs`, `typing`, `Hifz Progress Cmd Tests`, `get_settings`, `.get`, `services/check.py`, `hifz_progress.py`, `features/check.py`, `quran_page_progress`, `TranslationRegistry`, `auth.py`, `api/progress.py`, `juz_ref`, `ayah_count`, `surah_progress`, `juz_progress`, `.exists`, `test_hifz_progress.py`, `BismillahBot — Business Logic`, `to_day_specs`, `recall_check.py`, `auto_pace`, `juz_ref`, `pages.py`, `.get_next_ayah`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Ctx` (e.g. with `3. Architecture` and `4.1 Overlap with `MULTI_PLATFORM_PLAN.md``) actually correct?**
  _`Ctx` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Should `Quran` be split into smaller, more focused modules?**
  _Cohesion score 0.07505285412262157 - nodes in this community are weakly interconnected._