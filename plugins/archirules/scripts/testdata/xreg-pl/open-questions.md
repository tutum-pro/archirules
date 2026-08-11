# Pytania otwarte

### OQ-01 — Czy tabela blokad jest trzymana razem z tabelą faz
**Status:** OTWARTE · **Dotyka:** [ADR-0004](decisions/ADR-0004-niezalezny.md) · **Blokuje:** X2

Pytanie otwarte deklarujące, że blokuje fazę. Checker patrzy na dwie rzeczy naraz: czy
faza X2 ma status `⛔` oraz czy tabela blokad wymienia to pytanie pod X2. Rozejście się
tych dwóch zapisów jest wadą, której żaden z rejestrów nie widzi u siebie.

Dotyka rekordu **obowiązującego**, i to celowo. Wskazanie zastąpionego jest wadą, a
selftest wykonuje tę zmianę, żeby udowodnić, że checker to zauważa.

### OQ-02 — Czy wariant zarzucony w ADR-0002 wraca
**Status:** ROZSTRZYGNIĘTE → [ADR-0003](decisions/ADR-0003-modyfikacja.md), 2026-08-11 — nie wraca

Pytanie zamknięte, i nie deklaruje żadnej blokady. Tego właśnie wymaga checker: pytanie,
które ma odpowiedź, a mimo to nadal mówi, co wstrzymuje, zostawia fazę czekającą na nic.
Selftest dopisuje to pole z powrotem, żeby udowodnić, że kontrola działa.
