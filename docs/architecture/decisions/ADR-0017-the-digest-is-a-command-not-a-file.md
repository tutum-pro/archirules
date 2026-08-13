# ADR-0017 — The digest is a command, not a file

**Status:** Accepted (decided by Robert Sternal, 2026-08-13)
**Related:** [ADR-0010](ADR-0010-traceability-derived-from-git-trailers.md)

## Context

Reading these registers costs about **48 000 tokens**, and every question anybody asks an
assistant about this project is priced against that number. The concern was raised as one about
context economy: if answering anything requires reading everything, the arrangement is wasteful.

Half of that is true, and measuring which half changed what got built.

**Answering a question does not require reading the registers.** In practice the questions in
this project have been answered by searching — a grep over headings costs a few hundred tokens
against the 48 000 the whole set holds. Exactly one operation reads everything, and it does so by
definition: the audit.

**What is expensive is finding out what exists.** The decisions already have an index — the table
in `README.md`, 1 400 tokens for all sixteen. The other three registers have none, so the
question "what is open" costs 8 000 tokens to answer from a document whose answer is fifteen
lines long.

There is also a finding that no index would fix, recorded separately as
[OQ-15](../open-questions.md#oq-15--what-tells-a-record-that-carries-its-reasoning-from-one-that-is-merely-long):
the records written most recently average 2 155 tokens against 762 for the earliest five, which
carry the same required sections. The largest cost here is prose, not structure.

## Decision

### 1. A digest exists, and it prints

`digest.py` writes one line per entry across all four registers — identifier, state, subject —
and nothing else. **1 075 tokens** where reading the registers costs 48 000.

### 2. It is a command, and deliberately not a generated file

This is the decision worth recording, because a file is the obvious shape and it is wrong here.

A file has to be regenerated, can be edited by hand, needs a check to prove it was not, and joins
the set of artefacts a reader has to be told about. **A command cannot go stale**: it reads the
registers at the moment it is asked, so there is no staleness to detect and no check to write.

The generated traceability view is a file for the opposite reason, and the two are not
inconsistent: it exists to be read **by a person** auditing the project inside the register,
months later. The digest exists to spare **a machine** from reading everything to learn what
exists. Different readers, different artefacts.

This also settles the question [ADR-0013](ADR-0013-a-register-earns-its-existence-by-a-defect.md)
would otherwise raise. A command adds no document to `docs/architecture/`, so the bar for a new
register never applies to it.

### 3. What it must never do is leave something out

A digest that quietly omits an entry is worse than none, because the reader believes they have
seen everything. The self-test therefore does coverage accounting — how many entries were
printed against how many the register holds — rather than checking that it runs.

### 4. It takes no position on the wording of a register

Every status is reproduced as written, so there is no marker table and nothing to drift. The one
exception is the verification register's labels, which have drifted into six spellings of three
states; the digest groups them by the state each asserts, because reproducing them faithfully
produces an unreadable line and dignifies the drift.

## Considered and rejected

### 1. A generated `DIGEST.md` in the register

The obvious shape, greppable, visible on the forge to a reader who cannot run anything. Rejected:
it is a second copy of what the registers already say, which goes stale between regenerations and
needs its own check to prove it has not. The traceability view pays that price because a human
auditor needs to see it in place; the digest's reader is a machine that can run a command.

### 2. Retrieval over embeddings — a vector index, in the shape of the usual frameworks

Rejected on three grounds, the last decisive. The corpus is 174 KB in one repository, where an
exact search is instant and free; vector search earns its keep at a scale this is nowhere near.
An index is duplicated state that goes stale, which this register has refused three times
already. And retrieval by similarity is **approximate**: it returns what is probably relevant. In
a method whose central rule is to refuse rather than guess, a layer that silently returns an
incomplete subset produces an answer that looks complete and is not — the worst failure mode this
project has a name for.

There is a case where indexing does earn its place, and it is already registered as OQ-01:
queries **across** projects, which no local search can answer cheaply. Its resolution criterion is
three projects using the method. Until then, this is the wrong tool for a problem that does not
exist yet.

### 3. Shorten the records instead, and add nothing

The largest saving available — 23 700 of the 27 500 tokens in `decisions/` sit in eleven records.
Not rejected, deferred: it is a question about writing discipline with a specific failure mode,
since the first thing a shortening pass cuts is the rejected alternatives and the costs. Carried
as [OQ-15](../open-questions.md#oq-15--what-tells-a-record-that-carries-its-reasoning-from-one-that-is-merely-long)
with an experiment that settles it.

### 4. Nothing, on the grounds that grep already works

Defensible, and it is what the measurement showed for most questions. Rejected for the narrow
case grep does not serve: **learning what exists at all**. Searching finds what you can name, and
somebody who does not yet know that OQ-12 exists cannot search for it.

## Consequences

**Positive.** The question "what is in these registers" costs 1 075 tokens instead of 48 000, and
the answer cannot be out of date. Nothing was added to the register, so nothing new can rot.

**Costs, knowingly accepted.**

- **It is invisible to a reader browsing the forge.** Somebody reading this repository on the web
  cannot run it, and for them the registers remain what they were. That is the price of the
  choice in decision 2, and the index in `README.md` still serves them for decisions.
- **A summary invites being trusted as complete.** It lists subjects, not content; a decision's
  reasoning, costs and rejected alternatives are exactly what it leaves out. Coverage accounting
  guarantees no entry is missing, and guarantees nothing about whether the one line is enough.
- **It parses four registers with regular expressions**, so a register formatted unusually may
  yield less than it holds. The coverage check catches a **missing** entry; it cannot catch a
  subject line read badly.
- **The largest saving remains untaken.** This addresses the index, not the prose, and the prose
  is where 23 700 tokens sit.

## Implementation status

Done. `scripts/digest.py`, six self-test cases across both languages.

Shown to fail under two mutations. A digest that silently drops the last entry of each register
reports `0/1 ADR, 0/1 OQ` and turns four cases red — that is the case this decision exists for.
A digest that does not import fails the same four, and the two cases that assert a refusal
survive both, which is why they are separate.
