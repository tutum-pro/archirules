#!/usr/bin/env bash
# Prove that conform.py CAN FAIL. Without this, its "0 problems" means nothing.
#
# Rule W4: a check that cannot fail looks exactly like a check that passes. This
# script takes a known-good documentation set, breaks a copy of it in a specific
# way, and requires the checker to notice — once per kind of defect it claims to
# find, and once per language it claims to support.
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
failed=0
case_no=0

# expect <description> <expected exit code> <directory>
expect() {
  python3 "$here/conform.py" "$3" >/dev/null 2>&1
  local code=$?
  case_no=$((case_no + 1))
  if [ "$code" -eq "$2" ]; then
    printf "  ok    %-46s exit %s\n" "$1" "$code"
  else
    printf "  FAIL  %-46s exit %s, expected %s\n" "$1" "$code" "$2"
    failed=1
  fi
}

# break <name> <source set> -> prints the path of a broken copy
copy_of() {
  local dest="$tmp/$1"
  cp -r "$here/testdata/$2" "$dest"
  echo "$dest"
}

for lang in pl en; do
  set="valid-$lang"
  echo "  --- $set ---"

  expect "a conforming set passes" 0 "$(copy_of "clean-$lang" "$set")"

  d=$(copy_of "cost-$lang" "$set")
  if [ "$lang" = pl ]; then sed -i.bak 's/\*\*Koszt\./**Uwagi./' "$d"/decisions/ADR-*.md
  else sed -i.bak 's/\*\*Cost\./**Notes./' "$d"/decisions/ADR-*.md; fi
  expect "missing costs section is caught" 1 "$d"

  d=$(copy_of "impl-$lang" "$set")
  if [ "$lang" = pl ]; then sed -i.bak 's/## Stan realizacji/## Notatki/' "$d"/decisions/ADR-*.md
  else sed -i.bak 's/## Implementation status/## Notes/' "$d"/decisions/ADR-*.md; fi
  expect "missing implementation status is caught" 1 "$d"

  d=$(copy_of "gap-$lang" "$set")
  printf '\n### OQ-05 — A gap in the numbering\n**Status:** OPEN\n' >> "$d/open-questions.md"
  expect "a gap in question numbering is caught" 1 "$d"

  d=$(copy_of "detached-$lang" "$set")
  perl -0pi -e 's/(### OQ-01 —[^\n]*\n)/$1\n/' "$d/open-questions.md"
  expect "status detached from its heading is caught" 1 "$d"

  d=$(copy_of "index-$lang" "$set")
  printf '| [0002](decisions/ADR-0002-none.md) | Not there | Accepted |\n' >> "$d/README.md"
  expect "index disagreeing with decisions/ is caught" 1 "$d"

  d=$(copy_of "link-$lang" "$set")
  if [ "$lang" = pl ]; then sed -i.bak 's/(fazy-realizacji.md)/(nie-ma-takiego.md)/' "$d/README.md"
  else sed -i.bak 's/(phases.md)/(no-such-file.md)/' "$d/README.md"; fi
  expect "a link pointing nowhere is caught" 1 "$d"

  d=$(copy_of "verif-$lang" "$set")
  rm -f "$d"/rejestr-weryfikacji.md "$d"/verification.md
  expect "missing verification register is caught" 1 "$d"
done

# The language claim itself: the English set must be detected as English. If
# detection silently fell back to Polish, the English markers would not match and
# the conforming set above would have failed - so this asserts the reason, not
# just the result.
detected=$(python3 "$here/conform.py" "$here/testdata/valid-en" | sed -n 's/.*language: \([a-z]*\).*/\1/p')
case_no=$((case_no + 1))
if [ "$detected" = "en" ]; then
  printf "  ok    %-46s\n" "English set is detected as English"
else
  printf "  FAIL  %-46s detected '%s'\n" "English set is detected as English" "$detected"
  failed=1
fi

echo
if [ "$failed" -eq 0 ]; then
  echo "  $case_no cases: the checker fails when it should, in both languages"
else
  echo "  THE CHECKER IS NOT TRUSTWORTHY"
fi
exit $failed
