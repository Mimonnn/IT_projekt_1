# Kontekst projektu

Ostatnia aktualizacja: 2026-10-22.

## Cel i ustalenia

Projekt to strona sklepu narciarskiego z możliwością kupowania i wypożyczania sprzętu zimowego. Ma obejmować działający frontend, backend oraz bazę danych uruchamianą lokalnie na komputerze jednego z autorów. Dane widoczne na stronie, w tym liczby dostępnych produktów, mają pochodzić z bazy.

Praca odbywa się w VS Code z rozszerzeniem Codex na dwóch komputerach, z wykorzystaniem wspólnego repozytorium GitHub. Pliki `AGENTS.md`, `PROJECT_CONTEXT.md` i `TODO.md` utrzymują kontekst między komputerami i nowymi rozmowami.

## Uzgodniony zakres funkcjonalny

- Wspólny katalog sprzętu, konta klientów i panel administratora.
- Klient: rejestracja, logowanie, przeglądanie i filtrowanie katalogu, koszyk oraz składanie zamówień na zakup.
- Wypożyczanie: osobna rezerwacja z wyborem dat, sprawdzanie dostępności i historia własnych wypożyczeń.
- Dobór lub filtrowanie sprzętu według parametrów fizycznych, takich jak wzrost i waga, oraz poziomu zaawansowania.
- Administrator: zarządzanie użytkownikami, katalogiem, cenami, stanami magazynowymi, egzemplarzami sprzętu, rezerwacjami, wydaniami i zwrotami.
- Ewidencja stanu technicznego, w tym oznaczanie sprzętu do serwisu, oraz podstawowe raporty eksploatacyjne i finansowe.

## Decyzje dotyczące organizacji danych i pracy

- Zasoby na sprzedaż i egzemplarze do wypożyczenia są rozdzielone. Ten sam model sprzętu może być oferowany w obu formach, jeśli ma odpowiednie zasoby.
- Wybrany stos: Python, Django 5.2 LTS, PostgreSQL oraz HTML i CSS; JavaScript w miarę potrzeb. Django generuje frontend za pomocą szablonów, w jednym projekcie z backendem.
- „Szron” to robocza nazwa sklepu. Pierwszy wygląd wykorzystuje ciemną zieleń, jasne tło, limonkowy akcent oraz własne ilustracje SVG.
- Sprzedaż aktualizuje stan magazynowy. Wypożyczanie uwzględnia terminy, nakładające się rezerwacje, wydania, zwroty i stan techniczny egzemplarza.
- Projekt rozwijamy małymi, działającymi fragmentami obejmującymi bazę, backend i frontend. Ustalonym pierwszym kamieniem milowym jest wyświetlenie na stronie produktów odczytanych z lokalnej bazy danych.
- Kontekst sprawdzamy i aktualizujemy przy każdym commicie zgodnie z `AGENTS.md`.
- `TODO.md` początkowo pozostaje pusty. Pod koniec sesji zapisujemy w nim uzgodnione pomysły i zadania na następny raz.

## Aktualny postęp

- Wszystkie siedem głównych kategorii ma podkategorie w jednym polu `Product.subcategory`: 7 typów nart, 4 desek snowboardowych, 4 wiązań, 3 kasków, 4 gogli, 3 butów snowboardowych i 4 butów narciarskich. Wspólne definicje są w `catalog/taxonomy.py`. Menu na panoramie rozwija odnośniki, filtr katalogu i lista w panelu administratora zmieniają opcje zgodnie z kategorią, a szczegóły produktu pokazują nazwę typu.

- Strona główna ma pełną szerokość panoramy z czterema zdjęciami użytkownika, pokazem co 6 sekund i menu siedmiu kategorii. Pod panoramą pozostają wybrane oferty. Kategorie rozszerzono o wiązania, kaski, gogle i buty snowboardowe; zachowano `boots` dla butów narciarskich i dotychczasowe Akcesoria.

