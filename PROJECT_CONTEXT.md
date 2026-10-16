# Kontekst projektu

Ostatnia aktualizacja: 2026-10-16.

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

- Działa szkielet Django: `config` (konfiguracja), `accounts` (model użytkownika oparty na `AbstractUser`) i `catalog` (produkty i ich obsługa).
- Działa połączenie z lokalnym PostgreSQL, migracje i komenda `seed_demo`, dodająca cztery fikcyjne produkty bez nadpisywania późniejszych zmian.
- Działa strona główna, katalog, wyszukiwanie po nazwie i opisie, filtrowanie kategorii oraz szczegóły produktu. Ceny i stany sprzedażowe są odczytywane z bazy. Układ ma reguły CSS dla komputerów i telefonów.
- Administrator może dodawać, edytować i ukrywać produkty przez panel Django. Pola produktu: nazwa, unikalny adres, kategoria, opis, cena, liczba sztuk na sprzedaż i widoczność. Cena i stan są zabezpieczone przed wartościami ujemnymi.
- Dostęp do zarządzania kontroluje Django. Przyszłe konta klientów korzystają z własnego modelu użytkownika; rejestracja i interfejs logowania klientów pozostają kolejnymi etapami.
- Przygotowano instrukcję uruchomienia i odtworzenia środowiska na drugim komputerze w `README.md`, `.env.example`, przypięte wersje głównych zależności i skrypt `start.ps1`.
- `TODO.md` pozostaje pusty zgodnie z ustaleniami.

## Lokalne środowisko i uruchamianie

- Na bieżącym komputerze przygotowano `.venv` z Pythonem 3.12.4 i przenośny PostgreSQL 18.6 w ignorowanym katalogu `work/`. Baza nasłuchuje wyłącznie na `127.0.0.1:55432`; konfigurację aplikacji przechowuje ignorowany `.env`.
- `start.ps1` uruchamia przygotowaną bazę, jeśli jest zatrzymana, oraz stronę pod `http://127.0.0.1:8000/`. Na drugim komputerze można użyć zwykłej instalacji PostgreSQL i portu z własnego `.env`.
- Nie utworzono stałego konta administratora strony. Użytkownik tworzy je przez `manage.py createsuperuser`, samodzielnie podając dane. Testy korzystają z tymczasowych kont w osobnej bazie.
- Środowisko, pliki bazy i sekrety nie są współdzielone przez Git. Drugi komputer odtwarza bazę przez migracje i `seed_demo`.
- Zakupy i rezerwacje nie mają jeszcze aktywnych przycisków; interfejs oznacza je jako kolejne etapy. Egzemplarze wypożyczalni będą miały osobną ewidencję od stanu sprzedażowego.

## Problemy i kwestie organizacyjne

- W zgłoszeniu do wykładowcy opisano wypożyczalnię; później w rozmowie rozszerzono zakres o sprzedaż. Potwierdzenie tego rozszerzenia u wykładowcy pozostaje kwestią do ustalenia.
- Kontekst trafia na drugi komputer przez wysłanie i pobranie zmian w GitHub; nie synchronizuje się samą zmianą rozmowy.

## Ostatnia zmiana i weryfikacja

- Zmiana: pierwszy działający katalog Django z PostgreSQL, panelem administratora i ramą wizualną strony.
- Migracje wykonano na PostgreSQL 18.6, zapisano cztery produkty demonstracyjne. `manage.py check`, `makemigrations --check --dry-run` oraz `pip check` zakończyły się poprawnie.
- Wszystkie 11 testów na osobnej bazie PostgreSQL przeszło: odczyt produktów, aktualność ceny i stanu, filtrowanie, brak stanów ujemnych, ukrywanie, błędy 404, bezpieczne wyświetlanie opisów, powtarzalność danych demo i uprawnienia administratora. Test edycji przez panel potwierdza zmianę ceny i stanu w publicznym katalogu.
- W przeglądarce sprawdzono stronę główną i katalog oraz wybrano kategorię „Narty”, otrzymując jeden zgodny produkt. Widoku telefonu jeszcze nie zweryfikowano w przeglądarce.
- Potwierdzono odpowiedzi HTTP 200 strony głównej, katalogu, szczegółów, logowania administratora i zasobów statycznych. Sprawdzono start przez `start.ps1` w Windows PowerShell; plik ma kodowanie UTF-8 z BOM wymagane dla polskich znaków w PowerShell 5.1. Procesy używane do sprawdzania zatrzymano po weryfikacji; użytkownik uruchamia aplikację przez `start.ps1`.
- Nie wykonano commita ani wysyłania do GitHub.
