import logging
import os
from datetime import datetime

from aiogram import types, Router, F, Bot
from aiogram.types import FSInputFile

from data.db_connect import get_session
from data.user_requests import get_all_users
from utils.auxiliary_module import new_file
from utils.logging_settings import setup_logging

logger = logging.getLogger(setup_logging())

download_router = Router()


@download_router.message(F.text == '💾Выгрузить данные пользователей')
async def download_all_button(message: types.Message, bot: Bot) -> None:
    name_file = datetime.now().strftime('%d-%m-%Y')
    logger.info(f"Start download file {name_file}")

    async for session in get_session():
        data = await get_all_users(session)

        # Если данных нет, отправляем сообщение об этом
        if not data:
            await message.answer("В базе данных нет заполненных анкет")
            return

        # Создаём CSV-файл
        new_file(data=data, query='all')
        await message.answer("Файл будет сформирован в течение нескольких секунд...")

        # Отправляем файл
        download_file = FSInputFile(f'data/all_{name_file}.csv')
        try:
            await bot.send_document(chat_id=message.chat.id, document=download_file)
        finally:
            # Удаляем файл после отправки
            os.remove(f'data/all_{name_file}.csv')
            logger.info("Deleted file")
