# ADR-0002 — Wariant zarzucony

**Status:** ZASTĄPIONY przez [ADR-0003](ADR-0003-modyfikacja.md), 2026-08-11 — cała decyzja, nic z niej nie zostaje

## Decyzja

Wariant, z którego zrezygnowano. Zastąpiony w całości, podczas gdy ADR-0001 został
zastąpiony w części; metoda ma jedną relację na oba przypadki i rozróżnia je zakresem
wpisanym w status.

## Konsekwencje

**Pozytywne.** Zestaw zawiera rekord faktycznie wygaszony, więc wpis wskazujący na niego
daje się rozpoznać jako wskazujący na coś, co już nie obowiązuje.

**Koszt, przyjęty świadomie.** Rekord zostaje, choć nie obowiązuje.

## Stan realizacji

Służy wyłącznie testowi checkera.
