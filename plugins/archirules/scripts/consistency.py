#!/usr/bin/env python3
"""Check agreement BETWEEN archirules registers, and non-contradiction of decisions.

    consistency.py <path to docs/architecture> [--lang pl|en|auto]

`conform.py` checks the structure *inside* each register — sections of a decision
record, question numbering, the shape of the phase table. It cannot see a register
that disagrees with another one, because every file is well-formed on its own.

This checks the other axis:

  A. a question declaring it blocks a phase, against that phase's status and blocker list
  B. a phase waiting on a question, against that question's existence and status
  C. a resolved question still cited as a blocker anywhere
  D. references to decision records — existence and superseded status
  E. non-contradiction of decision records: modification links must be two-way,
     a modified record must say what changed, and two records must not resolve
     the same question without referencing each other

Exit code 0 when nothing is wrong, 1 otherwise, so it works as a CI gate.

Two rules taken from conform.py, for the same reasons:

1. **Language is detected, not assumed.** A wrong guess makes every marker miss and
   buries the real finding under spurious ones.
2. **Absent structure is not a finding.** The blocker table is a project convention,
   not part of the method — a set that does not keep one is not thereby defective.
   Checks A(ii) and B are skipped, and the skip is REPORTED, so that "0 problems"
   never silently means "0 checks ran".
"""
import os
import re
import sys
from collections import defaultdict

MARKERS = {
    "pl": {
        "binding": "Wymagania obowiązujące",
        "open": "OTWARTE",
        "resolved": "ROZSTRZYGNIĘTE",
        "blocks": "Blokuje",
        "blocker_table": "Co blokuje",
        "modified_by": "Zmodyfikowany przez",
        "modifies": "Modyfikuje",
        "supersedes": "Zastępuje",
        "superseded": "ZASTĄPIONY",
        "resolves": "Rozstrzyga",
        "what_changed": ("Co zostało zmienione", "Zakres zastąpienia"),
        "waits_on": "czeka na",
        "touches": "Dotyka",
        "question": "OQ",
    },
    "en": {
        "binding": "Binding requirements",
        "open": "OPEN",
        "resolved": "RESOLVED",
        "blocks": "Blocks",
        "blocker_table": "What blocks",
        "modified_by": "Modified by",
        "modifies": "Modifies",
        "supersedes": "Supersedes",
        "superseded": "SUPERSEDED",
        "resolves": "Resolves",
        "what_changed": ("What changed", "Scope of supersession"),
        "waits_on": "waits on",
        "touches": "Touches",
        "question": "OQ",
    },
}

QUESTION_FILES = ("open-questions.md",)
PHASE_FILES = ("fazy-realizacji.md", "phases.md")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def detect_language(directory, forced=None):
    """Return (language, confident). Never guesses silently — see module docstring."""
    if forced in ("pl", "en"):
        return forced, True
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
        p = os.path.join(directory, name)
        if os.path.isfile(p):
            return p
    return None


def questions(text, m):
    """{number: (status, whole block)} for every question heading."""
    out = {}
    for block in re.split(r"(?=^### %s-)" % m["question"], text, flags=re.M):
        head = re.match(r"### (%s-\d+)" % m["question"], block)
        if not head:
            continue
        st = re.search(r"\*\*Status:\*\*\s*(\S+)", block)
        out[head.group(1)] = (st.group(1) if st else "?", block)
    return out


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
    """{number: {'status','modifies','modified_by','resolves','has_what_changed','file'}}."""
    d = os.path.join(directory, "decisions")
    out = {}
    if not os.path.isdir(d):
        return out
    for fname in sorted(os.listdir(d)):
        num = re.match(r"(ADR-\d{4})", fname)
        if not num or not fname.endswith(".md"):
            continue
        text = read(os.path.join(d, fname))
        head = text[: text.find("\n## ")] if "\n## " in text else text
        out[num.group(1)] = {
            "file": fname,
            "status": m["superseded"] if m["superseded"] in head else "current",
            "modifies": set(re.findall(r"ADR-\d{4}", _field(head, m["modifies"]) + _field(head, m["supersedes"]))),
            # supersession is a valid reverse link, but it lives in Status — take that
            # line only, never the whole head, or neighbouring fields leak in
            "modified_by": set(re.findall(r"ADR-\d{4}",
                                          _field(head, m["modified_by"]) + " " +
                                          _field(head, "Status"))) - {num.group(1)},
            "resolves": set(re.findall(r"%s-\d+" % m["question"], _field(head, m["resolves"]))),
            "has_what_changed": any(h in text for h in m["what_changed"]),
        }
    return out


def _field(head, label):
    """Every occurrence of the field, each cut at the next '**Label:**' on the line.

    Two defects this guards against, both found by running the checker on a real set:
    a record may carry the same field twice (modified by two successors), and fields
    are separated by ' · ' on one line, so a greedy match swallows the neighbours.
    """
    out = []
    for hit in re.finditer(r"\*\*%s:?\*\*\s*(.*?)(?=\s*·\s*\*\*|$)" % re.escape(label),
                           head, flags=re.M):
        out.append(hit.group(1))
    return " ".join(out)


