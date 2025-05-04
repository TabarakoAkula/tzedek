from aiogram import F, html, Router
import aiogram.exceptions
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


async def menu_handler(message: Message, state: FSMContext, edit_message=False):
    await state.clear()
    if edit_message:
        await message.edit_text(
            text=html.italic(
                value="Menu\nТут разная информация, инструкции, объяснения и т.д.",
            ),
            reply_markup=keyboards.menu_keyboard_in(),
        )
    else:
        await message.answer(
            text=html.italic(
                value="Menu\nТут разная информация, инструкции, объяснения и т.д.",
            ),
            reply_markup=keyboards.menu_keyboard_in(),
        )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await menu_handler(callback.message, state, edit_message=True)
    except aiogram.exceptions.TelegramBadRequest:
        await menu_handler(callback.message, state)


@router.callback_query(F.data == "ask_question")
async def ask_user_question_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(states.QuestionsStatesGroup.ask_question)
    await callback.message.answer(
        text="Ask a question:",
        reply_markup=keyboards.back_to_menu(),
    )


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


@router.callback_query(F.data.startswith("questions_history_"))
async def question_history_handler(callback: CallbackQuery):
    page_num = callback.data.split("_")[-1]
    user_questions = await utils.get_user_questions(
        {
            "telegram_id": str(callback.message.chat.id),
            "page_num": int(page_num),
        }
    )
    count = user_questions["count"]
    if count == 0:
        return await callback.message.edit_text(
            text="История вопросов чиста, как маленький оленёнок🦌",
            reply_markup=keyboards.back_to_menu_ask_question(),
        )
    await callback.message.edit_text(
        text=f"Всего задано {count} вопросов\n\nНажми на вопрос"
        f", чтобы увидеть подробности",
        reply_markup=keyboards.questions_history(
            user_questions["data"],
            {
                "page_num": user_questions["page_num"],
                "next": user_questions["next"],
                "previous": user_questions["previous"],
                "count": user_questions["count"],
            },
        ),
    )


@router.callback_query(F.data.startswith("get_question_"))
async def get_question_handler(callback: CallbackQuery):
    page_num = callback.data.split("_")[-2]
    question_id = callback.data.split("_")[-1]
    question_data = await utils.get_question(str(question_id))
    await callback.message.edit_text(
        text=f"Вопрос от {question_data['created_at']}\n\n"
        f"Question: {question_data['question_text']}\n\n"
        f"Answer: {question_data['answer_text']}",
        reply_markup=keyboards.return_to_history(page_num=page_num),
    )
