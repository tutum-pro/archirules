#!/usr/bin/env python3
"""Report which version of the method is installed and which one the registers stand at.

    version.py [<path to docs/architecture>]

There are two versions in an archirules project and they can disagree:

  * the **method** installed, from the plugin's `plugin.json`;
  * the **registers**, from `docs/architecture/.archirules-version`, which records what they
    were last brought up to.

Nothing else shows both. `claude plugin list` shows the first and knows nothing about a
project; `/archirules:update` shows both but refuses to start on a dirty working tree —
which is exactly when somebody is mid-task and wants to know where they stand. This reads
two files, writes nothing, and needs neither a clean tree nor a git repository.

Exit 0 when the two agree, 1 when they do not, 2 for a usage error. "Do not agree"
deliberately includes **registers newer than the installed method**: that is a downgraded
plugin or a register written against an archirules this machine does not have, and reading
it as "fine" would be the silent kind of wrong (rule W1). It also includes a project with
no recorded version, because a question that cannot be answered is not the same as an
answer.
"""
import json
import os
import re
import sys

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAMP = ".archirules-version"


def die(message):
    print("  %s" % message, file=sys.stderr)
    raise SystemExit(2)


def as_number(version):
    """(1, 6, 1) for '1.6.1', or None when it is not a semantic version."""
    return (tuple(int(p) for p in version.split("."))
            if re.fullmatch(r"\d+\.\d+\.\d+", version or "") else None)


def method_version():
    path = os.path.join(PLUGIN, ".claude-plugin", "plugin.json")
    try:
        with open(path, encoding="utf-8") as fh:
            declared = json.load(fh).get("version")
    except (OSError, ValueError) as exc:
        die("cannot read the plugin manifest at %s: %s" % (path, exc))
    if not declared:
        die("%s declares no version; this plugin is not installable as a release" % path)
    return declared


def register_version(directory):
    """(text, problem) — the recorded version, or None with the reason it is absent."""
    path = os.path.join(directory, STAMP)
    if not os.path.isfile(path):
        return None, ("these registers record no version; `/archirules:update` will treat the "
                      "project as 1.0.0 and list every migration ever written")
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read().strip()
    except OSError as exc:
        die("cannot read %s: %s" % (path, exc))
    if not text:
        return None, "%s is empty" % STAMP
    if as_number(text) is None:
        return None, "%s holds %r, which is not a semantic version" % (STAMP, text)
    return text, None


def main(argv):
    for arg in argv:
        if arg.startswith("--"):
            die("unknown option: %s" % arg)
    directory = argv[0] if argv else "docs/architecture"
    if not os.path.isdir(directory):
        die("no such register directory: %s — run this from the project root, or pass the path"
            % directory)

    method = method_version()
    registers, problem = register_version(directory)

    if problem:
        print("  archirules %s installed · registers: unknown" % method)
        print("    x %s" % problem)
        print("    Record it with: printf '%%s\\n' <version> > %s"
              % os.path.join(directory, STAMP))
        return 1

    here, there = as_number(registers), as_number(method)
    if here == there:
        print("  archirules %s installed · registers at %s · up to date" % (method, registers))
        return 0

    if here > there:
        # Not a variant of "behind". Either the plugin was downgraded or these registers
        # were written against an archirules this machine does not have, and no migration
        # runs backwards.
        print("  archirules %s installed · registers at %s · REGISTERS ARE AHEAD"
              % (method, registers))
        print("    x the registers were written against a newer archirules than the one "
              "installed here")
        print("    Update the plugin rather than the project: /plugin update archirules@<market>")
        return 1

    print("  archirules %s installed · registers at %s · behind" % (method, registers))
    print("    x the registers have not been brought up to the installed method")
    print("    See what changed:  python3 %s --from %s --to %s"
          % (os.path.join(PLUGIN, "scripts", "migrations.py"), registers, method))
    print("    Then:              /archirules:update")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
