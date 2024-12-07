import logging

from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext

from data.application_requests import add_application
from filters.admins_filter import get_random_admin
from filters.phone_valid import is_valid_phone, clean_phone_number
from keyboards.admin_keyboards.main_admin_keyboards import admin_keyboards
from utils.logging_settings import setup_logging
from utils.states import StatesAddApplication
from data.db_connect import get_session

fsm_app_router = Router()

logger = logging.getLogger(setup_logging())


@fsm_app_router.callback_query(F.data == "submit_application")
async def add_name_application(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(StatesAddApplication.NAME)
    await callback_query.message.answer("Напишите свое имя!")


@fsm_app_router.message(StatesAddApplication.NAME)
async def add_phone_number(massage: types.Message, state: FSMContext):
    await state.update_data(name=massage.text)
    await state.set_state(StatesAddApplication.PHONE)
    await massage.answer("Напишите свой номер телефона!")


@fsm_app_router.message(StatesAddApplication.PHONE)
async def add_phone_number(message: types.Message, state: FSMContext, bot: Bot):
    phone = message.text.strip()  # Убираем лишние пробелы
    if not is_valid_phone(phone):  # Проверка на корректность номера
        await message.answer("Введите корректный номер телефона в формате "
                             "+7 (XXX) XXX-XX-XX, 8-XXX-XXX-XX-XX и т.п.")
        return

    clean_phone = clean_phone_number(phone)

    await state.update_data(phone=clean_phone)
    data = await state.get_data()
    await state.clear()

    try:
        async for session in get_session():
            await add_application(
                session=session,
                user_name=data.get("name"),
                phone=data.get("phone"),
            )
        await message.answer("Мы свяжемся с вами в ближайшее время!")
        admin_id = await get_random_admin()
        await bot.send_message(chat_id=admin_id, text=f"❗❗Пришла новая заявка!❗❗\n"
                                                      f"Имя: {data.get('name')}\n"
                                                      f"Телефон: {data.get('phone')}\n"
                                                      "Нажмите на кнопку '⏩Проверить заявки'",
                               reply_markup=await admin_keyboards())
    except Exception as e:
        logger.error(e)

