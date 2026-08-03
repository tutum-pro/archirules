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

## Narzędzia

```
python3 scripts/conform.py docs/architecture   # kontrola zgodności strukturalnej
bash    scripts/selftest.sh                    # dowód, że kontroler potrafi paść
```

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
