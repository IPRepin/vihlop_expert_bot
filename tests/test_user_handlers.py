import pytest
from unittest.mock import patch, AsyncMock
from handlers.user_handlers.main_handlers import (
    get_stocks_list,
    get_repair_list,
    get_tuning_list,
    get_chip_tuning_list,
    add_review,
    back_to_main_keyboard,
    view_service
)
from tests.mocks import get_mock_session, MockService

mock_services = [
    MockService(1, "Ремонт глушителя", "Описание услуги 1", 1000.0, 1, "test_image_1.jpg"),
    MockService(2, "Замена катализатора", "Описание услуги 2", 2000.0, 1, "test_image_2.jpg"),
]

async def mock_get_services(*args, **kwargs):
    return mock_services

async def mock_get_service(*args, **kwargs):
    service_id = kwargs.get('id')
    return next((service for service in mock_services if service.id == service_id), None)

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

@pytest.mark.asyncio
async def test_view_service_success(callback_query_mock, message_mock):
    # Подготовка тестовых данных
    callback_query_mock.data = "service_1"
    callback_query_mock.message = message_mock
    message_mock.photo_sent = False
    message_mock.photo_data = None
    message_mock.caption = None

    # Добавляем метод answer_photo в message_mock
    async def answer_photo(photo, caption):
        message_mock.photo_sent = True
        message_mock.photo_data = photo
        message_mock.caption = caption
        return message_mock

    message_mock.answer_photo = answer_photo

    # Выполнение теста
    with patch('handlers.user_handlers.main_handlers.get_session', return_value=get_mock_session()), \
         patch('handlers.user_handlers.main_handlers.get_service', side_effect=mock_get_service):
        await view_service(callback_query_mock)
        
        # Проверка результатов
        assert message_mock.photo_sent
        assert message_mock.photo_data == "test_image_1.jpg"
        assert "Ремонт глушителя" in message_mock.caption
        assert "Описание услуги 1" in message_mock.caption
        assert "1000.0" in message_mock.caption

@pytest.mark.asyncio
async def test_view_service_not_found(callback_query_mock, message_mock):
    # Подготовка тестовых данных
    callback_query_mock.data = "service_999"  # Несуществующий ID
    callback_query_mock.message = message_mock
    callback_query_mock.answered = False

    async def answer():
        callback_query_mock.answered = True

    callback_query_mock.answer = answer

    # Выполнение теста
    with patch('handlers.user_handlers.main_handlers.get_session', return_value=get_mock_session()), \
         patch('handlers.user_handlers.main_handlers.get_service', side_effect=mock_get_service):
        await view_service(callback_query_mock)
        
        # Проверка результатов
        assert message_mock.answered
        assert message_mock.answer_text == "Услуга не найдена."
        assert callback_query_mock.answered

@pytest.mark.asyncio
async def test_view_service_error(callback_query_mock, message_mock):
    # Подготовка тестовых данных
    callback_query_mock.data = "service_1"
    callback_query_mock.message = message_mock

    # Создаем функцию, которая будет вызывать ошибку
    async def answer_photo(*args, **kwargs):
        raise Exception("Test error")

    message_mock.answer_photo = answer_photo

    # Выполнение теста
    with patch('handlers.user_handlers.main_handlers.get_session', return_value=get_mock_session()), \
         patch('handlers.user_handlers.main_handlers.get_service', side_effect=mock_get_service):
        await view_service(callback_query_mock)
        
        # Проверка результатов
        assert message_mock.answered
        assert message_mock.answer_text == "Ошибка при отправке данных."
