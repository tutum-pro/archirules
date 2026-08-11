# ADR-0001 — Base

**Status:** SUPERSEDED by [ADR-0003](ADR-0003-modification.md), 2026-08-11 — the second point only; the rest holds

## Decision

A record a later one strips of force **in part**. It stays in the register: the history
of a decision is part of the decision.

The scope sits in the status line and not in a section below it. A correction written
under a field that still says the old thing is not a correction — rule P7, case C-04.
That placement is also why the scope is checked by `conform.py`, which reads one file at
a time, and not here.

## Consequences

**Positive.** The checker has a correct two-way link to recognise: forward from
ADR-0003's `Supersedes`, back from this status line.

**Cost, taken knowingly.** The reference set has to be maintained alongside the checker.

## Implementation state

Serves the checker's test only.
