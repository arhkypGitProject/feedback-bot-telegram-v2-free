from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_ids: frozenset[int]
    database_path: Path


def load_settings() -> Settings:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("BOT_TOKEN is not configured. Add it to the .env file.")

    raw_admin_ids = os.getenv("ADMIN_IDS", "").split(",")
    admin_ids = frozenset(
        int(value.strip()) for value in raw_admin_ids if value.strip().isdigit()
    )
    if not admin_ids:
        raise RuntimeError("ADMIN_IDS is not configured. Add at least one Telegram user ID.")

    return Settings(
        bot_token=token,
        admin_ids=admin_ids,
        database_path=BASE_DIR / os.getenv("DATABASE_PATH", "data/feedback.sqlite3"),
    )