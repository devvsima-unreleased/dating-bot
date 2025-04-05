from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.create_profile import service_location_kb
from app.others.states import ServiceProfileCreate
from app.routers import services_router
from database.models import UserModel
from database.models.location import LocationModel
from database.services.services import Services


@services_router.message(F.text == "🔄💰", StateFilter(None))
async def _create_service_profile_command(message: types.Message, state: FSMContext):
    """Запускает процесс создания профиля услуги"""
    await message.answer(umt.PHOTO)
    await state.set_state(ServiceProfileCreate.photo)


@services_router.message(StateFilter(ServiceProfileCreate.photo), F.photo)
async def _service_photo(message: types.Message, state: FSMContext):
    """Сохраняет фото для профиля услуги"""
    await state.update_data(photo=message.photo[0].file_id)
    await message.reply(umt.NAME)
    await state.set_state(ServiceProfileCreate.name)


@services_router.message(StateFilter(ServiceProfileCreate.name), F.text)
async def _service_name(message: types.Message, state: FSMContext):
    """Сохраняет имя для профиля услуги"""
    await state.update_data(name=message.text)
    await message.reply(umt.AGE)
    await state.set_state(ServiceProfileCreate.age)


@services_router.message(StateFilter(ServiceProfileCreate.age), F.text)
async def _service_age(message: types.Message, state: FSMContext):
    """Сохраняет возраст для профиля услуги"""
    await state.update_data(age=int(message.text))
    await message.reply(umt.CITY, reply_markup=service_location_kb())
    await state.set_state(ServiceProfileCreate.location)


@services_router.message(StateFilter(ServiceProfileCreate.location), F.text)
async def _service_location(message: types.Message, state: FSMContext, session):
    """Сохраняет локацию для профиля услуги"""
    location = await session.get(LocationModel, message.text)
    if not location:
        await message.reply(umt.INVALID_CITY_RESPONSE)
        return

    await state.update_data(location_id=location.id)
    await message.reply(umt.DESCRIPTION)
    await state.set_state(ServiceProfileCreate.description)


@services_router.message(StateFilter(ServiceProfileCreate.description), F.text)
async def _service_description(message: types.Message, state: FSMContext, user: UserModel, session):
    """Сохраняет описание и завершает создание профиля услуги"""
    data = await state.get_data()
    await Services.create_service_profile(
        session=session,
        user_id=user.id,
        name=data["name"],
        location_id=data["location_id"],
        photo=data["photo"],
        age=data["age"],
        description=message.text,
        instagram=None,  # Можно добавить ввод Instagram, если нужно
    )
    await state.clear()
    await message.reply("✅ Профиль услуги успешно создан!")
