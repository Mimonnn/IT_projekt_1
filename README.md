# Szron — sklep narciarski z wypożyczalnią

## Poradnik „Wybierz swoją trasę”

Na stronie głównej wybierz poziom: początkujący, średniozaawansowany lub zaawansowany.
Otwiera stronę z opisem umiejętności, doborem sprzętu i filtrem kategorii. Sekcja kupna
prowadzi do szczegółów produktu, koszyka i zamówienia; sekcja wypożyczenia do szczegółów
egzemplarza, wyboru dat i rezerwacji. Dostępność na termin sprawdzana jest po wybraniu dat.
Poradnik i oba procesy działają po polsku i angielsku.

Administrator edytuje pole **Poziomy zaawansowania** w produkcie. Model może należeć
do kilku poziomów lub nie być pokazywany w poradniku. Przypisania są w bazie, niezależnie
od ceny i magazynu sprzedaży. Egzemplarze do serwisu i niezwrócone wydania nie pojawiają
się w propozycjach wypożyczenia. Po pobraniu zmian na drugim komputerze wykonaj migracje:

```powershell
./.venv/Scripts/python.exe manage.py migrate
```

Migracje dodają poziomy i klasyfikują rozpoznane, niezmienione oferty demonstracyjne.
Nowe oferty demo otrzymują poziomy podczas `seed_demo`. Istniejące edycje zachowuje
także `--refresh-demo`; wyłącznie `seed_demo --refresh-skills` jawnie odtwarza przypisania
z JSON dla ofert o zgodnej kategorii, bez zmiany cen, stanów czy materiałów.

Lokalna aplikacja Django z PostgreSQL: sklep i wypożyczalnia sprzętu zimowego,
katalog PL/EN, konta klientów, koszyk, rezerwacje oraz wydania i zwroty obsługiwane
w panelu administratora. Działają również demonstracyjne zakupy z formularzem
dostawy i obsługą realizacji. „Szron” jest nazwą roboczą.

## Pobranie obecnej wersji na drugim komputerze

Jeśli masz już działającą kopię projektu, otwórz PowerShell w swoim folderze
z `manage.py`. Sprawdź `git status --short`: jeśli są lokalne zmiany, najpierw
zachowaj je i uzgodnij połączenie zmian; nie wykonuj resetowania plików.
Przy czystym katalogu wykonaj kolejno (przerwij, jeśli polecenie zwróci błąd):

```powershell
git pull --ff-only origin main
./.venv/Scripts/python -m pip install -r requirements.txt
./.venv/Scripts/python manage.py migrate
./.venv/Scripts/python manage.py seed_demo
./.venv/Scripts/python manage.py seed_rental_demo
./.venv/Scripts/python manage.py check
powershell -ExecutionPolicy Bypass -File ./start.ps1
```

Otwórz http://127.0.0.1:8000/ i odśwież przez Ctrl+F5. Własny `.env`, hasła,
ustawienia portu i bazę zachowaj lokalnie. Jeśli środowiska jeszcze nie ma,
wykonaj sekcję „Pierwsze uruchomienie na drugim komputerze” poniżej.

Repozytorium zawiera wszystkie zdjęcia, CSS, JavaScript, migracje i definicje
61 produktów demonstracyjnych. Migracje przypisują istniejącym ofertom demo
zdjęcia i wyróżnienie oraz kategorię Kaski; `seed_demo` tworzy brakujące produkty.
Na komputerze autora katalog nadal odpowiada tym danym: Drift 156 i Alpine 172
są wyróżnione. Każda z 29 podkategorii ma po 2 oferty; Akcesoria mają 3 pozycje. Odtworzenie tego zestawu
zapewnia ten sam układ i oferty. `seed_demo` nie nadpisuje własnych zmian produktów
ani nie usuwa dodatkowych ofert na drugim komputerze; takie różnice w bazie trzeba
uzgodnić oddzielnie. Nie przenosimy kont, haseł ani całych plików bazy przez GitHub.

