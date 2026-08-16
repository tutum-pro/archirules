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
# Several cases are not hypothetical. They are defects this checker had, each of which
# made it report a sound register as broken or a broken one as sound:
#
#   * a check keyed on a marker and a question number appearing on ONE line — a shape no
#     template produces. It could not fire, and nothing noticed, because it was the only
#     check here without a case of its own. Now cases 8 and 1 pin both directions.
#   * a `--lang` parser that accepted only the `=` form and silently detected the
#     language when given the spaced form the sibling checker documents. Case 17.
#   * a reference check that vanished entirely, without a word, when the set kept no
#     decisions/ directory. Case 14.
#
# The vocabulary these markers come from is asserted in selftest.sh, which checks both
# checkers at once: a marker no template produces is the defect that ADR-0006 is about.
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
PY="${1:-python3}"
CHK="$here/consistency.py"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
pass=0; fail=0

copy_of() { local d="$tmp/$1"; rm -rf "$d"; cp -r "$here/testdata/$2" "$d"; echo "$d"; }

ok()   { printf "  ok    %-56s %s\n" "$1" "$2"; pass=$((pass + 1)); }
bad()  { printf "  FAIL  %-56s %s\n" "$1" "$2"; fail=$((fail + 1)); }

expect() { # <description> <expected exit code> <directory> [extra args...]
  local what="$1" want="$2" dir="$3"; shift 3
  "$PY" "$CHK" "$dir" "$@" >/dev/null 2>&1
  local code=$?
  [ "$code" -eq "$want" ] && ok "$what" "exit $code" || bad "$what" "exit $code, expected $want"
}

expect_says() { # <description> <needle> <directory> [extra args...]
  # The output is captured BEFORE it is searched. Piping the checker straight into
  # grep looks equivalent and is not: under `pipefail` the checker's own exit code
  # outranks grep's, so every case whose subject also fails the register reads as
  # "printed nothing". A gate must not confuse a claim about output with an exit
  # status (rule W5) — this helper made that mistake and two cases went red for it.
  local what="$1" needle="$2" dir="$3"; shift 3
  local out
  out="$("$PY" "$CHK" "$dir" "$@" 2>&1)"
  if printf '%s' "$out" | grep -q "$needle"; then
    ok "$what" "said so"
  else
    bad "$what" "silent"
  fi
}

