# ADR-0003 — Modyfikacja podstawy

**Status:** Przyjęty · **Modyfikuje:** [ADR-0001](ADR-0001-podstawa.md) · **Zastępuje:** [ADR-0002](ADR-0002-zastapiony.md) · **Rozstrzyga:** OQ-02

## Decyzja

Rekord, który sięga do dwóch wcześniejszych: jednemu odbiera moc w części, drugiemu
w całości. Oba muszą o tym wiedzieć u siebie — link jednostronny to zapis, który
przestał być prawdą po jednej stronie.

## Konsekwencje

**Pozytywne.** Historia decyzji daje się przejść w obie strony.

**Koszt, przyjęty świadomie.** Każda modyfikacja to dwa pliki do zmiany, nie jeden.

## Stan realizacji

Służy wyłącznie testowi kontrolera.
