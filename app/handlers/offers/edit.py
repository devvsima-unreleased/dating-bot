from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.message_text import user_message_text as umt
from app.handlers.offers.menu import _view_service_profile_command
from app.others.states import OfferEdit
from app.routers import offers_router
from database.models import UserModel
from database.services.offer import Offers


@offers_router.message(F.text == "📸", StateFilter(None))
async def _edit_service_photo_command(message: types.Message, state: FSMContext) -> None:
    """Редактирует фотографию профиля услуги"""
    await state.set_state(OfferEdit.photo)
    await message.reply(umt.PHOTO)


@offers_router.message(StateFilter(OfferEdit.photo), F.photo)
async def _update_service_photo(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Обновляет фотографию профиля услуги"""
    await Offers.update_service_photo(session, user.offer, message.photo[0].file_id)
    await state.clear()
    await message.reply("✅ Фотография профиля услуги обновлена!")
    await _view_service_profile_command(message, user)


@offers_router.message(F.text == "📝", StateFilter(None))
async def _edit_service_description_command(message: types.Message, state: FSMContext) -> None:
    """Редактирует описание профиля услуги"""
    await state.set_state(OfferEdit.description)
    await message.reply(umt.DESCRIPTION)


@offers_router.message(StateFilter(OfferEdit.description), F.text)
async def _update_service_description(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Обновляет описание профиля услуги"""
    await Offers.update_service_description(session, user.offer, message.text)
    await state.clear()
    await message.reply("✅ Описание профиля услуги обновлено!")
    await _view_service_profile_command(message, user)


@offers_router.message(F.text == "🔴", StateFilter(None))
async def _disable_service_profile_command(
    message: types.Message, user: UserModel, session
) -> None:
    """Отключает профиль услуги, делая его неактивным"""
    await Offers.update_service_isactive(session, user.offer, False)
    await message.answer("❌ Профиль услуги отключен!")
