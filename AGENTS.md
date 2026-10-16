# Zasady pracy nad projektem

## Rozpoczęcie pracy

- Przeczytaj ten plik, `PROJECT_CONTEXT.md` oraz `TODO.md` na początku każdej nowej rozmowy i po zmianie komputera.
- Sprawdź bieżącą gałąź, stan zmian i odpowiednie pliki repozytorium. Dokumentację porównuj z rzeczywistą zawartością projektu; nie zakładaj, że jest zawsze aktualna.
- Nie zgaduj brakujących ustaleń i nie traktuj propozycji jako zaakceptowanych decyzji. Istotne rozbieżności wyjaśniaj przed wykonaniem zależnych od nich zmian.
- Przed rozpoczęciem pracy na drugim komputerze pobierz aktualne zmiany z GitHub, jeśli stan lokalnych plików na to pozwala. Nie nadpisuj ani nie usuwaj lokalnej pracy. Nie wykonuj automatycznie resetów ani wymuszonego wysyłania zmian.

## Architektura i konwencje

- Projekt obejmuje sklep narciarski z wypożyczalnią, frontend, backend oraz lokalną bazę danych. Aktualne decyzje i opis architektury utrzymuj w `PROJECT_CONTEXT.md`.
- Stos technologiczny: Python i Django 5.2 LTS, lokalny PostgreSQL, szablony HTML Django i CSS; JavaScript dodawaj w miarę potrzeb. Frontend i backend należą do jednego projektu. Nie wprowadzaj SQLite jako zastępstwa przy braku połączenia z PostgreSQL.
- `config` zawiera konfigurację, `accounts` własny model użytkownika, a `catalog` katalog produktów. Kod i identyfikatory pisz po angielsku, treści interfejsu i objaśniające komentarze po polsku. Ceny przechowuj jako `Decimal`, zmiany struktury bazy zapisuj w migracjach.
- Po zmianach backendu uruchamiaj odpowiednie testy na PostgreSQL oraz `manage.py check`; po zmianach modeli sprawdzaj migracje. Instrukcje konfiguracji i polecenia są w `README.md`.
- Oddzielaj zasoby przeznaczone na sprzedaż od konkretnych egzemplarzy przeznaczonych do wypożyczenia. Dostępność wypożyczenia zależy od terminu rezerwacji i stanu sprzętu.
- Uprawnienia klienta i administratora sprawdzaj w backendzie. Samo ukrycie elementów interfejsu nie zapewnia kontroli dostępu.
- Stosuj konwencje przyjęte w projekcie, czytelne nazwy i małe, spójne zmiany. Nowe konwencje oraz wybory technologii zapisuj po ich uzgodnieniu. Nie wprowadzaj zależności ani rozbudowy niezwiązanej z zadaniem.
- Sprawdzaj zmieniane zachowanie odpowiednio do zakresu prac. W kontekście zapisuj faktyczne wyniki weryfikacji i ograniczenia, bez deklarowania niewykonanych testów.
- Pisz dokumentację po polsku. Nie zapisuj haseł, tokenów, kluczy, danych dostępowych, poufnych danych użytkowników ani lokalnych plików bazy zawierających takie dane w repozytorium lub dokumentacji. Przykłady konfiguracji mogą zawierać wyłącznie bezpieczne wartości przykładowe.

## Utrzymywanie kontekstu przy każdym commicie

- Przed każdym commitem sprawdź zgodność `AGENTS.md`, `PROJECT_CONTEXT.md` i `TODO.md` z przygotowanymi zmianami.
- W każdym commicie aktualizuj `PROJECT_CONTEXT.md`: zapisz zwięźle aktualny postęp, opis zmiany i wynik weryfikacji. Dotyczy to także commitów dokumentacyjnych. Nie wpisuj hasha commita, który dopiero powstanie.
- `AGENTS.md` aktualizuj, gdy zmieniają się trwałe zasady pracy, architektura lub konwencje. Utrzymuj jeden aktualny opis zamiast powielania sprzecznych instrukcji.
- `TODO.md` służy do zapisywania uzgodnionych pomysłów i zadań na kolejną sesję, przede wszystkim pod koniec bieżącej sesji. Nie wypełniaj go automatycznie domyślnym planem. Jeśli zawiera zadania, aktualizuj ich status po wykonaniu, a priorytety zapisuj zgodnie z ustaleniami.
- Aktualizację kontekstu dołączaj do tego samego commita co opisywane zmiany. Unikaj kopiowania całej historii rozmowy; zachowuj aktualne ustalenia, postęp, istotne problemy i uzgodnione dalsze kroki.
- Przy commicie poświęconym wyłącznie dokumentacji kontekstu nie zmieniaj dodatkowo kodu aplikacji. Przy zwykłej pracy nad projektem normalnie modyfikuj kod w ramach zadania i commituj go wraz z aktualizacją kontekstu.
- Przed commitem przejrzyj przygotowany zakres zmian, aby nie dołączyć przypadkowych plików, cudzej pracy ani poufnych danych.

## Praca między komputerami

- Te trzy pliki są wspólną pamięcią projektu przechowywaną w Git. Historia rozmów nie zastępuje ich i nie musi być dostępna w nowej sesji.
- Aby przekazać kontekst na drugi komputer, zmiany muszą zostać zatwierdzone i wysłane do GitHub, a następnie pobrane na drugim komputerze.
- Instrukcje dotyczące każdego commita są zasadami pracy Codex; nie stanowią automatycznej kontroli commitów wykonywanych ręcznie poza sesją.
