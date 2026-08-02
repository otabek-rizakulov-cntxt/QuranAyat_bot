# Russian — Русский

strings = {
    "welcome_intro": (
        "Отправьте мне номер суры и аята, например <b>2:255</b>, и я пришлю этот аят из "
        "Священного Корана.\n\n"
        "Можно также отправить диапазон, например <b>59:22-24</b>, чтобы получить "
        "объединённое аудио-чтение."
    ),
    "welcome_commands_header": "Команды:",
    "welcome_inline": (
        "Меня можно использовать в любом чате: наберите <b>@QuranAyat_bot</b> и ссылку на "
        "аят."
    ),
    "about": (
        "Этот бот позволяет читать Священный Коран в Telegram на многих языках.\n\n"
        "Переводы взяты с tanzil.net (см. ATTRIBUTIONS.md с указанием издания и "
        "переводчика). Аудио — чтение шейха Махмуда Халиля аль-Хусари (everyayah.com). "
        "Тафсир — «Тафсир аль-Джалалейн» (altafsir.com), доступен на английском языке.\n\n"
        "Сменить язык можно в любой момент командой /language."
    ),
    "ayah_not_found": "Такого аята не существует!",
    "range_too_large": "Слишком большой диапазон, запрашивайте не более {n} аятов за раз.",
    "choose_language": "Выберите язык:",
    "language_set": "Язык изменён на {lang}.",
    "choose_translation_language": "Выберите язык перевода:",
    "translation_language_set": "Язык перевода изменён на {lang}.",
    "choose_reciter": "Выберите чтеца:",
    "reciter_set": "Чтец изменён на {reciter}.",
    "btn_search_reciter": "Поиск по имени",
    "reciter_search_prompt": "Введите имя чтеца для поиска (например, «Судаис», «Басит»).",
    "reciter_search_no_matches": "Чтецов с таким именем не найдено — попробуйте ещё раз.",
    "reciter_search_results": "Результаты поиска:",
    "btn_set_reciter": "Выбрать этого чтеца",
    "reciter_inline_description": "Нажмите, чтобы выбрать этого чтеца",
    "tafsir_en_note": "\n\n(Тафсир доступен только на английском языке.)",
    "btn_translation": "Перевод",
    "btn_tafsir": "Тафсир",
    "btn_arabic": "Арабский",
    "btn_audio": "Аудио",
    "btn_previous": "Назад",
    "btn_random": "Случайный",
    "btn_next": "Далее",
    "page_label": "Страница {n} из {total}",
    "page_out_of_range": "Отправьте номер страницы от 1 до {total}, например /page 255.",
    "juz_out_of_range": "Отправьте номер джуза от 1 до {total}, например /juz 30.",
    "sajda_list_title": "Аяты земного поклона (саджда):",
    "btn_ayah_view": "По аятам",
    "btn_repeat": "Повтор",
    "reciter_group_recitation": "Чтецы",
    "reciter_group_riwayah": "Ривая",
    "reciter_group_translation": "Смысл",
    "riwayah_warning": "Примечание: это ривая Варша — чтение коранического текста, отличное от чтения Хафса, которое показано здесь в арабском тексте и переводах, поэтому звук не всегда будет совпадать со словами на экране.",
    "translation_audio_warning": "Примечание: эта запись — не чтение Корана, а озвученный перевод смыслов. Чтобы услышать арабское чтение, выберите чтеца во вкладке «Чтецы».",
    "cmd_index": "Список всех сур",
    "cmd_page": "Читать страницу мусхафа",
    "cmd_juz": "Открыть джуз",
    "cmd_sajda": "Аяты земного поклона",
    "cmd_random": "Случайный аят",
    "cmd_language": "Сменить язык",
    "cmd_translation": "Сменить язык перевода",
    "cmd_reciter": "Сменить чтеца",
    "cmd_about": "Источники и благодарности",
    "quran_name": "Коран",

    # --- Hifz platform ---------------------------------------------------------

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Начать план заучивания",
    "cmd_progress": "Что вы выучили",
    "cmd_check": "Проверить память",
    "cmd_forgot": "Снять отметку о заучивании",
    "cmd_streak": "Ваша серия дней",
    "cmd_leaderboard": "Лучшие за эту неделю",
    "cmd_profile": "Ваш профиль и настройки",

    # Shared wizard controls
    "wizard_cancelled": "Отменено.",
    "wizard_nothing_to_cancel": "Отменять нечего.",
    "wizard_invalid_input": "Я не понял. Попробуйте ещё раз или отправьте /cancel.",
    "ref_invalid": "Не удалось распознать ссылку. Попробуйте, например, 67, 67:1-8 или джуз 30.",
    "btn_cancel": "Отмена",
    "btn_back": "Назад",
    "btn_confirm": "Подтвердить",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "Пн",
    "day_tue": "Вт",
    "day_wed": "Ср",
    "day_thu": "Чт",
    "day_fri": "Пт",
    "day_sat": "Сб",
    "day_sun": "Вс",

    # Profile (B1-B3)
    "profile_title": "Ваш профиль",
    "profile_name_set": "Имя: {name}",
    "profile_name_unset": "Имя: не задано",
    "profile_leaderboard_on": "Рейтинг: вы в списке",
    "profile_leaderboard_off": "Рейтинг: вы скрыты",
    "profile_timezone_set": "Часовой пояс: UTC{offset}",
    "profile_timezone_unset": "Часовой пояс: не задан",
    "profile_reminder_set": "Ежедневное напоминание: {time}",
    "profile_reminder_unset": "Ежедневное напоминание: выключено",
    "profile_plan_active": "План: {target} — день {day} из {total}",
    "profile_plan_none": "План: пока нет. Начните его командой /memorize.",
    "btn_edit_name": "Изменить имя",
    "btn_join_board": "Войти в рейтинг",
    "btn_leave_board": "Выйти из рейтинга",
    "btn_edit_timezone": "Изменить часовой пояс",
    "btn_edit_reminder": "Изменить время напоминания",
    "name_prompt": "Отправьте имя, под которым вы хотите отображаться в рейтинге.",
    "name_invalid": "Используйте от {min} до {max} символов.",
    "name_saved": "Вы будете отображаться как {name}.",
    "board_joined": "Теперь вы в рейтинге.",
    "board_left": "Вы убраны из рейтинга.",
    "timezone_prompt": (
        "Выберите своё смещение от UTC. От него зависит, когда начинается ваш день "
        "для серии и когда приходит дневная порция."
    ),
    "timezone_saved": "Часовой пояс установлен: UTC{offset}.",
    "reminder_prompt": "Отправьте время, когда присылать дневную порцию, в 24-часовом формате, например 07:30.",
    "reminder_invalid": "Отправьте время в 24-часовом формате, например 07:30.",
    "reminder_saved": "Ежедневное напоминание установлено на {time}.",
    "btn_reminder_off": "Выключить напоминания",
    "reminder_off": "Ежедневные напоминания выключены.",

    # Progress and /forgot (C3)
    "progress_title": "Что вы выучили",
    "progress_surah_line": "{name}: {done}/{total} аятов — {pct}%",
    "progress_juz_line": "Джуз {n}: {pct}%",
    "progress_quran_line": "Весь Коран: {pct}%",
    "progress_empty": (
        "Пока ничего не отмечено. Завершите порцию и нажмите «Знаю наизусть» "
        "или начните план командой /memorize."
    ),
    "forgot_usage": "Отправьте, с чего снять отметку, например /forgot 67:5-6.",
    "forgot_done": "Отметка снята: {ref}.",
    "forgot_nothing": "Это не было отмечено как выученное.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "Что вы хотите выучить наизусть?",
    "btn_target_surah": "Суру",
    "btn_target_juz": "Джуз",
    "btn_target_range": "Диапазон",
    "memorize_surah_prompt": "Отправьте номер суры, например 67.",
    "memorize_juz_prompt": "Отправьте номер джуза, от 1 до 30.",
    "memorize_range_prompt": "Отправьте диапазон, например 67:1-68:5.",
    "memorize_choose_pace": "Сколько вы хотите проходить каждый день?",
    "btn_pace_auto": "Выбрать за меня",
    "memorize_pace_prompt": "Отправьте, сколько аятов в день.",
    "memorize_pace_invalid": "Отправьте число от {min} до {max}.",
    "memorize_choose_days": "В какие дни вы хотите заниматься?",
    "btn_days_daily": "Каждый день",
    "btn_days_weekdays": "Будни",
    "btn_days_custom": "Выбрать дни",
    "memorize_days_prompt": "Отметьте нужные дни и подтвердите.",
    "memorize_preview_title": "Дней: {days}, с {start} по {end}:",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Начать этот план",
    "plan_saved": "План готов. Первая порция придёт {first_date}.",
    "plan_exists": "У вас уже есть активный план. Сначала приостановите или отмените его.",
    "btn_pause_plan": "Приостановить план",
    "btn_resume_plan": "Продолжить план",
    "btn_abandon_plan": "Отменить план",
    "plan_paused": "План приостановлен. Продолжить можно в любой момент через /profile.",
    "plan_resumed": "План возобновлён.",
    "plan_abandoned": "План отменён.",
    "plan_complete": "Вы завершили {target}. Да примет это Аллах от вас.",
    "drill_title": "{ref} — день {day} из {total}",
    "drill_none_today": "На сегодня ничего не запланировано.",
    "btn_start_drill": "Начать порцию дня",
    "btn_know_by_heart": "✅ Знаю наизусть",
    "know_confirmed": "{ref} отмечено как выученное. Ваш прогресс: {pct}%.",
    "know_already": "Это уже было отмечено.",

    # Recall check (E2, E3)
    "check_question": "Как это продолжается?",
    "check_usage": "Отправьте, что проверить, например /check 67.",
    "check_correct": "Верно.",
    "check_wrong": "Не совсем. Продолжение: {correct}",
    "check_already_today": (
        "Сегодняшнее занятие уже засчитано по проверке памяти — проверяйте себя "
        "сколько угодно, просто дважды это не засчитается."
    ),
    "btn_check_start": "Проверить меня",

    # Streaks (G2, G3)
    "streak_title": "Ваша серия",
    "streak_current": "Текущая серия, дней: {n}",
    "streak_longest": "Лучшая серия, дней: {n}",
    "streak_none": "Серии пока нет. Завершите порцию или пройдите проверку памяти сегодня, чтобы её начать.",
    "streak_graph_caption": "Последние 12 недель",
    "streak_milestone_7": "Целая неделя. Именно здесь рождается привычка.",
    "streak_milestone_30": "Тридцать дней. Постоянство теперь на вашей стороне.",
    "streak_milestone_100": "Сто дней. Так далеко доходят очень немногие.",
    "streak_milestone_365": "Целый год, каждый день без пропусков. Да сохранит Аллах то, что вы выучили.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "Рейтинг этой недели",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "Вы: {rank}. — {sessions}",
    "leaderboard_empty": "На этой неделе ещё никто не завершил занятие. Будьте первым.",
    "leaderboard_not_opted_in": "Вас нет в рейтинге. Присоединиться можно через /profile.",

    # --- Phase 2: group cluster (en/ru/uz/uz-Cyrl only) ---  # phase2
    'group_added': 'Ассаляму алейкум! Я могу вести ежедневный кружок заучивания в этой группе. Администратор, нажмите ниже для настройки.',
    'group_btn_setup': '⚙️ Настроить кружок',
    'group_setup_unknown': 'Я не знаю эту группу. Сначала добавьте меня в неё, затем нажмите ссылку настройки там.',
    'group_setup_not_admin': 'Настроить меня может только администратор этой группы.',
    'group_topic_prompt': 'Как назвать ежедневную тему? Пришлите название.',
    'group_topic_created': 'Тема <b>{name}</b> создана. Буду публиковать там каждый день.',
    'group_topic_fallback': 'В этой группе нет тем, поэтому буду публиковать в основном чате.',
    'group_translation_prompt': 'Какой перевод использовать в ежедневных публикациях?',
    'group_board_unknown': 'Этого кружка больше не существует.',
    'group_board_not_member': 'Чтобы попасть в таблицу, нужно быть участником этой группы.',
    'group_board_joined': 'Вы теперь в недельной таблице группы.',
    # --- Phase 2 J4/J5 ---  # phase2
    'group_target_prompt': 'Что учить кружку? Пришлите суру (67), джуз (джуз 30) или диапазон (2:1-10).',
    'group_target_invalid': 'Не удалось распознать. Попробуйте номер суры, «джуз 30» или «2:1-10».',
    'group_pace_prompt': 'Сколько аятов в день?',
    'group_btn_pace_auto': 'Авто',
    'group_days_prompt': 'В какие дни публиковать?',
    'group_btn_daily': 'Каждый день',
    'group_btn_weekdays': 'Будни',
    'group_timezone_prompt': 'Какой у группы часовой пояс (UTC)?',
    'group_post_time_prompt': 'В какое местное время публиковать каждый день? (напр. 07:00)',
    'group_post_time_invalid': 'Пришлите время в формате 07:00.',
    'group_setup_done': 'Готово — {days} частей за {total} дней. Участники могут присоединиться к таблице здесь: {board_link}',
    # --- Phase 2 J6 board ---  # phase2
    'group_board_title': '📿 Кружок на этой неделе',
    'group_board_row': '{rank}. {name} — {sessions}',
    'group_board_empty': 'На этой неделе ещё никто не завершил занятие. Будьте первым!',
}
