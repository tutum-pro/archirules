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

## Zaczynamy — od zera do działającego rejestru

### Czego potrzebujesz

- **Claude Code** (CLI, aplikacja albo rozszerzenie do IDE),
- katalog projektu, najlepiej będący repozytorium git.

Nic poza tym. Wtyczka nie instaluje zależności ani nie uruchamia usług.

### 1. Dodaj marketplace — raz na maszynę

W Claude Code wpisz:

```
/plugin marketplace add tutum-pro/archirules
```

To rejestruje **źródło** wtyczek. Robi się to raz; kolejne projekty na tej samej maszynie już
tego nie wymagają.

### 2. Zainstaluj wtyczkę

```
/plugin install archirules@archirules
```

Zapis to `nazwa-wtyczki@nazwa-marketplace'u` — i warto wiedzieć, **skąd te nazwy się biorą**,
bo żadna z nich nie wynika ze ścieżki repozytorium.

Dodając marketplace w kroku 1, podałeś **ścieżkę na GitHubie** (`tutum-pro/archirules`).
Claude pobrał z niej plik `.claude-plugin/marketplace.json` i zarejestrował źródło pod nazwą,
którą ten plik **deklaruje w polu `name`** — tutaj `archirules`. Od tej chwili ścieżka
repozytorium nie jest już do niczego potrzebna; posługujesz się zadeklarowaną nazwą.

Wtyczka nazywa się tak samo, bo repozytorium zawiera jedną wtyczkę o nazwie `archirules` —
stąd `archirules@archirules`. Gdyby pole `name` marketplace'u brzmiało inaczej, na przykład
`tutum-metoda`, instalowałbyś `archirules@tutum-metoda` **z tego samego repozytorium**.

Alternatywnie: `/plugin` otwiera przeglądarkę wtyczek, w której można ją znaleźć na liście.

Po instalacji sprawdź, czy skille są widoczne — wpisz `/archirules:` i powinna pojawić się
podpowiedź z siedmioma pozycjami.

### 3. Uruchom bootstrap **w katalogu projektu**

Otwórz Claude Code w katalogu projektu i wpisz:

```
/archirules:bootstrap
```

**Co się wydarzy.** Zostaniesz zapytany o dwie rzeczy:

- **język dokumentacji** — polski albo angielski; decyduje o szablonach i nazwach plików,
  i nie jest wyborem na zawsze (patrz `/archirules:language`);
- **czy projekt zaczyna się od modelu procesu biznesowego** — jeśli tak, powstanie też miejsce
  na modele.

Następnie powstanie:

```
docs/architecture/
  README.md              indeks decyzji + sekcja „Wymagania obowiązujące"
  decisions/             pusty, na rekordy decyzji
  open-questions.md      rejestr pytań otwartych
  fazy-realizacji.md     rejestr faz z kryteriami akceptacji
```

**Projekt, który już ma `docs/architecture/`, nie zostanie nadpisany.** Bootstrap zgłosi, co
zastał, i zaproponuje uzupełnienie brakujących elementów.

### 4. Zgódź się na wpis do `CLAUDE.md`

Bootstrap zaproponuje dopisanie fragmentu do `CLAUDE.md` projektu. **To jest krok, który
sprawia, że metoda obowiązuje bez proszenia o nią w każdej sesji** — bez niego skille istnieją,
ale trzeba je wołać ręcznie.

Fragment jest krótki i możesz go obejrzeć przed zgodą: `CLAUDE.md.pl.example` albo
`CLAUDE.md.en.example` we wtyczce.

### 5. Sprawdź, że wyszło

```
/archirules:audit
```

albo bezpośrednio:

```
SCRIPTS=~/.claude/plugins/marketplaces/archirules/plugins/archirules/scripts
python3 $SCRIPTS/conform.py docs/architecture       # wewnątrz plików
python3 $SCRIPTS/consistency.py docs/architecture   # między rejestrami
```

Zero naruszeń i kod wyjścia 0 znaczy, że rejestr jest kompletny strukturalnie i że rejestry nie
przeczą sobie nawzajem. Świeżo założony zawsze taki jest — sens tych kontroli pojawia się
później, gdy dokumentów przybędzie.

### Co dalej

| chcesz | wpisz |
|---|---|
| zapisać decyzję | `/archirules:adr` |
| zapisać wątpliwość, na którą nie ma teraz odpowiedzi | `/archirules:oq` |
| otworzyć fazę z kryterium akceptacji | `/archirules:phases` |
| sprawdzić, czy rejestr nie skłamał | `/archirules:audit` |
| dodać bramkę i udowodnić, że pada | `/archirules:verification` |
| przełączyć projekt na inny język | `/archirules:language` |

## Skąd się to wzięło

Z projektu, w którym po kilku dniach pracy okazało się między innymi, że bramka kontrolna
dwukrotnie zgłaszała „czysto" na celowo zepsutym kodzie, sześć testów przeszło mimo zepsutej
konfiguracji domyślnej, a rejestr decyzji przez dobę ogłaszał wybór technologii odwrócony dzień
wcześniej.

Każda z tych rzeczy została znaleziona **przez sprawdzenie, nie przez czytanie kodu**.

Dziesięć takich przypadków opisuje [`CASEBOOK.md`](plugins/archirules/CASEBOOK.md) — osobno od
reguł, celowo. **Regułę ma dać się zastosować bez znajomości cudzego projektu**, a przypadek
jest dowodem dla tych, którzy chcą wiedzieć, dlaczego brzmi właśnie tak.

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
