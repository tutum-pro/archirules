# ADR-0004 — Rekord bez powiązań

**Status:** Przyjęty

## Decyzja

Rekord, który niczego nie modyfikuje i którego nic nie modyfikuje. Zestaw musi zawierać
i taki, bo inaczej kontroler wymagający sekcji „Co zostało zmienione" od każdego rekordu
przeszedłby ten test niezauważony.

## Konsekwencje

**Pozytywne.** Osobny rekord do wstrzyknięcia sprzecznego rozstrzygnięcia w teście.

**Koszt, przyjęty świadomie.** Jeden plik więcej w zestawie.

## Stan realizacji

Służy wyłącznie testowi kontrolera.
