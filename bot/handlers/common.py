from aiogram.types import Message

from ..config import Settings
from ..database import Database
from ..keyboards import main_menu
from ..locales import get_text


async def show_home(message: Message, database: Database, settings: Settings) -> None:
    language = database.get_language(message.from_user.id)
    await message.answer(
        get_text(language, "welcome"),
        reply_markup=main_menu(language, message.from_user.id in settings.admin_ids),
    )
