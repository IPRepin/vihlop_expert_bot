import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import ProgrammingError

from data.db_connect import get_session
from data.services_requests import add_service, delete_service, update_service
from filters.admins_filter import AdminsFilter
from keyboards.admin_keyboards.service_admin_keyboards import (service_admin_keyboards,
                                                               select_category_keyboard,
                                                               select_admin_service_keyboard)
from utils.logging_settings import setup_logging
from utils.states import (StatesAddService, StatesDeleteService, StatesEditService)

logger = logging.getLogger(setup_logging())

admin_service_router = Router()


@admin_service_router.message(AdminsFilter(), F.text == "Меню услуг")
async def admin_service_handler(message: types.Message):
    await message.answer("Меню работы с услугами", reply_markup=await service_admin_keyboards())


@admin_service_router.message(AdminsFilter(), F.text == "Добавить услугу")
async def add_service_handler(message: types.Message, state: FSMContext):
    await state.set_state(StatesAddService.CATEGORY)
    await message.answer("Выберите направление услуги", reply_markup=await select_category_keyboard())


@admin_service_router.callback_query(AdminsFilter(), StatesAddService.CATEGORY)
async def add_title_service_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback_query.data.split("_")[-1])
    await callback_query.answer()
    await state.set_state(StatesAddService.TITLE)
    await callback_query.message.answer("Введите название услуги")


@admin_service_router.message(AdminsFilter(), StatesAddService.TITLE)
async def add_description_service_handler(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите описание услуги")
    await state.set_state(StatesAddService.DESCRIPTION)


@admin_service_router.message(AdminsFilter(), StatesAddService.DESCRIPTION)
async def add_image_service_handler(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Добавьте прямую ссылку на изображение.\n"
                         "Прямую ссылку можно получить загрузив изображение на сайт:\n"
                         "https://imgbb.com/")
    await state.set_state(StatesAddService.IMAGE)


@admin_service_router.message(AdminsFilter(), StatesAddService.IMAGE)
async def add_product_service_handler(message: types.Message, state: FSMContext):
    await state.update_data(image=message.text)
    await state.set_state(StatesAddService.PRICE)
    await message.answer("Введите стоимость услуги")


@admin_service_router.message(AdminsFilter(), StatesAddService.PRICE)
async def add_new_service_handler(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await state.clear()

    async for session in get_session():
        await add_service(
            session=session,
            title=data.get("title"),
            description=data.get("description"),
            image=data.get("image"),
            price=data.get("price"),
            category=int(data.get("category")),
        )
    await message.answer(f"Добавлена услуга {data.get('title')}", reply_markup=await service_admin_keyboards())


@admin_service_router.message(AdminsFilter(), F.text == "Удалить услугу")
async def remove_service_select_category(message: types.Message, state: FSMContext):
    await state.set_state(StatesDeleteService.CATEGORY)
    await message.answer("Выберите категорию услуги", reply_markup=await select_category_keyboard())


@admin_service_router.callback_query(AdminsFilter(), StatesDeleteService.CATEGORY)
async def remove_service_select_service(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    category_id = callback_query.data.split("_")[-1]
    await state.update_data(category=category_id)
    await state.set_state(StatesDeleteService.ID_SERVICE)
    await callback_query.message.answer(
        "Выберите услугу",
        reply_markup=await select_admin_service_keyboard(category_id=int(category_id))
    )
    await callback_query.answer()


@admin_service_router.callback_query(AdminsFilter(), StatesDeleteService.ID_SERVICE)
async def remove_service_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(service_id=callback_query.data.split("_")[-1])
    await callback_query.answer()
    data = await state.get_data()
    await state.clear()
    try:
        async for session in get_session():
            await delete_service(session=session, id=int(data.get("service_id")))
        await callback_query.message.answer("Услуга удалена", reply_markup=await service_admin_keyboards())
    except ProgrammingError as e:
        logger.error(e)


@admin_service_router.message(AdminsFilter(), F.text == "Редактировать услугу")
async def edit_service_select_category(message: types.Message, state: FSMContext):
    await state.set_state(StatesEditService.CATEGORY)
    await message.answer("Выберите категорию услуги", reply_markup=await select_category_keyboard())


@admin_service_router.callback_query(AdminsFilter(), StatesEditService.CATEGORY)
async def edit_service_select_service(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback_query.data.split("_")[-1])
    await state.set_state(StatesEditService.ID_SERVICE)
    await callback_query.message.answer("Выберите услугу",
                                        reply_markup=await select_admin_service_keyboard(
                                            category_id=int(callback_query.data.split("_")[-1])
                                        ))


@admin_service_router.callback_query(AdminsFilter(), StatesEditService.ID_SERVICE)
async def edit_service_title(callback_query: types.CallbackQuery, state: FSMContext):
    service_id = callback_query.data.split("_")[-1]
    print(service_id)
    await state.update_data(service_id=service_id)
    await callback_query.answer()
    await state.set_state(StatesEditService.TITLE)
    await callback_query.message.answer("Введите новое название услуги")


@admin_service_router.message(AdminsFilter(), StatesEditService.TITLE)
async def edit_service_description(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(StatesEditService.DESCRIPTION)
    await message.answer("Введите новое описание услуги")


@admin_service_router.message(AdminsFilter(), StatesEditService.DESCRIPTION)
async def edit_service_image(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(StatesEditService.IMAGE)
    await message.answer("Добавьте прямую ссылку на изображение.\n"
                         "Прямую ссылку можно получить загрузив изображение на сайт:\n"
                         "https://imgbb.com/")


@admin_service_router.message(AdminsFilter(), StatesEditService.IMAGE)
async def edit_service_price(message: types.Message, state: FSMContext):
    await state.update_data(image=message.text)
    await state.set_state(StatesEditService.PRICE)
    await message.answer("Введите новую стоимость услуги")


@admin_service_router.message(AdminsFilter(), StatesEditService.PRICE)
async def edit_service(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await state.clear()
    async for session in get_session():
        await update_service(
            session=session,
            id_service=int(data.get("service_id")),
            title=data.get("title"),
            description=data.get("description"),
            image=data.get("image"),
            price=data.get("price"),
            category_id=int(data.get("category")),
        )
    await message.answer(f"Услуга {data.get('title')} изменена", reply_markup=await service_admin_keyboards())
