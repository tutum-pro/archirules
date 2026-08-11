#!/usr/bin/env python3
"""Print the usage text of a skill, or list the skills that have one.

    help.py                 list every skill with its one-line description
    help.py <skill>         the full usage text of one skill

Claude Code does not parse flags. `/archirules:adr --help` passes the string
`--help` to the skill as `$ARGUMENTS`, and the skill's own instruction routes it
here. The routing is a sentence a model reads; **the answer is a file**. That
split is the whole point: a help text recited from memory drifts from the skill
it describes and nothing notices, which is a rule pretending to be enforced
(rule W9).

The usage text lives in a `## Usage` section of each `SKILL.md` and is written
for a person deciding whether to run the skill — what it needs from them, what it
will not do. The rest of the file is written for the model that runs it. Those
are different audiences and the section keeps them apart.

`selftest.sh` requires every skill to have one, so a skill added without usage
turns the self-test red rather than printing nothing at run time.
"""
import os
import re
import sys

SKILLS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills")
PLUGIN = "archirules"


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def frontmatter(text, key):
    """The value of one frontmatter key, or '' — the block only, never the body."""
    block = re.match(r"---\n(.*?)\n---", text, flags=re.S)
    if not block:
        return ""
    found = re.search(r"^%s:\s*(.+)$" % re.escape(key), block.group(1), flags=re.M)
    return found.group(1).strip() if found else ""


def usage(text):
    """The body of the `## Usage` section, or '' when the skill has none."""
    found = re.search(r"^## Usage\s*\n(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    return found.group(1).strip() if found else ""


def skills():
    """{name: (description, usage)} for every skill directory holding a SKILL.md."""
    out = {}
    if not os.path.isdir(SKILLS):
        return out
    for name in sorted(os.listdir(SKILLS)):
        path = os.path.join(SKILLS, name, "SKILL.md")
        if not os.path.isfile(path):
            continue
        text = read(path)
        out[name] = (frontmatter(text, "description"), usage(text))
    return out


def one_line(description):
    """First sentence only. A description is written to help a model choose a skill
    and is often three sentences long; a listing wants the first."""
    return re.split(r"(?<=[.!?])\s", description.strip())[0] if description else ""


def main(argv):
    found = skills()
    if not found:
        print("no skills found under %s" % SKILLS, file=sys.stderr)
        return 2

    if not argv:
        print("  archirules — skills in this plugin\n")
        for name, (description, _) in found.items():
            print("  /%s:%-14s %s" % (PLUGIN, name, one_line(description)))
        print("\n  Add --help to any of them for what it needs and what it will not do.")
        return 0

    name = argv[0].lstrip("/").replace("%s:" % PLUGIN, "")
    if name not in found:
        print("no skill named %r; there are: %s" % (name, ", ".join(found)), file=sys.stderr)
        return 2

    description, text = found[name]
    print("  /%s:%s — %s\n" % (PLUGIN, name, one_line(description)))
    if not text:
        # Refuse rather than guess (rule W1). Inventing a usage text here would be
        # the exact failure this script exists to prevent, and it would look like
        # success. The self-test makes sure a user never reaches this line.
        print("  This skill has no ## Usage section. That is a defect in the plugin,",
              file=sys.stderr)
        print("  not something you did — selftest.sh is supposed to catch it.", file=sys.stderr)
        return 1
    for line in text.split("\n"):
        print("  %s" % line if line.strip() else "")
    print("\n  Other skills: %s" % ", ".join(n for n in found if n != name))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
