# ADR-0004 — The checker ships with a proof that it fails

**Status:** Accepted (2026-08-03)
**Related:** ADR-0005

## Context

The method's central execution rule is that a check which cannot fail is indistinguishable from
one that passes. The repository ships a conformance checker. If that checker is wrong, it
certifies broken projects — the failure mode is worse than having no checker, because it
produces confidence.

This is not hypothetical here. During development, successive versions of checks in this
repository produced false results **six times**, each for a different reason: a pattern matching
only a plural form, a keyword list too narrow, a regular expression the tool refused to compile
with its error discarded, a shell that does not word-split, a safety net tightened along with
the thing it watched, and an anchor validator whose own normalisation was wrong.

## Decision

**`selftest.sh` is part of the deliverable, not a development aid.**

It takes a known-good documentation set, breaks a copy in each way the checker claims to catch,
and requires the checker to notice — in both supported languages. Twenty-one cases.

Two design rules follow from the incidents:

- **Match prefixes, not exact wordings.** A wording variant is not a deviation.
- **Account for coverage, and refuse to conclude on a mismatch.** The checker compares headings
  that *look like* entries against headings that *parsed*. This is the only mechanism that
  caught any of the six failures automatically.

The safety net must be **looser** than what it watches. Tightened together, both go blind at
once and the mismatch never fires.

## Considered and rejected

**Trust the checker because it was reviewed.** All six broken versions looked correct on
reading. Reading is how they got in.

**Test the checker against the real register only.** It passes there by construction — that is
what it was written against. A fixture that can be broken deliberately is the only way to
observe failure.

**Ship the checker without the fixtures**, to keep the plugin small. The fixtures are what make
the self-test runnable by anyone; without them the proof is a claim.

## Consequences

**Positive.** "Zero problems" means something, because it has been demonstrated that "one
problem" is reachable. New checks have an obvious place to prove themselves.

**Costs, knowingly accepted.**

- **Test data ships inside the plugin** and can be mistaken for examples. Mitigated by a README
  in that directory saying plainly that it is not.
- **Fixtures must be maintained** alongside the checker; a new required section means updating
  both language sets.
- **The self-test is not run automatically.** It is a command a human or a CI job invokes. Until
  the CI example exists, its execution depends on discipline.

## Implementation status

Done. Twenty-one cases across both languages, including one asserting that the English set is
detected as English — so a silent fallback in language detection cannot pass unnoticed.
