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
        "RU": "",
        "EN": "🔎 Ask one more",
        "HE": "",
    },
    "back_to_menu": {
        "RU": "",
        "EN": "🔙 Back to menu",
        "HE": "",
    },
}

TR_TG_TEXT = {
    "accepted": {
        "RU": "",
        "EN": "✅ Request accepted",
        "HE": "",
    },
    "in_work": {
        "RU": "",
        "EN": "🔎 Ask one more",
        "HE": "",
    },
    "kod_200": {
        "RU": "",
        "EN": "KOD 200 MI VMESTE",
        "HE": "",
    },
    "unknown_error": {
        "RU": "",
        "EN": "Unknown error | We will fix it in near future",
        "HE": "",
    },
}