def main(directory, forced=None):
    lang, confident = detect_language(directory, forced)
    m = MARKERS[lang]
    problems, skipped, checks = [], [], 0

    if not confident:
        problems.append(
            "language could not be detected from README.md; assuming %s, so every "
            "marker below may be wrong" % lang
        )

    qpath = os.path.join(directory, QUESTION_FILES[0])
    ppath = phase_register(directory)
    if not os.path.isfile(qpath):
        print("  missing %s — nothing to cross-check" % QUESTION_FILES[0])
        return 1
    qs = questions(read(qpath), m)
    ptext = read(ppath) if ppath else ""
    ph = phases(ptext)
    bt = blocker_table(ptext, m)
    if ppath and bt is None:
        skipped.append(
            "no blocker table (heading '%s') — checks A(ii) and B not run" % m["blocker_table"]
        )

    # A. question declares it blocks a phase
    for num, (status, block) in qs.items():
        field = _field(block, m["blocks"])
        if not field:
            continue
        for pid in re.findall(r"\b[A-Za-z]\w*\d\w*\b", field):
            if pid not in ph:
                continue
            checks += 1
            if status == m["open"] and ph[pid] != "⛔":
                problems.append(
                    "%s (%s) declares it blocks %s, but %s is marked '%s' instead of ⛔"
                    % (num, m["open"], pid, pid, ph[pid])
                )
            if bt is not None and status == m["open"] and num not in bt.get(pid, set()):
                checks += 1
                problems.append(
                    "%s declares 'blocks %s', but the blocker table for %s does not list it"
                    % (num, pid, pid)
                )

    # B. phase waits on a question
    if bt is not None:
        for pid, nums in bt.items():
            for num in nums:
                checks += 1
                if num not in qs:
                    problems.append("phase %s waits on %s, which does not exist" % (pid, num))
                elif qs[num][0] != m["open"]:
                    problems.append(
                        "phase %s waits on %s, whose status is %s" % (pid, num, qs[num][0])
                    )

    # C. a resolved question cited as a blocker
    closed = {n for n, (s, _) in qs.items() if s != m["open"]}
    for fname in os.listdir(directory):
        if not fname.endswith(".md"):
            continue
        text = read(os.path.join(directory, fname))
        for num in closed:
            checks += 1
            if re.search(r"(%s|%s)[^\n]*%s\b"
                         % (re.escape(m["blocks"]), re.escape(m["waits_on"]), num), text):
                problems.append("%s: %s is resolved, yet listed as a blocker" % (fname, num))

    # D. references to decision records
    adrs = decisions(directory, m)
    for fname in list(os.listdir(directory)) + [
        os.path.join("decisions", f) for f in os.listdir(os.path.join(directory, "decisions"))
    ] if os.path.isdir(os.path.join(directory, "decisions")) else []:
        if not fname.endswith(".md"):
            continue
        for lineno, line in enumerate(read(os.path.join(directory, fname)).split("\n"), 1):
            if line.strip().startswith("<!--"):
                continue
            for ref in re.findall(r"ADR-\d{4}", line):
                checks += 1
                if ref not in adrs:
                    problems.append("%s:%d: reference to non-existent %s" % (fname, lineno, ref))
                elif adrs[ref]["status"] != "current" and m["touches"] in line:
                    problems.append("%s:%d: entry points at %s, which is superseded" % (fname, lineno, ref))

    # E. non-contradiction of decision records
    for num, rec in adrs.items():
        for target in rec["modifies"]:
            checks += 1
            if target not in adrs:
                problems.append("%s modifies %s, which does not exist" % (num, target))
            elif num not in adrs[target]["modified_by"]:
                problems.append(
                    "%s modifies %s, but %s does not say it was modified by %s "
                    "(one-way link)" % (num, target, target, num)
                )
        if rec["modified_by"]:
            checks += 1
            if not rec["has_what_changed"]:
                problems.append(
                    "%s is modified by %s but has no '%s' section saying which points "
                    "lost force" % (num, ", ".join(sorted(rec["modified_by"])),
                                    " / ".join(m["what_changed"]))
                )
    by_question = defaultdict(list)
    for num, rec in adrs.items():
        for q in rec["resolves"]:
            by_question[q].append(num)
    for q, nums in by_question.items():
        if len(nums) < 2:
            continue
        checks += 1
        linked = any(
            b in adrs[a]["modifies"] or b in adrs[a]["modified_by"]
            for a in nums
            for b in nums
            if a != b
        )
        if not linked:
            problems.append(
                "%s is resolved by %s with no modification link between them — one "
                "record may not know about the other" % (q, " and ".join(sorted(nums)))
            )

    print("  language: %s · cross-register checks: %d · problems: %d" % (lang, checks, len(problems)))
    for s in skipped:
        print("    ~ skipped: %s" % s)
    for p in problems:
        print("    x %s" % p)
    return 1 if problems else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    forced = None
    for a in sys.argv[1:]:
        if a.startswith("--lang"):
            forced = a.split("=", 1)[1] if "=" in a else None
    sys.exit(main(args[0] if args else "docs/architecture", forced))
