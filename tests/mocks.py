from typing import List, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

class MockService:
    def __init__(self, id: int, name: str, description: str, price: float, category_id: int):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.title = name  # Добавляем поле title, которое используется в клавиатурах

class MockSession:
    def __init__(self):
        self.services = [
            MockService(1, "Ремонт глушителя", "Описание", 1000.0, 1),
            MockService(2, "Замена катализатора", "Описание", 2000.0, 1),
        ]

    async def execute(self, *args, **kwargs):
        return self

    def scalars(self):
        return self

    async def first(self):
        return self.services[0] if self.services else None

    def all(self):
        return self.services

async def get_mock_session() -> AsyncGenerator[AsyncSession, None]:
    yield MockSession()
