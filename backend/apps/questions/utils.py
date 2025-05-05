import asyncio
import json

import aiohttp
from apps.questions.constants import headers, payload, TR_TG_TEXT
from django.conf import settings


async def ask_question(data: dict) -> dict:
    await asyncio.sleep(data["timeout"])
    answer_text = TR_TG_TEXT["unknown_error"][data["language"]]
    error_text = ""
    chat_session_id = "None"
    success = False
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                settings.ONYX_URL + "/api/chat/create-chat-session",
                headers=headers,
                json={"persona_id": 1, "description": ""},
            ) as response:
                response.raise_for_status()
                chat_session_data = await response.json()
                chat_session_id = chat_session_data["chat_session_id"]
        payload["message"] = data["question"]
        payload["chat_session_id"] = chat_session_id
        async with aiohttp.ClientSession() as session:
            async with session.post(
                settings.ONYX_URL + "/api/chat/send-message",
                headers=headers,
                json=payload,
            ) as response:
                response.raise_for_status()
                edit_message_func = data["edit_message_func"]
                await edit_message_func(
                    data["telegram_id"],
                    {
                        "message": TR_TG_TEXT["kod_200"][data["language"]],
                        "message_id": data["message_id"],
                        "inline_reply_markup": [],
                    },
                )
                buffer = b""
                async for chunk in response.content.iter_chunked(1024):
                    buffer += chunk
                    while b"\n" in buffer:
                        line, buffer = buffer.split(b"\n", 1)
                        if not line.strip():
                            continue
                        last_line = line

        json_data = json.loads(last_line)
        if isinstance(json_data, dict):
            success = True
            answer_text = json_data["message"]
        else:
            error_text = (
                "\nНе удалось получить ни одного валидного JSON объекта из потока."
            )
    except KeyError as e:
        error_text = f"\nKeyError: {e}"
    except json.JSONDecodeError:
        error_text = "\nОшибка декодирования json`а"
    except Exception as e:
        error_text = f"\nПроизошла непредвиденная ошибка: {e}"

    data["success"] = success
    data["text"] = answer_text
    data["chat_session_id"] = chat_session_id
    if error_text:
        snitch_func = data["snitch_func"]
        await snitch_func(f"Error in ask_question(): {error_text}")
    return data
