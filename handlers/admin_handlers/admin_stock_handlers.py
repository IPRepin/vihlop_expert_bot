import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import ProgrammingError

from data.db_connect import get_session
from data.stock_requests import add_stock_requests, delete_stock_requests, update_stock
from filters.admins_filter import AdminsFilter
from keyboards.admin_keyboards.stocks_admin_keyboards import stocks_admin_keyboards, select_admin_stocks_keyboard
from utils.logging_settings import setup_logging
from utils.states import StatesAddStocks, StatesDeleteStocks, StatesEditStocks

logger = logging.getLogger(setup_logging())

admin_stocks_router = Router()


@admin_stocks_router.message(AdminsFilter(),
                             F.text == "Меню акций")
async def admin_stock_handler(message: types.Message) -> None:
    await message.answer("Меню работы с акциями", reply_markup=await stocks_admin_keyboards())


@admin_stocks_router.message(AdminsFilter(), F.text == "Добавить акцию")
async def add_title_stock(message: types.Message, state: FSMContext) -> None:
    await state.set_state(StatesAddStocks.TITLE)
    await message.answer("Введите название акции")


@admin_stocks_router.message(AdminsFilter(), StatesAddStocks.TITLE)
async def add_description_stock(message: types.Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await message.answer("Введите описание акции")
    await state.set_state(StatesAddStocks.DESCRIPTION)


@admin_stocks_router.message(AdminsFilter(), StatesAddStocks.DESCRIPTION)
async def add_image_stock(message: types.Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await message.answer("Добавьте изображение")
    await state.set_state(StatesAddStocks.IMAGE)


@admin_stocks_router.message(AdminsFilter(), StatesAddStocks.IMAGE, F.photo)
async def add_prices_stock(message: types.Message, state: FSMContext) -> None:
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Введите цену услуги по акции")
    await state.set_state(StatesAddStocks.PRICE)


@admin_stocks_router.message(AdminsFilter(), StatesAddStocks.PRICE)
async def add_new_stock(message: types.Message, state: FSMContext) -> None:
    await state.update_data(price=message.text)
    data = await state.get_data()
    await state.clear()
    async for session in get_session():
        await add_stock_requests(session,
                                 title=data.get("title"),
                                 description=data.get("description"),
                                 image=data.get("image"),
                                 price=data.get("price"))
    await message.answer(f"Добавлена акция {data.get('title')}", reply_markup=await stocks_admin_keyboards())


@admin_stocks_router.message(AdminsFilter(), F.text == "Удалить акцию")
async def select_delete_stock(message: types.Message, state: FSMContext) -> None:
    await state.set_state(StatesDeleteStocks.ID)
    await message.answer("Выберете акцию для удаления:",
                         reply_markup=await select_admin_stocks_keyboard())


@admin_stocks_router.callback_query(AdminsFilter(), StatesDeleteStocks.ID)
async def delete_stock(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.update_data(stock_id=callback_query.data.split("_")[-1])
    await callback_query.answer()
    data = await state.get_data()
    await state.clear()
    try:
        async for session in get_session():
            await delete_stock_requests(session=session, id=int(data.get("stock_id")))
        await callback_query.message.answer("Акция удалена", reply_markup=await stocks_admin_keyboards())
    except ProgrammingError as e:
        logger.error(e)


@admin_stocks_router.message(AdminsFilter(), F.text == "Редактировать акцию")
async def select_edit_stock(message: types.Message, state: FSMContext) -> None:
    await state.set_state(StatesEditStocks.ID)
    await message.answer("Выберете акцию для редактирования:",
                         reply_markup=await select_admin_stocks_keyboard())


@admin_stocks_router.callback_query(AdminsFilter(), StatesEditStocks.ID)
async def edit_title_stock(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.update_data(id_stock=callback_query.data.split("_")[-1])
    await callback_query.answer()
    await state.set_state(StatesEditStocks.TITLE)
    await callback_query.message.answer("Введите новое название акции")


@admin_stocks_router.message(AdminsFilter(), StatesEditStocks.TITLE)
async def edit_description_stock(message: types.Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(StatesEditStocks.DESCRIPTION)
    await message.answer("Введите новое описание акции")


@admin_stocks_router.message(AdminsFilter(), StatesEditStocks.DESCRIPTION)
async def edit_image_stock(message: types.Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(StatesEditStocks.IMAGE)
    await message.answer("Добавьте изображение.")


@admin_stocks_router.message(AdminsFilter(), StatesEditStocks.IMAGE, F.photo)
async def edit_prices_stock(message: types.Message, state: FSMContext) -> None:
    await state.update_data(image=message.photo[-1].file_id)
    await state.set_state(StatesEditStocks.PRICE)
    await message.answer("Введите новую цену услуги по акции")


@admin_stocks_router.message(AdminsFilter(), StatesEditStocks.PRICE)
async def edit_new_stock(message: types.Message, state: FSMContext) -> None:
    await state.update_data(price=message.text)
    data = await state.get_data()
    await state.clear()
    async for session in get_session():
        await update_stock(
            session=session,
            stock_id=int(data.get("id_stock")),
            title=data.get("title"),
            description=data.get("description"),
            image=data.get("image"),
            price=data.get("price")
        )
    await message.answer(f"Акция {data.get('title')} изменена", reply_markup=await stocks_admin_keyboards())


@admin_stocks_router.message(AdminsFilter(), StatesAddStocks.IMAGE, ~F.photo)
async def incorrect_service_add_photo(message: types.Message, state: FSMContext) -> None:
    await message.answer("Нужно загрузить фотографию!")


@admin_stocks_router.message(AdminsFilter(), StatesEditStocks.IMAGE, ~F.photo)
async def incorrect_service_edit_photo(message: types.Message, state: FSMContext) -> None:
    await message.answer("Нужно загрузить фотографию!")
