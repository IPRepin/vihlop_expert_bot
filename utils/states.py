from aiogram.fsm.state import StatesGroup, State


class StatesAddApplication(StatesGroup):
    """
    Модуль определения состояний для добавления заявки
    """
    NAME = State()
    PHONE = State()


class StatesApplication(StatesGroup):
    """
    Модуль определения состояний для проверки заявки
    """
    APPLICATION_ID = State()


class StatesAddStocks(StatesGroup):
    """
    Модуль определения состояний для добавления акций
    """
    TITLE = State()
    DESCRIPTION = State()
    IMAGE = State()
    PRICE = State()


class StatesDeleteStocks(StatesGroup):
    """
    Модуль определения состояний для удаления акций
    """
    ID = State()


class StatesEditStocks(StatesGroup):
    """
    Модуль определения состояний для изменения акций
    """
    ID = State()
    TITLE = State()
    DESCRIPTION = State()
    IMAGE = State()
    PRICE = State()
