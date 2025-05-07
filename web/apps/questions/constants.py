payload = {
    "alternate_assistant_id": 1,
    "chat_session_id": "",
    "parent_message_id": None,
    "message": "",
    "prompt_id": None,
    "search_doc_ids": None,
    "file_descriptors": [],
    "user_file_ids": [],
    "user_folder_ids": [],
    "regenerate": False,
    "retrieval_options": {
        "run_search": "always",
        "real_time": True,
        "filters": {
            "source_type": None,
            "document_set": None,
            "time_cutoff": None,
            "tags": [],
            "user_file_ids": [],
        },
    },
    "prompt_override": None,
    "llm_override": {"model_provider": "Default", "model_version": "gpt-4o-mini"},
    "use_agentic_search": False,
}

headers = {"Content-Type": "application/json"}

TR_TG_BUTTONS = {
    "ask_question": {
        "RU": "🔎 Задать ещё один вопрос",
        "EN": "🔎 Ask one more question",
        "HE": "🔎 שאל שאלה נוספת",
    },
    "back_to_menu": {
        "RU": "🔙 Меню",
        "EN": "🔙 Menu",
        "HE": "🔙 תפריט",
    },
}

TR_TG_TEXT = {
    "accepted": {
        "RU": "✅ Запрос принят",
        "EN": "✅ Request accepted",
        "HE": "✅ הבקשה התקבלה",
    },
    "kod_200": {
        "RU": "🤖 Генерирую ответ",
        "EN": "🤖 Generating a response",
        "HE": "🤖 יוצר תשובה",
    },
    "unknown_error": {
        "RU": "😢 Неизвестная ошибка\n😉 Мы исправим её в ближайшее время",
        "EN": "😢 Unknown error\n😉 We will fix it soon",
        "HE": "😢 שגיאה לא ידועה\n😉 נתקן את זה בקרוב",
    },
}

TR_PROMPT_TEXT = {
    "RU": "\nתשובה ברוסית",
    "EN": "\nתשובה באנגלית",
    "HE": "\nתשובה בעברית",
}
