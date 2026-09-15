[English](README.md) · [Русский](README.ru.md) · [Polski](README.pl.md)

# Clearline Feedback Bot

> A polished, multilingual Telegram feedback desk with private request history, transparent privacy messaging, and a protected administrator workspace.

## Overview

Clearline turns a Telegram chat into a small support desk. Users choose their language, create a feedback request, review the complete conversation history, and receive administrator replies in the same chat. Administrators get a protected panel with open requests, closed requests, and the complete request archive.

## Features

- 🌍 English, Russian, Polish, Ukrainian, and German interface
- ✉️ Inline-button feedback flow with `/feedback` command support
- 🗂 Personal request history with every user and administrator message
- 🛡 Administrator-only panel protected by Telegram user IDs
- 📥 Open requests, closed requests, and all request history views
- ✅ Close and reopen requests from the administrator conversation view
- 💾 Local SQLite database with no external database server
- 🔒 Clear notice that conversations are recorded, confidential, and reviewable by authorized administrators when required
- ⌨️ Telegram command menu registered on startup
- 🧱 Modular aiogram routers, FSM states, input limits, ownership checks, and HTML escaping

## Supported commands

| Command | Purpose |
| --- | --- |
| `/start` | Open the main menu |
| `/feedback` | Create a feedback request |
| `/history` | View personal request history |
| `/language` | Select English, Russian, Polish, Ukrainian, or German |
| `/help` | Read the localized usage and privacy guide |
| `/cancel` | Leave the current input flow |
| `/admin` | Open the administrator panel when authorized |

## User experience

The first screen is a compact inline menu. A user can create a request without learning commands, choose a language at any time, and open a request to see the full timeline. Messages are stored with their author role and UTC timestamp. Users can only view their own requests.

## Administrator experience

Telegram IDs listed in `ADMIN_IDS` can open the admin panel. The panel separates active work from historical work:

1. **Open requests** shows requests that still require attention.
2. **Closed requests** shows resolved requests.
3. **All request history** shows every stored request.

An administrator can open a request, inspect the complete conversation, reply to the owner, close it, and reopen it later. Replies are saved before delivery is attempted.

## Privacy and security

The bot tells users that support conversations are recorded for service quality and request history. The conversations are confidential, but authorized administrators may review them when needed to resolve a request. Keep `ADMIN_IDS` limited to trusted accounts.

The application also applies basic protections: administrator checks on every admin callback, request ownership checks for users, a 4,000-character message limit, HTML escaping for user content, a local `.env` file, and a database path excluded from Git.

## Project structure

```text
main.py                    Application entry point and Telegram commands
bot/config.py              Environment configuration
bot/database.py            SQLite schema and request repository
bot/locales.py             Localized interface copy
bot/keyboards.py           Inline menus
bot/states.py              FSM states
bot/handlers/start.py      Start, help, and language routes
bot/handlers/feedback.py   Request creation and cancellation
bot/handlers/history.py    User request history
bot/handlers/admin.py      Protected admin inbox and replies
README.md                  English documentation
README.ru.md               Russian documentation
LICENSE                    Permission to use and modify the project
```

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Configure `.env`:

```env
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_IDS=123456789,987654321
DATABASE_PATH=data/feedback.sqlite3
```

Get a bot token from [@BotFather](https://t.me/BotFather). Get a Telegram user ID from [@userinfobot](https://t.me/userinfobot). Start the application with:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Portfolio notes

This project is intentionally small and readable: the public interface, persistence layer, localization, and authorization boundaries are easy to demonstrate in a portfolio. Replace the branding, copy, database layer, or deployment setup to match your product.

## License

This project is released under the permissive MIT License. You may use it for personal or commercial purposes, modify it, redistribute it, and adapt it for your own needs. See [LICENSE](LICENSE) for the complete terms.
