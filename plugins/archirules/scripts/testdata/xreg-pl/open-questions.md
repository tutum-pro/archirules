# Pytania otwarte

### OQ-01 — Czy tabela blokad jest utrzymywana razem z tabelą faz
**Status:** OTWARTE · **Dotyka:** [ADR-0001](decisions/ADR-0001-podstawa.md) · **Blokuje:** X2

Pytanie otwarte, które deklaruje blokadę fazy. Kontroler sprawdza dwie rzeczy naraz:
że faza X2 ma status `⛔`, i że tabela blokad wymienia to pytanie przy X2. Rozejście się
tych dwóch zapisów jest defektem, którego żaden rejestr nie widzi u siebie.

### OQ-02 — Czy wariant porzucony w ADR-0002 wraca
**Status:** ROZSTRZYGNIĘTE · **Odpowiedź:** nie wraca; zamyka to [ADR-0003](decisions/ADR-0003-modyfikacja.md)

Pytanie rozstrzygnięte. Istnieje po to, żeby kontroler miał czego szukać w tabelach
blokad — pytanie zamknięte, a wciąż wymieniane jako blokada, zatrzymuje fazę bez powodu.
