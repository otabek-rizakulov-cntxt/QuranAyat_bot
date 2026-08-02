# Spanish — Español

strings = {
    "welcome_intro": (
        "Envíame un número de sura y aleya, por ejemplo <b>2:255</b>, y te responderé con "
        "ese versículo del Sagrado Corán.\n\n"
        "También puedes enviar un rango como <b>59:22-24</b> para obtener una recitación "
        "de audio combinada."
    ),
    "welcome_commands_header": "Comandos:",
    "welcome_inline": (
        "Puedes usarme en cualquier chat: escribe <b>@QuranAyat_bot</b> seguido de una "
        "referencia."
    ),
    "about": (
        "Este bot te permite explorar el Sagrado Corán en Telegram en muchos "
        "idiomas.\n\n"
        "Las traducciones provienen de tanzil.net (consulta ATTRIBUTIONS.md "
        "para ver la edición y el traductor de cada traducción). El audio es "
        "una recitación del jeque Mahmud Jalil al-Husari (everyayah.com). El "
        "tafsir es el Tafsir al-Yalalayn (altafsir.com), disponible en inglés.\n\n"
        "Cambia de idioma en cualquier momento con /language."
    ),
    "ayah_not_found": "¡Esa aleya no existe!",
    "range_too_large": "Rango demasiado grande, solicita como máximo {n} aleyas a la vez.",
    "choose_language": "Elige tu idioma:",
    "language_set": "Idioma cambiado a {lang}.",
    "choose_translation_language": "Elige el idioma de la traducción:",
    "translation_language_set": "Idioma de la traducción cambiado a {lang}.",
    "choose_reciter": "Elige un recitador:",
    "reciter_set": "Recitador cambiado a {reciter}.",
    "btn_search_reciter": "Buscar por nombre",
    "reciter_search_prompt": "Escribe el nombre de un recitador para buscarlo (p. ej. «Sudais», «Abdul Basit»).",
    "reciter_search_no_matches": "Ningún recitador coincide con ese nombre — inténtalo de nuevo.",
    "reciter_search_results": "Resultados de la búsqueda:",
    "btn_set_reciter": "Elegir como mi recitador",
    "reciter_inline_description": "Toca para elegirlo como tu recitador",
    "tafsir_en_note": "\n\n(El tafsir solo está disponible en inglés.)",
    "btn_translation": "Traducción",
    "btn_tafsir": "Tafsir",
    "btn_arabic": "Árabe",
    "btn_audio": "Audio",
    "btn_previous": "Anterior",
    "btn_random": "Aleatorio",
    "btn_next": "Siguiente",
    "page_label": "Página {n} de {total}",
    "page_out_of_range": "Envía un número de página entre 1 y {total}, por ejemplo /page 255.",
    "juz_out_of_range": "Envía un número de yuz entre 1 y {total}, por ejemplo /juz 30.",
    "sajda_list_title": "Aleyas de postración (sayda):",
    "btn_ayah_view": "Vista por aleyas",
    "btn_repeat": "Repetir",
    "reciter_group_recitation": "Recitadores",
    "reciter_group_riwayah": "Riwāya",
    "reciter_group_translation": "Significado",
    "riwayah_warning": "Nota: esta es la riwāya de Warsh, una lectura del texto coránico distinta de la de Hafs que se muestra aquí en el texto árabe y en las traducciones, por lo que el audio no siempre coincidirá con las palabras en pantalla.",
    "translation_audio_warning": "Nota: esta grabación no es recitación del Corán, sino la lectura en voz alta del significado traducido. Elige en la pestaña «Recitadores» para escuchar la recitación en árabe.",
    "cmd_index": "Lista de todas las suras",
    "cmd_page": "Leer una página del mushaf",
    "cmd_juz": "Abrir un yuz",
    "cmd_sajda": "Aleyas de postración",
    "cmd_random": "Una aleya al azar",
    "cmd_language": "Cambiar de idioma",
    "cmd_translation": "Cambiar el idioma de la traducción",
    "cmd_reciter": "Cambiar de recitador",
    "cmd_about": "Fuentes y créditos",
    "quran_name": "Corán",

    # --- Hifz platform ---------------------------------------------------------

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Empezar un plan de hifz",
    "cmd_progress": "Lo que has memorizado",
    "cmd_check": "Poner a prueba tu memoria",
    "cmd_forgot": "Desmarcar un rango memorizado",
    "cmd_streak": "Tu racha diaria",
    "cmd_leaderboard": "Los mejores de esta semana",
    "cmd_profile": "Tu perfil y tus ajustes",

    # Shared wizard controls
    "wizard_cancelled": "Cancelado.",
    "wizard_nothing_to_cancel": "No hay nada que cancelar.",
    "wizard_invalid_input": "No he entendido eso. Inténtalo de nuevo o envía /cancel.",
    "ref_invalid": "Esa referencia no la reconozco. Prueba con algo como 67, 67:1-8 o juz 30.",
    "btn_cancel": "Cancelar",
    "btn_back": "Atrás",
    "btn_confirm": "Confirmar",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "lun",
    "day_tue": "mar",
    "day_wed": "mié",
    "day_thu": "jue",
    "day_fri": "vie",
    "day_sat": "sáb",
    "day_sun": "dom",

    # Profile (B1-B3)
    "profile_title": "Tu perfil",
    "profile_name_set": "Nombre: {name}",
    "profile_name_unset": "Nombre: sin definir",
    "profile_leaderboard_on": "Clasificación: apareces en ella",
    "profile_leaderboard_off": "Clasificación: estás oculto",
    "profile_timezone_set": "Zona horaria: UTC{offset}",
    "profile_timezone_unset": "Zona horaria: sin definir",
    "profile_reminder_set": "Recordatorio diario: {time}",
    "profile_reminder_unset": "Recordatorio diario: desactivado",
    "profile_plan_active": "Plan: {target} — día {day} de {total}",
    "profile_plan_none": "Plan: ninguno todavía. Empieza uno con /memorize.",
    "btn_edit_name": "Cambiar nombre",
    "btn_join_board": "Unirme a la clasificación",
    "btn_leave_board": "Salir de la clasificación",
    "btn_edit_timezone": "Cambiar zona horaria",
    "btn_edit_reminder": "Cambiar hora del aviso",
    "name_prompt": "Envía el nombre con el que quieres aparecer en la clasificación.",
    "name_invalid": "Usa entre {min} y {max} caracteres.",
    "name_saved": "Aparecerás como {name}.",
    "board_joined": "Ya estás en la clasificación.",
    "board_left": "Se te ha quitado de la clasificación.",
    "timezone_prompt": (
        "Elige tu diferencia con UTC. Determina cuándo empieza tu día para las "
        "rachas y cuándo llega tu porción diaria."
    ),
    "timezone_saved": "Zona horaria establecida en UTC{offset}.",
    "reminder_prompt": "Envía la hora a la que quieres tu porción diaria, en formato de 24 horas, p. ej. 07:30.",
    "reminder_invalid": "Envía una hora en formato de 24 horas, p. ej. 07:30.",
    "reminder_saved": "Recordatorio diario fijado a las {time}.",
    "btn_reminder_off": "Desactivar avisos",
    "reminder_off": "Los recordatorios diarios están desactivados.",

    # Progress and /forgot (C3)
    "progress_title": "Lo que has memorizado",
    "progress_surah_line": "{name}: {done}/{total} aleyas — {pct} %",
    "progress_juz_line": "Yuz {n}: {pct} %",
    "progress_quran_line": "Corán completo: {pct} %",
    "progress_empty": (
        "Todavía no hay nada marcado. Termina una porción y toca "
        "«Me lo sé de memoria», o empieza un plan con /memorize."
    ),
    "forgot_usage": "Envía lo que quieres desmarcar, por ejemplo /forgot 67:5-6.",
    "forgot_done": "{ref} desmarcado.",
    "forgot_nothing": "No tenías eso marcado como memorizado.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "¿Qué te gustaría memorizar?",
    "btn_target_surah": "Una sura",
    "btn_target_juz": "Un yuz",
    "btn_target_range": "Un rango",
    "memorize_surah_prompt": "Envía el número de la sura, por ejemplo 67.",
    "memorize_juz_prompt": "Envía el número del yuz, del 1 al 30.",
    "memorize_range_prompt": "Envía el rango, por ejemplo 67:1-68:5.",
    "memorize_choose_pace": "¿Cuánto quieres hacer cada día?",
    "btn_pace_auto": "Elige por mí",
    "memorize_pace_prompt": "Envía cuántas aleyas al día.",
    "memorize_pace_invalid": "Envía un número entre {min} y {max}.",
    "memorize_choose_days": "¿Qué días quieres estudiar?",
    "btn_days_daily": "Todos los días",
    "btn_days_weekdays": "Entre semana",
    "btn_days_custom": "Elegir días",
    "memorize_days_prompt": "Toca los días que quieras y luego confirma.",
    "memorize_preview_title": "{days} días, del {start} al {end}:",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Empezar este plan",
    "plan_saved": "Tu plan está listo. La primera porción llega el {first_date}.",
    "plan_exists": "Ya tienes un plan en marcha. Páusalo o abandónalo primero.",
    "btn_pause_plan": "Pausar el plan",
    "btn_resume_plan": "Reanudar el plan",
    "btn_abandon_plan": "Abandonar el plan",
    "plan_paused": "Plan en pausa. Reanúdalo cuando quieras desde /profile.",
    "plan_resumed": "Plan reanudado.",
    "plan_abandoned": "Plan abandonado.",
    "plan_complete": "Has terminado {target}. Que Allah te lo acepte.",
    "drill_title": "{ref} — día {day} de {total}",
    "drill_none_today": "Hoy no hay nada programado.",
    "btn_start_drill": "Porción de hoy",
    "btn_know_by_heart": "✅ Me lo sé de memoria",
    "know_confirmed": "{ref} marcado como memorizado. Vas por el {pct} %.",
    "know_already": "Ya lo habías marcado.",

    # Recall check (E2, E3)
    "check_question": "¿Cómo continúa?",
    "check_usage": "Envía lo que quieres poner a prueba, por ejemplo /check 67.",
    "check_correct": "Correcto.",
    "check_wrong": "No exactamente. Continúa así: {correct}",
    "check_already_today": (
        "Ya has conseguido la sesión de hoy con una prueba de memoria — ponte a "
        "prueba cuantas veces quieras, solo que no contará dos veces."
    ),
    "btn_check_start": "Ponme a prueba",

    # Streaks (G2, G3)
    "streak_title": "Tu racha",
    "streak_current": "Racha actual: {n}",
    "streak_longest": "Racha más larga: {n}",
    "streak_none": "Todavía no hay racha. Termina una porción o supera una prueba de memoria hoy para empezar una.",
    "streak_graph_caption": "Las últimas 12 semanas",
    "streak_milestone_7": "Una semana completa. Aquí es donde empieza el hábito.",
    "streak_milestone_30": "Treinta días. La constancia ya está de tu parte.",
    "streak_milestone_100": "Cien días. Muy poca gente llega hasta aquí.",
    "streak_milestone_365": "Un año entero, día tras día. Que Allah preserve lo que has aprendido.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "Clasificación de esta semana",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "Tú: {rank}. — {sessions}",
    "leaderboard_empty": "Nadie ha completado una sesión esta semana todavía. Sé el primero.",
    "leaderboard_not_opted_in": "No estás en la clasificación. Únete desde /profile.",
}
