# ADR-0008 — `--help` is routed by a sentence and answered by a file

**Status:** Accepted (decided by Robert Sternal, 2026-08-11)
**Unblocks:** P9 · **Related:** [ADR-0004](ADR-0004-checker-ships-with-its-own-proof.md)

## Context

A user asked for `/archirules:<skill> --help`. Claude Code does not parse flags for skills: the
text after the skill name arrives as `$ARGUMENTS`, and whatever happens next happens because a
sentence in `SKILL.md` told the model to make it happen.

So the whole feature could be seven sentences — "if `$ARGUMENTS` is `--help`, summarise what
this skill does" — and it would appear to work immediately. It would also be a help text
recited from memory: correct on the day it is written, drifting from the skill afterwards, with
nothing to notice. That is the definition rule W9 gives for the worst kind of rule — one that
pretends to be enforced, so nobody watches it and everybody assumes somebody else does.

The plugin already had this argument once. `conform.py` exists because reading a document is not
the same as checking it.

## Decision

### 1. The routing is a sentence; the answer is a file

Each `SKILL.md` carries one instruction: on `--help`, run
`help.py <name>`, show the output, stop. The text itself comes from a `## Usage` section of that
same `SKILL.md`, extracted by the script. Only the routing is left to the model, and routing is
the part that has no other option.

### 2. Usage is written for a person, the rest of the file for a model

They are different audiences. The body of a `SKILL.md` is a procedure for the model executing
it; `## Usage` answers what a person wants before running something: what it needs from me, what
it will not do, what it costs me if I am wrong about it. Keeping them in one file with separate
headings means the two cannot drift apart into separate documents.

Every usage section states **"Will not"** explicitly. A skill's limits are the part a reader
cannot infer and the part that wastes their afternoon.

### 3. Discovery without an eighth skill

`help.py` with no argument lists every skill, and each skill's help ends with the others' names.
There is no `/archirules:help`, because a skill whose only job is to list skills is one more
thing to keep true.

### 4. The self-test checks four things, not one

That the section exists; that the file routes `--help` to the script **for its own name**; that
the usage does not name a different skill in its invocation line — the copy-paste defect, which
reads perfectly and sends the user elsewhere; and that the script actually produces output for
each skill. The last is what makes the other three more than a spelling check.

## Considered and rejected

### 1. One sentence per `SKILL.md`, no script

Fifteen minutes, no new code, works on the first try. Rejected: it is a rule with no
enforcement, and this repository's own binding requirements say that a rule which can be checked
mechanically should be. A help text nothing verifies is worse than none, because a user who
reads it believes it.

### 2. A single `/archirules:help` skill

Simpler, one place, no per-skill boilerplate. Rejected: it answers "what skills are there",
which `/help` already answers, and not "what does this one need from me" — which is the question
that made the user ask. Kept the listing, dropped the skill: `help.py` with no argument does it.

### 3. Generate usage from the skill body

No new sections, nothing to keep in sync, and the material is already there. Rejected: the body
is a procedure written for a model, and a summary of it answers a different question than the
one asked. Generation would also have to guess which limits matter, and a guessed limit stated
confidently is worse than a stated one.

### 4. Frontmatter fields instead of a section

`usage:` and `limits:` keys in the YAML block. Rejected: Claude Code reads specific keys from
that block and ignores others, so the plugin would depend on unspecified behaviour for a feature
that works fine in Markdown. Multi-paragraph text in YAML is also worse to write and worse to
read in a diff.

## Consequences

**Positive.** A user can ask any skill what it needs before running it, and the answer comes
from the same file as the skill. A skill added without usage cannot reach a release: the
self-test goes red, naming the skill.

**Costs, knowingly accepted.**

- **Seven files carry near-identical boilerplate.** The routing sentence is duplicated per
  skill because there is no shared preamble mechanism. Checked, so it cannot rot silently, but
  still duplication.
- **Usage sits in the model's context on every invocation.** A skill that runs pays a few
  hundred tokens for text meant for a human. Accepted as small against keeping the two in one
  file.
- **Routing remains probabilistic.** The model could ignore the instruction and answer from its
  own reading. Nothing available in the plugin system prevents that; what the mechanism
  guarantees is that a correct routing produces a correct, current answer.
- **The "will not" lines are prose and unverifiable.** Nothing checks that they are true. They
  are the most useful part of the text and the part with the least enforcement, which is stated
  here rather than left to be discovered.

## Implementation status

Done. `scripts/help.py`, a `## Usage` section in all seven skills, and a self-test case shown to
fail in five shapes: a new skill added without usage, a section removed, a routing line broken,
a usage naming another skill, and the script itself made unimportable. The last prints one line
per skill rather than going quiet, which is the C-11 lesson applied.
