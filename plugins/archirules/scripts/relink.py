#!/usr/bin/env python3
"""Turn bare register references in header fields into links.

    relink.py <path to docs/architecture> [--write]

Without `--write` it reports what it would change and touches nothing.

**Header fields only.** In a decision record that means the lines above its first `##`
section; in the open-questions register, the status line directly under each question's
heading. Prose is deliberately out of scope (ADR-0016): a paragraph naming a record three
times would carry three long links, and the readable version of the rule — "link the first
mention" — contains a judgement, which is the thing this method refuses to put inside a
gate.

The anchor for a question comes from `conform.py`'s own `slug`, imported rather than
reimplemented. Two copies of that rule would drift, and this tool would then produce links
the checker rejects.

Exit 0 when nothing needs converting, or when `--write` converted it. Exit 1 from a dry run
that found work, so a project can use it as a reminder. Exit 2 for a usage error.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import conform                                          # noqa: E402  (path set above)

LINK = re.compile(r"\[[^\]]*\]\([^)]*\)")
FIELD = re.compile(r"^\*\*[^*:]+:\*\*")
REFERENCE = re.compile(r"\b(?:ADR-\d{4}|OQ-\d+)\b")


def die(message):
    print("  %s" % message, file=sys.stderr)
    raise SystemExit(2)


def targets(directory):
    """({'ADR-0004': 'ADR-0004-name.md'}, {'OQ-07': 'oq-07--the-heading'})."""
    records, questions = {}, {}
    decisions = os.path.join(directory, "decisions")
    if os.path.isdir(decisions):
        for name in sorted(os.listdir(decisions)):
            match = re.match(r"(ADR-\d{4})", name)
            if match and name.endswith(".md"):
                records[match.group(1)] = name
    path = os.path.join(directory, "open-questions.md")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                match = re.match(r"^###\s+(OQ-\d+)\s+—", line)
                if match:
                    questions[match.group(1)] = conform.slug(line.lstrip("#").strip())
    return records, questions


def header_lines(path, text):
    """Line numbers that count as a header field in this file, and nothing else.

    Structural, not a pattern: a decision record's header is what stands above its first
    `##` section, and a question's is the line under its heading. Matching `**Word:**`
    anywhere instead would also catch `**To resolve:**` in the body of a question, which is
    prose and out of scope.
    """
    lines = text.split("\n")
    out = set()
    if os.path.basename(path).startswith("ADR-"):
        for i, line in enumerate(lines):
            if line.startswith("## "):
                break
            if FIELD.match(line):
                out.add(i)
    elif os.path.basename(path) == "open-questions.md":
        for i, line in enumerate(lines):
            if re.match(r"^###\s+OQ-\d+\s+—", line) and i + 1 < len(lines) \
                    and FIELD.match(lines[i + 1]):
                out.add(i + 1)
    return out


def convert(segment, records, questions, in_decisions):
    """Link every bare reference in a piece of text that holds no links already."""
    def one(match):
        ref = match.group(0)
        if ref.startswith("ADR"):
            if ref not in records:
                return ref        # refuse rather than guess; consistency.py reports it
            target = records[ref] if in_decisions else "decisions/" + records[ref]
        else:
            if ref not in questions:
                return ref
            target = ("../open-questions.md#" if in_decisions else "#") + questions[ref]
        return "[%s](%s)" % (ref, target)
    return REFERENCE.sub(one, segment)


def relink_line(line, records, questions, in_decisions):
    """Rebuild one line, leaving anything already a link exactly as it is.

    The obvious version of this — a lookbehind for `[` — is wrong, and was written and run
    before it was caught: a reference also occurs inside a link's own target path, where
    nothing precedes it, so a whole register got double-wrapped in one pass.
    """
    pieces, last = [], 0
    for match in LINK.finditer(line):
        pieces.append(convert(line[last:match.start()], records, questions, in_decisions))
        pieces.append(match.group(0))
        last = match.end()
    pieces.append(convert(line[last:], records, questions, in_decisions))
    return "".join(pieces)


def main(argv):
    write = "--write" in argv
    for arg in argv:
        if arg.startswith("--") and arg != "--write":
            die("unknown option: %s" % arg)
    positional = [a for a in argv if not a.startswith("--")]
    directory = positional[0] if positional else "docs/architecture"
    if not os.path.isdir(directory):
        die("no such register directory: %s" % directory)

    records, questions = targets(directory)
    changes = []
    for root, _, names in os.walk(directory):
        for name in sorted(names):
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            fields = header_lines(path, text)
            if not fields:
                continue
            in_decisions = os.path.basename(os.path.dirname(path)) == "decisions"
            lines = text.split("\n")
            touched = False
            for i in sorted(fields):
                new = relink_line(lines[i], records, questions, in_decisions)
                if new != lines[i]:
                    changes.append("%s:%d" % (os.path.relpath(path, directory), i + 1))
                    lines[i] = new
                    touched = True
            if touched and write:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("\n".join(lines))

    if not changes:
        print("  header fields: every reference is already a link")
        return 0
    print("  %s %d bare reference(s) in header fields"
          % ("linked" if write else "would link", len(changes)))
    for where in changes:
        print("    %s %s" % ("·" if write else "-", where))
    if not write:
        print("\n  Run again with --write to apply.")
    return 0 if write else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
