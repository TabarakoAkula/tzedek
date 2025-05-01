from aiogram.fsm.state import State, StatesGroup


class QuestionsStatesGroup(StatesGroup):
    ask_question = State()
    confirm_question = State()
