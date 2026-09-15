import html

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from ..config import Settings
from ..database import Database
from ..keyboards import history_menu
from ..locales import get_text


def create_router(database: Database, settings: Settings) -> Router:
    router = Router(name="history")

    async def show_history(target: Message | CallbackQuery) -> None:
        user_id = target.from_user.id
        language = database.get_language(user_id)
        requests = database.list_user_requests(user_id)
        text = (
            get_text(language, "history_empty")
            if not requests
            else get_text(language, "history_title")
        )
        markup = history_menu(requests) if requests else None
        if isinstance(target, CallbackQuery):
            await target.message.edit_text(text, reply_markup=markup)
            await target.answer()
        else:
            await target.answer(text, reply_markup=markup)

    @router.message(Command("history"))
    async def history_command(message: Message) -> None:
        await show_history(message)

    @router.callback_query(lambda query: query.data == "history")
    async def history_button(callback: CallbackQuery) -> None:
        await show_history(callback)

    @router.callback_query(
        lambda query: query.data and query.data.startswith("request:")
    )
    async def request_detail(callback: CallbackQuery) -> None:
        request_id = int(callback.data.split(":", 1)[1])
        request = database.get_request(request_id)
        if not request or request["user_id"] != callback.from_user.id:
            await callback.answer("Request not found", show_alert=True)
            return
        language = database.get_language(callback.from_user.id)
        conversation = "\n".join(
            f"<b>{'You' if item['author_role'] == 'user' else 'Support'}</b> [{item['created_at']}]\n{html.escape(item['body'])}"
            for item in database.get_messages(request_id)
        )
        status = get_text(language, f"status_{request['status']}")
        await callback.message.edit_text(
            get_text(
                language,
                "request_detail",
                request_id=request_id,
                status=status,
                created_at=request["created_at"],
                conversation=conversation,
            )
        )
        await callback.answer()

    return router
