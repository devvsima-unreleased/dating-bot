from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.location import LocationModel

from ..models.match import MatchModel


class Location:
    @staticmethod
    async def get_all(session: AsyncSession, user_id: int) -> list:
        """Возвращает список пользователей, которые лайкнули анкету"""
        result = await session.execute(
            select(MatchModel.sender_id).where(MatchModel.receiver_id == user_id)
        )

        return [row[0] for row in result.fetchall()]

    @staticmethod
    async def is_this_location(session: AsyncSession, location: str) -> list:
        """Возвращает список пользователей, которые лайкнули анкету"""
        result = await session.execute(select(LocationModel).where(LocationModel.name == location))
        location = result.scalar_one_or_none()
        return location
