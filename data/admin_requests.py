import logging

from sqlalchemy.ext.asyncio import AsyncSession
from data.models import Admin

from sqlalchemy import select, Select

from typing import Optional, List

from utils.logging_settings import setup_logging

logger = logging.getLogger(setup_logging())


async def add_admin(session: AsyncSession, admin_id: int, admin_name: str):
    admin = await session.scalar(select(Admin).where(Admin.id == admin_id))
    if not admin:
        session.add(Admin(user_id=admin_id, user_name=admin_name))
        await session.commit()
        logger.info(f'Admin {admin_id} добавлен')
    else:
        logger.error(f'Admin {admin_id} уже добавлен')


async def get_admins(session: AsyncSession) -> List[Admin]:
    admins = await session.scalars(select(Admin))
    return admins.all()


async def get_admin(session: AsyncSession, admin_id: int) -> Optional[Admin]:
    admin = await session.scalar(select(Admin).where(Admin.user_id == admin_id))
    return admin


async def delete_admin(session: AsyncSession, admin_id: int):
    admin = await session.scalar(select(Admin).where(Admin.id == admin_id))
    if not admin:
        logger.error('Admin %s не найден', admin_id)
    else:
        await session.delete(admin)
        await session.commit()
        logger.info('Admin %s удален', admin_id)
