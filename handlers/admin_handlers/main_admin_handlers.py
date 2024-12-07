import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from data.application_requests import get_application_by_filter, update_application
from data.db_connect import get_session
from filters.admins_filter import AdminsFilter
from keyboards.admin_keyboards.other_admin_keyboards import checking_applications
from utils.logging_settings import setup_logging
from utils.states import StatesApplication

main_admin_router = Router()

logger = logging.getLogger(setup_logging())


@main_admin_router.message(
    AdminsFilter(),
    F.text.contains("Проверить заявки")
)
async def get_new_application(message: types.Message, state: FSMContext):
    try:
        async for session in get_session():
            application = await get_application_by_filter(session=session, viewed=False)
            if application:
                await state.set_state(StatesApplication.APPLICATION_ID)
                await state.update_data(application_id=application.id)
                await message.answer(f"Новая заявка от {application.user_name}\n"
                                     f"Телефон: {application.phone}",
                                     reply_markup=await checking_applications())

            else:
                await message.answer("😎Все заявки проверены!")
    except Exception as e:
        logger.error(e)


@main_admin_router.callback_query(AdminsFilter(),
                                  F.data == "approved",
                                  StatesApplication.APPLICATION_ID
                                  )
async def approved_application(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    try:
        async for session in get_session():
            data = await state.get_data()
            await state.clear()
            await update_application(session=session, id=int(data.get("application_id")))
            await callback_query.message.answer("��Заявка успешно подтверждена!")
    except Exception as e:
        logger.error(e)
