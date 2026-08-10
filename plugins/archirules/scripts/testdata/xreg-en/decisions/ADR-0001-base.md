# ADR-0001 — Base

**Status:** Accepted · **Modified by:** [ADR-0003](ADR-0003-modification.md)

## Decision

A record a later one strips of force in part. It stays in the register — the history of
a decision is part of the decision.

## What changed

[ADR-0003](ADR-0003-modification.md) strips the second sentence of this decision of its
force. The rest holds. Without this section a reader knows something changed but not what.

## Consequences

**Positive.** The checker has a correct two-way link to recognise.

**Cost, taken knowingly.** The reference set has to be maintained alongside the checker.

## Implementation state

Serves the checker's test only.
