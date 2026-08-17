#!/usr/bin/env python3
"""Check agreement BETWEEN archirules registers, and non-contradiction of decisions.

    consistency.py <path to docs/architecture> [--lang pl|en]

`conform.py` checks the structure *inside* each register — sections of a decision
record, question numbering, the shape of the phase table. It cannot see a register
that disagrees with another one, because every file is well-formed on its own.

This checks the other axis:

  A. a question declaring it blocks a phase, against that phase's status and blocker list
  B. a phase waiting on a question, against that question's existence and status
  C. a question that is no longer open yet still declares what it blocks
  D. references to decision records — existence, and entries pointing at a superseded one
  E. non-contradiction of decision records: a supersession link must be two-way, and two
     records must not resolve the same question without referencing each other

Exit code 0 when nothing is wrong, 1 otherwise, so it works as a CI gate. Exit code 2
is a usage error, which is a different conversation from a defective register.

Three rules govern what may be added here:

1. **Language is detected, not assumed**, and forcing it is reconciled against the
   detection rather than replacing it. A wrong language makes every marker miss, so
   every check passes over its subject without a word and the run reports zero
   problems because it did almost nothing.
2. **Absent structure is not a finding — but the skip is REPORTED.** The blocker table
   is a project convention rather than part of the method, and a set that keeps none is
   not thereby defective. "0 problems" must never silently mean "0 checks ran".
3. **Every marker below occurs in a template or in a skill** (ADR-0006). A marker
   invented here and honoured only by the fixtures proves this script consistent with
   its own test data, which was never in doubt. `selftest.sh` asserts this; it is not
   left to review.
"""
import os
import re
import sys
from collections import defaultdict

# Every string here is produced by templates/<lang>/ or prescribed by a SKILL.md.
# The one exception is `blocker_table`, which is a project convention and is recorded
# as one in skills/audit/SKILL.md — see rule W9 and OQ-06.
MARKERS = {
    "pl": {
        "binding": "Wymagania obowiązujące",
        "open": "OTWARTE",
        "blocks": "Blokuje",
        "blocker_table": "Co blokuje",
        "supersedes": "Zastępuje",
        "superseded": "ZASTĄPIONY",
        "resolves": "Rozstrzyga",
        "touches": "Dotyka",
        "question": "OQ",
    },
    "en": {
        "binding": "Binding requirements",
        "open": "OPEN",
        "blocks": "Blocks",
        "blocker_table": "What blocks",
        "supersedes": "Supersedes",
        "superseded": "SUPERSEDED",
        "resolves": "Resolves",
        "touches": "Touches",
        "question": "OQ",
    },
}

QUESTION_FILES = ("open-questions.md",)
PHASE_FILES = ("fazy-realizacji.md", "phases.md")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def die(message):
    """Refuse rather than guess (rule W1). Exit 2, so it cannot read as a finding."""
    print("  %s" % message, file=sys.stderr)
    raise SystemExit(2)


def parse_args(argv):
    """Both `--lang en` and `--lang=en` are accepted, and an unusable value stops the run.

    The sibling checker documents the spaced form and this one used to accept only the
    `=` form — silently detecting the language instead of forcing it. Silent degradation
    looks exactly like success (rule W1), which is the whole reason for this function.
    """
    positional, forced, awaiting = [], None, False
    for arg in argv:
        if awaiting:
            forced, awaiting = arg, False
        elif arg == "--lang":
            awaiting = True
        elif arg.startswith("--lang="):
            forced = arg.split("=", 1)[1]
        elif arg.startswith("--"):
            die("unknown option: %s" % arg)
        else:
            positional.append(arg)
    if awaiting:
        die("--lang needs a value: %s" % " or ".join(sorted(MARKERS)))
    if forced is not None and forced not in MARKERS:
        die("--lang %s: no marker table for that language; supported: %s"
            % (forced, ", ".join(sorted(MARKERS))))
    return positional, forced


