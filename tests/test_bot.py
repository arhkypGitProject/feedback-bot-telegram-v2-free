import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from bot.config import load_settings
from bot.database import Database
from bot.handlers import admin, feedback, history, start
from bot.keyboards import admin_menu, language_menu, main_menu
from bot.locales import ERROR_TEXTS, EXTRA_TEXTS, LANGUAGES, TEXTS, get_text


class DatabaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = Database(Path(self.temp_dir.name) / "test.sqlite3")

    def tearDown(self) -> None:
        self.database.connection.close()
        self.temp_dir.cleanup()

    def test_user_language_is_saved(self) -> None:
        self.database.set_language(7, "uk")
        self.assertEqual(self.database.get_language(7), "uk")

    def test_request_conversation_and_status_lifecycle(self) -> None:
        request_id = self.database.create_request(7, "Initial message")
        self.database.add_message(request_id, 100, "admin", "Support reply")

        self.assertEqual(self.database.get_request(request_id)["status"], "answered")
        self.assertEqual(len(self.database.get_messages(request_id)), 2)
        self.assertEqual(
            self.database.get_messages(request_id)[1]["body"], "Support reply"
        )

        self.database.set_request_status(request_id, "closed")
        self.assertEqual(len(self.database.list_requests("open")), 0)
        self.assertEqual(len(self.database.list_requests("closed")), 1)
        self.assertEqual(len(self.database.list_requests()), 1)

    def test_user_history_is_isolated(self) -> None:
        self.database.create_request(7, "Visible request")
        self.database.create_request(8, "Private request")

        history = self.database.list_user_requests(7)

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["id"], 1)


class LocalizationTests(unittest.TestCase):
    def test_all_languages_have_all_copy_keys(self) -> None:
        keys = set(TEXTS["en"]) | set(EXTRA_TEXTS["en"]) | set(ERROR_TEXTS["en"])
        for language in LANGUAGES:
            available = set(TEXTS.get(language, {}))
            available |= set(EXTRA_TEXTS.get(language, {}))
            available |= set(ERROR_TEXTS.get(language, {}))
            self.assertEqual(keys - available, set(), language)

    def test_localized_text_formats_request_values(self) -> None:
        for language in LANGUAGES:
            text = get_text(language, "feedback_saved", request_id=12)
            self.assertIn("12", text)


class InterfaceTests(unittest.TestCase):
    def test_main_menu_contains_user_actions(self) -> None:
        menu = main_menu("ru", is_admin=True)
        callbacks = [
            button.callback_data for row in menu.inline_keyboard for button in row
        ]

        self.assertIn("feedback", callbacks)
        self.assertIn("history", callbacks)
        self.assertIn("language", callbacks)
        self.assertIn("help", callbacks)
        self.assertIn("admin", callbacks)

    def test_language_and_admin_menus_have_expected_callbacks(self) -> None:
        languages = language_menu()
        language_callbacks = [
            button.callback_data for row in languages.inline_keyboard for button in row
        ]
        self.assertEqual(
            set(language_callbacks), {f"lang:{code}" for code in LANGUAGES}
        )

        admin = admin_menu([{"id": 3, "status": "open"}], "en")
        admin_callbacks = [
            button.callback_data for row in admin.inline_keyboard for button in row
        ]
        self.assertIn("admin_list:open", admin_callbacks)
        self.assertIn("admin_list:closed", admin_callbacks)
        self.assertIn("admin_list:all", admin_callbacks)
        self.assertIn("admin_request:3", admin_callbacks)


class ConfigurationTests(unittest.TestCase):
    def test_settings_require_admin_id(self) -> None:
        test_token = os.environ.get("CI_TEST_TOKEN", "placeholder")
        with (
            patch.dict(
                os.environ, {"BOT_TOKEN": test_token, "ADMIN_IDS": ""}, clear=False
            ),
            self.assertRaisesRegex(RuntimeError, "ADMIN_IDS"),
        ):
            load_settings()

    def test_all_routers_can_be_created(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            test_token = os.environ.get("CI_TEST_TOKEN", "placeholder")
            with patch.dict(
                os.environ,
                {
                    "BOT_TOKEN": test_token,
                    "ADMIN_IDS": "1",
                    "DATABASE_PATH": str(Path(temp_dir) / "ci.sqlite3"),
                },
                clear=False,
            ):
                settings = load_settings()
                database = Database(settings.database_path)
                routers = [
                    start.create_router(database, settings),
                    feedback.create_router(database, settings),
                    history.create_router(database, settings),
                    admin.create_router(database, settings),
                ]
                self.assertEqual(len(routers), 4)
                database.connection.close()


if __name__ == "__main__":
    unittest.main()
