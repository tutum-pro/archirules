---
name: fazy
description: Manage the phase register — open a phase with its acceptance criterion, or close one with evidence. Use before starting a work phase and when reporting it complete.
---

# Rejestr faz

## Otwarcie fazy — **przed** pracą

Wpis w tabeli: identyfikator, nazwa, status `☐`, **kryterium akceptacji**.

Kryterium musi być **sprawdzalne i nietrywialne**:

| źle | dobrze |
|---|---|
| „zrobić persystencję" | „**instancja przeżywa restart i wznawia się**" |
| „dodać walidację" | „`@annuity` w warunku = **błąd kompilacji**" |
| „obsłużyć ponawianie" | „**dwukrotne dostarczenie kroku = jeden skutek**" |

Kryterium zapisane po fakcie zawsze jest spełnione — dlatego P5 wymaga zapisania go wcześniej.

## Twarda bramka

Przy podejściu kosztownym zapisz **warunek jego porzucenia**, zanim zaczniesz. Sformułuj tak,
żeby dało się go stwierdzić bez dyskusji: *„jeśli fazy B1–B5 nie mieszczą się w tygodniu
pracy, opcja C była zła"*.

## Zamknięcie fazy

**Nie zamykaj na podstawie tego, że kod istnieje.** Zamknięcie wymaga:

1. **Dowodu**, że kryterium akceptacji jest spełnione — polecenie i jego wynik, nie deklaracja.
2. **Dwóch przebiegów** testów pod rząd (reguła W7).
3. **Sekcji opisowej** pod tabelą: co zostało zrobione, **jakie decyzje projektowe** podjęto
   po drodze, **co świadomie pominięto** i pod jakim OQ to zapisano.
4. Odnotowania rzeczy, które wyszły przy okazji — zwłaszcza błędów znalezionych we własnej
   wcześniejszej pracy. To jest najcenniejsza część rejestru i jedyne miejsce, gdzie się
   utrwala.

## Gdy faza „prawie" gotowa

Status `◐` i **wypunktowanie, czego brakuje**. Nie zaokrąglaj w górę: faza zamknięta
przedwcześnie zabiera bramce cały sens.

Zanim zgłosisz fazę jako kompletną, **sprawdź kryterium dosłownie**. „Błąd kompilacji" znaczy
nieudane budowanie, a nie odmowę w czasie działania — to nie jest to samo i różnicę widać
dopiero, gdy się ją naprawdę uruchomi.
