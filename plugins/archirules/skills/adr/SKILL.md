---
name: adr
description: Write, supersede or amend an architecture decision record (ADR). Use when an architectural decision has been made, reversed, or discovered to be undocumented.
---

# Decision records

**`--help`** — if `$ARGUMENTS` is `--help`, run
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/help.py adr`, show its output, and stop there.

## Usage

```
/archirules:adr [--help]
```

Writes a new decision record, supersedes an existing one, or amends one written late.

**Needs from you:** the decision itself, the alternatives that were genuinely weighed, and the
reason each fell. If you cannot name one cost of the decision, the skill will say so rather than
write the record — an unnamed cost means the decision is not yet understood.

**Will not:** invent rejected alternatives to fill the template, or decide anything for you. It
writes down a decision that has been made.

**Reversing a decision** touches two files: the new record gets `Supersedes:`, the old one gets a
status line naming the date and **what stopped holding**. A bare pointer to the successor is a
finding in `conform.py`.

### Examples

```
/archirules:adr
/archirules:adr we call the payment provider directly instead of queueing
/archirules:adr supersede the storage decision — it is Postgres now, the durability part stands
```

The first form asks you what was decided. The others start from what you typed, and you will
still be asked for the rejected alternatives and the costs, because a record without them is not
a decision record.

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
2. The old record gets a status **at the top**, replacing the one it had:

   ```
   **Status:** SUPERSEDED by ADR-MMMM, <date> — <what stopped holding>
   ```

   The scope is not optional and not a separate section. Often only part of a decision is
   superseded, so "which part" is the point, and it belongs in the field that would otherwise
   still say the old thing — a correction written underneath one is not a correction (rule P7,
   case C-04). `conform.py` requires it; a bare pointer to the successor is a finding.

   **It stays in the register**: it documents the reasoning that led to the change.
3. The row in `README.md` is updated in both places.
4. If the record is written late, **say so in it**, including the period during which the
   register stated something untrue (rule P7).

## After writing

- add the row to the table in `README.md` — a record outside the index does not exist;
- close the open questions it resolves, pointing at this record;
- if the decision binds **every** piece of work, add it to the binding requirements.
