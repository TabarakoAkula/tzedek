from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from django.conf import settings


BOT_TOKEN = settings.BOT_TOKEN
LOGS_GROUP_ID = settings.LOGS_GROUP_ID


def build_inline_keyboard(data: list) -> InlineKeyboardMarkup:
    in_list = []
    for buttons_group in data:
        in_group = []
        for button in buttons_group:
            in_group.append(
                InlineKeyboardButton(
                    text=button["title"],
                    callback_data=button["callback"],
                )
            )
        in_list.append(in_group)
    return InlineKeyboardMarkup(inline_keyboard=in_list)


async def send_message(telegram_id: int, data: dict) -> str:
    async with AiohttpSession() as async_session:
        notify_bot = Bot(
            token=BOT_TOKEN,
            session=async_session,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
        )
        try:
            if data["inline_reply_markup"]:
                await notify_bot.send_message(
                    chat_id=telegram_id,
                    text=data["message"],
                    reply_markup=build_inline_keyboard(data["inline_reply_markup"]),
                )
            else:
                await notify_bot.send_message(
                    chat_id=telegram_id,
                    text=data["message"],
                )
        except Exception as error:
            return await logs_snitch(f"Error send_message for {telegram_id}: {error}")
    return f"Sent message to {telegram_id}"


async def edit_message(telegram_id: int, data: dict) -> str:
    async with AiohttpSession() as async_session:
        notify_bot = Bot(
            token=BOT_TOKEN,
            session=async_session,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
        )
        try:
            if data["inline_reply_markup"]:
                await notify_bot.edit_message_text(
                    chat_id=telegram_id,
                    message_id=data["message_id"],
                    text=data["message"],
                    reply_markup=build_inline_keyboard(data["inline_reply_markup"]),
                )
            else:
                await notify_bot.edit_message_text(
                    chat_id=telegram_id,
                    message_id=data["message_id"],
                    text=data["message"],
                )
        except Exception as error:
            return await logs_snitch(f"Error edit_message for {telegram_id}: {error}")
    return f"Edit message for {telegram_id}"


async def logs_snitch(message: str) -> str:
    async with AiohttpSession() as async_session:
        notify_bot = Bot(token=BOT_TOKEN, session=async_session)
        try:
            await notify_bot.send_message(
                chat_id=LOGS_GROUP_ID,
                text=message,
            )
        except Exception as error:
            return f"Snitch error: {error}"
    return "Successfully snitched 🫡"
