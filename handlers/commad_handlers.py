import logging

from aiogram import types, Router
from aiogram.filters import CommandStart

from data.db_connect import get_session
from data.user_requests import add_user
from filters.admins_filter import AdminsFilter
from keyboards.admin_keyboards.main_admin_keyboards import admin_keyboards
from utils.logging_settings import setup_logging

from keyboards.user_keyboards.main_keyboards import main_keyboard

main_router = Router()

logger = logging.getLogger(setup_logging())


@main_router.message(CommandStart)
async def command_start(message: types.Message) -> None:
    # Проверка через AdminsFilter
    admins_filter = AdminsFilter()
    is_admin = await admins_filter.__call__(message)

    if is_admin:
        await message.answer("Вы администратор. Добро пожаловать!",
                             reply_markup=await admin_keyboards())
    else:
        async for session in get_session():
            await add_user(session=session,
                           tg_id=message.from_user.id,
                           username=message.from_user.full_name,
                           )

        await message.answer_photo(
            photo="https://ibb.co/2n9hRWx",
            caption=f"Привет {message.from_user.first_name}!\n"
                    "Добро пожаловать Выхлоп эксперт!",
            reply_markup=await main_keyboard()
        )
