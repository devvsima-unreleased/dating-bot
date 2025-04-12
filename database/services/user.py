from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models.offer import OfferModel
from utils.logging import logger

from ..models.user import UserModel
from .profile import Profile


class User:
    @staticmethod
    async def get(session: AsyncSession, user_id: int) -> UserModel | None:
        """Возвращает пользователя по его id"""
        return await session.get(UserModel, user_id)

    async def get_all(session: AsyncSession) -> list[UserModel]:
        """Возвращает список всех пользователей"""
        result = await session.execute(select(UserModel))
        return result.scalars().all()

    @staticmethod
    async def get_with_dating_profile(session: AsyncSession, user_id: int):
        """Возвращает пользователя и его профиль"""
        result = await session.execute(
            select(UserModel).options(joinedload(UserModel.profile)).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_with_offer_profile(session: AsyncSession, user_id: int):
        """Возвращает пользователя и его профиль"""
        result = await session.execute(
            select(UserModel)
            .options(
                joinedload(UserModel.offer).joinedload(OfferModel.location)
            )  # Загружаем профиль и локацию
            .where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def set_user_ban_and_profile_status(session, user_id: int, is_banned: bool):
        user = await User.get_with_dating_profile(session, user_id)
        await User.update_isbanned(session, user, is_banned)
        await Profile.update_isactive(session, user.profile, not is_banned)

    @staticmethod
    async def get_or_create_dating(
        session: AsyncSession, user_id: int, username: str = None, language: str = None
    ) -> UserModel:
        if user := await User.get_with_dating_profile(session, user_id):
            return user, False
        await User.create(session, user_id=user_id, username=username, language=language)
        user = await User.get_with_dating_profile(session, user_id)
        return user, True

    @staticmethod
    async def get_or_create_offer(
        session: AsyncSession, user_id: int, username: str = None, language: str = None
    ) -> UserModel:
        if user := await User.get_with_offer_profile(session, user_id):
            return user, False
        await User.create(session, user_id=user_id, username=username, language=language)
        user = await User.get_with_offer_profile(session, user_id)
        return user, True

    @staticmethod
    async def create(
        session: AsyncSession, user_id: int, username: str = None, language: str = None
    ) -> UserModel:
        """Создает нового пользователя"""
        logger.log("DATABASE", f"New user: {user_id} (@{username}) {language}")
        session.add(UserModel(id=user_id, username=username, language=language))
        await session.commit()

    @staticmethod
    async def update_username(session: AsyncSession, user: UserModel, username: str = None) -> None:
        """Обновляет данные пользователя"""
        user.username = username
        await session.commit()
        logger.log("DATABASE", f"{user.id} ({user.username}): обновленно имя на - {username}")

    @staticmethod
    async def increment_referral_count(
        session: AsyncSession, user: UserModel, num: int = 1
    ) -> None:
        """Добавляет приведенного реферала к пользователю {inviter_id}"""
        user.referral += num
        await session.commit()
        logger.log("DATABASE", f"{user.id} (@{user.username}): привел нового пользователя")

    @staticmethod
    async def update_language(session: AsyncSession, user: UserModel, language: str) -> None:
        """Изменяет язык пользователя на {language}"""
        user.language = language
        await session.commit()
        logger.log("DATABASE", f"{user.id} (@{user.username}): изменил язык на - {language}")

    @staticmethod
    async def update_isbanned(session: AsyncSession, user: UserModel, is_banned: bool) -> None:
        """Меняет статус блокировки пользователя на {is_banned}"""
        user.is_banned = is_banned
        await session.commit()
        logger.log(
            "DATABASE", f"{user.id} (@{user.username}): статус блокировки изменен на - {is_banned}"
        )
