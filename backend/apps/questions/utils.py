import asyncio
import json

import aiohttp
from apps.questions.constants import headers, payload
from django.conf import settings


async def ask_question(data: dict) -> dict:
    answer_text = "Unknown error | We will fix it in near future"
    error_text = ""
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
                data["chat_session_id"] = chat_session_id
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
                        "message": "KOD 200 MI VMESTE",
                        "message_id": data["message_id"],
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
    if error_text:
        send_message_func = data["send_message_func"]
        await send_message_func(
            settings.LOGS_GROUP_ID,
            {
                "message": f"Error while answering question: {error_text}",
            },
        )
    await asyncio.sleep(0.5)
    return data
