from aiogram import html, Router
from aiogram.types import Message
import dotenv

dotenv.load_dotenv()

router = Router()


@router.message()
async def start_handler(message: Message):
    await message.answer("Welcome to system")
    await message.answer(html.italic("🤖 Creating new user"))
