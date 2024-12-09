import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from data.models import Stock

from typing import Optional, List

from utils.logging_settings import setup_logging

logger = logging.getLogger(setup_logging())


async def add_stock_requests(session: AsyncSession,
                             title: str,
                             image: str,
                             description: str,
                             price: str,) -> None:
    stock = session.scalar(select(Stock).where(Stock.title == title))
    if not stock:
        stock = Stock(title=title,
                      image=image,
                      description=description,
                      price=price)
        session.add(stock)
        await session.commit()
        await session.refresh(stock)
        logger.debug('Акция %s добавлена', stock.title)
    else:
        logger.debug("Акция уже существует")


async def get_stock_requests(session: AsyncSession, **kwargs) -> Optional[Stock]:
    try:
        query = select(Stock).filter_by(**kwargs)
        stock = await session.scalar(query)
        if stock:
            return stock
        logger.error("Акция не найдена")
    except Exception as e:
        logger.error("Ошибка при получении акции: %s", e)
    return None


async def get_all_stocks(session: AsyncSession, **kwargs) -> List[Stock]:
    try:
        query = select(Stock).filter_by(**kwargs)
        stocks = await session.scalars(query)
        return stocks.all()
    except Exception as e:
        logger.error("Ошибка при получении акций: %s", e)
    return []


async def delete_stock_requests(session: AsyncSession, **kwargs) -> None:
    try:
        query = select(Stock).filter_by(**kwargs)
        stock = await session.scalar(query)
        if stock:
            await session.delete(stock)
            await session.commit()
            logger.debug(f'Stock {stock.title} deleted')
        else:
            logger.error("Акция не найдена")
    except Exception as e:
        logger.error("Ошибка при удалении акции: %s", e)


async def update_stock(session: AsyncSession, **kwargs) -> None:
    try:
        stock = await session.scalar(select(Stock).where(**kwargs))
        if stock:
            stock.title = kwargs.get('title')
            stock.description = kwargs.get('description')
            stock.price = kwargs.get('price')
            stock.image = kwargs.get('image')
            await session.commit()
            logger.info("Акция %s обновлена", stock.title)
        else:
            logger.error("Акция не найдена")
    except Exception as e:
        logger.error("Ошибка при обновлении акции %s", e)
