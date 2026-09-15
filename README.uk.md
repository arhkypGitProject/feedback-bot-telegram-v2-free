[English](README.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Українська](README.uk.md)

[![CI](https://github.com/arhkypGitProject/feedback-bot-telegram-v2-free/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/arhkypGitProject/feedback-bot-telegram-v2-free/actions/workflows/main.yml) [![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/) [![License](https://img.shields.io/github/license/arhkypGitProject/feedback-bot-telegram-v2-free)](LICENSE)
[![Stars](https://img.shields.io/github/stars/arhkypGitProject/feedback-bot-telegram-v2-free?style=flat&logo=github)](https://github.com/arhkypGitProject/feedback-bot-telegram-v2-free/stargazers) [![Forks](https://img.shields.io/github/forks/arhkypGitProject/feedback-bot-telegram-v2-free?style=flat&logo=github)](https://github.com/arhkypGitProject/feedback-bot-telegram-v2-free/network/members) [![Issues](https://img.shields.io/github/issues/arhkypGitProject/feedback-bot-telegram-v2-free)](https://github.com/arhkypGitProject/feedback-bot-telegram-v2-free/issues) [![Views](https://komarev.com/ghpvc/?username=arhkypGitProject&repo=feedback-bot-telegram-v2-free&color=2563EB&style=flat)](https://github.com/arhkypGitProject/feedback-bot-telegram-v2-free)
[![Last commit](https://img.shields.io/github/last-commit/arhkypGitProject/feedback-bot-telegram-v2-free)](https://github.com/arhkypGitProject/feedback-bot-telegram-v2-free/commits/master) [![Repo size](https://img.shields.io/github/repo-size/arhkypGitProject/feedback-bot-telegram-v2-free)](https://github.com/arhkypGitProject/feedback-bot-telegram-v2-free)
[![Підтримати на Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/O2X6272I51)

# Clearline Feedback Bot

> Сучасний багатомовний Telegram-бот для зворотного зв’язку з приватною історією звернень, прозорим повідомленням про конфіденційність і захищеною панеллю адміністратора.

## Огляд

Clearline перетворює Telegram-чат на невеликий центр підтримки. Користувачі обирають мову, створюють звернення, переглядають повну історію листування та отримують відповіді адміністрації в тому самому чаті. Адміністратори мають захищену панель із відкритими, закритими зверненнями та повним архівом.

## Можливості

- 🌍 Інтерфейс англійською, російською, польською, українською та німецькою мовами
- ✉️ Створення звернень через inline-кнопки та команду `/feedback`
- 🗂 Особиста історія звернень із повідомленнями користувача й адміністратора
- 🛡 Панель лише для адміністраторів із перевіркою Telegram ID
- 📥 Розділи відкритих, закритих і всіх звернень
- ✅ Закриття та повторне відкриття звернень у вікні переписки адміністратора
- 💾 Локальна база SQLite без окремого сервера баз даних
- 🔒 Чітке повідомлення: переписка записується, є конфіденційною та може бути переглянута уповноваженими адміністраторами за потреби
- ⌨️ Меню команд Telegram автоматично реєструється під час запуску
- 🧱 Модульні роутери aiogram, FSM-стани, обмеження введення, перевірка власника та екранування HTML

## Підтримувані команди

| Команда | Призначення |
| --- | --- |
| `/start` | Відкрити головне меню |
| `/feedback` | Створити нове звернення |
| `/history` | Переглянути особисту історію звернень |
| `/language` | Обрати англійську, російську, польську, українську або німецьку мову |
| `/help` | Відкрити локалізовану довідку та інформацію про конфіденційність |
| `/cancel` | Вийти з поточного режиму введення |
| `/admin` | Відкрити панель адміністратора для авторизованих користувачів |

## Сценарій користувача

На першому екрані розташоване компактне inline-меню. Користувач може створити звернення без знання команд, у будь-який момент змінити мову та відкрити звернення для перегляду повної хронології. Повідомлення зберігаються разом із роллю автора та часом UTC. Користувач бачить лише власні звернення.

## Сценарій адміністратора

Telegram ID, указані в `ADMIN_IDS`, можуть відкрити панель адміністратора. Вона розділяє поточну роботу та історію:

1. **Відкриті звернення** показують запити, які потребують уваги.
2. **Закриті звернення** показують вирішені запити.
3. **Вся історія звернень** показує всі збережені запити.

Адміністратор може відкрити звернення, переглянути повну переписку, відповісти користувачу, закрити звернення та відкрити його знову. Відповідь зберігається до спроби доставки.

## Конфіденційність і безпека

Бот повідомляє користувачам, що переписка з командою підтримки записується для якості сервісу та історії звернень. Переписка є конфіденційною, але уповноважені адміністратори можуть переглядати її, коли це потрібно для вирішення звернення. Обмежте `ADMIN_IDS` довіреними обліковими записами.

Застосунок також використовує базові заходи захисту: перевірку адміністратора в кожному callback панелі, перевірку власника звернення, обмеження повідомлень до 4 000 символів, екранування HTML користувача, локальний файл `.env` і шлях до бази, виключений із Git.

## Структура проєкту

```text
main.py                    Точка запуску та команди Telegram
bot/config.py              Конфігурація середовища
bot/database.py            Схема SQLite і репозиторій звернень
bot/locales.py             Локалізовані тексти інтерфейсу
bot/keyboards.py           Inline-меню
bot/states.py              FSM-стани
bot/handlers/start.py      Старт, довідка та вибір мови
bot/handlers/feedback.py   Створення та скасування звернень
bot/handlers/history.py    Історія звернень користувача
bot/handlers/admin.py      Захищена панель і відповіді адміністратора
README.md                  Документація англійською
README.ru.md               Документація російською
README.pl.md               Документація польською
README.uk.md               Документація українською
LICENSE                    Дозвіл використовувати та змінювати проєкт
```

## Встановлення

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Налаштуйте файл `.env`:

```env
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_IDS=123456789,987654321
DATABASE_PATH=data/feedback.sqlite3
```

Токен бота можна отримати в [@BotFather](https://t.me/BotFather), а Telegram ID — через [@userinfobot](https://t.me/userinfobot). Запустіть застосунок:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Для портфоліо

Проєкт навмисно зроблено невеликим і зрозумілим: публічний інтерфейс, рівень зберігання даних, локалізацію та межі авторизації легко продемонструвати в портфоліо. Ви можете змінити бренд, тексти, базу даних або спосіб розгортання відповідно до власного продукту.

## Ліцензія

Проєкт поширюється за дозвільною ліцензією MIT. Ви можете використовувати його для особистих і комерційних цілей, змінювати, поширювати та адаптувати під власні потреби. Повні умови наведено у файлі [LICENSE](LICENSE).
