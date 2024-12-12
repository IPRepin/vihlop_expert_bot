from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def admin_keyboards() -> ReplyKeyboardMarkup:
    admin_markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="⏩Проверить заявки"),
            KeyboardButton(text="📨Отправить рассылку"),
        ],
        [
            KeyboardButton(text="💾Выгрузить данные пользователей")
        ],
        [
            KeyboardButton(text="Меню услуг"),
            KeyboardButton(text="Меню акций")
        ],
        [
            KeyboardButton(text="Меню пользователя"),
        ],
    ],
        resize_keyboard=True
    )
    return admin_markup

async def get_confirm_button() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Добавить кнопку", callback_data="add_mailing_button")
    keyboard_builder.button(text="Продолжить без кнопки", callback_data="no_mailing_button")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def confirm_keyboard() -> InlineKeyboardMarkup:
    confirm_maling_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Отправить",
                    callback_data="confirm_mailing"
                )
            ],
            [InlineKeyboardButton(
                text="Отменить",
                callback_data="cancel_mailing"
            )],
        ])
    return confirm_maling_button


async def add_mailing_button(text_button: str, url_button: str) -> InlineKeyboardMarkup:
    added_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=text_button,
                url=url_button
            )]
        ]
    )
    return added_keyboard
