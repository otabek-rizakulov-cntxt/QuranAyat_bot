# English — the canonical UI strings. Every other locale falls back to these
# per-key, so this table must define every key the bot uses.

strings = {
    "welcome_intro": (
        "Send me a surah and ayah number, for example <b>2:255</b>, and I'll reply with "
        "that verse of the Holy Qur'an.\n\n"
        "You can also send a range like <b>59:22-24</b> for a combined audio recitation."
    ),
    "welcome_commands_header": "Commands:",
    "welcome_inline": (
        "You can use me inline in any chat: type <b>@QuranAyat_bot</b> followed by a "
        "reference."
    ),
    "about": (
        "This bot lets you explore the Holy Qur'an on Telegram in many languages.\n\n"
        "Translations are sourced from tanzil.net (see ATTRIBUTIONS.md for each "
        "translation's edition and translator). Audio recitations are sourced from "
        "everyayah.com — pick your reciter any time with /reciter. The tafsir is "
        "Tafsir al-Jalalayn (altafsir.com), available in English.\n\n"
        "Change your UI language with /language, and your translation language "
        "separately with /translation."
    ),
    "ayah_not_found": "Ayah does not exist!",
    "range_too_large": "Range too large, please request at most {n} ayahs at a time.",
    "choose_language": "Choose your language:",
    "language_set": "Language set to {lang}.",
    "choose_translation_language": "Choose your translation language:",
    "translation_language_set": "Translation language set to {lang}.",
    "choose_reciter": "Choose a reciter:",
    "reciter_set": "Reciter set to {reciter}.",
    "btn_search_reciter": "Search by name",
    "reciter_search_prompt": "Type a reciter's name to search (e.g. \"Sudais\", \"Basit\").",
    "reciter_search_no_matches": "No reciters matched that name — try again.",
    "reciter_search_results": "Search results:",
    "btn_set_reciter": "Set as my reciter",
    "reciter_inline_description": "Tap to set as your reciter",
    "tafsir_en_note": "\n\n(Tafsir is available in English only.)",
    "btn_translation": "Translation",
    "btn_tafsir": "Tafsir",
    "btn_arabic": "Arabic",
    "btn_audio": "Audio",
    "btn_previous": "Previous",
    "btn_random": "Random",
    "btn_next": "Next",
    "page_label": "Page {n} of {total}",
    "page_out_of_range": "Send a page number between 1 and {total}, for example /page 255.",
    "juz_out_of_range": "Send a juz number between 1 and {total}, for example /juz 30.",
    "sajda_list_title": "Verses of prostration (sajda):",
    "btn_ayah_view": "Ayah view",
    "btn_repeat": "Repeat",
    "reciter_group_recitation": "Reciters",
    "reciter_group_riwayah": "Riwāyah",
    "reciter_group_translation": "Meaning",
    "riwayah_warning": (
        "Note: this is the Warsh riwāyah — a different reading of the Qur'anic text "
        "from the Ḥafṣ one shown in the Arabic and translations here, so the audio "
        "will not always match the words on screen."
    ),
    "translation_audio_warning": (
        "Note: this recording is not Qur'an recitation — it is the translated meaning "
        "read aloud. Choose from the Reciters tab to hear the Arabic recitation."
    ),
    "cmd_index": "List all surahs",
    "cmd_page": "Read a mushaf page",
    "cmd_juz": "Open a juz",
    "cmd_sajda": "Verses of prostration",
    "cmd_random": "A random verse",
    "cmd_language": "Change UI language",
    "cmd_translation": "Change translation language",
    "cmd_reciter": "Change reciter",
    "cmd_about": "Sources & credits",
    "quran_name": "Qur'an",

    # --- Hifz platform ---------------------------------------------------------
    # Frozen key set for the memorization features. Every key here is documented
    # in docs/HIFZ_STRINGS.md — placeholder names and all — because 47 other
    # locales are translated from that manifest rather than from this file.
    #
    # Two house rules for anything added below:
    #   * no HTML tags. Only welcome_intro / welcome_inline / about are checked
    #     for balanced <b>, and an unbalanced tag makes Telegram reject the whole
    #     message. Plain text cannot fail that way in 48 languages.
    #   * as few placeholders as possible, and never a positional one — every
    #     placeholder is multiplied by 47 translators.

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Start a memorization plan",
    "cmd_progress": "What you have memorized",
    "cmd_check": "Test your recall",
    "cmd_forgot": "Unmark a memorized range",
    "cmd_streak": "Your daily streak",
    "cmd_leaderboard": "This week's top memorizers",
    "cmd_profile": "Your profile and settings",

    # Shared wizard controls
    "wizard_cancelled": "Cancelled.",
    "wizard_nothing_to_cancel": "There is nothing to cancel.",
    "wizard_invalid_input": "I didn't understand that. Try again, or send /cancel.",
    "ref_invalid": "That isn't a reference I recognise. Try something like 67, 67:1-8 or juz 30.",
    "btn_cancel": "Cancel",
    "btn_back": "Back",
    "btn_confirm": "Confirm",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "Mon",
    "day_tue": "Tue",
    "day_wed": "Wed",
    "day_thu": "Thu",
    "day_fri": "Fri",
    "day_sat": "Sat",
    "day_sun": "Sun",

    # Profile (B1-B3)
    "profile_title": "Your profile",
    "profile_name_set": "Name: {name}",
    "profile_name_unset": "Name: not set",
    "profile_leaderboard_on": "Leaderboard: you are listed",
    "profile_leaderboard_off": "Leaderboard: you are hidden",
    "profile_timezone_set": "Time zone: UTC{offset}",
    "profile_timezone_unset": "Time zone: not set",
    "profile_reminder_set": "Daily reminder: {time}",
    "profile_reminder_unset": "Daily reminder: off",
    "profile_plan_active": "Plan: {target} — day {day} of {total}",
    "profile_plan_none": "Plan: none yet. Start one with /memorize.",
    "btn_edit_name": "Change name",
    "btn_join_board": "Join the leaderboard",
    "btn_leave_board": "Leave the leaderboard",
    "btn_edit_timezone": "Change time zone",
    "btn_edit_reminder": "Change reminder time",
    "name_prompt": "Send the name you would like to appear under on the leaderboard.",
    "name_invalid": "Use between {min} and {max} characters.",
    "name_saved": "You will appear as {name}.",
    "board_joined": "You are on the leaderboard now.",
    "board_left": "You have been removed from the leaderboard.",
    "timezone_prompt": (
        "Pick your UTC offset. It decides when your day starts for streaks and "
        "when your daily portion arrives."
    ),
    "timezone_saved": "Time zone set to UTC{offset}.",
    "reminder_prompt": "Send the time you want your daily portion, in 24-hour form, e.g. 07:30.",
    "reminder_invalid": "Send a time in 24-hour form, e.g. 07:30.",
    "reminder_saved": "Daily reminder set for {time}.",
    "btn_reminder_off": "Turn reminders off",
    "reminder_off": "Daily reminders are off.",

    # Progress and /forgot (C3)
    "progress_title": "What you have memorized",
    "progress_surah_line": "{name}: {done}/{total} ayahs — {pct}%",
    "progress_juz_line": "Juz {n}: {pct}%",
    "progress_quran_line": "Whole Qur'an: {pct}%",
    "progress_empty": (
        "Nothing marked yet. Finish a portion and tap \"I know this by heart\", "
        "or start a plan with /memorize."
    ),
    "forgot_usage": "Send what to unmark, for example /forgot 67:5-6.",
    "forgot_done": "Unmarked {ref}.",
    "forgot_nothing": "You had not marked that as memorized.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "What would you like to memorize?",
    "btn_target_surah": "A surah",
    "btn_target_juz": "A juz",
    "btn_target_range": "A range",
    "memorize_surah_prompt": "Send the surah number, for example 67.",
    "memorize_juz_prompt": "Send the juz number, from 1 to 30.",
    "memorize_range_prompt": "Send the range, for example 67:1-68:5.",
    "memorize_choose_pace": "How much would you like to do each day?",
    "btn_pace_auto": "Choose for me",
    "memorize_pace_prompt": "Send how many ayahs a day.",
    "memorize_pace_invalid": "Send a number between {min} and {max}.",
    "memorize_choose_days": "Which days would you like to study?",
    "btn_days_daily": "Every day",
    "btn_days_weekdays": "Weekdays",
    "btn_days_custom": "Pick days",
    "memorize_days_prompt": "Tap the days you want, then confirm.",
    "memorize_preview_title": "{days} days, {start} to {end}:",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Start this plan",
    "plan_saved": "Your plan is set. The first portion arrives on {first_date}.",
    "plan_exists": "You already have a plan running. Pause or abandon it first.",
    "btn_pause_plan": "Pause plan",
    "btn_resume_plan": "Resume plan",
    "btn_abandon_plan": "Abandon plan",
    "plan_paused": "Plan paused. Resume it any time from /profile.",
    "plan_resumed": "Plan resumed.",
    "plan_abandoned": "Plan abandoned.",
    "plan_complete": "You have finished {target}. May Allah accept it from you.",
    "drill_title": "{ref} — day {day} of {total}",
    "drill_none_today": "Nothing is scheduled for today.",
    "btn_start_drill": "Start today's portion",
    "btn_know_by_heart": "✅ I know this by heart",
    "know_confirmed": "{ref} marked as memorized. You are at {pct}%.",
    "know_already": "You had already marked that one.",

    # Recall check (E2, E3)
    "check_question": "How does this continue?",
    "check_usage": "Send what to test, for example /check 67.",
    "check_correct": "Correct.",
    "check_wrong": "Not quite. It continues: {correct}",
    "check_already_today": (
        "You have already earned today's session from a recall check — test "
        "yourself as often as you like, it just will not count twice."
    ),
    "btn_check_start": "Test me",

    # Streaks (G2, G3)
    "streak_title": "Your streak",
    "streak_current": "Current streak: {n} days",
    "streak_longest": "Longest streak: {n} days",
    "streak_none": "No streak yet. Finish a portion or pass a recall check today to start one.",
    "streak_graph_caption": "The last 12 weeks",
    "streak_milestone_7": "A full week. This is where the habit starts.",
    "streak_milestone_30": "Thirty days. Consistency is now on your side.",
    "streak_milestone_100": "A hundred days. Very few people get this far.",
    "streak_milestone_365": "A whole year, every single day. May Allah preserve what you have learned.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "This week's leaderboard",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "You: {rank}. — {sessions}",
    "leaderboard_empty": "Nobody has completed a session this week yet. Be the first.",
    "leaderboard_not_opted_in": "You are not on the leaderboard. Join it from /profile.",

    # --- Phase 2: group cluster (en/ru/uz/uz-Cyrl only) ---  # phase2
    'group_added': 'As-salamu alaykum! I can run a daily memorization circle in this group. An admin, tap below to set me up.',
    'group_btn_setup': '⚙️ Set up the circle',
    'group_setup_unknown': "I don't know this group. Add me to it first, then tap the setup link there.",
    'group_setup_not_admin': 'Only an admin of that group can set me up.',
    'group_topic_prompt': 'What should I name the daily topic? Send me a name.',
    'group_topic_created': "Topic <b>{name}</b> created. I'll post there each day.",
    'group_topic_fallback': "This group has no Topics, so I'll post in the main chat instead.",
    'group_translation_prompt': 'Which translation should the daily posts use?',
    'group_board_unknown': 'That study circle no longer exists.',
    'group_board_not_member': 'You need to be a member of that group to join its board.',
    'group_board_joined': "You're on the group's weekly board now.",
    # --- Phase 2 J4/J5 ---  # phase2
    'group_target_prompt': 'What should the circle memorize? Send a surah (67), a juz (juz 30), or a range (2:1-10).',
    'group_target_invalid': 'I couldn\'t read that. Try a surah number, "juz 30", or "2:1-10".',
    'group_pace_prompt': 'How many ayahs per day?',
    'group_btn_pace_auto': 'Auto',
    'group_days_prompt': 'Which days should I post?',
    'group_btn_daily': 'Every day',
    'group_btn_weekdays': 'Weekdays',
    'group_timezone_prompt': "What's the group's UTC offset?",
    'group_post_time_prompt': 'What local time should I post each day? (e.g. 07:00)',
    'group_post_time_invalid': 'Please send a time like 07:00.',
    'group_setup_done': 'All set — {days} portions over {total} days. Members can join the weekly board here: {board_link}',
    # --- Phase 2 J6 board ---  # phase2
    'group_board_title': "📿 This week's circle",
    'group_board_row': '{rank}. {name} — {sessions}',
    'group_board_empty': 'No one has completed a session yet this week. Be the first!',
}
