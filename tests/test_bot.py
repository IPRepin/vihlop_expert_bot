import pytest
from aiogram import Bot, Dispatcher


@pytest.mark.asyncio
async def test_bot_initialization(bot, dp):
    """Test bot initialization."""
    assert isinstance(bot, Bot)
    assert isinstance(dp, Dispatcher)
