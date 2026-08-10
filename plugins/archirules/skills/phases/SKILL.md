---
name: phases
description: Manage the phase register — open a phase with its acceptance criterion, or close one with evidence. Use before starting a work phase and when reporting it complete.
---

# The phase register

**`--help`** — if `$ARGUMENTS` is `--help`, run
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/help.py phases`, show its output, and stop there.

## Usage

```
/archirules:phases [--help]
```

Opens a phase with its acceptance criterion, or closes one with evidence.

**Needs from you:** for opening, a criterion that can be settled without discussion — "an
instance survives a restart and resumes", not "do persistence". For closing, the command output
that shows the criterion met.

**Will not:** close a phase because the code exists. Closing needs evidence, two consecutive
runs of the suite, and a prose section saying what was built, what was deliberately left out,
and under which question it is recorded.

A criterion written after the work is always met, which is why it is written before.

## Opening a phase — **before** the work

A row in the table: identifier, name, status `☐`, **acceptance criterion**.

The criterion has to be **checkable and non-trivial**:

| bad | good |
|---|---|
| "do persistence" | "**an instance survives a restart and resumes**" |
| "add validation" | "`@annuity` in a guard is a **compile error**" |
| "handle retries" | "**a step delivered twice produces one effect**" |

A criterion written afterwards is always met — which is why P5 requires it up front.

## The hard gate

For an expensive approach, write down **the condition for abandoning it** before you start.
Phrase it so it can be settled without discussion: *"if phases B1–B5 do not fit in a week of
work, option C was wrong"*.

## Closing a phase

**Do not close it because the code exists.** Closing requires:

1. **Evidence** that the acceptance criterion is met — a command and its output, not a claim.
2. **Two consecutive runs** of the tests (rule W7).
3. **A prose section** under the table: what was built, **what design decisions** were taken
   along the way, **what was deliberately left out** and under which question it is recorded.
4. A note on what surfaced incidentally — especially defects found in your own earlier work.
   That is the most valuable part of the register and the only place it survives.

## When a phase is "nearly" done

Status `◐` and **a list of what is missing**. Do not round up: a phase closed early takes the
whole point out of the gate.

Before reporting a phase complete, **check the criterion literally**. "Compile error" means a
failing build, not a refusal at run time — those are not the same thing, and the difference is
only visible if you actually run it.