def detect_language(directory):
    """Return (language, confident) from README.md alone — never a silent guess.

    Forcing is reconciled against this rather than replacing it. A forced language that
    contradicts the register's own README makes every marker miss, and every check then
    passes over its subject in silence: the run reports zero problems because it did
    almost nothing. The language skill already asks a human to confirm that the detected
    language is the intended one; this is that check, mechanised (rule W9).
    """
    readme = os.path.join(directory, "README.md")
    if os.path.isfile(readme):
        text = read(readme)
        if MARKERS["pl"]["binding"] in text:
            return "pl", True
        if MARKERS["en"]["binding"] in text:
            return "en", True
    return "pl", False


def phase_register(directory):
    for name in PHASE_FILES:
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            return path
    return None


def questions(text, m):
    """{number: (status, whole block)} for every question heading."""
    out = {}
    for block in re.split(r"(?=^### %s-)" % m["question"], text, flags=re.M):
        head = re.match(r"### (%s-\d+)" % m["question"], block)
        if not head:
            continue
        status = re.search(r"\*\*Status:\*\*\s*(\S+)", block)
        out[head.group(1)] = (status.group(1) if status else "?", block)
    return out


def field_of_status(block):
    """The Status paragraph of a question — everything up to the first blank line."""
    match = re.search(r"\*\*Status:\*\*(.*?)(?:\n\s*\n|\Z)", block, re.S)
    return match.group(1) if match else ""


def phases(text):
    """{id: status} taken from the first column of the phase table — any identifier."""
    out = {}
    for pid, status in re.findall(
        r"^\|\s*([A-Za-z]\w*)\s*\|[^|]*\|\s*([☐◐☑⛔])\s*\|", text, flags=re.M
    ):
        out[pid] = status
    return out


def blocker_table(text, m):
    """{phase: {question, ...}} — or None when the project keeps no such table."""
    secs = re.findall(r"###[^\n]*%s(.*?)(?=\n##|\Z)" % re.escape(m["blocker_table"]), text, re.S)
    if not secs:
        return None
    out = {}
    for sec in secs:                       # a set may keep one table per path
        for pid, cell in re.findall(r"^\|\s*([A-Za-z]\w*)\s*\|([^|]*)\|", sec, flags=re.M):
            out.setdefault(pid, set()).update(re.findall(r"%s-\d+" % m["question"], cell))
    return out


def decisions(directory, m):
    """{number: {'status', 'supersedes', 'superseded_by', 'resolves', 'file'}}.

    The method has one relation between records, not two: supersession, whole or
    partial. Its forward half is the `Supersedes:` field on the new record and its
    reverse half is the status line of the old one — which is where adr/SKILL.md puts
    it, and where rule P7 requires it, a correction sitting above a field that still
    lies not being a correction (case C-04).
    """
    directory = os.path.join(directory, "decisions")
    out = {}
    for fname in sorted(os.listdir(directory)):
        num = re.match(r"(ADR-\d{4})", fname)
        if not num or not fname.endswith(".md"):
            continue
        text = read(os.path.join(directory, fname))
        head = text[: text.find("\n## ")] if "\n## " in text else text
        out[num.group(1)] = {
            "file": fname,
            "status": m["superseded"] if m["superseded"] in head else "current",
            "supersedes": set(re.findall(r"ADR-\d{4}", field(head, m["supersedes"]))),
            # the reverse link lives in Status; take that field only, never the whole
            # head, or the neighbouring fields leak in
            "superseded_by": set(re.findall(r"ADR-\d{4}", field(head, "Status"))) - {num.group(1)},
            "resolves": set(re.findall(r"%s-\d+" % m["question"], field(head, m["resolves"]))),
        }
    return out


