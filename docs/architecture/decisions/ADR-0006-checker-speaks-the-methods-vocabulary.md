# ADR-0006 — A checker keys only on wording the method itself produces

**Status:** Accepted (decided by Robert Sternal, 2026-08-11)
**Unblocks:** P7 · **Related:** [ADR-0004](ADR-0004-checker-ships-with-its-own-proof.md)

## Context

`consistency.py` was written to check agreement **between** registers, and it invented the
vocabulary it needed: `Modifies:`, `Modified by:`, `## What changed`, `## Scope of supersession`,
`### What blocks`. None of those strings occurs anywhere else in this repository — not in
`templates/`, not in any `SKILL.md`, not in `RULES.md`. They exist in the checker and in the
fixtures the checker was tested against, and nowhere else.

The method's own mechanism for a reversed decision is different and older
([`adr/SKILL.md`](../../../plugins/archirules/skills/adr/SKILL.md), "Superseding"): a new record
carrying `Supersedes: ADR-NNNN`, and the old record carrying a status at the top —
`SUPERSEDED by ADR-MMMM`, with the date and the scope, because often only part of it is
superseded.

So the checker passed its self-test and failed reality. A register built by following that skill
literally — the licence decision reversed, the old record given its status line with date and
scope — was reported as broken:

```
x ADR-0002 is modified by ADR-0006 but has no 'What changed / Scope of supersession'
  section saying which points lost force
exit=1
```

The successor in that reproduction was a hypothetical record, which happened to take the number
this one now carries. The same construction, staged on a scratch copy with a successor numbered
past the end of this register, is the evidence recorded for phase P7 — and it now passes. It
stays on a scratch copy deliberately: a decision record invented to exercise a checker does not
belong in a register of real decisions.

This is the failure direction the verification skill names and nobody tests for: a sound
register reported as defective. It survived twenty-eight self-test cases because every one of
them ran against fixtures written in the checker's private vocabulary. **The self-test was
measuring its own artefact** (rule W8, case C-10) — it proved the checker consistent with its
fixtures, which was never in doubt.

## Decision

### 1. A checker keys only on wording a template or a skill produces

`Modifies:` and `Modified by:` are dropped. The relation the method actually has is
supersession — whole or partial — and its reverse link lives in the `Status` field, which is
where `adr/SKILL.md` already puts it. Nothing is lost: the two-way link check survives intact,
because both halves of the vocabulary it needs were already in the method.

### 2. Where the method left the wording implicit, the template states it

Two omissions surfaced, both of them the template lagging behind the skill rather than the
method lacking something:

- `templates/pl/ADR.md` documented `**Zastępuje:**` but never the Polish form of the superseded
  status, although `adr/SKILL.md` prescribes such a status for every language.
- `templates/*/OQ.md` documented `Depends on:` and `Touches:` but not `Blocks:`, although both
  `oq/SKILL.md` and rule P4 list all three.

Filling those in is not growing the method. The distinction is the one drawn in the hard gate
below, and it was applied rather than assumed — see "Considered and rejected".

### 3. A property of a single record belongs to `conform.py`

"A supersession names a scope, not just a pointer" is checkable inside one file, so it moves to
the structural checker. `consistency.py` keeps only what needs two files open at once. Without
that line there is no answer to why the plugin ships two scripts instead of one.

### 4. Each checker ships its own proof, and the binding requirement says so

The requirement in this register named one file, `scripts/selftest.sh`, from the days when there
was one checker. It now names the obligation instead of the file.

### 5. The vocabulary itself becomes a checked property

The self-test asserts that **every marker string either checker keys on occurs in a template or
in a skill**, searching outside the fixture directory. This defect was invisible to reading —
the checker looked correct, the fixtures looked correct, and they agreed with each other. Only a
check that leaves the pair can see it.

## Considered and rejected

### 1. Teach the templates the checker's vocabulary

Add `Modifies:`, `Modified by:` and a `## What changed` section to the ADR template, and be done
in ten minutes.

