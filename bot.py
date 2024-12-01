import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter


from config import settings
from handlers.commad_handlers import main_router
from utils.commands import register_commands
from utils.logging_settings import setup_logging



async def bot_connect():
    storage = RedisStorage.from_url(settings.REDIS_URL)
    bot = Bot(token=settings.TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        main_router,
    )
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
        await register_commands(bot)
    except TelegramNetworkError as err:
        logger.error("Ошибка подключения /n %s", err)
    finally:
        await bot.close()


def main():
    try:
        asyncio.run(bot_connect())
    except TelegramRetryAfter as error:
        logger.error(error)
    except KeyboardInterrupt as error:
        logger.error(error)


if __name__ == '__main__':
    setup_logging()
    logger = logging.getLogger(setup_logging())
    main()

