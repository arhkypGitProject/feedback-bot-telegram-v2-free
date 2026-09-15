import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from bot.config import load_settings
from bot.database import Database
from bot.handlers import admin, feedback, history, start


async def configure_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Open the support menu"),
            BotCommand(command="feedback", description="Create a feedback request"),
            BotCommand(command="history", description="View your request history"),
            BotCommand(command="language", description="Change interface language"),
            BotCommand(command="help", description="Show help"),
            BotCommand(command="cancel", description="Cancel current action"),
            BotCommand(command="admin", description="Open admin panel"),
        ]
    )


async def main() -> None:
    settings = load_settings()
    database = Database(settings.database_path)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()
    dispatcher.include_router(start.create_router(database, settings))
    dispatcher.include_router(feedback.create_router(database, settings))
    dispatcher.include_router(history.create_router(database, settings))
    dispatcher.include_router(admin.create_router(database, settings))

    try:
        await configure_commands(bot)
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