- Działa szkielet Django: `config` (konfiguracja), `accounts` (model użytkownika oparty na `AbstractUser`) i `catalog` (produkty i ich obsługa).
- Działa połączenie z lokalnym PostgreSQL, migracje i komenda `seed_demo`, dodająca cztery fikcyjne produkty bez nadpisywania późniejszych zmian.
- Działa strona główna, katalog, wyszukiwanie po nazwie i opisie, filtrowanie kategorii oraz szczegóły produktu. Ceny i stany sprzedażowe są odczytywane z bazy. Układ ma reguły CSS dla komputerów i telefonów.
- Administrator może dodawać, edytować i ukrywać produkty przez panel Django. Pola produktu: nazwa, unikalny adres, kategoria, opis, cena, liczba sztuk na sprzedaż i widoczność. Cena i stan są zabezpieczone przed wartościami ujemnymi.
- Dostęp do zarządzania kontroluje Django. Przyszłe konta klientów korzystają z własnego modelu użytkownika; rejestracja i interfejs logowania klientów pozostają kolejnymi etapami.
- Przygotowano instrukcję uruchomienia i odtworzenia środowiska na drugim komputerze w `README.md`, `.env.example`, przypięte wersje głównych zależności i skrypt `start.ps1`.
- `TODO.md` pozostaje pusty zgodnie z ustaleniami.

## Lokalne środowisko i uruchamianie

- Pierwszy komputer korzystał z Pythona 3.12.4 i przenośnego PostgreSQL 18.6 w ignorowanym `work/`, na porcie 55432. Na drugim komputerze przygotowano `.venv` z Pythonem 3.14.4, zależności z `requirements.txt`, ignorowany `.env` i bazę na zainstalowanym PostgreSQL 18.4 pod `127.0.0.1:5432`. Migracje i `seed_demo` wykonano pomyślnie; `pip check` przeszedł. Python 3.14 jest wspierany przez używaną wersję Django.
- `start.ps1` uruchamia przygotowaną bazę, jeśli jest zatrzymana, oraz stronę pod `http://127.0.0.1:8000/`. Na drugim komputerze można użyć zwykłej instalacji PostgreSQL i portu z własnego `.env`.
- Nie utworzono stałego konta administratora strony. Użytkownik tworzy je przez `manage.py createsuperuser`, samodzielnie podając dane. Testy korzystają z tymczasowych kont w osobnej bazie.
- Środowisko, pliki bazy i sekrety nie są współdzielone przez Git. Drugi komputer odtwarza bazę przez migracje i `seed_demo`.
- Zakupy i rezerwacje nie mają jeszcze aktywnych przycisków; interfejs oznacza je jako kolejne etapy. Egzemplarze wypożyczalni będą miały osobną ewidencję od stanu sprzedażowego.

## Problemy i kwestie organizacyjne

- W zgłoszeniu do wykładowcy opisano wypożyczalnię; później w rozmowie rozszerzono zakres o sprzedaż. Potwierdzenie tego rozszerzenia u wykładowcy pozostaje kwestią do ustalenia.
- Kontekst trafia na drugi komputer przez wysłanie i pobranie zmian w GitHub; nie synchronizuje się samą zmianą rozmowy.

## Ostatnia zmiana i weryfikacja

### 2026-10-22 — zatwierdzenie podkategorii

- Na polecenie użytkownika przygotowano wspólny commit podkategorii wszystkich siedmiu kategorii: modele, migracje 0006–0009, formularze administratora, filtry, szklane panele menu, testy i dokumentację.
- Ostatnia kontrola: 35 testów na PostgreSQL poprawnych, kompletne migracje, poprawna konfiguracja Django, zależności i składnia JavaScript; szczegóły audytu poniżej. Przed zatwierdzeniem ponownie sprawdzono zakres zmian i `git diff --check`.
- AGENTS.md i kontekst są aktualne; TODO.md pozostaje pusty. Pliki lokalnego środowiska i sekrety są ignorowane. Użytkownik zlecił sam commit, bez wysyłania na GitHub. Po pobraniu tego commita na drugim komputerze trzeba wykonać `manage.py migrate`.

### 2026-10-22 — kontrola przed commitem