Przed prezentacją sprawdź pokaz czterech panoram, wyróżnione narty i snowboard,
przejście do szczegółów oraz po 2 produkty w każdej z 29 podkategorii.
Kategorie główne zawierają sumę ofert swoich podkategorii, a Akcesoria mają 3 pozycje.
Jeśli masz wcześniejsze oferty demo i chcesz wczytać ich nowe ceny oraz zdjęcia,
wykonaj jednorazowo `manage.py seed_demo --refresh-demo` (szczegóły poniżej).

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
./.venv/Scripts/python manage.py seed_rental_demo
./.venv/Scripts/python manage.py createsuperuser
./start.ps1
```

`seed_demo` dodaje 61 fikcyjnych produktów: po 2 w każdej z 29 podkategorii i 3 akcesoria. Można uruchamiać je wielokrotnie:
nie duplikuje produktów ani nie nadpisuje późniejszych zmian ich ceny i stanu.
Każda oferta demo ma lokalne zdjęcie produktu referencyjnego. Nazwy są wymyślone,
a ceny pochodzą z ofert sprawdzonych 31.10.2026. Zestawienie znajduje się w
[CATALOG_SOURCES.md](CATALOG_SOURCES.md), a dane w `catalog/data/demo_products.json`.
Zdjęcia nie potwierdzają istnienia rzeczywistych modeli pod fikcyjnymi nazwami.

Jawne odświeżenie istniejących ofert demonstracyjnych:

```powershell
./.venv/Scripts/python manage.py seed_demo --refresh-demo
```

Ta opcja zmienia cenę, zdjęcie, opis, podkategorię, parametry i materiały znanych ofert demo, zachowując
nazwę, stan magazynowy, widoczność i kolejność wyróżnienia. Pomija oferty ze zmienioną
kategorią i nie rusza własnych produktów administratora. W zwykłej codziennej pracy
korzystaj z `seed_demo` bez tej opcji, aby zachować własne edycje cen i opisów.

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

Próbę prezentacji klienta i administratora można uruchomić osobno:

```powershell
./.venv/Scripts/python.exe manage.py test catalog.test_acceptance
```

Test tworzy lokalny serwer HTTP na losowym porcie `127.0.0.1` i używa osobnej bazy
testowej. Sprawdza prawdziwe żądania, sesje i CSRF w PL/EN: rejestrację, profil,
ulubione, zakup z odbiorem i kurierem, realizację przez administratora, rezerwację,
wydanie, zwrot do serwisu, historię po ponownym logowaniu i prywatność zamówień.
Nie zastępuje kontroli wizualnej w przeglądarce; JavaScript wymaga osobnego sprawdzenia.

## Język polski i angielski

W nagłówku sklepu i administracji są przyciski z flagami „Polski” / „English”.
Zmiana języka odbywa się standardowym formularzem Django z ochroną CSRF;
zachowuje bieżący adres i filtry. Wybór jest zapisany w ciasteczku przeglądarki
na rok, także po wylogowaniu. Język bazowy to polski; bez zapisanego wyboru Django
uwzględnia preferowany język przeglądarki. Nie zmieniamy adresów URL, identyfikatorów
kategorii, materiałów ani wartości rozmiaru przesyłanych w filtrach.

Przetłumaczono szablony, komunikaty, formularze, etykiety kategorii i podkategorii,
teksty JavaScript, informacje o sklepie i interfejs administratora. Kwoty nadal
są w PLN; zmiana języka nie przelicza cen ani rabatów. Nazwy modeli i nazwy własne
(np. ulice i miasta) pozostają niezmienione.

61 ofert demo ma angielskie opisy, konstrukcję, wymiary, zakres masy i rozmiary;
15 materiałów ma angielskie nazwy. Dane źródłowe po polsku pozostają w dotychczasowych
polach. Pola z końcówką `_en` można edytować w panelu administratora. Prezentacja
używa właściwości `display_*`; jeżeli własny produkt nie ma tłumaczenia, pokazuje
tekst źródłowy. Dodając własny produkt lub materiał, uzupełnij także wersję angielską.

Po pobraniu zmian na drugim komputerze wykonaj:

```powershell
./.venv/Scripts/python manage.py migrate
```

Migracja `0012` dodaje pola angielskie, a `0013` uzupełnia znane oferty demo
na podstawie zamrożonych danych. Sprawdza zgodność tekstu źródłowego dla każdego
pola i zachowuje własne edycje oraz istniejące angielskie treści. Na pustej bazie
`seed_demo` tworzy od razu obie wersje językowe. Zwykłe wywołanie nadal nie
nadpisuje późniejszych edycji. Jawne odświeżenie angielskich treści demo:

```powershell
./.venv/Scripts/python manage.py seed_demo --refresh-translations
```

Ta opcja zmienia wyłącznie angielskie treści znanych ofert i materiałów. Zachowuje
polskie opisy, ceny, rabaty, stany, zdjęcia i przypisania materiałów; pomija oferty
przeklasyfikowane do innej kategorii. `--refresh-specs` odświeża teraz parametry
i opisy w obu językach, a `--refresh-demo` pełny zestaw danych w obu językach.

Tłumaczenia interfejsu korzystają z `LocaleMiddleware`, `gettext` / `gettext_lazy`
oraz znaczników `{% translate %}` i `{% blocktranslate %}`. Źródło tłumaczeń jest
w `locale/en/LC_MESSAGES/django.po`, a skompilowany `django.mo` należy przechowywać
w Git razem z nim, aby druga kopia działała bez instalowania narzędzi tłumaczeniowych.
Po zmianach interfejsu, z zainstalowanym GNU gettext, wykonaj:

```powershell
./.venv/Scripts/python manage.py makemessages -l en --no-wrap --ignore .venv --ignore work
# Uzupełnij angielskie msgstr w django.po, następnie:
./.venv/Scripts/python manage.py compilemessages -l en --ignore .venv --ignore work
```

Nowe funkcje wypożyczalni przygotowujemy od początku w obu językach. Katalog,
formularze i koszyk nie wymagają zewnętrznego serwisu automatycznych tłumaczeń.

## Logowanie, konto klienta i koszyk

- Przycisk „Zaloguj się” prowadzi do `/zaloguj/`. Formularz służy klientom i administratorom: konto z `is_staff=True` po zwykłym logowaniu przechodzi do panelu administratora, a klient do swoich aktualnych zamówień. Powrót po logowaniu z karty produktu prowadzi z powrotem do produktu. Django sprawdza uprawnienia panelu niezależnie od nawigacji.
- „Utwórz konto” (`/zarejestruj/`) rejestruje zwykłego klienta i automatycznie go loguje. Nie umożliwia nadania sobie uprawnień administratora. Używa walidacji i haszowania haseł Django. Istniejące konta i ich hasła pozostają bez zmian; administratora nadal tworzy się przez `manage.py createsuperuser`.
- „Moje konto” otwiera zakładkę Zamówienia i rezerwacje: aktywne zakupy oraz rezerwacje/wypożyczenia. Historia pokazuje zakończone i anulowane rekordy. Osobna zakładka Moje wypożyczenia zachowuje pełną listę rezerwacji. Dane są prywatne i pozostają po ponownym zalogowaniu; ukrycie produktu nie usuwa historii.
- Zalogowany użytkownik dodaje produkt z jego strony szczegółów. Koszyk pozwala zmienić ilość, usunąć pozycję i zobaczyć sumę aktualnych cen. Dane należą do konta w PostgreSQL i pozostają po wylogowaniu. Każdy klient ma dostęp wyłącznie do własnego koszyka.
- Koszyk nie rezerwuje sztuk ani nie zmniejsza magazynu. Dodawanie i zmiany ilości sprawdzają stan w backendzie. Zmiana ceny lub dostępności w katalogu jest widoczna w koszyku; pozycja niedostępna zostaje oznaczona i można ją usunąć. Zakup uruchamia przycisk Przejdź do zamówienia; dopiero potwierdzenie zmniejsza stan sprzedaży.
- Wylogowanie i zmiany koszyka wymagają formularza POST z ochroną CSRF. Także `/admin/login/` wyświetla wspólny formularz logowania.

Na drugim komputerze po pobraniu tej zmiany wykonaj `manage.py migrate`:
migracja `accounts/0002_cartitem.py` tworzy tabelę koszyka. Konta i koszyki nie są
przesyłane przez GitHub; pozostają w lokalnej bazie danego komputera.

## Dane profilu, ulubione i zwroty

„Moje konto” zawiera dodatkowe zakładki: Dane profilu, Ulubione i Zwroty.
W danych profilu zalogowana osoba może zmienić lub wyczyścić imię, nazwisko,
adres e-mail i numer telefonu. Formularz sprawdza format e-maila i telefonu;
zapisuje wyłącznie te cztery pola na bieżącym koncie. Login, hasło i uprawnienia
nie są zmieniane przez ten formularz. E-mail jest obecnie danymi kontaktowymi,
nie loginem; serwis nie wysyła wiadomości weryfikacyjnych.

Produkty można zapisać w ulubionych z katalogu lub strony szczegółów. Lista
jest prywatna i pozostaje zapisana w bazie po wylogowaniu. Ten sam produkt
pojawia się na niej tylko raz. Ukryte oferty nie są wyświetlane; brak stanu
magazynowego nie blokuje zapisania ulubionego produktu. Zapisanie nie dodaje
produktu do koszyka i nie rezerwuje go. Usuwanie działa z własnej listy.

Zwroty mają obecnie zakładkę z pustym stanem i informacją o przyszłej obsłudze.
Zgłaszanie zwrotów zakupów pozostaje osobnym etapem po wdrożeniu
systemu zakupów. Nie utworzono fikcyjnych zgłoszeń ani formularza wysyłającego
zwroty bez istniejącego zakupu.

Po pobraniu zmian na drugim komputerze wykonaj `manage.py migrate`.
Migracja `accounts/0003_user_phone_favorite.py` dodaje telefon i tabelę ulubionych.
Dane osobowe i ulubione pozostają wyłącznie w lokalnej bazie i nie trafiają do Git.

## Informacje o sklepie

Stopka każdej strony prowadzi do `/regulamin/`, `/kontakt/` i `/sklepy/`.
Regulamin opisuje wersję demonstracyjną bez rzeczywistych zamówień i płatności.
Dane pomocy klienta i czterech sklepów są wspólne w `catalog/store_info.py`:
Gliwice, Katowice, Szczyrk oraz Białka Tatrzańska, z dwoma fikcyjnymi punktami
przy stokach. Adresy, godziny i kontakt oznaczono jako wymyślone. Adres pomocy
używa domeny `.example`, a telefon jest niedziałającym numerem demonstracyjnym.
Strona nie wysyła zgłoszeń ani wiadomości do obsługi.

## Promocje na stronie głównej

Pod panoramą, nad dotychczasową sekcją wyróżnionych ofert, znajdują się trzy karty
promocyjne: Alpine 172 (narty, −10%), Halo S3 (gogle, −15%) i Roam 500 (buty
snowboardowe, −20%). Przy cenach regularnych z zestawu demo ceny po obniżce wynoszą
odpowiednio 1529,10 zł, 212,49 zł i 471,99 zł. Karty pokazują rabat, przekreśloną
cenę regularną, nową cenę i oszczędność oraz prowadzą do produktu.

`Product.price` pozostaje ceną regularną, a `discount_percent` rabatem (0–99%;
0 wyłącza promocję). `selling_price` oblicza cenę po rabacie z zaokrągleniem do
groszy, a koszyk mnoży tak obliczoną cenę jednostkową przez ilość. Katalog,
ulubione, wyróżnione oferty, szczegóły i koszyk korzystają z tej samej ceny.
Zmiana lub wyłączenie rabatu jest widoczna także w już istniejącym koszyku.

Administrator może zmieniać rabat na formularzu produktu. Strona główna pokazuje
maksymalnie trzy aktywne, przecenione oferty z dodatnim stanem, w kolejności rabatu
rosnąco, następnie identyfikatora. Sekcja działa niezależnie od wyróżnienia ofert;
znika, jeżeli brak dostępnych promocji. Nowe rabaty są przykładem promocji Szron,
nie rabatami ze sklepów źródłowych ani historią najniższych cen.

Na drugim komputerze wykonaj `manage.py migrate`: migracja
`catalog/0011_product_discount_percent_and_more.py` doda rabat i ustawi trzy
promocje dla istniejących ofert demo o zgodnych kategoriach. Na pustej bazie
`seed_demo` odtwarza te rabaty z JSON. Zwykły seed i `--refresh-specs` zachowują
własne zmiany rabatów; jawne `--refresh-demo` odświeża również rabaty demo.

## Opisy, parametry i filtry produktów

Każda z 61 ofert demonstracyjnych ma rozbudowany opis, rozmiar, materiały,
opis konstrukcji, wymiary z jednostkami oraz masę w gramach. Pole „masa dotyczy”
wyjaśnia, czy chodzi np. o parę butów, deskę bez wiązań czy komplet śrub.
Parametry to przykładowe dane fikcyjnych modeli Szron i są tak oznaczone na stronie.
Źródła rzeczywistych cen i zdjęć nie potwierdzają tych wymyślonych specyfikacji.

W katalogu można jednocześnie wybrać kategorię, podkategorię, rozmiar i materiał
oraz wpisać wyszukiwaną frazę. Produkt może mieć kilka materiałów, np. drewno
i włókno szklane; pasuje do filtra każdego z nich. Rozmiary i materiały pochodzą
z aktywnych produktów danej grupy. JavaScript aktualizuje opcje po zmianie kategorii
lub typu i czyści poprzedni wybór; „Pokaż sprzęt” zatwierdza filtry. Bez JavaScript
najpierw zatwierdź kategorię, aby załadować właściwe opcje. „Wyczyść” usuwa filtry.

W panelu administratora edytuj pola parametrów produktu i przypisuj wiele materiałów.
Lista materiałów ma osobny ekran administracji. Masa jest opcjonalna dla nowych
własnych ofert, ale podana wartość musi być dodatnia. Oznaczenie „parametry
demonstracyjne” można wyłączyć po zastąpieniu przykładowych danych zweryfikowanymi.

Na istniejącej bazie, również na drugim komputerze, wczytaj nowe opisy i parametry:

```powershell
./.venv/Scripts/python manage.py migrate
./.venv/Scripts/python manage.py seed_demo --refresh-specs
```

Migracja `catalog/0010_material_product_construction_product_dimensions_and_more.py`
dodaje strukturę parametrów i tabelę materiałów. `--refresh-specs` odświeża opisy,
parametry i przypisania materiałów znanych ofert demo. Zachowuje ceny, zdjęcia,
nazwy, stany magazynowe, widoczność, wyróżnienia i podkategorie. Pomija oferty
przeniesione do innych kategorii oraz własne produkty administratora.
Zwykłe `seed_demo` nadal zachowuje istniejące edycje; na pustej bazie tworzy oferty
od razu z parametrami. `--refresh-demo` odświeża także parametry i materiały.

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

Pierwotne zdjęcia `snowboard1.jpg` i `narty.jpg` pozostają w repozytorium.
Odświeżony zestaw demo używa 32 zdjęć w `static/img/products/`, opisanych w
[CATALOG_SOURCES.md](CATALOG_SOURCES.md). `snowboard2.jpg` nadal jest nieprzypisany.
Każdą ofertę można później zilustrować własnym zdjęciem przez panel administratora.

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
- `accounts/` — konta, logowanie i rejestracja, zakładki profilu oraz zapisany w bazie koszyk.
- `catalog/` — produkty, widoki, panel administratora, migracje i testy.
- `rentals/` — osobne egzemplarze wypożyczalni, ich katalog, administracja i dane demo.
- `orders/` — formularz zakupu, zamówienia i pozycje, transakcyjny zapis oraz obsługa realizacji.
- `templates/` — wspólna rama HTML i strony katalogu.
- `static/` — style i własne ilustracje SVG. Strona nie wymaga zewnętrznych fontów ani usług.

Ceny są przechowywane jako liczby dziesiętne, a `sale_stock` opisuje wyłącznie sztuki
na sprzedaż. Egzemplarze `rentals.RentalItem` mają osobną ewidencję.
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


## Podstawa wypożyczalni

Zakładka **Wypożyczalnia** (`/wypozyczalnia/`) działa po polsku i angielsku.
Pokazuje poszczególne fizyczne egzemplarze sprzętu, ich rozmiary, stawki dobowe
i bieżące statusy: na stanie, wypożyczony lub do serwisu. Kategorię, model i rozmiar wybiera się z rozwijanych list.
Modele wynikają z widocznych egzemplarzy danej kategorii, a rozmiary dodatkowo
z wybranego modelu. Listy aktualizują się od razu po zmianie wyboru, bez duplikatów.
Bez JavaScript opcje odświeża przycisk „Pokaż sprzęt”. Ukryte egzemplarze i nieaktywne produkty
nie są publikowane. Notatki techniczne pozostają wyłącznie w administracji.

W panelu administratora otwórz **Wypożyczalnia → Egzemplarze do wypożyczenia**.
Każda sztuka ma unikalny numer ewidencyjny (wielkie litery, cyfry i myślniki),
powiązanie z produktem, własny rozmiar (także opcjonalnie po angielsku), dodatnią
stawkę za dobę w PLN, status i widoczność. Uprawnienia Django kontrolują odczyt
i edycję; samo `is_staff` nie nadaje praw do zarządzania egzemplarzami.
Powiązanego produktu nie można usunąć — można go ukryć.

Na drugim komputerze, po pobraniu zmian i aktywowaniu środowiska:

```powershell
./.venv/Scripts/python manage.py migrate
./.venv/Scripts/python manage.py seed_demo
./.venv/Scripts/python manage.py seed_rental_demo
```

Ostatnia komenda tworzy 10 demonstracyjnych egzemplarzy: 4 pary nart, 4 deski
i 2 kaski, w tym jeden egzemplarz do serwisu. Stawki 15–75 zł/dobę są fikcyjne.
Powtórne uruchomienie zachowuje wszystkie edycje istniejących egzemplarzy,
ich statusy i widoczność. Nie kopiuje lokalnej bazy ani kont i nie zmienia
cen, rabatów ani liczby sztuk na sprzedaż. Wymaga wcześniejszego `seed_demo`.

Rezerwacje i sprawdzanie terminów działają zgodnie z opisem poniżej. Wydania i zwroty działają zgodnie z opisem poniżej i automatycznie aktualizują
status egzemplarza; sama etykieta „na stanie” nie gwarantuje dostępności
w wybranym terminie — należy podać daty i potwierdzić rezerwację.


## Rezerwowanie sprzętu

Zdjęcie, nazwa i odnośnik **Zobacz szczegóły** prowadzą do publicznej karty
egzemplarza `/wypozyczalnia/<id>/`. Karta zawiera opis modelu, zdjęcie, materiały,
konstrukcję, wymiary i masę, a osobno rozmiar egzemplarza i jego stawkę dobową.
Opis i parametry są wspólne ze sprzedażą; nie trzeba ich wpisywać ponownie.
Przycisk **Zarezerwuj** pozostaje na liście i jest także w szczegółach, jeśli
sprzęt jest dostępny. Wybrane daty są przekazywane dalej, a powrót zachowuje
filtry katalogu. W szczegółach można ponownie sprawdzić cenę i dostępność
na inne daty. Czytanie nie wymaga logowania; potwierdzenie rezerwacji wymaga konta.

1. W **Wypożyczalni** wybierz kategorię, model, rozmiar oraz daty odbioru i zwrotu.
2. Kliknij **Pokaż sprzęt**. Po podaniu poprawnych dat lista zawiera wyłącznie
   egzemplarze na stanie bez kolidujących rezerwacji i pokazuje cenę całego okresu.
3. Wybierz **Zarezerwuj**. Zaloguj się, jeżeli trzeba, sprawdź termin i koszt,
   a następnie kliknij **Potwierdź rezerwację**. Możesz też najpierw wejść
   w wybrany egzemplarz i sprawdzić daty przyciskiem **Sprawdź cenę i dostępność**.
4. Rezerwacja jest widoczna w **Moje konto → Moje wypożyczenia**.
   Anulowanie jest możliwe do dnia odbioru włącznie i zwalnia termin.

Liczymy oba dni: od 10 do 12 listopada to 3 dni, a odbiór i zwrot tego samego
dnia to 1 dzień. Po zwrocie 12 listopada następna rezerwacja może zaczynać się
13 listopada. Daty w przeszłości i odwrócony zakres są odrzucane. Nie pobieramy
płatności online; są to demonstracyjne rezerwacje projektu.

Podsumowanie przed potwierdzeniem pokazuje dokładne daty. Zmiana dat w formularzu
blokuje przycisk potwierdzenia do ponownego sprawdzenia ceny i dostępności.
Bez JavaScript potwierdzenie dotyczy dat wyraźnie pokazanych w podsumowaniu.

Rezerwacja dotyczy konkretnego `RentalItem`. Cena dobowa, nazwa i rozmiar są
kopiowane przy zapisie; późniejsze zmiany cennika i katalogu nie zmieniają historii.
Serwer ponownie sprawdza dostępność i stawkę przy potwierdzeniu. Jeżeli stawka
się zmieniła, trzeba ponownie sprawdzić cenę. Powtórzenie tego samego potwierdzenia
nie tworzy drugiej identycznej aktywnej rezerwacji tego klienta.

Zapis i anulowanie działają w transakcji z blokadą wiersza egzemplarza PostgreSQL.
Chroni to przed jednoczesnym rezerwowaniem tego samego terminu przez dwa konta.
Wszystkie przyszłe zapisy rezerwacji muszą korzystać z `rentals.services`;
zwykłe ręczne zapisy ORM/SQL nie zapewniają kontroli kolizji. Ograniczenia bazy
pilnują kolejności dat, dodatniej stawki i dozwolonych statusów. Potwierdzenie
rezerwacji nie zmniejsza `sale_stock` i nie zmienia statusu sprzętu na wypożyczony.

Administrator widzi rezerwacje w **Wypożyczalnia → Rezerwacje**.
Historia jest tylko do odczytu; uprawnienie zmiany rezerwacji pozwala użyć akcji
**Anuluj zaznaczone rezerwacje**, z tym samym ograniczeniem terminu anulowania.
Rezerwacji nie usuwa się z panelu. Egzemplarze i konta z historią są chronione
przed usunięciem. Zmiana stanu sprzętu na „do serwisu” blokuje nowe rezerwacje,
ale nie anuluje istniejących — wymagają osobnego rozpatrzenia przez obsługę.

Na drugim komputerze po pobraniu kodu uruchom `manage.py migrate`.
Migracja `rentals/0002_reservation.py` tworzy tabelę; nie dodaje przykładowych
rezerwacji ani kont. Nie potrzeba nowych zależności ani ponownego odświeżania
katalogu. Wydanie i potwierdzenie faktycznego zwrotu opisano w kolejnym rozdziale.


## Wydawanie i przyjmowanie zwrotów

W panelu **Wypożyczalnia → Rezerwacje** zaznacz rezerwację i wybierz akcję:

- **Wydaj sprzęt z zaznaczonych rezerwacji** — zmienia rezerwację na
  „Wypożyczony”, a egzemplarz na „Wypożyczony”. Zapisuje datę i pracownika.
- **Przyjmij zwrot — sprzęt na stan** — kończy wypożyczenie statusem „Zwrócono”
  i przywraca egzemplarz na stan.
- **Przyjmij zwrot — sprzęt do serwisu** — kończy wypożyczenie i blokuje
  egzemplarz do czasu serwisu. Uwagi zapisz w wewnętrznych notatkach egzemplarza.

Wydanie jest możliwe tylko dla potwierdzonej rezerwacji w jej okresie, gdy sprzęt
jest na stanie, widoczny i nie ma innego blokującego wypożyczenia/rezerwacji.
Zwrot przyjmuje się tylko dla wydanego sprzętu; może nastąpić wcześniej lub później
niż planowano. Faktyczne daty i obsługujących pracowników zapisuje serwer.
Każdy zaznaczony rekord jest sprawdzany osobno; przy błędnym stanie panel pokazuje
komunikat, a ten rekord pozostaje bez zmian.

Operacje wymagają aktywnego konta `is_staff` oraz obu uprawnień:
`rentals.change_reservation` i `rentals.change_rentalitem` (superadministrator
ma je domyślnie). Sam dostęp do panelu lub odczyt rezerwacji nie wystarcza.
Historia pozostaje tylko do odczytu, zmiany wymagają POST i CSRF.
Podczas trwającego wypożyczenia status i dane identyfikujące egzemplarz są
w jego formularzu tylko do odczytu — należy użyć akcji zwrotu.

Klient w **Moje konto → Moje wypożyczenia** widzi status oraz daty faktycznego
wydania i zwrotu. Po wydaniu nie może anulować rezerwacji. Gdy minie termin
zwrotu, widzi komunikat o opóźnieniu. Niezwrócony sprzęt nadal blokuje nowe
rezerwacje, również na dalsze terminy. Cena nie jest automatycznie zmieniana
przy wcześniejszym ani opóźnionym zwrocie; dopłat i rozliczeń jeszcze nie ma.

Wszystkie operacje przechodzą przez `rentals.services`, w transakcji blokującej
najpierw egzemplarz, potem rezerwację. Powtórzone wydanie lub identyczny zwrot
nie zmienia dat pierwotnej operacji. Próba zmiany wyniku już zapisanego zwrotu
jest odrzucana; dalszy serwis obsługuje się w ewidencji egzemplarzy.
PostgreSQL dodatkowo blokuje dwa niezwrócone wydania jednego egzemplarza oraz
niespójne statusy, daty i dane pracowników. Magazyn sprzedaży pozostaje niezależny.

Na drugim komputerze po pobraniu uruchom `manage.py migrate`:
`rentals/0003_remove_reservation_reservation_status_valid_and_more.py`
dodaje historię operacji, nowe statusy i ograniczenia. Zachowuje dotychczasowe
rezerwacje; nie tworzy kont ani demonstracyjnych wydań. Nowe zależności nie są wymagane.


## Zakupy i widoczność rezerwacji na koncie

Rezerwacje nie trafiały wcześniej na domyślny ekran Aktualne zamówienia,
który był pustym szablonem. Teraz zakładka **Zamówienia i rezerwacje** pokazuje
aktywne zakupy i wypożyczenia. Po zakończeniu/anulowaniu rekordy są w historii;
pełna lista rezerwacji pozostaje także w **Moich wypożyczeniach**.
Dodano ochronę przed nieaktualną zawartością prywatnych ekranów (`never_cache`).
GitHub nadal nie synchronizuje lokalnych baz: konta, zamówienia i rezerwacje
utworzone na jednym komputerze nie pojawiają się automatycznie na drugim.

Aby kupić produkt w wersji demonstracyjnej:

1. Zaloguj się, dodaj produkty do koszyka i wybierz **Przejdź do zamówienia**.
2. Wypełnij dane kontaktowe. Wybierz darmowy odbiór w jednym z 4 salonów
   lub kuriera za pobraniem (demonstracyjny koszt 19,99 zł, dostawa w Polsce).
3. Dla kuriera podaj ulicę, kod pocztowy i miejscowość; dla odbioru wybierz sklep.
4. Sprawdź podsumowanie i potwierdź zamówienie demonstracyjne.
5. Zobacz zapisane pozycje, cenę i postęp realizacji na koncie.

Nie ma bramki płatniczej, wysyłania e-maili ani rzeczywistej dostawy. Dane formularza
są zapisywane wyłącznie w lokalnym zamówieniu i nie nadpisują profilu. Interfejs
ma układ dwóch kolumn na komputerze i jednej na mniejszym ekranie; podsumowanie
pokazuje produkty, dostawę i sumę. Przełączenie dostawy przelicza kwoty w groszach;
backend zawsze samodzielnie waliduje dane, ceny, podpis podsumowania i dostępność.

Zapis zakupu jest atomowy: blokuje konto i produkty, utrwala kopie nazw/rozmiarów/cen,
zmniejsza magazyn sprzedaży i czyści własny koszyk. Ponowne potwierdzenie tego samego
tokenu nie tworzy duplikatu ani nie usuwa później dodanych produktów. Zmiana koszyka,
ceny lub wariantu po otwarciu formularza wymaga ponownego potwierdzenia. Nie można
sprzedać tej samej ostatniej sztuki dwóm klientom. Wypożyczalnia ma niezależne zasoby.

Administrator otwiera **Zakupy → Zamówienia zakupu**. Historia jest tylko do odczytu;
akcje prowadzą przez: przyjęte → przygotowanie → gotowe do odbioru / wysłane →
zrealizowane. Wymagają uprawnień `orders.change_order` i `catalog.change_product`.
Klient może anulować własne nowe zamówienie; obsługa także przygotowywane/gotowe do
odbioru. Anulowanie przywraca produkty na stan tylko raz. Wysłanego/zakończonego
zamówienia nie można anulować; zwroty zakupów pozostają osobnym przyszłym etapem.

Na drugim komputerze po pobraniu kodu wykonaj:

```powershell
./.venv/Scripts/python.exe manage.py migrate
```

Migracja `orders/0001_initial.py` tworzy tabele zakupów, bez dodawania przykładowych
zamówień. Nowe zależności nie są wymagane. Kod, migracje i tłumaczenia synchronizuje
Git; danych kont i zamówień nie publikujemy w repozytorium.
