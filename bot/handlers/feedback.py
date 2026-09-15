import html
import logging

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..config import Settings
from ..database import Database
from ..keyboards import main_menu
from ..locales import get_text
from ..states import FeedbackState

logger = logging.getLogger(__name__)


def create_router(database: Database, settings: Settings) -> Router:
    router = Router(name="feedback")

    async def begin(
        message: Message, state: FSMContext, user_id: int | None = None
    ) -> None:
        language = database.get_language(user_id or message.from_user.id)
        await state.set_state(FeedbackState.waiting_for_message)
        await message.answer(
            f"{get_text(language, 'feedback_prompt')}\n\n{get_text(language, 'privacy')}"
        )

    @router.message(Command("feedback"))
    async def feedback_command(message: Message, state: FSMContext) -> None:
        await begin(message, state)

    @router.message(Command("cancel"))
    async def cancel_feedback(message: Message, state: FSMContext) -> None:
        language = database.get_language(message.from_user.id)
        await state.clear()
        await message.answer(
            get_text(language, "cancelled"),
            reply_markup=main_menu(
                language, message.from_user.id in settings.admin_ids
            ),
        )

    @router.callback_query(lambda query: query.data == "feedback")
    async def feedback_button(callback: CallbackQuery, state: FSMContext) -> None:
        await begin(callback.message, state, callback.from_user.id)
        await callback.answer()

    @router.message(FeedbackState.waiting_for_message, F.text)
    async def save_feedback(message: Message, state: FSMContext, bot: Bot) -> None:
        body = message.text.strip()
        language = database.get_language(message.from_user.id)
        if not body:
            await message.answer(get_text(language, "unsupported"))
            return
        if len(body) > 4000:
            await message.answer("Please keep your message under 4,000 characters.")
            return
        request_id = database.create_request(message.from_user.id, body)
        await state.clear()
        await message.answer(
            get_text(language, "feedback_saved", request_id=request_id),
            reply_markup=main_menu(
                language, message.from_user.id in settings.admin_ids
            ),
        )
        admin_text = f"<b>New feedback #{request_id}</b>\nFrom: <code>{message.from_user.id}</code>\n\n{html.escape(body)}"
        for admin_id in settings.admin_ids:
            try:
                await bot.send_message(admin_id, admin_text)
            except TelegramAPIError as error:
                logger.warning("Could not notify administrator %s: %s", admin_id, error)

    return router