Rejected for three reasons, the last of them decisive. It introduces a second name for a
relation the method already has — partial supersession — and two names for one thing is what the
casebook is full of. It makes every register written before today non-conforming, for no defect
of theirs. And it is precisely the hard gate agreed at P7 before this work started: fields added
to a template whose only purpose is to satisfy a script mean the script was measuring its own
fixtures. The gate was written to be fired, and this is the case it was written for.

### 2. Accept both vocabularies as synonyms

Cheap, backward-compatible, nothing breaks. Rejected: dead vocabulary that no template produces
still has to be maintained, translated and explained, and it would leave the fixtures as the only
documents in existence written that way — which is the defect, still there, now with a
compatibility shim over it.

### 3. Keep the scope requirement in `consistency.py`

It works there and moving it costs a second fixture set and four more self-test cases. Rejected:
it is a single-file property, and putting it in the between-files checker erases the only line
that distinguishes the two scripts. A boundary that is argued in a record and ignored in the
code is not a boundary.

### 4. Drop cross-record checking altogether

The literal remedy the P7 gate offers. Rejected because the gate's condition was not met for
this check: the two-way link check needed **nothing** added to the method — `Supersedes:` and
the `SUPERSEDED by` status were both already there. Only the scope requirement needed a home,
and it had one. The gate did fire once, on the blocker table (decision 6 below), and there the
answer was to add nothing.

### 5. Give the phase template a blocker table

Two of the five cross-register checks only run where the phase register keeps one, and no
template produces it. Adding it would switch those checks on everywhere.

Rejected — this is the case where the gate genuinely fires. The blocker table appears in no rule
and no skill; it is duplicated state, the same fact written in the question and in the phase
register, and duplicated state is what this checker exists to police. Registered as
[OQ-06](../open-questions.md#oq-06--should-the-blocker-table-be-part-of-the-method-or-stay-a-project-convention)
rather than settled on the spot. Until it is answered, those two checks stay skipped and the
skip stays printed.

## Consequences

**Positive.** A register produced by following the skills is accepted by the checkers, which was
not true before this record. The self-test now fails when the plugin's own documentation and its
scripts drift apart, so the class of defect this record exists to fix cannot return silently.
The two scripts have a stated axis — inside one file, between files — and a check can be placed
by reading it.

**Costs, knowingly accepted.**

- **Two checkers and two self-tests.** An audit is four commands, not two. Accepted because
  merging them would mean one script with two unrelated failure modes, and the audit skill would
  still have to explain the difference.
- **A template edit is no longer free.** Renaming a heading in `templates/` can now fail the
  self-test. That is the mechanism working, but it is a cost paid on every future translation
  and rewording.
- **The reference sets had to be rewritten, not translated.** Cases that passed against the old
  vocabulary say nothing about the new one, so every case was re-derived. The self-test's case
  count is not comparable across this change.
- **The vocabulary check is a whole-string search, not a parse.** A marker that appears in a
  template only inside a comment, or only in prose, satisfies it. It catches invention, which is
  the defect that happened; it does not catch a marker that is documented but unreachable.
- **Cross-register coverage stays partial by default.** Where no blocker table is kept, two of
  five checks do not run. Visible in the output, unanswered until OQ-06.

## Implementation status

Done and verified. `consistency.py` keys on `Supersedes` and the superseded status word only;
`conform.py` carries the supersession-scope check; both self-tests were extended and both were
shown to fail. Numbers, commands and the mutation re-derivation are in the
[verification register](../verification.md#the-cross-register-checker) rather than repeated
here, because they change whenever a case is added and a record that quotes them goes stale.

Deliberately not done: checking that a supersession status carries a **date** as well as a
scope, although `adr/SKILL.md` asks for both. Every additional required token is another way to
report a sound register as broken, and the date has no cross-record consequence — nothing
resolves differently for the absence of it. Reconsider if a register is ever found with a
supersession nobody can place in time.

Limits recorded rather than fixed:
[OQ-05](../open-questions.md#oq-05--is-a-stale-blocker-findable-anywhere-except-the-questions-own-field)
and
[OQ-06](../open-questions.md#oq-06--should-the-blocker-table-be-part-of-the-method-or-stay-a-project-convention).
