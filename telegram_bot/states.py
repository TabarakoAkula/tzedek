from aiogram.fsm.state import State, StatesGroup


class QuestionsStatesGroup(StatesGroup):
    ask_question = State()
    confirm_question = State()


class ChooseLanguageStatesGroup(StatesGroup):
    start_handler = State()


class SettingsStatesGrou(StatesGroup):
    settings_handler = State()
