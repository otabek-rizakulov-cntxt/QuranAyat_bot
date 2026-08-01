# Dutch — Nederlands

strings = {
    "welcome_intro": (
        "Stuur me een soera- en aya-nummer, bijvoorbeeld <b>2:255</b>, dan stuur ik je "
        "dat vers uit de Heilige Koran.\n\n"
        "Je kunt ook een bereik zoals <b>59:22-24</b> sturen voor een gecombineerde "
        "audiorecitatie."
    ),
    "welcome_commands_header": "Commando's:",
    "welcome_inline": (
        "Je kunt me in elke chat gebruiken: typ <b>@QuranAyat_bot</b> gevolgd door een "
        "verwijzing."
    ),
    "about": (
        "Met deze bot kun je de Heilige Koran op Telegram in veel talen lezen.\n\n"
        "De vertalingen komen van tanzil.net (zie ATTRIBUTIONS.md voor de "
        "editie en vertaler van elke vertaling). De audio is een recitatie van "
        "sjeik Mahmoud Khalil al-Husary (everyayah.com). De tafsir is Tafsir "
        "al-Jalalayn (altafsir.com), beschikbaar in het Engels.\n\n"
        "Wijzig de taal op elk moment met /language."
    ),
    "ayah_not_found": "Dit vers bestaat niet!",
    "range_too_large": "Bereik te groot, vraag maximaal {n} verzen tegelijk aan.",
    "choose_language": "Kies je taal:",
    "language_set": "Taal ingesteld op {lang}.",
    "choose_translation_language": "Kies de vertaaltaal:",
    "translation_language_set": "Vertaaltaal ingesteld op {lang}.",
    "choose_reciter": "Kies een reciteerder:",
    "reciter_set": "Reciteerder ingesteld op {reciter}.",
    "btn_search_reciter": "Zoeken op naam",
    "reciter_search_prompt": "Typ de naam van een reciteerder om te zoeken (bijv. «Sudais», «Abdul Basit»).",
    "reciter_search_no_matches": "Geen reciteerder gevonden met die naam — probeer het opnieuw.",
    "reciter_search_results": "Zoekresultaten:",
    "btn_set_reciter": "Instellen als mijn reciteerder",
    "reciter_inline_description": "Tik om als jouw reciteerder in te stellen",
    "tafsir_en_note": "\n\n(De tafsir is alleen in het Engels beschikbaar.)",
    "btn_translation": "Vertaling",
    "btn_tafsir": "Tafsir",
    "btn_arabic": "Arabisch",
    "btn_audio": "Audio",
    "btn_previous": "Vorige",
    "btn_random": "Willekeurig",
    "btn_next": "Volgende",
    "page_label": "Pagina {n} van {total}",
    "page_out_of_range": "Stuur een paginanummer tussen 1 en {total}, bijvoorbeeld /page 255.",
    "juz_out_of_range": "Stuur een djuz-nummer tussen 1 en {total}, bijvoorbeeld /juz 30.",
    "sajda_list_title": "Verzen van neerknieling (sadjda):",
    "btn_ayah_view": "Versweergave",
    "btn_repeat": "Herhalen",
    "reciter_group_recitation": "Reciteurs",
    "reciter_group_riwayah": "Riwāya",
    "reciter_group_translation": "Betekenis",
    "riwayah_warning": "Let op: dit is de Warsh-riwāya — een lezing van de Koraantekst die verschilt van de Hafs-lezing die hier in de Arabische tekst en de vertalingen wordt getoond, dus de audio komt niet altijd overeen met de woorden op het scherm.",
    "translation_audio_warning": "Let op: deze opname is geen Koranrecitatie, maar de hardop voorgelezen vertaalde betekenis. Kies uit het tabblad «Reciteurs» om de Arabische recitatie te horen.",
    "cmd_index": "Alle soera's weergeven",
    "cmd_page": "Een moshaf-pagina lezen",
    "cmd_juz": "Een djuz openen",
    "cmd_sajda": "Verzen van neerknieling",
    "cmd_random": "Een willekeurig vers",
    "cmd_language": "Taal wijzigen",
    "cmd_translation": "Vertaaltaal wijzigen",
    "cmd_reciter": "Reciteerder wijzigen",
    "cmd_about": "Bronnen en dankwoord",
    "quran_name": "Koran",

    # --- Hifz platform ---------------------------------------------------------

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Een hifz-plan starten",
    "cmd_progress": "Wat je uit het hoofd kent",
    "cmd_check": "Je geheugen testen",
    "cmd_forgot": "Een markering wissen",
    "cmd_streak": "Je dagelijkse reeks",
    "cmd_leaderboard": "De besten van deze week",
    "cmd_profile": "Je profiel en instellingen",

    # Shared wizard controls
    "wizard_cancelled": "Geannuleerd.",
    "wizard_nothing_to_cancel": "Er is niets om te annuleren.",
    "wizard_invalid_input": "Dat begreep ik niet. Probeer het opnieuw of stuur /cancel.",
    "ref_invalid": "Die verwijzing herken ik niet. Probeer iets als 67, 67:1-8 of juz 30.",
    "btn_cancel": "Annuleren",
    "btn_back": "Terug",
    "btn_confirm": "Bevestigen",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "ma",
    "day_tue": "di",
    "day_wed": "wo",
    "day_thu": "do",
    "day_fri": "vr",
    "day_sat": "za",
    "day_sun": "zo",

    # Profile (B1-B3)
    "profile_title": "Je profiel",
    "profile_name_set": "Naam: {name}",
    "profile_name_unset": "Naam: niet ingesteld",
    "profile_leaderboard_on": "Ranglijst: je staat erin",
    "profile_leaderboard_off": "Ranglijst: je bent verborgen",
    "profile_timezone_set": "Tijdzone: UTC{offset}",
    "profile_timezone_unset": "Tijdzone: niet ingesteld",
    "profile_reminder_set": "Dagelijkse herinnering: {time}",
    "profile_reminder_unset": "Dagelijkse herinnering: uit",
    "profile_plan_active": "Plan: {target} — dag {day} van {total}",
    "profile_plan_none": "Plan: nog geen. Start er een met /memorize.",
    "btn_edit_name": "Naam wijzigen",
    "btn_join_board": "Op de ranglijst",
    "btn_leave_board": "Uit de ranglijst",
    "btn_edit_timezone": "Tijdzone wijzigen",
    "btn_edit_reminder": "Herinnering wijzigen",
    "name_prompt": "Stuur de naam waaronder je op de ranglijst wilt staan.",
    "name_invalid": "Gebruik tussen {min} en {max} tekens.",
    "name_saved": "Je verschijnt als {name}.",
    "board_joined": "Je staat nu op de ranglijst.",
    "board_left": "Je bent van de ranglijst gehaald.",
    "timezone_prompt": (
        "Kies je UTC-verschil. Het bepaalt wanneer je dag begint voor reeksen en "
        "wanneer je dagportie aankomt."
    ),
    "timezone_saved": "Tijdzone ingesteld op UTC{offset}.",
    "reminder_prompt": "Stuur het tijdstip waarop je je dagportie wilt, in 24-uursnotatie, bijv. 07:30.",
    "reminder_invalid": "Stuur een tijd in 24-uursnotatie, bijv. 07:30.",
    "reminder_saved": "Dagelijkse herinnering ingesteld op {time}.",
    "btn_reminder_off": "Herinneringen uit",
    "reminder_off": "Dagelijkse herinneringen staan uit.",

    # Progress and /forgot (C3)
    "progress_title": "Wat je uit het hoofd kent",
    "progress_surah_line": "{name}: {done}/{total} verzen — {pct}%",
    "progress_juz_line": "Djuz {n}: {pct}%",
    "progress_quran_line": "Hele Koran: {pct}%",
    "progress_empty": (
        "Nog niets gemarkeerd. Rond een portie af en tik op «Ik ken dit uit het "
        "hoofd», of start een plan met /memorize."
    ),
    "forgot_usage": "Stuur welke markering je wilt wissen, bijvoorbeeld /forgot 67:5-6.",
    "forgot_done": "Markering van {ref} gewist.",
    "forgot_nothing": "Dat had je niet als uit het hoofd gemarkeerd.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "Wat wil je uit het hoofd leren?",
    "btn_target_surah": "Een soera",
    "btn_target_juz": "Een djuz",
    "btn_target_range": "Een bereik",
    "memorize_surah_prompt": "Stuur het soeranummer, bijvoorbeeld 67.",
    "memorize_juz_prompt": "Stuur het djuz-nummer, van 1 tot 30.",
    "memorize_range_prompt": "Stuur het bereik, bijvoorbeeld 67:1-68:5.",
    "memorize_choose_pace": "Hoeveel wil je elke dag doen?",
    "btn_pace_auto": "Kies voor mij",
    "memorize_pace_prompt": "Stuur hoeveel verzen per dag.",
    "memorize_pace_invalid": "Stuur een getal tussen {min} en {max}.",
    "memorize_choose_days": "Op welke dagen wil je studeren?",
    "btn_days_daily": "Elke dag",
    "btn_days_weekdays": "Doordeweeks",
    "btn_days_custom": "Dagen kiezen",
    "memorize_days_prompt": "Tik de dagen aan die je wilt en bevestig daarna.",
    "memorize_preview_title": "{days} dagen, {start} tot {end}:",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Dit plan starten",
    "plan_saved": "Je plan staat klaar. De eerste portie komt op {first_date}.",
    "plan_exists": "Je hebt al een lopend plan. Pauzeer het eerst of stop ermee.",
    "btn_pause_plan": "Plan pauzeren",
    "btn_resume_plan": "Plan hervatten",
    "btn_abandon_plan": "Plan stoppen",
    "plan_paused": "Plan gepauzeerd. Hervat het wanneer je wilt via /profile.",
    "plan_resumed": "Plan hervat.",
    "plan_abandoned": "Plan gestopt.",
    "plan_complete": "Je hebt {target} afgerond. Moge Allah het van je aannemen.",
    "drill_title": "{ref} — dag {day} van {total}",
    "drill_none_today": "Voor vandaag staat er niets gepland.",
    "btn_start_drill": "Portie van vandaag",
    "btn_know_by_heart": "✅ Ik ken dit uit het hoofd",
    "know_confirmed": "{ref} gemarkeerd als geleerd. Je zit op {pct}%.",
    "know_already": "Die had je al gemarkeerd.",

    # Recall check (E2, E3)
    "check_question": "Hoe gaat dit verder?",
    "check_usage": "Stuur wat je wilt testen, bijvoorbeeld /check 67.",
    "check_correct": "Juist.",
    "check_wrong": "Net niet. Het gaat verder met: {correct}",
    "check_already_today": (
        "Je hebt de sessie van vandaag al verdiend met een geheugentest — test "
        "jezelf zo vaak je wilt, het telt alleen niet dubbel."
    ),
    "btn_check_start": "Test mij",

    # Streaks (G2, G3)
    "streak_title": "Je reeks",
    "streak_current": "Huidige reeks: {n}",
    "streak_longest": "Langste reeks: {n}",
    "streak_none": "Nog geen reeks. Rond vandaag een portie af of haal een geheugentest om er een te beginnen.",
    "streak_graph_caption": "De laatste 12 weken",
    "streak_milestone_7": "Een hele week. Hier begint de gewoonte.",
    "streak_milestone_30": "Dertig dagen. De regelmaat staat nu aan jouw kant.",
    "streak_milestone_100": "Honderd dagen. Maar heel weinig mensen komen zo ver.",
    "streak_milestone_365": "Een heel jaar, elke dag opnieuw. Moge Allah bewaren wat je hebt geleerd.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "De ranglijst van deze week",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "Jij: {rank}. — {sessions}",
    "leaderboard_empty": "Deze week heeft nog niemand een sessie afgerond. Wees de eerste.",
    "leaderboard_not_opted_in": "Je staat niet op de ranglijst. Doe mee via /profile.",
}
