# Portuguese — Português

strings = {
    "welcome_intro": (
        "Envie-me um número de surata e versículo, por exemplo <b>2:255</b>, e eu "
        "responderei com esse versículo do Sagrado Alcorão.\n\n"
        "Você também pode enviar um intervalo como <b>59:22-24</b> para receber uma "
        "recitação em áudio combinada."
    ),
    "welcome_commands_header": "Comandos:",
    "welcome_inline": (
        "Você pode me usar em qualquer conversa: digite <b>@QuranAyat_bot</b> seguido de "
        "uma referência."
    ),
    "about": (
        "Este bot permite explorar o Sagrado Alcorão no Telegram em muitos "
        "idiomas.\n\n"
        "As traduções vêm do tanzil.net (veja ATTRIBUTIONS.md para a edição e o "
        "tradutor de cada tradução). O áudio é uma recitação do xeique Mahmoud "
        "Khalil al-Husary (everyayah.com). O tafsir é o Tafsir al-Jalalayn "
        "(altafsir.com), disponível em inglês.\n\n"
        "Mude de idioma a qualquer momento com /language."
    ),
    "ayah_not_found": "Esse versículo não existe!",
    "range_too_large": "Intervalo grande demais, peça no máximo {n} versículos por vez.",
    "choose_language": "Escolha o seu idioma:",
    "language_set": "Idioma alterado para {lang}.",
    "choose_translation_language": "Escolha o idioma da tradução:",
    "translation_language_set": "Idioma da tradução definido para {lang}.",
    "choose_reciter": "Escolha um recitador:",
    "reciter_set": "Recitador definido para {reciter}.",
    "btn_search_reciter": "Pesquisar por nome",
    "reciter_search_prompt": "Digite o nome de um recitador para pesquisar (ex.: «Sudais», «Abdul Basit»).",
    "reciter_search_no_matches": "Nenhum recitador corresponde a esse nome — tente novamente.",
    "reciter_search_results": "Resultados da pesquisa:",
    "btn_set_reciter": "Definir como meu recitador",
    "reciter_inline_description": "Toque para definir como o seu recitador",
    "tafsir_en_note": "\n\n(O tafsir está disponível apenas em inglês.)",
    "btn_translation": "Tradução",
    "btn_tafsir": "Tafsir",
    "btn_arabic": "Árabe",
    "btn_audio": "Áudio",
    "btn_previous": "Anterior",
    "btn_random": "Aleatório",
    "btn_next": "Próximo",
    "page_label": "Página {n} de {total}",
    "page_out_of_range": "Envie um número de página entre 1 e {total}, por exemplo /page 255.",
    "juz_out_of_range": "Envie um número de juz entre 1 e {total}, por exemplo /juz 30.",
    "sajda_list_title": "Versículos de prostração (sajda):",
    "btn_ayah_view": "Vista por versículos",
    "btn_repeat": "Repetir",
    "reciter_group_recitation": "Recitadores",
    "reciter_group_riwayah": "Riwāya",
    "reciter_group_translation": "Significado",
    "riwayah_warning": "Nota: esta é a riwāya de Warsh — uma leitura do texto corânico diferente da de Hafs mostrada aqui no texto árabe e nas traduções, portanto o áudio nem sempre corresponderá às palavras no ecrã.",
    "translation_audio_warning": "Nota: esta gravação não é recitação do Alcorão, mas a leitura em voz alta do significado traduzido. Escolha no separador «Recitadores» para ouvir a recitação em árabe.",
    "cmd_index": "Listar todas as suratas",
    "cmd_page": "Ler uma página do mushaf",
    "cmd_juz": "Abrir um juz",
    "cmd_sajda": "Versículos de prostração",
    "cmd_random": "Um versículo aleatório",
    "cmd_language": "Mudar de idioma",
    "cmd_translation": "Mudar o idioma da tradução",
    "cmd_reciter": "Mudar de recitador",
    "cmd_about": "Fontes e créditos",
    "quran_name": "Alcorão",

    # --- Hifz platform ---------------------------------------------------------

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "Começar um plano de hifz",
    "cmd_progress": "O que você memorizou",
    "cmd_check": "Testar a sua memória",
    "cmd_forgot": "Desmarcar um intervalo memorizado",
    "cmd_streak": "A sua sequência diária",
    "cmd_leaderboard": "Os melhores desta semana",
    "cmd_profile": "O seu perfil e configurações",

    # Shared wizard controls
    "wizard_cancelled": "Cancelado.",
    "wizard_nothing_to_cancel": "Não há nada para cancelar.",
    "wizard_invalid_input": "Não entendi. Tente de novo ou envie /cancel.",
    "ref_invalid": "Não reconheço essa referência. Tente algo como 67, 67:1-8 ou juz 30.",
    "btn_cancel": "Cancelar",
    "btn_back": "Voltar",
    "btn_confirm": "Confirmar",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "seg",
    "day_tue": "ter",
    "day_wed": "qua",
    "day_thu": "qui",
    "day_fri": "sex",
    "day_sat": "sáb",
    "day_sun": "dom",

    # Profile (B1-B3)
    "profile_title": "O seu perfil",
    "profile_name_set": "Nome: {name}",
    "profile_name_unset": "Nome: não definido",
    "profile_leaderboard_on": "Classificação: você aparece nela",
    "profile_leaderboard_off": "Classificação: você está oculto",
    "profile_timezone_set": "Fuso horário: UTC{offset}",
    "profile_timezone_unset": "Fuso horário: não definido",
    "profile_reminder_set": "Lembrete diário: {time}",
    "profile_reminder_unset": "Lembrete diário: desativado",
    "profile_plan_active": "Plano: {target} — dia {day} de {total}",
    "profile_plan_none": "Plano: ainda nenhum. Comece um com /memorize.",
    "btn_edit_name": "Mudar o nome",
    "btn_join_board": "Entrar na classificação",
    "btn_leave_board": "Sair da classificação",
    "btn_edit_timezone": "Mudar o fuso horário",
    "btn_edit_reminder": "Mudar o lembrete",
    "name_prompt": "Envie o nome com que quer aparecer na classificação.",
    "name_invalid": "Use entre {min} e {max} caracteres.",
    "name_saved": "Você vai aparecer como {name}.",
    "board_joined": "Você já está na classificação.",
    "board_left": "Você foi retirado da classificação.",
    "timezone_prompt": (
        "Escolha o seu fuso UTC. Ele define quando o seu dia começa para as "
        "sequências e quando chega a sua porção diária."
    ),
    "timezone_saved": "Fuso horário definido para UTC{offset}.",
    "reminder_prompt": "Envie a hora a que quer receber a sua porção diária, no formato de 24 horas, por exemplo 07:30.",
    "reminder_invalid": "Envie uma hora no formato de 24 horas, por exemplo 07:30.",
    "reminder_saved": "Lembrete diário definido para {time}.",
    "btn_reminder_off": "Desativar lembretes",
    "reminder_off": "Os lembretes diários estão desativados.",

    # Progress and /forgot (C3)
    "progress_title": "O que você memorizou",
    "progress_surah_line": "{name}: {done}/{total} versículos — {pct}%",
    "progress_juz_line": "Juz {n}: {pct}%",
    "progress_quran_line": "Alcorão inteiro: {pct}%",
    "progress_empty": (
        "Ainda não há nada marcado. Termine uma porção e toque em «Sei de cor», "
        "ou comece um plano com /memorize."
    ),
    "forgot_usage": "Envie o que quer desmarcar, por exemplo /forgot 67:5-6.",
    "forgot_done": "{ref} desmarcado.",
    "forgot_nothing": "Você não tinha marcado isso como memorizado.",

    # Memorization plans and drills (D1, D3-D5)
    "memorize_choose_target": "O que gostaria de memorizar?",
    "btn_target_surah": "Uma surata",
    "btn_target_juz": "Um juz",
    "btn_target_range": "Um intervalo",
    "memorize_surah_prompt": "Envie o número da surata, por exemplo 67.",
    "memorize_juz_prompt": "Envie o número do juz, de 1 a 30.",
    "memorize_range_prompt": "Envie o intervalo, por exemplo 67:1-68:5.",
    "memorize_choose_pace": "Quanto quer fazer por dia?",
    "btn_pace_auto": "Escolha por mim",
    "memorize_pace_prompt": "Envie quantos versículos por dia.",
    "memorize_pace_invalid": "Envie um número entre {min} e {max}.",
    "memorize_choose_days": "Em que dias quer estudar?",
    "btn_days_daily": "Todos os dias",
    "btn_days_weekdays": "Dias de semana",
    "btn_days_custom": "Escolher dias",
    "memorize_days_prompt": "Toque nos dias que quiser e depois confirme.",
    "memorize_preview_title": "{days} dias, de {start} a {end}:",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "Começar este plano",
    "plan_saved": "O seu plano está pronto. A primeira porção chega em {first_date}.",
    "plan_exists": "Você já tem um plano em curso. Pause-o ou abandone-o primeiro.",
    "btn_pause_plan": "Pausar o plano",
    "btn_resume_plan": "Retomar o plano",
    "btn_abandon_plan": "Abandonar o plano",
    "plan_paused": "Plano pausado. Retome-o quando quiser em /profile.",
    "plan_resumed": "Plano retomado.",
    "plan_abandoned": "Plano abandonado.",
    "plan_complete": "Você terminou {target}. Que Allah aceite isso de você.",
    "drill_title": "{ref} — dia {day} de {total}",
    "drill_none_today": "Não há nada marcado para hoje.",
    "btn_start_drill": "Porção de hoje",
    "btn_know_by_heart": "✅ Sei de cor",
    "know_confirmed": "{ref} marcado como memorizado. Você está em {pct}%.",
    "know_already": "Você já tinha marcado essa.",

    # Recall check (E2, E3)
    "check_question": "Como continua?",
    "check_usage": "Envie o que quer testar, por exemplo /check 67.",
    "check_correct": "Correto.",
    "check_wrong": "Não é bem assim. Continua: {correct}",
    "check_already_today": (
        "Você já garantiu a sessão de hoje com um teste de memória — teste-se "
        "quantas vezes quiser, só não conta duas vezes."
    ),
    "btn_check_start": "Testar-me",

    # Streaks (G2, G3)
    "streak_title": "A sua sequência",
    "streak_current": "Sequência atual: {n}",
    "streak_longest": "Sequência mais longa: {n}",
    "streak_none": "Ainda sem sequência. Termine uma porção ou passe num teste de memória hoje para começar uma.",
    "streak_graph_caption": "As últimas 12 semanas",
    "streak_milestone_7": "Uma semana inteira. É aqui que o hábito começa.",
    "streak_milestone_30": "Trinta dias. A constância já está do seu lado.",
    "streak_milestone_100": "Cem dias. Muito pouca gente chega tão longe.",
    "streak_milestone_365": "Um ano inteiro, todos os dias. Que Allah preserve o que você aprendeu.",

    # Leaderboard (H1, H2)
    "leaderboard_title": "Classificação desta semana",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "Você: {rank}. — {sessions}",
    "leaderboard_empty": "Ninguém completou uma sessão esta semana ainda. Seja o primeiro.",
    "leaderboard_not_opted_in": "Você não está na classificação. Entre nela em /profile.",
}
