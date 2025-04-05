from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database.models.profile import ProfileModel
from loader import _


def start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("Создать анкету")),
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
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.location import LocationModel


async def service_location_kb(session: AsyncSession) -> ReplyKeyboardMarkup:
    """Создает клавиатуру с доступными локациями"""
    # Получаем список локаций из базы данных
    locations = await session.execute(
        session.query(LocationModel.name).order_by(LocationModel.name)
    )
    location_names = [row[0] for row in locations.fetchall()]

    # Создаем кнопки для каждой локации
    buttons = [KeyboardButton(text=location) for location in location_names]

    # Создаем клавиатуру
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    return keyboard
