# ADR-0001 — Podstawa

**Status:** ZASTĄPIONY przez [ADR-0003](ADR-0003-modyfikacja.md), 2026-08-11 — wyłącznie punkt drugi; reszta obowiązuje

## Decyzja

Rekord, któremu późniejszy odbiera moc **w części**. Zostaje w rejestrze: historia
decyzji jest częścią decyzji.

Zakres stoi w linii statusu, a nie w sekcji poniżej. Sprostowanie napisane pod polem,
które nadal mówi swoje, nie jest sprostowaniem — reguła P7, przypadek C-04. To samo
umiejscowienie jest powodem, dla którego zakres sprawdza `conform.py`, czytający jeden
plik naraz, a nie ten checker.

## Konsekwencje

**Pozytywne.** Checker ma poprawne powiązanie dwustronne do rozpoznania: w przód z pola
`Zastępuje` w ADR-0003, w tył z tej linii statusu.

**Koszt, przyjęty świadomie.** Zestaw wzorcowy trzeba utrzymywać razem z checkerem.

## Stan realizacji

Służy wyłącznie testowi checkera.
