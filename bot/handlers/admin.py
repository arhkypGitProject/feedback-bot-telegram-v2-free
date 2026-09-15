import html

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..config import Settings
from ..database import Database
from ..keyboards import admin_menu, admin_request_menu
from ..locales import get_text
from ..states import AdminState


def create_router(database: Database, settings: Settings) -> Router:
    router = Router(name="admin")

    def is_admin(user_id: int) -> bool:
        return user_id in settings.admin_ids

    async def show_admin(target: Message | CallbackQuery) -> None:
        user_id = target.from_user.id
        if not is_admin(user_id):
            if isinstance(target, CallbackQuery):
                await target.answer(get_text(database.get_language(user_id), "admin_only"), show_alert=True)
            else:
                await target.answer(get_text(database.get_language(user_id), "admin_only"))
            return
        language = database.get_language(user_id)
        requests = database.list_open_requests()
        text = get_text(language, "admin_title", count=len(requests)) if requests else get_text(language, "admin_empty")
        markup = admin_menu(requests, language) if requests else None
        if isinstance(target, CallbackQuery):
            await target.message.edit_text(text, reply_markup=markup)
            await target.answer()
        else:
            await target.answer(text, reply_markup=markup)

    @router.message(Command("admin"))
    async def admin_command(message: Message) -> None:
        await show_admin(message)

    @router.callback_query(lambda query: query.data == "admin")
    async def admin_button(callback: CallbackQuery) -> None:
        await show_admin(callback)

    @router.callback_query(lambda query: query.data and query.data.startswith("admin_list:"))
    async def admin_list(callback: CallbackQuery) -> None:
        if not is_admin(callback.from_user.id):
            await callback.answer(get_text(database.get_language(callback.from_user.id), "admin_only"), show_alert=True)
            return
        section = callback.data.split(":", 1)[1]
        status = None if section == "all" else section
        requests = database.list_requests(status)
        language = database.get_language(callback.from_user.id)
        title_key = {"open": "admin_section_open", "closed": "admin_section_closed", "all": "admin_section_all"}[section]
        text = get_text(language, title_key, count=len(requests)) if requests else get_text(language, "no_requests")
        await callback.message.edit_text(text, reply_markup=admin_menu(requests, language))
        await callback.answer()

    @router.callback_query(lambda query: query.data and query.data.startswith("admin_request:"))
    async def admin_request(callback: CallbackQuery) -> None:
        if not is_admin(callback.from_user.id):
            await callback.answer(get_text(database.get_language(callback.from_user.id), "admin_only"), show_alert=True)
            return
        request_id = int(callback.data.split(":", 1)[1])
        request = database.get_request(request_id)
        if not request:
            await callback.answer(get_text(database.get_language(callback.from_user.id), "not_found"), show_alert=True)
            return
        language = database.get_language(callback.from_user.id)
        conversation = "\n".join(f"<b>{item['author_role']}</b> [{item['created_at']}]\n{html.escape(item['body'])}" for item in database.get_messages(request_id))
        status = get_text(language, f"status_{request['status']}")
        await callback.message.edit_text(get_text(language, "admin_request", request_id=request_id, user_id=request["user_id"], status=status, created_at=request["created_at"], conversation=conversation), reply_markup=admin_request_menu(request_id, language, request["status"]))
        await callback.answer()

    @router.callback_query(lambda query: query.data and query.data.startswith("admin_close:"))
    async def close_request(callback: CallbackQuery) -> None:
        if not is_admin(callback.from_user.id):
            await callback.answer(get_text(database.get_language(callback.from_user.id), "admin_only"), show_alert=True)
            return
        request_id = int(callback.data.split(":", 1)[1])
        request = database.get_request(request_id)
        if not request:
            await callback.answer(get_text(database.get_language(callback.from_user.id), "not_found"), show_alert=True)
            return
        database.set_request_status(request_id, "closed")
        language = database.get_language(callback.from_user.id)
        await callback.answer(get_text(language, "request_closed", request_id=request_id))
        await callback.message.edit_reply_markup(reply_markup=admin_request_menu(request_id, language, "closed"))

    @router.callback_query(lambda query: query.data and query.data.startswith("admin_reopen:"))
    async def reopen_request(callback: CallbackQuery) -> None:
        if not is_admin(callback.from_user.id):
            await callback.answer(get_text(database.get_language(callback.from_user.id), "admin_only"), show_alert=True)
            return
        request_id = int(callback.data.split(":", 1)[1])
        request = database.get_request(request_id)
        if not request:
            await callback.answer(get_text(database.get_language(callback.from_user.id), "not_found"), show_alert=True)
            return
        database.set_request_status(request_id, "open")
        language = database.get_language(callback.from_user.id)
        await callback.answer(get_text(language, "request_reopened", request_id=request_id))
        await callback.message.edit_reply_markup(reply_markup=admin_request_menu(request_id, language, "open"))

    @router.callback_query(lambda query: query.data and query.data.startswith("admin_reply:"))
    async def start_reply(callback: CallbackQuery, state: FSMContext) -> None:
        if not is_admin(callback.from_user.id):
            await callback.answer(get_text(database.get_language(callback.from_user.id), "admin_only"), show_alert=True)
            return
        request_id = int(callback.data.split(":", 1)[1])
        await state.update_data(request_id=request_id)
        await state.set_state(AdminState.waiting_for_reply)
        await callback.message.answer(get_text(database.get_language(callback.from_user.id), "reply_prompt", request_id=request_id))
        await callback.answer()

    @router.message(AdminState.waiting_for_reply, F.text)
    async def send_reply(message: Message, state: FSMContext, bot: Bot) -> None:
        if not is_admin(message.from_user.id):
            await state.clear()
            return
        data = await state.get_data()
        request_id = int(data["request_id"])
        request = database.get_request(request_id)
        body = message.text.strip()
        if not request or not body or len(body) > 4000:
            await message.answer(get_text(database.get_language(message.from_user.id), "reply_invalid"))
            return
        database.add_message(request_id, message.from_user.id, "admin", body)
        await state.clear()
        await message.answer(get_text(database.get_language(message.from_user.id), "reply_sent", request_id=request_id))
        user_language = database.get_language(request["user_id"])
        try:
            await bot.send_message(request["user_id"], get_text(user_language, "new_reply", request_id=request_id, message=html.escape(body)))
        except Exception:
            await message.answer(get_text(database.get_language(message.from_user.id), "delivery_failed"))

    return router