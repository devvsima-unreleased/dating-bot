from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from database.services import User


class OfferMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable, message: Message | CallbackQuery, data: dict
    ) -> Any:
        session = data["session"]
        user, is_create = await User.get_or_create_offer(
            session,
            user_id=message.from_user.id,
            username=message.from_user.username,
            language=message.from_user.language_code,
        )
        if not user.is_banned:
            if user.offer:
                if not user.offer.is_active:
                    return
            data["user"] = user
            return await handler(message, data)
        return
