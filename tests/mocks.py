from typing import List, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

class MockService:
    def __init__(self, id: int, name: str, description: str, price: float, category_id: int, image: str = "test_image.jpg"):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.title = name  # Добавляем поле title, которое используется в клавиатурах
        self.image = image  # Добавляем поле image для тестирования отправки фото
        self.__tablename__ = 'services'

class MockApplication:
    def __init__(self, id: int, user_name: str, phone: str, viewed: bool = False):
        self.id = id
        self.user_name = user_name
        self.phone = phone
        self.viewed = viewed
        self.__tablename__ = 'applications'

class MockSession:
    def __init__(self):
        self.applications = []
        self.services = [
            MockService(1, "Ремонт глушителя", "Описание услуги 1", 1000.0, 1, "test_image_1.jpg"),
            MockService(2, "Замена катализатора", "Описание услуги 2", 2000.0, 1, "test_image_2.jpg"),
        ]
        self._query = None
        self._is_closed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._is_closed:
            self._is_closed = True
            return self
        raise StopAsyncIteration
        
    async def execute(self, query):
        self._query = query
        return self

    async def scalar(self, query=None):
        if query:
            self._query = query
        if hasattr(self._query, '_where_criteria'):
            for criterion in self._query._where_criteria:
                if 'phone' in str(criterion.left):
                    phone = criterion.right.value
                    return next((app for app in self.applications if app.phone == phone), None)
        return None

    async def scalars(self, query=None):
        if query:
            self._query = query
        return self

    def all(self):
        if hasattr(self._query, '_where_criteria'):
            for criterion in self._query._where_criteria:
                if 'category_id' in str(criterion.left):
                    category_id = criterion.right.value
                    return [s for s in self.services if s.category_id == category_id]
        return self.services

    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def close(self):
        self._is_closed = True

    def is_closed(self):
        return self._is_closed

    def add(self, obj):
        if obj.__tablename__ == 'applications':
            self.applications.append(obj)
        elif obj.__tablename__ == 'services':
            self.services.append(obj)

class MockState:
    def __init__(self):
        self.state = None
        self.data = {}

    async def set_state(self, state):
        self.state = state

    async def get_state(self):
        return self.state

    async def set_data(self, data):
        self.data = data

    async def get_data(self):
        return self.data

    async def clear(self):
        self.state = None
        self.data = {}

async def get_mock_session() -> AsyncGenerator[MockSession, None]:
    session = MockSession()
    try:
        yield session
    finally:
        await session.close()
