# archirules — wtyczka

Metoda prowadzenia projektu wytwórczego IT jako zestaw skilli dla Claude Code.

**Reguły:** [`RULES.md`](RULES.md) (kanoniczne, PL) · [`RULES.en.md`](RULES.en.md) (EN)

## Skille

| skill | do czego |
|---|---|
| `/archirules:bootstrap` | założenie rejestrów w projekcie, wybór języka dokumentacji |
| `/archirules:adr` | zapisanie, zastąpienie albo poprawienie decyzji |
| `/archirules:oq` | zarejestrowanie albo zamknięcie pytania otwartego |
| `/archirules:fazy` | otwarcie fazy z kryterium akceptacji, zamknięcie z dowodem |
| `/archirules:audyt` | audyt kompletności i prawdziwości rejestrów |
| `/archirules:weryfikacja` | dyscyplina dowodu: udowodnij, że bramka pada |

## Szablony

`templates/pl/` i `templates/en/` — ADR, OQ, rejestr faz, rejestr weryfikacji, README.

Polski jest kanoniczny. Angielski to tłumaczenie; **przy rozbieżności rozstrzyga polski**.
Rozumowanie skupione jest w `RULES.md`, a szablony są celowo ubogie w prozę — żeby rozjazd
wersji miał gdzie nie powstać.

## Pierwsze użycie w projekcie

```
/archirules:bootstrap
```

Następnie wklej `CLAUDE.md.example` do `CLAUDE.md` projektu, żeby metoda obowiązywała bez
przypominania o niej w każdej sesji.
