# Szron — sklep narciarski z wypożyczalnią

Pierwszy etap: lokalna aplikacja Django z PostgreSQL, stroną główną, katalogiem,
szczegółami produktu oraz panelem administratora. „Szron” jest nazwą roboczą.
Zakupy, konta klientów i rezerwacje będą rozwijane w kolejnych etapach.

## Uruchomienie na obecnym komputerze

W VS Code otwórz **katalog zawierający ten README i plik `manage.py`**.
Środowisko Python, prywatny `.env`, przenośny PostgreSQL i cztery produkty
demonstracyjne zostały przygotowane lokalnie. Pliki te nie trafiają do GitHub.

W terminalu PowerShell:

```powershell
./start.ps1
```

Otwórz [stronę sklepu](http://127.0.0.1:8000/) lub
[panel administratora](http://127.0.0.1:8000/admin/).
Jeśli PowerShell blokuje skrypt, możesz uruchomić go tylko dla tego procesu:

```powershell
powershell -ExecutionPolicy Bypass -File ./start.ps1
```

Utwórz własne konto administratora w drugim terminalu; login i hasło podaj w pytaniach programu:

```powershell
./.venv/Scripts/python manage.py createsuperuser
```

Nie ma wspólnego ani domyślnego hasła administratora. Po utworzeniu konta zaloguj
się w panelu i otwórz „Produkty”. Zmień cenę lub liczbę sztuk, zapisz i odśwież katalog.
Zmiana powinna być widoczna od razu. `Ctrl+C` zatrzymuje stronę, baza działa osobno.
Przenośny serwer w tej kopii korzysta z portu **55432**, dostępnego wyłącznie lokalnie.
Możesz go zatrzymać po zakończeniu pracy:

```powershell
./work/postgres/pgsql/bin/pg_ctl -D ./work/pgdata-local -w stop
```

## Pierwsze uruchomienie na drugim komputerze

### 1. Zainstaluj narzędzia

- Python 3.12 lub 3.13, dostępny jako `python`.
- PostgreSQL 18 z [oficjalnego instalatora](https://www.postgresql.org/download/windows/).
  Zapisz swoje hasło administratora bazy poza repozytorium. pgAdmin jest opcjonalnym
  interfejsem do przeglądania bazy; Stack Builder nie jest potrzebny.
- Pobierz repozytorium i otwórz jego katalog w VS Code.

Wszystkie poniższe polecenia wykonuj w katalogu z `manage.py`.

### 2. Przygotuj Pythona

```powershell
python -m venv .venv
./.venv/Scripts/python -m pip install -r requirements.txt
Copy-Item .env.example .env
./.venv/Scripts/python -c "from django.core.management.utils import get_random_secret_key; from dotenv import set_key; set_key('.env', 'DJANGO_SECRET_KEY', get_random_secret_key())"
```

W VS Code wybierz interpreter `.venv/Scripts/python.exe`.
Wygenerowany klucz jest zapisywany tylko w ignorowanym `.env`, bez wyświetlania go.

### 3. Utwórz lokalną bazę PostgreSQL

Uruchom **SQL Shell (psql)** z menu Start i połącz się jako `postgres` z lokalnym
serwerem. Domyślny port instalatora to 5432. Wpisz w SQL Shell:

```sql
CREATE ROLE szron_app LOGIN CREATEDB;
\password szron_app
CREATE DATABASE szron OWNER szron_app ENCODING 'UTF8';
```

Polecenie `\password` poprosi o Twoje własne hasło użytkownika aplikacji.
Nie jest to hasło konta klienta ani administratora strony.
Uprawnienie `CREATEDB` służy do tworzenia osobnej bazy testowej podczas lokalnych testów;
nie oznacza uprawnień superużytkownika PostgreSQL.

Uzupełnij `.env`: wpisz to hasło w `POSTGRES_PASSWORD` i sprawdź host, port,
nazwę bazy i użytkownika. Jeśli wartość zawiera znaki specjalne, otocz ją
pojedynczymi cudzysłowami zgodnie z formatem dotenv. Nie kopiuj ustawień portu 55432
z pierwszego komputera, jeżeli Twój serwer działa na 5432.

### 4. Utwórz strukturę i dane

```powershell
./.venv/Scripts/python manage.py migrate
./.venv/Scripts/python manage.py seed_demo
./.venv/Scripts/python manage.py createsuperuser
./start.ps1
```

`seed_demo` dodaje cztery fikcyjne produkty. Można uruchamiać je wielokrotnie:
nie duplikuje produktów ani nie nadpisuje późniejszych zmian ich ceny i stanu.
Ilustracje w katalogu są własnymi grafikami kategorii, nie zdjęciami konkretnych modeli.

## Codzienna praca i sprawdzanie

Po pobraniu zmian z GitHub zainstaluj zależności, jeśli zmienił się `requirements.txt`,
i uruchom migracje. Każdy komputer ma własną bazę oraz własne konta i hasła.
Git synchronizuje kod, migracje i definicje danych demonstracyjnych, a nie zawartość baz.

```powershell
./.venv/Scripts/python manage.py migrate
./.venv/Scripts/python manage.py check
./.venv/Scripts/python manage.py test
./.venv/Scripts/python manage.py makemigrations --check --dry-run
```

Testy korzystają z PostgreSQL i tworzą oraz usuwają osobną bazę `test_szron`;
nie uruchamiaj ich na bazie produkcyjnej ani na bazie z taką nazwą zawierającej ważne dane.
Przy zmianie modeli twórz migracje przez `manage.py makemigrations` i dodawaj je do commita.

## Organizacja kodu

- `config/` — ustawienia, adresy i uruchamianie aplikacji.
- `accounts/` — własny model użytkownika oparty na Django, przygotowany do dalszej rozbudowy.
- `catalog/` — produkty, widoki, panel administratora, migracje i testy.
- `templates/` — wspólna rama HTML i strony katalogu.
- `static/` — style i własne ilustracje SVG. Strona nie wymaga zewnętrznych fontów ani usług.

Ceny są przechowywane jako liczby dziesiętne, a `sale_stock` opisuje wyłącznie sztuki
na sprzedaż. Przyszłe egzemplarze wypożyczalni będą miały osobną ewidencję.
Produkty można ukryć bez usuwania ich z bazy. Uprawnienia panelu sprawdza backend Django.

## Kontekst i bezpieczeństwo konfiguracji

Przed pracą przeczytaj `AGENTS.md`, `PROJECT_CONTEXT.md` i `TODO.md`.
Przy każdym commicie aktualizuj kontekst. `TODO.md` wypełniamy uzgodnionymi
zadaniami na kolejną sesję, przede wszystkim pod koniec pracy.

Nigdy nie commituj `.env`, `.venv`, danych bazy ani katalogu `work/`.
`.env.example` zawiera wyłącznie nazwy ustawień i puste miejsca na sekrety.
Serwer `runserver` i `DJANGO_DEBUG=True` służą do pracy lokalnej. Publikacja strony
wymaga osobnej konfiguracji HTTPS, hostów, plików statycznych i ustawień bezpieczeństwa.

Jeżeli połączenie z bazą nie działa, sprawdź, czy PostgreSQL jest uruchomiony,
port w `.env` jest poprawny oraz czy wpisane konto ma dostęp do wskazanej bazy.
Brak `DJANGO_SECRET_KEY` oznacza, że trzeba dokończyć konfigurację `.env`.
