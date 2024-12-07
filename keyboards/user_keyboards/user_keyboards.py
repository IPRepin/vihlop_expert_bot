from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.db_connect import get_session
from data.services_requests import get_services


async def add_review_keyboard():
    review_clinic_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬Оставить отзыв на Яндекс Картах",
                    web_app=WebAppInfo(url="https://clck.ru/3F2E4p")
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬Оставить отзыв ВКонтакте",
                    web_app=WebAppInfo(url="https://vk.com/vihlopexpert")
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬Оставить отзыв на АВИТО",
                    web_app=WebAppInfo(url="https://www.avito.ru/brands/8f51494e77196e4becadd0029507402d?src=sharing")
                )
            ],
            [InlineKeyboardButton(text="На главное меню",
                                  callback_data="main_keyboard")],
        ]
    )
    return review_clinic_keyboard


async def repair_services_keyboard(category_id: int):
    keyboard = InlineKeyboardBuilder()
    async for session in get_session():
        all_services = await get_services(session=session, category_id=category_id)
        if all_services:  # Проверяем, что список услуг не None
            for service in all_services:
                keyboard.add(InlineKeyboardButton(text=service.title, callback_data=f"service_{service.id}"))
    keyboard.add(InlineKeyboardButton(text='На главное меню', callback_data="main_keyboard"))
    return keyboard.adjust(1).as_markup()


async def tuning_services_keyboard(category_id: int):
    keyboard = InlineKeyboardBuilder()
    async for session in get_session():
        all_services = await get_services(session=session, category_id=category_id)
        if all_services:  # Проверяем, что список услуг не None
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


async def service_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
                text="📲Связаться через телеграм",
                url="https://t.me/TriBubi",
            ))
    keyboard.add(InlineKeyboardButton(text="Оставить заявку", callback_data="submit_application"))
    keyboard.add(InlineKeyboardButton(text='К выбору услуг', callback_data="back_services"))
    return keyboard.adjust(1).as_markup()
