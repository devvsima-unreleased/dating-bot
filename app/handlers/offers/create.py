from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select

from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.create_profile import service_location_kb
from app.others.states import OfferCreate
from app.routers import offers_router
from database.models import UserModel
from database.models.location import LocationModel
from database.models.offer import OfferModel, OfferTypeModel


@offers_router.message(F.text == "Создать анкету для улсуг", StateFilter(None))
@offers_router.message(F.text == "🔃", StateFilter(None))
async def _create_offer_command(message: types.Message, state: FSMContext):
    """Запускает процесс создания анкеты услуги"""
    await message.answer(umt.PHOTO)
    await state.set_state(OfferCreate.photo)


@offers_router.message(StateFilter(OfferCreate.photo), F.photo)
async def _offer_photo(message: types.Message, state: FSMContext):
    """Сохраняет фото для анкеты услуги"""
    await state.update_data(photo=message.photo[0].file_id)
    await message.reply(umt.NAME)
    await state.set_state(OfferCreate.name)


@offers_router.message(StateFilter(OfferCreate.name), F.text)
async def _offer_name(message: types.Message, state: FSMContext):
    """Сохраняет имя для анкеты услуги"""
    await state.update_data(name=message.text)
    await message.reply(umt.AGE)
    await state.set_state(OfferCreate.age)


@offers_router.message(StateFilter(OfferCreate.age), F.text)
async def _offer_age(message: types.Message, state: FSMContext, session):
    """Сохраняет возраст для анкеты услуги"""
    await state.update_data(age=int(message.text))
    await message.reply(umt.CITY, reply_markup=await service_location_kb(session))
    await state.set_state(OfferCreate.location)


@offers_router.message(StateFilter(OfferCreate.location), F.text)
async def _offer_location(message: types.Message, state: FSMContext, session):
    """Сохраняет локацию для анкеты услуги"""
    result = await session.execute(select(LocationModel).where(LocationModel.name == message.text))
    location = result.scalar_one_or_none()

    if not location:
        await message.reply(umt.INVALID_CITY_RESPONSE)
        return

    await state.update_data(location_id=location.id)
    await message.reply(umt.SERVICE_TYPES)
    await state.set_state(OfferCreate.service_types)


@offers_router.message(StateFilter(OfferCreate.service_types), F.text)
async def _offer_service_types(message: types.Message, state: FSMContext, session):
    """Отправляет клавиатуру с типами услуг для выбора"""
    keyboard = await service_types_kb(session)
    await message.reply("Выберите типы услуг:", reply_markup=keyboard)


@offers_router.message(StateFilter(OfferCreate.description), F.text)
async def _offer_description(message: types.Message, state: FSMContext, user: UserModel, session):
    """Сохраняет описание и завершает создание анкеты услуги"""
    data = await state.get_data()

    # Получаем выбранные типы услуг из состояния
    selected_service_type_ids = data["service_types"]

    # Находим соответствующие объекты OfferTypeModel
    result = await session.execute(
        select(OfferTypeModel).where(OfferTypeModel.id.in_(selected_service_type_ids))
    )
    selected_service_types = result.scalars().all()

    # Создаем объект OfferModel
    offer = OfferModel(
        user_id=user.id,
        name=data["name"],
        location_id=data["location_id"],
        photo=data["photo"],
        description=message.text,
        offer_types=selected_service_types,  # Устанавливаем связь с типами услуг
    )
    session.add(offer)
    await session.commit()
    await state.clear()
    await message.reply("✅ Анкета услуги успешно создана!")


async def service_types_kb(session, selected_service_types=None) -> InlineKeyboardMarkup:
    """Создает клавиатуру с доступными типами услуг"""
    result = await session.execute(select(OfferTypeModel))
    service_types = result.scalars().all()

    # Создаем список списков кнопок
    keyboard_buttons = []
    selected_service_types = selected_service_types or []

    for service_type in service_types:
        text = (
            f"✅ {service_type.name}"
            if service_type.id in selected_service_types
            else service_type.name
        )
        button = InlineKeyboardButton(
            text=text, callback_data=f"toggle_service_type:{service_type.id}"
        )
        keyboard_buttons.append([button])  # Каждая кнопка в отдельной строке

    # Добавляем кнопку "Готово" в отдельную строку
    keyboard_buttons.append(
        [InlineKeyboardButton(text="Готово", callback_data="service_types_done")]
    )

    # Создаем клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard


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
    keyboard = await service_types_kb(session, selected_service_types)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@offers_router.callback_query(F.data == "service_types_done")
async def _service_types_done(callback: types.CallbackQuery, state: FSMContext):
    """Завершает выбор типов услуг"""
    await callback.message.reply("✅ Типы услуг успешно выбраны!")
    await state.set_state(OfferCreate.description)
    await callback.message.answer(umt.DESCRIPTION)
    await callback.answer()
