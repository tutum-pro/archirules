#!/usr/bin/env python3
"""Check an architecture documentation set against the archirules structure.

    conform.py <path to docs/architecture> [--lang pl|en|auto]

Exit code 0 when nothing is wrong, 1 otherwise, so it works as a CI gate.

MATCHING IS BY PREFIX, not by exact wording. In Polish, `**Koszt.**` (singular) is
correct when a decision has one cost, and is not a deviation. The first version of
this checker required `**Koszty` and reported six false gaps in a project that had
a complete set — which is why prefixes are a rule here and not a convenience.

The checker deliberately does NOT report a missing "considered and rejected"
section. In practice that content is often written into the prose of the decision
instead, and reporting it absent would be a claim about a document nobody read
(rule W3). Extracting it into its own section is what the template teaches for new
records, not something to retrofit by machine.

Language is detected from README.md and can be forced with --lang.
"""
import glob
import os
import re
import sys

MARKERS = {
    "pl": {
        "conseq": r"^## Konsekwencje",
        "impl": r"^## Stan realizacji",
        "cost": r"\*\*Koszt",
        "binding": "Wymagania obowiązujące",
        "legend": "Legenda",
        "criterion": "Kryterium akceptacji",
        "gate": "Twarda bramka",
    },
    "en": {
        "conseq": r"^## Consequences",
        "impl": r"^## Implementation status",
        "cost": r"\*\*Cost",
        "binding": "Binding requirements",
        "legend": "Legend",
        "criterion": "Acceptance criterion",
        "gate": "Hard gate",
    },
}

# Both naming conventions are accepted so that an existing project never has to
# rename files to become checkable.
PHASE_FILES = ["fazy-realizacji.md", "phases.md"]
VERIFICATION_FILES = ["rejestr-weryfikacji.md", "verification.md"]


def first_existing(directory, names):
    for name in names:
        if os.path.isfile(os.path.join(directory, name)):
            return name
    return None


def detect_language(directory):
    readme = os.path.join(directory, "README.md")
    if os.path.isfile(readme):
        text = open(readme, encoding="utf-8").read()
        if MARKERS["pl"]["binding"] in text:
            return "pl"
        if MARKERS["en"]["binding"] in text:
            return "en"
    return "pl"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    directory = sys.argv[1]
    language = "auto"
    if "--lang" in sys.argv:
        language = sys.argv[sys.argv.index("--lang") + 1]
    if language == "auto":
        language = detect_language(directory)
    marker = MARKERS[language]

    problems = []
    checks = 0

    def check(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            problems.append(message)

    # 1. Required artefacts.
    check(os.path.isfile(f"{directory}/README.md"), "missing artefact: README.md")
    check(os.path.isfile(f"{directory}/open-questions.md"), "missing artefact: open-questions.md")
    phases = first_existing(directory, PHASE_FILES)
    check(phases is not None, f"missing phase register ({' or '.join(PHASE_FILES)})")
    check(
        first_existing(directory, VERIFICATION_FILES) is not None,
        f"missing verification register ({' or '.join(VERIFICATION_FILES)})",
    )
    check(os.path.isdir(f"{directory}/decisions"), "missing decisions/ directory")

    # 2. Every decision record carries the sections a decision needs to be one.
    records = sorted(glob.glob(f"{directory}/decisions/ADR-*.md"))
    check(len(records) > 0, "no decision records in decisions/")
    for path in records:
        text = open(path, encoding="utf-8").read()
        name = os.path.basename(path)
        check(re.search(r"^\*\*Status:\*\*", text, re.M), f"{name}: no **Status:**")
        check(re.search(marker["conseq"], text, re.M), f"{name}: no consequences section")
        check(re.search(marker["impl"], text, re.M), f"{name}: no implementation status section")
        check(re.search(marker["cost"], text), f"{name}: no costs section (prefix {marker['cost']})")

    # 3. The index and the directory must agree: a record outside the index is
    #    invisible, which is the same as not existing.
    if os.path.isfile(f"{directory}/README.md"):
        readme = open(f"{directory}/README.md", encoding="utf-8").read()
        rows = len(re.findall(r"^\| \[\d{4}\]", readme, re.M))
        check(rows == len(records), f"index lists {rows} records, decisions/ holds {len(records)}")
        check(marker["binding"] in readme, f"README: no '{marker['binding']}' section")

    # 4. Open questions: a number is a public reference, so duplicates and gaps
    #    both make references ambiguous.
    if os.path.isfile(f"{directory}/open-questions.md"):
        questions = open(f"{directory}/open-questions.md", encoding="utf-8").read()
        numbers = [int(n) for n in re.findall(r"^### OQ-(\d+) —", questions, re.M)]
        duplicates = sorted({n for n in numbers if numbers.count(n) > 1})
        check(not duplicates, f"duplicate open-question numbers: {duplicates}")
        if numbers:
            gaps = sorted(set(range(1, max(numbers) + 1)) - set(numbers))
            check(not gaps, f"gaps in open-question numbering: {gaps}")
        for match in re.finditer(r"^### OQ-(\d+) —[^\n]*\n(.*)$", questions, re.M):
            check(
                match.group(2).startswith("**Status:**"),
                f"OQ-{match.group(1)}: **Status:** is not directly under the heading",
            )

    # 5. Internal links must resolve. A rename that leaves references behind is the
    #    normal way a documentation set breaks, and switching a project's language
    #    renames files by design.
    for path in glob.glob(f"{directory}/**/*.md", recursive=True):
        text = open(path, encoding="utf-8").read()
        base = os.path.dirname(path)
        for target in re.findall(r"\]\(([^)]+)\)", text):
            target = target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            check(
                os.path.exists(os.path.join(base, target)),
                f"{os.path.relpath(path, directory)}: link points nowhere: {target}",
            )

    # 6. Phase register.
    if phases:
        register = open(f"{directory}/{phases}", encoding="utf-8").read()
        check(marker["legend"] in register, "phase register: no legend")
        check(marker["criterion"] in register, "phase register: no acceptance-criterion column")
        check(marker["gate"] in register, "phase register: no hard gate")

    print(f"  language: {language} · checks: {checks} · problems: {len(problems)}")
    for problem in problems:
        print(f"    x {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
