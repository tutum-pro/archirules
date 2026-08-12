# ADR-0003 — The casebook is separate from the rules

**Status:** Accepted (2026-08-03)
**Resolves:** [OQ-02](../open-questions.md#oq-02--how-do-we-learn-what-a-newcomer-cannot-understand) · **Related:** [ADR-0001](ADR-0001-language-split.md)

## Context

Every rule in the method came from a specific failure in the project it was extracted from, and
the first version told each failure inline, with that project's details: named markers in
Polish, particular counts, a specific engine.

A reader outside that project reported that the rules were hard to follow — not because the
rules were wrong, but because their justification assumed context that was unavailable. In one
case, the audit skill showed Polish marker strings in a table without saying what they were.

This is a real risk to adoption. A rule that cannot be understood is not followed.

## Decision

**Two layers of text.**

- **Rules** state the principle and the failure shape generically, and are readable standalone.
- **The casebook** holds the incidents in full, numbered `C-NN`, referenced from the rules.

A rule may say "silent degradation is worse than refusal because it looks like success" and
point at `C-09`. The reader who wants the principle stops there; the reader who wants the
evidence follows the link.

The casebook names its origin once, at the top, rather than assuming it: "all of them come from
one project — a leasing platform built in Go".

## Considered and rejected

**Strip the anecdotes entirely.** Cheapest, and it removes the only reason to believe the rules.
A rule without its failure is a preference; with it, it is a conclusion.

**Generalise the anecdotes in place.** Keeps one document but loses the specificity that makes
an incident recognisable — and a generic incident convinces nobody.

**Keep them inline and add a glossary.** Treats the symptom. The problem is not vocabulary, it
is that a reader must absorb somebody else's project to reach a rule they could otherwise
apply immediately.

## Consequences

**Positive.** Rules are usable on first reading. Evidence is preserved and, being collected,
is easier to extend. Each case is written to be recognised in the reader's own work rather than
understood as history.

**Costs, knowingly accepted.**

- **Two documents to keep in step.** A rule whose case is deleted becomes an assertion; a case
  whose rule is renamed dangles. Both link directions are checked.
- **The casebook needs its own translation.** Same drift risk as everything else in ADR-0001.
- **Some vividness is lost** where a rule now states a shape instead of telling a story.

## Implementation status

Done. Ten cases, both languages. Twenty links from the rules to case anchors, all verified to
resolve — after the first anchor validator turned out to be wrong itself and reported all ten
as broken.
