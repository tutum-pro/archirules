#!/usr/bin/env bash
# Prove that consistency.py CAN FAIL. Without this, its "0 problems" means nothing.
#
# Rule W4: a check that cannot fail looks exactly like a check that passes. This script
# takes a known-good register set, breaks a copy of it in one specific way, and requires
# the checker to notice — once per class of defect it claims to find, and once per
# language it claims to support.
#
#   selftest-consistency.sh [python]
#
# Six of these cases are not hypothetical. They are defects this checker itself had on
# its first run against a real register set of 22 decision records, each of which made it
# report a sound register as broken or a broken one as sound. They stay here as guards.
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
PY="${1:-python3}"
CHK="$here/consistency.py"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
pass=0; fail=0

copy_of() { local d="$tmp/$1"; rm -rf "$d"; cp -r "$here/testdata/$2" "$d"; echo "$d"; }

expect() { # <description> <expected exit code> <directory>
  "$PY" "$CHK" "$3" >/dev/null 2>&1
  local code=$?
  if [ "$code" -eq "$2" ]; then
    printf "  ok    %-54s exit %s\n" "$1" "$code"; pass=$((pass + 1))
  else
    printf "  FAIL  %-54s exit %s, expected %s\n" "$1" "$code" "$2"; fail=$((fail + 1))
  fi
}

for lang in pl en; do
  set="xreg-$lang"
  echo "  --- $set ---"

  if [ "$lang" = "pl" ]; then
    phases=fazy-realizacji.md
    blocks='\*\*Blokuje:\*\*'      ; modified_by='\*\*Zmodyfikowany przez:\*\*'
    what_changed='## Co zostało zmienione' ; resolves='**Rozstrzyga:** OQ-02'
    heading='### Co blokuje'       ; heading_full='### Co blokuje fazy ścieżki X'
    heading_alt='### Co blokuje fazy sciezki X (inaczej)' ; heading_gone='### Zależności'
    accepted='\*\*Status:\*\* Przyjęty$' ; accepted_plus='**Status:** Przyjęty · '
    a_base=ADR-0001-podstawa.md    ; a_free=ADR-0004-niezalezny.md
  else
    phases=phases.md
    blocks='\*\*Blocks:\*\*'       ; modified_by='\*\*Modified by:\*\*'
    what_changed='## What changed'  ; resolves='**Resolves:** OQ-02'
    heading='### What blocks'      ; heading_full='### What blocks the phases of path X'
    heading_alt='### What blocks path X phases (reworded)' ; heading_gone='### Dependencies'
    accepted='\*\*Status:\*\* Accepted$' ; accepted_plus='**Status:** Accepted · '
    a_base=ADR-0001-base.md        ; a_free=ADR-0004-unconnected.md
  fi

  expect "a conforming set passes" 0 "$(copy_of "clean-$lang" "$set")"

  # A question naming a phase the register does not know is not a finding by design:
  # the identifier may belong to a path label, not to a row.
  d="$(copy_of "c1-$lang" "$set")"
  sed -i.bak "s/$blocks X2/$blocks Z99/" "$d/open-questions.md"
  expect "question blocks a phase that does not exist" 0 "$d"

  # --- B: a phase waiting on a question -------------------------------------
  d="$(copy_of "c2-$lang" "$set")"
  sed -i.bak 's/OQ-01/OQ-77/g' "$d/$phases"
  expect "phase waits on a question that does not exist" 1 "$d"

  d="$(copy_of "c3-$lang" "$set")"
  sed -i.bak 's/OQ-01/OQ-02/g' "$d/$phases"
  expect "phase waits on a resolved question" 1 "$d"

  # --- D: references to decision records -------------------------------------
  d="$(copy_of "c4-$lang" "$set")"
  sed -i.bak 's/ADR-0003/ADR-0099/g' "$d/open-questions.md"
  expect "reference to a non-existent decision record" 1 "$d"

  # --- A: a question against the phase status and the blocker table ----------
  d="$(copy_of "c5-$lang" "$set")"
  sed -i.bak 's/⛔ |/☐ |/' "$d/$phases"
  expect "phase ready despite an open blocking question" 1 "$d"

  d="$(copy_of "c6-$lang" "$set")"
  sed -i.bak '/^| X2 | \[OQ-01\]/d' "$d/$phases"
  expect "blocker row removed while the question still claims it" 1 "$d"

  # --- E: non-contradiction of decision records ------------------------------
  d="$(copy_of "c7-$lang" "$set")"
  sed -i.bak "s/ · $modified_by.*$//" "$d/decisions/$a_base"
  expect "one-way modification link (target stays silent)" 1 "$d"

  d="$(copy_of "c8-$lang" "$set")"
  sed -i.bak "s|^$what_changed|## Notes|" "$d/decisions/$a_base"
  expect "modified record does not say what changed" 1 "$d"

  d="$(copy_of "c9-$lang" "$set")"
  sed -i.bak "s|^$accepted|$accepted_plus$resolves|" "$d/decisions/$a_free"
  expect "two records resolve one question, no link between them" 1 "$d"

  # --- guards against the checker's own past defects -------------------------
  # A reworded heading is not a deviation: the prefix must still match, so the correct
  # outcome here is 0. An exact-match checker reports a sound set as broken.
  d="$(copy_of "c10-$lang" "$set")"
  sed -i.bak "s|^$heading_full|$heading_alt|" "$d/$phases"
  expect "reworded blocker heading is still matched (not a finding)" 0 "$d"

  # The opposite case: no blocker table at all. Also not a failure — the table is a
  # project convention, not part of the method. But the skip MUST be visible, or
  # "0 problems" silently means "0 checks ran".
  d="$(copy_of "c11-$lang" "$set")"
  sed -i.bak "s|^$heading|$heading_gone|" "$d/$phases"
  if "$PY" "$CHK" "$d" 2>&1 | grep -q "skipped"; then
    printf "  ok    %-54s reported\n" "absent blocker table is reported, not passed over"
    pass=$((pass + 1))
  else
    printf "  FAIL  %-54s silent\n" "absent blocker table is reported, not passed over"
    fail=$((fail + 1))
  fi

  # A wrong language guess makes every marker miss and buries the real findings under
  # spurious ones. Undetectable language is itself the finding.
  d="$(copy_of "c12-$lang" "$set")"
  rm -f "$d/README.md"
  expect "language undetectable is reported, not guessed" 1 "$d"

  # Forcing the language must actually take effect: run the other language's set with
  # this one's markers and require the mismatch to surface.
  other=$([ "$lang" = "pl" ] && echo en || echo pl)
  d="$(copy_of "c13-$lang" "xreg-$other")"
  "$PY" "$CHK" "$d" --lang="$lang" >/dev/null 2>&1
  code=$?      # must be captured here: $? inside the `if` would be the previous test's
  if [ "$code" -ne 0 ]; then
    printf "  ok    %-54s exit %s\n" "--lang overrides detection (markers then miss)" "$code"
    pass=$((pass + 1))
  else
    printf "  FAIL  %-54s exit 0\n" "--lang overrides detection (markers then miss)"
    fail=$((fail + 1))
  fi
done

printf "\n  %d passed, %d failed\n" "$pass" "$fail"
[ "$fail" -eq 0 ]
