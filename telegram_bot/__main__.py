import asyncio
import logging
import os
import sys

from aiogram import Dispatcher
from aiogram.webhook.aiohttp_server import (
    setup_application,
    SimpleRequestHandler,
)
from aiohttp import web
from bot_instance import bot
import dotenv
from handlers import router

dotenv.load_dotenv()

USE_WEBHOOK = os.getenv("USE_WEBHOOK").lower() == "true"
USE_REDIS = os.getenv("USE_REDIS").lower() == "true"

if USE_REDIS:
    from aiogram.fsm.storage.redis import RedisStorage

    storage = RedisStorage.from_url(
        os.getenv("REDIS_BOT_URL"),
    )
else:
    from aiogram.fsm.storage.memory import MemoryStorage

    storage = MemoryStorage()

dp = Dispatcher(storage=storage)

dp.include_router(router)


async def on_startup() -> None:
    webhook_url = os.getenv("DOMAIN_URL") + os.getenv("WEBHOOK_PATH")
    await bot.set_webhook(
        url=webhook_url,
        secret_token=os.getenv("WEBHOOK_SECRET"),
    )


def run_webhook() -> None:
    dp.startup.register(on_startup)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=os.getenv("WEBHOOK_SECRET"),
    )
    webhook_requests_handler.register(
        app,
        path=os.getenv("WEBHOOK_PATH"),
    )
    setup_application(app, dp, bot=bot)
    web.run_app(
        app,
        host=os.getenv("WEB_SERVER_HOST"),
        port=int(os.getenv("WEB_SERVER_PORT")),
    )


async def run_polling() -> None:
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    if USE_WEBHOOK:
        run_webhook()
    else:
        asyncio.run(run_polling())