- Przejrzano cały zakres zmian, nowe pliki, migracje, formularze i obsługę frontendu. Poprawiono adres skryptu w `ProductAdmin.Media`: parametr wersji jest dodawany do gotowego adresu statycznego, ponieważ wpisanie go w nazwie pliku powodowało kodowanie `?` i błędny adres zasobu.
- Kontrola edycji wyróżnienia z listy administratora ujawniła błąd dla wcześniejszych produktów bez podkategorii. Walidację pola przeniesiono do `clean_fields`, z obsługą `exclude` i łączeniem błędów: zmiana samej kolejności działa, a pełna edycja i dodawanie nadal wymagają poprawnego typu. Dodano dwa testy regresji.
- Wszystkie 35 testów na PostgreSQL przeszło. `manage.py check`, `makemigrations --check --dry-run`, `migrate --check` i `pip check` poprawne. Sprawdzono składnię trzech skryptów JavaScript przez Node oraz odpowiedzi HTTP 200 ich właściwych adresów i arkusza panelu.
- Sprawdzono pliki śledzone i nowe nieignorowane: brak `.env`, środowiska, katalogu roboczego lub plików bazy. Skan typowych tokenów/kluczy i porównanie z lokalnymi wartościami sekretów nie wykazały ich obecności w plikach do commita. `git diff --check` poprawne; komunikaty LF/CRLF są ostrzeżeniami o końcach linii.
- AGENTS.md przejrzano; TODO.md pozostaje pusty. Zmiany są gotowe do zatwierdzenia łącznie z nowymi plikami i migracjami 0006–0009. Na drugim komputerze po pobraniu potrzebne jest `manage.py migrate`. Nie wykonano commita ani wysyłania do GitHub. Weryfikacja wizualna ekranów komputera pozostaje opisana poniżej; widoku telefonu i osobnego testu najechania nadal nie wykonano.

### 2026-10-22 — podkategorie pozostałych kategorii

- Rozszerzono identyczny wzór panelu nart na Snowboard, Wiązania, Kaski, Gogle, Buty snowboardowe i Buty narciarskie. Nazwy są zgodne z listą użytkownika, bez opisów przeznaczenia. Wiązania mają cztery pozycje rozróżniające sprzęt: narciarskie zjazdowe, narciarskie skiturowe, snowboardowe paskowe i snowboardowe z szybkim wpinaniem. Zachowano efekt zaparowanej szyby i strzałkę w prawo. Wspólne pliki CSS/JS zachowują historyczne nazwy `ski-menu`.
- Zamiast oddzielnych pól dla kategorii zastosowano wspólne `Product.subcategory` i definicje w `catalog/taxonomy.py`. Migracja `0008` usuwa stare ograniczenie, zmienia nazwę kolumny przez `RenameField` bez utraty przypisań nart, powiększa pole i dodaje ograniczenie poprawnych par kategoria/typ. Migracja `0009` przypisuje All-mountain tylko znanej ofercie Drift 156 z zachowanym opisem demo. Migracje wykonano lokalnie. Istniejące inne produkty zachowują pusty typ do uzupełnienia w panelu; walidacja wymaga klasyfikacji przy dodawaniu i edycji.
- Nowe odnośniki używają `subcategory`; backend zachowuje obsługę starych parametrów `ski_subcategory` dla nart. W katalogu jeden filtr pobiera opcje wybranej kategorii, czyści poprzedni wybór przy zmianie kategorii i łączy się z wyszukiwaniem. Akcesoria pozostają bez podkategorii.
- Formularz administratora i jego JavaScript pokazują właściwe opcje na podstawie kategorii. Lista produktów ma wspólny filtr podkategorii z nazwą kategorii, żeby identyczne nazwy typów nie mieszały różnych sprzętów. Szczegóły produktu pokazują etykietę z właściwej kategorii.
- Otwieranie panelu zamyka pozostałe panele. Przyciski mają unikalne powiązania z panelami, a panele przy prawej krawędzi są wyrównywane do prawej. Zmieniono wersje CSS i JavaScript.
- Wszystkie 33 testy na PostgreSQL przeszły, w tym testy wszystkich 29 typów i ich odnośników, filtrowania, poprawnych i błędnych par, formularzy administratora, starych adresów i zachowania danych w migracji. `manage.py check` oraz `makemigrations --check --dry-run` poprawne.
- W przeglądarce na porcie 8000 kolejno otwarto klawiaturą siedem paneli: zawsze dokładnie jeden widoczny, wszystkie w granicach ekranu, współrzędne i wymiary wszystkich głównych kategorii identyczne przed i po otwarciu. Potwierdzono przejście ze Snowboard → All-mountain do Drift 156 i poprawne opcje filtra wszystkich kategorii, wraz z czyszczeniem wartości i ukrywaniem dla Akcesoriów. Widoku telefonu i najechania kursorem nie sprawdzono osobno.
- Zaktualizowano README i AGENTS.md. TODO.md pozostaje pusty. Bez commita i wysyłania do GitHub.

