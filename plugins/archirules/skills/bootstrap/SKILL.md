---
name: bootstrap
description: Scaffold the architecture documentation set (decision records, open questions, phase register) in a project that does not have one yet. Use when starting a new project or introducing the archirules method into an existing one.
---

# Założenie rejestrów w projekcie

## Zanim cokolwiek utworzysz

1. Sprawdź, czy `docs/architecture/` już istnieje. **Jeśli tak — nie nadpisuj.** Zgłoś, co
   zastałeś, i zaproponuj uzupełnienie brakujących elementów.
2. Ustal z użytkownikiem **język dokumentacji** (`pl` lub `en`) — decyduje o tym, których
   szablonów użyjesz z `templates/`. Zapisz wybór w `README.md` rejestru, żeby kolejna sesja
   nie musiała zgadywać.
3. Ustal, **czy projekt zaczyna się od modelu procesu** (reguła P1). Jeśli tak, załóż też
   katalog na modele i pierwszy plik `.bpmn` albo równoważny.

## Co utworzyć

```
docs/architecture/
  README.md              indeks + sekcja "Wymagania obowiązujące"
  decisions/             (pusty, na ADR-y)
  open-questions.md      z nagłówkiem i pustą numeracją
  fazy-realizacji.md     z legendą i pustą tabelą faz
```

`rejestr-weryfikacji.md` **zakładaj dopiero**, gdy pojawi się pierwsze twierdzenie wymagające
sprostowania. Pusty rejestr weryfikacji uczy, że można go ignorować.

## Sekcja „Wymagania obowiązujące"

To jest najważniejsza część `README.md` i jedyna, którą czyta się przy **każdym** zadaniu.
Trafiają tu wyłącznie decyzje wiążące pracę poza własnym obszarem — na starcie zwykle pusta,
z jednym zdaniem wyjaśniającym, co tu trafi.

## Na koniec

Zaproponuj dopisanie do `CLAUDE.md` projektu fragmentu z `CLAUDE.md.example`, żeby metoda
obowiązywała bez proszenia o nią w każdej sesji. **Nie dopisuj bez zgody** — to zmienia
domyślne zachowanie w całym projekcie.
