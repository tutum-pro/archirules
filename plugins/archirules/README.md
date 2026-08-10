# archirules — wtyczka

Metoda prowadzenia projektu wytwórczego IT jako zestaw skilli dla Claude Code.

**Reguły:** [`RULES.md`](RULES.md) (kanoniczne, PL) · [`RULES.en.md`](RULES.en.md) (EN)

## Skille

| skill | do czego |
|---|---|
| `/archirules:bootstrap` | założenie rejestrów w projekcie, wybór języka dokumentacji |
| `/archirules:adr` | zapisanie, zastąpienie albo poprawienie decyzji |
| `/archirules:oq` | zarejestrowanie albo zamknięcie pytania otwartego |
| `/archirules:phases` | otwarcie fazy z kryterium akceptacji, zamknięcie z dowodem |
| `/archirules:audit` | audyt kompletności i prawdziwości rejestrów |
| `/archirules:language` | przełączenie języka dokumentacji projektu, całościowo |
| `/archirules:verification` | dyscyplina dowodu: udowodnij, że bramka pada |

Do każdego skilla można dopisać `--help`:

```
/archirules:adr --help
```

Wypisze, czego skill od ciebie potrzebuje i **czego nie zrobi**. Tekst pochodzi z sekcji
`## Usage` w tym samym `SKILL.md`, wyciąganej przez `scripts/help.py` — nie z pamięci modelu.
Skill dodany bez takiej sekcji zapala selftest na czerwono.

## Narzędzia

```
python3 scripts/conform.py docs/architecture      # zgodność strukturalna, wewnątrz plików
bash    scripts/selftest.sh                       # dowód, że powyższy potrafi paść
python3 scripts/consistency.py docs/architecture  # zgodność między rejestrami
bash    scripts/selftest-consistency.sh           # dowód, że powyższy potrafi paść
```

Dwa kontrolery, bo mają różne osie. `conform.py` czyta jeden plik naraz: sekcje rekordu decyzji,
numerację pytań, kształt tabeli faz. `consistency.py` czyta relacje **między** dokumentami,
których pierwszy nie widzi, bo każdy plik z osobna jest poprawny — pytanie kontra faza, którą
blokuje, zastąpienie zapisane w obie strony, odnośnik do rekordu, który już nie obowiązuje.

Ostatni przypadek w `selftest.sh` nie dotyczy żadnego rejestru: wymaga, żeby **każdy marker,
na którym opiera się którykolwiek kontroler, występował w szablonie albo w skillu**. Marker
wymyślony przez skrypt i honorowany wyłącznie przez jego własne dane testowe dowodzi zgodności
skryptu z samym sobą — patrz C-11 w kazuistyce.

`scripts/testdata/` to **dane wejściowe samotestu, nie przykłady do kopiowania** — najmniejsze
dokumenty spełniające kontroler, w dwóch językach, bo obsługę dwujęzyczną też trzeba czymś
pilnować.

## Szablony

`templates/pl/` i `templates/en/` — ADR, OQ, rejestr faz, rejestr weryfikacji, README.

Polski jest kanoniczny **dla treści metody** (`RULES.md`, szablony, ten plik). Angielski to
tłumaczenie; przy rozbieżności rozstrzyga polski.

**Warstwa wykonywalna jest po angielsku bez wyjątku:** skille, skrypty, metadane wtyczki.
`SKILL.md` konsumuje model w czasie działania i czyta każdy, kto instaluje wtyczkę — bliżej
mu do kodu niż do prozy. Język instrukcji nie determinuje języka wyniku: angielski skill
produkuje polskie ADR-y, jeśli taki jest język projektu.
Rozumowanie skupione jest w `RULES.md`, a szablony są celowo ubogie w prozę — żeby rozjazd
wersji miał gdzie nie powstać.

## Pierwsze użycie w projekcie

```
/archirules:bootstrap
```

Następnie wklej `CLAUDE.md.example` do `CLAUDE.md` projektu, żeby metoda obowiązywała bez
przypominania o niej w każdej sesji.

## Licencja

[CC BY-SA 4.0](../../LICENSE) · Copyright © 2026 Robert Sternal (tutum-pro).

Licencja nie udziela praw do nazw „archirules" ani „tutum-pro" — szczegóły w
[README repozytorium](../../README.md#znaki-towarowe).
