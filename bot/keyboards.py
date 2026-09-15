from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .locales import LANGUAGES


def main_menu(language: str, is_admin: bool = False) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(text=f"{icon} {label}", callback_data=action)
            for icon, label, action in [
                ("✉️", _text(language, "menu_feedback"), "feedback"),
                ("🗂", _text(language, "menu_history"), "history"),
            ]
        ],
        [
            InlineKeyboardButton(
                text=f"🌐 {_text(language, 'menu_language')}", callback_data="language"
            ),
            InlineKeyboardButton(
                text=f"ℹ️ {_text(language, 'menu_help')}", callback_data="help"
            ),
        ],
    ]
    if is_admin:
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"🛡 {_text(language, 'menu_admin')}", callback_data="admin"
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def language_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=label, callback_data=f"lang:{code}")]
            for code, label in LANGUAGES.items()
        ]
    )


def history_menu(requests: list[dict]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"#{item['id']} · {item['status']}",
                    callback_data=f"request:{item['id']}",
                )
            ]
            for item in requests
        ]
    )


def admin_menu(requests: list[dict], language: str = "en") -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text=_text(language, "admin_open"), callback_data="admin_list:open"
            ),
            InlineKeyboardButton(
                text=_text(language, "admin_closed"), callback_data="admin_list:closed"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_text(language, "admin_all"), callback_data="admin_list:all"
            )
        ],
    ]
    rows.extend(
        [
            [
                InlineKeyboardButton(
                    text=f"#{item['id']} · {item['status']}",
                    callback_data=f"admin_request:{item['id']}",
                )
            ]
            for item in requests
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_request_menu(
    request_id: int, language: str = "en", status: str = "open"
) -> InlineKeyboardMarkup:
    action = "admin_reopen" if status == "closed" else "admin_close"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="↩️ Reply", callback_data=f"admin_reply:{request_id}"
                ),
                InlineKeyboardButton(
                    text=_text(language, action), callback_data=f"{action}:{request_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_text(language, "admin_back"), callback_data="admin"
                )
            ],
        ]
    )


def _text(language: str, key: str) -> str:
    from .locales import get_text

    return get_text(language, key)
