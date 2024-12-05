from typing import List, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

class MockService:
    def __init__(self, id: int, name: str, description: str, price: float, category_id: int, image: str = None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.title = name  # Добавляем поле title, которое используется в клавиатурах
        self.image = image  # Добавляем поле image для тестирования отправки фото

class MockSession:
    def __init__(self):
        self.services = [
            MockService(1, "Ремонт глушителя", "Описание услуги 1", 1000.0, 1, "test_image_1.jpg"),
            MockService(2, "Замена катализатора", "Описание услуги 2", 2000.0, 1, "test_image_2.jpg"),
        ]

    async def execute(self, *args, **kwargs):
        return self

    def scalars(self):
        return self

    async def first(self):
        return self.services[0] if self.services else None

    def all(self):
        return self.services

    def get_service_by_id(self, service_id: int):
        return next((service for service in self.services if service.id == service_id), None)

async def get_mock_session() -> AsyncGenerator[AsyncSession, None]:
    yield MockSession()
