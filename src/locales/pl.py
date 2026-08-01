# Polish — Polski

strings = {
    "welcome_intro": (
        "Wyślij mi numer sury i wersetu, na przykład <b>2:255</b>, a odeślę ci ten werset "
        "Świętego Koranu.\n\n"
        "Możesz też wysłać zakres, np. <b>59:22-24</b>, aby otrzymać połączoną recytację "
        "audio."
    ),
    "welcome_commands_header": "Polecenia:",
    "welcome_inline": (
        "Możesz używać mnie na każdym czacie: wpisz <b>@QuranAyat_bot</b>, a po nim "
        "odnośnik."
    ),
    "about": (
        "Ten bot pozwala czytać Święty Koran na Telegramie w wielu językach.\n\n"
        "Tłumaczenia pochodzą z tanzil.net (zobacz ATTRIBUTIONS.md, aby poznać "
        "wydanie i tłumacza każdego przekładu). Nagranie to recytacja szejka "
        "Mahmuda Chalila al-Husariego (everyayah.com). Tafsir to Tafsir "
        "al-Dżalalajn (altafsir.com), dostępny po angielsku.\n\n"
        "Język zmienisz w każdej chwili poleceniem /language."
    ),
    "ayah_not_found": "Taki werset nie istnieje!",
    "range_too_large": "Zakres jest za duży, poproś o maksymalnie {n} wersetów naraz.",
    "choose_language": "Wybierz swój język:",
    "language_set": "Język ustawiony na {lang}.",
    "choose_translation_language": "Wybierz język tłumaczenia:",
    "translation_language_set": "Język tłumaczenia ustawiono na {lang}.",
    "choose_reciter": "Wybierz recytatora:",
    "reciter_set": "Recytatora ustawiono na {reciter}.",
    "btn_search_reciter": "Szukaj po imieniu",
    "reciter_search_prompt": "Wpisz imię recytatora, aby wyszukać (np. „Sudais”, „Abdul Basit”).",
    "reciter_search_no_matches": "Nie znaleziono recytatora o tym imieniu — spróbuj ponownie.",
    "reciter_search_results": "Wyniki wyszukiwania:",
    "btn_set_reciter": "Ustaw jako mojego recytatora",
    "reciter_inline_description": "Dotknij, aby ustawić jako swojego recytatora",
    "tafsir_en_note": "\n\n(Tafsir jest dostępny tylko po angielsku.)",
    "btn_translation": "Tłumaczenie",
    "btn_tafsir": "Tafsir",
    "btn_arabic": "Arabski",
    "btn_audio": "Audio",
    "btn_previous": "Poprzedni",
    "btn_random": "Losowy",
    "btn_next": "Następny",
    "page_label": "Strona {n} z {total}",
    "page_out_of_range": "Wyślij numer strony od 1 do {total}, na przykład /page 255.",
    "juz_out_of_range": "Wyślij numer dżuzu od 1 do {total}, na przykład /juz 30.",
    "sajda_list_title": "Wersety pokłonu (sadżda):",
    "btn_ayah_view": "Widok wersetów",
    "btn_repeat": "Powtórz",
    "reciter_group_recitation": "Recytatorzy",
    "reciter_group_riwayah": "Riwaja",
    "reciter_group_translation": "Znaczenie",
    "riwayah_warning": "Uwaga: to riwaja Warsza — odczytanie tekstu koranicznego różne od odczytania Hafsa pokazanego tu w tekście arabskim i tłumaczeniach, więc dźwięk nie zawsze będzie zgodny ze słowami na ekranie.",
    "translation_audio_warning": "Uwaga: to nagranie nie jest recytacją Koranu, lecz odczytaniem na głos przetłumaczonego znaczenia. Wybierz z zakładki «Recytatorzy», aby usłyszeć recytację po arabsku.",
    "cmd_index": "Lista wszystkich sur",
    "cmd_page": "Przeczytaj stronę mushafu",
    "cmd_juz": "Otwórz dżuz",
    "cmd_sajda": "Wersety pokłonu",
    "cmd_random": "Losowy werset",
    "cmd_language": "Zmień język",
    "cmd_translation": "Zmień język tłumaczenia",
    "cmd_reciter": "Zmień recytatora",
    "cmd_about": "Źródła i podziękowania",
    "quran_name": "Koran",

    # --- Hifz platform ---------------------------------------------------------

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Zacznij plan zapamiętywania",
    "cmd_progress": "Co znasz na pamięć",
    "cmd_check": "Sprawdź swoją pamięć",
    "cmd_forgot": "Usuń oznaczenie zapamiętania",
    "cmd_streak": "Twoja seria dni",
    "cmd_leaderboard": "Najlepsi w tym tygodniu",
    "cmd_profile": "Twój profil i ustawienia",

    # Shared wizard controls
    "wizard_cancelled": "Anulowano.",
    "wizard_nothing_to_cancel": "Nie ma czego anulować.",
    "wizard_invalid_input": "Nie zrozumiałem. Spróbuj ponownie albo wyślij /cancel.",
    "ref_invalid": "Nie rozpoznaję takiego odnośnika. Spróbuj czegoś w rodzaju 67, 67:1-8 lub dżuz 30.",
    "btn_cancel": "Anuluj",
    "btn_back": "Wstecz",
    "btn_confirm": "Potwierdź",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "Pon",
    "day_tue": "Wt",
    "day_wed": "Śr",
    "day_thu": "Czw",
    "day_fri": "Pt",
    "day_sat": "Sob",
    "day_sun": "Nd",

    # Profile (B1-B3)
    "profile_title": "Twój profil",
    "profile_name_set": "Nazwa: {name}",
    "profile_name_unset": "Nazwa: nie ustawiono",
    "profile_leaderboard_on": "Ranking: jesteś widoczny",
    "profile_leaderboard_off": "Ranking: jesteś ukryty",
    "profile_timezone_set": "Strefa czasowa: UTC{offset}",
    "profile_timezone_unset": "Strefa czasowa: nie ustawiono",
    "profile_reminder_set": "Codzienne przypomnienie: {time}",
    "profile_reminder_unset": "Codzienne przypomnienie: wyłączone",
    "profile_plan_active": "Plan: {target} — dzień {day} z {total}",
    "profile_plan_none": "Plan: jeszcze żaden. Zacznij go przez /memorize.",
    "btn_edit_name": "Zmień nazwę",
    "btn_join_board": "Dołącz do rankingu",
    "btn_leave_board": "Opuść ranking",
    "btn_edit_timezone": "Zmień strefę czasową",
    "btn_edit_reminder": "Zmień godzinę przypomnienia",
    "name_prompt": "Wyślij nazwę, pod którą chcesz widnieć w rankingu.",
    "name_invalid": "Użyj od {min} do {max} znaków.",
    "name_saved": "Będziesz widnieć jako {name}.",
    "board_joined": "Jesteś już w rankingu.",
    "board_left": "Zostałeś usunięty z rankingu.",
    "timezone_prompt": (
        "Wybierz swoje przesunięcie względem UTC. Decyduje ono, kiedy dla serii "
        "zaczyna się twój dzień i kiedy przychodzi dzienna porcja."
    ),
    "timezone_saved": "Strefa czasowa ustawiona na UTC{offset}.",
    "reminder_prompt": "Wyślij godzinę, o której chcesz dzienną porcję, w formacie 24-godzinnym, np. 07:30.",
    "reminder_invalid": "Wyślij godzinę w formacie 24-godzinnym, np. 07:30.",
    "reminder_saved": "Codzienne przypomnienie ustawione na {time}.",
    "btn_reminder_off": "Wyłącz przypomnienia",
    "reminder_off": "Codzienne przypomnienia są wyłączone.",

    # Progress and /forgot (C3)
    "progress_title": "Co znasz na pamięć",
    "progress_surah_line": "{name}: {done}/{total} wersetów — {pct}%",
    "progress_juz_line": "Dżuz {n}: {pct}%",
    "progress_quran_line": "Cały Koran: {pct}%",
    "progress_empty": (
        "Nic jeszcze nie zostało oznaczone. Skończ porcję i dotknij «Znam na "
        "pamięć» albo zacznij plan przez /memorize."
    ),
    "forgot_usage": "Wyślij, co odznaczyć, na przykład /forgot 67:5-6.",
    "forgot_done": "Odznaczono: {ref}.",
    "forgot_nothing": "Tego nie oznaczyłeś jako zapamiętane.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "Czego chcesz nauczyć się na pamięć?",
    "btn_target_surah": "Surę",
    "btn_target_juz": "Dżuz",
    "btn_target_range": "Zakres",
    "memorize_surah_prompt": "Wyślij numer sury, na przykład 67.",
    "memorize_juz_prompt": "Wyślij numer dżuzu, od 1 do 30.",
    "memorize_range_prompt": "Wyślij zakres, na przykład 67:1-68:5.",
    "memorize_choose_pace": "Ile chcesz robić każdego dnia?",
    "btn_pace_auto": "Wybierz za mnie",
    "memorize_pace_prompt": "Wyślij, ile wersetów dziennie.",
    "memorize_pace_invalid": "Wyślij liczbę od {min} do {max}.",
    "memorize_choose_days": "W które dni chcesz się uczyć?",
    "btn_days_daily": "Codziennie",
    "btn_days_weekdays": "Dni robocze",
    "btn_days_custom": "Wybierz dni",
    "memorize_days_prompt": "Dotknij wybranych dni, a potem potwierdź.",
    "memorize_preview_title": "Liczba dni: {days}, od {start} do {end}:",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Zacznij ten plan",
    "plan_saved": "Plan jest gotowy. Pierwsza porcja przyjdzie {first_date}.",
    "plan_exists": "Masz już aktywny plan. Najpierw go wstrzymaj albo porzuć.",
    "btn_pause_plan": "Wstrzymaj plan",
    "btn_resume_plan": "Wznów plan",
    "btn_abandon_plan": "Porzuć plan",
    "plan_paused": "Plan wstrzymany. Wznów go kiedy zechcesz przez /profile.",
    "plan_resumed": "Plan wznowiony.",
    "plan_abandoned": "Plan porzucony.",
    "plan_complete": "Ukończyłeś {target}. Niech Allah to od ciebie przyjmie.",
    "drill_title": "{ref} — dzień {day} z {total}",
    "drill_none_today": "Na dziś nic nie zaplanowano.",
    "btn_start_drill": "Zacznij dzisiejszą porcję",
    "btn_know_by_heart": "✅ Znam na pamięć",
    "know_confirmed": "{ref} oznaczone jako zapamiętane. Jesteś na {pct}%.",
    "know_already": "To już było oznaczone.",

    # Recall check (E2, E3)
    "check_question": "Jak brzmi dalszy ciąg?",
    "check_usage": "Wyślij, co sprawdzić, na przykład /check 67.",
    "check_correct": "Poprawnie.",
    "check_wrong": "Nie do końca. Dalej brzmi to tak: {correct}",
    "check_already_today": (
        "Dzisiejszą sesję masz już zaliczoną ze sprawdzianu pamięci — sprawdzaj "
        "się, ile chcesz, tylko nie policzy się to drugi raz."
    ),
    "btn_check_start": "Sprawdź mnie",

    # Streaks (G2, G3)
    "streak_title": "Twoja seria",
    "streak_current": "Obecna seria, dni: {n}",
    "streak_longest": "Najdłuższa seria, dni: {n}",
    "streak_none": "Nie masz jeszcze serii. Skończ dziś porcję albo zdaj sprawdzian pamięci, żeby ją zacząć.",
    "streak_graph_caption": "Ostatnie 12 tygodni",
    "streak_milestone_7": "Cały tydzień. Tu zaczyna się nawyk.",
    "streak_milestone_30": "Trzydzieści dni. Regularność jest teraz po twojej stronie.",
    "streak_milestone_100": "Sto dni. Bardzo niewielu dochodzi tak daleko.",
    "streak_milestone_365": "Cały rok, każdego dnia. Niech Allah zachowa to, czego się nauczyłeś.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "Ranking tego tygodnia",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "Ty: {rank}. — {sessions}",
    "leaderboard_empty": "W tym tygodniu nikt jeszcze nie ukończył sesji. Bądź pierwszy.",
    "leaderboard_not_opted_in": "Nie ma cię w rankingu. Dołącz przez /profile.",
}
