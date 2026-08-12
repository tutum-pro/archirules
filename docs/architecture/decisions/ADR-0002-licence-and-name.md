# ADR-0002 — CC BY-SA 4.0 and a reserved name

**Status:** Accepted (2026-08-03)
**Related:** [ADR-0005](ADR-0005-distribution-as-a-plugin.md)

## Context

The repository is public and meant to be reused, including inside commercial projects for
third-party clients. The author bears the legal and financial responsibility for the work and
wanted the strictest licence that is still genuinely open.

The content is 23 files of Markdown and two JSON files. There is no executable product.

## Decision

**CC BY-SA 4.0**, plus an explicit statement that the licence grants no rights to the names
"archirules" and "tutum-pro".

Three consequences are spelled out in the README rather than left to be inferred:

1. **Internal use carries no obligations.** ShareAlike triggers on distribution, not on use.
2. **Publishing an adaptation requires the same licence.**
3. **Documents produced with the method are not derivative works.** The registers written in a
   user's project belong to that user. The licence covers the method, not its output.

The legal text is the canonical one, fetched from the licence steward rather than reproduced
from memory.

## Considered and rejected

**NC — non-commercial.** Sounds like the strongest protection and is a trap. It is not open
source under the OSI definition, and the author's own use case is commercial client work: it
would create friction exactly where it was meant to help.

**ND — no derivatives.** A method that may not be adapted is a dead method.

**GPL / AGPL.** Copyleft designed for linked code does not bite on prose, and the legal status
of prompt files is unsettled. It would read as strict while achieving nothing concrete.

**CC BY.** Maximum reach, but anyone could close a derivative. Rejected because ShareAlike costs
adoption only for those who intend to close it.

## Consequences

**Positive.** Attribution is compulsory. Derivatives stay open. Internal adaptation by any team
is unencumbered.

**Costs, knowingly accepted.**

- **Publishing an adaptation forces BY-SA on it**, which some organisations avoid on principle.
  Accepted: those are also the organisations least likely to contribute back.
- **A licence does not protect a name.** The trademark note does that, and its enforcement is
  social, not automatic.
- **Nothing prevents commercial use of the method.** Copyleft forbids closing, not selling.

## Implementation status

Done. `LICENSE` holds the canonical text (verified by header, the ShareAlike clause, and the
first and last sections). GitHub detects it as `cc-by-sa-4.0`. The trademark note is in both
READMEs.
