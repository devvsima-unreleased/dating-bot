from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.bot_utils import send_profile
from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.base import dating_menu_kb, dating_profile_kb
from app.routers import dating_router
from database.models import UserModel


@dating_router.message(F.text == "💘", StateFilter(None))
async def _dating_menu(message: types.Message, state: FSMContext) -> None:
    await message.answer(umt.DATING_MENU, reply_markup=dating_menu_kb)


@dating_router.message(F.text == "👤", StateFilter(None))
async def profile_command(message: types.Message, user: UserModel) -> None:
    """Отправляет профиль пользователя"""
    await send_profile(message.from_user.id, user.profile)
    await message.answer(umt.DATING_PROFILE_MENU, reply_markup=dating_profile_kb)
