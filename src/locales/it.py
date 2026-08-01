# Italian — Italiano

strings = {
    "welcome_intro": (
        "Inviami un numero di sura e versetto, ad esempio <b>2:255</b>, e ti risponderò "
        "con quel versetto del Sacro Corano.\n\n"
        "Puoi anche inviare un intervallo come <b>59:22-24</b> per una recitazione audio "
        "combinata."
    ),
    "welcome_commands_header": "Comandi:",
    "welcome_inline": (
        "Puoi usarmi in qualsiasi chat: digita <b>@QuranAyat_bot</b> seguito da un "
        "riferimento."
    ),
    "about": (
        "Questo bot ti permette di esplorare il Sacro Corano su Telegram in "
        "molte lingue.\n\n"
        "Le traduzioni provengono da tanzil.net (vedi ATTRIBUTIONS.md per "
        "l'edizione e il traduttore di ogni traduzione). L'audio è una "
        "recitazione dello sceicco Mahmoud Khalil al-Husary (everyayah.com). Il "
        "tafsir è il Tafsir al-Jalalayn (altafsir.com), disponibile in inglese.\n\n"
        "Cambia lingua in qualsiasi momento con /language."
    ),
    "ayah_not_found": "Questo versetto non esiste!",
    "range_too_large": "Intervallo troppo grande, richiedi al massimo {n} versetti alla volta.",
    "choose_language": "Scegli la tua lingua:",
    "language_set": "Lingua impostata su {lang}.",
    "choose_translation_language": "Scegli la lingua della traduzione:",
    "translation_language_set": "Lingua della traduzione impostata su {lang}.",
    "choose_reciter": "Scegli un recitatore:",
    "reciter_set": "Recitatore impostato su {reciter}.",
    "btn_search_reciter": "Cerca per nome",
    "reciter_search_prompt": "Scrivi il nome di un recitatore per cercarlo (es. «Sudais», «Abdul Basit»).",
    "reciter_search_no_matches": "Nessun recitatore corrisponde a quel nome — riprova.",
    "reciter_search_results": "Risultati della ricerca:",
    "btn_set_reciter": "Imposta come mio recitatore",
    "reciter_inline_description": "Tocca per impostarlo come tuo recitatore",
    "tafsir_en_note": "\n\n(Il tafsir è disponibile solo in inglese.)",
    "btn_translation": "Traduzione",
    "btn_tafsir": "Tafsir",
    "btn_arabic": "Arabo",
    "btn_audio": "Audio",
    "btn_previous": "Precedente",
    "btn_random": "Casuale",
    "btn_next": "Successivo",
    "page_label": "Pagina {n} di {total}",
    "page_out_of_range": "Invia un numero di pagina tra 1 e {total}, per esempio /page 255.",
    "juz_out_of_range": "Invia un numero di juz tra 1 e {total}, per esempio /juz 30.",
    "sajda_list_title": "Versetti di prosternazione (sajda):",
    "btn_ayah_view": "Vista per versetti",
    "btn_repeat": "Ripeti",
    "reciter_group_recitation": "Recitatori",
    "reciter_group_riwayah": "Riwāya",
    "reciter_group_translation": "Significato",
    "riwayah_warning": "Nota: questa è la riwāya di Warsh — una lettura del testo coranico diversa da quella di Hafs mostrata qui nel testo arabo e nelle traduzioni, perciò l'audio non corrisponderà sempre alle parole sullo schermo.",
    "translation_audio_warning": "Nota: questa registrazione non è recitazione del Corano, ma la lettura ad alta voce del significato tradotto. Scegli dalla scheda «Recitatori» per ascoltare la recitazione in arabo.",
    "cmd_index": "Elenco di tutte le sure",
    "cmd_page": "Leggi una pagina del mushaf",
    "cmd_juz": "Apri un juz",
    "cmd_sajda": "Versetti di prosternazione",
    "cmd_random": "Un versetto casuale",
    "cmd_language": "Cambia lingua",
    "cmd_translation": "Cambia la lingua della traduzione",
    "cmd_reciter": "Cambia recitatore",
    "cmd_about": "Fonti e ringraziamenti",
    "quran_name": "Corano",

    # --- Hifz platform ---------------------------------------------------------

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Avvia un piano di hifz",
    "cmd_progress": "Ciò che hai memorizzato",
    "cmd_check": "Metti alla prova la memoria",
    "cmd_forgot": "Rimuovi un intervallo memorizzato",
    "cmd_streak": "La tua serie quotidiana",
    "cmd_leaderboard": "I migliori di questa settimana",
    "cmd_profile": "Il tuo profilo e le impostazioni",

    # Shared wizard controls
    "wizard_cancelled": "Annullato.",
    "wizard_nothing_to_cancel": "Non c'è nulla da annullare.",
    "wizard_invalid_input": "Non ho capito. Riprova, oppure invia /cancel.",
    "ref_invalid": "Questo riferimento non lo riconosco. Prova con 67, 67:1-8 o juz 30.",
    "btn_cancel": "Annulla",
    "btn_back": "Indietro",
    "btn_confirm": "Conferma",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "lun",
    "day_tue": "mar",
    "day_wed": "mer",
    "day_thu": "gio",
    "day_fri": "ven",
    "day_sat": "sab",
    "day_sun": "dom",

    # Profile (B1-B3)
    "profile_title": "Il tuo profilo",
    "profile_name_set": "Nome: {name}",
    "profile_name_unset": "Nome: non impostato",
    "profile_leaderboard_on": "Classifica: sei in elenco",
    "profile_leaderboard_off": "Classifica: sei nascosto",
    "profile_timezone_set": "Fuso orario: UTC{offset}",
    "profile_timezone_unset": "Fuso orario: non impostato",
    "profile_reminder_set": "Promemoria giornaliero: {time}",
    "profile_reminder_unset": "Promemoria giornaliero: disattivato",
    "profile_plan_active": "Piano: {target} — giorno {day} di {total}",
    "profile_plan_none": "Piano: ancora nessuno. Avviane uno con /memorize.",
    "btn_edit_name": "Cambia nome",
    "btn_join_board": "Entra in classifica",
    "btn_leave_board": "Esci dalla classifica",
    "btn_edit_timezone": "Cambia fuso orario",
    "btn_edit_reminder": "Cambia ora promemoria",
    "name_prompt": "Invia il nome con cui vuoi comparire in classifica.",
    "name_invalid": "Usa tra {min} e {max} caratteri.",
    "name_saved": "Comparirai come {name}.",
    "board_joined": "Ora sei in classifica.",
    "board_left": "Sei stato rimosso dalla classifica.",
    "timezone_prompt": (
        "Scegli il tuo scarto rispetto a UTC. Decide quando inizia la tua "
        "giornata per le serie e quando arriva la porzione quotidiana."
    ),
    "timezone_saved": "Fuso orario impostato su UTC{offset}.",
    "reminder_prompt": "Invia l'ora a cui vuoi la porzione quotidiana, in formato 24 ore, ad esempio 07:30.",
    "reminder_invalid": "Invia un'ora in formato 24 ore, ad esempio 07:30.",
    "reminder_saved": "Promemoria giornaliero impostato alle {time}.",
    "btn_reminder_off": "Disattiva promemoria",
    "reminder_off": "I promemoria giornalieri sono disattivati.",

    # Progress and /forgot (C3)
    "progress_title": "Ciò che hai memorizzato",
    "progress_surah_line": "{name}: {done}/{total} versetti — {pct}%",
    "progress_juz_line": "Juz {n}: {pct}%",
    "progress_quran_line": "Corano intero: {pct}%",
    "progress_empty": (
        "Non hai ancora segnato nulla. Completa una porzione e tocca "
        "«Lo so a memoria», oppure avvia un piano con /memorize."
    ),
    "forgot_usage": "Invia cosa vuoi rimuovere, ad esempio /forgot 67:5-6.",
    "forgot_done": "{ref} rimosso.",
    "forgot_nothing": "Non l'avevi segnato come memorizzato.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "Che cosa vuoi memorizzare?",
    "btn_target_surah": "Una sura",
    "btn_target_juz": "Un juz",
    "btn_target_range": "Un intervallo",
    "memorize_surah_prompt": "Invia il numero della sura, ad esempio 67.",
    "memorize_juz_prompt": "Invia il numero del juz, da 1 a 30.",
    "memorize_range_prompt": "Invia l'intervallo, ad esempio 67:1-68:5.",
    "memorize_choose_pace": "Quanto vuoi fare ogni giorno?",
    "btn_pace_auto": "Scegli tu per me",
    "memorize_pace_prompt": "Invia quanti versetti al giorno.",
    "memorize_pace_invalid": "Invia un numero tra {min} e {max}.",
    "memorize_choose_days": "In quali giorni vuoi studiare?",
    "btn_days_daily": "Tutti i giorni",
    "btn_days_weekdays": "Giorni feriali",
    "btn_days_custom": "Scegli i giorni",
    "memorize_days_prompt": "Tocca i giorni che vuoi, poi conferma.",
    "memorize_preview_title": "{days} giorni, dal {start} al {end}:",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Avvia questo piano",
    "plan_saved": "Il tuo piano è pronto. La prima porzione arriva il {first_date}.",
    "plan_exists": "Hai già un piano in corso. Mettilo in pausa o abbandonalo prima.",
    "btn_pause_plan": "Metti in pausa",
    "btn_resume_plan": "Riprendi il piano",
    "btn_abandon_plan": "Abbandona il piano",
    "plan_paused": "Piano in pausa. Riprendilo quando vuoi da /profile.",
    "plan_resumed": "Piano ripreso.",
    "plan_abandoned": "Piano abbandonato.",
    "plan_complete": "Hai completato {target}. Che Allah te lo accetti.",
    "drill_title": "{ref} — giorno {day} di {total}",
    "drill_none_today": "Per oggi non è previsto nulla.",
    "btn_start_drill": "Porzione di oggi",
    "btn_know_by_heart": "✅ Lo so a memoria",
    "know_confirmed": "{ref} segnato come memorizzato. Sei al {pct}%.",
    "know_already": "L'avevi già segnato.",

    # Recall check (E2, E3)
    "check_question": "Come prosegue?",
    "check_usage": "Invia cosa vuoi verificare, ad esempio /check 67.",
    "check_correct": "Corretto.",
    "check_wrong": "Non proprio. Prosegue così: {correct}",
    "check_already_today": (
        "Hai già ottenuto la sessione di oggi con una verifica di memoria — "
        "mettiti alla prova quanto vuoi, semplicemente non conterà due volte."
    ),
    "btn_check_start": "Mettimi alla prova",

    # Streaks (G2, G3)
    "streak_title": "La tua serie",
    "streak_current": "Serie attuale: {n}",
    "streak_longest": "Serie più lunga: {n}",
    "streak_none": "Ancora nessuna serie. Completa una porzione oggi o supera una verifica di memoria per iniziarne una.",
    "streak_graph_caption": "Le ultime 12 settimane",
    "streak_milestone_7": "Una settimana intera. È qui che nasce l'abitudine.",
    "streak_milestone_30": "Trenta giorni. Ora la costanza è dalla tua parte.",
    "streak_milestone_100": "Cento giorni. Pochissimi arrivano fin qui.",
    "streak_milestone_365": "Un anno intero, ogni singolo giorno. Che Allah preservi ciò che hai imparato.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "La classifica di questa settimana",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "Tu: {rank}. — {sessions}",
    "leaderboard_empty": "Questa settimana nessuno ha ancora completato una sessione. Sii il primo.",
    "leaderboard_not_opted_in": "Non sei in classifica. Entraci da /profile.",
}
