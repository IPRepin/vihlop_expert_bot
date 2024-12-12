import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter


from config import settings
from handlers.admin_handlers.admin_mailing_hendlers import admin_mailing_router
from handlers.admin_handlers.admin_service_handlers import admin_service_router
from handlers.admin_handlers.admin_stock_handlers import admin_stocks_router
from handlers.admin_handlers.application_admin_handlers import application_admin_router
from handlers.admin_handlers.other_admin_handlers import other_admin_router
from handlers.commad_handlers import main_router
from handlers.user_handlers.fsm_application import fsm_app_router
from handlers.user_handlers.main_handlers import main_user_router
from handlers.user_handlers.service_handlers import service_router
from handlers.user_handlers.stock_user_handlers import stock_user_router
from utils.commands import register_commands
from utils.logging_settings import setup_logging



async def bot_connect():
    storage = RedisStorage.from_url(settings.REDIS_URL)
    bot = Bot(token=settings.TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        application_admin_router,
        admin_stocks_router,
        admin_service_router,
        admin_mailing_router,
        other_admin_router,
        main_user_router,
        stock_user_router,
        fsm_app_router,
        service_router,
        main_router,
    )
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await register_commands(bot)
        await dp.start_polling(bot)
    except TelegramRetryAfter as err:
        logger.error("Превышен лимит запросов к Telegram. Ожидание %s секунд", err.retry_after)
        await asyncio.sleep(err.retry_after)
    except TelegramNetworkError as err:
        logger.error("Ошибка подключения: %s", err)
    except Exception as err:
        logger.error("Неожиданная ошибка: %s", err)
    finally:
        await storage.close()
        await bot.session.close()
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
