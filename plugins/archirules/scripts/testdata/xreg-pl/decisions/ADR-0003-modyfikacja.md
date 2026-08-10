# ADR-0003 — Sięga wstecz do dwóch wcześniejszych rekordów

**Status:** Przyjęty · **Zastępuje:** [ADR-0001](ADR-0001-podstawa.md), [ADR-0002](ADR-0002-zastapiony.md) · **Rozstrzyga:** OQ-02

## Decyzja

Rekord sięgający wstecz do dwóch wcześniejszych: jednemu odbiera moc w części, drugiemu
w całości. **Oba muszą wiedzieć o tym u siebie** — powiązanie jednostronne to rekord,
który przestał być prawdziwy na jednym końcu, i akurat na ten koniec czytelnik trafia
najpierw.

## Konsekwencje

**Pozytywne.** Historię decyzji da się przejść w obie strony.

**Koszt, przyjęty świadomie.** Każde zastąpienie to dwa pliki do zmiany, nie jeden.

## Stan realizacji

Służy wyłącznie testowi checkera.
