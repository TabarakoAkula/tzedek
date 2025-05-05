from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from constants import TR_BUTTONS


def menu_keyboard_in(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TR_BUTTONS["ask_question"][language],
                    callback_data="ask_question",
                ),
                InlineKeyboardButton(
                    text=TR_BUTTONS["questions_history"][language],
                    callback_data="questions_history_1",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=TR_BUTTONS["settings"][language], callback_data="settings"
                ),
            ],
        ]
    )


def question_approve_keyboard_in(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TR_BUTTONS["back_to_menu"][language],
                    callback_data="back_to_menu",
                ),
                InlineKeyboardButton(
                    text=TR_BUTTONS["question_continue"][language],
                    callback_data="question_continue",
                ),
            ],
        ]
    )


def back_to_menu(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TR_BUTTONS["back_to_menu"][language],
                    callback_data="back_to_menu",
                ),
            ],
        ]
    )


def back_to_menu_ask_question(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TR_BUTTONS["back_to_menu"][language],
                    callback_data="back_to_menu",
                ),
                InlineKeyboardButton(
                    text=TR_BUTTONS["ask_question"][language],
                    callback_data="ask_question",
                ),
            ],
        ]
    )


def questions_history(
    questions: list[dict],
    pages_info: dict,
    language: str,
) -> InlineKeyboardMarkup:
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
                text=TR_BUTTONS["back_to_menu"][language],
                callback_data="back_to_menu",
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def return_to_history(page_num: int, language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TR_BUTTONS["back_to_menu"][language],
                    callback_data="back_to_menu",
                ),
                InlineKeyboardButton(
                    text=TR_BUTTONS["questions_history"][language],
                    callback_data=f"questions_history_{page_num}",
                ),
            ],
        ]
    )


def choose_language() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇷🇺Русский",
                    callback_data="choose_language_RU",
                ),
                InlineKeyboardButton(
                    text="🇬🇧English",
                    callback_data="choose_language_EN",
                ),
                InlineKeyboardButton(
                    text="🇮🇱עברית",
                    callback_data="choose_language_HE",
                ),
            ],
        ]
    )


def change_language(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇷🇺Русский",
                    callback_data="change_language_RU",
                ),
                InlineKeyboardButton(
                    text="🇬🇧English",
                    callback_data="change_language_EN",
                ),
                InlineKeyboardButton(
                    text="🇮🇱עברית",
                    callback_data="change_language_HE",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=TR_BUTTONS["back_to_settings"][language],
                    callback_data="settings",
                ),
            ],
        ]
    )


def settings(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=TR_BUTTONS["back_to_menu"][language],
                    callback_data="back_to_menu",
                ),
                InlineKeyboardButton(
                    text=TR_BUTTONS["change_language"][language],
                    callback_data="change_language",
                ),
            ],
        ]
    )
