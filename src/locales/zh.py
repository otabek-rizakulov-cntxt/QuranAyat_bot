# Chinese — 中文
#
# Traditional characters, to match the bundled zh.majian translation text.

strings = {
    "welcome_intro": (
        "請把蘇拉和經文編號發給我，例如 <b>2:255</b>，我就會把《古蘭經》的那節經文發給你。\n\n"
        "你也可以發送像 <b>59:22-24</b> 這樣的範圍，以取得合併的誦讀音頻。"
    ),
    "welcome_commands_header": "命令：",
    "welcome_inline": "你可以在任何聊天中使用我：輸入 <b>@QuranAyat_bot</b>，然後加上經文編號。",
    "about": (
        "這個機器人讓你在 Telegram 上以多種語言閱讀《古蘭經》。\n\n"
        "譯文來自 tanzil.net（每個譯本的版本與譯者請見 ATTRIBUTIONS.md）。"
        "音頻是謝赫馬哈茂德·哈利勒·胡薩里的誦讀（everyayah.com）。"
        "經注為《哲拉萊尼經注》（altafsir.com），提供英文版。\n\n"
        "隨時可用 /language 更改語言。"
    ),
    "ayah_not_found": "沒有這節經文！",
    "range_too_large": "範圍太大，每次最多請求 {n} 節經文。",
    "choose_language": "請選擇你的語言：",
    "language_set": "語言已設為 {lang}。",
    "choose_translation_language": "選擇譯文語言：",
    "translation_language_set": "譯文語言已設為 {lang}。",
    "choose_reciter": "選擇誦讀者：",
    "reciter_set": "誦讀者已設為 {reciter}。",
    "btn_search_reciter": "按姓名搜尋",
    "reciter_search_prompt": "輸入誦讀者姓名進行搜尋（例如「蘇戴斯」「阿卜杜勒·巴西特」）。",
    "reciter_search_no_matches": "沒有找到該姓名的誦讀者——請重試。",
    "reciter_search_results": "搜尋結果：",
    "btn_set_reciter": "設為我的誦讀者",
    "reciter_inline_description": "點按即可設為你的誦讀者",
    "tafsir_en_note": "\n\n（經注僅提供英文版。）",
    "btn_translation": "譯文",
    "btn_tafsir": "經注",
    "btn_arabic": "阿拉伯文",
    "btn_audio": "音頻",
    "btn_previous": "上一節",
    "btn_random": "隨機",
    "btn_next": "下一節",
    "page_label": "第 {n} 頁，共 {total} 頁",
    "page_out_of_range": "請發送 1 至 {total} 之間的頁碼，例如 /page 255。",
    "juz_out_of_range": "請發送 1 至 {total} 之間的部（juz）編號，例如 /juz 30。",
    "sajda_list_title": "叩拜（辛吉達）的經文：",
    "btn_ayah_view": "逐節檢視",
    "btn_repeat": "重複",
    "reciter_group_recitation": "誦讀者",
    "reciter_group_riwayah": "傳述",
    "reciter_group_translation": "意義",
    "riwayah_warning": "注意：這是瓦爾什傳述本——與此處阿拉伯文原文及譯文所依據的哈夫斯讀法不同，因此音頻未必與螢幕上的文字一致。",
    "translation_audio_warning": "注意：此錄音並非《古蘭經》誦讀，而是譯文意義的朗讀。若要聆聽阿拉伯語誦讀，請從「誦讀者」分頁中選擇。",
    "cmd_index": "列出所有蘇拉",
    "cmd_page": "閱讀一頁穆斯哈夫",
    "cmd_juz": "開啟一部",
    "cmd_sajda": "叩拜的經文",
    "cmd_random": "隨機一節經文",
    "cmd_language": "更改語言",
    "cmd_translation": "更改譯文語言",
    "cmd_reciter": "更改誦讀者",
    "cmd_about": "來源與致謝",
    "quran_name": "古蘭經",

    # --- Hifz platform ---------------------------------------------------------

    # Command descriptions (the Telegram menu and the /start list)
    "cmd_memorize": "開始背誦計劃",
    "cmd_progress": "你已背誦的內容",
    "cmd_check": "測驗你的記憶",
    "cmd_forgot": "取消已背誦的標記",
    "cmd_streak": "你的每日連續紀錄",
    "cmd_leaderboard": "本週背誦最多的人",
    "cmd_profile": "你的個人資料與設定",

    # Shared wizard controls
    "wizard_cancelled": "已取消。",
    "wizard_nothing_to_cancel": "目前沒有可取消的操作。",
    "wizard_invalid_input": "我不明白。請再試一次，或發送 /cancel。",
    "ref_invalid": "這不是我認得的經文編號。可以試試 67、67:1-8 或 juz 30。",
    "btn_cancel": "取消",
    "btn_back": "返回",
    "btn_confirm": "確認",

    # Days of the week — the plan's day picker, and the streak grid's header
    "day_mon": "週一",
    "day_tue": "週二",
    "day_wed": "週三",
    "day_thu": "週四",
    "day_fri": "週五",
    "day_sat": "週六",
    "day_sun": "週日",

    # Profile
    "profile_title": "你的個人資料",
    "profile_name_set": "名稱：{name}",
    "profile_name_unset": "名稱：未設定",
    "profile_leaderboard_on": "排行榜：你已列入",
    "profile_leaderboard_off": "排行榜：你已隱藏",
    "profile_timezone_set": "時區：UTC{offset}",
    "profile_timezone_unset": "時區：未設定",
    "profile_reminder_set": "每日提醒：{time}",
    "profile_reminder_unset": "每日提醒：已關閉",
    "profile_plan_active": "計劃：{target} — 第 {day} 天，共 {total} 天",
    "profile_plan_none": "計劃：尚未建立。用 /memorize 開始一個。",
    "btn_edit_name": "更改名稱",
    "btn_join_board": "加入排行榜",
    "btn_leave_board": "退出排行榜",
    "btn_edit_timezone": "更改時區",
    "btn_edit_reminder": "更改提醒時間",
    "name_prompt": "請發送你想在排行榜上顯示的名稱。",
    "name_invalid": "請使用 {min} 到 {max} 個字元。",
    "name_saved": "你將顯示為 {name}。",
    "board_joined": "你已加入排行榜。",
    "board_left": "你已從排行榜中移除。",
    "timezone_prompt": (
        "請選擇你的 UTC 時差。它決定連續紀錄從何時算作新的一天，以及每日份量何時送達。"
    ),
    "timezone_saved": "時區已設為 UTC{offset}。",
    "reminder_prompt": "請以 24 小時制發送你想收到每日份量的時間，例如 07:30。",
    "reminder_invalid": "請以 24 小時制發送時間，例如 07:30。",
    "reminder_saved": "每日提醒已設為 {time}。",
    "btn_reminder_off": "關閉提醒",
    "reminder_off": "每日提醒已關閉。",

    # Progress and /forgot
    "progress_title": "你已背誦的內容",
    "progress_surah_line": "{name}：{done}/{total} 節 — {pct}%",
    "progress_juz_line": "第 {n} 部：{pct}%",
    "progress_quran_line": "整部古蘭經：{pct}%",
    "progress_empty": (
        "尚未標記任何內容。完成一段後點按「我已背熟」，或用 /memorize 開始一個計劃。"
    ),
    "forgot_usage": "請發送要取消標記的範圍，例如 /forgot 67:5-6。",
    "forgot_done": "已取消 {ref} 的標記。",
    "forgot_nothing": "你並未把那一段標記為已背誦。",

    # Memorization plans and drills
    "memorize_choose_target": "你想背誦什麼？",
    "btn_target_surah": "一章蘇拉",
    "btn_target_juz": "一部",
    "btn_target_range": "一個範圍",
    "memorize_surah_prompt": "請發送蘇拉編號，例如 67。",
    "memorize_juz_prompt": "請發送 1 至 30 的部編號。",
    "memorize_range_prompt": "請發送範圍，例如 67:1-68:5。",
    "memorize_choose_pace": "你每天想背多少？",
    "btn_pace_auto": "幫我決定",
    "memorize_pace_prompt": "請發送每天要背幾節。",
    "memorize_pace_invalid": "請發送 {min} 到 {max} 之間的數字。",
    "memorize_choose_days": "你想在哪幾天學習？",
    "btn_days_daily": "每天",
    "btn_days_weekdays": "平日",
    "btn_days_custom": "自選日子",
    "memorize_days_prompt": "點選你要的日子，然後確認。",
    "memorize_preview_title": "共 {days} 天，{start} 至 {end}：",
    "memorize_preview_row": "{date} — {ref}",
    "btn_confirm_plan": "開始這個計劃",
    "plan_saved": "你的計劃已設定。第一份將於 {first_date} 送達。",
    "plan_exists": "你已有一個進行中的計劃。請先暫停或放棄它。",
    "btn_pause_plan": "暫停計劃",
    "btn_resume_plan": "繼續計劃",
    "btn_abandon_plan": "放棄計劃",
    "plan_paused": "計劃已暫停。隨時可從 /profile 繼續。",
    "plan_resumed": "計劃已繼續。",
    "plan_abandoned": "計劃已放棄。",
    "plan_complete": "你已完成 {target}。願安拉悅納。",
    "drill_title": "{ref} — 第 {day} 天，共 {total} 天",
    "drill_none_today": "今天沒有安排任何內容。",
    "btn_start_drill": "開始今天的份量",
    "btn_know_by_heart": "✅ 我已背熟",
    "know_confirmed": "{ref} 已標記為背熟。你已達到 {pct}%。",
    "know_already": "那一段你已經標記過了。",

    # Recall check
    "check_question": "接下來是什麼？",
    "check_usage": "請發送要測驗的範圍，例如 /check 67。",
    "check_correct": "答對了。",
    "check_wrong": "還差一點。接下來是：{correct}",
    "check_already_today": (
        "你今天的紀錄已經透過一次記憶測驗完成了——你可以隨意多測幾次，只是不會重複計算。"
    ),
    "btn_check_start": "測驗我",

    # Streaks
    "streak_title": "你的連續紀錄",
    "streak_current": "目前連續：{n} 天",
    "streak_longest": "最長連續：{n} 天",
    "streak_none": "還沒有連續紀錄。今天完成一段或通過一次記憶測驗就能開始。",
    "streak_graph_caption": "最近 12 週",
    "streak_milestone_7": "整整一週。習慣就是從這裡開始的。",
    "streak_milestone_30": "三十天。堅持已經站在你這一邊了。",
    "streak_milestone_100": "一百天。很少有人能走到這一步。",
    "streak_milestone_365": "整整一年，一天也沒斷。願安拉護佑你所學的一切。",

    # Leaderboard
    "leaderboard_title": "本週排行榜",
    "leaderboard_row": "{rank}. {name} — {sessions}",
    "leaderboard_you_row": "你：{rank}. — {sessions}",
    "leaderboard_empty": "本週還沒有人完成任何一次學習。來當第一個吧。",
    "leaderboard_not_opted_in": "你不在排行榜上。可從 /profile 加入。",
}
