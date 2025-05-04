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
                    callback_data="questions_history_1",
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


def back_to_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Back to menu",
                    callback_data="back_to_menu",
                ),
            ],
        ]
    )


def back_to_menu_ask_question() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Back to menu",
                    callback_data="back_to_menu",
                ),
                InlineKeyboardButton(
                    text="🔎 Ask a question",
                    callback_data="ask_question",
                ),
            ],
        ]
    )


def questions_history(questions: list[dict], pages_info: dict) -> InlineKeyboardMarkup:
    keyboard = []
    for question in questions:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=question["question_text"][:35],
                    callback_data=f"get_question_{pages_info['page_num']}"
                    f"_{question['id']}",
                )
            ]
        )
    system_buttons = [
        InlineKeyboardButton(
            text=f"{pages_info['page_num']}/{pages_info['count'] // 5}",
            callback_data="do_nothing",
        ),
    ]
    if pages_info["previous"]:
        system_buttons.insert(
            0,
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"questions_history_{pages_info['page_num'] - 1}",
            ),
        )
    if pages_info["next"]:
        system_buttons.append(
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"questions_history_{pages_info['page_num'] + 1}",
            ),
        )
    keyboard.append(system_buttons)
    keyboard.append(
        [
            InlineKeyboardButton(
                text="🔙 Back to menu",
                callback_data="back_to_menu",
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def return_to_history(page_num: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Back to menu",
                    callback_data="back_to_menu",
                ),
                InlineKeyboardButton(
                    text="📚 Return to history",
                    callback_data=f"questions_history_{page_num}",
                ),
            ],
        ]
    )
