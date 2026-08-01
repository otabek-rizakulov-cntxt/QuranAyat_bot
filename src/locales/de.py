# German — Deutsch

strings = {
    "welcome_intro": (
        "Sende mir eine Sure und Versnummer, zum Beispiel <b>2:255</b>, und ich schicke "
        "dir diesen Vers aus dem Heiligen Koran.\n\n"
        "Du kannst auch einen Bereich wie <b>59:22-24</b> senden, um eine zusammengefügte "
        "Audio-Rezitation zu erhalten."
    ),
    "welcome_commands_header": "Befehle:",
    "welcome_inline": (
        "Du kannst mich in jedem Chat verwenden: Tippe <b>@QuranAyat_bot</b> gefolgt von "
        "einer Versangabe."
    ),
    "about": (
        "Mit diesem Bot kannst du den Heiligen Koran auf Telegram in vielen "
        "Sprachen lesen.\n\n"
        "Die Übersetzungen stammen von tanzil.net (siehe ATTRIBUTIONS.md für "
        "Ausgabe und Übersetzer jeder Übersetzung). Die Audioaufnahme ist eine "
        "Rezitation von Scheich Mahmud Chalil al-Husari (everyayah.com). Der "
        "Tafsir ist Tafsir al-Dschalalain (altafsir.com), verfügbar auf Englisch.\n\n"
        "Die Sprache kannst du jederzeit mit /language ändern."
    ),
    "ayah_not_found": "Dieser Vers existiert nicht!",
    "range_too_large": "Bereich zu groß, bitte höchstens {n} Verse auf einmal anfragen.",
    "choose_language": "Wähle deine Sprache:",
    "language_set": "Sprache auf {lang} gestellt.",
    "choose_translation_language": "Wähle die Übersetzungssprache:",
    "translation_language_set": "Übersetzungssprache auf {lang} gesetzt.",
    "choose_reciter": "Wähle einen Rezitator:",
    "reciter_set": "Rezitator auf {reciter} gesetzt.",
    "btn_search_reciter": "Nach Namen suchen",
    "reciter_search_prompt": "Gib den Namen eines Rezitators ein (z. B. „Sudais“, „Abdul Basit“).",
    "reciter_search_no_matches": "Kein Rezitator mit diesem Namen gefunden — versuche es erneut.",
    "reciter_search_results": "Suchergebnisse:",
    "btn_set_reciter": "Als meinen Rezitator festlegen",
    "reciter_inline_description": "Tippe, um ihn als deinen Rezitator festzulegen",
    "tafsir_en_note": "\n\n(Der Tafsir ist nur auf Englisch verfügbar.)",
    "btn_translation": "Übersetzung",
    "btn_tafsir": "Tafsir",
    "btn_arabic": "Arabisch",
    "btn_audio": "Audio",
    "btn_previous": "Zurück",
    "btn_random": "Zufällig",
    "btn_next": "Weiter",
    "page_label": "Seite {n} von {total}",
    "page_out_of_range": "Sende eine Seitenzahl zwischen 1 und {total}, zum Beispiel /page 255.",
    "juz_out_of_range": "Sende eine Dschuz-Nummer zwischen 1 und {total}, zum Beispiel /juz 30.",
    "sajda_list_title": "Verse der Niederwerfung (Sadschda):",
    "btn_ayah_view": "Vers-Ansicht",
    "btn_repeat": "Wiederholen",
    "reciter_group_recitation": "Rezitatoren",
    "reciter_group_riwayah": "Riwāya",
    "reciter_group_translation": "Bedeutung",
    "riwayah_warning": "Hinweis: Dies ist die Warsch-Riwāya — eine Lesart des koranischen Textes, die sich von der hier im arabischen Text und in den Übersetzungen gezeigten Hafs-Lesart unterscheidet. Das Audio stimmt daher nicht immer mit den Worten auf dem Bildschirm überein.",
    "translation_audio_warning": "Hinweis: Diese Aufnahme ist keine Koranrezitation, sondern die vorgelesene übersetzte Bedeutung. Wähle aus dem Reiter «Rezitatoren», um die arabische Rezitation zu hören.",
    "cmd_index": "Alle Suren auflisten",
    "cmd_page": "Eine Mushaf-Seite lesen",
    "cmd_juz": "Einen Dschuz öffnen",
    "cmd_sajda": "Verse der Niederwerfung",
    "cmd_random": "Ein zufälliger Vers",
    "cmd_language": "Sprache ändern",
    "cmd_translation": "Übersetzungssprache ändern",
    "cmd_reciter": "Rezitator ändern",
    "cmd_about": "Quellen und Danksagungen",
    "quran_name": "Koran",

    # --- Hifz platform ---------------------------------------------------------

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Einen Hifz-Plan starten",
    "cmd_progress": "Was du auswendig kannst",
    "cmd_check": "Dein Gedächtnis testen",
    "cmd_forgot": "Eine Markierung entfernen",
    "cmd_streak": "Deine tägliche Serie",
    "cmd_leaderboard": "Die Besten dieser Woche",
    "cmd_profile": "Dein Profil und deine Einstellungen",

    # Shared wizard controls
    "wizard_cancelled": "Abgebrochen.",
    "wizard_nothing_to_cancel": "Es gibt nichts abzubrechen.",
    "wizard_invalid_input": "Das habe ich nicht verstanden. Versuch es erneut oder sende /cancel.",
    "ref_invalid": "Diese Versangabe kenne ich nicht. Versuche etwas wie 67, 67:1-8 oder juz 30.",
    "btn_cancel": "Abbrechen",
    "btn_back": "Zurück",
    "btn_confirm": "Bestätigen",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "Mo",
    "day_tue": "Di",
    "day_wed": "Mi",
    "day_thu": "Do",
    "day_fri": "Fr",
    "day_sat": "Sa",
    "day_sun": "So",

    # Profile (B1-B3)
    "profile_title": "Dein Profil",
    "profile_name_set": "Name: {name}",
    "profile_name_unset": "Name: nicht gesetzt",
    "profile_leaderboard_on": "Rangliste: du bist gelistet",
    "profile_leaderboard_off": "Rangliste: du bist ausgeblendet",
    "profile_timezone_set": "Zeitzone: UTC{offset}",
    "profile_timezone_unset": "Zeitzone: nicht gesetzt",
    "profile_reminder_set": "Tägliche Erinnerung: {time}",
    "profile_reminder_unset": "Tägliche Erinnerung: aus",
    "profile_plan_active": "Plan: {target} — Tag {day} von {total}",
    "profile_plan_none": "Plan: noch keiner. Starte einen mit /memorize.",
    "btn_edit_name": "Namen ändern",
    "btn_join_board": "Rangliste beitreten",
    "btn_leave_board": "Rangliste verlassen",
    "btn_edit_timezone": "Zeitzone ändern",
    "btn_edit_reminder": "Erinnerung ändern",
    "name_prompt": "Sende den Namen, unter dem du in der Rangliste erscheinen möchtest.",
    "name_invalid": "Verwende zwischen {min} und {max} Zeichen.",
    "name_saved": "Du erscheinst als {name}.",
    "board_joined": "Du stehst jetzt in der Rangliste.",
    "board_left": "Du wurdest aus der Rangliste entfernt.",
    "timezone_prompt": (
        "Wähle deinen UTC-Versatz. Er bestimmt, wann dein Tag für die Serie "
        "beginnt und wann deine Tagesportion kommt."
    ),
    "timezone_saved": "Zeitzone auf UTC{offset} gesetzt.",
    "reminder_prompt": "Sende die Uhrzeit für deine Tagesportion im 24-Stunden-Format, z. B. 07:30.",
    "reminder_invalid": "Sende eine Uhrzeit im 24-Stunden-Format, z. B. 07:30.",
    "reminder_saved": "Tägliche Erinnerung auf {time} gesetzt.",
    "btn_reminder_off": "Erinnerungen aus",
    "reminder_off": "Tägliche Erinnerungen sind aus.",

    # Progress and /forgot (C3)
    "progress_title": "Was du auswendig kannst",
    "progress_surah_line": "{name}: {done}/{total} Verse — {pct} %",
    "progress_juz_line": "Dschuz {n}: {pct} %",
    "progress_quran_line": "Ganzer Koran: {pct} %",
    "progress_empty": (
        "Noch nichts markiert. Schließe eine Portion ab und tippe auf "
        "„Das kann ich auswendig“, oder starte einen Plan mit /memorize."
    ),
    "forgot_usage": "Sende, was nicht mehr markiert sein soll, zum Beispiel /forgot 67:5-6.",
    "forgot_done": "{ref} ist nicht mehr markiert.",
    "forgot_nothing": "Das hattest du nicht als auswendig markiert.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "Was möchtest du auswendig lernen?",
    "btn_target_surah": "Eine Sure",
    "btn_target_juz": "Ein Dschuz",
    "btn_target_range": "Ein Bereich",
    "memorize_surah_prompt": "Sende die Surennummer, zum Beispiel 67.",
    "memorize_juz_prompt": "Sende die Dschuz-Nummer, von 1 bis 30.",
    "memorize_range_prompt": "Sende den Bereich, zum Beispiel 67:1-68:5.",
    "memorize_choose_pace": "Wie viel möchtest du täglich schaffen?",
    "btn_pace_auto": "Für mich wählen",
    "memorize_pace_prompt": "Sende, wie viele Verse pro Tag.",
    "memorize_pace_invalid": "Sende eine Zahl zwischen {min} und {max}.",
    "memorize_choose_days": "An welchen Tagen möchtest du lernen?",
    "btn_days_daily": "Jeden Tag",
    "btn_days_weekdays": "Wochentags",
    "btn_days_custom": "Tage wählen",
    "memorize_days_prompt": "Tippe die gewünschten Tage an und bestätige dann.",
    "memorize_preview_title": "{days} Tage, {start} bis {end}:",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Plan starten",
    "plan_saved": "Dein Plan steht. Die erste Portion kommt am {first_date}.",
    "plan_exists": "Du hast schon einen laufenden Plan. Pausiere oder verwirf ihn zuerst.",
    "btn_pause_plan": "Plan pausieren",
    "btn_resume_plan": "Plan fortsetzen",
    "btn_abandon_plan": "Plan verwerfen",
    "plan_paused": "Plan pausiert. Du kannst ihn jederzeit über /profile fortsetzen.",
    "plan_resumed": "Plan fortgesetzt.",
    "plan_abandoned": "Plan verworfen.",
    "plan_complete": "Du hast {target} abgeschlossen. Möge Allah es von dir annehmen.",
    "drill_title": "{ref} — Tag {day} von {total}",
    "drill_none_today": "Für heute ist nichts geplant.",
    "btn_start_drill": "Heutige Portion",
    "btn_know_by_heart": "✅ Das kann ich auswendig",
    "know_confirmed": "{ref} als auswendig markiert. Du bist bei {pct} %.",
    "know_already": "Das hattest du schon markiert.",

    # Recall check (E2, E3)
    "check_question": "Wie geht es weiter?",
    "check_usage": "Sende, was geprüft werden soll, zum Beispiel /check 67.",
    "check_correct": "Richtig.",
    "check_wrong": "Nicht ganz. Es geht weiter: {correct}",
    "check_already_today": (
        "Die heutige Einheit hast du schon mit einer Gedächtnisprüfung verdient — "
        "prüfe dich, so oft du magst, es zählt nur nicht doppelt."
    ),
    "btn_check_start": "Prüf mich",

    # Streaks (G2, G3)
    "streak_title": "Deine Serie",
    "streak_current": "Aktuelle Serie: {n}",
    "streak_longest": "Längste Serie: {n}",
    "streak_none": "Noch keine Serie. Schließe heute eine Portion ab oder bestehe eine Gedächtnisprüfung, um eine zu starten.",
    "streak_graph_caption": "Die letzten 12 Wochen",
    "streak_milestone_7": "Eine ganze Woche. Hier beginnt die Gewohnheit.",
    "streak_milestone_30": "Dreißig Tage. Die Beständigkeit ist jetzt auf deiner Seite.",
    "streak_milestone_100": "Hundert Tage. Nur sehr wenige kommen so weit.",
    "streak_milestone_365": "Ein ganzes Jahr, jeden einzelnen Tag. Möge Allah bewahren, was du gelernt hast.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "Die Rangliste dieser Woche",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "Du: {rank}. — {sessions}",
    "leaderboard_empty": "Diese Woche hat noch niemand eine Einheit abgeschlossen. Mach du den Anfang.",
    "leaderboard_not_opted_in": "Du stehst nicht in der Rangliste. Tritt ihr über /profile bei.",
}
