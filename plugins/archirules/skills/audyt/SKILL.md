---
name: audyt
description: Audit the architecture documentation for completeness and truthfulness — numbering defects, missing index entries, superseded records still claiming to be current, statuses that reality has overtaken. Use periodically and before any milestone.
---

# Audyt kompletności rejestrów

**Sprawdzaj, nie zapewniaj.** Wynikiem audytu jest lista znalezisk albo zdanie „sprawdziłem
N rzeczy, nic nie znalazłem" — nigdy „wszystko wygląda dobrze".

## 1. Wady numeracji

```
grep -oE "^### OQ-[0-9]+" open-questions.md | sort | uniq -d          # duplikaty
grep -oE "^### OQ-[0-9]+" open-questions.md | grep -oE "[0-9]+" \
  | sort -n -u                                                        # luki
```

Duplikat numeru czyni **każde** odwołanie do niego niejednoznacznym. Przy poprawianiu
przenumeruj tę pozycję, do której jest **mniej odwołań**, i popraw wszystkie odwołania.

## 2. Indeks kontra rzeczywistość

Liczba plików w `decisions/` musi się zgadzać z liczbą wierszy w tabeli `README.md`. **ADR
spoza indeksu nie istnieje** — nikt go nie znajdzie.

## 3. Zapisy, które przestały być prawdą

Najgroźniejsza kategoria i najtrudniejsza do znalezienia:

- ADR ze statusem *Przyjęty*, którego decyzja została w praktyce odwrócona;
- OQ *ZABLOKOWANE przez* pytanie już rozstrzygnięte;
- OQ *OTWARTE*, którego treść jest zbudowana;
- zdanie w ADR opisujące zachowanie, którego kod nie ma.

Dla każdego ADR-a zapytaj: **czy gdyby ktoś przeczytał tylko ten dokument, wyciągnąłby
wniosek zgodny z tym, co jest zbudowane?**

## 4. Kod bez śladu w dokumentacji

Wypisz elementy wprowadzone od ostatniego audytu — migracje, bramki, moduły, publiczne typy —
i sprawdź, czy każdy ma wzmiankę. Szukaj **pojęcia**, nie nazwy pliku: migracja `0007_retry.sql`
bywa opisana jako „migracja `0007`".

## 5. Decyzje, które nigdy nie trafiły do rejestru

Przejrzyj historię commitów i rejestr faz pod kątem rozstrzygnięć żyjących wyłącznie w kodzie.
**To jest najczęstsze i najpoważniejsze znalezisko.** Decyzja podjęta w trakcie pracy rzadko
sama prosi się o ADR.

## 6. Ryzyka odkryte i nieodnotowane

Zwłaszcza bezpieczeństwo i operacje: klucze w historii, repozytoria bez kopii, poświadczenia
w manifestach, konfiguracja istniejąca tylko na jednej maszynie. Sprawdź **stan faktyczny**
(`git ls-remote`, `git branch`, obecność obiektu), nie wspomnienie o nim.

## Wynik

Raportuj z podziałem na wagę i **z dowodem przy każdym znalezisku**. Poprawki wnoś osobnym
commitem od pracy funkcjonalnej — historia z jednym commitem „funkcja + dokumentacja" ukrywa,
że audyt coś znalazł.
