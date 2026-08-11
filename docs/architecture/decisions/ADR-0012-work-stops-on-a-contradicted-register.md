# ADR-0012 — Work stops when the register contradicts itself or a question says it blocks that work

**Status:** Accepted (decided by Robert Sternal, 2026-08-11)
**Unblocks:** P13 · **Related:** [ADR-0006](ADR-0006-checker-speaks-the-methods-vocabulary.md)

## Context

The checkers report. Nothing acts on the report. A register that contradicts itself, or a phase
whose blocking question has no answer, is today a message on a terminal that a person may read
and proceed anyway — and usually will, because the work is what they came to do.

That is the shape of a rule which everybody can see and nobody has to obey. This record decides
that the two conditions the checkers already detect **stop the work** rather than describe it.

Two things the method does not currently have, and this record has to supply:

- **"Inconsistency" needs a definition that is not a judgement.** It is a non-zero exit from
  `conform.py` or `consistency.py`. Nothing else counts; in particular a `~ skipped` line is not
  a finding and does not stop anything.
- **"Critical path" does not exist in this method at all.** There is no such concept in
  `RULES.md`, in any skill or in any template. It is defined here, narrowly, as: *an open
  question whose `Blocks:` field names the phase the work belongs to.* Nothing wider.

## Decision

### 1. Two conditions stop work, and only two

**A.** `conform.py` or `consistency.py` exits non-zero on the project's registers.

**B.** An open question declares `Blocks: <phase>` for the phase the work belongs to.

Anything else — an open question that blocks nothing, a question blocking a different phase, a
skipped check, a stale traceability view — does **not** stop anything.

### 2. It triggers at the boundaries of work, not continuously

At **opening** a phase and at **closing** one, and at whatever gate the project chooses to wire
into its own CI or pre-commit. Not on every edit. The method governs decisions, not keystrokes,
and a check that runs on every save gets disabled within a week.

### 3. "Stops" means two different strengths, and they are labelled

- **The skills refuse.** `/archirules:phases` will not open or close a phase under either
  condition. This is an instruction a model reads, so it is a refusal, not a prevention — the
  same residue as `--help` routing, and it is called that here rather than dressed up.
- **A script exits non-zero**, so a project can make it binding by putting it in CI or a
  pre-commit hook **it controls**. Real prevention exists exactly where a project wires it in
  and nowhere else.

Claiming that a plugin of Markdown files and Python scripts *prevents* somebody from writing
code would be the plugin's own worst failure mode: a rule that pretends to be enforced. The
distinction is stated in the skill, in the script's output, and here.

### 4. Enforcement does not ship before the override exists

This is a hard condition on the phase, not a preference. A gate that stops work and offers no
sanctioned way past it gets removed, or routed around, by the first person it stops unfairly —
and what gets removed is the whole mechanism, not the one case that was wrong.

The override is deliberately not designed here. It is
[OQ-09](../open-questions.md#oq-09--how-does-somebody-with-authority-sanction-breaking-the-consistency-rule)
and
[OQ-10](../open-questions.md#oq-10--how-is-the-list-of-people-who-may-sanction-it-defined-and-protected),
both declaring that they block P13.

## Considered and rejected

### 1. Stop on every open question, not only those declaring `Blocks:`

The literal reading of "open questions in the critical path", and much simpler to implement:
any `OPEN` entry halts work.

**Rejected, and this is the most important rejection here.** Registering a doubt would then
carry a cost — it would stop the registrant's own work. The predictable adaptation is not better
questions; it is silence, and the doubt gets settled by whoever touches the files first. That is
precisely the failure rule P4 exists to prevent, so the wide reading would use the method to
defeat the method.

The narrow trigger keeps registering a question free and makes **declaring that it blocks a
phase** the deliberate act. That declaration is already a documented field and already checked.

### 2. Warn, as now, and rely on discipline

The status quo: both checkers print findings and exit non-zero, and a person decides. Rejected
because it is what the project already does and the contradiction survives it. A finding that
everybody sees and nobody must act on is how a register rots while looking maintained.

### 3. Enforce it in a git hook the plugin installs

`pre-commit` refusing the commit. Rejected on the same ground as the traceability decision:
`.git/hooks` is not versioned, so every clone would have to install it and most would not. A
rule enforced on some machines is one nobody can rely on. The plugin supplies the exit code; the
project decides where to bind it.

### 4. Let the skills refuse and call that prevention

Cheapest, and it would read well. Rejected: a `SKILL.md` instruction is followed by a model, not
by a mechanism, and calling that "the framework prevents it" would be a claim the plugin cannot
support. Both strengths ship, each labelled for what it is.

### 5. Ship the block now and design the override later

Faster, and the override is a separate concern. Rejected: a gate with no sanctioned way past it
is removed the first time it is wrong, and the removal takes the mechanism with it. Sequencing
the override first costs a delay; shipping it second costs the feature.

## Consequences

**Positive.** The two conditions the checkers already detect acquire teeth at the two moments
where they matter. A phase cannot be opened on a register that contradicts itself, nor closed
while a question that declares it blocks that phase is unanswered. "Blocked" stops being a
status somebody wrote and becomes a state with an effect.

**Costs, knowingly accepted.**

- **It creates a reason not to declare a blocker.** Narrowing the trigger moves the disincentive
  from *registering a question* to *saying that it blocks a phase*, which is better but not free.
  Somebody under deadline pressure can leave the field empty, and nothing detects a blocker that
  was never written down.
- **A forgotten `Blocks:` gives no protection; a stale one stops work for nothing.** The field is
  maintained by hand, so both errors are available and neither is mechanically detectable.
- **Prevention is real only where the project wires it in.** Elsewhere this is a refusal that a
  determined person walks around in ten seconds, and a contributor who does not have the plugin
  installed is not affected at all.
- **A structural defect anywhere blocks work everywhere.** Condition A is repository-wide: a
  missing section in an unrelated decision record stops an unrelated phase. That is the price of
  a definition that is not a judgement, and the alternative — deciding which findings are
  serious — is a judgement call inside a gate, which is worse.
- **The escape hatch will be used, including when it should not be.** That is what an escape
  hatch is. What OQ-09 has to get right is that using it leaves a record.

## Implementation status

**Not implemented, deliberately.** This record decides the rule; no code, skill or gate
implements it yet. Phase P13 carries the work and is **blocked** by OQ-09 and OQ-10, per
decision 4 — the override has to be designed before the block ships, or the block does not
survive contact with the first person it stops unfairly.

What exists today is unchanged: both checkers report and exit non-zero, and nothing acts on it.
