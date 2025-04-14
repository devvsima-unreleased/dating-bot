from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.bot_utils import menu, send_service_profile
from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.base import search_kb
from app.others.states import ServiceSearch
from app.routers import offers_router
from database.models import UserModel
from database.services.offer import Offers
from database.services.search import search_service_profiles

from ..common.cancel import cancel_command


@offers_router.message(F.text == "🔎", StateFilter(None))
async def _search_service_command(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Бот подбирает профили услуг, соответствующие предпочтениям пользователя, и предлагает их"""
    await message.answer(umt.SEARCH_SERVICES, reply_markup=search_kb)

    # Выполняем поиск профилей услуг
    service_list = await search_service_profiles(session, user)
    if service_list:
        await state.set_state(ServiceSearch.search)
        await state.update_data(ids=service_list)

        # Загружаем первый профиль услуги
        service_profile = await Offers.get(session, service_list[0])
        await send_service_profile(message.from_user.id, service_profile)
    else:
        await message.answer(umt.INVALID_SERVICE_SEARCH)
        await menu(message.from_user.id)


@offers_router.message(F.text.in_(("❤️", "👎")), StateFilter(ServiceSearch.search))
async def _search_service_profile(message: types.Message, state: FSMContext, session) -> None:
    """
    Пользователь может взаимодействовать с профилями услуг, предложенными ботом,
    ставя лайк или дизлайк.
    """
    data = await state.get_data()
    service_list = data.get("ids", [])
    current_service = await Offers.get(session, service_list[0])

    if message.text == "❤️":
        await message.answer("Вы добавили эту услугу в избранное!")
        # Здесь можно добавить логику для сохранения избранных услуг

    elif message.text == "👎":
        await message.answer("Вы пропустили эту услугу.")

    service_list.pop(0)
    if service_list:
        next_service = await Offers.get(session, service_list[0])
        await state.update_data(ids=service_list)
        await send_service_profile(message.from_user.id, next_service)
    else:
        await message.answer(umt.EMPTY_SERVICE_SEARCH)
        await cancel_command(message, state)
