from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from app.handlers.message_text import user_message_text as umt
from app.handlers.offers.menu import offer_menu
from app.keyboards.default.create_offer_profile import service_location_kb
from app.keyboards.inline.offer import offer_types_ikb
from app.others.states import OfferCreate
from app.routers import offers_router
from database.models import UserModel
from database.models.offer import OfferTypeModel
from database.services.location import Location
from database.services.offer import Offers


@offers_router.message(F.text == "Создать анкету для улсуг", StateFilter(None))
@offers_router.message(F.text == "🔃", StateFilter(None))
async def _create_offer_command(message: types.Message, state: FSMContext):
    """Запускает процесс создания анкеты услуги"""
    await message.answer(umt.PHOTO)
    await state.set_state(OfferCreate.photo)


# < photo >
@offers_router.message(StateFilter(OfferCreate.photo), F.photo)
async def _offer_photo(message: types.Message, state: FSMContext):
    """Сохраняет фото для анкеты услуги"""
    await state.update_data(photo=message.photo[0].file_id)
    await message.reply(umt.NAME)
    await state.set_state(OfferCreate.name)


# < name >
@offers_router.message(StateFilter(OfferCreate.name), F.text)
async def _offer_name(message: types.Message, state: FSMContext, session):
    """Сохраняет имя для анкеты услуги"""
    await state.update_data(name=message.text)
    await message.reply(umt.CITY, reply_markup=await service_location_kb(session))
    await state.set_state(OfferCreate.location)


# < location >
@offers_router.message(StateFilter(OfferCreate.location), F.text)
async def _offer_location(message: types.Message, state: FSMContext, session):
    """Сохраняет локацию для анкеты услуги"""

    if location := await Location.is_this_location(session, message.text):
        await state.update_data(location_id=location.id)
        keyboard = await offer_types_ikb(session)

        await message.reply(umt.SERVICE_TYPES, reply_markup=keyboard)
        await state.set_state(OfferCreate.service_types)
    else:
        await message.reply(umt.INVALID_CITY_RESPONSE)


# < service_types >
@offers_router.callback_query(F.data.startswith("toggle_service_type:"))
async def _toggle_service_type(callback: types.CallbackQuery, state: FSMContext, session):
    """Переключает выбор типа услуги"""
    service_type_id = int(callback.data.split(":")[1])

    # Получаем текущие выбранные типы услуг из состояния
    data = await state.get_data()
    selected_service_types = data.get("service_types", [])

    # Добавляем или удаляем тип услуги из списка
    if service_type_id in selected_service_types:
        selected_service_types.remove(service_type_id)
    else:
        selected_service_types.append(service_type_id)

    # Обновляем состояние
    await state.update_data(service_types=selected_service_types)

    # Обновляем клавиатуру
    keyboard = await offer_types_ikb(session, selected_service_types)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@offers_router.callback_query(F.data == "service_types_done")
async def _service_types_done(callback: types.CallbackQuery, state: FSMContext):
    """Завершает выбор типов услуг"""
    await callback.message.reply("✅ Типы услуг успешно выбраны!")
    await state.set_state(OfferCreate.description)
    await callback.message.answer(umt.DESCRIPTION)
    await callback.answer()


# < description >
@offers_router.message(StateFilter(OfferCreate.description), F.text)
async def _offer_description(message: types.Message, state: FSMContext, user: UserModel, session):
    """Сохраняет описание и завершает создание анкеты услуги"""
    data = await state.get_data()

    # Находим соответствующие объекты OfferTypeModel
    result = await session.execute(
        select(OfferTypeModel).where(OfferTypeModel.id.in_(data["service_types"]))
    )
    selected_service_types = result.scalars().all()

    await Offers.create_service_profile(
        session=session,
        user_id=user.id,
        name=data["name"],
        location_id=data["location_id"],
        photo=data["photo"],
        description=message.text,
        offer_types=selected_service_types,
    )

    await state.clear()
    await offer_menu(message)
