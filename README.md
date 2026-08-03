# archirules

[![Licencja: CC BY-SA 4.0](https://img.shields.io/badge/Licencja-CC%20BY--SA%204.0-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-wtyczka-orange.svg)](https://github.com/tutum-pro/archirules)

🇬🇧 [English](README.en.md) — tłumaczenie; przy rozbieżności rozstrzyga ta wersja

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
- `plugins/archirules/scripts/` — kontroler zgodności strukturalnej wraz z samotestem
  dowodzącym, że potrafi paść

## Skąd się to wzięło

Z projektu, w którym po kilku dniach pracy okazało się, że: bramka kontrolna dwukrotnie
zgłaszała „czysto" na celowo zepsutym kodzie, sześć testów przeszło mimo zepsutej konfiguracji
domyślnej, a rejestr decyzji przez dobę ogłaszał wybór technologii odwrócony dzień wcześniej.

Każda z tych rzeczy została znaleziona **przez sprawdzenie, nie przez czytanie kodu**. Reguły
w `RULES.md` są zapisem tego, jak się je znajduje.

## Licencja

**[CC BY-SA 4.0](LICENSE)** — Uznanie autorstwa · Na tych samych warunkach 4.0 Międzynarodowe.

Copyright © 2026 Robert Sternal (tutum-pro).

Wolno kopiować, rozpowszechniać i adaptować, również komercyjnie, pod dwoma warunkami:
**wskazania autorstwa** oraz **udostępnienia utworów zależnych na tej samej licencji**.

Co to znaczy w praktyce:

- **Użycie wewnątrz firmy — bez żadnych zobowiązań.** Share-alike uruchamia się przy
  rozpowszechnianiu, nie przy stosowaniu. Adaptacja metody na wewnętrzne potrzeby zespołu
  czy klienta nie rodzi obowiązku publikacji.
- **Publikacja adaptacji — na CC BY-SA 4.0.** Wydając zmienioną wersję na zewnątrz,
  udostępniasz ją na tych samych warunkach.
- **Dokumenty wytworzone metodą nie są utworami zależnymi.** ADR-y, rejestry i plany powstałe
  w Twoim projekcie należą do Ciebie. Licencja obejmuje samą metodę — reguły, skille
  i szablony — a nie to, co przy ich użyciu napiszesz.

## Znaki towarowe

**Licencja nie udziela praw do nazw „archirules" ani „tutum-pro".**

Utwory zależne nie mogą używać tych nazw ani sugerować, że są firmowane, wspierane lub
zatwierdzone przez autora. Nazwij swoją adaptację inaczej — wskazanie źródła („na podstawie
archirules") jest wymagane przez licencję i jest w porządku; **posłużenie się nazwą jako
własną — nie**.

To rozróżnienie, a nie klauzula copyleft, jest tym, co realnie chroni tożsamość metody.
