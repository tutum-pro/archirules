# Architektura — rejestr decyzji

Zestaw wzorcowy dla `consistency.py`. Zawiera po jednym egzemplarzu każdej relacji
**między** rejestrami, którą kontroler sprawdza: pytanie blokujące fazę, faza czekająca
na pytanie, rekord modyfikujący inny, rekord zastąpiony i rekord bez żadnych powiązań.

Zestaw `valid-pl` obok jest za mały do tego celu — ma jeden ADR i nie ma tabeli blokad,
więc kontroler przechodzi po nim bez wykonania ani jednego sprawdzenia międzyrejestrowego.

| ADR | Temat | Status |
|---|---|---|
| [0001](decisions/ADR-0001-podstawa.md) | Podstawa | **zmodyfikowany przez 0003** |
| [0002](decisions/ADR-0002-zastapiony.md) | Wariant porzucony | ZASTĄPIONY przez 0003 |
| [0003](decisions/ADR-0003-modyfikacja.md) | Modyfikacja podstawy — modyfikuje 0001, zastępuje 0002 | Przyjęty |
| [0004](decisions/ADR-0004-niezalezny.md) | Rekord bez powiązań | Przyjęty |

## Wymagania obowiązujące

Brak. Ta sekcja musi tu być — po jej nagłówku kontroler rozpoznaje język zestawu.

Patrz [rejestr faz](fazy-realizacji.md) i [pytania otwarte](open-questions.md).
