# Szron — sklep narciarski z wypożyczalnią

Pierwszy etap: lokalna aplikacja Django z PostgreSQL, stroną główną, katalogiem,
szczegółami produktu oraz panelem administratora. „Szron” jest nazwą roboczą.
Zakupy, konta klientów i rezerwacje będą rozwijane w kolejnych etapach.

## Pobranie obecnej wersji przed prezentacją (22.10.2026)

Jeśli masz już działającą kopię projektu, otwórz PowerShell w swoim folderze
z `manage.py`. Sprawdź `git status --short`: jeśli są lokalne zmiany, najpierw
zachowaj je i uzgodnij połączenie zmian; nie wykonuj resetowania plików.
Przy czystym katalogu wykonaj kolejno (przerwij, jeśli polecenie zwróci błąd):

```powershell
git pull --ff-only origin main
./.venv/Scripts/python -m pip install -r requirements.txt
./.venv/Scripts/python manage.py migrate
./.venv/Scripts/python manage.py seed_demo
./.venv/Scripts/python manage.py check
powershell -ExecutionPolicy Bypass -File ./start.ps1
```

Otwórz http://127.0.0.1:8000/ i odśwież przez Ctrl+F5. Własny `.env`, hasła,
ustawienia portu i bazę zachowaj lokalnie. Jeśli środowiska jeszcze nie ma,
wykonaj sekcję „Pierwsze uruchomienie na drugim komputerze” poniżej.

Repozytorium zawiera wszystkie zdjęcia, CSS, JavaScript, migracje i definicje
czterech produktów demonstracyjnych. Migracje przypisują istniejącym ofertom demo
zdjęcia i wyróżnienie oraz kategorię Kaski; `seed_demo` tworzy brakujące produkty.
Na komputerze autora katalog nadal odpowiada tym danym: Drift 156 i Alpine 172
są wyróżnione, a Summit 27 i Ridge M pozostają w katalogu. Odtworzenie tego zestawu
zapewnia ten sam układ i oferty. `seed_demo` nie nadpisuje własnych zmian produktów
ani nie usuwa dodatkowych ofert na drugim komputerze; takie różnice w bazie trzeba
uzgodnić oddzielnie. Nie przenosimy kont, haseł ani całych plików bazy przez GitHub.

Przed prezentacją sprawdź pokaz czterech panoram, wyróżnione narty i snowboard,
przejście do szczegółów oraz filtr Kaski (Ridge M). Puste kategorie są prawidłowe:
nie dodano jeszcze ofert wiązań, gogli ani butów snowboardowych.

## Uruchomienie na obecnym komputerze

W VS Code otwórz **katalog zawierający ten README i plik `manage.py`**.
Środowisko Python, prywatny `.env` i baza PostgreSQL są przygotowywane lokalnie.
Nie trafiają do GitHub. Na pierwszym komputerze baza jest przenośna, na drugim
działa jako zainstalowana usługa PostgreSQL.

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
Przenośny serwer pierwszego komputera korzysta z portu **55432**; zwykła instalacja
na drugim komputerze z portu **5432**. Właściwy port określa lokalny `.env`.
Poniższe polecenie zatrzymania dotyczy wyłącznie kopii z przenośną bazą w `work/`:

```powershell
./work/postgres/pgsql/bin/pg_ctl -D ./work/pgdata-local -w stop
```

## Pierwsze uruchomienie na drugim komputerze

### 1. Zainstaluj narzędzia

- Python 3.12, 3.13 lub 3.14, dostępny jako `python` (na drugim komputerze sprawdzono 3.14.4).
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

### Zdjęcia i wybór ofert na stronie głównej

W panelu administratora edytuj produkt i uzupełnij „Zdjęcie produktu”, np.
`img/snowboard1.jpg`. Plik musi znajdować się w `static/img/`; można też używać
podfolderów, np. `img/products/deska.jpg`. Nazwy bez spacji, obsługiwane rozszerzenia:
`jpg`, `jpeg`, `png`, `webp`. Pliki dodajemy do repozytorium razem ze zmianami.
Puste pole zachowuje dotychczasową ilustrację kategorii.

Ustaw „Kolejność na stronie głównej” (np. 1, 2, 3), aby wyróżnić ofertę.
Puste pole wyłącza wyróżnienie. Ekspozycja pod panoramą pokazuje maksymalnie trzy aktywne
produkty ze zdjęciem, według tej kolejności. Cena i odnośnik pochodzą z tej samej
oferty co w katalogu. Jeśli nie wybrano ofert, sekcja wybranych produktów jest pomijana.
Zdjęcie produktu jest wspólne dla strony głównej, katalogu i szczegółów.

Na start zdjęcia `snowboard1.jpg` i `narty.jpg` przypisano do fikcyjnych ofert
Drift 156 i Alpine 172 jako materiały zastępcze. Nie identyfikują one rzeczywistych
modeli pod tymi nazwami. `snowboard2.jpg` pozostaje nieprzypisany. Źródła i prawa
do zdjęć pobranych przez użytkownika nie zostały zweryfikowane.

