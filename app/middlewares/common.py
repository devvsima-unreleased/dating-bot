from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from app.handlers.bot_utils import new_user_alert_to_group
from database.services import User
from database.services.profile import Profile
from utils.base62 import decode_base62


class CommonMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable, message: Message | CallbackQuery, data: dict
    ) -> Any:
        session = data["session"]
        user, is_create = await User.get_or_create_dating(
            session,
            user_id=message.from_user.id,
            username=message.from_user.username,
            language=message.from_user.language_code,
        )
        if user.is_banned:
            return

        data["user"] = user
        if isinstance(message, Message):
            if is_create and (inviter_code := getattr(data.get("command"), "args", None)):
                await new_user_alert_to_group(user)
                if inviter := await User.get(session, decode_base62(inviter_code)):
                    await User.increment_referral_count(session, inviter)

            if user.profile and not user.profile.is_active:
                await Profile.update_isactive(session, user.profile, True)

        return await handler(message, data)
