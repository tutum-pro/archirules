---
name: adr
description: Write, supersede or amend an architecture decision record (ADR). Use when an architectural decision has been made, reversed, or discovered to be undocumented.
---

# Decision records

## A new record

1. **Number** — the highest existing one plus one, zero-padded (`ADR-0014`). Read the
   directory, not your memory.
2. **Header** — `Status`, `Resolves` (question numbers), `Unblocks` (phases), `Related`, and
   `Supersedes` when reversing an earlier decision.
3. Fill in `templates/<language>/ADR.md`.

## Mandatory sections

**"Considered and rejected"** — every rejected option with its reason. Without it somebody
proposes the same option again and nobody can say why it fell (rule P3).

**"Costs, knowingly accepted"** — in the indicative. Not "risks", not "to consider". If you
cannot name a single cost, **the decision is not yet understood** — go back to analysis instead
of writing a record.

**"Implementation status"** — what is built, what is verified and **by what**. Not "it works",
but the result.

## Superseding

When a decision is reversed:

1. A new record with `Supersedes: ADR-NNNN`.
2. The old record gets a status **at the top**: `SUPERSEDED by ADR-MMMM`, with the date and the
   scope — often only part of it is superseded. **It stays in the register**: it documents the
   reasoning that led to the change.
3. The row in `README.md` is updated in both places.
4. If the record is written late, **say so in it**, including the period during which the
   register stated something untrue (rule P7).

## After writing

- add the row to the table in `README.md` — a record outside the index does not exist;
- close the open questions it resolves, pointing at this record;
- if the decision binds **every** piece of work, add it to the binding requirements.
