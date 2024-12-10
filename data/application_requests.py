import logging

from sqlalchemy.ext.asyncio import AsyncSession
from data.models import Application

from sqlalchemy import select

from typing import Optional

from utils.logging_settings import setup_logging

logger = logging.getLogger(setup_logging())


async def add_application(session: AsyncSession, user_name: str, phone: str) -> Optional[Application]:
    try:
        # Проверяем наличие заявки с указанным телефоном
        application = await session.scalar(select(Application).filter_by(phone=phone))

        if application:
            # Если заявка существует и поле viewed == True, обновляем его на False
            if application.viewed:
                application.viewed = False
                application.user_name = user_name
                await session.commit()
                await session.refresh(application)
            return application
        else:
            # Если заявки не существует, создаем новую
            application = Application(user_name=user_name, phone=phone)
            session.add(application)
            await session.commit()
            await session.refresh(application)
            logger.info("Добавлена заявка от %s с телефоном %s", user_name, phone)
            return application

    except Exception as ex:
        logger.error("Ошибка при добавлении заявки %s", ex)
        return None

async def get_all_applications(session: AsyncSession) -> Optional[Application]:
    try:
        applications = await session.scalars(select(Application))
        return applications.all()
    except Exception as ex:
        logger.error("Ошибка при получении заявок %s", ex)
        return None


async def get_application_by_filter(session: AsyncSession, **kwargs) -> Optional[Application]:
    try:
        application = await session.scalar(select(Application).filter_by(**kwargs))
        return application
    except Exception as ex:
        logger.error("Ошибка при получении заявок %s", ex)
        return None

async def update_application(session: AsyncSession, **kwargs) -> Application:
    try:
        application = await session.scalar(select(Application).filter_by(**kwargs))
        application.viewed = True
        await session.commit()
        await session.refresh(application)
        return application
    except Exception as ex:
        logger.error("Ошибка при обновлении заявки %s", ex)
