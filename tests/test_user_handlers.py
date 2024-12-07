import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from handlers.user_handlers.main_handlers import (
    get_service_list,
    get_chip_tuning_list,
    add_review,
    back_to_main_keyboard
)
from handlers.user_handlers.service_handlers import view_service
from tests.mocks import get_mock_session, MockService
from data.services_requests import get_services, get_service

mock_services = {
    1: [  # Услуги ремонта
        MockService(1, "Удаление Катализатора", "Описание услуги 1", 1000.0, 1, "test_image_1.jpg"),
        MockService(2, "Удаление Сажевого фильтра", "Описание услуги 2", 2000.0, 1, "test_image_2.jpg"),
    ],
    2: [  # Услуги тюнинга
        MockService(3, "Тюнинг выхлопной системы", "Описание услуги 3", 3000.0, 2, "test_image_3.jpg"),
        MockService(4, "Спортивный выхлоп", "Описание услуги 4", 4000.0, 2, "test_image_4.jpg"),
    ]
}

async def mock_get_services(session, **kwargs):
    category_id = kwargs.get('category_id')
    return mock_services.get(category_id, [])

@pytest.mark.asyncio
async def test_get_service_list_repair(message_mock):
    message_mock.text = "Ремонт"
    with patch('data.db_connect.get_session', side_effect=get_mock_session), \
         patch('data.services_requests.get_services', side_effect=mock_get_services):
        await get_service_list(message_mock)
        assert message_mock.answered
        assert message_mock.answer_text == "Выберите услугу ремонта"
        assert message_mock.reply_markup is not None

@pytest.mark.asyncio
async def test_get_service_list_tuning(message_mock):
    message_mock.text = "Тюнинг"
    with patch('data.db_connect.get_session', side_effect=get_mock_session), \
         patch('data.services_requests.get_services', side_effect=mock_get_services):
        await get_service_list(message_mock)
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


@pytest.mark.asyncio
async def test_view_service_not_found(callback_query_mock, message_mock):
    callback_query_mock.data = "service_999"
    callback_query_mock.message = message_mock
    callback_query_mock.answered = False

    async def answer():
        callback_query_mock.answered = True

    callback_query_mock.answer = answer

    with patch('data.db_connect.get_session', side_effect=get_mock_session), \
         patch('data.services_requests.get_service', return_value=None):
        await view_service(callback_query_mock)
        
        assert message_mock.answered
        assert message_mock.answer_text == "Услуга не найдена."
        assert callback_query_mock.answered
