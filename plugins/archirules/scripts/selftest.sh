#!/usr/bin/env bash
# Dowodzi, że conform.py POTRAFI PAŚĆ — bez tego jego „zero naruszeń" nic nie znaczy.
#
# Reguła W4: kontrola, która nie potrafi paść, wygląda identycznie jak kontrola,
# która przechodzi. Ten skrypt psuje kopię poprawnego zestawu na cztery sposoby
# i wymaga, żeby każdy z nich został wykryty.
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
ok="$here/fixtures/ok"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
fail=0

expect() { # nazwa, oczekiwany kod, katalog
  python3 "$here/conform.py" "$3" >/dev/null 2>&1
  local rc=$?
  if [ "$rc" -eq "$2" ]; then printf "  ok    %-42s kod %s\n" "$1" "$rc"
  else printf "  BŁĄD  %-42s kod %s, oczekiwano %s\n" "$1" "$rc" "$2"; fail=1; fi
}

cp -r "$ok" "$tmp/clean"; expect "zestaw poprawny przechodzi" 0 "$tmp/clean"

cp -r "$ok" "$tmp/a"; sed -i.bak 's/\*\*Koszt\./**Uwagi./' "$tmp/a/decisions/ADR-0001-przyklad.md"
expect "brak sekcji kosztów wykryty" 1 "$tmp/a"

cp -r "$ok" "$tmp/b"; sed -i.bak 's/## Stan realizacji/## Notatki/' "$tmp/b/decisions/ADR-0001-przyklad.md"
expect "brak stanu realizacji wykryty" 1 "$tmp/b"

cp -r "$ok" "$tmp/c"
printf '\n### OQ-05 — Luka w numeracji\n**Status:** OTWARTE\n' >> "$tmp/c/open-questions.md"
expect "luka w numeracji OQ wykryta" 1 "$tmp/c"

cp -r "$ok" "$tmp/d"
perl -0pi -e 's/(### OQ-01 —[^\n]*\n)/$1\n/' "$tmp/d/open-questions.md"
expect "Status oderwany od nagłówka wykryty" 1 "$tmp/d"

cp -r "$ok" "$tmp/e"; rm "$tmp/e/rejestr-weryfikacji.md"
expect "brak rejestru weryfikacji wykryty" 1 "$tmp/e"

[ "$fail" -eq 0 ] && echo "  kontroler potrafi paść na wszystkich sześciu wadach" || echo "  KONTROLER NIE JEST WIARYGODNY"
exit $fail
