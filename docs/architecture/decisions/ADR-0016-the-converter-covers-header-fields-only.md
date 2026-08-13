# ADR-0016 — The converter covers header fields, and the narrowing is the decision

**Status:** Accepted (decided by Robert Sternal, 2026-08-13)
**Related:** [ADR-0015](ADR-0015-references-are-links-and-anchors-are-checked.md)

## Context

[ADR-0015](ADR-0015-references-are-links-and-anchors-are-checked.md) decided that a reference to
a register entry is a link, and then had to admit two things it had left unguarded: nothing
checks that a reference *is* a link, and the conversion of an existing register was nobody's
job — the ten references here were converted by a throwaway script that shipped nowhere.

The plan agreed after that: ship the means first, enforce afterwards. This record is the means.

Before writing it, the references in this repository were counted by context:

| where the reference sits | plain | linked |
|---|---|---|
| header field | **0** | 32 |
| prose | **76** | 44 |
| generated traceability view | 15 | 0 |

That table decided the shape of the tool, and the interesting decision here is not that a
converter exists. **It is where it stops.**

## Decision

### 1. `relink.py` converts header fields, and nothing else

Bare `ADR-NNNN` and `OQ-NN` in a header field become links. A dry run reports and changes
nothing; `--write` applies.

### 2. Prose is out of scope, deliberately

Extending the tool to prose would mean 76 conversions in this repository alone, and the result
reads worse: a paragraph naming a record three times would carry three long links where it now
carries three short identifiers. A reference in prose is a **mention**; a reference in a header
field is **navigation**. They are different things that happen to share a spelling.

The narrowing is recorded rather than left as an oversight, and what remains unsettled is
carried as
[OQ-14](../open-questions.md#oq-14--should-a-reference-in-prose-be-a-link-too).

### 3. "Header field" is defined structurally, not by pattern

A decision record's header is what stands above its first `##` section; a question's is the line
directly under its heading. Matching `**Word:**` anywhere instead would also catch `**To
resolve:**` inside the body of a question — which is prose, and out of scope by decision 2. The
obvious pattern would have quietly widened the tool past its own decision.

### 4. The anchor rule is imported from `conform.py`, never copied

The converter builds anchors with the same `slug` the checker validates them with. Two copies of
that rule would drift, and a converter producing links its own checker rejects is worse than no
converter.

### 5. A reference whose target does not exist is left alone

`consistency.py` already reports it. Inventing a link to a missing file would turn one finding
into two, the second of them wrong.

### 6. Enforcement is not in this release

Requiring links belongs to the next major version. Shipping the requirement alongside the tool
would mean the rule arrives the same day as the means, leaving projects no window in which the
converter exists and the rule does not.

## Considered and rejected

### 1. Convert prose as well, for consistency

The tidier-sounding option, and the one the phrase "a reference is a link" literally implies.
Rejected on the measurement: 76 conversions here, and documents that read worse afterwards. A
rule whose faithful application makes the text harder to read is a rule scoped wrongly.

### 2. Link the first mention in each document, leave the rest

The version a careful writer would choose by hand, and it produces good prose. Rejected because
"the first mention" is a judgement, and a judgement inside a gate is what this method refuses —
it cannot be checked, so enforcing it later would be impossible and the tool would be applying a
rule nothing could verify.

### 3. Recognise header fields by matching `**Word:**`

Three lines instead of a structural walk. Rejected: it matches `**To resolve:**` and any other
emphasised label in a body, so the tool would edit prose while its own record said it did not.
This was caught before it shipped, by asking what the pattern matches rather than what it was
meant to match.

### 4. Ship the converter and the enforcement together

One release, one migration, done. Rejected: the requirement would land the same day as the means,
so every project would meet the rule and the tool at once, under time pressure. A window in which
the tool exists and the rule does not costs one release and removes that.

### 5. Reimplement the anchor rule inside the converter

Would avoid importing a checker into a tool. Rejected for the reason recorded when the vocabulary
assertion was written: two copies of one rule are two rules, and they drift.

## Consequences

**Positive.** The conversion this repository performed by hand is now something any project can
run, which is what makes the later enforcement fair rather than punitive. The scope is written
down, so the tool cannot grow into a reformatter of whole documents by increments.

**Costs, knowingly accepted.**

- **Prose stays mixed**, 76 bare against 44 linked, and a reader sees an inconsistency the
  method has decided not to fix. That is visibly untidy and is the price of not putting a
  judgement inside a tool.
- **The tool has nothing to do in this repository.** Its only proof is fixtures and a
  reconstructed pre-2.0.0 register; it has never run on somebody else's real one.
- **`--write` is a bulk edit.** It changes many files at once, and the only thing standing
  between a mistake and a committed register is the reader looking at the diff. The dry run is
  the default for that reason.
- **The rule is still unenforced.** Until the next major release, a register full of bare header
  fields passes everything. This record narrows the gap and does not close it.

## Implementation status

Done. `scripts/relink.py`, fifteen self-test cases across both languages, and the register's own
same-file anchors normalised to the form the tool produces, so the tool is the source of truth
rather than a second convention.

Shown to fail under two mutations. A converter that does nothing fails four cases. The naive
guard that was actually written first — a lookbehind for `[`, which misses the reference inside a
link's own target path and double-wraps the register — is caught by the **idempotency** case: the
second run finds work again because the first run's output is malformed. That case exists for
exactly that bug, and it earned its place by catching it.