for lang in pl en; do
  set="xreg-$lang"
  echo "  --- $set ---"

  if [ "$lang" = "pl" ]; then
    phases=fazy-realizacji.md         ; blocks_field='**Blokuje:** X1'
    blocks='\*\*Blokuje:\*\*'         ; superseded='\*\*Status:\*\* ZASTĄPIONY'
    accepted='\*\*Status:\*\* Przyjęty$' ; accepted_plus='**Status:** Przyjęty · **Rozstrzyga:** OQ-02'
    plain_status='**Status:** Przyjęty'
    heading='### Co blokuje'           ; heading_full='### Co blokuje fazy ścieżki X'
    heading_alt='### Co blokuje fazy sciezki X (inaczej)' ; heading_gone='### Zależności'
    current=ADR-0004                   ; superseded_ref=ADR-0002
    resolved_status='\*\*Status:\*\* ROZSTRZYGNIĘTE' ; reopened='**Status:** OTWARTE'
    resolved_line='**Status:** ROZSTRZYGNIĘTE → [ADR-0009](decisions/ADR-0009-nieistotny.md), 2026-08-11 — nie wraca'
  else
    phases=phases.md                  ; blocks_field='**Blocks:** X1'
    blocks='\*\*Blocks:\*\*'          ; superseded='\*\*Status:\*\* SUPERSEDED'
    accepted='\*\*Status:\*\* Accepted$' ; accepted_plus='**Status:** Accepted · **Resolves:** OQ-02'
    plain_status='**Status:** Accepted'
    heading='### What blocks'          ; heading_full='### What blocks the phases of path X'
    heading_alt='### What blocks path X phases (reworded)' ; heading_gone='### Dependencies'
    current=ADR-0004                   ; superseded_ref=ADR-0002
    resolved_status='\*\*Status:\*\* RESOLVED' ; reopened='**Status:** OPEN'
    resolved_line='**Status:** RESOLVED → [ADR-0009](decisions/ADR-0009-irrelevant.md), 2026-08-11 — it does not'
  fi

  expect "a conforming set passes" 0 "$(copy_of "clean-$lang" "$set")"

  # --- A: a question against the phase status and the blocker table ----------
  # A question naming a phase the register does not know is not a finding by design:
  # the identifier may belong to a path label, not to a row.
  d="$(copy_of "c1-$lang" "$set")"
  sed -i.bak "s/$blocks X2/$blocks Z99/" "$d/open-questions.md"
  expect "question blocks a phase that does not exist" 0 "$d"

  d="$(copy_of "c2-$lang" "$set")"
  sed -i.bak 's/⛔ |/☐ |/' "$d/$phases"
  expect "phase ready despite an open blocking question" 1 "$d"

  d="$(copy_of "c3-$lang" "$set")"
  sed -i.bak '/^| X2 | \[OQ-01\]/d' "$d/$phases"
  expect "blocker row removed while the question still claims it" 1 "$d"

  # --- B: a phase waiting on a question -------------------------------------
  d="$(copy_of "c4-$lang" "$set")"
  sed -i.bak 's/OQ-01/OQ-77/g' "$d/$phases"
  expect "phase waits on a question that does not exist" 1 "$d"

  d="$(copy_of "c5-$lang" "$set")"
  sed -i.bak 's/OQ-01/OQ-02/g' "$d/$phases"
  expect "phase waits on a resolved question" 1 "$d"

  # --- C: a closed question that still declares a blocker --------------------
  # The check this replaces could not fire at all. Appending the field to the file
  # puts it inside the last question's block, which is the resolved one.
  d="$(copy_of "c6-$lang" "$set")"
  printf '\n%s\n' "$blocks_field" >> "$d/open-questions.md"
  expect "resolved question still declares what it blocks" 1 "$d"

  # --- D: references to decision records -------------------------------------
  d="$(copy_of "c7-$lang" "$set")"
  sed -i.bak 's/ADR-0003/ADR-0099/g' "$d/open-questions.md"
  expect "reference to a non-existent decision record" 1 "$d"

  d="$(copy_of "c8-$lang" "$set")"
  sed -i.bak "s/$current/$superseded_ref/g" "$d/open-questions.md"
  expect "entry points at a record that is superseded" 1 "$d"

  # --- E: non-contradiction of decision records ------------------------------
  d="$(copy_of "c9-$lang" "$set")"
  sed -i.bak "s|^$superseded.*$|$plain_status|" "$d"/decisions/ADR-0001-*.md
  expect "one-way supersession link (target status stays silent)" 1 "$d"

  d="$(copy_of "c10-$lang" "$set")"
  sed -i.bak "s|^$accepted|$accepted_plus|" "$d"/decisions/ADR-0004-*.md
  expect "two records resolve one question, no link between them" 1 "$d"

  # A decision that settles a question, against a question that still calls itself
  # open. Neither file reveals it alone: the decision reads as final, the question
  # reads as unanswered, and each is internally consistent. Found in a live register.
  d="$(copy_of "c10a-$lang" "$set")"
  sed -i.bak "s|^$resolved_status.*|$reopened|" "$d/open-questions.md"
  expect "record resolves a question that still calls itself open" 1 "$d"

  # The other direction: the question is closed, but by a different record than the
  # one claiming to have closed it. A one-way link, and the reader of either file is
  # told something true about that file and false about the pair.
  d="$(copy_of "c10b-$lang" "$set")"
  sed -i.bak "s|^$resolved_status.*|$resolved_line|" "$d/open-questions.md"
  expect "question is closed by a record other than the one claiming it" 1 "$d"

  # A SUPERSEDED record keeps its original "resolves" line — that is its history. The
  # question rightly names the record in force, so this must NOT be reported.
  d="$(copy_of "c10c-$lang" "$set")"
  expect "superseded record keeping its resolves line is not a finding" 0 "$d"

  # --- guards against the checker's own past defects -------------------------
  # A reworded heading is not a deviation: the prefix must still match, so the correct
  # outcome here is 0. An exact-match checker reports a sound set as broken.
  d="$(copy_of "c11-$lang" "$set")"
  sed -i.bak "s|^$heading_full|$heading_alt|" "$d/$phases"
  expect "reworded blocker heading is still matched (not a finding)" 0 "$d"

  # The opposite case: no blocker table at all. Also not a failure — the table is a
  # project convention, not part of the method. But the skip MUST be visible, or
  # "0 problems" silently means "0 checks ran".
  d="$(copy_of "c12-$lang" "$set")"
  sed -i.bak "s|^$heading|$heading_gone|" "$d/$phases"
  expect_says "absent blocker table is reported, not passed over" "skipped" "$d"

  # Same rule, the case that used to break it: with no decisions/ directory the
  # reference checks disappeared entirely and said nothing at all.
  d="$(copy_of "c13-$lang" "$set")"
  rm -rf "$d/decisions"
  expect_says "absent decisions/ is reported, not passed over" "skipped" "$d"
  expect "absent decisions/ is not itself a finding" 0 "$d"

  # A wrong language guess makes every marker miss and buries the real findings under
  # spurious ones. Undetectable language is itself the finding.
  d="$(copy_of "c14-$lang" "$set")"
  rm -f "$d/README.md"
  expect "language undetectable is reported, not guessed" 1 "$d"

  # Forcing the language must actually take effect: run the other language's set with
  # this one's markers and require the mismatch to surface. BOTH spellings — the spaced
  # form used to be accepted and then silently ignored, which is the worst of the three
  # possible behaviours because it looks like success.
  other=$([ "$lang" = "pl" ] && echo en || echo pl)
  d="$(copy_of "c15-$lang" "xreg-$other")"
  expect "--lang=$lang contradicts the README and is reported" 1 "$d" "--lang=$lang"
  expect "--lang $lang, spaced, is honoured the same way" 1 "$d" "--lang" "$lang"
  # Pin the REASON, not just the code. The forced language used to be caught only by
  # the findings it happened to produce downstream; when those checks moved, the case
  # passed for no reason at all and then stopped passing.
  expect_says "and the reason given is the contradiction itself" \
    "README.md reads as $other" "$d" "--lang=$lang"

  # An unsupported language is a usage error, not a defective register, and the two
  # must not share an exit code (rule W1: refuse rather than guess).
  expect "--lang with no marker table refuses, exit 2" 2 "$d" "--lang=klingon"
done

# Not an exit code: a claim about what the checker actually printed. A checker that
# died on a syntax error exits 1, which is indistinguishable from "defect found" in
# every case above. This one tells them apart.
echo "  --- the checker ran at all ---"
expect_says "the English set is reported as English" "language: en" "$here/testdata/xreg-en"

printf "\n  %d passed, %d failed\n" "$pass" "$fail"
if [ "$fail" -ne 0 ]; then
  echo "  THE CROSS-REGISTER CHECKER IS NOT TRUSTWORTHY"
fi
[ "$fail" -eq 0 ]
