from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.db_connect import get_session
from data.services_requests import get_services
from data.stock_requests import get_all_stocks

from config import settings


async def add_review_keyboard():
    """
    Клавиатура для добавления отзыва
    """
    review_clinic_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬Оставить отзыв на Яндекс Картах",
                    web_app=WebAppInfo(url=settings.YANDEX_MAP_URL)
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬Оставить отзыв ВКонтакте",
                    web_app=WebAppInfo(url=settings.VK_URL)
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬Оставить отзыв на АВИТО",
                    web_app=WebAppInfo(url=settings.AVITO_URL)
                )
            ],
            [InlineKeyboardButton(text="➡️На главное меню⬅️",
                                  callback_data="main_keyboard")],
        ]
    )
    return review_clinic_keyboard


async def select_repair_services_keyboard(category_id: int):
    """
    Клавиатура для выбора услуги ремонта
    """
    keyboard = InlineKeyboardBuilder()
    async for session in get_session():
        all_services = await get_services(session=session, category_id=category_id)
        if all_services:  # Проверяем, что список услуг не None
            for service in all_services:
                keyboard.add(InlineKeyboardButton(text=service.title, callback_data=f"service_{service.id}"))
    keyboard.add(InlineKeyboardButton(text='➡️На главное меню⬅️', callback_data="main_keyboard"))
    return keyboard.adjust(1).as_markup()


async def select_tuning_services_keyboard(category_id: int):
    """
    Клавиатура для выбора услуги тюнинга
    """
    keyboard = InlineKeyboardBuilder()
    async for session in get_session():
        all_services = await get_services(session=session, category_id=category_id)
        if all_services:  # Проверяем, что список услуг не None
            for service in all_services:
                keyboard.add(InlineKeyboardButton(text=service.title, callback_data=f"service_{service.id}"))
    keyboard.add(InlineKeyboardButton(text='➡️На главное меню⬅️', callback_data="main_keyboard"))
    return keyboard.adjust(1).as_markup()


async def chip_tuning_keyboard():
    """
    Клавиатура для выбора услуги чип-тюнинга
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
                text="✏️Напишите нам",
                url=settings.SUPPORT_URL,
            ))
    keyboard.add(InlineKeyboardButton(text='➡️На главное меню⬅️', callback_data="main_keyboard"))
    return keyboard.adjust(1).as_markup()


async def service_keyboard(category_id: int):
    """
    Клавиатура  'Оставить заявку'
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
                text="✏️Напишите нам",
                url=settings.SUPPORT_URL,
            ))
    keyboard.add(InlineKeyboardButton(text="✏️Записаться на Тюнинг", callback_data="submit_application"))
    keyboard.add(InlineKeyboardButton(text='➡️Предыдущее меню⬅️', callback_data=f"back_services_{category_id}"))
    keyboard.add(InlineKeyboardButton(text='➡️На главное меню⬅️', callback_data="main_keyboard"))
    return keyboard.adjust(1).as_markup()


async def select_stocks_keyboard():
    """
    Клавиатура для выбора акции
    """
    keyboard = InlineKeyboardBuilder()
    async for session in get_session():
        all_stocks = await get_all_stocks(session=session)
        if all_stocks:
            for stock in all_stocks:
                keyboard.add(InlineKeyboardButton(text=stock.title, callback_data=f"stock_{stock.id}"))
    keyboard.add(InlineKeyboardButton(text='➡️На главное меню⬅️', callback_data="main_keyboard"))
    return keyboard.adjust(1).as_markup()


async def stock_keyboard():
    """
    Клавиатура для записи на акцию
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
                text="✏️Напишите нам",
                url=settings.SUPPORT_URL,
            ))
    keyboard.add(InlineKeyboardButton(text="Записаться по акции", callback_data="submit_application"))
    keyboard.add(InlineKeyboardButton(text='➡️Предыдущее меню⬅️', callback_data="back_stocks"))
    keyboard.add(InlineKeyboardButton(text='➡️На главное меню⬅️', callback_data="main_keyboard"))
    return keyboard.adjust(1).as_markup()