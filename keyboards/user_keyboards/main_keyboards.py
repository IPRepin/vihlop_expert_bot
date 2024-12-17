from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def main_keyboard():
    main_markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text='Акции и скидки'),
            KeyboardButton(text='Оставить отзыв')
        ],
        [
            KeyboardButton(text='Тюнинг выхлопной системы'),
        ],
        [
            KeyboardButton(text='Ремонт глушителя'),
        ],
        [
            KeyboardButton(text='Чип тюнинг двигателя'),
        ],
    ], resize_keyboard=True,
        input_field_placeholder="Выберете одну из опций ниже ⬇️",
        one_time_keyboard=True)
    return main_markup