### Panorama i kategorie

Na górze strony głównej pokazujemy cztery zdjęcia z `static/img/hero/`:
`panorama1.jpg` do `panorama4.jpg`. Można je zastąpić własnymi plikami o tych
samych nazwach; obecne mają około 1920 × 1080 px. Dostosowanie liczby zdjęć i ich
opisów wymaga aktualizacji `hero_slides` w `catalog/views.py`.

Pokaz zmienia zdjęcie co 6 sekund z łagodnym przejściem. Przyciski pozwalają
wybrać zdjęcie i wstrzymać pokaz. Automatyczna zmiana zatrzymuje się w ukrytej
karcie oraz podczas obsługi klawiaturą wewnątrz panoramy. Preferencja ograniczenia
ruchu wyłącza automatyczny start i przejścia; bez JavaScript widoczne jest pierwsze
zdjęcie, a menu kategorii działa normalnie.

Menu na zdjęciach prowadzi do filtrów: Narty, Snowboard, Wiązania, Kaski, Gogle,
Buty snowboardowe, Buty narciarskie. Kategorie są dostępne również w panelu
administratora. Techniczny identyfikator `boots` zachowano dla butów narciarskich;
dotychczasowe Akcesoria pozostają dostępne w katalogu, aby zachować istniejące dane.
Demonstracyjny Ridge M przeniesiono do Kasków. Puste kategorie nie otrzymują
automatycznie nowych produktów. Źródła i prawa do panoram dostarczonych przez
użytkownika nie zostały zweryfikowane.

- `config/` — ustawienia, adresy i uruchamianie aplikacji.
- `accounts/` — własny model użytkownika oparty na Django, przygotowany do dalszej rozbudowy.
- `catalog/` — produkty, widoki, panel administratora, migracje i testy.
- `templates/` — wspólna rama HTML i strony katalogu.
- `static/` — style i własne ilustracje SVG. Strona nie wymaga zewnętrznych fontów ani usług.

Ceny są przechowywane jako liczby dziesiętne, a `sale_stock` opisuje wyłącznie sztuki
na sprzedaż. Przyszłe egzemplarze wypożyczalni będą miały osobną ewidencję.
Produkty można ukryć bez usuwania ich z bazy. Uprawnienia panelu sprawdza backend Django.

## Podkategorie sprzętu

Wszystkie siedem kategorii głównych ma podmenu z półprzezroczystym, rozmytym tłem.
Narty mają 7 typów, deski snowboardowe 4, wiązania 4, kaski 3, gogle 4,
buty snowboardowe 3, a buty narciarskie 4. Definicje są wspólne dla interfejsu,
modelu i formularzy w `catalog/taxonomy.py`. Akcesoria pozostają bez podkategorii.

Panele otwierają się po najechaniu, kliknięciu albo Enter/Spacji. Escape zamyka panel,
a strzałka w dół przenosi fokus na pierwszy odnośnik. Jednocześnie otwarty jest tylko
jeden panel. Panel nakłada się na zdjęcie bez zmiany położenia kategorii, a przy
prawej krawędzi ekranu jest wyrównany do prawej. Bez JavaScript pozostają odnośniki
do katalogów poszczególnych kategorii.

W katalogu lista „Podkategoria” zawiera typy właściwe dla wybranej kategorii.
Zmiana kategorii czyści poprzedni wybór; dla Akcesoriów i wszystkich kategorii
pole jest ukryte. Filtr łączy się z wyszukiwaniem. „Wszystkie podkategorie” pokazuje
również wcześniejsze produkty bez ustalonego typu. Bez JavaScript zatwierdź kategorię
przyciskiem „Pokaż sprzęt”, aby odświeżyć opcje.

W panelu administratora podkategoria jest wymagana przy dodawaniu lub edycji
produktów z siedmiu kategorii głównych. Lista opcji zmienia się po wyborze kategorii.
Baza i formularze blokują nieznane lub niedopasowane typy. Dla Akcesoriów pole musi
być puste. Typ jest wyświetlany również w szczegółach produktu.

Po pobraniu zmian na drugim komputerze wykonaj:

```powershell
./.venv/Scripts/python manage.py migrate
```

Migracja zmienia nazwę pola `ski_subcategory` na wspólne `subcategory`, zachowując
dotychczasowe przypisania nart. Dotychczasowe odnośniki z parametrem `ski_subcategory`
nadal działają dla nart; nowe korzystają z `subcategory`. Alpine 172 i Drift 156 są
klasyfikowane tylko wtedy, gdy mają zachowane, jednoznaczne opisy demo. Innym produktom
nie zgadujemy typu — należy go uzupełnić w panelu. `seed_demo` zachowuje późniejsze edycje.

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
