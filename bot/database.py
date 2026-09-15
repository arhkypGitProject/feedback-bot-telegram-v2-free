import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock


class Database:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.lock = Lock()
        self._create_tables()

    def _create_tables(self) -> None:
        with self.connection:
            self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                language TEXT NOT NULL DEFAULT 'en',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'open',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER NOT NULL,
                author_id INTEGER NOT NULL,
                author_role TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """)

    def _now(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    def ensure_user(self, telegram_id: int) -> None:
        with self.lock, self.connection:
            self.connection.execute(
                "INSERT OR IGNORE INTO users(telegram_id, created_at) VALUES (?, ?)",
                (telegram_id, self._now()),
            )

    def get_language(self, telegram_id: int) -> str:
        self.ensure_user(telegram_id)
        row = self.connection.execute(
            "SELECT language FROM users WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
        return row["language"] if row else "en"

    def set_language(self, telegram_id: int, language: str) -> None:
        self.ensure_user(telegram_id)
        with self.lock, self.connection:
            self.connection.execute(
                "UPDATE users SET language = ? WHERE telegram_id = ?",
                (language, telegram_id),
            )

    def create_request(self, user_id: int, body: str) -> int:
        now = self._now()
        with self.lock, self.connection:
            cursor = self.connection.execute(
                "INSERT INTO requests(user_id, created_at, updated_at) VALUES (?, ?, ?)",
                (user_id, now, now),
            )
            request_id = cursor.lastrowid
            self.connection.execute(
                "INSERT INTO messages(request_id, author_id, author_role, body, created_at) VALUES (?, ?, 'user', ?, ?)",
                (request_id, user_id, body, now),
            )
            return int(request_id)

    def add_message(
        self, request_id: int, author_id: int, role: str, body: str
    ) -> None:
        now = self._now()
        with self.lock, self.connection:
            self.connection.execute(
                "INSERT INTO messages(request_id, author_id, author_role, body, created_at) VALUES (?, ?, ?, ?, ?)",
                (request_id, author_id, role, body, now),
            )
            self.connection.execute(
                "UPDATE requests SET status = ?, updated_at = ? WHERE id = ?",
                ("answered" if role == "admin" else "open", now, request_id),
            )

    def list_user_requests(self, user_id: int) -> list[dict]:
        rows = self.connection.execute(
            "SELECT id, status, created_at FROM requests WHERE user_id = ? ORDER BY id DESC",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]

    def list_open_requests(self) -> list[dict]:
        rows = self.connection.execute(
            "SELECT id, user_id, status, created_at FROM requests WHERE status IN ('open', 'answered') ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]

    def list_requests(self, status: str | None = None) -> list[dict]:
        if status == "open":
            rows = self.connection.execute(
                "SELECT id, user_id, status, created_at FROM requests WHERE status IN ('open', 'answered') ORDER BY id DESC"
            ).fetchall()
        elif status:
            rows = self.connection.execute(
                "SELECT id, user_id, status, created_at FROM requests WHERE status = ? ORDER BY id DESC",
                (status,),
            ).fetchall()
        else:
            rows = self.connection.execute(
                "SELECT id, user_id, status, created_at FROM requests ORDER BY id DESC"
            ).fetchall()
        return [dict(row) for row in rows]

    def set_request_status(self, request_id: int, status: str) -> None:
        with self.lock, self.connection:
            self.connection.execute(
                "UPDATE requests SET status = ?, updated_at = ? WHERE id = ?",
                (status, self._now(), request_id),
            )

    def get_request(self, request_id: int) -> dict | None:
        row = self.connection.execute(
            "SELECT id, user_id, status, created_at FROM requests WHERE id = ?",
            (request_id,),
        ).fetchone()
        return dict(row) if row else None

    def get_messages(self, request_id: int) -> list[dict]:
        rows = self.connection.execute(
            "SELECT author_id, author_role, body, created_at FROM messages WHERE request_id = ? ORDER BY id",
            (request_id,),
        ).fetchall()
        return [dict(row) for row in rows]
