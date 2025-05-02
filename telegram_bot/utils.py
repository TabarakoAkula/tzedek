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


async def send_question(data: dict) -> None:
    await asyncio.to_thread(
        requests.post,
        url=DOCKER_URL + "questions/",
        json=data,
        headers={"X-Api-Key": API_KEY},
    )
