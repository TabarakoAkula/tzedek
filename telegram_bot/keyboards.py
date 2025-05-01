from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def menu_keyboard_in() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔎 Ask a question",
                    callback_data="ask_question",
                ),
                InlineKeyboardButton(
                    text="📚 History of questions",
                    callback_data="questions_history",
                ),
            ],
            [InlineKeyboardButton(text="🛞 Settings", callback_data="settings")],
        ]
    )


def question_approve_keyboard_in() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Back to menu",
                    callback_data="back_to_menu",
                ),
                InlineKeyboardButton(
                    text="✅ Continue",
                    callback_data="question_continue",
                ),
            ],
        ]
    )
