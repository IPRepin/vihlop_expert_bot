import pytest
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

@pytest.fixture
async def bot():
    """Create test bot instance."""
    # Используем формат реального токена для тестов
    bot = Bot(token="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789", default=DefaultBotProperties(parse_mode="HTML"))
    try:
        yield bot
    finally:
        await bot.session.close()

@pytest.fixture
async def dp():
    """Create test dispatcher instance."""
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    return dp

@pytest.fixture
def message_mock():
    """Create message mock."""
    class MessageMock:
        def __init__(self):
            self.text = ""
            self.answered = False
            self.answer_text = ""
            self.reply_markup = None

        async def answer(self, text, reply_markup=None):
            self.answered = True
            self.answer_text = text
            self.reply_markup = reply_markup
            return self

    return MessageMock()

@pytest.fixture
def callback_query_mock():
    """Create callback query mock."""
    class CallbackQueryMock:
        def __init__(self):
            self.data = ""
            self.message = None
            self.answered = False

        async def answer(self):
            self.answered = True
            return self

    return CallbackQueryMock()
