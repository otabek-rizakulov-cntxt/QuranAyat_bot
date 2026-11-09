# Graph Report - QuranAyat_bot  (2026-11-09)

## Corpus Check
- 304 files · ~290,825 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 7, .example 1, .ini 1)

## Summary
- 5487 nodes · 13258 edges · 315 communities (173 shown, 142 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1233 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e56e7ba1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_plan
- link_token.py
- Quran
- SendCtx
- .start
- routes/whatsapp.py
- export.py
- Ctx
- to_whatsapp
- dispatch.py
- Ref
- InMemoryScheduleStore
- Wizard
- build_grid
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
- features/profile.py
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
- 1. Why
- Schema
- Services
- test_tajweed_lessons.py
- services/check.py
- api/progress.py
- api/check.py
- GroupStore
- reader.py
- whatsapp_setup.py
- os
- store/__init__.py
- surah_progress
- test_reciter_picker.py
- .test_full_flow_queues_the_first_send
- Mini App Plan
- localtime.py
- info.py
- IdentityStore
- summarize
- require_user
- .reply
- surah_progress
- parse_ayah_range
- Hifz Seam Tests
- session.py
- handle_update
- whatsapp_format.py
- SendCtx
- quran_page_progress
- bundle_translations.py
- Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd
- pytest
- ._send_media
- Groups: PostgresGroupStore
- InMemorySessionStore
- Scheduler Tests
- .get
- PostgresProfileStore
- send_surah
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
- TestDaily
- Wizard
- InMemoryIdentityStore
- asyncio
- BismillahBot — Business Logic
- TestTransliteration
- TestSchedule
- offset_keyboard
- fixture
- Koyeb Capacity Report
- Blue Green Ci
- Blue Green Ci: name
- PostgresScheduleStore
- InMemoryGroupStore
- PostgresIdentityStore
- test_store_selection.py
- compute_streak
- Hifz platform frozen string manifest
- _align
- button_rows
- InMemoryStore
- Blue Green Ci: jobs
- Blue Green Ci: with
- Portion
- test_hifz_intervals.py
- time
- answer_inline_query
- TestPlans
- Channel
- TestPickerFlow
- reciter_keyboard
- test_media_cache_keys.py
- Tajweed (tajvid) section: plan
- .get_surah_length
- MINI_APP_PLAN.md
- Phase 2 — DRY the duplicated patterns
- TestRestartDeliversExactlyOnce
- parse_ayah
- weekly_board
- PostgresHifzStore
- keyboards/menu.py
- TestLeaderboard
- test_page_mode.py
- Hifz Seam Tests: TestConflictFreeByConstruction
- Scheduler Tests: TestRegistry
- Scheduler Tests: TestTheLoopSurvivesABadRow
- reciter_kind
- 11.1 Profile settings reset after a while — `fix/settings-persistence`
- Blue Green Ci: env
- test_channels_whatsapp.py
- TestProfiles
- graphify-autopush.sh
- test_settings.py
- Dependency rule (app -> bot -> services -> domain)
- account_link.py
- reciter_label
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
- send_repeated_audio
- test_uz_audio_timings.py
- test_tajweed_data.py
- _ayah_text
- BismillahBot README
- test_keyboard_snapshots.py
- split
- Graph
- Blue Green Ci: deploygreen
- Blue Green Ci: promote
- Phase 1 — Take `main.py` apart (pure moves) — *done*
- lang_hint
- Hifz Seam Tests: test_longest_prefix_wins
- TestStateStore
- 6. Phased task breakdown
- next_scheduled_date
- .search_performers
- TestIdentity
- Claude
- ._send_choices
- Hifz Seam Tests: TestDispatchCommand
- _callback
- .wa_user
- handle_message
- GroupPlanDayRow
- Graph
- Identity table (platform, external_id → user_id)
- .test_sends_todays_ayah_and_queues_tomorrow
- exchange
- WhatsAppChannel
- TestSessions
- milestone_for
- export_web_content.py
- version
- features/check.py
- BismillahBot — Multilingual Support Plan
- Telegram
- reset_for_tests
- test_hifz_seam.py
- _patch_client
- TestSettings
- TestSevenTheCommandsExist
- PostgresStore
- locales/__init__.py
- test_the_basmala_heading_is_not_part_of_the_question
- sweep_refs
- TestReaderPosition
- TestRunScheduler
- .has_page_audio
- test_pick_ayah_accepts_anything_with_as_tuple
- get_store
- get_settings
- test_the_answer_is_not_findable_by_sorting_on_length
- test_sweep_produces_a_well_formed_question_everywhere
- test_options_are_distinct_even_ignoring_vowelling
- test_prompt_is_never_offered_back_as_an_option
- test_correct_option_really_follows_the_prompt
- Separate quranayat-miniapp Next.js repo; API in this repo
- test_both_question_modes_show_up_in_the_sweep
- test_next_ayah_mode_answers_with_the_whole_short_ayah
- test_long_ayah_prompt_and_options_stay_button_sized
- test_next_ayah_prompt_is_truncated_and_says_so
- TestSenderIds
- SendCtx
- test_every_option_carries_the_same_word_count
- test_same_inputs_give_the_same_question
- test_a_different_date_gives_a_different_question
- test_dates_and_iso_strings_are_interchangeable
- test_the_global_random_module_is_never_touched
- test_the_answer_does_not_always_land_in_the_same_slot
- test_the_first_and_last_ayah_of_the_quran
- test_muqattaat_get_muqattaat_shaped_distractors
- test_no_option_carries_a_reference_suffix_or_a_bom
- test_options_need_no_html_escaping_beyond_the_callers
- test_pick_then_build_is_the_whole_check_flow
- test_preload_corpus_returns_the_same_cached_object
- test_correct_option_is_never_a_length_outlier
- test_correct_option_is_never_the_extreme_by_a_wide_ratio
- TestRegistration
- tajweed_lessons.py
- test_export_web_content.py
- WhatsApp

## God Nodes (most connected - your core abstractions)
1. `get_store()` - 174 edges
2. `Ctx` - 164 edges
3. `t()` - 150 edges
4. `Quran` - 146 edges
5. `handle_update()` - 103 edges
6. `fixture()` - 89 edges
7. `UserSettings` - 84 edges
8. `Choice` - 75 edges
9. `build_plan()` - 72 edges
10. `File` - 64 edges

## Surprising Connections (you probably didn't know these)
- `2. Current-state audit (what is hardcoded English)` --references--> `build_data()`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/app/lifespan.py
- `3. Architecture` --references--> `Ctx`  [INFERRED]
  docs/MINI_APP_PLAN.md → src/bot/context.py
- `The seam (`src/hifz/`)` --references--> `handle_update()`  [INFERRED]
  docs/BUSINESS_LOGIC.md → src/bot/dispatch.py
- `Detection & selection flow` --references--> `handle_update()`  [INFERRED]
  docs/MULTILINGUAL_PLAN.md → src/bot/dispatch.py
- `2. Goals and non-goals` --references--> `handle_update()`  [INFERRED]
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

## Communities (315 total, 142 thin omitted)

### Community 0 - "build_plan"
Cohesion: 0.05
Nodes (17): advancing(), build_plan(), juz_ref(), surah_ref(), to_day_specs(), assert_covers_target_once(), assert_well_formed(), spans() (+9 more)

### Community 1 - "link_token.py"
Cohesion: 0.17
Nodes (9): _b64url_decode(), _b64(), InvalidLinkToken, issue(), _key(), redeem(), _secret(), _unb64() (+1 more)

### Community 2 - "Quran"
Cohesion: 0.05
Nodes (19): 4. Navigation model, Page images and page audio, Structural divisions (page / juz / sajda), Translation-only catalogue entries, deliver_page_audio(), source(), stitch(), page_caption() (+11 more)

### Community 3 - "SendCtx"
Cohesion: 0.06
Nodes (26): ctx(), push_daily(), session(), _consented(), push_plan_day(), ayah_for(), _send_plain_message(), deliver_push() (+18 more)

### Community 5 - "routes/whatsapp.py"
Cohesion: 0.05
Nodes (23): _stress_reset(), _stress_stats(), _commands_for(), initialize(), lifespan(), _set_bot_commands(), _process_update(), telegram_webhook() (+15 more)

### Community 6 - "export.py"
Cohesion: 0.10
Nodes (19): main(), strip_notes(), decode_16k(), load_reference(), mp3_path(), Mp3Info, probe(), to_float() (+11 more)

### Community 7 - "Ctx"
Cohesion: 0.11
Nodes (22): 4.1 Overlap with `MULTI_PLATFORM_PLAN.md`, 4. Target layout and layering, Ctx, _board_message(), leaderboard(), on_leaderboard(), _caption(), _keyboard() (+14 more)

### Community 8 - "to_whatsapp"
Cohesion: 0.19
Nodes (3): to_whatsapp(), TestTags, TestWhatTheBotSends

### Community 9 - "dispatch.py"
Cohesion: 0.06
Nodes (15): handle_incoming(), _incoming(), resolve_settings(), Caps, Incoming, data(), TestCodes, bot() (+7 more)

### Community 10 - "Ref"
Cohesion: 0.08
Nodes (17): _clip(), _covered(), _focus_surah(), _intersect(), _page_share(), _pages_of(), quran_page_progress(), _recency_key() (+9 more)

### Community 12 - "Wizard"
Cohesion: 0.08
Nodes (12): _CallbackQuery, _ctx(), _isolate_registries(), _Message, _run_wizard(), _Settings, _tap(), TestDrill (+4 more)

### Community 13 - "build_grid"
Cohesion: 0.07
Nodes (13): render(), build_grid(), _counts(), draw_contribution_graph(), Grid, level_for(), render_streak_graph(), _semaphore() (+5 more)

### Community 14 - "Choice"
Cohesion: 0.10
Nodes (29): on_group_tap(), memorize(), on_tap(), plan_step(), _expired(), _ref_to_draft(), _know_by_heart(), _start_drill() (+21 more)

### Community 15 - "UserSettings"
Cohesion: 0.06
Nodes (12): InMemoryProfileStore, UserSettingsRow, _legacy_lang_key(), SettingsRow, UserSettings, _seed_legacy_lang(), TestDefaults, TestIndependence (+4 more)

### Community 16 - "Context"
Cohesion: 0.16
Nodes (14): _added_update(), _bot(), _ctx(), _member(), _run_setup_to_plan(), _Settings, TestAdded, tap() (+6 more)

### Community 17 - "bot/media.py"
Cohesion: 0.06
Nodes (15): download_combined_audio(), download_stitched_audio(), fetch_and_stitch(), _fit_for_telegram(), _semaphore(), stitch_images(), data(), no_cdn() (+7 more)

### Community 18 - "parse_reference"
Cohesion: 0.06
Nodes (13): clamp_to_quran(), _clean(), format_ref(), parse_range(), parse_reference(), TestSurahSpans, TestAcrossSurahs, TestContainsAndClamp (+5 more)

### Community 19 - "RedisSingleton"
Cohesion: 0.06
Nodes (15): 6. Issues fixed in this refactor, forget(), _key(), pick(), remember(), get(), _key(), save() (+7 more)

### Community 20 - "t"
Cohesion: 0.06
Nodes (27): _ref_from_draft(), _send_drill(), _cancel_row(), _custom_days_keyboard(), _days_keyboard(), _drill_keyboard(), _pace_keyboard(), _plan_keyboard() (+19 more)

### Community 21 - "WhatsAppChannel"
Cohesion: 0.15
Nodes (4): _bytes_and_name(), _resolve(), _split_choices(), TestMedia

### Community 22 - "group.py"
Cohesion: 0.09
Nodes (22): _begin_setup(), bot_username(), _chat_id(), _create_topic(), _days_keyboard(), _deep_link(), _enqueue_next_board(), group_board_entries() (+14 more)

### Community 23 - "Hifz Progress Cmd Tests"
Cohesion: 0.13
Nodes (13): _CallbackQuery, _ctx(), _edited(), _intervals(), _isolate_registries(), _mark(), _Message, _progress() (+5 more)

### Community 24 - "services/plans.py"
Cohesion: 0.05
Nodes (44): not_found(), ref_out(), RefOut, surah_name(), active(), _build(), complete(), create() (+36 more)

### Community 25 - "Refactor — Implementation Plan"
Cohesion: 0.15
Nodes (13): 10. Found along the way (out of scope — behaviour changes), 2. Goals and non-goals, 3. Principles applied, 6. Ordering, risk, size, 7. Safety net, 8. Expected result, 9. Decisions and open questions, Expected result metrics (§8) (+5 more)

### Community 26 - "TelegramChannel"
Cohesion: 0.10
Nodes (6): TelegramChannel, TestAnswerAndTyping, TestEditChoices, TestEditText, TestMedia, TestSendText

### Community 27 - "test_hifz_streak.py"
Cohesion: 0.10
Nodes (14): cache_key(), _caption(), _ctx(), _earn(), _isolate_registries(), _photo_message(), _Settings, _streak() (+6 more)

### Community 28 - "Hifz Platform - Plan & Progress"
Cohesion: 0.09
Nodes (20): Hifz Platform - Plan & Progress, Phase 1 acceptance criteria (tests/test_acceptance.py), Hifz change log, claim_due claimed_at clock bug, Hifz data model (user_profile, hifz_interval, plan, plan_day, session_log, scheduled_send, group_*), Phase 2 group cluster (J1-J6, forum topics), Workstream I: i18n & commands for 48 locales, Workstream C: interval merge-on-insert + derived percentages (+12 more)

### Community 29 - "Acceptance Tests"
Cohesion: 0.10
Nodes (12): _CallbackQuery, _cmd(), _ctx(), _Message, _run_wizard(), _save_plan(), _Settings, _tap() (+4 more)

### Community 30 - "features/profile.py"
Cohesion: 0.08
Nodes (20): _template_text(), _translation_text(), _cancel_keyboard(), _join_board(), name_step(), on_profile_tap(), _plan_line(), profile_command() (+12 more)

### Community 31 - "Docker Compose.stress"
Cohesion: 0.06
Nodes (33): build, container_name, cpus, depends_on, env_file, environment, mem_limit, mem_swappiness (+25 more)

### Community 33 - "test_recall_check.py"
Cohesion: 0.18
Nodes (3): test_pick_ayah_is_deterministic_per_user_and_date(), test_pick_ayah_on_an_inverted_or_empty_span(), test_unknown_ayahs_are_rejected()

### Community 34 - "stats.py"
Cohesion: 0.18
Nodes (10): BoardEntry, BoardMe, DayCount, leaderboard(), LeaderboardOut, MilestoneOut, streak(), StreakOut (+2 more)

### Community 35 - "infra/uz_audio.py"
Cohesion: 0.12
Nodes (12): byte_range(), entry(), estimated(), Part, parts(), reset_for_tests(), seconds(), size() (+4 more)

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
Nodes (15): _baqarah(), _data(), _fatiha(), fetched(), table(), test_api_send_runs_the_bot_feature(), test_clip_fetches_its_range_and_marks_estimated(), test_fetch_rejects_a_bad_response() (+7 more)

### Community 41 - "TranslationRegistry"
Cohesion: 0.09
Nodes (8): 12. Testing, parse_quran(), TranslationRegistry, corpus(), preload_corpus(), TestCorpusIntegrity, TestCaching, TestFallback

### Community 42 - "PostgresPlanStore"
Cohesion: 0.05
Nodes (5): InMemoryPlanStore, PlanDayRow, PlanRow, PlanStore, PostgresPlanStore

### Community 43 - "to_markup"
Cohesion: 0.12
Nodes (8): page_keyboard(), verse_keyboard(), to_button(), to_markup(), TestToMarkup, TestPageKeyboard, _button(), TestVerseKeyboard

### Community 44 - "handle_update"
Cohesion: 0.20
Nodes (7): reference(), _inline_query(), _of_type(), _results(), TestInlineArabicImage, TestRangeAudio, TestRangeText

### Community 45 - "Streaks"
Cohesion: 0.14
Nodes (4): record_session(), TestFiveAndSixTheBoard, TestThreeTheStreak, TestRecordSession

### Community 46 - "asyncio"
Cohesion: 0.11
Nodes (6): range_audio(), content(), TestRangeAudioRoute, fake_download(), TestStitching, __init__()

### Community 47 - "Four multilingual dimensions (UI, translation, tafsir, audio)"
Cohesion: 0.17
Nodes (13): Four multilingual dimensions (UI, translation, tafsir, audio), Per-user language preference (lang:{chat_id}, detect from language_code, /language), locales/ tables + t(key, lang) with English fallback, Multilingual phased roadmap (UI i18n -> translations -> polish -> content depth), Quran.from_file(path) refactor, setMyCommands per language, TafsirRegistry with fallback to en, tanzil.net translation catalogue (+5 more)

### Community 48 - "1. Why"
Cohesion: 0.09
Nodes (19): 1. Why, 5. Phases, Phase 0 — Guardrails (no code moves) — *done*, Phase 2 — DRY the duplicated patterns — *done*, Phase 4 — Split infrastructure god-objects — *done*, Phase 5 — Fix the layering — *done*, Phase 6 — Repository hygiene — *done*, _post_portion() (+11 more)

### Community 49 - "Schema"
Cohesion: 0.10
Nodes (29): daily_ayah_sub, group_config, group_member_link, group_plan, group_plan_chat_status_idx, group_plan_day, group_plan_day_plan_date_idx, hifz_interval (+21 more)

### Community 50 - "Services"
Cohesion: 0.14
Nodes (20): client(), _jwt_secret(), _login(), test_bare_check_falls_back_to_juz_30(), test_cannot_complete_someone_elses_portion(), test_catalogs(), test_drill_in_app_and_chat_logs_one_session(), test_lifecycle_and_today() (+12 more)

### Community 51 - "test_tajweed_lessons.py"
Cohesion: 0.11
Nodes (17): _case(), to_cyrillic(), to_latin(), _word_to_cyr(), _buttons(), _ctx(), reviewers(), store() (+9 more)

### Community 52 - "services/check.py"
Cohesion: 0.13
Nodes (8): build_question(), pick_ayah(), RecallQuestion, ask(), default_span(), rebuild(), Score, score()

### Community 53 - "api/progress.py"
Cohesion: 0.19
Nodes (16): parse_ref_or_422(), forget(), ForgetIn, ForgetOut, _juz(), JuzRatio, progress(), ProgressOut (+8 more)

### Community 54 - "api/check.py"
Cohesion: 0.15
Nodes (11): require_user(), _unauthorized(), answer(), AnswerIn, AnswerOut, make_token(), question(), QuestionOut (+3 more)

### Community 55 - "GroupStore"
Cohesion: 0.10
Nodes (4): GroupConfig, GroupMemberLink, GroupPlanRow, GroupStore

### Community 56 - "reader.py"
Cohesion: 0.09
Nodes (20): juz(), page(), turn_page(), random_ayah(), read_text(), reader_position(), repeat(), _send_verse() (+12 more)

### Community 57 - "whatsapp_setup.py"
Cohesion: 0.11
Nodes (16): build(), main_(), main(), score(), automation(), _bot_api(), Graph, main() (+8 more)

### Community 58 - "os"
Cohesion: 0.10
Nodes (22): main(), placeholders(), export(), languages(), main(), resolved_table(), _write(), _modules() (+14 more)

### Community 59 - "store/__init__.py"
Cohesion: 0.07
Nodes (12): Milestone, offset_of(), StreakCounts, InMemoryDailyStore, HifzStore, InMemoryHifzStore, InMemoryStore, MemoryState (+4 more)

### Community 60 - "surah_progress"
Cohesion: 0.11
Nodes (7): juz_progress(), JuzProgress, quran_progress(), _spans(), started_juzs(), TestJuzProgress, TestQuranProgress

### Community 61 - "test_reciter_picker.py"
Cohesion: 0.16
Nodes (5): reciter_page_of(), reciter_catalog(), reciter_group(), TestCatalogOrder, TestCurrentReciter

### Community 62 - ".test_full_flow_queues_the_first_send"
Cohesion: 0.38
Nodes (5): _buttons(), _message(), _tap(), TestTelegramSetup, _texts()

### Community 63 - "Mini App Plan"
Cohesion: 0.11
Nodes (18): 10. Risks, 11. Decisions (resolved 2026-10-20), 12. Change log, 1. Scope, 2. Decisions (confirmed 2026-10-20), 3. Architecture, 4.1 Flow, 4.2 Rules (+10 more)

### Community 64 - "localtime.py"
Cohesion: 0.06
Nodes (17): _enqueue_next_group(), offset_from_callback(), _as_utc(), format_offset(), local_date(), local_now(), local_time(), next_due_utc() (+9 more)

### Community 65 - "info.py"
Cohesion: 0.14
Nodes (13): command, Routing rules (in `serve`), _is_telegram_id(), link(), unlink(), about(), help_(), index() (+5 more)

### Community 67 - "summarize"
Cohesion: 0.06
Nodes (9): Progress, ProgressSummary, summarize(), SurahProgress, HifzInterval, load_summary(), _at(), TestLoadSummary (+1 more)

### Community 68 - "require_user"
Cohesion: 0.29
Nodes (7): 8. Phased task breakdown, Phase 0 — Foundations, Phase 1 — Service-layer extraction (this repo, no UI change), Phase 2 — Reader parity (read-only, low risk, ships first), Phase 3 — Hifz parity, Phase 4 — Recitation checker UI (depends on the investigation's Phase A), Phase 5 — Later

### Community 69 - ".reply"
Cohesion: 0.08
Nodes (27): 5. API surface (`/api/v1`), Phase 2 — WhatsApp MVP (reader + daily ayat), 7. The keyboard & command localization challenge, Telegram command menu, _ask_time(), daily(), _enable(), _hhmm() (+19 more)

### Community 70 - "surah_progress"
Cohesion: 0.11
Nodes (5): started_surahs(), surah_progress(), TestInputHandling, TestSpecAcceptance, TestSurahProgress

### Community 71 - "parse_ayah_range"
Cohesion: 0.23
Nodes (3): parse_ayah_range(), TestCommandArguments, TestParseAyahRange

### Community 72 - "Hifz Seam Tests"
Cohesion: 0.16
Nodes (3): _ctx(), TestCtx, TestDispatchWizard

### Community 73 - "session.py"
Cohesion: 0.08
Nodes (30): init_data_max_age(), jwt_secret(), auth_link(), auth_telegram(), AuthOut, LinkAuthIn, me(), _me() (+22 more)

### Community 74 - "handle_update"
Cohesion: 0.19
Nodes (18): handle_update(), _callback(), fake_bot(), _message(), test_about_uses_html(), test_group_chats_are_ignored(), test_index_sends_surah_index(), test_inline_query_valid_ayah_returns_all_four_views() (+10 more)

### Community 75 - "whatsapp_format.py"
Cohesion: 0.20
Nodes (3): _Converter, _render(), _wrap()

### Community 76 - "SendCtx"
Cohesion: 0.09
Nodes (16): register_send_handler(), registered_kinds(), _same_origin(), decorate(), catch_up(), run_scheduler(), _wait(), _deliver() (+8 more)

### Community 77 - "quran_page_progress"
Cohesion: 0.11
Nodes (3): juz_page_progress(), TestPageProgress, _whole_quran_spans()

### Community 78 - "bundle_translations.py"
Cohesion: 0.22
Nodes (7): bundle_one(), fetch_edition(), main(), to_lines(), transliterate_uz(), write_attributions(), write_file()

### Community 79 - "Recitation Checker Investigation: RECITATION_CHECKER_INVESTIGATIONmd"
Cohesion: 0.11
Nodes (20): Audio catalog kinds, Repeat (memorization), Translation-only catalogue entries (UI_LANGUAGES vs LANGUAGES), Mini App feature parity map, Phase 4 — Recitation checker UI, Mini App phased task breakdown (Phases 0-5), Word alignment (Needleman-Wunsch) with confidence gating, Riwayah divergence table (closed-set check at farsh points) (+12 more)

### Community 80 - "pytest"
Cohesion: 0.10
Nodes (11): ignore_not_modified(), test_any_other_bad_request_propagates(), test_not_modified_is_swallowed(), test_other_errors_propagate(), _as_dict(), _ctx(), _Settings, _static_cases() (+3 more)

### Community 81 - "._send_media"
Cohesion: 0.15
Nodes (4): _build(), _send(), send_cached(), build()

### Community 83 - "InMemorySessionStore"
Cohesion: 0.07
Nodes (6): InMemorySessionStore, LeaderboardEntry, PostgresSessionStore, SessionRow, SessionStore, WeeklyBoard

### Community 84 - "Scheduler Tests"
Cohesion: 0.17
Nodes (4): _claimed_at(), _record(), TestCatchUp, TestTick

### Community 85 - ".get"
Cohesion: 0.17
Nodes (3): TestCorruptState, TestLifecycle, TestOneDraftPerUser

### Community 87 - "send_surah"
Cohesion: 0.28
Nodes (6): build(), send_surah(), build(), surah_key(), fetch(), url()

### Community 88 - "main.py"
Cohesion: 0.07
Nodes (7): privacy(), webhook_secret(), setup_logging(), test_http_client_request_urls_are_never_logged(), test_startup_registers_the_webhook_without_the_token(), test_the_secret_does_not_reveal_the_token(), test_webhook_acks_before_initialization()

### Community 89 - "test_api_auth.py"
Cohesion: 0.15
Nodes (21): _init_data_secret(), InvalidInitData, sign_init_data(), validate_init_data(), _auth(), _fields(), _jwt_secret(), test_added_field_is_rejected() (+13 more)

### Community 90 - "Store Contract Tests"
Cohesion: 0.11
Nodes (3): _spans(), TestHifzIntervalEdges, TestHifzIntervals

### Community 91 - "Multi Platform Plan: MultiPlatform Implementation Plan"
Cohesion: 0.12
Nodes (17): 10. Other platforms — shortlist for Phase 6, 11. Open decisions (needed before Phase 1), 12. Change log, 1. Scope, 2. Decisions (proposed — confirm before Phase 1), 3. Architecture, 4. WhatsApp constraints that shape the design, 5. Data model changes (`src/common/schema.sql`) (+9 more)

### Community 92 - "test_inline_reciter_search.py"
Cohesion: 0.15
Nodes (18): _audio_result(), fake_bot(), _inline_callback(), _inline_query(), test_ayah_audio_dropped_for_unknown_reciter(), test_ayah_audio_dropped_without_public_base_url(), test_ayah_audio_uses_callers_reciter(), test_ayah_query_is_personal_and_briefly_cached() (+10 more)

### Community 93 - "_hifz"
Cohesion: 0.10
Nodes (4): _hifz(), _spans(), TestAddInterval, TestRemoveRange

### Community 95 - "test_whatsapp_router.py"
Cohesion: 0.15
Nodes (10): bodies(), fixture_message(), known_user(), rows(), tap(), TestBoundaries, TestMenu, stitch() (+2 more)

### Community 97 - "test_hifz_check.py"
Cohesion: 0.06
Nodes (21): _parse_answer(), percentile_band(), refresh_streaks(), streak_summary(), user_today(), _answer_data(), _AnyDay, _ask() (+13 more)

### Community 99 - "_message"
Cohesion: 0.21
Nodes (4): _message(), TestJuzCommand, TestPageCommand, TestSajdaCommand

### Community 101 - "File"
Cohesion: 0.10
Nodes (6): image_url(), File, TestAudioFilename, TestImageFilename, TestLegacyLanguageKey, TestCoexistsWithTheReciterFlow

### Community 103 - "api/uz_audio.py"
Cohesion: 0.29
Nodes (6): send(), SendIn, SendOut, available(), send_to_user(), valid_clip()

### Community 104 - "recall_check.py"
Cohesion: 0.08
Nodes (21): _assemble(), _at_offset(), _continuation_question(), _date_key(), display_length(), _distinct(), _everything(), _gather() (+13 more)

### Community 105 - "button_action"
Cohesion: 0.09
Nodes (8): button_action(), keyboard_rows(), missing_keys(), _reverse_button_map(), _placeholders(), TestButtonAction, TestGroupLocaleExemption, TestLocaleIntegrity

### Community 107 - "Wizard"
Cohesion: 0.15
Nodes (4): Wizard, test_draft_is_written_with_that_ttl(), TestCancel, wiz()

### Community 109 - "asyncio"
Cohesion: 0.14
Nodes (12): batch(), message_update(), random_text(), _container_alive(), _docker_stats(), _fire_one(), main(), _mem_to_mb() (+4 more)

### Community 110 - "BismillahBot — Business Logic"
Cohesion: 0.11
Nodes (17): 1. Overview, 2. Architecture, 3. Request lifecycle, 5. Caching strategy, 7. Known limitations / tech debt, 8. Future roadmap, 9. The hifz platform, BismillahBot — Business Logic (+9 more)

### Community 111 - "TestTransliteration"
Cohesion: 0.12
Nodes (4): missing_locales(), TestCatalogue, TestAvailable, TestTransliteration

### Community 113 - "offset_keyboard"
Cohesion: 0.35
Nodes (7): offset_keyboard(), _grid(), test_a_label_prefix_changes_only_the_label(), test_cancel_data_adds_a_localized_cancel_row(), test_every_offset_is_offered_in_order_under_the_callers_prefix(), test_no_cancel_row_unless_asked(), test_rows_are_columns_wide()

### Community 114 - "fixture"
Cohesion: 0.04
Nodes (34): _clean_state_store(), build_data(), signature(), get_default_query_results(), make_index(), _isolate_registries(), data(), probe() (+26 more)

### Community 115 - "Koyeb Capacity Report"
Cohesion: 0.25
Nodes (7): Koyeb free-tier capacity report, CPU-bound queueing failure mode (~24 msg/s ceiling), Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start), Neon managed Postgres, Capacity results 5-1000 concurrent (no errors, 70-91 MB), Stress environment (docker-compose.stress.yml, cpus 0.1, 512m), Synthetic traffic mix (scripts/stress/gen_updates.py)

### Community 116 - "Blue Green Ci"
Cohesion: 0.14
Nodes (13): concurrency, cancel-in-progress, group, env, PYTHON_DEFAULT, name, on, pull_request (+5 more)

### Community 117 - "Blue Green Ci: name"
Cohesion: 0.23
Nodes (14): steps, steps, steps, steps, steps, steps, steps, env (+6 more)

### Community 118 - "PostgresScheduleStore"
Cohesion: 0.06
Nodes (6): enqueue(), idempotency_key(), schedule_daily(), PostgresScheduleStore, ScheduledSend, ScheduleStore

### Community 121 - "test_store_selection.py"
Cohesion: 0.06
Nodes (15): health(), cache_backend(), database_url(), _failing_create_pool(), create_pool(), _FakePool, fast_retries(), fresh_redis() (+7 more)

### Community 122 - "compute_streak"
Cohesion: 0.24
Nodes (3): compute_streak(), days_back(), TestComputeStreak

### Community 123 - "Hifz platform frozen string manifest"
Cohesion: 0.13
Nodes (13): Translation Attributions, alquran.cloud API, en.ahmedraza (Ahmed Raza Khan), tanzil.net, Translation editions table (48 codes), Hifz platform frozen string manifest, src/locales/en.py source of truth, Key conventions (btn_*, cmd_*) (+5 more)

### Community 124 - "_align"
Cohesion: 0.11
Nodes (27): align(), _align(), containment(), load_pins(), onset_cut(), quiet_mask(), quiet_runs(), skeleton() (+19 more)

### Community 125 - "button_rows"
Cohesion: 0.17
Nodes (7): sajda(), button_rows(), sajda_keyboard(), test_a_non_positive_width_is_one_per_row(), test_an_exact_fit_has_no_empty_trailing_row(), test_nothing_in_nothing_out(), test_packs_in_order_with_a_short_last_row()

### Community 126 - "InMemoryStore"
Cohesion: 0.12
Nodes (6): _covers(), _merge_span(), _overlaps(), _split_span(), _touches(), TestHelpers

### Community 127 - "Blue Green Ci: jobs"
Cohesion: 0.15
Nodes (13): name, needs, runs-on, jobs, build, lint, rollback, name (+5 more)

### Community 128 - "Blue Green Ci: with"
Cohesion: 0.15
Nodes (13): with, cache, cache-dependency-path, cache-from, cache-to, context, if-no-files-found, load (+5 more)

### Community 130 - "test_hifz_intervals.py"
Cohesion: 0.23
Nodes (6): _assert_invariant(), _ayahs(), test_a_random_walk_never_leaks_across_users(), test_any_sequence_of_marks_and_removals_keeps_the_invariant(), test_intervals_from_many_surahs_come_back_in_mushaf_order(), TestEveryRelativePosition

### Community 131 - "time"
Cohesion: 0.25
Nodes (10): _b64url(), decode_token(), InvalidToken, issue_token(), _sign(), test_expired_token_is_rejected(), test_token_round_trip(), test_token_signed_with_other_secret_is_rejected() (+2 more)

### Community 132 - "answer_inline_query"
Cohesion: 0.14
Nodes (7): answer_inline_query(), inline_audio_result(), inline_photo_results(), combined_audio_key(), range_audio_url(), ref_key(), performer_name()

### Community 135 - "TestPickerFlow"
Cohesion: 0.15
Nodes (6): _callback(), _message(), _reciter_buttons(), _tab_row(), TestAudioNeverFollowsLanguage, TestPickerFlow

### Community 136 - "reciter_keyboard"
Cohesion: 0.27
Nodes (4): reciter_keyboard(), reciter_page_count(), _pager_row(), TestPagination

### Community 137 - "test_media_cache_keys.py"
Cohesion: 0.38
Nodes (5): _bot(), _next_id(), send_audio(), send_photo(), test_a_rejected_cached_id_is_rebuilt_and_recached()

### Community 138 - "Tajweed (tajvid) section: plan"
Cohesion: 0.13
Nodes (14): 10. Phases, 11. Testing, 12. Attribution, 13. Open questions, 1. Decisions (2026-11-09), 2. Data: where the rules come from, 3. Curriculum (v1, ~24 lessons), 4. Picking good examples automatically (+6 more)

### Community 139 - ".get_surah_length"
Cohesion: 0.16
Nodes (5): ayah_count(), plan_target(), TestAyahCount, test_short_surahs_still_get_four_distinct_options(), test_the_last_ayah_of_every_surah_produces_a_question()

### Community 140 - "MINI_APP_PLAN.md"
Cohesion: 0.09
Nodes (21): Central callback prefix allocation (hifz.PREFIXES), Future roadmap and prioritized backlog, The hifz platform (memorization companion), Pure plan builder (build_plan), Streak day ticks on completed session, /api/v1 REST surface, Bot ↔ Mini App integration (menu button, startapp, /app), initData HMAC validation → short-lived JWT (+13 more)

### Community 141 - "Phase 2 — DRY the duplicated patterns"
Cohesion: 0.14
Nodes (11): graphify knowledge graph (graphify-out/), CLAUDE.md graphify lookup rules, button_rows() row-packing helper, Copy-pasted patterns table (§1.3), ignore_not_modified() context manager, Shared UTC offset picker (time_pickers.offset_keyboard), Found along the way (out-of-scope behaviour changes), Phase 2 — DRY the duplicated patterns (+3 more)

### Community 144 - "weekly_board"
Cohesion: 0.07
Nodes (16): user_week_window(), week_window(), weekly_board(), _CallbackQuery, _ctx(), _earn(), _isolate_registries(), _join() (+8 more)

### Community 146 - "keyboards/menu.py"
Cohesion: 0.25
Nodes (7): on_menu(), show_main_menu(), main_menu(), _rows(), settings_menu(), welcome_choices(), send_welcome()

### Community 148 - "test_page_mode.py"
Cohesion: 0.29
Nodes (7): send_page(), _buffer(), _stub_stitch(), stub(), TestPageCard, capture(), counting()

### Community 153 - "11.1 Profile settings reset after a while — `fix/settings-persistence`"
Cohesion: 0.22
Nodes (6): 11.1 Profile settings reset after a while — `fix/settings-persistence`, 11.2 Timezone picker by country — `feat/timezone-by-country`, 11. User-reported problems, DatabaseUnavailable, get_pool(), _lock()

### Community 154 - "Blue Green Ci: env"
Cohesion: 0.40
Nodes (10): env, ACTIVE, BLUE_SERVICE, GREEN_SERVICE, KOYEB_API_TOKEN, KOYEB_APP, PRODUCTION_DOMAIN, TARGET (+2 more)

### Community 155 - "test_channels_whatsapp.py"
Cohesion: 0.12
Nodes (6): taps(), TestChoices, TestDressing, TestNumberedMenuLifetime, TestText, TestTransport

### Community 159 - "Dependency rule (app -> bot -> services -> domain)"
Cohesion: 0.22
Nodes (8): tests/test_layering.py ratchet (KNOWN violations), Overlap with MULTI_PLATFORM_PLAN channel seam, Decisions and open questions (§9), Phase 0 — Guardrails (ruff, layering test, logging), Phase 5 — Fix the layering, Target layout (app/ bot/ services/ domain/ infra/), Timezone picker by country (feat/timezone-by-country), Memorizing (hifz): /memorize, /check, /progress, /streak, /leaderboard, /profile

### Community 160 - "account_link.py"
Cohesion: 0.31
Nodes (5): _code_key(), issue(), redeem(), too_many_tries(), _tries_key()

### Community 161 - "reciter_label"
Cohesion: 0.24
Nodes (3): reciter_label(), reciter_search_keyboard(), TestLabels

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
Cohesion: 0.22
Nodes (10): ALLOW_MEMORY_STORE flag / DatabaseUnavailable / CacheUnavailable, lib/utils.File god class, GET / health with store and cache status (503), Silent in-memory store fallback, Phase 4 — Split infrastructure god-objects, Profile settings reset fix (fix/settings-persistence), Typed frozen Settings (config/settings.py), Blue-Green CI pipeline (blue-green-ci.yml) (+2 more)

### Community 170 - "features/__init__.py"
Cohesion: 0.08
Nodes (21): Phase 3 — One router for everything — *done*, _on_callback(), _on_text(), _search_reciters(), decorate(), _cancel(), command(), decorate() (+13 more)

### Community 171 - "Blue Green Ci: smokegreen"
Cohesion: 0.25
Nodes (8): BLUE_HEALTH_URL, GREEN_HEALTH_URL, smoke-green, env, if, name, needs, runs-on

### Community 172 - "test_miniapp_links.py"
Cohesion: 0.22
Nodes (11): set_menu_button(), _app_command(), app_on(), test_app_command(), test_app_command_without_url(), test_cards_and_drill_link_to_their_screens(), test_inline_messages_never_get_a_web_app_button(), test_menu_button() (+3 more)

### Community 173 - "FakeChannel"
Cohesion: 0.20
Nodes (6): FakeChannel, test_big_surah_goes_in_parts(), test_small_surah_goes_by_url(), test_source_failure_is_reported_not_raised(), test_tap_sends_and_acknowledges(), test_verified_surah_has_no_estimate_note()

### Community 174 - "send_repeated_audio"
Cohesion: 0.26
Nodes (3): send_repeated_audio(), _stub_audio(), TestRepeatForMemorization

### Community 175 - "test_uz_audio_timings.py"
Cohesion: 0.22
Nodes (7): Fixing a wrong timing, Format and the download formula, Pipeline, Setup (once), Transcribing on Colab (preferred), Uzbek translation audio — timing tool, test_baqarah_matches_the_cuts_approved_by_ear()

### Community 176 - "test_tajweed_data.py"
Cohesion: 0.20
Nodes (3): test_every_annotation_is_a_known_rule_inside_its_ayah(), test_every_rule_has_real_examples(), test_text_covers_every_ayah()

### Community 177 - "_ayah_text"
Cohesion: 0.20
Nodes (5): _ayah_text(), _basmala_prefix(), _clean(), _option_from(), _whole_ayah_option()

### Community 178 - "BismillahBot README"
Cohesion: 0.14
Nodes (14): Four ayah representations (english, tafsir, arabic, audio), Known limitations / tech debt, Issues fixed in the refactor (12 bugs), Documentation, Documentation index (docs/README.md), Phase 6 — Repository hygiene, CI — Blue-Green pipeline, Running the tests locally (+6 more)

### Community 179 - "test_keyboard_snapshots.py"
Cohesion: 0.23
Nodes (5): _as_dict(), _keyboards(), _render(), _search_markup(), test_keyboards_match_their_snapshots()

### Community 182 - "Blue Green Ci: deploygreen"
Cohesion: 0.33
Nodes (6): environment, if, name, needs, runs-on, deploy-green

### Community 183 - "Blue Green Ci: promote"
Cohesion: 0.33
Nodes (6): promote, environment, if, name, needs, runs-on

### Community 184 - "Phase 1 — Take `main.py` apart (pure moves) — *done*"
Cohesion: 0.31
Nodes (3): Phase 1 — Take `main.py` apart (pure moves) — *done*, reciter_set_confirmation(), TestKindWarnings

### Community 185 - "lang_hint"
Cohesion: 0.20
Nodes (3): lang_hint(), TestKeywords, TestUsernames

### Community 188 - "6. Phased task breakdown"
Cohesion: 0.25
Nodes (8): 6. Phased task breakdown, Phase 0 — Prerequisites (no code), Phase 1 — Channel seam (this repo, no user-visible change), Phase 3 — Hifz on WhatsApp, Phase 4 — Recitation checker on WhatsApp, Phase 5 — Web access outside Telegram, Phase 6 — Later, bot()

### Community 189 - "next_scheduled_date"
Cohesion: 0.29
Nodes (3): _advance(), next_scheduled_date(), _validated_days()

### Community 197 - ".wa_user"
Cohesion: 0.36
Nodes (4): apps(), Apps, _code(), TestLinking

### Community 198 - "handle_message"
Cohesion: 0.15
Nodes (8): _allowed_command(), as_command(), handle_message(), _now(), opt_out(), _tap(), TestFirstContact, text()

### Community 200 - "Graph"
Cohesion: 0.20
Nodes (4): client(), data(), graph(), Graph

### Community 203 - "Identity table (platform, external_id → user_id)"
Cohesion: 0.67
Nodes (4): Identity table (platform, external_id → user_id), WhatsApp opt-in / STOP opt-out flow, WhatsApp constraints (24-h window, templates, pricing, opt-in), Window-aware scheduler (session message vs template)

### Community 207 - "WhatsAppChannel"
Cohesion: 0.08
Nodes (10): for_platform(), WhatsAppChannel, TestForPlatform, cache(), channel(), graph(), Graph, test_a_bsuid_is_addressed_as_recipient() (+2 more)

### Community 209 - "milestone_for"
Cohesion: 0.33
Nodes (3): milestone_for(), _milestone_key(), TestMilestones

### Community 210 - "export_web_content.py"
Cohesion: 0.16
Nodes (8): build_meta(), export(), main(), _spans(), split_basmalah(), uz_audio_doc(), _write(), parse_quran_tafsir()

### Community 211 - "version"
Cohesion: 0.40
Nodes (4): ayah_key(), part_key(), version(), test_cache_keys_follow_the_timing_version()

### Community 212 - "features/check.py"
Cohesion: 0.18
Nodes (7): _answer_data(), _ask(), check(), on_check(), _options_keyboard(), _question_text(), _score()

### Community 213 - "BismillahBot — Multilingual Support Plan"
Cohesion: 0.14
Nodes (14): 10. File-by-file change list, 11. Memory & performance (free-tier reality), 13. Risks & open questions, 14. Recommended first step, 1. Goal & scope, 2. Current-state audit (what is hardcoded English), 3. Target architecture, 4. User language preference (+6 more)

### Community 216 - "test_hifz_seam.py"
Cohesion: 0.20
Nodes (3): _isolate_registries(), _Settings, TestSchemaApplication

### Community 266 - "_patch_client"
Cohesion: 0.67
Nodes (4): _patch_client(), client(), test_fetch_sends_the_range_and_returns_the_bytes(), handler()

### Community 270 - "PostgresStore"
Cohesion: 0.06
Nodes (9): DailyStore, DailySubRow, PostgresDailyStore, PostgresStore, Store, ApprovalRow, PostgresTajweedStore, TajweedStore (+1 more)

### Community 271 - "locales/__init__.py"
Cohesion: 0.06
Nodes (16): nav_labels(), _division_marks(), get_translation(), _load_locales(), _module_name(), get_language(), is_supported(), is_ui_language() (+8 more)

### Community 280 - "get_store"
Cohesion: 0.16
Nodes (5): get_store(), _lock(), TestFourProgress, TestBoard, TestDailyPost

### Community 282 - "get_settings"
Cohesion: 0.05
Nodes (25): get_position(), _lang(), LanguageOut, languages(), LanguagesOut, put_position(), ReaderPosition, Reciter (+17 more)

### Community 289 - "Separate quranayat-miniapp Next.js repo; API in this repo"
Cohesion: 0.13
Nodes (13): Inline query answering (all four representations, ranges), Navigation model ((surah, ayah, type) per chat_id), Page audio with stitched fallback, Page image stitching (lib/page_image.py), Structural divisions (page / juz / sajda from quran-data.xml), Verse card (inline keyboard, edit in place), Uthmani text in Amiri Quran / KFGQPC font, Client-side playlist audio (no server stitching) (+5 more)

### Community 295 - "SendCtx"
Cohesion: 0.51
Nodes (4): _due_rows(), TestWhatsApp, wa_tap(), wa_text()

### Community 317 - "tajweed_lessons.py"
Cohesion: 0.11
Nodes (15): examples(), _examples(), _hash(), Lesson, lesson(), lessons(), _load(), neighbours() (+7 more)

### Community 332 - "test_export_web_content.py"
Cohesion: 0.14
Nodes (10): _load(), test_every_ui_language_is_exported_resolved_like_t(), test_languages_catalogue_carries_rtl(), _count(), _load(), test_arabic_has_every_ayah(), test_basmalah_is_lifted_into_a_flag(), test_every_translation_has_every_ayah() (+2 more)

### Community 333 - "WhatsApp"
Cohesion: 0.24
Nodes (4): test_a_week_on_whatsapp_matches_a_week_on_telegram(), test_without_consent_whatsapp_gets_no_reminders(), _week(), WhatsApp

## Knowledge Gaps
- **51 isolated node(s):** `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres`, `Capacity results 5-1000 concurrent (no errors, 70-91 MB)`, `Central callback prefix allocation (hifz.PREFIXES)` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1839 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **142 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_store()` connect `get_store` to `routes/whatsapp.py`, `dispatch.py`, `Wizard`, `build_grid`, `PostgresStore`, `UserSettings`, `Context`, `weekly_board`, `RedisSingleton`, `Hifz Progress Cmd Tests`, `services/plans.py`, `11.1 Profile settings reset after a while — `fix/settings-persistence``, `test_hifz_streak.py`, `Acceptance Tests`, `stats.py`, `_ctx`, `SendCtx`, `Streaks`, `Services`, `api/progress.py`, `api/check.py`, `reader.py`, `store/__init__.py`, `.test_full_flow_queues_the_first_send`, `summarize`, `.wa_user`, `handle_message`, `surah_progress`, `session.py`, `handle_update`, `SendCtx`, `.test_sends_todays_ayah_and_queues_tomorrow`, `WhatsApp`, `pytest`, `_hifz`, `test_whatsapp_router.py`, `test_hifz_check.py`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `get_store()` (e.g. with `11.1 Profile settings reset after a while — `fix/settings-persistence`` and `.apply_schema()`) actually correct?**
  _`get_store()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Synthetic traffic mix (scripts/stress/gen_updates.py)`, `Fidelity limits (no Telegram RTT, local Postgres for Neon, no cold start)`, `Neon managed Postgres` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_plan` be split into smaller, more focused modules?**
  _Cohesion score 0.05225885225885226 - nodes in this community are weakly interconnected._
- **Why does `Ctx` connect `Ctx` to `info.py`, `.reply`, `dispatch.py`, `features/__init__.py`, `Wizard`, `Choice`, `1. Why`, `Context`, `keyboards/menu.py`, `pytest`, `features/check.py`, `t`, `group.py`, `reader.py`, `TelegramChannel`, `button_rows`, `features/profile.py`, `Mini App Plan`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 44 inferred relationships involving `Ctx` (e.g. with `3. Architecture` and `4.1 Overlap with `MULTI_PLATFORM_PLAN.md``) actually correct?**
  _`Ctx` has 44 INFERRED edges - model-reasoned connections that need verification._
- **Should `Quran` be split into smaller, more focused modules?**
  _Cohesion score 0.04679089026915114 - nodes in this community are weakly interconnected._