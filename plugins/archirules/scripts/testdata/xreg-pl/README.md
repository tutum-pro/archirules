# Architektura — rejestr decyzji

Zestaw wzorcowy dla `consistency.py`. Zawiera po jednym egzemplarzu każdej relacji
**między** rejestrami, na które checker patrzy: pytanie blokujące fazę, fazę czekającą
na pytanie, rekord zastąpiony w części, rekord zastąpiony w całości oraz rekord bez
żadnych powiązań.

Każde pole użyte tutaj pochodzi z szablonu albo z instrukcji w skillu. Zestaw testowy
napisany słownictwem wymyślonym przez checkera dowodzi zgodności checkera z zestawem
testowym i niczego więcej — patrz rekord o słownictwie checkerów w rejestrze
architektury samej wtyczki.

Sąsiedni zestaw `valid-pl` jest na to za mały — jeden rekord decyzji i brak tabeli
blokad, więc checker przechodzi po nim, nie wykonując ani jednej kontroli międzyrejestrowej.

| ADR | Temat | Status |
|---|---|---|
| [0001](decisions/ADR-0001-podstawa.md) | Podstawa | ZASTĄPIONY w części przez 0003 |
| [0002](decisions/ADR-0002-zastapiony.md) | Wariant zarzucony | ZASTĄPIONY przez 0003 |
| [0003](decisions/ADR-0003-modyfikacja.md) | Sięga wstecz do 0001 i 0002 | Przyjęty |
| [0004](decisions/ADR-0004-niezalezny.md) | Rekord bez powiązań | Przyjęty |

## Wymagania obowiązujące

Brak. Ten nagłówek musi tu być — checker odczytuje z niego język zestawu.

Patrz [rejestr faz](fazy-realizacji.md) i [pytania otwarte](open-questions.md).
