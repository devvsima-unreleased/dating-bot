from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.message_text import user_message_text as umt
from app.others.states import ServiceProfileEdit
from app.routers import services_router
from database.models import UserModel
from database.services.services import Services


@services_router.message(F.text == "🖼💰", StateFilter(None))
async def _edit_service_photo_command(message: types.Message, state: FSMContext):
    """Редактирует фотографию профиля услуги"""
    await state.set_state(ServiceProfileEdit.photo)
    await message.reply(umt.PHOTO)


@services_router.message(StateFilter(ServiceProfileEdit.photo), F.photo)
async def _update_service_photo(
    message: types.Message, state: FSMContext, user: UserModel, session
):
    """Обновляет фотографию профиля услуги"""
    await Services.update_service_photo(session, user.service_profile, message.photo[0].file_id)
    await state.clear()
    await message.reply("✅ Фотография профиля услуги обновлена!")


@services_router.message(F.text == "✍️💰", StateFilter(None))
async def _edit_service_description_command(message: types.Message, state: FSMContext):
    """Редактирует описание профиля услуги"""
    await state.set_state(ServiceProfileEdit.description)
    await message.reply(umt.DESCRIPTION)


@services_router.message(StateFilter(ServiceProfileEdit.description), F.text)
async def _update_service_description(
    message: types.Message, state: FSMContext, user: UserModel, session
):
    """Обновляет описание профиля услуги"""
    await Services.update_service_description(session, user.service_profile, message.text)
    await state.clear()
    await message.reply("✅ Описание профиля услуги обновлено!")
