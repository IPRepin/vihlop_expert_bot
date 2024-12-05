import logging

from sqlalchemy.ext.asyncio import AsyncSession
from data.models import User

from sqlalchemy import select

from typing import Optional, List

from utils.logging_settings import setup_logging

logger = logging.getLogger(setup_logging())


async def add_user(session: AsyncSession,
                   tg_id: int,
                   username: str,
                   ) -> Optional[User]:
    user = await session.scalar(select(User).where(User.user_id == tg_id))
    try:
        if not user:
            session.add(User(
                user_name=username,
                user_id=tg_id,
            )
            )
            await session.commit()
            await session.refresh(user)
            logger.info("Пользователь %e добавлен", tg_id)
            return user
        else:
            logger.info("Пользователь %e найден", tg_id)
    except Exception as ex:
        logger.error("Ошибка при добавлении пользователя %e", ex)


async def get_user(session: AsyncSession, **kwargs) -> Optional[User]:
    user = await session.scalar(select(User).where(**kwargs))
    if not user:
        logger.info("Пользователь %e не найден", kwargs.get("user_id"))
    return user


async def get_all_users(session: AsyncSession) -> Optional[List[User]]:
    users = await session.scalars(select(User))
    return users.all()


async def delete_user(session: AsyncSession, **kwargs):
    user = await session.scalar(select(User).where(**kwargs))
    if user:
        await session.delete(user)
        await session.commit()
        logger.info("Пользователь %e удален", user.user_id)
    else:
        logger.info("Пользователь %e не найден", kwargs.get("user_id"))
