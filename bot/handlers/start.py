from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from ..config import Settings
from ..database import Database
from ..keyboards import language_menu, main_menu
from ..locales import get_text
from .common import show_home


def create_router(database: Database, settings: Settings) -> Router:
    router = Router(name="start")

    @router.message(CommandStart())
    async def start(message: Message) -> None:
        database.ensure_user(message.from_user.id)
        await show_home(message, database, settings)

    @router.message(Command("language"))
    async def language_command(message: Message) -> None:
        language = database.get_language(message.from_user.id)
        await message.answer(get_text(language, "language"), reply_markup=language_menu())

    @router.callback_query(lambda query: query.data == "language")
    async def language_button(callback: CallbackQuery) -> None:
        language = database.get_language(callback.from_user.id)
        await callback.message.edit_text(get_text(language, "language"), reply_markup=language_menu())
        await callback.answer()

    @router.callback_query(lambda query: query.data and query.data.startswith("lang:"))
    async def language_selected(callback: CallbackQuery) -> None:
        language = callback.data.split(":", 1)[1]
        if language not in {"en", "ru", "pl", "uk", "de"}:
            await callback.answer("Unsupported language", show_alert=True)
            return
        database.set_language(callback.from_user.id, language)
        await callback.message.edit_text(get_text(language, "welcome"), reply_markup=main_menu(language, callback.from_user.id in settings.admin_ids))
        await callback.answer(get_text(language, "language_saved"))

    @router.message(Command("help"))
    async def help_command(message: Message) -> None:
        language = database.get_language(message.from_user.id)
        await message.answer(get_text(language, "help"))

    @router.callback_query(lambda query: query.data == "help")
    async def help_button(callback: CallbackQuery) -> None:
        language = database.get_language(callback.from_user.id)
        await callback.message.edit_text(get_text(language, "help"), reply_markup=main_menu(language, callback.from_user.id in settings.admin_ids))
        await callback.answer()

    return router