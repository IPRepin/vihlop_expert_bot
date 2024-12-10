import logging

from aiogram import types, Router, F

from keyboards.user_keyboards.main_keyboards import (main_keyboard)
from keyboards.user_keyboards.user_keyboards import (add_review_keyboard, select_repair_services_keyboard,
                                                     chip_tuning_keyboard, select_tuning_services_keyboard,
                                                     select_stocks_keyboard)
from utils.logging_settings import setup_logging

main_user_router = Router()

logger = logging.getLogger(setup_logging())


@main_user_router.message(F.text.contains("Акции"))
async def get_stocks_list(message: types.Message):
    await message.answer("Выберите акцию", reply_markup=await select_stocks_keyboard())


@main_user_router.message(F.text.contains("Ремонт") | F.text.contains("Тюнинг"))
async def get_service_list(message: types.Message):
    if "Ремонт" in message.text:
        category_id = 1
        category_name = "ремонта"
        keyboard_func = select_repair_services_keyboard
    elif "Тюнинг" in message.text:
        category_id = 2
        category_name = "тюнинга"
        keyboard_func = select_tuning_services_keyboard
    else:
        return  # Если текст не совпадает, выходим из функции

    await message.answer(f"Выберите услугу {category_name}",
                         reply_markup=await keyboard_func(category_id=category_id))


@main_user_router.message(F.text.contains("Чип"))
async def get_chip_tuning_list(message: types.Message):
    await message.answer("Небольшое описание услуги, приглашение задать вопросы в телеграм",
                         reply_markup=await chip_tuning_keyboard())


@main_user_router.message(F.text.contains("отзыв"))
async def add_review(message: types.Message):
    await message.answer("Оставить отзыв", reply_markup=await add_review_keyboard())


@main_user_router.callback_query(F.data == "main_keyboard")
async def back_to_main_keyboard(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Главное меню", reply_markup=await main_keyboard())
    await callback_query.answer()
