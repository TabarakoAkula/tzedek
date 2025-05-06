from aiogram import F, html, Router
import aiogram.exceptions
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import constants
import dotenv
import keyboards
import states
import utils

dotenv.load_dotenv()

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    user = await utils.get_user(message.chat.id)
    if user["success"]:
        return await menu_handler(message, state)
    await state.set_state(states.ChooseLanguageStatesGroup.start_handler)
    await message.answer(
        text="🇬🇧Choose language\n🇷🇺Выбери язык\n🇮🇱בחר שפה",
        reply_markup=keyboards.choose_language(),
    )


@router.callback_query(
    F.data.startswith("choose_language_"),
    states.ChooseLanguageStatesGroup.start_handler,
)
async def choose_language_handler(callback: CallbackQuery, state: FSMContext):
    language = callback.data.split("_")[-1]
    await utils.create_user(
        {
            "telegram_id": str(callback.message.chat.id),
            "username": callback.message.chat.username,
            "language": language,
        },
    )
    await menu_handler(callback.message, state, edit_message=True)


async def menu_handler(message: Message, state: FSMContext, edit_message=False):
    await state.clear()
    user = await utils.get_user(message.chat.id)
    if edit_message:
        await message.edit_text(
            text=html.italic(value=constants.TR_TEXT["menu_info"][user["language"]]),
            reply_markup=keyboards.menu_keyboard_in(language=user["language"]),
        )
    else:
        await message.answer(
            text=html.italic(value=constants.TR_TEXT["menu_info"][user["language"]]),
            reply_markup=keyboards.menu_keyboard_in(language=user["language"]),
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
    user = await utils.get_user(callback.message.chat.id)
    await state.update_data({"language": user["language"]})
    await callback.message.answer(
        text=constants.TR_TEXT["ask_question"][user["language"]],
        reply_markup=keyboards.back_to_menu(language=user["language"]),
    )


@router.message(states.QuestionsStatesGroup.ask_question)
async def get_question_message_handler(message: Message, state: FSMContext):
    question = message.text
    data = await state.get_data()
    await state.update_data({"question_text": question})
    await state.set_state(states.QuestionsStatesGroup.confirm_question)
    await message.answer(
        text=f"{constants.TR_TEXT['your_question'][data['language']]}\n\n{question}",
        reply_markup=keyboards.question_approve_keyboard_in(language=data["language"]),
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
    await callback.message.edit_text(
        text=constants.TR_TEXT["request_sent"][data["language"]],
    )
    await state.clear()


@router.callback_query(F.data.startswith("questions_history_"))
async def question_history_handler(callback: CallbackQuery):
    user = await utils.get_user(callback.message.chat.id)
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
            text=constants.TR_TEXT["history_clear"][user["language"]],
            reply_markup=keyboards.back_to_menu_ask_question(language=user["language"]),
        )
    await callback.message.edit_text(
        text=f"{constants.TR_TEXT['total_questions'][user['language']]}{count}\n\n"
        f"{constants.TR_TEXT['click_for_info'][user['language']]}",
        reply_markup=keyboards.questions_history(
            questions=user_questions["data"],
            pages_info={
                "page_num": user_questions["page_num"],
                "next": user_questions["next"],
                "previous": user_questions["previous"],
                "count": user_questions["count"],
            },
            language=user["language"],
        ),
    )


@router.callback_query(F.data.startswith("get_question_"))
async def get_question_handler(callback: CallbackQuery):
    user = await utils.get_user(callback.message.chat.id)
    page_num = callback.data.split("_")[-2]
    question_id = callback.data.split("_")[-1]
    question_data = await utils.get_question(str(question_id))
    await callback.message.edit_text(
        text=f"{constants.TR_TEXT['question_date'][user['language']]}"
        f"{question_data['created_at']}\n\n"
        f"{constants.TR_TEXT['question'][user['language']]}"
        f"{question_data['question_text']}\n\n"
        f"{constants.TR_TEXT['answer'][user['language']]}"
        f"{question_data['answer_text']}",
        reply_markup=keyboards.return_to_history(
            page_num=page_num,
            language=user["language"],
        ),
    )


@router.callback_query(F.data == "settings")
async def settings_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(states.SettingsStatesGrou.settings_handler)
    user = await utils.get_user(callback.message.chat.id)
    await callback.message.edit_text(
        text=f"{constants.TR_TEXT['language_now'][user['language']]}"
        f"{constants.LANGUAGES[user['language']]}",
        reply_markup=keyboards.settings(language=user["language"]),
    )


@router.callback_query(F.data == "change_language")
async def change_language_handler(callback: CallbackQuery):
    user = await utils.get_user(callback.message.chat.id)
    await callback.message.edit_text(
        text=constants.TR_TEXT["change_language"][user["language"]],
        reply_markup=keyboards.change_language(user["language"]),
    )


@router.callback_query(F.data.startswith("change_language_"))
async def language_changer_handler(callback: CallbackQuery, state: FSMContext):
    language = callback.data.split("_")[-1]
    await utils.change_language(
        {
            "telegram_id": str(callback.message.chat.id),
            "language": language,
        }
    )
    await settings_handler(callback, state)