### 2026-10-22 — szklane tło podmenu

- Panel podkategorii ma półprzezroczyste przyciemnienie `rgba(15, 34, 39, .68)` oraz rozmycie tła `backdrop-filter: blur(18px) saturate(.85)`, także z prefiksem dla Safari. Rozmywa się wyłącznie panorama pod panelem, a nie tekst. Jasne napisy mają delikatny cień; przeglądarki bez obsługi rozmycia otrzymują mocniej przyciemnione tło dla czytelności.
- Zwiększono wersję arkusza menu do 3. W przeglądarce na porcie 8000 sprawdzono wygląd otwartego panelu oraz rzeczywiście zastosowane wartości półprzezroczystości i rozmycia. To zmiana CSS bez zmian układu, JavaScript i bazy; nie uruchamiano ponownie testów backendu. TODO.md pozostaje pusty, bez commita i wysyłania do GitHub.

### 2026-10-22 — usunięcie rozwijania paska przez podmenu

- Po ponownym zgłoszeniu użytkownika zmieniono konstrukcję: usunięto `details/summary`. Narty są zwykłym przyciskiem z `aria-expanded` i `aria-controls`, a osobny panel otwiera się przez zmianę `hidden`. Krytyczne pozycjonowanie absolutne panelu jest zapisane także bezpośrednio w HTML, więc nawet brak arkusza menu nie wprowadzi podkategorii do układu nawigacji. Pasek wyrównuje elementy do góry zamiast centrować je względem wysokości rozwiniętej zawartości.
- Obsługa JavaScript zachowuje najechanie, kliknięcie, Enter/Spację, Escape i zamknięcie po wyjściu poza menu. Strzałka w dół przenosi fokus na pierwszy odnośnik. Bez JavaScript dostępny jest odnośnik do wszystkich nart. Zaktualizowano wersje CSS i JS oraz README.
- W przeglądarce na `127.0.0.1:8000` potwierdzono otwarcie nowego panelu klawiszem Enter. Dla wszystkich siedmiu głównych kategorii porównano współrzędne i wymiary przed otwarciem i po nim: zmiana położenia pionowego wyniosła 0 pikseli w każdym przypadku; szerokości i wysokości też były identyczne. Próba ruchu kursora przez przeciągnięcie nie otworzyła menu, dlatego nie traktujemy jej jako potwierdzenia obsługi najechania w przeglądarce.
- Jest to poprawka struktury frontendu; baza pozostaje bez zmian. TODO.md nadal pusty. Bez commita i wysyłania do GitHub.

### 2026-10-22 — poprawne ładowanie stylów panelu

