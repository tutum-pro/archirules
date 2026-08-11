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

# expect <description> <expected exit code> <directory> [extra args...]
expect() {
  local what="$1" want="$2" dir="$3"; shift 3
  python3 "$here/conform.py" "$dir" "$@" >/dev/null 2>&1
  local code=$?
  case_no=$((case_no + 1))
  if [ "$code" -eq "$want" ]; then
    printf "  ok    %-46s exit %s\n" "$what" "$code"
  else
    printf "  FAIL  %-46s exit %s, expected %s\n" "$what" "$code" "$want"
    failed=1
  fi
}

# expect_says <description> <needle> <directory> [extra args...]
# An exit code says a defect was found; it does not say WHICH. Where a case could
# pass for an unrelated reason, the reason itself is pinned here. The output is
# captured before it is searched: piped straight into grep, `pipefail` would let
# the checker's own exit code outrank grep's and every real finding would read as
# "printed nothing" (rule W5).
expect_says() {
  local what="$1" needle="$2" dir="$3"; shift 3
  local out
  out="$(python3 "$here/conform.py" "$dir" "$@" 2>&1)"
  case_no=$((case_no + 1))
  if printf '%s' "$out" | grep -q "$needle"; then
    printf "  ok    %-46s said so\n" "$what"
  else
    printf "  FAIL  %-46s silent\n" "$what"
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

  d=$(copy_of "drift-$lang" "$set")
  perl -0pi -e 's/^### OQ-(\d+) — /### OQ-$1: /gm' "$d/open-questions.md"
  expect "a drifted question-heading format is caught" 1 "$d"

  d=$(copy_of "nolang-$lang" "$set")
  if [ "$lang" = pl ]; then sed -i.bak 's/Wymagania obowiązujące/Wymagania inne/' "$d/README.md"
  else sed -i.bak 's/Binding requirements/Other requirements/' "$d/README.md"; fi
  expect "undetectable documentation language is caught" 1 "$d"

  d=$(copy_of "verif-$lang" "$set")
  rm -f "$d"/rejestr-weryfikacji.md "$d"/verification.md
  expect "missing verification register is caught" 1 "$d"

  # A supersession has to say WHICH part stopped holding, because often only part of
  # it did (rule P7). The scope belongs in the status line and not in a section below
  # it — a correction sitting above a field that still lies is not one (case C-04).
  # Both directions are pinned: a bare pointer is a finding, a stated scope is not.
  if [ "$lang" = pl ]; then
    bare='**Status:** ZASTĄPIONY przez ADR-0002'
    scoped='**Status:** ZASTĄPIONY przez ADR-0002, 2026-08-11 — wyłącznie punkt drugi'
    was='\*\*Status:\*\* Przyjęty'
  else
    bare='**Status:** SUPERSEDED by ADR-0002'
    scoped='**Status:** SUPERSEDED by ADR-0002, 2026-08-11 — the second point only'
    was='\*\*Status:\*\* Accepted'
  fi

  d=$(copy_of "scope-$lang" "$set")
  sed -i.bak "s|^$was|$bare|" "$d"/decisions/ADR-*.md
  expect "a supersession naming no scope is caught" 1 "$d"
  expect_says "and it is caught for that reason" "names no scope" "$d"

  d=$(copy_of "scoped-$lang" "$set")
  sed -i.bak "s|^$was|$scoped|" "$d"/decisions/ADR-*.md
  expect "a supersession that names its scope passes" 0 "$d"

  # Forcing a language the register does not use makes every marker miss, so the run
  # finds nothing and looks exactly like a run that found nothing wrong. The language
  # skill asks a human to confirm the detected language; this is that check.
  other=$([ "$lang" = "pl" ] && echo en || echo pl)
  d=$(copy_of "forced-$lang" "$set")
  expect "--lang contradicting the README is caught" 1 "$d" --lang "$other"
  expect_says "and it names the contradiction" "README.md reads as $lang" "$d" --lang "$other"
  expect "--lang with no marker table refuses, exit 2" 2 "$d" --lang klingon
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

# The vocabulary claim, for BOTH checkers (ADR-0006). Every marker string a checker
# keys on has to occur in a template or in a skill. A marker invented by a script and
# honoured only by its own fixtures proves the script consistent with its test data,
# which was never in doubt — and that is exactly how a check that could not fire
# survived twenty-eight passing cases. This is the only assertion here that leaves
# the fixtures entirely, which is the whole reason it can see what they cannot.
missing=$(python3 - "$here" <<'PY'
import importlib.util
import os
import sys

scripts = sys.argv[1]
root = os.path.dirname(scripts)               # plugins/archirules
prose = []
for sub in ("templates", "skills"):
    for path, _, names in os.walk(os.path.join(root, sub)):
        for name in names:
            if name.endswith(".md"):
                with open(os.path.join(path, name), encoding="utf-8") as fh:
                    prose.append(fh.read())
prose = "\n".join(prose)

absent = []
for script in ("conform.py", "consistency.py", "trace.py"):
    spec = importlib.util.spec_from_file_location(script[:-3], os.path.join(scripts, script))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # MARKERS is {language: {key: wording}}; TRAILERS is {key: wording} and has no
    # language axis, because a git trailer is part of the executable layer and that
    # layer is English without exception (ADR-0001).
    tables = {}
    if hasattr(module, "MARKERS"):
        tables.update(module.MARKERS)
    if hasattr(module, "TRAILERS"):
        tables["trailer"] = module.TRAILERS
    if not tables:
        absent.append("%s exposes neither MARKERS nor TRAILERS to check" % script)
    for language, markers in tables.items():
        for key, value in markers.items():
            # a few markers are anchored regexes: drop the syntax, keep the wording
            wording = value.replace("^", "").replace("\\", "")
            if wording not in prose:
                absent.append("%s %s:%s = %r" % (script, language, key, wording))
# A sentinel, not an empty result. If loading a checker raises — a syntax error, a
# renamed table — the program dies and prints nothing, and "nothing" would read as
# "nothing missing". The assertion would then pass BECAUSE the thing it measures
# stopped working, which is the shape of failure this whole file exists to catch.
print("\n".join(sorted(set(absent))) or "VOCABULARY-OK")
PY
)
case_no=$((case_no + 1))
if [ "$missing" = "VOCABULARY-OK" ]; then
  printf "  ok    %-46s\n" "every marker occurs in a template or a skill"
else
  printf "  FAIL  %-46s\n" "markers no template or skill produces:"
  echo "${missing:-(the vocabulary check itself did not run)}" | sed 's/^/        /'
  failed=1
fi

# The explanation claim (ADR-0011). The help skill describes the method to somebody who
# has not read it, which is the one text here nobody can check by recognising what it
# refers to. So every rule, case, script and skill it names must exist — and it must name
# no entry from this repository's own registers, because a reader of the plugin does not
# have them. Prose that cannot be verified stays prose; references are verified.
explained=$(python3 - "$here" <<'PY'
import os
import re
import sys

scripts = sys.argv[1]
root = os.path.dirname(scripts)
path = os.path.join(root, "skills", "help", "SKILL.md")
try:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    with open(os.path.join(root, "CASEBOOK.en.md"), encoding="utf-8") as fh:
        casebook = fh.read()
    with open(os.path.join(root, "RULES.en.md"), encoding="utf-8") as fh:
        rules = fh.read()
except OSError as exc:
    print("unreadable: %s" % exc)
    raise SystemExit(0)

wrong = []
for case in sorted(set(re.findall(r"\bC-\d{2}\b", text))):
    if "## %s " % case not in casebook:
        wrong.append("names %s, which is not in the casebook" % case)
for rule in sorted(set(re.findall(r"\b([PW]\d{1,2})\b(?=[ .,)])", text))):
    if "### %s." % rule not in rules:
        wrong.append("names rule %s, which is not in RULES.en.md" % rule)
for script in sorted(set(re.findall(r"\b([a-z-]+\.(?:py|sh))\b", text))):
    if not os.path.isfile(os.path.join(scripts, script)):
        wrong.append("names %s, which is not in scripts/" % script)
for skill in sorted(set(re.findall(r"/archirules:([a-z]+)", text))):
    if not os.path.isfile(os.path.join(root, "skills", skill, "SKILL.md")):
        wrong.append("names /archirules:%s, which is not a skill" % skill)
# A reader of the plugin has no access to this repository's registers, so a reference to
# one is a rule that cannot be used without knowing somebody else's project history.
for entry in sorted(set(re.findall(r"\b(?:ADR-\d{4}|OQ-\d{2})\b", text))):
    wrong.append("names %s — this repository's own register, which a reader does not have"
                 % entry)
print("\n".join(wrong) or "EXPLANATION-OK")
PY
)
case_no=$((case_no + 1))
if [ "$explained" = "EXPLANATION-OK" ]; then
  printf "  ok    %-46s\n" "every reference in the help text resolves"
else
  printf "  FAIL  %-46s\n" "the help text refers to things that do not exist:"
  echo "${explained:-(the explanation check itself did not run)}" | sed 's/^/        /'
  failed=1
fi

# The traceability claim (ADR-0010). trace.py needs real commits, so this builds a
# throwaway repository rather than a fixture directory: the thing under test is what git
# history says, and a fixture cannot have history.
tr="$tmp/trace-repo"
mkdir -p "$tr/docs/architecture/decisions"
cat > "$tr/docs/architecture/phases.md" <<'MD'
# Phase register

**Legend:** `☐` not started · `☑` complete

| | Phase | Status | Acceptance criterion |
|---|---|---|---|
| T1 | First | ☑ 2026-08-11 | it exists |
| T2 | Second | ☐ | later |

**Hard gate:** none.
MD
printf '# Open questions\n\n### OQ-01 — A question\n**Status:** OPEN\n\nText.\n' \
  > "$tr/docs/architecture/open-questions.md"
printf '# ADR-0001 — A decision\n\n**Status:** Accepted\n\n## Decision\n\nX.\n' \
  > "$tr/docs/architecture/decisions/ADR-0001-a.md"
(
  cd "$tr" || exit 1
  git init -q && git config user.email t@t && git config user.name T
  git add -A && git commit -q -m "First phase" -m "Archirules-Phase: T1
Archirules-ADR: 0001
Archirules-OQ: 01"
) >/dev/null 2>&1

traced() { python3 "$here/trace.py" "$tr/docs/architecture" "$@" >/dev/null 2>&1; echo $?; }
trace_case() { # <description> <expected exit> [args...]
  local what="$1" want="$2"; shift 2
  local code; code=$(traced "$@")
  case_no=$((case_no + 1))
  if [ "$code" -eq "$want" ]; then
    printf "  ok    %-46s exit %s\n" "trace: $what" "$code"
  else
    printf "  FAIL  %-46s exit %s, expected %s\n" "trace: $what" "$code" "$want"
    failed=1
  fi
}

traced --write >/dev/null
trace_case "a fully traced repository passes" 0
trace_case "and passes --strict too" 0 --strict

# A trailer naming an entry no register holds. Same class as a dangling reference to a
# decision record, and the one check here safe to enforce in any repository.
(cd "$tr" && git commit -q --allow-empty -m "Phantom" -m "Archirules-Phase: T9") >/dev/null 2>&1
trace_case "a trailer naming a missing entry is caught" 1
(cd "$tr" && git reset -q --hard HEAD~1) >/dev/null 2>&1

# The generated view must be a regeneration, not a document somebody edited.
traced --write >/dev/null
sed -i.bak 's/| T2 | ☐ | — |/| T2 | ☑ | `deadbee` |/' "$tr/docs/architecture/traceability.md"
trace_case "a hand-edited view is caught" 1
traced --write >/dev/null; rm -f "$tr/docs/architecture/"*.bak

mv "$tr/docs/architecture/traceability.md" "$tmp/view.md"
trace_case "a missing view is caught" 1
mv "$tmp/view.md" "$tr/docs/architecture/traceability.md"

cp "$tr/docs/architecture/traceability.md" "$tmp/view.md"
sed -i.bak '/^Generated at commit/d' "$tr/docs/architecture/traceability.md"
trace_case "a view recording no commit is caught" 1
cp "$tmp/view.md" "$tr/docs/architecture/traceability.md"; rm -f "$tr/docs/architecture/"*.bak

# Behind HEAD: a note by default, a finding under --strict. The default has to tolerate it
# or the file would be stale the instant it is committed, and a gate nobody can satisfy is
# a gate everybody switches off.
(cd "$tr" && git add -A && git commit -q -m "Second phase" -m "Archirules-Phase: T2") >/dev/null 2>&1
trace_case "a view behind HEAD is tolerated by default" 0
trace_case "a view behind HEAD fails --strict" 1 --strict

# Usage errors must not share an exit code with a finding about a register.
trace_case "an unknown option refuses, exit 2" 2 --nonsense
mkdir -p "$tmp/nogit/docs/architecture"
printf '| X1 | a | ☐ | b |\n' > "$tmp/nogit/docs/architecture/phases.md"
case_no=$((case_no + 1))
python3 "$here/trace.py" "$tmp/nogit/docs/architecture" >/dev/null 2>&1
if [ $? -eq 2 ]; then
  printf "  ok    %-46s exit 2\n" "trace: outside a repository refuses"
else
  printf "  FAIL  %-46s\n" "trace: outside a repository refuses"
  failed=1
fi

# The migration claim (ADR-0009). /archirules:update reads migrations.py and nothing
# else, so what this script does on each kind of range is the contract. The case that
# matters is the unrecognised version: a migration that silently skips a release it did
# not understand leaves a register half-converted, which is worse than not migrating.
migrate() { python3 "$here/migrations.py" --changelog "$1" "${@:2}" >/dev/null 2>&1; echo $?; }
migrate_says() { python3 "$here/migrations.py" --changelog "$1" "${@:2}" 2>&1; }

fixture="$tmp/changelog.md"
cat > "$fixture" <<'MD'
# Changelog

## 2.0.0 — 2026-09-01

**Changed**

- Something that reaches registers.

### Migration

Rename the thing to the other thing.

## 1.5.0 — 2026-08-20

**Added**

- Something additive.

## 1.0.0

Initial release.
MD

for probe in \
  "a range with work:1:--from 1.0.0 --to 2.0.0:0" \
  "a range with no register changes:1:--from 1.0.0 --to 1.5.0:0" \
  "already at the newest version:1:--from 2.0.0:0" \
  "a version the changelog does not know:1:--from 9.9.9:2" \
  "a malformed version:1:--from banana:2" \
  "a changelog that is not there:1:--from 1.0.0 --changelog-missing:2"
do
  what=${probe%%:*}; rest=${probe#*:}; rest=${rest#*:}
  args=${rest%:*}; want=${rest##*:}
  if [ "$args" = "--from 1.0.0 --changelog-missing" ]; then
    code=$(migrate "$tmp/no-such-changelog.md" --from 1.0.0)
  else
    # shellcheck disable=SC2086
    code=$(migrate "$fixture" $args)
  fi
  case_no=$((case_no + 1))
  if [ "$code" -eq "$want" ]; then
    printf "  ok    %-46s exit %s\n" "migrations: $what" "$code"
  else
    printf "  FAIL  %-46s exit %s, expected %s\n" "migrations: $what" "$code" "$want"
    failed=1
  fi
done

# "Nothing to do" must be a sentence, not an empty output. An empty result would read
# the same as a script that failed to find its input, and the reader would act on it.
case_no=$((case_no + 1))
if migrate_says "$fixture" --from 1.0.0 --to 1.5.0 | grep -q "no work\|need no work\|changes anything"; then
  printf "  ok    %-46s said so\n" "migrations: an empty range says so in words"
else
  printf "  FAIL  %-46s silent\n" "migrations: an empty range says so in words"
  failed=1
fi

# The help claim (ADR-0008). Every skill must answer --help, and the answer has to come
# from help.py rather than from the model's memory. Three ways this goes wrong and all
# three are checked: a skill with no `## Usage` section, a skill whose SKILL.md never
# routes --help to the script, and a usage text that names the wrong skill in its own
# invocation line — the copy-paste defect, which reads perfectly and sends the user to
# another skill.
help_state=$(python3 - "$here" <<'PY'
import os
import re
import subprocess
import sys

scripts = sys.argv[1]
skills_dir = os.path.join(os.path.dirname(scripts), "skills")
broken = []
try:
    names = sorted(
        n for n in os.listdir(skills_dir)
        if os.path.isfile(os.path.join(skills_dir, n, "SKILL.md"))
    )
except OSError as exc:
    print("unreadable: %s" % exc)
    raise SystemExit(0)
if not names:
    print("no skills found under %s" % skills_dir)
    raise SystemExit(0)

for name in names:
    with open(os.path.join(skills_dir, name, "SKILL.md"), encoding="utf-8") as fh:
        text = fh.read()
    section = re.search(r"^## Usage\s*\n(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    if not section or not section.group(1).strip():
        broken.append("%s: no ## Usage section" % name)
        continue
    if "help.py %s" % name not in text:
        broken.append("%s: SKILL.md does not route --help to help.py %s" % (name, name))
    if "/archirules:%s" % name not in section.group(1):
        broken.append("%s: its usage names another skill in the invocation line" % name)
    # A form is not an example. `/archirules:adr [--help]` says how to type it and not
    # what to type into it, which is the question people actually arrive with.
    examples = re.search(r"^### Examples\s*\n(.*?)(?=^## |\Z)", section.group(1),
                         flags=re.M | re.S)
    if not examples:
        broken.append("%s: no ### Examples section in its usage" % name)
    elif not re.search(r"^/archirules:%s\b" % name, examples.group(1), flags=re.M):
        broken.append("%s: its examples show no invocation of itself" % name)
    # and the script must actually produce it, which is the claim that matters
    run = subprocess.run([sys.executable, os.path.join(scripts, "help.py"), name],
                         capture_output=True, text=True)
    if run.returncode != 0 or "/archirules:%s" % name not in run.stdout:
        broken.append("%s: help.py prints nothing usable (exit %d)" % (name, run.returncode))
print("\n".join(broken) or "HELP-OK %d skills" % len(names))
PY
)
case_no=$((case_no + 1))
case "$help_state" in
  "HELP-OK "*)
    printf "  ok    %-46s %s\n" "every skill answers --help from the script" \
      "${help_state#HELP-OK }" ;;
  *)
    printf "  FAIL  %-46s\n" "skills whose --help is missing or wrong:"
    echo "${help_state:-(the help check itself did not run)}" | sed 's/^/        /'
    failed=1 ;;
esac

# The release claim (ADR-0007). The version in plugin.json is what /archirules:update
# migrates between, and CHANGELOG.md is where it reads what changed. Two files that must
# agree, so the agreement is asserted rather than left to attention. A sentinel again,
# not an empty result: if either file is unreadable the check must go red, not quiet.
version=$(python3 - "$here" <<'PY'
import json
import os
import re
import sys

root = os.path.dirname(sys.argv[1])                     # plugins/archirules
try:
    with open(os.path.join(root, ".claude-plugin", "plugin.json"), encoding="utf-8") as fh:
        declared = json.load(fh).get("version")
    with open(os.path.join(root, "CHANGELOG.md"), encoding="utf-8") as fh:
        headings = re.findall(r"^## (\d+\.\d+\.\d+)", fh.read(), flags=re.M)
except Exception as exc:                                # noqa: BLE001 - reported, not swallowed
    print("unreadable: %s" % exc)
    raise SystemExit(0)
if not declared:
    print("plugin.json declares no version")
elif not headings:
    print("CHANGELOG.md has no version heading")
elif declared != headings[0]:
    print("plugin.json says %s, newest CHANGELOG heading is %s" % (declared, headings[0]))
else:
    print("VERSION-OK " + declared)
PY
)
case_no=$((case_no + 1))
case "$version" in
  "VERSION-OK "*)
    printf "  ok    %-46s %s\n" "plugin version and changelog agree" "${version#VERSION-OK }" ;;
  *)
    printf "  FAIL  %-46s %s\n" "plugin version and changelog disagree" \
      "${version:-(the version check itself did not run)}"
    failed=1 ;;
esac

echo
if [ "$failed" -eq 0 ]; then
  echo "  $case_no cases: the checker fails when it should, in both languages"
else
  echo "  THE CHECKER IS NOT TRUSTWORTHY"
fi
exit $failed
