#!/usr/bin/env python3
"""Everything the registers contain, in one screen, so that reading them is a choice.

    digest.py [<path to docs/architecture>]

One line per entry: what it is, what state it is in, what it is about, and — for a
decision — which file holds it. That is what somebody needs in order to decide **which
document to open**, and it is all they need.

**This prints; it does not write a file.** An index kept as a file is another artefact
that can go stale, needs a check to prove it has not, and joins the set of things a reader
must be told about. A command cannot go stale: it reads the registers at the moment it is
asked. The generated traceability view is a file for the opposite reason — it exists to be
read by a person auditing the project, in the register, months later. This exists to spare
a machine from reading 48 000 tokens to answer a question about fourteen of them.

Language-agnostic on purpose: every status is printed as the register wrote it, so nothing
here needs a marker table and nothing drifts when one changes.

Exit 0 always, unless the directory is not a register — this reports, it does not judge.
"""
import glob
import os
import re
import sys

PHASE_FILES = ("fazy-realizacji.md", "phases.md")
VERIFICATION_FILES = ("rejestr-weryfikacji.md", "verification.md")


def die(message):
    print("  %s" % message, file=sys.stderr)
    raise SystemExit(2)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def first_existing(directory, names):
    for name in names:
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            return path
    return None


def decisions(directory):
    """[(number, status, subject, filename)] — read from the records, not from the index.

    The index in README.md carries the same three facts and is cheaper to parse, but it is
    maintained by hand and nothing checks that its status column still matches the record.
    Reading the records costs this script sixteen file opens and costs the reader nothing.
    """
    out = []
    for path in sorted(glob.glob(os.path.join(directory, "decisions", "ADR-*.md"))):
        text = read(path)
        title = re.match(r"^#\s+(?:ADR-\d{4}\s*[—–-]\s*)?(.*)", text)
        status = re.search(r"^\*\*Status:\*\*\s*(.+?)\s*$", text, flags=re.M)
        cleaned = re.sub(r"\s*·.*$", "", status.group(1)) if status else "?"
        cleaned = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cleaned)
        out.append((os.path.basename(path)[:8],
                    re.sub(r"\s*\([^)]*\)\s*$", "", cleaned).strip(),
                    title.group(1).strip() if title else "?",
                    os.path.basename(path)))
    return out


def questions(directory):
    """[(number, status, subject)] for every question, open or not."""
    path = os.path.join(directory, "open-questions.md")
    if not os.path.isfile(path):
        return []
    out, lines = [], read(path).split("\n")
    for i, line in enumerate(lines):
        heading = re.match(r"^###\s+(OQ-\d+)\s+[—–-]\s+(.*)", line)
        if not heading:
            continue
        status = "?"
        if i + 1 < len(lines):
            found = re.match(r"^\*\*Status:\*\*\s*(\S+)", lines[i + 1])
            if found:
                status = found.group(1)
        out.append((heading.group(1), status, heading.group(2).strip()))
    return out


def phases(directory):
    """[(id, status, name)] from the first columns of the phase table."""
    path = first_existing(directory, PHASE_FILES)
    if not path:
        return []
    return [(pid, status.strip(), name.strip())
            for pid, name, status in re.findall(
                r"^\|\s*([A-Za-z]\w*)\s*\|([^|]*)\|\s*([☐◐☑⛔][^|]*)\|", read(path), flags=re.M)]


def verification(directory):
    """{label: count} for the register's own entry labels, whatever they happen to be."""
    path = first_existing(directory, VERIFICATION_FILES)
    if not path:
        return {}, 0
    text = read(path)
    labels = {}
    for label in re.findall(r"^\*\*([A-Z][^*]{2,80}?)\.?\*\*", text, flags=re.M):
        text_of = label.strip().lower()
        if text_of.startswith("not verified") or text_of.startswith("not traceable"):
            key = "not verified"
        elif text_of.startswith("asserted"):
            key = "asserted, not verified"
        elif text_of.startswith("verified"):
            key = "verified"
        else:
            continue
        labels[key] = labels.get(key, 0) + 1
    return labels, len(re.findall(r"^## ", text, flags=re.M))


def main(argv):
    for arg in argv:
        if arg.startswith("--"):
            die("unknown option: %s" % arg)
    directory = argv[0] if argv else "docs/architecture"
    if not os.path.isdir(directory):
        die("no such register directory: %s" % directory)

    adrs, oqs, phs = decisions(directory), questions(directory), phases(directory)
    labels, subjects = verification(directory)
    if not (adrs or oqs or phs):
        die("%s holds no registers this can read" % directory)

    open_now = sum(1 for _, status, _ in oqs if status.upper() in ("OPEN", "OTWARTE"))
    done = sum(1 for _, status, _ in phs if status.startswith("☑"))
    print("  %s · %d decisions · %d questions (%d open) · %d phases (%d done)"
          % (directory, len(adrs), len(oqs), open_now, len(phs), done))

    if adrs:
        print("\n  DECISIONS")
        for number, status, subject, fname in adrs:
            print("    %-8s %-12s %s" % (number, status[:12], subject))
        print("    (open one with: decisions/ADR-NNNN*)")
    if oqs:
        print("\n  QUESTIONS")
        for number, status, subject in oqs:
            print("    %-6s %-10s %s" % (number, status[:10], subject))
    if phs:
        print("\n  PHASES")
        for pid, status, name in phs:
            print("    %-5s %-13s %s" % (pid, status[:13], name))
    if labels:
        print("\n  VERIFICATION · %d subjects · %s"
              % (subjects, " · ".join("%d %s" % (n, k.lower())
                                      for k, n in sorted(labels.items(), key=lambda kv: -kv[1]))))
    print("\n  Open a document only when this is not enough.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
