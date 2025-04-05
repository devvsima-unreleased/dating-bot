from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from utils.logging import logger

from ..models.service_profile import ServiceProfileModel


class Services:
    @staticmethod
    async def get_service_profile(session: AsyncSession, user_id: int):
        """Возвращает профиль сервиса пользователя"""
        return await session.get(ServiceProfileModel, user_id)

    @staticmethod
    async def delete_service_profile(session: AsyncSession, user_id: int):
        """Удаляет профиль сервиса пользователя"""
        stmt = delete(ServiceProfileModel).where(ServiceProfileModel.user_id == user_id)
        await session.execute(stmt)
        await session.commit()
        logger.log("DATABASE", f"{user_id}: удалил профиль сервиса")

    @staticmethod
    async def update_service_isactive(
        session: AsyncSession, service_profile: ServiceProfileModel, is_active: bool
    ) -> None:
        """Задает профилю сервиса статус, активный/не активный"""
        service_profile.is_active = is_active
        await session.commit()
        logger.log(
            "DATABASE",
            f"{service_profile.user_id}: поменял статус профиля сервиса на - {is_active}",
        )

    @staticmethod
    async def update_service_photo(
        session: AsyncSession, service_profile: ServiceProfileModel, photo: str
    ):
        """Изменяет фотографию профиля сервиса"""
        service_profile.photo = photo
        await session.commit()
        logger.log("DATABASE", f"{service_profile.user_id}: изменил фотографию профиля сервиса")

    @staticmethod
    async def update_service_description(
        session: AsyncSession, service_profile: ServiceProfileModel, description: str
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
        age: int,
        description: str,
        instagram: str | None,
    ):
        """Создает профиль сервиса пользователя, если профиль есть - удаляет его"""
        if await Services.get_service_profile(session, user_id):
            await Services.delete_service_profile(session, user_id)

        service_profile = ServiceProfileModel(
            user_id=user_id,
            name=name,
            location_id=location_id,
            photo=photo,
            age=age,
            description=description,
            instagram=instagram,
        )

        session.add(service_profile)
        await session.commit()
        logger.log("DATABASE", f"{user_id}: создал профиль сервиса")
        return service_profile
