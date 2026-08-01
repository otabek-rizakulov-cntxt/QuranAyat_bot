# Swedish — Svenska

strings = {
    "welcome_intro": (
        "Skicka mig ett sura- och versnummer, till exempel <b>2:255</b>, så skickar jag "
        "den versen ur den heliga Koranen.\n\n"
        "Du kan även skicka ett intervall som <b>59:22-24</b> för en sammanslagen "
        "ljudrecitation."
    ),
    "welcome_commands_header": "Kommandon:",
    "welcome_inline": (
        "Du kan använda mig i vilken chatt som helst: skriv <b>@QuranAyat_bot</b> följt "
        "av en hänvisning."
    ),
    "about": (
        "Med den här boten kan du läsa den heliga Koranen på Telegram på många "
        "språk.\n\n"
        "Översättningarna kommer från tanzil.net (se ATTRIBUTIONS.md för varje "
        "översättnings utgåva och översättare). Ljudet är en recitation av "
        "shejk Mahmoud Khalil al-Husary (everyayah.com). Tafsir är Tafsir "
        "al-Jalalayn (altafsir.com), tillgänglig på engelska.\n\n"
        "Byt språk när du vill med /language."
    ),
    "ayah_not_found": "Den versen finns inte!",
    "range_too_large": "Intervallet är för stort, begär högst {n} verser åt gången.",
    "choose_language": "Välj ditt språk:",
    "language_set": "Språket är inställt på {lang}.",
    "choose_translation_language": "Välj översättningsspråk:",
    "translation_language_set": "Översättningsspråk inställt på {lang}.",
    "choose_reciter": "Välj en recitatör:",
    "reciter_set": "Recitatör inställd på {reciter}.",
    "btn_search_reciter": "Sök efter namn",
    "reciter_search_prompt": "Skriv namnet på en recitatör för att söka (t.ex. ”Sudais”, ”Abdul Basit”).",
    "reciter_search_no_matches": "Ingen recitatör matchade det namnet — försök igen.",
    "reciter_search_results": "Sökresultat:",
    "btn_set_reciter": "Ange som min recitatör",
    "reciter_inline_description": "Tryck för att ange som din recitatör",
    "tafsir_en_note": "\n\n(Tafsir finns endast på engelska.)",
    "btn_translation": "Översättning",
    "btn_tafsir": "Tafsir",
    "btn_arabic": "Arabiska",
    "btn_audio": "Ljud",
    "btn_previous": "Föregående",
    "btn_random": "Slumpmässig",
    "btn_next": "Nästa",
    "page_label": "Sida {n} av {total}",
    "page_out_of_range": "Skicka ett sidnummer mellan 1 och {total}, till exempel /page 255.",
    "juz_out_of_range": "Skicka ett juz-nummer mellan 1 och {total}, till exempel /juz 30.",
    "sajda_list_title": "Verser med nedfallande (sajda):",
    "btn_ayah_view": "Versvy",
    "btn_repeat": "Upprepa",
    "reciter_group_recitation": "Recitatörer",
    "reciter_group_riwayah": "Riwāya",
    "reciter_group_translation": "Betydelse",
    "riwayah_warning": "Obs: detta är Warsh-riwāyan — en läsning av korantexten som skiljer sig från Hafs-läsningen som visas här i den arabiska texten och översättningarna, så ljudet stämmer inte alltid med orden på skärmen.",
    "translation_audio_warning": "Obs: denna inspelning är inte koranrecitation, utan den översatta betydelsen uppläst. Välj från fliken «Recitatörer» för att höra den arabiska recitationen.",
    "cmd_index": "Lista alla suror",
    "cmd_page": "Läs en mushaf-sida",
    "cmd_juz": "Öppna en juz",
    "cmd_sajda": "Verser med nedfallande",
    "cmd_random": "En slumpmässig vers",
    "cmd_language": "Byt språk",
    "cmd_translation": "Byt översättningsspråk",
    "cmd_reciter": "Byt recitatör",
    "cmd_about": "Källor och tack",
    "quran_name": "Koranen",

    # --- Hifz platform ---------------------------------------------------------

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Starta en hifz-plan",
    "cmd_progress": "Det du kan utantill",
    "cmd_check": "Testa ditt minne",
    "cmd_forgot": "Ta bort en markering",
    "cmd_streak": "Din dagliga svit",
    "cmd_leaderboard": "Veckans bästa",
    "cmd_profile": "Din profil och dina inställningar",

    # Shared wizard controls
    "wizard_cancelled": "Avbrutet.",
    "wizard_nothing_to_cancel": "Det finns inget att avbryta.",
    "wizard_invalid_input": "Det förstod jag inte. Försök igen eller skicka /cancel.",
    "ref_invalid": "Den hänvisningen känner jag inte igen. Prova något som 67, 67:1-8 eller juz 30.",
    "btn_cancel": "Avbryt",
    "btn_back": "Tillbaka",
    "btn_confirm": "Bekräfta",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "mån",
    "day_tue": "tis",
    "day_wed": "ons",
    "day_thu": "tors",
    "day_fri": "fre",
    "day_sat": "lör",
    "day_sun": "sön",

    # Profile (B1-B3)
    "profile_title": "Din profil",
    "profile_name_set": "Namn: {name}",
    "profile_name_unset": "Namn: inte angivet",
    "profile_leaderboard_on": "Topplista: du visas",
    "profile_leaderboard_off": "Topplista: du är dold",
    "profile_timezone_set": "Tidszon: UTC{offset}",
    "profile_timezone_unset": "Tidszon: inte angiven",
    "profile_reminder_set": "Daglig påminnelse: {time}",
    "profile_reminder_unset": "Daglig påminnelse: av",
    "profile_plan_active": "Plan: {target} — dag {day} av {total}",
    "profile_plan_none": "Plan: ingen än. Starta en med /memorize.",
    "btn_edit_name": "Byt namn",
    "btn_join_board": "Gå med i topplistan",
    "btn_leave_board": "Lämna topplistan",
    "btn_edit_timezone": "Byt tidszon",
    "btn_edit_reminder": "Byt påminnelsetid",
    "name_prompt": "Skicka namnet du vill visas under på topplistan.",
    "name_invalid": "Använd mellan {min} och {max} tecken.",
    "name_saved": "Du visas som {name}.",
    "board_joined": "Du är med på topplistan nu.",
    "board_left": "Du har tagits bort från topplistan.",
    "timezone_prompt": (
        "Välj din UTC-förskjutning. Den avgör när ditt dygn börjar för sviten "
        "och när din dagsportion kommer."
    ),
    "timezone_saved": "Tidszonen är inställd på UTC{offset}.",
    "reminder_prompt": "Skicka tiden då du vill ha din dagsportion, i 24-timmarsformat, t.ex. 07:30.",
    "reminder_invalid": "Skicka en tid i 24-timmarsformat, t.ex. 07:30.",
    "reminder_saved": "Daglig påminnelse inställd på {time}.",
    "btn_reminder_off": "Stäng av påminnelser",
    "reminder_off": "Dagliga påminnelser är avstängda.",

    # Progress and /forgot (C3)
    "progress_title": "Det du kan utantill",
    "progress_surah_line": "{name}: {done}/{total} verser — {pct} %",
    "progress_juz_line": "Juz {n}: {pct} %",
    "progress_quran_line": "Hela Koranen: {pct} %",
    "progress_empty": (
        "Inget är markerat än. Slutför en portion och tryck på ”Detta kan jag "
        "utantill”, eller starta en plan med /memorize."
    ),
    "forgot_usage": "Skicka vad som ska avmarkeras, till exempel /forgot 67:5-6.",
    "forgot_done": "{ref} är avmarkerad.",
    "forgot_nothing": "Du hade inte markerat det som memorerat.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "Vad vill du lära dig utantill?",
    "btn_target_surah": "En sura",
    "btn_target_juz": "En juz",
    "btn_target_range": "Ett intervall",
    "memorize_surah_prompt": "Skicka suranumret, till exempel 67.",
    "memorize_juz_prompt": "Skicka juz-numret, från 1 till 30.",
    "memorize_range_prompt": "Skicka intervallet, till exempel 67:1-68:5.",
    "memorize_choose_pace": "Hur mycket vill du göra varje dag?",
    "btn_pace_auto": "Välj åt mig",
    "memorize_pace_prompt": "Skicka hur många verser per dag.",
    "memorize_pace_invalid": "Skicka ett tal mellan {min} och {max}.",
    "memorize_choose_days": "Vilka dagar vill du studera?",
    "btn_days_daily": "Varje dag",
    "btn_days_weekdays": "Vardagar",
    "btn_days_custom": "Välj dagar",
    "memorize_days_prompt": "Tryck på de dagar du vill ha och bekräfta sedan.",
    "memorize_preview_title": "{days} dagar, {start} till {end}:",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Starta planen",
    "plan_saved": "Din plan är klar. Den första portionen kommer den {first_date}.",
    "plan_exists": "Du har redan en plan igång. Pausa eller avbryt den först.",
    "btn_pause_plan": "Pausa planen",
    "btn_resume_plan": "Återuppta planen",
    "btn_abandon_plan": "Avbryt planen",
    "plan_paused": "Planen är pausad. Återuppta den när du vill från /profile.",
    "plan_resumed": "Planen är återupptagen.",
    "plan_abandoned": "Planen är avbruten.",
    "plan_complete": "Du har slutfört {target}. Må Allah ta emot det från dig.",
    "drill_title": "{ref} — dag {day} av {total}",
    "drill_none_today": "Inget är inplanerat i dag.",
    "btn_start_drill": "Dagens portion",
    "btn_know_by_heart": "✅ Detta kan jag utantill",
    "know_confirmed": "{ref} är markerad som memorerad. Du är på {pct} %.",
    "know_already": "Den hade du redan markerat.",

    # Recall check (E2, E3)
    "check_question": "Hur fortsätter det här?",
    "check_usage": "Skicka vad som ska testas, till exempel /check 67.",
    "check_correct": "Rätt.",
    "check_wrong": "Inte riktigt. Det fortsätter: {correct}",
    "check_already_today": (
        "Du har redan tjänat in dagens pass med ett minnestest — testa dig själv "
        "hur ofta du vill, det räknas bara inte två gånger."
    ),
    "btn_check_start": "Testa mig",

    # Streaks (G2, G3)
    "streak_title": "Din svit",
    "streak_current": "Nuvarande svit: {n}",
    "streak_longest": "Längsta svit: {n}",
    "streak_none": "Ingen svit än. Slutför en portion eller klara ett minnestest i dag för att starta en.",
    "streak_graph_caption": "De senaste 12 veckorna",
    "streak_milestone_7": "En hel vecka. Det är här vanan börjar.",
    "streak_milestone_30": "Trettio dagar. Nu har du uthålligheten på din sida.",
    "streak_milestone_100": "Hundra dagar. Väldigt få kommer så här långt.",
    "streak_milestone_365": "Ett helt år, varenda dag. Må Allah bevara det du har lärt dig.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "Veckans topplista",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "Du: {rank}. — {sessions}",
    "leaderboard_empty": "Ingen har slutfört ett pass den här veckan än. Bli först.",
    "leaderboard_not_opted_in": "Du är inte med på topplistan. Gå med från /profile.",
}
