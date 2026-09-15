[English](README.md) · [Русский](README.ru.md) · [Polski](README.pl.md)

# Clearline Feedback Bot

> Nowoczesny, wielojęzyczny bot Telegram do obsługi opinii, z prywatną historią zgłoszeń, jasną informacją o prywatności i chronionym panelem administratora.

## Przegląd

Clearline zamienia rozmowę na Telegramie w małe centrum obsługi. Użytkownicy wybierają język, tworzą zgłoszenia, przeglądają pełną historię rozmowy i otrzymują odpowiedzi administratorów w tym samym czacie. Administratorzy mają chroniony panel z otwartymi zgłoszeniami, zamkniętymi zgłoszeniami i pełnym archiwum.

## Funkcje

- 🌍 Interfejs w języku angielskim, rosyjskim, polskim, ukraińskim i niemieckim
- ✉️ Tworzenie zgłoszeń przez przyciski inline oraz komendę `/feedback`
- 🗂 Osobista historia zgłoszeń zawierająca wiadomości użytkownika i administratora
- 🛡 Panel dostępny wyłącznie dla administratorów na podstawie identyfikatorów Telegram
- 📥 Widoki otwartych zgłoszeń, zamkniętych zgłoszeń i całej historii
- ✅ Zamykanie i ponowne otwieranie zgłoszeń z poziomu rozmowy administratora
- 💾 Lokalna baza SQLite bez dodatkowego serwera baz danych
- 🔒 Jasna informacja, że rozmowy są zapisywane, poufne i mogą być przeglądane przez upoważnionych administratorów, gdy jest to konieczne
- ⌨️ Menu komend Telegrama rejestrowane automatycznie przy uruchomieniu
- 🧱 Modułowe routery aiogram, stany FSM, limity wejścia, kontrola właściciela i escapowanie HTML

## Obsługiwane komendy

| Komenda | Zastosowanie |
| --- | --- |
| `/start` | Otwiera menu główne |
| `/feedback` | Tworzy nowe zgłoszenie |
| `/history` | Pokazuje osobistą historię zgłoszeń |
| `/language` | Wybiera język angielski, rosyjski, polski, ukraiński lub niemiecki |
| `/help` | Otwiera zlokalizowaną pomoc i informacje o prywatności |
| `/cancel` | Opuszcza bieżący tryb wprowadzania |
| `/admin` | Otwiera panel administratora dla uprawnionych użytkowników |

## Doświadczenie użytkownika

Pierwszy ekran zawiera kompaktowe menu inline. Użytkownik może utworzyć zgłoszenie bez znajomości komend, w dowolnym momencie zmienić język i otworzyć zgłoszenie, aby zobaczyć pełną oś czasu. Wiadomości są przechowywane wraz z rolą autora i czasem UTC. Użytkownik widzi wyłącznie własne zgłoszenia.

## Doświadczenie administratora

Identyfikatory Telegrama znajdujące się w `ADMIN_IDS` mogą otworzyć panel administratora. Panel rozdziela bieżącą pracę od historii:

1. **Otwarte zgłoszenia** pokazują sprawy wymagające uwagi.
2. **Zamknięte zgłoszenia** pokazują rozwiązane sprawy.
3. **Cała historia zgłoszeń** pokazuje wszystkie zapisane sprawy.

Administrator może otworzyć zgłoszenie, sprawdzić pełną rozmowę, odpowiedzieć użytkownikowi, zamknąć zgłoszenie i otworzyć je ponownie. Odpowiedzi są zapisywane przed próbą dostarczenia.

## Prywatność i bezpieczeństwo

Bot informuje użytkowników, że rozmowy z zespołem wsparcia są zapisywane na potrzeby jakości obsługi i historii zgłoszeń. Rozmowy są poufne, ale upoważnieni administratorzy mogą je przeglądać, gdy jest to potrzebne do rozwiązania sprawy. Ogranicz `ADMIN_IDS` do zaufanych kont.

Aplikacja stosuje również podstawowe zabezpieczenia: sprawdzanie administratora przy każdym callbacku panelu, kontrolę właściciela zgłoszenia, limit wiadomości do 4000 znaków, escapowanie HTML użytkownika, lokalny plik `.env` oraz ścieżkę bazy wykluczoną z Git.

## Struktura projektu

```text
main.py                    Punkt wejścia aplikacji i komendy Telegrama
bot/config.py              Konfiguracja środowiska
bot/database.py            Schemat SQLite i repozytorium zgłoszeń
bot/locales.py             Zlokalizowane teksty interfejsu
bot/keyboards.py           Menu inline
bot/states.py              Stany FSM
bot/handlers/start.py      Start, pomoc i wybór języka
bot/handlers/feedback.py   Tworzenie i anulowanie zgłoszeń
bot/handlers/history.py    Historia zgłoszeń użytkownika
bot/handlers/admin.py      Chroniony panel i odpowiedzi administratora
README.md                  Dokumentacja angielska
README.ru.md               Dokumentacja rosyjska
README.pl.md               Dokumentacja polska
LICENSE                    Zezwolenie na używanie i modyfikowanie projektu
```

## Instalacja

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Skonfiguruj plik `.env`:

```env
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_IDS=123456789,987654321
DATABASE_PATH=data/feedback.sqlite3
```

Token bota otrzymasz od [@BotFather](https://t.me/BotFather), a identyfikator Telegrama możesz uzyskać przez [@userinfobot](https://t.me/userinfobot). Uruchom aplikację:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Informacje do portfolio

Projekt jest celowo mały i czytelny: interfejs publiczny, warstwa przechowywania danych, lokalizacja i granice autoryzacji łatwo zaprezentować w portfolio. Możesz zmienić markę, teksty, bazę danych lub sposób wdrożenia zgodnie z własnym produktem.

## Licencja

Projekt jest udostępniany na liberalnej licencji MIT. Możesz używać go do celów prywatnych i komercyjnych, modyfikować, rozpowszechniać i dostosowywać do własnych potrzeb. Pełne warunki znajdują się w pliku [LICENSE](LICENSE).
