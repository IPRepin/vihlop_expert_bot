import logging

from sqlalchemy.ext.asyncio import AsyncSession
from data.models import Category

from sqlalchemy import select

from typing import Optional, List

from utils.logging_settings import setup_logging

logger = logging.getLogger(setup_logging())


async def add_category(session: AsyncSession, title: str) -> Category:
    category = await session.scalar(select(Category).where(Category.title == title))
    if not category:
        session.add(
            Category(title=title)
        )
        await session.commit()
        logger.info("Добавлена категория %s", title)
        return category
    else:
        logger.info("Категория %s уже существует", title)


async def get_categories(session: AsyncSession) -> List[Category]:
    categories = await session.scalars(select(Category))
    return categories.all()


async def get_category(session: AsyncSession, title: str) -> Optional[Category]:
    category = await session.scalar(select(Category).where(Category.title == title))
    if not category:
        logger.info("Категория %s не найдена", title)
    return category


async def delete_category(session: AsyncSession, title: str):
    category = await session.scalar(select(Category).where(Category.title == title))
    if not category:
        logger.info("Категория %s не найдена", title)
    else:
        await session.delete(category)
        await session.commit()
        logger.info("Категория %s удалена", title)

