from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from app.filters.kb_filter import LangCallback
from database.models.offer import OfferTypeModel
from loader import i18n


async def offer_types_ikb(session, selected_service_types=None) -> InlineKeyboardMarkup:
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
