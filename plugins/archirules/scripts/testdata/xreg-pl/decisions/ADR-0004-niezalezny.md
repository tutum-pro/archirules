# ADR-0004 — Rekord bez powiązań

**Status:** Przyjęty

## Decyzja

Rekord, który nikogo nie zastępuje i którego nikt nie zastępuje. Zestaw musi taki
zawierać, bo inaczej checker wymagający zakresu zastąpienia od **każdego** rekordu
przeszedłby ten test niezauważony.

Jest to również rekord, na który wskazują pytania otwarte, bo wpis `Dotyka` wycelowany w
rekord obowiązujący to przypadek poprawny. Selftest przestawia go na zastąpiony, żeby
udowodnić, że checker widzi różnicę.

## Konsekwencje

**Pozytywne.** Osobny rekord, w który da się w teście wstrzyknąć sprzeczne rozstrzygnięcie,
nie ruszając łańcucha zastąpień.

**Koszt, przyjęty świadomie.** Jeden plik więcej w zestawie.

## Stan realizacji

Służy wyłącznie testowi checkera.
