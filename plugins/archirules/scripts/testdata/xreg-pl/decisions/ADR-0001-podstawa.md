# ADR-0001 — Podstawa

**Status:** Przyjęty · **Zmodyfikowany przez:** [ADR-0003](ADR-0003-modyfikacja.md)

## Decyzja

Rekord, któremu późniejszy rekord odbiera moc w części. Zostaje w rejestrze — historia
decyzji jest częścią decyzji.

## Co zostało zmienione

[ADR-0003](ADR-0003-modyfikacja.md) odbiera moc drugiemu zdaniu tej decyzji. Reszta
obowiązuje. Bez tej sekcji czytelnik wie, że coś się zmieniło, ale nie wie co.

## Konsekwencje

**Pozytywne.** Kontroler ma po czym poznać poprawny link dwustronny.

**Koszt, przyjęty świadomie.** Zestaw wzorcowy trzeba utrzymywać razem z kontrolerem.

## Stan realizacji

Służy wyłącznie testowi kontrolera.
