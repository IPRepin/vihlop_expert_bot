import logging

from aiogram import F, types,  Router

from data.db_connect import get_session
from data.stock_requests import get_stock
from keyboards.user_keyboards.user_keyboards import stock_keyboard, select_stocks_keyboard
from utils.logging_settings import setup_logging

logger = logging.getLogger(setup_logging())

stock_user_router = Router()


@stock_user_router.callback_query(F.data.startswith("stock_"))
async def view_stock(callback_query: types.CallbackQuery):
    async for session in get_session():
        stock_id = int(callback_query.data.split("_")[1])
        stock = await get_stock(session=session, id=stock_id)
        if stock is None:
            await callback_query.answer("Не удалось найти акцию", show_alert=True)
            return
        try:
            await callback_query.message.answer_photo(
                photo=stock.image,
                caption=f"{stock.title}\n"
                        f"{stock.description}\n"
                        f"Цена: {stock.price}\n",
                reply_markup=await stock_keyboard()
            )
        except Exception as e:
            logger.error(e)
        finally:
            await callback_query.answer()


@stock_user_router.callback_query(F.data == "back_stocks")
async def back_stocks(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Выберите акцию", reply_markup=await select_stocks_keyboard())
    await callback_query.answer()