# French — Français

strings = {
    "welcome_intro": (
        "Envoyez-moi un numéro de sourate et de verset, par exemple <b>2:255</b>, et je "
        "vous répondrai avec ce verset du Saint Coran.\n\n"
        "Vous pouvez aussi envoyer une plage comme <b>59:22-24</b> pour une récitation "
        "audio combinée."
    ),
    "welcome_commands_header": "Commandes :",
    "welcome_inline": (
        "Vous pouvez m'utiliser dans n'importe quelle discussion : tapez "
        "<b>@QuranAyat_bot</b> suivi d'une référence."
    ),
    "about": (
        "Ce bot vous permet d'explorer le Saint Coran sur Telegram en plusieurs "
        "langues.\n\n"
        "Les traductions proviennent de tanzil.net (voir ATTRIBUTIONS.md pour "
        "l'édition et le traducteur de chaque traduction). L'audio est une "
        "récitation du cheikh Mahmoud Khalil al-Hussary (everyayah.com). Le "
        "tafsir est le Tafsir al-Jalalayn (altafsir.com), disponible en anglais.\n\n"
        "Changez de langue à tout moment avec /language."
    ),
    "ayah_not_found": "Ce verset n'existe pas !",
    "range_too_large": "Plage trop grande, veuillez demander au maximum {n} versets à la fois.",
    "choose_language": "Choisissez votre langue :",
    "language_set": "Langue définie sur {lang}.",
    "choose_translation_language": "Choisissez la langue de traduction :",
    "translation_language_set": "Langue de traduction définie sur {lang}.",
    "choose_reciter": "Choisissez un récitateur :",
    "reciter_set": "Récitateur défini sur {reciter}.",
    "btn_search_reciter": "Rechercher par nom",
    "reciter_search_prompt": "Tapez le nom d'un récitateur pour le rechercher (ex. « Soudais », « Abdul Basit »).",
    "reciter_search_no_matches": "Aucun récitateur ne correspond à ce nom — réessayez.",
    "reciter_search_results": "Résultats de la recherche :",
    "btn_set_reciter": "Définir comme mon récitateur",
    "reciter_inline_description": "Appuyez pour le définir comme votre récitateur",
    "tafsir_en_note": "\n\n(Le tafsir n'est disponible qu'en anglais.)",
    "btn_translation": "Traduction",
    "btn_tafsir": "Tafsir",
    "btn_arabic": "Arabe",
    "btn_audio": "Audio",
    "btn_previous": "Précédent",
    "btn_random": "Aléatoire",
    "btn_next": "Suivant",
    "page_label": "Page {n} sur {total}",
    "page_out_of_range": "Envoie un numéro de page entre 1 et {total}, par exemple /page 255.",
    "juz_out_of_range": "Envoie un numéro de juz entre 1 et {total}, par exemple /juz 30.",
    "sajda_list_title": "Versets de prosternation (sajda) :",
    "btn_ayah_view": "Vue par versets",
    "btn_repeat": "Répéter",
    "reciter_group_recitation": "Récitateurs",
    "reciter_group_riwayah": "Riwāya",
    "reciter_group_translation": "Sens",
    "riwayah_warning": "Remarque : il s'agit de la riwāya de Warsh — une lecture du texte coranique différente de celle de Hafs affichée ici dans le texte arabe et les traductions ; l'audio ne correspondra donc pas toujours aux mots à l'écran.",
    "translation_audio_warning": "Remarque : cet enregistrement n'est pas une récitation du Coran, mais la lecture à voix haute du sens traduit. Choisis dans l'onglet « Récitateurs » pour entendre la récitation en arabe.",
    "cmd_index": "Liste de toutes les sourates",
    "cmd_page": "Lire une page du mushaf",
    "cmd_juz": "Ouvrir un juz",
    "cmd_sajda": "Versets de prosternation",
    "cmd_random": "Un verset au hasard",
    "cmd_language": "Changer de langue",
    "cmd_translation": "Changer la langue de traduction",
    "cmd_reciter": "Changer de récitateur",
    "cmd_about": "Sources et remerciements",
    "quran_name": "Coran",

    # --- Hifz platform ---------------------------------------------------------

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Commencer un plan de hifz",
    "cmd_progress": "Ce que vous avez mémorisé",
    "cmd_check": "Tester votre mémoire",
    "cmd_forgot": "Retirer une plage mémorisée",
    "cmd_streak": "Votre série quotidienne",
    "cmd_leaderboard": "Les meilleurs de la semaine",
    "cmd_profile": "Votre profil et vos réglages",

    # Shared wizard controls
    "wizard_cancelled": "Annulé.",
    "wizard_nothing_to_cancel": "Il n'y a rien à annuler.",
    "wizard_invalid_input": "Je n'ai pas compris. Réessayez, ou envoyez /cancel.",
    "ref_invalid": "Ce n'est pas une référence que je reconnais. Essayez plutôt 67, 67:1-8 ou juz 30.",
    "btn_cancel": "Annuler",
    "btn_back": "Retour",
    "btn_confirm": "Confirmer",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "lun",
    "day_tue": "mar",
    "day_wed": "mer",
    "day_thu": "jeu",
    "day_fri": "ven",
    "day_sat": "sam",
    "day_sun": "dim",

    # Profile (B1-B3)
    "profile_title": "Votre profil",
    "profile_name_set": "Nom : {name}",
    "profile_name_unset": "Nom : non défini",
    "profile_leaderboard_on": "Classement : vous y figurez",
    "profile_leaderboard_off": "Classement : vous êtes masqué",
    "profile_timezone_set": "Fuseau horaire : UTC{offset}",
    "profile_timezone_unset": "Fuseau horaire : non défini",
    "profile_reminder_set": "Rappel quotidien : {time}",
    "profile_reminder_unset": "Rappel quotidien : désactivé",
    "profile_plan_active": "Plan : {target} — jour {day} sur {total}",
    "profile_plan_none": "Plan : aucun pour l'instant. Lancez-en un avec /memorize.",
    "btn_edit_name": "Changer de nom",
    "btn_join_board": "Rejoindre le classement",
    "btn_leave_board": "Quitter le classement",
    "btn_edit_timezone": "Changer de fuseau",
    "btn_edit_reminder": "Changer le rappel",
    "name_prompt": "Envoyez le nom sous lequel vous voulez apparaître au classement.",
    "name_invalid": "Utilisez entre {min} et {max} caractères.",
    "name_saved": "Vous apparaîtrez sous le nom {name}.",
    "board_joined": "Vous êtes maintenant au classement.",
    "board_left": "Vous avez été retiré du classement.",
    "timezone_prompt": (
        "Choisissez votre décalage UTC. Il détermine quand votre journée commence "
        "pour les séries et quand votre portion quotidienne arrive."
    ),
    "timezone_saved": "Fuseau horaire réglé sur UTC{offset}.",
    "reminder_prompt": "Envoyez l'heure à laquelle vous voulez votre portion quotidienne, au format 24 h, par exemple 07:30.",
    "reminder_invalid": "Envoyez une heure au format 24 h, par exemple 07:30.",
    "reminder_saved": "Rappel quotidien réglé à {time}.",
    "btn_reminder_off": "Désactiver les rappels",
    "reminder_off": "Les rappels quotidiens sont désactivés.",

    # Progress and /forgot (C3)
    "progress_title": "Ce que vous avez mémorisé",
    "progress_surah_line": "{name} : {done}/{total} versets — {pct} %",
    "progress_juz_line": "Juz {n} : {pct} %",
    "progress_quran_line": "Coran entier : {pct} %",
    "progress_empty": (
        "Rien de marqué pour l'instant. Terminez une portion et appuyez sur "
        "« Je le sais par cœur », ou lancez un plan avec /memorize."
    ),
    "forgot_usage": "Envoyez ce qu'il faut retirer, par exemple /forgot 67:5-6.",
    "forgot_done": "{ref} retiré.",
    "forgot_nothing": "Vous n'aviez pas marqué cela comme mémorisé.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "Que souhaitez-vous mémoriser ?",
    "btn_target_surah": "Une sourate",
    "btn_target_juz": "Un juz",
    "btn_target_range": "Une plage",
    "memorize_surah_prompt": "Envoyez le numéro de la sourate, par exemple 67.",
    "memorize_juz_prompt": "Envoyez le numéro du juz, de 1 à 30.",
    "memorize_range_prompt": "Envoyez la plage, par exemple 67:1-68:5.",
    "memorize_choose_pace": "Combien voulez-vous faire chaque jour ?",
    "btn_pace_auto": "Choisir pour moi",
    "memorize_pace_prompt": "Envoyez le nombre de versets par jour.",
    "memorize_pace_invalid": "Envoyez un nombre entre {min} et {max}.",
    "memorize_choose_days": "Quels jours souhaitez-vous étudier ?",
    "btn_days_daily": "Tous les jours",
    "btn_days_weekdays": "En semaine",
    "btn_days_custom": "Choisir les jours",
    "memorize_days_prompt": "Appuyez sur les jours voulus, puis confirmez.",
    "memorize_preview_title": "{days} jours, du {start} au {end} :",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Démarrer ce plan",
    "plan_saved": "Votre plan est prêt. La première portion arrive le {first_date}.",
    "plan_exists": "Un plan est déjà en cours. Mettez-le en pause ou abandonnez-le d'abord.",
    "btn_pause_plan": "Mettre en pause",
    "btn_resume_plan": "Reprendre le plan",
    "btn_abandon_plan": "Abandonner le plan",
    "plan_paused": "Plan en pause. Reprenez-le quand vous voulez depuis /profile.",
    "plan_resumed": "Plan repris.",
    "plan_abandoned": "Plan abandonné.",
    "plan_complete": "Vous avez terminé {target}. Qu'Allah l'accepte de vous.",
    "drill_title": "{ref} — jour {day} sur {total}",
    "drill_none_today": "Rien n'est prévu aujourd'hui.",
    "btn_start_drill": "Portion du jour",
    "btn_know_by_heart": "✅ Je le sais par cœur",
    "know_confirmed": "{ref} marqué comme mémorisé. Vous êtes à {pct} %.",
    "know_already": "Vous l'aviez déjà marqué.",

    # Recall check (E2, E3)
    "check_question": "Comment cela continue-t-il ?",
    "check_usage": "Envoyez ce qu'il faut tester, par exemple /check 67.",
    "check_correct": "Correct.",
    "check_wrong": "Pas tout à fait. La suite est : {correct}",
    "check_already_today": (
        "Vous avez déjà validé la séance du jour avec un test de mémoire — "
        "testez-vous autant que vous voulez, cela ne comptera simplement pas deux fois."
    ),
    "btn_check_start": "Me tester",

    # Streaks (G2, G3)
    "streak_title": "Votre série",
    "streak_current": "Série actuelle : {n}",
    "streak_longest": "Plus longue série : {n}",
    "streak_none": "Pas encore de série. Terminez une portion ou réussissez un test de mémoire aujourd'hui pour en commencer une.",
    "streak_graph_caption": "Les 12 dernières semaines",
    "streak_milestone_7": "Une semaine complète. C'est là que l'habitude commence.",
    "streak_milestone_30": "Trente jours. La régularité est désormais de votre côté.",
    "streak_milestone_100": "Cent jours. Très peu de gens vont aussi loin.",
    "streak_milestone_365": "Une année entière, chaque jour. Qu'Allah préserve ce que vous avez appris.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "Classement de la semaine",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "Vous : {rank}. — {sessions}",
    "leaderboard_empty": "Personne n'a encore terminé de séance cette semaine. Soyez le premier.",
    "leaderboard_not_opted_in": "Vous n'êtes pas au classement. Rejoignez-le depuis /profile.",
}
