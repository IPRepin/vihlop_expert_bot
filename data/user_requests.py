import logging

from sqlalchemy.ext.asyncio import AsyncSession
from data.models import User

from sqlalchemy import select

from typing import Optional

from utils.logging_settings import setup_logging

logger = logging.getLogger(setup_logging())


async def add_user(session: AsyncSession,
                   tg_id: int,
                   username: str,
                   ) -> Optional[User]:
    user = await session.scalar(select(User).where(User.user_id == tg_id))

    if not user:
        session.add(User(
            user_name=username,
            user_id=tg_id,
        )
        )
        await session.commit()
        logger.info("Пользователь %e добавлен", tg_id)
        return user
    else:
        logger.info("Пользователь %e найден", tg_id)
