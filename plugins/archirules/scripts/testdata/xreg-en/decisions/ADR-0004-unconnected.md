# ADR-0004 — Record with no links

**Status:** Accepted

## Decision

A record that supersedes nothing and that nothing supersedes. The set has to hold one,
or a checker demanding a supersession scope from **every** record would pass this test
without anyone noticing.

It is also the record the open questions point at, because a `Touches` entry aimed at a
current record is the correct case. The self-test aims it at a superseded one instead,
to prove the checker can tell the difference.

## Consequences

**Positive.** A separate record to inject a contradicting resolution into during the
test, without disturbing the supersession chain.

**Cost, taken knowingly.** One more file in the set.

## Implementation state

Serves the checker's test only.
