import logging
import random

from aiogram.filters import Filter
from aiogram import types

from sqlalchemy.exc import SQLAlchemyError

from data.admin_requests import get_admin, get_admins
from data.db_connect import get_session

from utils.logging_settings import setup_logging

logger = logging.getLogger(setup_logging())


class AdminsFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        if not message.from_user:
            return False

        user_id = message.from_user.id

        async for session in get_session():
            try:
                admin = await get_admin(session, admin_id=user_id)
                return admin is not None
            except SQLAlchemyError as e:
                logger.error(f"Ошибка при проверке администратора: {e}")
                return False


async def get_random_admin():
    try:
        async for session in get_session():
            try:
                # Получаем всех администраторов из базы
                admins_list = []
                admins = await get_admins(session)
                if not admins:
                    logger.warning("Список администраторов пуст.")
                    return None

                for admin in admins:
                    admins_list.append(int(admin.user_id))

                # Выбираем случайного администратора
                return random.choice(admins_list)
            except SQLAlchemyError as e:
                logger.error(f"Ошибка при получении администраторов: {e}")
                return None
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        return None