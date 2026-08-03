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

## 7. Zgodność strukturalna — uruchom kontroler, nie pisz go od nowa

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/conform.py docs/architecture
```

Sprawdza artefakty, sekcje każdego ADR-a, zgodność indeksu z liczbą plików, numerację
i kształt wpisów OQ oraz rejestr faz. Rozpoznaje wariant polski i angielski po `README.md`.
Kod wyjścia 1 przy jakimkolwiek naruszeniu, więc nadaje się do bramki CI.

**Zanim mu uwierzysz**, uruchom dowód, że potrafi paść:

```
bash ${CLAUDE_PLUGIN_ROOT}/scripts/selftest.sh
```

Psuje kopię poprawnego zestawu na sześć sposobów i wymaga wykrycia każdego.

### Dlaczego kontroler wygląda tak, a nie inaczej

Sprawdzenie, czy każdy ADR ma wymagane sekcje, jest kuszące do zautomatyzowania i **bardzo
łatwe do zepsucia**. Cztery kolejne wersje takiego kontrolera dały wyniki fałszywe, każda
z innego powodu:

| błąd | skutek |
|---|---|
| wzorzec `**Koszty` | nie widział `**Koszt.**` w liczbie pojedynczej → 6 fałszywych braków |
| lista słów `odrzuc\|odpad\|alternatyw` | nie widziała „**Nie zakładamy** trzeciego namespace" |
| wzorzec regularny z pustą alternatywą | narzędzie zwróciło błąd na stderr, skrypt wypisał „czysto" |
| `for x in $zmienna` w **zsh** | brak podziału na słowa → jeden obieg zamiast jedenastu |

Stąd trzy zasady, wbudowane już w `conform.py`:

1. **Dopasowuj prefiksy, nie pełne brzmienia.** `**Koszt` zamiast `**Koszty, przyjęte
   świadomie.**`. Wariant językowy nie jest niezgodnością.
2. **Zanim zgłosisz brak — otwórz plik.** Treść bywa pod innym nagłówkiem albo w prozie.
   Zgłoszenie „brak sekcji" jest twierdzeniem o dokumencie, więc podlega regule W3.
3. **Rozliczaj pokrycie.** Licz sprawdzone kontra wszystkie i **odmawiaj orzeczenia przy
   niezgodności**. To jedyna z czterech pułapek powyżej, którą wykryto automatycznie —
   dokładnie dzięki temu licznikowi.

Rozbieżność brzmienia nagłówków sama w sobie **nie jest wadą dokumentu**. `**Koszt.**` przy
jednym koszcie jest poprawne, a `**Koszty i warunki wstępne**` niesie treść, której skrócenie
by usunęło. Wadą jest dopiero to, że **nie da się tego sprawdzić maszynowo** — i naprawia się
to w kontrolerze oraz w szablonie dla nowych dokumentów, nie przez przepisywanie historii.

## Wynik

Raportuj z podziałem na wagę i **z dowodem przy każdym znalezisku**. Poprawki wnoś osobnym
commitem od pracy funkcjonalnej — historia z jednym commitem „funkcja + dokumentacja" ukrywa,
że audyt coś znalazł.
