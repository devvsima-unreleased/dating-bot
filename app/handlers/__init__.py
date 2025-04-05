from aiogram import Dispatcher
from aiogram.types import ErrorEvent

from utils.logging import logger

from .admin import admin_router
from .common import common_router
from .dating import dating_router
from .other import voide_router
from .service import services_router


def setup_handlers(dp: Dispatcher) -> None:
    async def _error(event: ErrorEvent):
        logger.exception(event.exception)

    dp.errors.register(_error)

    dp.include_routers(common_router, dating_router, services_router, admin_router, voide_router)