- Użytkownik pokazał nadal rozciągnięty pasek i widoczny znacznik natywny. Zrzut odpowiada brakowi nowych stylów menu, mimo że działający serwer na porcie 8000 zwracał aktualny HTML i CSS. Nie odczytywano pamięci podręcznej przeglądarki użytkownika, więc jej udział jest wnioskiem z objawów.
- Przeniesiono reguły panelu do osobnego `static/css/ski-menu.css`, ładowanego w bloku `extra_styles` strony głównej. Nadano wersjonowane adresy obu arkuszom, aby odświeżenie strony pobrało aktualny zestaw. AGENTS.md opisuje aktualizowanie tych wersji przy kolejnych zmianach CSS.
- Tym razem weryfikację przeglądarkową wykonano na działającej stronie `127.0.0.1:8000`. Potwierdzono załadowanie obu nowych adresów CSS, ciemne tło panelu i pozycjonowanie absolutne. Porównano położenie i rozmiary wszystkich głównych kategorii przed otwarciem i po otwarciu klawiaturą: pozostały identyczne. Sprawdzono zrzut z pojedynczą strzałką w prawo i osobnym panelem. Pozostawiono działający serwer użytkownika.
- Bez zmian bazy, commita i wysyłania do GitHub. TODO.md pozostaje pusty.

### 2026-10-22 — nieruchoma etykieta i panel podkategorii

- Usunięto dodatkową strzałkę w dół za „Narty”. Przed napisem pozostaje pojedyncza, stała strzałka w prawo; domyślny znacznik przeglądarki jest ukryty.
- Podmenu jest osobnym, ciemnozielonym panelem z odnośnikami, cieniem i zaokrąglonym dołem, inspirowanym przykładem użytkownika. Pozycjonowanie panelu jest absolutne. Kontener oraz etykieta mają stałe wymiary, dzięki czemu otwarcie nie przestawia kategorii ani nie zmienia wysokości paska. Usunięto zmianę tła i podkreślenia etykiety przy najechaniu; zachowano obramowanie fokusu dla klawiatury.
- W przeglądarce porównano geometrię etykiety i paska przed otwarciem oraz po otwarciu klawiszem Enter: pozycja, szerokość, wysokość i wysokość nawigacji były identyczne. Sprawdzono wygląd panelu na ekranie komputera. Obsługa najechania pozostaje w istniejącym JavaScript; w tej kontroli nie symulowano osobno ruchu myszki ani telefonu.
- Zmiana dotyczy wyłącznie prezentacji menu i kontekstu; bez zmian bazy. TODO.md pozostaje pusty. Bez commita i wysyłania do GitHub.

### 2026-10-22 — podkategorie nart

- Dodano siedem wartości `SkiSubcategory` i pole `ski_subcategory`. Walidacja formularzy wymaga wybrania typu nart i odrzuca go dla innych kategorii. Ograniczenie PostgreSQL blokuje nieznane wartości i niezgodne kategorie. Dla kompatybilności baza dopuszcza pusty typ przy dotychczasowych nartach; trzeba go uzupełnić podczas edycji w panelu. Pozostałym produktom nie nadano domyślnej podkategorii.
- Migracje `0006` i `0007` dodają pole, ograniczenie oraz klasyfikują tylko ofertę demo Alpine 172 z zachowanym opisem nart trasowych. `seed_demo` ustawia typ wyłącznie nowo tworzonym nartom demo, bez nadpisywania późniejszych edycji. Migracje wykonano na lokalnym PostgreSQL.
- Menu na stronie głównej używa `details/summary`: najechanie myszką otwiera podmenu, kliknięcie lub klawiatura obsługuje rozwijanie, Escape zamyka. Widoczne są same nazwy, bez opisów przeznaczenia. Bez JavaScript pozostaje natywne rozwijanie kliknięciem lub klawiaturą.
- Filtr katalogu jest pokazywany od razu po wyborze „Narty”; przy zmianie na inną kategorię jest ukrywany, czyszczony i wyłączany. Backend ignoruje podkategorię poza kategorią nart. Puste pole oznacza wszystkie narty, również dotychczasowe bez klasyfikacji; nieznana podkategoria daje pusty wynik. Bez JavaScript najpierw zatwierdza się kategorię przyciskiem formularza.
- Wszystkie 25 testów na PostgreSQL przeszło, w tym nowe testy filtrowania, walidacji modelu i bazy, odnośników, edycji w panelu i zachowania zmian danych demo. `makemigrations --check --dry-run` nie wykazało brakujących migracji; kontrola Django poprawna.
- W przeglądarce potwierdzono rozwinięcie menu klawiszem Enter, widoczność siedmiu nazw, przejście do nart trasowych z Alpine 172, ukrycie pola po wyborze Snowboardów i pusty wynik dla Freeride. Formularz nie powoduje poziomego przewijania na sprawdzonym ekranie komputera. Widoku telefonu i najechania myszką nie sprawdzono osobno w przeglądarce.
- README uzupełniono o obsługę i migracje. AGENTS.md przejrzano; zasady pozostają aktualne. TODO.md pozostaje pusty. Nie wykonano commita ani wysyłania do GitHub.

