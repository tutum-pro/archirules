# ADR-0010 — Traceability lives in commit trailers and is derived, never copied into a register

**Status:** Accepted (decided by Robert Sternal, 2026-08-11)
**Unblocks:** P11 · **Related:** [ADR-0006](ADR-0006-checker-speaks-the-methods-vocabulary.md)

## Context

The registers say what was decided and what was to be built. Git says what was actually built.
Nothing connected the two, so "is this phase really done" was answerable only by reading code and
trusting a memory of which commits belonged to it.

The obvious fix is to write commit identifiers into the phase register when a phase closes. It is
also the fix this project has already argued against twice: a fact kept in two places is what
`consistency.py` exists to police, and a commit identifier is worse than most, because it stops
being true at the first rebase, squash or cherry-pick and nothing about the register looks
different afterwards.

## Decision

### 1. The claim lives in the commit, in a trailer

```
Archirules-Phase: P11
Archirules-ADR: 0010
Archirules-OQ: 05
```

One commit may carry several. Git history is the single source of truth, and it is the one
artefact here that cannot drift from the work, because it **is** the work.

### 2. The readable view is generated, and the generator is a checker

`traceability.md` is written by `trace.py --write` and never by hand. Being generated is not
enough on its own — a generated file can be edited afterwards and nothing would notice — so the
check **recomputes the view and byte-compares**. A hand-edited traceability table is a finding.

This is what the user asked for and it is worth naming as a cost: the view is a second copy of
what git already knows. It is accepted because it is derived on demand and verified against its
source, which is the property a hand-maintained list can never have.

### 3. The view records the commit it was generated at, and is checked against that

Comparing against `HEAD` instead would make the file stale the instant it is committed: the
commit that writes it cannot contain its own identifier. So the file records its own basis and
the check recomputes at that basis.

The working pattern that follows: commit the work with trailers, regenerate, and commit the view
**in a commit carrying no trailer**. A trailerless commit adds nothing to the view, so the view
stays current instead of chasing itself.

### 4. Two checks always, two behind `--strict`

Always: a trailer naming an entry no register holds, and a view that is not a faithful
regeneration. Both are safe in any repository at any age.

Behind `--strict`: a closed phase no commit claims, and a view behind HEAD. This repository
cannot satisfy either — ten phases closed before the mechanism existed and their history is
pushed. Enabling them by default would ship a gate that fails on day one for reasons nobody can
fix, and the thing people do with such a gate is switch it off. Carried as
[OQ-07](../open-questions.md#oq-07--when-should---strict-traceability-become-the-gate-rather-than-an-option).

## Considered and rejected

### 1. Commit identifiers written into the phase register

What the register would look like if a person did this by hand, and readable with no tooling at
all. Rejected: it is duplicated state that goes wrong silently. A rebase rewrites every SHA and
leaves a register full of identifiers that resolve to nothing, or worse, to something else. This
project polices exactly that class of defect in other people's documents.

### 2. Trailers only, with no generated view

Purest version: git holds everything, `trace.py` answers questions on demand, no file to keep
current. Rejected because auditability that requires running a tool is not auditability for the
person doing the audit — they want to see the mapping, in the register, next to what it maps.
The compromise is that the view is generated and verified rather than maintained.

### 3. A git hook that adds the trailer automatically

`commit-msg` could refuse a commit with no trailer, or add one. Rejected on two counts. Hooks
live in `.git/hooks`, which is not versioned, so every clone would have to install it and most
would not — a rule enforced on some machines is a rule nobody can rely on. And a trailer added
automatically would be a guess about which register entry a commit belongs to, which is the one
thing here that needs a person.

### 4. A `PostToolUse` hook in the plugin, matching `git commit`

The plugin system does allow it. Rejected: matching a shell command by pattern is fragile —
`git commit`, `git commit -F -`, a commit made by a tool that is not Bash — and a mechanism that
works most of the time produces a trace with holes in it that look like absences of work.

## Consequences

**Positive.** A register entry can be traced to the commits that implement it, and the reverse: a
commit says which decision it serves. The mapping cannot rot, because it is derived. A trailer
naming a register entry that does not exist is caught, which is the traceability equivalent of a
dangling reference.

**Costs, knowingly accepted.**

- **The trailer is written by hand and can be forgotten.** Nothing catches a commit that should
  have carried one — only `--strict` does, and it is off. This is the honest limit of the
  mechanism and the subject of OQ-07.
- **A generated file in the register.** It is a second copy of what git knows, accepted because
  it is verified against its source on every audit. It also changes on most commits, so diffs get
  noisier.
- **The two-commit pattern is a rule people will forget.** Work with trailers, then the view
  without. Forgetting it produces a view one commit behind, which is tolerated by default and
  therefore easy not to notice.
- **Ten phases will never be traceable.** P1 to P10 closed before this existed and their history
  is pushed. They are listed under their own heading in the view, permanently.
- **Trailers are English and unversioned.** `Archirules-Phase` is part of the executable layer
  (ADR-0001), so a project working in Polish still writes English trailers. Renaming them later
  would silently orphan every commit already carrying the old spelling.

## Implementation status

Done. `scripts/trace.py`, `traceability.md` in this register, trailers documented in
`phases/SKILL.md` and `audit/SKILL.md`, and the vocabulary assertion extended so that
`trace.py`'s trailers must appear in a skill exactly as the checkers' markers must.

Ten self-test cases, run against a throwaway git repository built by the test rather than a
fixture directory — the thing under test is what history says, and a fixture has no history.
Shown to fail on: a trailer naming a missing entry, a hand-edited view, a missing view, a view
recording no commit, a view behind HEAD under `--strict`, an unknown option, and a directory
outside a repository. Usage errors exit 2, so they cannot be read as findings about a register.
