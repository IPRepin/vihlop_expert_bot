from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo



async def add_review_keyboard():
    review_clinic_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬Оставить отзыв на Яндекс Картах",
                    web_app=WebAppInfo(url="https://clck.ru/3F2E4p")
                )
            ],
            [InlineKeyboardButton(text="На главное меню",
                                  callback_data="main_keyboard")],
        ]
    )
    return review_clinic_keyboard

