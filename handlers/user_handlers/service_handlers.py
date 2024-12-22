import logging

from aiogram import F, types,  Router

from data.db_connect import get_session
from data.services_requests import get_service
from keyboards.user_keyboards.user_keyboards import service_keyboard, select_stocks_keyboard
from utils.logging_settings import setup_logging

service_router = Router()

logger = logging.getLogger(setup_logging())


@service_router.callback_query(F.data.startswith("service_"))
async def view_service(callback_query: types.CallbackQuery):
    async for session in get_session():
        service_id = int(callback_query.data.split("_")[1])
        service = await get_service(session=session, id=service_id)
        if service is None:
            await callback_query.message.answer("Услуга не найдена.")
            await callback_query.answer()
            return
        try:
            await callback_query.message.answer_photo(
                photo=service.image,
                caption=f"Услуга: {service.title}\n"
                        f"Описание: {service.description}\n"
                        f"Цена: {service.price}\n"
                        f"Узнать подробнее об услуге {service.title}, записаться на "
                        f"бесплатную диагностику вы можете оставив заявку или просто "
                        f"напишите нам в Телеграм!",
                reply_markup=await service_keyboard()
            )
        except Exception as e:
            await callback_query.message.answer("Ошибка при отправке данных.")
            logger.error("Ошибка при отправке фото или текста: %s", e)
        finally:
            await callback_query.answer()


@service_router.callback_query(F.data == "back_services")
async def back_services(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Выберете услугу", reply_markup=await select_stocks_keyboard())
    await callback_query.answer()