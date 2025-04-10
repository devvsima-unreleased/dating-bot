from aiogram import F, types
from aiogram.filters.state import StateFilter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.handlers.bot_utils import send_service_profile
from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.base import offer_menu_kb, offer_profile_kb
from app.routers import offers_router
from database.models import UserModel


@offers_router.message(F.text == "💼", StateFilter(None))
async def _offer_menu(message: types.Message) -> None:
    await message.answer(umt.OFFER_MENU, reply_markup=offer_menu_kb)


@offers_router.message(F.text == "💰", StateFilter(None))
async def _view_service_profile_command(
    message: types.Message, session: AsyncSession, user: UserModel
):
    """Отправляет профиль услуги пользователя"""
    # Выполняем запрос для получения пользователя с профилем услуги
    result = await session.execute(
        select(UserModel)
        .options(joinedload(UserModel.offer))  # Загружаем профиль
        .where(UserModel.id == user.id)
    )
    user_with_profile = result.scalar_one_or_none()

    if user_with_profile and user_with_profile.offer:
        await send_service_profile(message.from_user.id, user_with_profile.offer)
        await message.answer(umt.OFFER_PROFILE_MENU, reply_markup=offer_profile_kb)
    else:
        await message.reply("❌ У вас ещё нет профиля услуги. Создайте его, чтобы продолжить.")
