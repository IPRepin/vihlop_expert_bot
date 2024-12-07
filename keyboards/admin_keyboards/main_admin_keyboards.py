from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



async def admin_keyboards() -> ReplyKeyboardMarkup:
    admin_markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="⏩Проверить заявки"),
        ],
        [
            KeyboardButton(text="💾Выгрузить данные пользователей")
        ],
        [
            KeyboardButton(text="📨Отправить рассылку")
        ],
    ],
        resize_keyboard=True
    )
    return admin_markup