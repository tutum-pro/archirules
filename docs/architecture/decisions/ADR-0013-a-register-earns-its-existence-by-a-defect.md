# ADR-0013 — A new register earns its existence by a defect its absence caused

**Status:** Accepted (decided by Robert Sternal, 2026-08-11)
**Related:** [ADR-0003](ADR-0003-casebook-apart-from-rules.md)

## Context

Two registers were proposed: **CHR** (change requests) and **Errors**, both described by their
proposer as keeping a history of facts with **no direct effect on the implementation work**, with
rules and pipelines between them and the existing ADR and OQ registers to be designed afterwards.

The proposal is reasonable on its face — most methodologies have both — and it is worth stating
why this one does not, because the same proposal will arrive again.

**The four registers are not places for facts. Each answers a different question about
epistemic status:** ADR — settled; OQ — not yet known; the phase register — progress against a
criterion agreed in advance; the verification register — demonstrated as opposed to claimed.

CHR and Errors are not epistemic states. They are **event streams**: somebody asked, something
broke. Placing event streams inside a set of state registers produces a structure where "which
register does this belong in" has no answer derivable from the definitions — only a judgement,
made under time pressure, and answered by whichever file is closer to hand.

The proposal's own wording is the sharpest argument against it. **A register with no effect is a
log.** Every existing register has teeth: an ADR produces binding requirements, an OQ blocks a
phase, a phase gates its own closure, the verification register decides what may be claimed. And
this method already states what becomes of a register nobody's work depends on — *an unmaintained
register is worse than none, because it looks current*. A register with no effect is the first
candidate for neglect, because nothing breaks when it is neglected.

## Decision

### 1. No CHR register. Its content already has three homes

A change request that **lands** is the `## Context` of the decision record it forced — which is
what that section is for: *what forced the decision; facts, not preferences*. One that was
seriously weighed and fell is a rejected alternative in the same record. One still undecided is
an open question. The method deliberately records **the decision, not the request**.

A change-request register additionally presumes a requirements baseline, that deviations from it
are separately trackable, and that somebody approves them. This method has none of the three, and
knows no roles at all — there is no mention of a lead, an architect or a project manager anywhere
in `RULES.md`, in either language. That is a property, not an omission: a decision is a decision
whoever wrote it. CHR would import stage-gate governance through the side door, which is not
adding a register but grafting on a different methodology.

### 2. No Errors register. Split the case and both halves have a home

An error that **changes nothing** is work, and belongs in the issue tracker every project already
has. Duplicating it here would be duplicated state — the thing `consistency.py` exists to police,
and something this register has already refused twice: commit identifiers copied into a register
([ADR-0010](ADR-0010-traceability-derived-from-git-trailers.md)), and the blocker table
(OQ-06). Keeping a *different subset* is worse: the rule for what goes where becomes a judgement.

An error that **invalidates a claim or a rule** is evidence, and the verification register already
carries it under a dated correction heading. The precedent is stronger still: the casebook **is**
the error register of this method, and its design rule
([ADR-0003](ADR-0003-casebook-apart-from-rules.md)) is that incidents are kept apart from rules
and **referenced, not inlined**. The question has been answered here once already.

### 3. One question register stays one

The proposer was right about this and the reason is worth recording: an OQ number is a public
reference, so splitting question-space across registers makes every reference ambiguous.

But an OQ must not become a hub referencing the other two. **An error is not a doubt — it is a
fact. A change request is not a doubt — it is an input.** Routing all three through one numbering
conflates three epistemic states, and keeping them apart is where this method's value comes from.

### 4. The test any future register must pass

**Name the defect its absence caused.** Not "it would be tidier", not symmetry with another
methodology: an event that happened and cannot be reconstructed today.

The precedent is already in the rules. The verification register is not created on day one; it is
started **at the first defect caused by an unverified claim**, at which point its necessity is not
in question. That is the standard, generalised.

### 5. This is a binding requirement here, and deliberately **not** a numbered rule in `RULES.md`

It is added to the binding requirements of this register, so it governs every future proposal to
grow the method.

It is **not** added to `RULES.md` as a numbered rule, because that file's stated principle is that
every rule exists because its absence broke something specific — and no incident produced this
one. Adding it would be the first rule in the set with no failure behind it, which would damage
the claim the whole file rests on. If a project ever adds a register that rots and costs
something, that is the incident, and then it becomes a rule.

## Considered and rejected

### 1. Add both registers as proposed

Rejected on the grounds above: they are event streams, not states; by their proposer's own
description they change nothing; and the content already has homes.

There is also a cost that is easy to underestimate. Four registers make six pairs and this method
mechanises five relations between them. Bringing those five to a state where they can be trusted
took forty-one self-test cases — and one of them still turned out to be **incapable of firing at
all** (casebook C-11). Six registers make fifteen pairs. Without a matching increase in
mechanism, the new relations would be conventions: rules that pretend to be enforced.

### 2. Add Errors only, as the more defensible of the two

Tempting, because defects are concrete and change requests are administrative. Rejected: it is
the half with the strongest existing coverage. Between the issue tracker, the verification
register's corrections and the casebook, an error has three homes already, and a fourth would
divide them rather than complete them.

### 3. Make OQ the hub that references CHR and Errors

The proposal's own suggested compromise, and the least invasive version. Rejected for the reason
in decision 3: it keeps one numbering, which is right, and uses it to conflate three epistemic
states, which is the thing worth not doing.

### 4. Write the rule into `RULES.md` now

It reads like a method-level rule and it would reach every user of the plugin, which a binding
requirement in this repository does not. Rejected for now: no incident produced it, and a rule
without one contradicts the sentence that makes `RULES.md` worth trusting. Recorded here instead,
where reasoning belongs, with the promotion path stated.

## Consequences

**Positive.** The next proposal to add a register — and there will be one — meets a stated test
rather than a debate. The reasoning survives this conversation instead of having to be
reconstructed. The four registers keep the property that makes them checkable: each answers one
question about epistemic status, and nothing in the set is a log.

**Costs, knowingly accepted.**

- **A real gap stays open.** There is no home for an external fact that constrains the project
  and is neither a decision nor a doubt — a vendor deprecation, a regulatory change. Today it
  exists only as the `Context` of whichever record happened to be written, and if none was, it
  exists nowhere. Carried as
  [OQ-11](../open-questions.md#oq-11--where-does-an-external-fact-live-when-it-is-neither-a-decision-nor-a-doubt).
- **Accountability towards a client is not served, and will not be.** If the need behind CHR is
  "who asked for what, and when", that is contract administration rather than architecture. This
  method does not do it, and pointing at the right tool is more honest than growing the method to
  pretend otherwise.
- **The test is a judgement, not a check.** "Name the defect its absence caused" cannot be
  mechanised, so it is a review convention — the category rule W9 says must be named explicitly
  rather than left to look enforced. It is named here and in the binding requirements.
- **It can be wrong.** A defect that has not happened yet is not a defect that will not happen,
  and this rule refuses on the strength of evidence not yet gathered. The cost of being wrong is
  a register created later than it should have been, which is recoverable; the cost of the
  opposite error is a set of registers nobody maintains, which is not.

## Implementation status

Done, as far as it goes: the binding requirement is in
[the index](../README.md#binding-requirements), the gap is registered as OQ-11, and no register
was created.

Nothing is mechanised, and nothing can be. A checker cannot ask whether a defect happened.
