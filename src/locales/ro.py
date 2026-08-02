# Romanian — Română

strings = {
    "welcome_intro": (
        "Trimite-mi un număr de sură și verset, de exemplu <b>2:255</b>, iar eu îți voi "
        "trimite acel verset din Sfântul Coran.\n\n"
        "Poți trimite și un interval precum <b>59:22-24</b> pentru o recitare audio "
        "combinată."
    ),
    "welcome_commands_header": "Comenzi:",
    "welcome_inline": (
        "Mă poți folosi în orice conversație: scrie <b>@QuranAyat_bot</b> urmat de o "
        "referință."
    ),
    "about": (
        "Acest bot îți permite să citești Sfântul Coran pe Telegram în multe "
        "limbi.\n\n"
        "Traducerile provin de la tanzil.net (vezi ATTRIBUTIONS.md pentru "
        "ediția și traducătorul fiecărei traduceri). Audio este o recitare a "
        "șeicului Mahmoud Khalil al-Husary (everyayah.com). Tafsirul este "
        "Tafsir al-Jalalayn (altafsir.com), disponibil în engleză.\n\n"
        "Schimbă limba oricând cu /language."
    ),
    "ayah_not_found": "Acest verset nu există!",
    "range_too_large": "Interval prea mare, cere cel mult {n} versete odată.",
    "choose_language": "Alege limba ta:",
    "language_set": "Limba a fost setată pe {lang}.",
    "choose_translation_language": "Alegeți limba traducerii:",
    "translation_language_set": "Limba traducerii a fost setată la {lang}.",
    "choose_reciter": "Alegeți un recitator:",
    "reciter_set": "Recitatorul a fost setat la {reciter}.",
    "btn_search_reciter": "Caută după nume",
    "reciter_search_prompt": "Scrieți numele unui recitator pentru a căuta (ex. «Sudais», «Abdul Basit»).",
    "reciter_search_no_matches": "Niciun recitator nu corespunde acelui nume — încercați din nou.",
    "reciter_search_results": "Rezultatele căutării:",
    "btn_set_reciter": "Setează ca recitatorul meu",
    "reciter_inline_description": "Atingeți pentru a-l seta ca recitatorul dvs.",
    "tafsir_en_note": "\n\n(Tafsirul este disponibil doar în engleză.)",
    "btn_translation": "Traducere",
    "btn_tafsir": "Tafsir",
    "btn_arabic": "Arabă",
    "btn_audio": "Audio",
    "btn_previous": "Anterior",
    "btn_random": "Aleatoriu",
    "btn_next": "Următor",
    "page_label": "Pagina {n} din {total}",
    "page_out_of_range": "Trimite un număr de pagină între 1 și {total}, de exemplu /page 255.",
    "juz_out_of_range": "Trimite un număr de juz între 1 și {total}, de exemplu /juz 30.",
    "sajda_list_title": "Versete de prosternare (sajda):",
    "btn_ayah_view": "Vizualizare pe versete",
    "btn_repeat": "Repetă",
    "reciter_group_recitation": "Recitatori",
    "reciter_group_riwayah": "Riwāya",
    "reciter_group_translation": "Sens",
    "riwayah_warning": "Notă: aceasta este riwāya lui Warsh — o citire a textului coranic diferită de cea a lui Hafs afișată aici în textul arab și în traduceri, așa că sunetul nu va corespunde întotdeauna cuvintelor de pe ecran.",
    "translation_audio_warning": "Notă: această înregistrare nu este recitare a Coranului, ci citirea cu voce tare a sensului tradus. Alege din fila «Recitatori» pentru a asculta recitarea în arabă.",
    "cmd_index": "Lista tuturor surelor",
    "cmd_page": "Citește o pagină din mushaf",
    "cmd_juz": "Deschide un juz",
    "cmd_sajda": "Versete de prosternare",
    "cmd_random": "Un verset aleatoriu",
    "cmd_language": "Schimbă limba",
    "cmd_translation": "Schimbă limba traducerii",
    "cmd_reciter": "Schimbă recitatorul",
    "cmd_about": "Surse și mulțumiri",
    "quran_name": "Coran",

    # --- Hifz platform ---------------------------------------------------------

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Începe un plan de memorare",
    "cmd_progress": "Ce ai memorat",
    "cmd_check": "Testează-ți memoria",
    "cmd_forgot": "Anulează un interval memorat",
    "cmd_streak": "Seria ta zilnică",
    "cmd_leaderboard": "Cei mai buni din această săptămână",
    "cmd_profile": "Profilul și setările tale",

    # Shared wizard controls
    "wizard_cancelled": "Anulat.",
    "wizard_nothing_to_cancel": "Nu este nimic de anulat.",
    "wizard_invalid_input": "Nu am înțeles. Încearcă din nou sau trimite /cancel.",
    "ref_invalid": "Nu recunosc această referință. Încearcă ceva precum 67, 67:1-8 sau juz 30.",
    "btn_cancel": "Anulează",
    "btn_back": "Înapoi",
    "btn_confirm": "Confirmă",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "Lun",
    "day_tue": "Mar",
    "day_wed": "Mie",
    "day_thu": "Joi",
    "day_fri": "Vin",
    "day_sat": "Sâm",
    "day_sun": "Dum",

    # Profile (B1-B3)
    "profile_title": "Profilul tău",
    "profile_name_set": "Nume: {name}",
    "profile_name_unset": "Nume: nesetat",
    "profile_leaderboard_on": "Clasament: ești afișat",
    "profile_leaderboard_off": "Clasament: ești ascuns",
    "profile_timezone_set": "Fus orar: UTC{offset}",
    "profile_timezone_unset": "Fus orar: nesetat",
    "profile_reminder_set": "Reamintire zilnică: {time}",
    "profile_reminder_unset": "Reamintire zilnică: oprită",
    "profile_plan_active": "Plan: {target} — ziua {day} din {total}",
    "profile_plan_none": "Plan: niciunul încă. Începe unul cu /memorize.",
    "btn_edit_name": "Schimbă numele",
    "btn_join_board": "Intră în clasament",
    "btn_leave_board": "Ieși din clasament",
    "btn_edit_timezone": "Schimbă fusul orar",
    "btn_edit_reminder": "Schimbă ora reamintirii",
    "name_prompt": "Trimite numele sub care vrei să apari în clasament.",
    "name_invalid": "Folosește între {min} și {max} caractere.",
    "name_saved": "Vei apărea ca {name}.",
    "board_joined": "Ești acum în clasament.",
    "board_left": "Ai fost scos din clasament.",
    "timezone_prompt": (
        "Alege-ți decalajul față de UTC. El stabilește când începe ziua ta pentru "
        "serii și când sosește porția zilnică."
    ),
    "timezone_saved": "Fusul orar a fost setat la UTC{offset}.",
    "reminder_prompt": "Trimite ora la care vrei porția zilnică, în format de 24 de ore, de ex. 07:30.",
    "reminder_invalid": "Trimite o oră în format de 24 de ore, de ex. 07:30.",
    "reminder_saved": "Reamintirea zilnică a fost setată la {time}.",
    "btn_reminder_off": "Oprește reamintirile",
    "reminder_off": "Reamintirile zilnice sunt oprite.",

    # Progress and /forgot (C3)
    "progress_title": "Ce ai memorat",
    "progress_surah_line": "{name}: {done}/{total} versete — {pct}%",
    "progress_juz_line": "Juz {n}: {pct}%",
    "progress_quran_line": "Întregul Coran: {pct}%",
    "progress_empty": (
        "Încă nu ai marcat nimic. Termină o porție și apasă «Știu pe de rost» sau "
        "începe un plan cu /memorize."
    ),
    "forgot_usage": "Trimite ce să anulez, de exemplu /forgot 67:5-6.",
    "forgot_done": "Marcaj anulat: {ref}.",
    "forgot_nothing": "Nu marcaseși asta ca memorată.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "Ce ai vrea să memorezi?",
    "btn_target_surah": "O sură",
    "btn_target_juz": "Un juz",
    "btn_target_range": "Un interval",
    "memorize_surah_prompt": "Trimite numărul surei, de exemplu 67.",
    "memorize_juz_prompt": "Trimite numărul juzului, de la 1 la 30.",
    "memorize_range_prompt": "Trimite intervalul, de exemplu 67:1-68:5.",
    "memorize_choose_pace": "Cât vrei să faci în fiecare zi?",
    "btn_pace_auto": "Alege tu pentru mine",
    "memorize_pace_prompt": "Trimite câte versete pe zi.",
    "memorize_pace_invalid": "Trimite un număr între {min} și {max}.",
    "memorize_choose_days": "În ce zile vrei să studiezi?",
    "btn_days_daily": "În fiecare zi",
    "btn_days_weekdays": "Zile lucrătoare",
    "btn_days_custom": "Alege zilele",
    "memorize_days_prompt": "Atinge zilele dorite, apoi confirmă.",
    "memorize_preview_title": "Număr de zile: {days}, de la {start} la {end}:",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Începe acest plan",
    "plan_saved": "Planul este gata. Prima porție sosește pe {first_date}.",
    "plan_exists": "Ai deja un plan în desfășurare. Întrerupe-l sau renunță la el mai întâi.",
    "btn_pause_plan": "Întrerupe planul",
    "btn_resume_plan": "Reia planul",
    "btn_abandon_plan": "Renunță la plan",
    "plan_paused": "Plan întrerupt. Îl poți relua oricând din /profile.",
    "plan_resumed": "Planul a fost reluat.",
    "plan_abandoned": "Ai renunțat la plan.",
    "plan_complete": "Ai terminat {target}. Fie ca Allah să primească asta de la tine.",
    "drill_title": "{ref} — ziua {day} din {total}",
    "drill_none_today": "Pentru azi nu este programat nimic.",
    "btn_start_drill": "Începe porția de azi",
    "btn_know_by_heart": "✅ Știu pe de rost",
    "know_confirmed": "{ref} a fost marcat ca memorat. Ești la {pct}%.",
    "know_already": "Asta era deja marcată.",

    # Recall check (E2, E3)
    "check_question": "Cum continuă?",
    "check_usage": "Trimite ce să testez, de exemplu /check 67.",
    "check_correct": "Corect.",
    "check_wrong": "Nu chiar. Continuă așa: {correct}",
    "check_already_today": (
        "Sesiunea de azi ți-a fost deja acordată printr-o verificare a memoriei — "
        "testează-te cât vrei, doar că nu se va număra de două ori."
    ),
    "btn_check_start": "Testează-mă",

    # Streaks (G2, G3)
    "streak_title": "Seria ta",
    "streak_current": "Serie curentă, zile: {n}",
    "streak_longest": "Cea mai lungă serie, zile: {n}",
    "streak_none": "Încă nu ai o serie. Termină azi o porție sau treci o verificare a memoriei ca să o începi.",
    "streak_graph_caption": "Ultimele 12 săptămâni",
    "streak_milestone_7": "O săptămână întreagă. De aici începe obiceiul.",
    "streak_milestone_30": "Treizeci de zile. Consecvența este acum de partea ta.",
    "streak_milestone_100": "O sută de zile. Foarte puțini ajung atât de departe.",
    "streak_milestone_365": "Un an întreg, zi de zi. Fie ca Allah să păstreze ceea ce ai învățat.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "Clasamentul acestei săptămâni",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "Tu: {rank}. — {sessions}",
    "leaderboard_empty": "Nimeni nu a terminat o sesiune săptămâna aceasta. Fii primul.",
    "leaderboard_not_opted_in": "Nu ești în clasament. Alătură-te din /profile.",
}
