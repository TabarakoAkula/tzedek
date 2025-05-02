from aiogram import F, html, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import dotenv
import keyboards
import states
import utils

dotenv.load_dotenv()

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await utils.create_user(
        {
            "telegram_id": str(message.chat.id),
            "username": message.chat.username,
        },
    )
    await menu_handler(message, state)


async def menu_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=html.italic("Menu\nТут разная информация, инструкции, объяснения и т.д."),
        reply_markup=keyboards.menu_keyboard_in(),
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_handler(callback: CallbackQuery, state: FSMContext):
    await menu_handler(callback.message, state)


@router.callback_query(F.data == "ask_question")
async def ask_user_question_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(states.QuestionsStatesGroup.ask_question)
    await callback.message.answer("ask a question:")


@router.message(states.QuestionsStatesGroup.ask_question)
async def get_question_message_handler(message: Message, state: FSMContext):
    question = message.text
    await state.update_data({"question_text": question})
    await state.set_state(states.QuestionsStatesGroup.confirm_question)
    await message.answer(
        text=f"Your question: \n\n{question}",
        reply_markup=keyboards.question_approve_keyboard_in(),
    )


@router.callback_query(
    F.data == "question_continue",
    states.QuestionsStatesGroup.confirm_question,
)
async def send_question_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["author"] = str(callback.message.chat.id)
    data["message_id"] = str(callback.message.message_id)
    await utils.send_question(data)
    await callback.message.edit_text("🔁 Request sent")
    await state.clear()
