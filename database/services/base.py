from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Mapped


class BaseService:
    def __init__(self, model: Mapped):
        self.model = model

    async def create(self, session: AsyncSession, **kwargs):
        """Создаёт новую запись в таблице."""
        instance = self.model(**kwargs)
        session.add(instance)
        await session.commit()
        return instance

    async def get_by_id(self, session: AsyncSession, id: int):
        """Получает запись по ID."""
        result = await session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def update(self, session: AsyncSession, id: int, **kwargs):
        """Обновляет запись по ID."""
        instance = await self.get_by_id(session, id)
        if not instance:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await session.commit()
        return instance

    async def delete(self, session: AsyncSession, id: int):
        """Удаляет запись по ID."""
        instance = await self.get_by_id(session, id)
        if instance:
            await session.delete(instance)
            await session.commit()
        return instance


# exemple
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.profile import ProfileModel
from .base import BaseService


class ProfileService(BaseService):
    def __init__(self):
        super().__init__(ProfileModel)

    async def search_profiles(self, session: AsyncSession, **filters):
        """Пример дополнительного метода для поиска профилей."""
        query = select(self.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()
