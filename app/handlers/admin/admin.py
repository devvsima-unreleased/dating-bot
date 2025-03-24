from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.others.commands import set_admins_commands
from app.routers import admin_router


@admin_router.message(Command("admin"), StateFilter(None))
async def _admin_command(message: types.Message) -> None:
    """Админ панель"""
    await set_admins_commands(message.from_user.id)
    await message.answer("You are an administrator!")
