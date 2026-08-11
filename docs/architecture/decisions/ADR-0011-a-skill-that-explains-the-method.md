# ADR-0011 — The method explains itself in a skill, and every reference in it is checked

**Status:** Accepted (decided by Robert Sternal, 2026-08-11)
**Unblocks:** P12 · **Related:** [ADR-0008](ADR-0008-help-comes-from-a-file-not-from-memory.md)

## Context

Somebody meeting this plugin has `/help`, which lists eight skills with one-line descriptions,
and `--help` on each, which says what that skill needs from them. Neither answers the question
people actually ask first: **what is this, and why would I run my project this way.**

The `README.md` answers it, but a reader inside a session does not have the repository open, and
the plugin ships without it in front of anyone.

There is a specific hazard in writing that text. An explanation of a method is the natural
habitat of the sentence that sounds true and is not: a claimed benefit nobody measured, a rule
that does not exist, a casebook case invented because it would illustrate the point well. The
text describes the method **to somebody who cannot yet recognise a wrong claim about it** — which
is exactly the reader least able to catch it.

### Relation to ADR-0008

That record rejected "a single `/archirules:help` skill". The rejection stands and this does not
reverse it: what was rejected was a skill **listing the other skills**, on the grounds that
`/help` already does that and it would not answer "what does this one need from me". This skill
answers a third question — what the method is — which neither `/help` nor `--help` addresses.
The name is the same and the content is not. A note has been added inside ADR-0008 so a reader
arriving there is not left with a rejection that appears to forbid what now exists (rule P7).

## Decision

### 1. A skill that explains the method, not the skills

`/archirules:help` states the problem the method addresses, what it consists of, the four ideas
that make it more than paperwork, what is mechanised and what is not, what it costs, what it
does not do, and how much evidence there actually is.

### 2. Every reference in it is verified; the prose is not

The self-test requires that every casebook case, rule identifier, script and skill named in the
text **exists**. A `C-99` that reads plausibly, a rule `P9` that was never written, a
`conformance.py` — all fail the run.

This does not check that the text is true. It checks that it is not made of things that are not
there, which is the failure mode specific to this kind of writing and the only part of it that
can be checked at all.

### 3. It names no entry from this repository's own registers

`ADR-NNNN` and `OQ-NN` references are a **failure**, enforced. A reader of the plugin does not
have this repository's registers, so a rule that points at one cannot be used without knowing
somebody else's project history — which is a binding requirement here, and the reason the
casebook was split out of the rules in the first place.

The older skills do not hold to this yet, and that gap is registered rather than quietly
tolerated: [OQ-08](../open-questions.md#oq-08--skills-cite-this-repositorys-own-registers-which-a-reader-of-the-plugin-cannot-resolve).

### 4. The text states its own weakest point

The method has been applied end to end to exactly one project: this one. The text says so, in
those words, and points at the hard gate that has not been passed — somebody who did not
co-create it using it without asking its author how.

An explanation that omits this would be the most consequential untrue thing in the plugin.
Including it is not modesty; it is the same rule that requires a decision record to name its
costs.

## Considered and rejected

### 1. Point at `README.md` and write nothing new

No duplication, nothing to keep in sync. Rejected: the reader is inside a session, and "go read
the repository" is the answer that ends the conversation rather than answering it. The overlap
is real and is accepted as a cost below.

### 2. A short overview — three paragraphs and a link

Cheap, low maintenance, no context cost. Rejected because it would answer the question at the
level the question is usually asked and not at the level it is usually meant. Someone asking
what this is wants to know whether it is worth the trouble, and that needs the costs and the
limits, which is most of the length.

### 3. A banned-words check against marketing register

"Seamless", "robust", "best practice", "empowers". Mechanically trivial. Rejected: it polices
vocabulary rather than truthfulness, and a text can be entirely free of those words and still
claim things nobody measured. Worse, passing it would create the impression that the prose had
been checked. The reference check makes a narrow claim and makes it precisely; this one would
make a broad claim it cannot support.

### 4. Generate the text from `RULES.md`

The rules are already written and already carry their reasons. Rejected: the rules are written
for somebody applying them, and this text is for somebody deciding whether to. Generation would
also flatten the part that matters most — what the method does **not** do — which appears in the
rules as one section and needs to be a third of an explanation.

## Consequences

**Positive.** The first question anybody asks has an answer inside the session, at the depth the
question is actually meant. A reference that does not exist cannot survive a release, which
removes the most likely kind of error in this specific text.

**Costs, knowingly accepted.**

- **The claims worth most are the ones nothing checks.** The costs, the limits and the state of
  the evidence are prose. The gate verifies that references resolve, not that sentences are
  true, and the difference is where an untrue explanation would actually live.
- **It overlaps `README.md` and `RULES.md`.** Three documents now describe the method to
  different audiences, and they can drift. Nothing detects a drift in meaning; only invented
  references are caught.
- **Context cost on every invocation.** This is a long skill, loaded in full when it runs.
- **The register-reference rule holds for this skill alone.** Applying it to the older skills
  would turn the self-test red today, so it is scoped here and the gap is carried as an open
  question rather than fixed silently or ignored.

## Implementation status

Done. `skills/help/`, and a self-test case shown to fail in six shapes: an invented casebook
case, an invented rule identifier, a renamed script, a skill that does not exist, a reference to
this repository's own registers, and the casebook removed so the check cannot run — the last
prints the reason rather than passing, which is the C-11 lesson applied again.
