from aiogram import F, types
from aiogram.filters.state import StateFilter

from app.handlers.bot_utils import send_profile
from app.routers import services_router
from database.models import UserModel


@services_router.message(F.text == "👤", StateFilter(None))
async def _view_service_profile_command(message: types.Message, user: UserModel):
    """Отправляет профиль услуги пользователя"""
    if user.service_profile:
        await send_profile(message.from_user.id, user.service_profile)
    else:
        await message.reply("❌ У вас ещё нет профиля услуги. Создайте его, чтобы продолжить.")
