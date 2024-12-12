from aiogram import types, F, Router

from filters.admins_filter import AdminsFilter
from keyboards.user_keyboards.main_keyboards import main_keyboard

other_admin_router = Router()


@other_admin_router.message(AdminsFilter(), F.text == "Меню пользователя")
async def go_to_user_menu(message: types.Message):
    await message.answer("Вы перешли в меню пользователя.\n"
                         "Для возврата в меню администратора введите команду \n"
                         "/start", reply_markup=await main_keyboard())