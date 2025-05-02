from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from django.conf import settings


BOT_TOKEN = settings.BOT_TOKEN


async def send_message(telegram_id: int, data: dict) -> str | Exception:
    async with AiohttpSession() as async_session:
        notify_bot = Bot(token=BOT_TOKEN, session=async_session)
        try:
            await notify_bot.send_message(
                chat_id=telegram_id,
                text=data["message"],
            )
        except Exception as error:
            return f"Error {telegram_id}: {error}"
    return f"Sent message to {telegram_id}"


async def edit_message(telegram_id: int, data: dict) -> str | Exception:
    async with AiohttpSession() as async_session:
        notify_bot = Bot(token=BOT_TOKEN, session=async_session)
        try:
            await notify_bot.edit_message_text(
                chat_id=telegram_id,
                message_id=data["message_id"],
                text=data["message"],
            )
        except Exception as error:
            return f"Error {telegram_id}: {error}"
    return f"Edit message for {telegram_id}"
