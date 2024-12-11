from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.db_connect import get_session
from data.services_requests import get_services


async def service_admin_keyboards() -> ReplyKeyboardMarkup:
    main_markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text='Добавить услугу'),
            KeyboardButton(text='Удалить услугу'),
        ],
        [
            KeyboardButton(text='Редактировать услугу'),
            KeyboardButton(text='◀️НАЗАД'),
        ]
    ], resize_keyboard=True,
        input_field_placeholder="Выберете одну из опций ниже ⬇️",
        one_time_keyboard=True)
    return main_markup


async def select_category_keyboard():
    main_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Ремонт глушителей",
                    callback_data="repair_1"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Тюнинг выхлопной системы",
                    callback_data="repair_2"
                )
            ],
        ]
    )
    return main_keyboard

async def select_admin_service_keyboard(category_id: int):
    keyboard = InlineKeyboardBuilder()
    async for session in get_session():
        all_services = await get_services(session=session, category_id=category_id)
        if all_services:
            for service in all_services:
                keyboard.add(InlineKeyboardButton(text=service.title, callback_data=f"admin_service_{service.id}"))
    keyboard.add(InlineKeyboardButton(text='На главное меню', callback_data="main_admin_keyboard"))
    return keyboard.adjust(1).as_markup()