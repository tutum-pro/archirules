# Open questions

### OQ-01 — Is the blocker table kept together with the phase table
**Status:** OPEN · **Touches:** [ADR-0004](decisions/ADR-0004-unconnected.md) · **Blocks:** X2

An open question declaring that it blocks a phase. The checker looks at two things at
once: that phase X2 carries status `⛔`, and that the blocker table names this question
under X2. The two records drifting apart is a defect neither register can see in itself.

It touches a record that is **current**, on purpose. Pointing it at a superseded one is
a defect, and the self-test makes that edit to prove the checker notices.

### OQ-02 — Does the variant abandoned in ADR-0002 come back
**Status:** RESOLVED → [ADR-0003](decisions/ADR-0003-modification.md), 2026-08-11 — it does not

A closed question, and it declares no blocker. That combination is what the checker
requires: a question that has an answer and still says what it holds up leaves a phase
waiting for nothing. The self-test adds the field back to prove the check fires.
