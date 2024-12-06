from aiogram.fsm.state import StatesGroup, State


class StatesAddApplication(StatesGroup):
    """
    Модуль определения состояний для добавления заявки
    """
    NAME = State()
    PHONE = State()