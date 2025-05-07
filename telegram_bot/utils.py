import asyncio
import os

import dotenv
import requests

dotenv.load_dotenv()

DOCKER_URL = os.getenv("DOCKER_URL")
API_KEY = os.getenv("API_KEY")


async def create_user(data: dict) -> None:
    telegram_id = data["telegram_id"]
    await asyncio.to_thread(
        requests.post,
        url=DOCKER_URL + f"users/{telegram_id}",
        json=data,
        headers={"X-Api-Key": API_KEY},
    )


async def get_user(telegram_id: int) -> None:
    response = await asyncio.to_thread(
        requests.get,
        url=DOCKER_URL + f"users/{telegram_id}",
        params={"api_key": API_KEY},
    )
    data = response.json()
    try:
        data["data"]["success"] = data["success"]
    except KeyError:
        return {"success": False}
    return data["data"]


async def send_question(data: dict) -> None:
    await asyncio.to_thread(
        requests.post,
        url=DOCKER_URL + "questions/create_question",
        json=data,
        headers={"X-Api-Key": API_KEY},
    )


async def get_user_questions(data: dict) -> dict:
    data = await asyncio.to_thread(
        requests.get,
        url=DOCKER_URL + f"users/get_questions/{data['telegram_id']}",
        headers={"X-Api-Key": API_KEY},
        params={
            "api_key": API_KEY,
            "page": data["page_num"],
        },
    )
    return data.json()


async def get_question(question_id: str) -> dict:
    data = await asyncio.to_thread(
        requests.get,
        url=DOCKER_URL + f"questions/{question_id}",
        headers={"X-Api-Key": API_KEY},
        params={"api_key": API_KEY},
    )
    return data.json()


async def change_language(data: dict) -> None:
    await asyncio.to_thread(
        requests.post,
        url=DOCKER_URL + "users/change_language",
        json=data,
        headers={"X-Api-Key": API_KEY},
    )
