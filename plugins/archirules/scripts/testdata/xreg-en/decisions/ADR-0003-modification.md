# ADR-0003 — Reaches back to two earlier records

**Status:** Accepted · **Supersedes:** [ADR-0001](ADR-0001-base.md), [ADR-0002](ADR-0002-superseded.md) · **Resolves:** OQ-02

## Decision

A record reaching back to two earlier ones: it strips one of force in part and the
other in whole. **Both have to know about it on their own side** — a one-way link is a
record that stopped being true at one end, and that end is the one a reader arrives at
first.

## Consequences

**Positive.** The history of a decision can be walked in both directions.

**Cost, taken knowingly.** Every supersession means two files to change, not one.

## Implementation state

Serves the checker's test only.
