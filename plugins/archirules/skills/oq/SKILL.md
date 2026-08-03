---
name: oq
description: Register a new open question or resolve an existing one in the open-questions register. Use when a doubt has no answer yet, or when a decision closes one.
---

# The open-questions register

## Registering

1. **Number** — the highest plus one. Check for **duplicates and gaps** before assigning:
   ```
   grep -oE "^### OQ-[0-9]+" open-questions.md | sort | uniq -d     # duplicates
   ```
   Do not count headings to guess the next number — archived entries and duplicates will skew
   the count. Take the **maximum**, not the count.

2. **Entry header:**
   ```
   ### OQ-NN — <a question, not a topic>
   **Status:** OPEN · **Depends on / Blocks / Touches:** ...
   ```
   Add a priority only when it is high or critical. A field filled in on every routine question
   becomes noise and stops meaning anything.

3. **The body** answers three things: what we do not know, what happens if we leave it
   unresolved, and what has to be known before it can be answered.

## When to open a question

- a doubt you are tempted to settle with "let's do X for now" — **always**;
- a boundary that cannot be enforced mechanically (rule W9);
- a risk discovered while doing something else, which you are not fixing now;
- a decision deliberately deferred — recording **until when** and **on what** it depends.

If you are writing a code comment that starts with "for now", "eventually" or "to be
considered", that is an open question, not a comment.

## Closing

Change the status to `RESOLVED → <record or phase>, <date>` and **state the answer** — a bare
link forces the reader through an entire decision record.

Three special cases:

- **The answer was reversed** — say that the first one was different and why. That matters more
  than swapping the link.
- **The question stopped existing** — say so plainly instead of dressing it up as a resolution.
- **Partially closed** — leave it open and move the body onto what remains.
