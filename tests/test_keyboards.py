import pytest
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton
from keyboards.user_keyboards.main_keyboards import main_keyboard
from keyboards.user_keyboards.user_keyboards import (
    add_review_keyboard,
    repair_services_keyboard,
    chip_tuning_keyboard
)
from tests.mocks import get_mock_session, MockService
from unittest.mock import patch, AsyncMock

def get_keyboard_buttons(keyboard):
    """Helper function to extract button texts from keyboard"""
    if isinstance(keyboard, InlineKeyboardMarkup):
        return [button.text for row in keyboard.inline_keyboard for button in row]
    elif isinstance(keyboard, ReplyKeyboardMarkup):
        return [button.text for row in keyboard.keyboard for button in row]
    return []

async def mock_get_services(*args, **kwargs):
    category_id = kwargs.get('category_id')
    services = [
        MockService(1, "Удаление Катализатора", "Описание услуги 1", 1000.0, 1),
        MockService(2, "Удаление Сажевого фильтра", "Описание услуги 2", 2000.0, 1),
        MockService(3, "Универсальный глушитель (тихий, штатный звук)", "Описание услуги 3", 3000.0, 1),
    ]
    return [s for s in services if s.category_id == category_id]

@pytest.mark.asyncio
async def test_repair_services_keyboard():
    with patch('keyboards.user_keyboards.user_keyboards.get_session', return_value=get_mock_session()), \
         patch('keyboards.user_keyboards.user_keyboards.get_services', side_effect=mock_get_services):
        keyboard = await repair_services_keyboard(category_id=1)
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) > 0
        
        buttons_text = get_keyboard_buttons(keyboard)
        assert "Удаление Катализатора" in buttons_text
        assert "Удаление Сажевого фильтра" in buttons_text
        assert "На главное меню" in buttons_text

@pytest.mark.asyncio
async def test_chip_tuning_keyboard():
    keyboard = await chip_tuning_keyboard()
    assert isinstance(keyboard, InlineKeyboardMarkup)
    assert len(keyboard.inline_keyboard) > 0
    
    buttons_text = get_keyboard_buttons(keyboard)
    assert "📲Связаться через телеграм" in buttons_text
    assert "На главное меню" in buttons_text

@pytest.mark.asyncio
async def test_main_keyboard():
    keyboard = await main_keyboard()
    assert isinstance(keyboard, ReplyKeyboardMarkup)
    assert len(keyboard.keyboard) > 0
    
    buttons_text = get_keyboard_buttons(keyboard)
    assert "Акции и скидки" in buttons_text
    assert "Оставить отзыв" in buttons_text
    assert "Ремонт глушителя" in buttons_text
    assert "Тюнинг выхлопной системы" in buttons_text
    assert "Чип тюнинг двигателя" in buttons_text

@pytest.mark.asyncio
async def test_add_review_keyboard():
    keyboard = await add_review_keyboard()
    assert isinstance(keyboard, InlineKeyboardMarkup)
    assert len(keyboard.inline_keyboard) > 0
    
    buttons_text = get_keyboard_buttons(keyboard)
    assert "💬Оставить отзыв на Яндекс Картах" in buttons_text
    assert "💬Оставить отзыв ВКонтакте" in buttons_text
    assert "💬Оставить отзыв на АВИТО" in buttons_text
    assert "На главное меню" in buttons_text
