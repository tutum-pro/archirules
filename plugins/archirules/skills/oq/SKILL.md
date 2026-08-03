---
name: oq
description: Register a new open question or resolve an existing one in the open-questions register. Use when a doubt has no answer yet, or when a decision closes one.
---

# Rejestr pytań otwartych

## Rejestrowanie

1. **Numer** — najwyższy + 1. Sprawdź **duplikaty i luki** przed nadaniem:
   ```
   grep -oE "^### OQ-[0-9]+" open-questions.md | sort | uniq -d     # duplikaty
   ```
   Nie licz nagłówków, żeby zgadnąć kolejny numer — wpisy archiwalne i duplikaty zafałszują
   wynik. Weź **maksimum**, nie liczbę.

2. **Nagłówek wpisu:**
   ```
   ### OQ-NN — <pytanie, nie temat>
   **Status:** OTWARTE · **Priorytet: ...** · **Blokuje/Zależy od/Dotyka:** ...
   ```

3. **Treść** odpowiada na trzy rzeczy: czego nie wiemy, co się stanie, jeśli nie
   rozstrzygniemy, i co trzeba wiedzieć, żeby rozstrzygnąć.

## Kiedy zakładać OQ

- wątpliwość, którą kusi rozstrzygnąć „na razie tak" — **zawsze**;
- granica, której nie da się wyegzekwować maszynowo (reguła W9);
- ryzyko odkryte przy okazji innej pracy, którego teraz nie naprawiasz;
- decyzja odłożona świadomie — z zapisem, **do kiedy** i **od czego** zależy.

Jeśli piszesz w kodzie komentarz zaczynający się od „na razie", „docelowo" albo „do
rozważenia" — to jest OQ, nie komentarz.

## Zamykanie

Status zmień na `ROZSTRZYGNIĘTE → <ADR albo faza>, <data>` i **napisz, jak brzmi
odpowiedź** — link bez odpowiedzi zmusza do czytania całego ADR-a.

Trzy przypadki szczególne:

- **Odpowiedź odwrócona** — zaznacz, że pierwsza była inna i dlaczego się zmieniła. To
  ważniejsze niż podmiana linku.
- **Pytanie przestało istnieć** — napisz to wprost zamiast udawać rozstrzygnięcie.
- **Zamknięte częściowo** — zostaw otwarte i przenieś sedno wpisu na to, co zostało.
