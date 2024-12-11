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


class StatesAddService(StatesGroup):
    """
    Модуль определения состояний для добавления услуг
    """
    CATEGORY = State()
    TITLE = State()
    PRICE = State()
    IMAGE = State()
    DESCRIPTION = State()

class StatesEditService(StatesGroup):
    """
    Модуль определения состояний для изменения услуг
    """
    CATEGORY = State()
    ID_SERVICE = State()
    TITLE = State()
    PRICE = State()
    IMAGE = State()
    DESCRIPTION = State()

class StatesDeleteService(StatesGroup):
    """
    Модуль определения состояний для удаления услуг
    """
    CATEGORY = State()
    ID_SERVICE = State()

