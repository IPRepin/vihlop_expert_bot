import logging

from aiogram import F, types,  Router

from data.db_connect import get_session
from data.services_requests import get_service
from keyboards.user_keyboards.user_keyboards import service_keyboard, select_stocks_keyboard, \
    select_repair_services_keyboard, select_tuning_services_keyboard
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
                caption=f"{service.title}\n"
                        f"Описание: {service.description}\n"
                        f"Цена: {service.price}\n"
                        f"Вы можете записаться в сервис по услуге '{service.title}', на "
                        f"бесплатную диагностику или просто "
                        f"напишите нам в Телеграм, и мы ответим на все ваши вопросы!",
                reply_markup=await service_keyboard()
            )
        except Exception as e:
            await callback_query.message.answer("Ошибка при отправке данных.")
            logger.error("Ошибка при отправке фото или текста: %s", e)
        finally:
            await callback_query.answer()


@service_router.callback_query(F.data.startswith("back_services_"))
async def back_services(callback_query: types.CallbackQuery):
    category_id = int(callback_query.data.split("_")[-1])
    if category_id == 1:
        category_name = "ремонта"
        keyboard_func = select_repair_services_keyboard
    elif category_id == 2:
        category_name = "тюнинга"
        keyboard_func = select_tuning_services_keyboard
    else:
        return  # Если текст не совпадает, выходим из функции

    await callback_query.message.answer(f"Выберите услугу {category_name}",
                         reply_markup=await keyboard_func(category_id=category_id))
    await callback_query.answer()