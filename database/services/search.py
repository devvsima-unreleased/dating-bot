import random

from loguru import logger
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import (
    AGE_RANGE,
    BLOCK_SIZE,
    INITIAL_DISTANCE,
    MAX_DISTANCE,
    MIN_PROFILES,
    RADIUS,
    RADIUS_STEP,
)
from database.models.offer import OfferModel
from database.models.profile import ProfileModel
from database.models.user import UserModel


async def search_profiles(
    session: AsyncSession,
    profile: ProfileModel,
) -> list:
    """
    Динамический поиск анкет: начинаем с малого радиуса и увеличиваем, пока не найдём достаточно анкет.
    """

    found_profiles = []
    current_distance = INITIAL_DISTANCE

    while current_distance <= MAX_DISTANCE and len(found_profiles) < MIN_PROFILES:
        # Расчёт расстояния
        distance_expr = (
            func.acos(
                func.greatest(
                    func.least(
                        func.cos(func.radians(profile.latitude))
                        * func.cos(func.radians(ProfileModel.latitude))
                        * func.cos(
                            func.radians(ProfileModel.longitude) - func.radians(profile.longitude)
                        )
                        + func.sin(func.radians(profile.latitude))
                        * func.sin(func.radians(ProfileModel.latitude)),
                        1.0,
                    ),
                    -1.0,
                )
            )
            * RADIUS
        )

        stmt = (
            select(ProfileModel.user_id, distance_expr.label("distance"))
            .where(
                and_(
                    ProfileModel.is_active == True,
                    distance_expr < current_distance,
                    or_(ProfileModel.gender == profile.find_gender, profile.find_gender == "all"),
                    or_(
                        profile.gender == ProfileModel.find_gender,
                        ProfileModel.find_gender == "all",
                    ),
                    ProfileModel.age.between(profile.age - AGE_RANGE, profile.age + AGE_RANGE),
                    ProfileModel.user_id != profile.user_id,
                )
            )
            .order_by(distance_expr)
        )

        result = await session.execute(stmt)
        found_profiles = result.fetchall()

        # Если анкет мало — увеличиваем радиус и пробуем снова
        current_distance += RADIUS_STEP

    # Разделение на блоки и перемешивание
    blocks = {}
    for user_id, dist in found_profiles:
        block_key = int(dist // BLOCK_SIZE)
        blocks.setdefault(block_key, []).append(user_id)

    for key in blocks:
        random.shuffle(blocks[key])

    id_list = [user_id for key in sorted(blocks.keys()) for user_id in blocks[key]]

    logger.log(
        "DATABASE",
        f"{profile.user_id} начал поиск анкет, результат: {id_list}, радиус: {current_distance - RADIUS_STEP} км",
    )
    return id_list


async def search_service_profiles(session: AsyncSession, user: UserModel) -> list[int]:
    """Ищет профили услуг, соответствующие предпочтениям пользователя"""
    result = await session.execute(
        select(OfferModel.user_id)
        .where(OfferModel.is_active == True)  # Только активные профили
        .where(OfferModel.user_id != user.id)  # Исключаем свои услуги
    )
    return [row[0] for row in result.fetchall()]
