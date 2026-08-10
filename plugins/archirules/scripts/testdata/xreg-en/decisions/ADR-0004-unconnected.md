# ADR-0004 — Record with no links

**Status:** Accepted

## Decision

A record that modifies nothing and that nothing modifies. The set has to hold one, or a
checker demanding a "What changed" section from every record would pass this test
unnoticed.

## Consequences

**Positive.** A separate record to inject a contradicting resolution into during the test.

**Cost, taken knowingly.** One more file in the set.

## Implementation state

Serves the checker's test only.
