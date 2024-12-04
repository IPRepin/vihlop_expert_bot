from aiogram import types, Router, F

from keyboards.user_keyboards.user_keyboards import add_review_keyboard

main_user_router = Router()


@main_user_router.message(F.text.contains("Акции"))
async def get_stocks_list(message: types.Message):
    await message.answer("Выберите акцию")


@main_user_router.message(F.text.contains("Ремонт"))
async def get_repair_list(message: types.Message):
    await message.answer("Выберите услугу ремонта")


@main_user_router.message(F.text.contains("Тюнинг"))
async def get_tuning_list(message: types.Message):
    await message.answer("Выберите услугу тюнинга")


@main_user_router.message(F.text.contains("Чип"))
async def get_chip_tuning_list(message: types.Message):
    await message.answer("Выберите услугу чип тюнинга двигателя")


@main_user_router.message(F.text.contains("отзыв"))
async def add_review(message: types.Message):
    await message.answer("Оставить отзыв", reply_markup=await add_review_keyboard())
