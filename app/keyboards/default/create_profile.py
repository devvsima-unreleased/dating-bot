from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlalchemy import select

from database.models.profile import ProfileModel
from loader import _


def start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("Создать анкету для знакомств")),
                KeyboardButton(text=_("Создать анкету для улсуг")),
            ],
        ],
    )
    return kb


def gender_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text=_("Парень")), KeyboardButton(text=_("Девушка"))],
        ],
    )
    return kb


def find_gender_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("Парней")),
                KeyboardButton(text=_("Девушек")),
                KeyboardButton(text=_("Всех")),
            ],
        ],
    )
    return kb


def location_kb(profile: ProfileModel | None):
    builder = ReplyKeyboardBuilder()
    if profile and profile.city != "📍":
        builder.button(text=_("Оставить предыдущее"))
    builder.button(
        text=_("📍 Отправить местоположение"),
        request_location=True,
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.location import LocationModel


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
