import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from data.models import Service

from typing import Optional, List

from utils.logging_settings import setup_logging

logger = logging.getLogger(setup_logging())


async def add_service(session: AsyncSession,
                      title: str,
                      description: str,
                      price: str,
                      image: str,
                      category: int, ) -> None:
    service = await session.scalar(select(Service).where(Service.title == title))
    try:
        if service is None:
            service = Service(title=title,
                              description=description,
                              price=price,
                              image=image,
                              category_id=category)
            session.add(service)
            await session.commit()
            await session.refresh(service)
            logger.info('Услуга %s добавлена в базу данных', service.title)
        else:
            logger.info("Услуга %s уже есть в базе данных", service.title)
    except Exception as e:
        logger.error("Ошибка при добавлении сервиса %s", e)


async def get_services(session: AsyncSession, **kwargs) -> List[Service]:
    try:
        stmt = select(Service).filter_by(**kwargs)  # Используем filter_by для удобства
        services = await session.scalars(stmt)
        return services.all()
    except Exception as e:
        logger.error("Ошибка при получении списка услуг %s", e)
        return []  # Возвращаем пустой список вместо None


async def get_service(session: AsyncSession, **kwargs) -> Optional[Service]:
    try:
        query = select(Service).filter_by(**kwargs)
        service = await session.scalar(query)
        if service:
            return service
        logger.error("Услуга не найдена")
    except Exception as e:
        logger.error("Ошибка при получении услуги: %s", e)
    return None  # Явно возвращаем None, если ничего не найдено



async def delete_service(session: AsyncSession, **kwargs) -> None:
    try:
        service = await session.scalar(select(Service).filter_by(**kwargs))
        if service:
            await session.delete(service)
            await session.commit()
            logger.info("Услуга %s удалена из базы данных", service.title)
        else:
            logger.error("Услуга не найдена")
    except Exception as e:
        logger.error("Ошибка при удалении услуги %s", e)


async def update_service(session: AsyncSession, id_service: int, **kwargs) -> None:
    try:
        service = await session.scalar(select(Service).filter_by(id=id_service))
        if service:
            service.title = kwargs.get('title')
            service.description = kwargs.get('description')
            service.price = kwargs.get('price')
            service.image = kwargs.get('image')
            service.category_id = kwargs.get('category_id')
            await session.commit()
            logger.info("Услуга %s обновлена", service.title)
        else:
            logger.error("Услуга не найдена")
    except Exception as e:
        logger.error("Ошибка при обновлении услуги %s", e)
