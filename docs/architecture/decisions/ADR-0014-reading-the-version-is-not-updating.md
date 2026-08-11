# ADR-0014 — Reading which version a project stands at is a separate, read-only act

**Status:** Accepted (decided by Robert Sternal, 2026-08-11)
**Unblocks:** P14 · **Related:** [ADR-0009](ADR-0009-updating-a-project-is-not-updating-the-plugin.md)

## Context

An archirules project carries two versions: the **method** installed, in the plugin's manifest,
and the **registers**, in `.archirules-version`, recording what they were last brought up to.
They can disagree, and the disagreement is the thing worth knowing.

Nothing showed both. `claude plugin list` shows the first and knows nothing about a project.
`/archirules:update` computes both — and then **refuses to start on a dirty working tree**,
which is correct for a command that edits registers and useless for the moment the question
actually gets asked: mid-task, with uncommitted work, deciding whether an update is due.

The need was reported by somebody using the method rather than derived from the design. That is
the evidence this project treats as strongest, and the only kind that finds this class of gap —
the author of a tool does not notice the question they never have to ask.

## Decision

### 1. A read-only skill, and its script writes nothing

`/archirules:version` reads two files and prints. No snapshot, no migration, no clean tree, no
git repository required. The whole point is that it answers where `/archirules:update` refuses.

### 2. "Ahead" is a distinct outcome, not a variant of "behind"

Registers newer than the installed method mean a downgraded plugin, or registers written on a
machine with a newer archirules. **No migration runs backwards.** Printing the same advice as for
"behind" would send somebody to `/archirules:update`, which would take a snapshot and then have
nothing to do. The fix is to update the plugin, and the output says so.

### 3. A version that cannot be read is a non-zero exit

No stamp, an empty stamp, a stamp holding something that is not a version: all exit 1. A question
that cannot be answered is not the same as an answer, and exit 0 would say the project is fine.

### 4. It never guesses the missing version

It reports the consequence — `/archirules:update` will treat the project as 1.0.0 and list every
migration — and offers to record one **only if the user knows it**. Inferring a version from the
shape of the registers was already rejected in
[ADR-0009](ADR-0009-updating-a-project-is-not-updating-the-plugin.md): shape cannot distinguish
"written at 1.0.0" from "written later and missing a section", and guessing high skips migrations
in silence.

### 5. It says nothing about whether the registers are correct

Only which version they claim. A project can sit at the current version with a register that
contradicts itself. That is what the checkers are for, and the skill says so rather than letting
a green line be read as a clean bill of health.

## Considered and rejected

### 1. Nothing — `claude plugin list` already exists

It shows the installed plugin version, which is one of the two numbers and not the interesting
one. Rejected: the question is whether **this project** matches the installed method, and no
tool outside archirules can answer that, because `.archirules-version` is this method's own file.

### 2. Fold it into `/archirules:update`

It already computes both versions and stops when they agree, so the information is there.
Rejected on two grounds. It refuses on a dirty tree, so it cannot answer at the moment the
question is asked. And nobody invokes a command called *update* to ask a question — the naming
alone deters it, and a tool people avoid running is a tool that does not exist.

### 3. A flag on `/archirules:audit`

Audit already runs everything and reports. Rejected: audit answers whether the registers are
**correct**, this answers which version they **are**. Different questions, and folding them means
running three checkers and two self-tests to read two files.

### 4. Make "behind" informational — exit 0 with a note

Friendlier, and avoids a red on every project that has not migrated yet. Rejected: it would make
the most common real answer the one that exits successfully, and no CI could gate on "is this
project on the current method". A status command whose interesting outcome is indistinguishable
from its boring one is a status command nobody wires into anything.

## Consequences

**Positive.** The two-version question has an answer that costs nothing to ask, works mid-task,
and distinguishes three outcomes that need three different responses. "Ahead" in particular can
no longer be mistaken for "behind", which is the one that would have wasted somebody's afternoon.

**Costs, knowingly accepted.**

- **A tenth skill.** The set grows, each one costs context in the listing, and every future
  reader has one more thing to understand before finding the one they want.
- **It duplicates half of what `/archirules:update` computes.** Two places now read the same two
  files, and a change to where the version lives has to reach both. Accepted because folding them
  costs the dirty-tree case, which is the reason this exists.
- **Exit 1 on a project that never adopted version stamping.** Such a project sees a red every
  time it asks, for a condition it may have chosen. One line fixes it, and the message says which
  line, but the default is a complaint.
- **It invites being read as a health check.** A green line says the versions match and nothing
  about whether the registers hold together. Stated in the skill; nothing enforces that a reader
  believes it.

## Implementation status

Done. `scripts/version.py`, `skills/version/`, and eight self-test cases covering the three
disagreement shapes, the two unreadable ones, agreement, and a usage error.

Shown to fail under two mutations that break **different** subsets: with the script always
returning 0, the five cases expecting a finding go red; with the script made unimportable, the
three that do not — the agreement case, the usage-error case, and the one that reads printed
output rather than an exit code. Neither mutation alone covers the set, which is why both were
run.