### 2026-10-21 — przygotowanie wspólnej wersji do prezentacji

- Użytkownik zlecił zatwierdzenie i wysłanie obecnego stanu na GitHub, aby kolega pobrał go na prezentację 22.10.2026. Zakres obejmuje wcześniejsze zmiany katalogu i strony głównej, wszystkie siedem plików JPG, migracje, JavaScript oraz dokumentację.
- README zawiera instrukcję aktualizacji istniejącej kopii: sprawdzenie zmian lokalnych, pobranie `main`, instalacja zależności, migracje, `seed_demo`, kontrola Django i start PowerShell. Poprawiono opis obu lokalnych środowisk i listę obsługiwanych wersji Pythona.
- Sprawdzono publiczne dane czterech produktów w lokalnej bazie: ceny, stany, kategorie, zdjęcia i wyróżnienie odpowiadają definicjom demo. Git nie przenosi baz i kont; migracje oraz `seed_demo` odtwarzają ten zestaw. Ewentualne własne zmiany katalogu u kolegi pozostają zachowane i mogą wymagać osobnego uzgodnienia.
- Weryfikacja 21.10: wszystkie 15 testów na osobnej bazie PostgreSQL przeszło, `manage.py check`, `makemigrations --check --dry-run` i `pip check` poprawne. Po `git fetch origin` lokalny HEAD i `origin/main` były zgodne przed nowym commitem. Kontrole przeglądarkowe pozostają opisane przy zmianach z 18.10; nie wykonywano ich ponownie w tej sesji.
- Przed commitem przejrzano AGENTS.md (bez potrzeby zmiany zasad), niniejszy kontekst i pusty TODO.md. Nie uzgodniono nowych zadań. Sekrety i środowisko pozostają ignorowane.

### 2026-10-18 — panorama i menu kategorii

- Użytkownik dostarczył cztery panoramy w `static/img/hero/` i uzgodnił siedem pozycji menu: Narty, Snowboard, Wiązania, Kaski, Gogle, Buty snowboardowe, Buty narciarskie. Na pełnej szerokości strony, pod głównym nagłówkiem nawigacji, wyświetla się panorama z menu na tle zdjęcia. Wybrane produkty pozostają poniżej.
- Pokaz w czystym JavaScript zmienia zdjęcie co 6 sekund; ma pauzę i ręczny wybór zdjęć. Zatrzymuje automatyczną zmianę w ukrytej karcie i przy fokusie klawiatury wewnątrz panoramy. Respektuje ograniczenie ruchu, a bez JavaScript zachowuje pierwsze zdjęcie i działające odnośniki kategorii. CSS dostosowuje menu i panoramę do wąskich ekranów.
- Dodano kategorie do modelu i migrację; istniejące `boots` i `accessories` zachowano. Migracja przenosi wyłącznie demonstracyjny `kask-ridge-m` z Akcesoriów do Kasków. Nowe produkty demo otrzymują tę samą kategorię. Nowe kategorie bez zdjęć korzystają z istniejących ilustracji zastępczych, bez odnośników do nieistniejących plików.
- Weryfikacja: migracje wykonano na PostgreSQL, wszystkie 15 testów przeszło, `manage.py check` i `makemigrations --check --dry-run` poprawne. W przeglądarce potwierdzono pełną szerokość zdjęcia, automatyczną zmianę slajdów, pauzę, ręczny wybór zdjęcia oraz przejście z menu Kaski do katalogu z wybranym filtrem i Ridge M. Widoku telefonu i preferencji ograniczenia ruchu nie zweryfikowano w przeglądarce.
- Instrukcje panoramy i kategorii dodano do README. Nie wykonano commita ani wysyłania do GitHub. Źródła i prawa do zdjęć użytkownika pozostają niezweryfikowane. `TODO.md` bez nowych uzgodnionych zadań.

