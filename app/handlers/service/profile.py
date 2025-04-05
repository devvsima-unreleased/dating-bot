from aiogram import F, types
from aiogram.filters.state import StateFilter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.handlers.bot_utils import send_service_profile
from app.routers import services_router
from database.models import UserModel
from database.services.services import Services


@services_router.message(F.text == "👤💰", StateFilter(None))
async def _view_service_profile_command(
    message: types.Message, session: AsyncSession, user: UserModel
):
    """Отправляет профиль услуги пользователя"""
    # Выполняем запрос для получения пользователя с профилем услуги
    result = await session.execute(
        select(UserModel)
        .options(joinedload(UserModel.service_profile))  # Загружаем профиль услуги
        .where(UserModel.id == user.id)
    )
    user_with_profile = result.scalar_one_or_none()

    if user_with_profile and user_with_profile.service_profile:
        await send_service_profile(message.from_user.id, user_with_profile.service_profile)
    else:
        await message.reply("❌ У вас ещё нет профиля услуги. Создайте его, чтобы продолжить.")
