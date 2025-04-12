from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.location import LocationModel
from loader import _


async def service_location_kb(session: AsyncSession) -> ReplyKeyboardMarkup:
    """Создает клавиатуру с доступными локациями"""
    # Выполняем асинхронный запрос для получения списка локаций
    result = await session.execute(select(LocationModel.name).order_by(LocationModel.name))
    location_names = [row[0] for row in result.fetchall()]

    # Создаем кнопки для каждой локации
    buttons = [
        [KeyboardButton(text=location)] for location in location_names
    ]  # Список списков кнопок

    # Создаем клавиатуру
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return keyboard
