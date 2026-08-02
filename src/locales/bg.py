# Bulgarian — Български

strings = {
    "welcome_intro": (
        "Изпрати ми номер на сура и знамение, например <b>2:255</b>, и ще ти изпратя това "
        "знамение от Свещения Коран.\n\n"
        "Можеш да изпратиш и диапазон като <b>59:22-24</b> за обединено аудио четене."
    ),
    "welcome_commands_header": "Команди:",
    "welcome_inline": (
        "Можеш да ме използваш във всеки чат: напиши <b>@QuranAyat_bot</b>, следвано от "
        "препратка."
    ),
    "about": (
        "Този бот ти позволява да четеш Свещения Коран в Telegram на много "
        "езици.\n\n"
        "Преводите са взети от tanzil.net (виж ATTRIBUTIONS.md за изданието и "
        "преводача на всеки превод). Аудиото е четене на шейх Махмуд Халил "
        "ал-Хусари (everyayah.com). Тафсирът е Тафсир ал-Джалалайн "
        "(altafsir.com), достъпен на английски.\n\n"
        "Смени езика по всяко време с /language."
    ),
    "ayah_not_found": "Такова знамение не съществува!",
    "range_too_large": "Диапазонът е твърде голям, заявявай най-много {n} знамения наведнъж.",
    "choose_language": "Избери своя език:",
    "language_set": "Езикът е сменен на {lang}.",
    "choose_translation_language": "Изберете език на превода:",
    "translation_language_set": "Езикът на превода е зададен на {lang}.",
    "choose_reciter": "Изберете четец:",
    "reciter_set": "Четецът е зададен на {reciter}.",
    "btn_search_reciter": "Търсене по име",
    "reciter_search_prompt": "Въведете име на четец за търсене (напр. «Судаис», «Абдул Басит»).",
    "reciter_search_no_matches": "Няма четец с това име — опитайте отново.",
    "reciter_search_results": "Резултати от търсенето:",
    "btn_set_reciter": "Задай като мой четец",
    "reciter_inline_description": "Докоснете, за да го зададете като ваш четец",
    "tafsir_en_note": "\n\n(Тафсирът е достъпен само на английски.)",
    "btn_translation": "Превод",
    "btn_tafsir": "Тафсир",
    "btn_arabic": "Арабски",
    "btn_audio": "Аудио",
    "btn_previous": "Назад",
    "btn_random": "Случайно",
    "btn_next": "Напред",
    "page_label": "Страница {n} от {total}",
    "page_out_of_range": "Изпратете номер на страница между 1 и {total}, например /page 255.",
    "juz_out_of_range": "Изпратете номер на джуз между 1 и {total}, например /juz 30.",
    "sajda_list_title": "Айети на поклон (саджда):",
    "btn_ayah_view": "Изглед по айети",
    "btn_repeat": "Повтори",
    "reciter_group_recitation": "Четци",
    "reciter_group_riwayah": "Ривая",
    "reciter_group_translation": "Значение",
    "riwayah_warning": "Забележка: това е риваята на Уарш — прочит на кораничния текст, различен от този на Хафс, показан тук в арабския текст и преводите, затова звукът невинаги ще съвпада с думите на екрана.",
    "translation_audio_warning": "Забележка: този запис не е коранично четене, а прочит на преведеното значение на глас. Изберете от раздела «Четци», за да чуете арабското четене.",
    "cmd_index": "Списък на всички сури",
    "cmd_page": "Четене на страница от мусхафа",
    "cmd_juz": "Отваряне на джуз",
    "cmd_sajda": "Айети на поклон",
    "cmd_random": "Случайно знамение",
    "cmd_language": "Смяна на езика",
    "cmd_translation": "Смяна на езика на превода",
    "cmd_reciter": "Смяна на четеца",
    "cmd_about": "Източници и благодарности",
    "quran_name": "Коран",

    # --- Hifz platform ---------------------------------------------------------

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Започни план за заучаване",
    "cmd_progress": "Какво си научил наизуст",
    "cmd_check": "Провери паметта си",
    "cmd_forgot": "Премахни отметка за заучено",
    "cmd_streak": "Твоята серия от дни",
    "cmd_leaderboard": "Най-добрите тази седмица",
    "cmd_profile": "Твоят профил и настройки",

    # Shared wizard controls
    "wizard_cancelled": "Отменено.",
    "wizard_nothing_to_cancel": "Няма какво да се отмени.",
    "wizard_invalid_input": "Не разбрах. Опитай отново или изпрати /cancel.",
    "ref_invalid": "Не разпознавам такава препратка. Опитай нещо като 67, 67:1-8 или джуз 30.",
    "btn_cancel": "Отказ",
    "btn_back": "Назад",
    "btn_confirm": "Потвърди",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "Пн",
    "day_tue": "Вт",
    "day_wed": "Ср",
    "day_thu": "Чт",
    "day_fri": "Пт",
    "day_sat": "Сб",
    "day_sun": "Нд",

    # Profile (B1-B3)
    "profile_title": "Твоят профил",
    "profile_name_set": "Име: {name}",
    "profile_name_unset": "Име: не е зададено",
    "profile_leaderboard_on": "Класация: показван си",
    "profile_leaderboard_off": "Класация: скрит си",
    "profile_timezone_set": "Часова зона: UTC{offset}",
    "profile_timezone_unset": "Часова зона: не е зададена",
    "profile_reminder_set": "Дневно напомняне: {time}",
    "profile_reminder_unset": "Дневно напомняне: изключено",
    "profile_plan_active": "План: {target} — ден {day} от {total}",
    "profile_plan_none": "План: още няма. Започни с /memorize.",
    "btn_edit_name": "Смяна на името",
    "btn_join_board": "Влез в класацията",
    "btn_leave_board": "Напусни класацията",
    "btn_edit_timezone": "Смяна на часовата зона",
    "btn_edit_reminder": "Смяна на часа за напомняне",
    "name_prompt": "Изпрати името, под което искаш да се показваш в класацията.",
    "name_invalid": "Използвай между {min} и {max} знака.",
    "name_saved": "Ще се показваш като {name}.",
    "board_joined": "Вече си в класацията.",
    "board_left": "Премахнат си от класацията.",
    "timezone_prompt": (
        "Избери своето отместване спрямо UTC. То определя кога започва денят ти "
        "за сериите и кога пристига дневната ти порция."
    ),
    "timezone_saved": "Часовата зона е зададена на UTC{offset}.",
    "reminder_prompt": "Изпрати часа, в който искаш дневната си порция, в 24-часов формат, напр. 07:30.",
    "reminder_invalid": "Изпрати час в 24-часов формат, напр. 07:30.",
    "reminder_saved": "Дневното напомняне е зададено за {time}.",
    "btn_reminder_off": "Изключи напомнянията",
    "reminder_off": "Дневните напомняния са изключени.",

    # Progress and /forgot (C3)
    "progress_title": "Какво си научил наизуст",
    "progress_surah_line": "{name}: {done}/{total} айета — {pct}%",
    "progress_juz_line": "Джуз {n}: {pct}%",
    "progress_quran_line": "Целият Коран: {pct}%",
    "progress_empty": (
        "Още нищо не е отбелязано. Завърши порция и натисни «Знам го наизуст» "
        "или започни план с /memorize."
    ),
    "forgot_usage": "Изпрати какво да премахна, например /forgot 67:5-6.",
    "forgot_done": "Отметката е премахната: {ref}.",
    "forgot_nothing": "Това не беше отбелязано като заучено.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "Какво искаш да научиш наизуст?",
    "btn_target_surah": "Сура",
    "btn_target_juz": "Джуз",
    "btn_target_range": "Диапазон",
    "memorize_surah_prompt": "Изпрати номера на сурата, например 67.",
    "memorize_juz_prompt": "Изпрати номера на джуза, от 1 до 30.",
    "memorize_range_prompt": "Изпрати диапазона, например 67:1-68:5.",
    "memorize_choose_pace": "Колко искаш да учиш всеки ден?",
    "btn_pace_auto": "Избери вместо мен",
    "memorize_pace_prompt": "Изпрати по колко айета на ден.",
    "memorize_pace_invalid": "Изпрати число между {min} и {max}.",
    "memorize_choose_days": "В кои дни искаш да учиш?",
    "btn_days_daily": "Всеки ден",
    "btn_days_weekdays": "Делнични дни",
    "btn_days_custom": "Избери дни",
    "memorize_days_prompt": "Докосни желаните дни и потвърди.",
    "memorize_preview_title": "Брой дни: {days}, от {start} до {end}:",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Започни този план",
    "plan_saved": "Планът е готов. Първата порция пристига на {first_date}.",
    "plan_exists": "Вече имаш активен план. Първо го постави на пауза или се откажи от него.",
    "btn_pause_plan": "Пауза на плана",
    "btn_resume_plan": "Продължи плана",
    "btn_abandon_plan": "Откажи плана",
    "plan_paused": "Планът е на пауза. Продължи го по всяко време от /profile.",
    "plan_resumed": "Планът е подновен.",
    "plan_abandoned": "Планът е прекратен.",
    "plan_complete": "Ти завърши {target}. Нека Аллах го приеме от теб.",
    "drill_title": "{ref} — ден {day} от {total}",
    "drill_none_today": "За днес няма нищо насрочено.",
    "btn_start_drill": "Започни днешната порция",
    "btn_know_by_heart": "✅ Знам го наизуст",
    "know_confirmed": "{ref} е отбелязано като заучено. Вече си на {pct}%.",
    "know_already": "Това вече беше отбелязано.",

    # Recall check (E2, E3)
    "check_question": "Как продължава това?",
    "check_usage": "Изпрати какво да проверя, например /check 67.",
    "check_correct": "Вярно.",
    "check_wrong": "Не съвсем. Продължава така: {correct}",
    "check_already_today": (
        "Днешната сесия вече ти е зачетена от проверка на паметта — изпитвай се "
        "колкото искаш, просто няма да се брои два пъти."
    ),
    "btn_check_start": "Изпитай ме",

    # Streaks (G2, G3)
    "streak_title": "Твоята серия",
    "streak_current": "Текуща серия, дни: {n}",
    "streak_longest": "Най-дълга серия, дни: {n}",
    "streak_none": "Още нямаш серия. Завърши порция или мини проверка на паметта днес, за да я започнеш.",
    "streak_graph_caption": "Последните 12 седмици",
    "streak_milestone_7": "Цяла седмица. Оттук започва навикът.",
    "streak_milestone_30": "Тридесет дни. Постоянството вече е на твоя страна.",
    "streak_milestone_100": "Сто дни. Много малко хора стигат дотук.",
    "streak_milestone_365": "Цяла година, всеки един ден. Нека Аллах опази това, което си научил.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "Класацията за тази седмица",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "Ти: {rank}. — {sessions}",
    "leaderboard_empty": "Тази седмица още никой не е завършил сесия. Бъди първият.",
    "leaderboard_not_opted_in": "Не си в класацията. Присъедини се от /profile.",
}
