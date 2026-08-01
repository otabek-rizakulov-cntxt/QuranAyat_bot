# Norwegian — Norsk

strings = {
    "welcome_intro": (
        "Send meg et sura- og versnummer, for eksempel <b>2:255</b>, og jeg sender deg "
        "det verset fra den hellige Koranen.\n\n"
        "Du kan også sende et intervall som <b>59:22-24</b> for en sammensatt "
        "lydresitasjon."
    ),
    "welcome_commands_header": "Kommandoer:",
    "welcome_inline": (
        "Du kan bruke meg i alle chatter: skriv <b>@QuranAyat_bot</b> etterfulgt av en "
        "henvisning."
    ),
    "about": (
        "Med denne boten kan du lese den hellige Koranen på Telegram på mange "
        "språk.\n\n"
        "Oversettelsene er hentet fra tanzil.net (se ATTRIBUTIONS.md for hver "
        "oversettelses utgave og oversetter). Lyden er en resitasjon av sjeik "
        "Mahmoud Khalil al-Husary (everyayah.com). Tafsiren er Tafsir "
        "al-Jalalayn (altafsir.com), tilgjengelig på engelsk.\n\n"
        "Bytt språk når som helst med /language."
    ),
    "ayah_not_found": "Dette verset finnes ikke!",
    "range_too_large": "Intervallet er for stort, be om maksimalt {n} vers om gangen.",
    "choose_language": "Velg språket ditt:",
    "language_set": "Språket er satt til {lang}.",
    "choose_translation_language": "Velg oversettelsesspråk:",
    "translation_language_set": "Oversettelsesspråk satt til {lang}.",
    "choose_reciter": "Velg en resitatør:",
    "reciter_set": "Resitatør satt til {reciter}.",
    "btn_search_reciter": "Søk etter navn",
    "reciter_search_prompt": "Skriv navnet på en resitatør for å søke (f.eks. «Sudais», «Abdul Basit»).",
    "reciter_search_no_matches": "Ingen resitatør samsvarte med det navnet — prøv igjen.",
    "reciter_search_results": "Søkeresultater:",
    "btn_set_reciter": "Angi som min resitatør",
    "reciter_inline_description": "Trykk for å angi som din resitatør",
    "tafsir_en_note": "\n\n(Tafsiren er bare tilgjengelig på engelsk.)",
    "btn_translation": "Oversettelse",
    "btn_tafsir": "Tafsir",
    "btn_arabic": "Arabisk",
    "btn_audio": "Lyd",
    "btn_previous": "Forrige",
    "btn_random": "Tilfeldig",
    "btn_next": "Neste",
    "page_label": "Side {n} av {total}",
    "page_out_of_range": "Send et sidetall mellom 1 og {total}, for eksempel /page 255.",
    "juz_out_of_range": "Send et juz-nummer mellom 1 og {total}, for eksempel /juz 30.",
    "sajda_list_title": "Vers med nedbøyelse (sajda):",
    "btn_ayah_view": "Versvisning",
    "btn_repeat": "Gjenta",
    "reciter_group_recitation": "Resitatører",
    "reciter_group_riwayah": "Riwāya",
    "reciter_group_translation": "Betydning",
    "riwayah_warning": "Merk: dette er Warsh-riwāyaen — en lesning av korateksten som skiller seg fra Hafs-lesningen som vises her i den arabiske teksten og oversettelsene, så lyden vil ikke alltid stemme med ordene på skjermen.",
    "translation_audio_warning": "Merk: dette opptaket er ikke koranresitasjon, men den oversatte betydningen lest høyt. Velg fra fanen «Resitatører» for å høre den arabiske resitasjonen.",
    "cmd_index": "Liste over alle suraer",
    "cmd_page": "Les en mushaf-side",
    "cmd_juz": "Åpne en juz",
    "cmd_sajda": "Vers med nedbøyelse",
    "cmd_random": "Et tilfeldig vers",
    "cmd_language": "Bytt språk",
    "cmd_translation": "Bytt oversettelsesspråk",
    "cmd_reciter": "Bytt resitatør",
    "cmd_about": "Kilder og takk",
    "quran_name": "Koranen",

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Start en memoreringsplan",
    "cmd_progress": "Det du kan utenat",
    "cmd_check": "Test hukommelsen din",
    "cmd_forgot": "Fjern merkingen av et intervall",
    "cmd_streak": "Din daglige rekke",
    "cmd_leaderboard": "Ukens beste",
    "cmd_profile": "Profilen og innstillingene dine",

    # Shared wizard controls
    "wizard_cancelled": "Avbrutt.",
    "wizard_nothing_to_cancel": "Det er ingenting å avbryte.",
    "wizard_invalid_input": "Det forsto jeg ikke. Prøv igjen, eller send /cancel.",
    "ref_invalid": "Det er ikke en henvisning jeg kjenner igjen. Prøv noe som 67, 67:1-8 eller juz 30.",
    "btn_cancel": "Avbryt",
    "btn_back": "Tilbake",
    "btn_confirm": "Bekreft",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "man",
    "day_tue": "tir",
    "day_wed": "ons",
    "day_thu": "tor",
    "day_fri": "fre",
    "day_sat": "lør",
    "day_sun": "søn",

    # Profile (B1-B3)
    "profile_title": "Profilen din",
    "profile_name_set": "Navn: {name}",
    "profile_name_unset": "Navn: ikke angitt",
    "profile_leaderboard_on": "Ledertavle: du vises",
    "profile_leaderboard_off": "Ledertavle: du er skjult",
    "profile_timezone_set": "Tidssone: UTC{offset}",
    "profile_timezone_unset": "Tidssone: ikke angitt",
    "profile_reminder_set": "Daglig påminnelse: {time}",
    "profile_reminder_unset": "Daglig påminnelse: av",
    "profile_plan_active": "Plan: {target} — dag {day} av {total}",
    "profile_plan_none": "Plan: ingen ennå. Start en med /memorize.",
    "btn_edit_name": "Bytt navn",
    "btn_join_board": "Bli med på ledertavlen",
    "btn_leave_board": "Forlat ledertavlen",
    "btn_edit_timezone": "Bytt tidssone",
    "btn_edit_reminder": "Bytt påminnelsestid",
    "name_prompt": "Send navnet du vil vises med på ledertavlen.",
    "name_invalid": "Bruk mellom {min} og {max} tegn.",
    "name_saved": "Du vises som {name}.",
    "board_joined": "Du er med på ledertavlen nå.",
    "board_left": "Du er fjernet fra ledertavlen.",
    "timezone_prompt": (
        "Velg UTC-forskyvningen din. Den avgjør når døgnet ditt begynner for rekken, "
        "og når dagsporsjonen din kommer."
    ),
    "timezone_saved": "Tidssonen er satt til UTC{offset}.",
    "reminder_prompt": "Send tidspunktet du vil ha dagsporsjonen din, i 24-timersformat, f.eks. 07:30.",
    "reminder_invalid": "Send et tidspunkt i 24-timersformat, f.eks. 07:30.",
    "reminder_saved": "Daglig påminnelse satt til {time}.",
    "btn_reminder_off": "Slå av påminnelser",
    "reminder_off": "Daglige påminnelser er av.",

    # Progress and /forgot (C3)
    "progress_title": "Det du kan utenat",
    "progress_surah_line": "{name}: {done}/{total} vers — {pct} %",
    "progress_juz_line": "Juz {n}: {pct} %",
    "progress_quran_line": "Hele Koranen: {pct} %",
    "progress_empty": (
        "Ingenting er merket ennå. Fullfør en porsjon og trykk «Dette kan jeg utenat», "
        "eller start en plan med /memorize."
    ),
    "forgot_usage": "Send hva som skal avmerkes, for eksempel /forgot 67:5-6.",
    "forgot_done": "{ref} er avmerket.",
    "forgot_nothing": "Du hadde ikke merket det som memorert.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "Hva vil du lære utenat?",
    "btn_target_surah": "En sura",
    "btn_target_juz": "En juz",
    "btn_target_range": "Et intervall",
    "memorize_surah_prompt": "Send suranummeret, for eksempel 67.",
    "memorize_juz_prompt": "Send juz-nummeret, fra 1 til 30.",
    "memorize_range_prompt": "Send intervallet, for eksempel 67:1-68:5.",
    "memorize_choose_pace": "Hvor mye vil du ta hver dag?",
    "btn_pace_auto": "Velg for meg",
    "memorize_pace_prompt": "Send hvor mange vers per dag.",
    "memorize_pace_invalid": "Send et tall mellom {min} og {max}.",
    "memorize_choose_days": "Hvilke dager vil du studere?",
    "btn_days_daily": "Hver dag",
    "btn_days_weekdays": "Hverdager",
    "btn_days_custom": "Velg dager",
    "memorize_days_prompt": "Trykk på dagene du vil ha, og bekreft.",
    "memorize_preview_title": "{days} dager, {start} til {end}:",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Start denne planen",
    "plan_saved": "Planen din er klar. Den første porsjonen kommer {first_date}.",
    "plan_exists": "Du har allerede en plan i gang. Sett den på pause eller avslutt den først.",
    "btn_pause_plan": "Sett planen på pause",
    "btn_resume_plan": "Fortsett planen",
    "btn_abandon_plan": "Avslutt planen",
    "plan_paused": "Planen er satt på pause. Fortsett den når som helst fra /profile.",
    "plan_resumed": "Planen fortsetter.",
    "plan_abandoned": "Planen er avsluttet.",
    "plan_complete": "Du har fullført {target}. Måtte Allah ta imot det fra deg.",
    "drill_title": "{ref} — dag {day} av {total}",
    "drill_none_today": "Ingenting er planlagt i dag.",
    "btn_start_drill": "Start dagens porsjon",
    "btn_know_by_heart": "✅ Dette kan jeg utenat",
    "know_confirmed": "{ref} er merket som memorert. Du er på {pct} %.",
    "know_already": "Den hadde du allerede merket.",

    # Recall check (E2, E3)
    "check_question": "Hvordan fortsetter dette?",
    "check_usage": "Send hva som skal testes, for eksempel /check 67.",
    "check_correct": "Riktig.",
    "check_wrong": "Ikke helt. Det fortsetter: {correct}",
    "check_already_today": (
        "Du har allerede sikret dagens økt med en hukommelsestest — test deg selv så "
        "ofte du vil, det telles bare ikke to ganger."
    ),
    "btn_check_start": "Test meg",

    # Streaks (G2, G3)
    "streak_title": "Rekken din",
    "streak_current": "Dager på rad nå: {n}",
    "streak_longest": "Flest dager på rad: {n}",
    "streak_none": "Ingen rekke ennå. Fullfør en porsjon eller bestå en hukommelsestest i dag for å starte en.",
    "streak_graph_caption": "De siste 12 ukene",
    "streak_milestone_7": "En hel uke. Det er her vanen begynner.",
    "streak_milestone_30": "Tretti dager. Nå har du jevnheten på din side.",
    "streak_milestone_100": "Hundre dager. Svært få kommer så langt.",
    "streak_milestone_365": "Et helt år, hver eneste dag. Måtte Allah bevare det du har lært.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "Ukens ledertavle",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "Deg: {rank}. — {sessions}",
    "leaderboard_empty": "Ingen har fullført en økt denne uken ennå. Bli den første.",
    "leaderboard_not_opted_in": "Du er ikke på ledertavlen. Bli med fra /profile.",
}