def field(head, label):
    """Every occurrence of the field, each cut at the next '**Label:**' on the line.

    Two defects this guards against, both found by running the checker on a real set:
    a record may carry the same field twice, and fields are separated by ' · ' on one
    line, so a greedy match swallows the neighbours.
    """
    return " ".join(
        hit.group(1)
        for hit in re.finditer(r"\*\*%s:?\*\*\s*(.*?)(?=\s*·\s*\*\*|$)" % re.escape(label),
                               head, flags=re.M)
    )


def main(directory, forced=None):
    detected, confident = detect_language(directory)
    lang = forced if forced is not None else detected
    m = MARKERS[lang]
    problems, skipped, checks = [], [], 0

    if forced is None and not confident:
        problems.append(
            "language could not be detected from README.md; assuming %s, so every "
            "marker below may be wrong" % lang
        )
    elif forced is not None and confident and forced != detected:
        problems.append(
            "--lang %s was given, but README.md reads as %s; the checks below ran against "
            "%s wording and will have missed their subject rather than approved it"
            % (forced, detected, forced)
        )

    qpath = os.path.join(directory, QUESTION_FILES[0])
    if not os.path.isfile(qpath):
        print("  missing %s — nothing to cross-check" % QUESTION_FILES[0])
        return 1
    qs = questions(read(qpath), m)
    ppath = phase_register(directory)
    ptext = read(ppath) if ppath else ""
    ph = phases(ptext)
    bt = blocker_table(ptext, m)
    if ppath and bt is None:
        skipped.append(
            "no blocker table (heading '%s') — checks A(ii) and B not run" % m["blocker_table"]
        )

    # Coverage accounting before anything keys on a status: a question whose status
    # cannot be read silently drops out of checks A and C, which is worse than any
    # single defect they would have found.
    unreadable = {num for num, (status, _) in qs.items() if status == "?"}
    for num in sorted(unreadable):
        problems.append(
            "%s: **Status:** could not be read, so the checks keying on it did not run "
            "for this question" % num
        )

    # A. a question declares it blocks a phase
    for num, (status, block) in sorted(qs.items()):
        if num in unreadable or status != m["open"]:
            continue
        declared = field(block, m["blocks"])
        if not declared:
            continue
        for pid in re.findall(r"\b[A-Za-z]\w*\d\w*\b", declared):
            if pid not in ph:
                continue
            checks += 1
            if ph[pid] != "⛔":
                problems.append(
                    "%s (%s) declares it blocks %s, but %s is marked '%s' instead of ⛔"
                    % (num, m["open"], pid, pid, ph[pid])
                )
            if bt is not None:
                checks += 1
                if num not in bt.get(pid, set()):
                    problems.append(
                        "%s declares 'blocks %s', but the blocker table for %s does not list it"
                        % (num, pid, pid)
                    )

    # B. a phase waits on a question
    if bt is not None:
        for pid, nums in sorted(bt.items()):
            for num in sorted(nums):
                checks += 1
                if num not in qs:
                    problems.append("phase %s waits on %s, which does not exist" % (pid, num))
                elif qs[num][0] != m["open"]:
                    problems.append(
                        "phase %s waits on %s, whose status is %s" % (pid, num, qs[num][0])
                    )

    # C. a question that is no longer open yet still declares what it blocks.
    #    Independent of the blocker table, so it runs everywhere. The earlier version
    #    of this check searched for a marker and a question number on ONE line, a shape
    #    no template produces — it could not fire, and nothing noticed because it had no
    #    self-test case. See ADR-0006 and rule W4.
    for num, (status, block) in sorted(qs.items()):
        if num in unreadable or status == m["open"]:
            continue
        checks += 1
        declared = field(block, m["blocks"]).strip()
        if declared:
            problems.append(
                "%s is %s yet still declares 'blocks %s' — either the question is not "
                "actually closed, or a phase is being held for an answered question"
                % (num, status, declared)
            )

    # D and E both need the records themselves. Their absence is a structural defect
    # conform.py reports on its own axis; repeating it here as a flood of dangling
    # references would bury it.
    if not os.path.isdir(os.path.join(directory, "decisions")):
        skipped.append("no decisions/ directory — checks D and E not run "
                       "(conform.py reports the missing directory itself)")
        adrs = {}
    else:
        adrs = decisions(directory, m)
        files = [f for f in sorted(os.listdir(directory)) if f.endswith(".md")]
        files += [os.path.join("decisions", f)
                  for f in sorted(os.listdir(os.path.join(directory, "decisions")))
                  if f.endswith(".md")]

        # D. references to decision records
        for fname in files:
            for lineno, line in enumerate(read(os.path.join(directory, fname)).split("\n"), 1):
                if line.strip().startswith("<!--"):
                    continue
                for ref in re.findall(r"ADR-\d{4}", line):
                    checks += 1
                    if ref not in adrs:
                        problems.append("%s:%d: reference to non-existent %s" % (fname, lineno, ref))
                    elif adrs[ref]["status"] != "current" and m["touches"] in line:
                        problems.append(
                            "%s:%d: entry points at %s, which is superseded" % (fname, lineno, ref)
                        )

        # E. non-contradiction of decision records
        for num, rec in sorted(adrs.items()):
            for target in sorted(rec["supersedes"]):
                checks += 1
                if target not in adrs:
                    problems.append("%s supersedes %s, which does not exist" % (num, target))
                elif num not in adrs[target]["superseded_by"]:
                    problems.append(
                        "%s supersedes %s, but the status of %s does not say so "
                        "(one-way link)" % (num, target, target)
                    )
        # An ADR that claims to settle a question, against a question that does not
        # say it was settled.
        #
        # The two registers can drift apart in either direction and neither file
        # reveals it alone: the decision reads as final, the question reads as open,
        # and whoever opens one of them is told something true about that file and
        # false about the pair. Found in a real register, where ADR-0022 settled the
        # choice in its §4 while OQ-68 still called itself open AND named that same
        # ADR as blocked by it — a cycle nobody would write on purpose.
        for num, rec in sorted(adrs.items()):
            # A superseded record keeps its original "resolves" line — that is its
            # history, and rewriting it would erase what was decided at the time.
            # The question rightly names the record in force instead, so demanding a
            # back-link here would report correct bookkeeping as a defect.
            if m["superseded"] in rec["status"]:
                continue
            for question in sorted(rec["resolves"]):
                checks += 1
                if question not in qs:
                    problems.append(
                        "%s says it resolves %s, which does not exist" % (num, question)
                    )
                    continue
                status, block = qs[question]
                if status == m["open"]:
                    problems.append(
                        "%s says it resolves %s, but %s still calls itself %s"
                        % (num, question, question, status)
                    )
                    continue
                checks += 1
                if num not in re.findall(r"ADR-\d+", field_of_status(block)):
                    problems.append(
                        "%s says it resolves %s, but %s does not name %s in its status "
                        "(one-way link)" % (num, question, question, num)
                    )

        by_question = defaultdict(list)
        for num, rec in sorted(adrs.items()):
            for question in rec["resolves"]:
                by_question[question].append(num)
        for question, nums in sorted(by_question.items()):
            if len(nums) < 2:
                continue
            checks += 1
            linked = any(
                b in adrs[a]["supersedes"] or b in adrs[a]["superseded_by"]
                for a in nums
                for b in nums
                if a != b
            )
            if not linked:
                problems.append(
                    "%s is resolved by %s with no supersession link between them — one "
                    "record may not know about the other" % (question, " and ".join(sorted(nums)))
                )

    print("  language: %s · cross-register checks: %d · problems: %d"
          % (lang, checks, len(problems)))
    for note in skipped:
        print("    ~ skipped: %s" % note)
    for problem in problems:
        print("    x %s" % problem)
    return 1 if problems else 0


if __name__ == "__main__":
    positional, forced_language = parse_args(sys.argv[1:])
    sys.exit(main(positional[0] if positional else "docs/architecture", forced_language))
