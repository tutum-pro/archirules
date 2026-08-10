#!/usr/bin/env python3
"""Print the migration work between two versions of the method, read from CHANGELOG.md.

    migrations.py --from 1.0.0 [--to 1.2.0] [--changelog PATH]

`/archirules:update` reads this and nothing else. The contract, set in ADR-0007:

  **An entry with no `### Migration` block requires nothing of the reader.** That is what
  its absence means. So "no migration blocks in range" is a RESULT, printed plainly —
  never an empty output that could equally mean the script failed to find the file.

Exit 0 when the range was read, whether or not it contained work. Exit 2 for a usage
error: an unreadable changelog, or a version that is not in it. Refusing on an unknown
version matters more here than anywhere else in this plugin — a migration that silently
skips a version it did not recognise leaves a register half-converted, which is the one
outcome worse than not migrating at all (rule W1).
"""
import os
import re
import sys

DEFAULT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "CHANGELOG.md")


def die(message):
    print("  %s" % message, file=sys.stderr)
    raise SystemExit(2)


def parse_args(argv):
    values = {"--from": None, "--to": None, "--changelog": DEFAULT}
    awaiting = None
    for arg in argv:
        if awaiting:
            values[awaiting], awaiting = arg, None
        elif arg in values:
            awaiting = arg
        elif "=" in arg and arg.split("=", 1)[0] in values:
            key, value = arg.split("=", 1)
            values[key] = value
        else:
            die("unknown argument: %s" % arg)
    if awaiting:
        die("%s needs a value" % awaiting)
    if not values["--from"]:
        die("--from is required: the version the project is at")
    return values


def as_number(version):
    """(1, 2, 0) for '1.2.0' — comparable, and a wrong shape is a usage error."""
    if not re.fullmatch(r"\d+\.\d+\.\d+", version or ""):
        die("%r is not a semantic version" % version)
    return tuple(int(part) for part in version.split("."))


def entries(text):
    """[(version, body)] newest first, for every '## X.Y.Z' heading."""
    out = []
    for found in re.finditer(r"^## (\d+\.\d+\.\d+)[^\n]*\n(.*?)(?=^## \d|\Z)", text,
                             flags=re.M | re.S):
        out.append((found.group(1), found.group(2)))
    return out


def migration(body):
    """The '### Migration' block of one entry, or '' when it has none."""
    found = re.search(r"^### Migration\s*\n(.*?)(?=^### |\Z)", body, flags=re.M | re.S)
    return found.group(1).strip() if found else ""


def main(argv):
    values = parse_args(argv)
    try:
        with open(values["--changelog"], encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        die("cannot read %s: %s" % (values["--changelog"], exc))

    releases = entries(text)
    if not releases:
        die("%s holds no version headings" % values["--changelog"])

    known = {version for version, _ in releases}
    target = values["--to"] or releases[0][0]
    for label, version in (("--from", values["--from"]), ("--to", target)):
        as_number(version)
        if version not in known:
            die("%s %s is not in the changelog; it knows: %s"
                % (label, version, ", ".join(sorted(known, key=as_number))))

    start, end = as_number(values["--from"]), as_number(target)
    if start > end:
        die("--from %s is newer than --to %s; this script does not undo releases — "
            "restore the snapshot instead" % (values["--from"], target))

    # Oldest first: migrations are applied in the order they were released, and a later
    # one may assume the earlier one has run.
    applicable = [(version, migration(body)) for version, body in reversed(releases)
                  if start < as_number(version) <= end]
    work = [(version, block) for version, block in applicable if block]

    print("  archirules %s → %s · %d release(s) in range · %d with register changes"
          % (values["--from"], target, len(applicable), len(work)))
    if not applicable:
        print("\n  Already at %s. Nothing to do." % target)
        return 0
    if not work:
        print("\n  None of these releases changes anything in a register:")
        for version, _ in applicable:
            print("    %s" % version)
        print("\n  Update the plugin; the registers need no work.")
        return 0
    for version, block in work:
        print("\n  ── %s ──" % version)
        for line in block.split("\n"):
            print("  %s" % line if line.strip() else "")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
