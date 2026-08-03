# archirules

**Meta-reguły prowadzenia projektu wytwórczego IT** — jako wtyczka do Claude Code.

Metoda wypracowana w praktyce, przy budowie platformy leasingowej. **Każda reguła istnieje
dlatego, że jej brak coś zepsuł**, a nie dlatego, że dobrze brzmi — przy większości zapisana
jest awaria, której zapobiega.

## Co robi

Zamienia decyzje architektoniczne, wątpliwości, fazy i dowody w **artefakty pierwszej klasy**:
wersjonowane razem z kodem, przeglądane jak kod i tak samo jak kod zdolne stać się
nieaktualnymi — co też się odnotowuje.

Projekt wytwórczy rzadko przegrywa z trudnymi decyzjami. Przegrywa z decyzjami **podjętymi
milcząco** — przez kolejność refaktorów, przez wartość domyślną, przez to, że nikt nie zapisał
alternatywy.

## Instalacja

```
/plugin marketplace add tutum-pro/archirules
/plugin install archirules@archirules
```

W projekcie:

```
/archirules:bootstrap
```

## Zawartość

- [`RULES.md`](plugins/archirules/RULES.md) — reguły, wersja kanoniczna (PL)
- [`RULES.en.md`](plugins/archirules/RULES.en.md) — tłumaczenie (EN)
- `plugins/archirules/skills/` — sześć skilli
- `plugins/archirules/templates/` — szablony PL i EN

## Skąd się to wzięło

Z projektu, w którym po kilku dniach pracy okazało się, że: bramka kontrolna dwukrotnie
zgłaszała „czysto" na celowo zepsutym kodzie, sześć testów przeszło mimo zepsutej konfiguracji
domyślnej, a rejestr decyzji przez dobę ogłaszał wybór technologii odwrócony dzień wcześniej.

Każda z tych rzeczy została znaleziona **przez sprawdzenie, nie przez czytanie kodu**. Reguły
w `RULES.md` są zapisem tego, jak się je znajduje.

## Licencja

<!-- DO USTALENIA. Repozytorium przeznaczone do publicznego udostępnienia i ponownego
     użycia w innych projektach; brak pliku LICENSE oznacza domyślnie "wszelkie prawa
     zastrzeżone", co prawdopodobnie nie jest intencją. Decyzja prawna, nie inżynierska. -->
