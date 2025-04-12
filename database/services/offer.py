from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from utils.logging import logger

from ..models.offer import OfferModel


class Offers:
    @staticmethod
    async def get_service_profile(session: AsyncSession, user_id: int):
        """Возвращает профиль сервиса пользователя"""
        return await session.get(OfferModel, user_id)

    @staticmethod
    async def delete_service_profile(session: AsyncSession, user_id: int):
        """Удаляет профиль сервиса пользователя"""
        stmt = delete(OfferModel).where(OfferModel.user_id == user_id)
        await session.execute(stmt)
        await session.commit()
        logger.log("DATABASE", f"{user_id}: удалил профиль сервиса")

    @staticmethod
    async def update_service_isactive(
        session: AsyncSession, service_profile: OfferModel, is_active: bool
    ) -> None:
        """Задает профилю сервиса статус, активный/не активный"""
        service_profile.is_active = is_active
        await session.commit()
        logger.log(
            "DATABASE",
            f"{service_profile.user_id}: поменял статус профиля сервиса на - {is_active}",
        )

    @staticmethod
    async def update_service_photo(session: AsyncSession, service_profile: OfferModel, photo: str):
        """Изменяет фотографию профиля сервиса"""
        service_profile.photo = photo
        await session.commit()
        logger.log("DATABASE", f"{service_profile.user_id}: изменил фотографию профиля сервиса")

    @staticmethod
    async def update_service_description(
        session: AsyncSession, service_profile: OfferModel, description: str
    ):
        """Изменяет описание профиля сервиса"""
        service_profile.description = description
        await session.commit()
        logger.log(
            "DATABASE",
            f"{service_profile.user_id}: изменил описание профиля сервиса на - {description}",
        )

    @staticmethod
    async def create_service_profile(
        session: AsyncSession,
        user_id: int,
        name: str,
        location_id: int | None,
        photo: str,
        description: str,
        instagram: str | None,
    ):
        """Создает профиль сервиса пользователя, если профиль есть - удаляет его"""
        if await Offers.get_service_profile(session, user_id):
            await Offers.delete_service_profile(session, user_id)

        service_profile = OfferModel(
            user_id=user_id,
            name=name,
            location_id=location_id,
            photo=photo,
            description=description,
            instagram=instagram,
        )

        session.add(service_profile)
        await session.commit()
        logger.log("DATABASE", f"{user_id}: создал профиль сервиса")
        return service_profile
