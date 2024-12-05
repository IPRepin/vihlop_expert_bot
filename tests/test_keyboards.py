import pytest
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from keyboards.user_keyboards.main_keyboards import (
    repair_services_keyboard,
    chip_tuning_keyboard,
    main_keyboard
)
from keyboards.user_keyboards.user_keyboards import add_review_keyboard

@pytest.mark.asyncio
async def test_repair_services_keyboard():
    keyboard = await repair_services_keyboard(category_id=1)
    assert isinstance(keyboard, InlineKeyboardMarkup)
    # Add more specific assertions based on your keyboard structure

@pytest.mark.asyncio
async def test_chip_tuning_keyboard():
    keyboard = await chip_tuning_keyboard()
    assert isinstance(keyboard, InlineKeyboardMarkup)
    # Add more specific assertions based on your keyboard structure

@pytest.mark.asyncio
async def test_main_keyboard():
    keyboard = await main_keyboard()
    assert isinstance(keyboard, ReplyKeyboardMarkup)  # Изменено на правильный тип
    # Add more specific assertions based on your keyboard structure

@pytest.mark.asyncio
async def test_add_review_keyboard():
    keyboard = await add_review_keyboard()
    assert isinstance(keyboard, InlineKeyboardMarkup)
    # Add more specific assertions based on your keyboard structure
