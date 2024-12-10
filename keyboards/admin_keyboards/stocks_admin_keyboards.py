from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.db_connect import get_session
from data.stock_requests import get_all_stocks


async def stocks_admin_keyboards() -> ReplyKeyboardMarkup:
    main_markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text='Добавить акцию'),
            KeyboardButton(text='Удалить акцию'),
        ],
        [
            KeyboardButton(text='Редактировать акцию'),
            KeyboardButton(text='◀️НАЗАД'),
        ]
    ], resize_keyboard=True,
        input_field_placeholder="Выберете одну из опций ниже ⬇️",
        one_time_keyboard=True)
    return main_markup


async def tuning_admin_stocks_keyboard():
    keyboard = InlineKeyboardBuilder()
    async for session in get_session():
        all_stocks = await get_all_stocks(session=session)
        if all_stocks:
            for stock in all_stocks:
                keyboard.add(InlineKeyboardButton(text=stock.title, callback_data=f"admin_stock_{stock.id}"))
    keyboard.add(InlineKeyboardButton(text='На главное меню', callback_data="main_admin_keyboard"))
    return keyboard.adjust(1).as_markup()
