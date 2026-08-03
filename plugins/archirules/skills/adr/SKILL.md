---
name: adr
description: Write, supersede or amend an architecture decision record (ADR). Use when an architectural decision has been made, reversed, or discovered to be undocumented.
---

# Rejestr decyzji

## Nowy ADR

1. **Numer** — najwyższy istniejący + 1, z zerami wiodącymi (`ADR-0014`). Sprawdź katalog,
   nie pamięć.
2. **Nagłówek** — `Status`, `Rozstrzyga` (numery OQ), `Odblokowuje` (fazy), `Powiązane`,
   a przy zastąpieniu `Zastępuje`.
3. Wypełnij szablon `templates/<język>/ADR.md`.

## Sekcje obowiązkowe

**„Rozważone i odrzucone"** — każda odrzucona opcja z powodem. Bez tego ktoś zaproponuje ją
ponownie i nikt nie będzie umiał odpowiedzieć (reguła P3).

**„Koszty, przyjęte świadomie"** — w trybie oznajmującym. Nie „ryzyka", nie „do rozważenia".
Jeśli nie umiesz wymienić ani jednego kosztu, **decyzja nie jest jeszcze zrozumiana** —
wróć do analizy zamiast pisać ADR.

**„Stan realizacji"** — co zbudowane, co zweryfikowane i **czym** zweryfikowane. Nie „działa",
tylko wynik.

## Zastępowanie

Gdy decyzja zostaje odwrócona:

1. Nowy ADR z polem `Zastępuje: ADR-NNNN`.
2. Stary ADR dostaje **na górze** status `ZASTĄPIONY przez ADR-MMMM` z datą i zakresem
   (często zastępowana jest tylko część). **Zostaje w rejestrze** — opisuje rozumowanie, które
   doprowadziło do zmiany.
3. Wiersz w tabeli `README.md` aktualizowany w obu miejscach.
4. Jeśli ADR powstał z opóźnieniem — **napisz to w nim**, wraz z okresem, w którym rejestr
   mówił nieprawdę (reguła P7).

## Po zapisaniu

- dopisz wiersz do tabeli w `README.md` — ADR spoza indeksu nie istnieje;
- zamknij rozstrzygnięte OQ, wskazując ten ADR;
- jeśli decyzja wiąże **każdą** pracę, dopisz ją do „Wymagań obowiązujących".
