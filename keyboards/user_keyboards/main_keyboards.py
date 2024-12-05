from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.db_connect import get_session
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

from data.services_requests import get_services


async def main_keyboard():
    main_markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text='Акции и скидки'),
            KeyboardButton(text='Оставить отзыв')
        ],
        [
            KeyboardButton(text='Ремонт глушителя'),
        ],
        [
            KeyboardButton(text='Тюнинг выхлопной системы'),
        ],
        [
            KeyboardButton(text='Чип тюнинг двигателя'),
        ],
    ], resize_keyboard=True,
        input_field_placeholder="Выберете одну из опций ниже ⬇️",
        one_time_keyboard=True)
    return main_markup


async def repair_services_keyboard(category_id: int):
    keyboard = InlineKeyboardBuilder()
    async for session in get_session():
        all_services = await get_services(session=session, category_id=category_id)
        for service in all_services:
            keyboard.add(InlineKeyboardButton(text=service.title, callback_data=f"service_{service.id}"))
    keyboard.add(InlineKeyboardButton(text='На главное меню', callback_data="main_keyboard"))
    return keyboard.adjust(1).as_markup()


async def chip_tuning_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
                text="📲Связаться через телеграм",
                url="https://t.me/TriBubi",
            ))
    keyboard.add(InlineKeyboardButton(text='На главное меню', callback_data="main_keyboard"))
    return keyboard.adjust(1).as_markup()