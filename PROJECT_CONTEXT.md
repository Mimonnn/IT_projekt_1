# Kontekst projektu

Ostatnia aktualizacja: 2026-10-21.

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