### 2026-10-18 — ekspozycja wybranych ofert

- Zgodnie z wyborem użytkownika rozpoczęto od wyglądu strony głównej: duże zdjęcia wybranych produktów z odnośnikami do ich ofert. Zachowano kolory projektu, dodano responsywne kafle i ograniczenie ruchu zgodne z preferencjami przeglądarki.
- Produkt ma opcjonalną ścieżkę zdjęcia w `static/img/` i kolejność wyróżnienia. Administrator może zmieniać oba pola; strona pokazuje maksymalnie trzy aktywne, wyróżnione oferty ze zdjęciem. Brak wyboru pomija sekcję produktów; panorama pozostaje widoczna. Zdjęcia są wspólne dla katalogu i szczegółów; ceny nadal pochodzą z bazy.
- Użytkownik dostarczył trzy zdjęcia JPG jako tymczasowe przykłady. Narty i pierwszy snowboard powiązano z istniejącymi demonstracyjnymi Alpine 172 i Drift 156 (bez zmiany cen i nazw). Zdjęcia nie są potwierdzeniem rzeczywistych modeli pod tymi nazwami. Drugi snowboard pozostaje nieprzypisany do czasu dodania kolejnej oferty. Źródła i prawa do zdjęć nie zostały zweryfikowane.
- Dodano migracje pól i inicjalizacji wyróżnienia istniejących ofert demo. `seed_demo` ustawia zdjęcia i wyróżnienie tylko dla nowo tworzonych produktów; zachowuje późniejsze edycje.
- Weryfikacja na drugim komputerze: migracje wykonane, wszystkie 14 testów na osobnej bazie PostgreSQL przeszło; `manage.py check` i `makemigrations --check --dry-run` poprawne. W przeglądarce potwierdzono poprawne wyświetlenie dużych zdjęć i układu na komputerze. Widoku telefonu nie sprawdzono w przeglądarce.
- Instrukcję wymiany zdjęć i wyboru ofert dodano do README. Nie wykonano commita ani wysyłania do GitHub. `TODO.md` pozostaje pusty, bez nowych uzgodnionych zadań.

### Weryfikacja poprzedniego etapu (2026-10-16)

- Zmiana: pierwszy działający katalog Django z PostgreSQL, panelem administratora i ramą wizualną strony.
- Migracje wykonano na PostgreSQL 18.6, zapisano cztery produkty demonstracyjne. `manage.py check`, `makemigrations --check --dry-run` oraz `pip check` zakończyły się poprawnie.
- Wszystkie 11 testów na osobnej bazie PostgreSQL przeszło: odczyt produktów, aktualność ceny i stanu, filtrowanie, brak stanów ujemnych, ukrywanie, błędy 404, bezpieczne wyświetlanie opisów, powtarzalność danych demo i uprawnienia administratora. Test edycji przez panel potwierdza zmianę ceny i stanu w publicznym katalogu.
- W przeglądarce sprawdzono stronę główną i katalog oraz wybrano kategorię „Narty”, otrzymując jeden zgodny produkt. Widoku telefonu jeszcze nie zweryfikowano w przeglądarce.
- Potwierdzono odpowiedzi HTTP 200 strony głównej, katalogu, szczegółów, logowania administratora i zasobów statycznych. Sprawdzono start przez `start.ps1` w Windows PowerShell; plik ma kodowanie UTF-8 z BOM wymagane dla polskich znaków w PowerShell 5.1. Procesy używane do sprawdzania zatrzymano po weryfikacji; użytkownik uruchamia aplikację przez `start.ps1`.
- Nie wykonano commita ani wysyłania do GitHub.
