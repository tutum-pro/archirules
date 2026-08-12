#!/usr/bin/env python3
"""Check an architecture documentation set against the archirules structure.

    conform.py <path to docs/architecture> [--lang pl|en|auto]

Exit code 0 when nothing is wrong, 1 otherwise, so it works as a CI gate.

MATCHING IS BY PREFIX, not by exact wording. A singular heading is correct when a
decision has one cost, and is not a deviation. The first version of this checker
matched only the plural form and reported six sections absent that were all
present — which is why prefixes are a rule here and not a convenience.
See CASEBOOK case C-05.

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
import unicodedata

MARKERS = {
    "pl": {
        "conseq": r"^## Konsekwencje",
        "impl": r"^## Stan realizacji",
        "cost": r"\*\*Koszt",
        "binding": "Wymagania obowiązujące",
        "legend": "Legenda",
        "criterion": "Kryterium akceptacji",
        "gate": "Twarda bramka",
        "superseded": "ZASTĄPIONY",
        "by": "przez",
    },
    "en": {
        "conseq": r"^## Consequences",
        "impl": r"^## Implementation status",
        "cost": r"\*\*Cost",
        "binding": "Binding requirements",
        "legend": "Legend",
        "criterion": "Acceptance criterion",
        "gate": "Hard gate",
        "superseded": "SUPERSEDED",
        "by": "by",
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
    """Return (language, confident).

    Detection keys on the binding-requirements heading. When neither variant is
    present the caller is TOLD so rather than being handed a silent default: a
    fallback that guesses wrong makes every marker miss and buries the real cause
    under dozens of spurious findings.
    """
    readme = os.path.join(directory, "README.md")
    if os.path.isfile(readme):
        text = open(readme, encoding="utf-8").read()
        if MARKERS["pl"]["binding"] in text:
            return "pl", True
        if MARKERS["en"]["binding"] in text:
            return "en", True
    return "pl", False


def slug(heading):
    """A heading's anchor, by the rule the renderers use.

    Lowercase; drop every character that is not a letter, a digit, a space, a hyphen
    or an underscore; turn spaces into hyphens. Letters outside ASCII survive, which
    is what makes Polish headings work. An em dash is punctuation, so it disappears
    and leaves behind the hyphens made from the spaces on either side of it — that is
    where the doubled hyphen in these anchors comes from.
    """
    kept = []
    for ch in heading.strip().lower():
        if ch.isalnum() or ch in " -_" or unicodedata.category(ch).startswith("M"):
            kept.append(ch)
    return "".join(kept).replace(" ", "-")


def anchors_of(path, _cache={}):
    """Every anchor a document offers, or None when it cannot be read.

    Headings inside fenced code blocks are not headings. Repeated headings get the
    renderers' `-1`, `-2` suffixes.
    """
    if path in _cache:
        return _cache[path]
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        _cache[path] = None
        return None
    seen, out, fenced = {}, set(), False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        heading = re.match(r"^#{1,6}\s+(.*?)\s*$", line)
        if not heading:
            continue
        base = slug(heading.group(1))
        count = seen.get(base, 0)
        seen[base] = count + 1
        out.add(base if count == 0 else "%s-%d" % (base, count))
    _cache[path] = out
    return out


def names_a_scope(status_line, marker):
    """True when a supersession status says more than which record replaced it.

    Rule P7: often only part of a decision stops holding, so the status has to say
    which part. It belongs in the status line itself rather than in a section further
    down — a correction sitting above a field that still lies is not a correction
    (case C-04). That placement is why this check lives here, in the checker that
    reads one file at a time, and not in the cross-register one (ADR-0006).

    Deliberately generous: anything surviving the removal of the keyword, the
    connector, the pointer and a date counts. This asks whether a scope is stated at
    all, not whether it is a good one. A stricter reading would start reporting sound
    records as broken, which costs more trust than it recovers.
    """
    rest = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", status_line)   # links -> their text
    rest = rest.replace(marker["superseded"], "")
    rest = re.sub(r"ADR-\d{4}", "", rest)
    rest = re.sub(r"\d{4}-\d{2}-\d{2}", "", rest)
    rest = re.sub(r"\b%s\b" % re.escape(marker["by"]), "", rest)
    return len(re.sub(r"[\W\d_]+", "", rest)) >= 3


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    directory = sys.argv[1]
    forced = None
    if "--lang" in sys.argv:
        forced = sys.argv[sys.argv.index("--lang") + 1]
    if forced == "auto":
        forced = None
    if forced is not None and forced not in MARKERS:
        # Refuse rather than guess (rule W1). Exit 2, so a usage error cannot be read
        # as a finding about the register.
        print(
            f"  --lang {forced}: no marker table for that language; "
            f"supported: {', '.join(sorted(MARKERS))}",
            file=sys.stderr,
        )
        return 2
    detected, confident = detect_language(directory)
    language = forced if forced is not None else detected
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
        status = re.search(r"^\*\*Status:\*\*(.*)$", text, re.M)
        if status and marker["superseded"] in status.group(1):
            check(
                names_a_scope(status.group(1), marker),
                f"{name}: status says {marker['superseded']} but names no scope — "
                "which part of the decision stopped holding, and since when",
            )
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
        check(
            confident or forced is not None,
            "language could not be detected from README.md (no binding-requirements heading "
            f"in either variant); assuming {language}, so every marker below may be wrong",
        )
        # The language skill ends its procedure by asking a human to confirm that the
        # language the checker detects is the target one. That is a check, so it is
        # mechanised here (rule W9): a forced language contradicting the register's own
        # README makes every marker miss, and a run that finds nothing then looks
        # exactly like a run that found nothing wrong.
        check(
            not (forced is not None and confident and forced != detected),
            f"--lang {forced} was given, but README.md reads as {detected}; the checks "
            f"ran against {forced} wording and will have missed their subject",
        )

    # 4. Open questions: a number is a public reference, so duplicates and gaps
    #    both make references ambiguous.
    if os.path.isfile(f"{directory}/open-questions.md"):
        questions = open(f"{directory}/open-questions.md", encoding="utf-8").read()
        # Any dash. A translator writing "-" instead of "—" must not be able to
        # switch the whole section off: with a strict pattern, an entire register of
        # questions parsed as zero and the checker reported success (case C-06).
        # Any dash, but it must be separated from the number: "### OQ-20-archiwum"
        # is an archived variant, not a twentieth question, and a pattern loose
        # enough to swallow it invents a duplicate that is not there.
        numbers = [int(n) for n in re.findall(r"^### OQ-(\d+)\s+[—–-]\s", questions, re.M)]
        # Counted with the LOOSEST pattern that still excludes deliberate
        # non-questions such as "### OQ-20-archiwum". Tightening this the same way
        # as the parser above would blind the safety net to exactly the drift it
        # exists to catch — which is what happened the first time: headings and
        # parsed entries both fell to zero together and the mismatch never fired
        # (case C-07).
        headings = len(re.findall(r"^### OQ-\d+(?![\w-])", questions, re.M))
        # Coverage accounting for the PARSER itself: if a heading looks like an
        # open question but does not parse, the checks below silently stop
        # applying, which is worse than any single defect they would have found.
        check(
            headings == len(numbers),
            f"{headings} headings look like open questions but only {len(numbers)} parsed; "
            "the heading format has drifted and the checks below did not run",
        )
        duplicates = sorted({n for n in numbers if numbers.count(n) > 1})
        check(not duplicates, f"duplicate open-question numbers: {duplicates}")
        if numbers:
            gaps = sorted(set(range(1, max(numbers) + 1)) - set(numbers))
            check(not gaps, f"gaps in open-question numbering: {gaps}")
        for match in re.finditer(r"^### OQ-(\d+)\s*[—–-][^\n]*\n(.*)$", questions, re.M):
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
        shown = os.path.relpath(path, directory)
        fenced = False
        for lineno, line in enumerate(text.split("\n"), 1):
            if line.lstrip().startswith("```"):
                fenced = not fenced
                continue
            # A link written as an example, in a code fence or between backticks, is not
            # a link. Reading one as real reports a document as broken for showing what a
            # link looks like — which this checker did, in this repository's own register.
            if fenced:
                continue
            for target in re.findall(r"\]\(([^)]+)\)", re.sub(r"`[^`]*`", "", line)):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                file_part, _, anchor = target.partition("#")
                file_part, anchor = file_part.strip(), anchor.strip()
                destination = os.path.join(base, file_part) if file_part else path
                if file_part:
                    check(
                        os.path.exists(destination),
                        f"{shown}:{lineno}: link points nowhere: {file_part}",
                    )
                if not anchor:
                    continue
                # The anchor is the half that rots in silence: renaming a heading leaves
                # every link to it resolving to a file that exists and a place in it that
                # does not.
                offered = anchors_of(destination)
                if offered is None:
                    continue                      # the missing file is already reported
                check(
                    anchor in offered,
                    f"{shown}:{lineno}: link resolves to the file but not to a heading "
                    f"in it: #{anchor}",
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
