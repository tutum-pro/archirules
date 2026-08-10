# Open questions

### OQ-01 — Is the blocker table kept together with the phase table
**Status:** OPEN · **Touches:** [ADR-0001](decisions/ADR-0001-base.md) · **Blocks:** X2

An open question declaring that it blocks a phase. The checker looks at two things at
once: that phase X2 carries status `⛔`, and that the blocker table names this question
under X2. The two records drifting apart is a defect neither register can see in itself.

### OQ-02 — Does the variant abandoned in ADR-0002 come back
**Status:** RESOLVED · **Answer:** it does not; [ADR-0003](decisions/ADR-0003-modification.md) closes it

A resolved question. It exists so the checker has something to look for in blocker
tables — a closed question still listed as a blocker holds a phase for no reason.
