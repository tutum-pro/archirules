# ADR-0015 — A reference to a register entry is a link, and the anchor is checked

**Status:** Accepted (decided by Robert Sternal, 2026-08-12)
**Resolves:** [OQ-13](../open-questions.md#oq-13--should-a-reference-to-a-question-be-a-link-when-nothing-checks-that-a-link-still-lands) · **Related:** [ADR-0007](ADR-0007-explicit-version-as-the-migration-anchor.md)

## Context

References between the registers were written three ways at once, and the split fell exactly
where the authorship changed rather than where anyone decided anything.

[OQ-13](../open-questions.md#oq-13--should-a-reference-to-a-question-be-a-link-when-nothing-checks-that-a-link-still-lands)
held that the answer depended on one fact nobody had established: **can a link's anchor be
verified?** A decision record is its own file, so a link to it either resolves or does not. A
question is a heading inside a shared file, so a link to it is built from the wording of that
heading — rename the question and the link silently lands at the top of the document instead.

The question was deliberately left open with two opposite answers available: if anchors can be
checked cheaply, link everything; if they cannot, **never link a question at all**, because a
bare `OQ-02` cannot rot.

So it was measured rather than argued.

## The measurement

A prototype implementing the renderers' anchor rule — lowercase, drop anything that is not a
letter, digit, space, hyphen or underscore, spaces become hyphens — was run over every link
carrying an anchor in this repository:

| | |
|---|---|
| anchored links examined | **68** |
| resolved to a real heading | **66** |
| false positives | **0** |
| Polish anchors with diacritics, all resolved | **24** |
| genuine defects nobody knew about | **2** |

The 24 Polish anchors matter most. They were written by hand, in the canonical Polish files, by
somebody not thinking about this check — the strongest available test that the rule is right and
not merely fitted to English.

The two defects were `open-questions.md#oq-01` in the test fixtures: an abbreviated anchor that
renders as a link, resolves to the file, and lands nowhere. Nothing had ever reported them.

The check was then shown to catch the failure that actually happened here: a question's heading
was reworded during this work and two links to it had to be repaired by hand, with both checkers
green throughout. With the anchor check in place, that rename is reported.

## Decision

### 1. A reference to a register entry is a link, in every direction and every field

`Resolves:`, `Related:`, `Depends on:`, `Touches:`, `Supersedes:` and prose alike. The ten bare
references in this repository were converted as part of this record.

### 2. `conform.py` verifies the anchor, not only the file

A link that resolves to the right document and to no heading inside it is a finding. This is the
half that rots in silence, and it is now the half that is checked.

### 3. An example link is not a link

Text between backticks, and anything inside a fenced code block, is excluded before links are
extracted. The checker previously read an example written in backticks as a real link and
reported a document as broken for showing what a link looks like — which it did, in this
register, while OQ-13 was being written.

### 4. The generated traceability view keeps bare identifiers

There, an identifier is the **subject** of its row, as in a table of contents, not a reference
inside prose. And phases have no heading to anchor to at all, so linking two of the three kinds
would be less consistent than linking none.

### 5. The templates say so

They previously prescribed plain text in every field, which is what the first five decision
records here correctly followed and the nine later ones ignored. The templates now show the
link form.

## Considered and rejected

### 1. Never link a question, in either direction

The alternative OQ-13 held open, and it had a real argument: a number is already a public
reference, and `OQ-02` written plainly cannot break. Rejected because the measurement removed its
premise — anchors are checkable, with no false positives across 68 links and two languages. Had
the numbers come out differently this is the decision that would have been written.

### 2. Leave the checker as it was, verifying files only

No new code, no new failure mode, and links keep rendering. Rejected: it makes the register look
navigable while half of every anchored link is unverified. Two dead links had already survived
that way, in the plugin's own fixtures, for as long as they had existed.

### 3. Match anchors loosely — accept a prefix

Would have let `#oq-01` pass and spared the two fixture repairs. Rejected: `#oq-01` is precisely
the defect. A check that accepts the most common way of getting this wrong is a check that
reports the register as sound because it was written to.

### 4. Link everything and check nothing

The cheap half of the decision. Rejected for the reason that made OQ-13 hesitate in the first
place: linking without checking multiplies the number of things that can quietly stop working,
and would have made the situation worse than leaving the references bare.

## Consequences

**Positive.** Navigation works in both directions and is verified rather than assumed. The
failure that already happened here — a heading reworded, links left behind — is now reported
instead of being caught by chance. Two dead links were found and fixed on the first run.

**Costs, knowingly accepted.**

- **This is a breaking release.** A register that conformed yesterday fails today if it holds a
  dangling anchor. By the versioning rule set in
  [ADR-0007](ADR-0007-explicit-version-as-the-migration-anchor.md) that makes it a major version,
  and it ships with a migration block saying what to repair.
- **The anchor rule belongs to the renderers, not to us.** It was verified against 68 links
  including 24 with Polish diacritics, but a renderer that normalises differently would produce
  false positives. That is a claim about other people's software, and it is stated as one.
- **Duplicate headings are handled by the same rule** — `-1`, `-2` suffixes — and that part is
  implemented from the documented behaviour rather than measured, because this repository has no
  duplicate headings to measure it on.
- **Renaming a heading is now work.** Every link to it has to move. The checker names them, so
  the work is bounded, but it is no longer free.
- **Anchors are long and unpleasant to read in the source.** A reference now occupies most of a
  line where it used to occupy nine characters.
- **The rule itself is not enforced, only the anchors are.** Nothing checks that a reference *is*
  a link. A register full of bare `ADR-0004` passes every check, so decision 1 is a convention —
  the shape rule W9 names as the worst kind of rule, because nobody watches it and everybody
  assumes somebody else does. It is stated here rather than left to be discovered, and the
  reason for accepting it is below.
- **Converting an existing register is nobody's job yet.** The ten references here were converted
  by a throwaway script that ships nowhere, so this repository did something a user of the method
  cannot. The 2.0.0 migration therefore asks only for dangling anchors to be repaired and says
  plainly that conversion is optional — an instruction to convert, with no tool and no check,
  would be work handed over without means.

<!-- Added 2026-08-12, after the record was first written. The question "will the update skill
     link my references?" made both omissions obvious: the record described what was decided and
     not what was left unguarded. Rule P7 — added in place, with the date and the reason. -->

**Why the unenforced half is accepted for now.** Requiring links would be a second breaking
release in a day, forcing every existing register to convert before it could pass again — and
the tool that would do the converting does not exist. Enforcement without that tool is a rule
that punishes people for lacking something the method never gave them. What is enforced today is
the half that fails silently; the half that fails visibly, by simply not being a link, can wait
for the means to fix it.

## Implementation status

Done. `conform.py` verifies anchors and ignores example links; ten bare references in this
register were converted; the two dead links in the fixtures were repaired; the templates show
the link form.

Eight self-test cases across both languages, shown to fail: a heading renamed under a link, an
abbreviated anchor that renders but lands nowhere, and — in the opposite direction, which is the
one that costs trust — an example link inside backticks that must **not** be reported.
