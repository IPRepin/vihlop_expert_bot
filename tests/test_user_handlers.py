import pytest
from unittest.mock import patch
from handlers.user_handlers.main_handlers import (
    get_stocks_list,
    get_repair_list,
    get_tuning_list,
    get_chip_tuning_list,
    add_review,
    back_to_main_keyboard
)
from tests.mocks import get_mock_session, MockService

mock_services = [
    MockService(1, "Ремонт глушителя", "Описание", 1000.0, 1),
    MockService(2, "Замена катализатора", "Описание", 2000.0, 1),
]

async def mock_get_services(*args, **kwargs):
    return mock_services

@pytest.mark.asyncio
async def test_get_stocks_list(message_mock):
    message_mock.text = "Акции"
    await get_stocks_list(message_mock)
    assert message_mock.answered
    assert message_mock.answer_text == "Выберите акцию"

@pytest.mark.asyncio
async def test_get_repair_list(message_mock):
    message_mock.text = "Ремонт"
    with patch('keyboards.user_keyboards.main_keyboards.get_session', return_value=get_mock_session()), \
         patch('keyboards.user_keyboards.main_keyboards.get_services', side_effect=mock_get_services):
        await get_repair_list(message_mock)
        assert message_mock.answered
        assert message_mock.answer_text == "Выберите услугу ремонта"
        assert message_mock.reply_markup is not None

@pytest.mark.asyncio
async def test_get_tuning_list(message_mock):
    message_mock.text = "Тюнинг"
    with patch('keyboards.user_keyboards.main_keyboards.get_session', return_value=get_mock_session()), \
         patch('keyboards.user_keyboards.main_keyboards.get_services', side_effect=mock_get_services):
        await get_tuning_list(message_mock)
        assert message_mock.answered
        assert message_mock.answer_text == "Выберите услугу тюнинга"
        assert message_mock.reply_markup is not None

@pytest.mark.asyncio
async def test_get_chip_tuning_list(message_mock):
    message_mock.text = "Чип"
    await get_chip_tuning_list(message_mock)
    assert message_mock.answered
    assert "Небольшое описание услуги" in message_mock.answer_text
    assert message_mock.reply_markup is not None

@pytest.mark.asyncio
async def test_add_review(message_mock):
    message_mock.text = "отзыв"
    await add_review(message_mock)
    assert message_mock.answered
    assert message_mock.answer_text == "Оставить отзыв"
    assert message_mock.reply_markup is not None

@pytest.mark.asyncio
async def test_back_to_main_keyboard(callback_query_mock, message_mock):
    callback_query_mock.data = "main_keyboard"
    callback_query_mock.message = message_mock
    await back_to_main_keyboard(callback_query_mock)
    assert message_mock.answered
    assert message_mock.answer_text == "Главное меню"
    assert message_mock.reply_markup is not None
