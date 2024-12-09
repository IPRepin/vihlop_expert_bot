from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def checking_applications():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text="Заявка проверена",
        callback_data="approved",
    ))
    keyboard.add(InlineKeyboardButton(
        text='На главное меню',
        callback_data="main_keyboard_admin"
    ))
    return keyboard.adjust(1).as_markup()
