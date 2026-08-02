# Bosnian — Bosanski

strings = {
    "welcome_intro": (
        "Pošalji mi broj sure i ajeta, na primjer <b>2:255</b>, i poslat ću ti taj ajet "
        "iz Časnog Kur'ana.\n\n"
        "Možeš poslati i raspon poput <b>59:22-24</b> za objedinjeno audio učenje."
    ),
    "welcome_commands_header": "Naredbe:",
    "welcome_inline": (
        "Možeš me koristiti u bilo kojem chatu: upiši <b>@QuranAyat_bot</b> i zatim "
        "referencu."
    ),
    "about": (
        "Ovaj bot ti omogućava da čitaš Časni Kur'an na Telegramu na mnogim "
        "jezicima.\n\n"
        "Prijevodi su preuzeti sa tanzil.net (pogledaj ATTRIBUTIONS.md za "
        "izdanje i prevodioca svakog prijevoda). Audio je učenje šejha Mahmuda "
        "Halila el-Husarija (everyayah.com). Tefsir je Tefsir el-Dželalejn "
        "(altafsir.com), dostupan na engleskom.\n\n"
        "Jezik promijeni bilo kada pomoću /language."
    ),
    "ayah_not_found": "Taj ajet ne postoji!",
    "range_too_large": "Raspon je prevelik, zatraži najviše {n} ajeta odjednom.",
    "choose_language": "Odaberi svoj jezik:",
    "language_set": "Jezik postavljen na {lang}.",
    "choose_translation_language": "Izaberite jezik prijevoda:",
    "translation_language_set": "Jezik prijevoda postavljen na {lang}.",
    "choose_reciter": "Izaberite učača:",
    "reciter_set": "Učač postavljen na {reciter}.",
    "btn_search_reciter": "Pretraga po imenu",
    "reciter_search_prompt": "Upišite ime učača za pretragu (npr. «Sudais», «Abdul Basit»).",
    "reciter_search_no_matches": "Nijedan učač ne odgovara tom imenu — pokušajte ponovo.",
    "reciter_search_results": "Rezultati pretrage:",
    "btn_set_reciter": "Postavi kao mog učača",
    "reciter_inline_description": "Dodirnite da postavite kao svog učača",
    "tafsir_en_note": "\n\n(Tefsir je dostupan samo na engleskom.)",
    "btn_translation": "Prijevod",
    "btn_tafsir": "Tefsir",
    "btn_arabic": "Arapski",
    "btn_audio": "Audio",
    "btn_previous": "Prethodni",
    "btn_random": "Nasumično",
    "btn_next": "Sljedeći",
    "page_label": "Stranica {n} od {total}",
    "page_out_of_range": "Pošaljite broj stranice između 1 i {total}, na primjer /page 255.",
    "juz_out_of_range": "Pošaljite broj džuza između 1 i {total}, na primjer /juz 30.",
    "sajda_list_title": "Ajeti sedžde:",
    "btn_ayah_view": "Prikaz ajeta",
    "btn_repeat": "Ponovi",
    "reciter_group_recitation": "Učači",
    "reciter_group_riwayah": "Rivajet",
    "reciter_group_translation": "Značenje",
    "riwayah_warning": "Napomena: ovo je Waršov rivajet — čitanje kur'anskog teksta različito od Hafsovog koje je ovdje prikazano u arapskom tekstu i prijevodima, pa se zvuk neće uvijek podudarati s riječima na ekranu.",
    "translation_audio_warning": "Napomena: ovaj snimak nije učenje Kur'ana — to je naglas pročitano prevedeno značenje. Odaberite iz kartice «Učači» da čujete arapsko učenje.",
    "cmd_index": "Popis svih sura",
    "cmd_page": "Čitaj stranicu mushafa",
    "cmd_juz": "Otvori džuz",
    "cmd_sajda": "Ajeti sedžde",
    "cmd_random": "Nasumičan ajet",
    "cmd_language": "Promijeni jezik",
    "cmd_translation": "Promijeni jezik prijevoda",
    "cmd_reciter": "Promijeni učača",
    "cmd_about": "Izvori i zahvale",
    "quran_name": "Kur'an",

    # --- Hifz platform ---------------------------------------------------------

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Pokreni plan hifza",
    "cmd_progress": "Šta si naučio napamet",
    "cmd_check": "Provjeri svoje pamćenje",
    "cmd_forgot": "Ukloni oznaku naučenog",
    "cmd_streak": "Tvoj niz dana",
    "cmd_leaderboard": "Najbolji ove sedmice",
    "cmd_profile": "Tvoj profil i postavke",

    # Shared wizard controls
    "wizard_cancelled": "Otkazano.",
    "wizard_nothing_to_cancel": "Nema ničega za otkazati.",
    "wizard_invalid_input": "Nisam razumio. Pokušaj ponovo ili pošalji /cancel.",
    "ref_invalid": "To nije referenca koju prepoznajem. Probaj nešto poput 67, 67:1-8 ili džuz 30.",
    "btn_cancel": "Otkaži",
    "btn_back": "Nazad",
    "btn_confirm": "Potvrdi",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "Pon",
    "day_tue": "Uto",
    "day_wed": "Sri",
    "day_thu": "Čet",
    "day_fri": "Pet",
    "day_sat": "Sub",
    "day_sun": "Ned",

    # Profile (B1-B3)
    "profile_title": "Tvoj profil",
    "profile_name_set": "Ime: {name}",
    "profile_name_unset": "Ime: nije postavljeno",
    "profile_leaderboard_on": "Rang-lista: prikazan si",
    "profile_leaderboard_off": "Rang-lista: skriven si",
    "profile_timezone_set": "Vremenska zona: UTC{offset}",
    "profile_timezone_unset": "Vremenska zona: nije postavljena",
    "profile_reminder_set": "Dnevni podsjetnik: {time}",
    "profile_reminder_unset": "Dnevni podsjetnik: isključen",
    "profile_plan_active": "Plan: {target} — dan {day} od {total}",
    "profile_plan_none": "Plan: još nemaš. Pokreni ga sa /memorize.",
    "btn_edit_name": "Promijeni ime",
    "btn_join_board": "Uđi na rang-listu",
    "btn_leave_board": "Napusti rang-listu",
    "btn_edit_timezone": "Promijeni vremensku zonu",
    "btn_edit_reminder": "Promijeni vrijeme podsjetnika",
    "name_prompt": "Pošalji ime pod kojim želiš biti prikazan na rang-listi.",
    "name_invalid": "Koristi od {min} do {max} znakova.",
    "name_saved": "Bit ćeš prikazan kao {name}.",
    "board_joined": "Sada si na rang-listi.",
    "board_left": "Uklonjen si sa rang-liste.",
    "timezone_prompt": (
        "Odaberi svoj pomak od UTC. On određuje kada ti počinje dan za nizove i "
        "kada stiže dnevna porcija."
    ),
    "timezone_saved": "Vremenska zona postavljena na UTC{offset}.",
    "reminder_prompt": "Pošalji vrijeme kada želiš dnevnu porciju, u 24-satnom obliku, npr. 07:30.",
    "reminder_invalid": "Pošalji vrijeme u 24-satnom obliku, npr. 07:30.",
    "reminder_saved": "Dnevni podsjetnik postavljen na {time}.",
    "btn_reminder_off": "Isključi podsjetnike",
    "reminder_off": "Dnevni podsjetnici su isključeni.",

    # Progress and /forgot (C3)
    "progress_title": "Šta si naučio napamet",
    "progress_surah_line": "{name}: {done}/{total} ajeta — {pct}%",
    "progress_juz_line": "Džuz {n}: {pct}%",
    "progress_quran_line": "Cijeli Kur'an: {pct}%",
    "progress_empty": (
        "Još ništa nije označeno. Završi porciju i dodirni «Znam napamet» ili "
        "pokreni plan sa /memorize."
    ),
    "forgot_usage": "Pošalji šta da odznačim, na primjer /forgot 67:5-6.",
    "forgot_done": "Oznaka uklonjena: {ref}.",
    "forgot_nothing": "To nisi ni označio kao naučeno.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "Šta želiš naučiti napamet?",
    "btn_target_surah": "Suru",
    "btn_target_juz": "Džuz",
    "btn_target_range": "Raspon",
    "memorize_surah_prompt": "Pošalji broj sure, na primjer 67.",
    "memorize_juz_prompt": "Pošalji broj džuza, od 1 do 30.",
    "memorize_range_prompt": "Pošalji raspon, na primjer 67:1-68:5.",
    "memorize_choose_pace": "Koliko želiš raditi svaki dan?",
    "btn_pace_auto": "Odaberi umjesto mene",
    "memorize_pace_prompt": "Pošalji koliko ajeta dnevno.",
    "memorize_pace_invalid": "Pošalji broj između {min} i {max}.",
    "memorize_choose_days": "Kojim danima želiš učiti?",
    "btn_days_daily": "Svaki dan",
    "btn_days_weekdays": "Radnim danima",
    "btn_days_custom": "Odaberi dane",
    "memorize_days_prompt": "Dodirni dane koje želiš, pa potvrdi.",
    "memorize_preview_title": "Broj dana: {days}, od {start} do {end}:",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Pokreni ovaj plan",
    "plan_saved": "Plan je postavljen. Prva porcija stiže {first_date}.",
    "plan_exists": "Već imaš aktivan plan. Prvo ga pauziraj ili napusti.",
    "btn_pause_plan": "Pauziraj plan",
    "btn_resume_plan": "Nastavi plan",
    "btn_abandon_plan": "Napusti plan",
    "plan_paused": "Plan je pauziran. Nastavi ga bilo kada iz /profile.",
    "plan_resumed": "Plan je nastavljen.",
    "plan_abandoned": "Plan je napušten.",
    "plan_complete": "Završio si {target}. Neka ti Allah primi.",
    "drill_title": "{ref} — dan {day} od {total}",
    "drill_none_today": "Za danas ništa nije zakazano.",
    "btn_start_drill": "Počni današnju porciju",
    "btn_know_by_heart": "✅ Znam napamet",
    "know_confirmed": "{ref} označeno kao naučeno. Sada si na {pct}%.",
    "know_already": "To si već bio označio.",

    # Recall check (E2, E3)
    "check_question": "Kako se ovo nastavlja?",
    "check_usage": "Pošalji šta da provjerim, na primjer /check 67.",
    "check_correct": "Tačno.",
    "check_wrong": "Nije baš tako. Nastavlja se: {correct}",
    "check_already_today": (
        "Današnju sesiju si već zaradio kroz provjeru pamćenja — provjeravaj se "
        "koliko god želiš, samo se neće brojati dvaput."
    ),
    "btn_check_start": "Provjeri me",

    # Streaks (G2, G3)
    "streak_title": "Tvoj niz",
    "streak_current": "Trenutni niz, dana: {n}",
    "streak_longest": "Najduži niz, dana: {n}",
    "streak_none": "Još nemaš niz. Završi porciju ili danas prođi provjeru pamćenja da ga započneš.",
    "streak_graph_caption": "Posljednjih 12 sedmica",
    "streak_milestone_7": "Puna sedmica. Ovdje počinje navika.",
    "streak_milestone_30": "Trideset dana. Dosljednost je sada na tvojoj strani.",
    "streak_milestone_100": "Stotinu dana. Vrlo malo ljudi stigne dovde.",
    "streak_milestone_365": "Cijela godina, svaki jedan dan. Neka Allah sačuva ono što si naučio.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "Rang-lista ove sedmice",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "Ti: {rank}. — {sessions}",
    "leaderboard_empty": "Ove sedmice još niko nije završio sesiju. Budi prvi.",
    "leaderboard_not_opted_in": "Nisi na rang-listi. Pridruži se iz /profile.",
}
