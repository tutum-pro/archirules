# ADR-0001 — Polish for the method, English for the executable layer

**Status:** Accepted (2026-08-03)
**Related:** [ADR-0003](ADR-0003-casebook-apart-from-rules.md), [ADR-0005](ADR-0005-distribution-as-a-plugin.md)

## Context

The method was written and argued in Polish, by a Polish-speaking author, for a Polish team. It
is published for reuse — including in projects whose teams are not Polish-speaking.

An early version mixed the two without a rule. One `SKILL.md` had an English `description` in
its frontmatter and a Polish body. That is not bilingualism; it is inconsistency that nobody
decided.

## Decision

**Two layers, two languages, no exceptions.**

| layer | language | why |
|---|---|---|
| method content — `RULES.md`, `CASEBOOK.md`, templates, READMEs | Polish canonical, English translation | it is prose to read and argue about; the original carries the reasoning |
| executable layer — skills, scripts, plugin metadata | English only | consumed by a model at run time and read by everyone who installs the plugin; closer to code than to prose |

**Where a translation disagrees with the Polish original, the Polish version wins.**

The language of an instruction does not determine the language of its output: an English skill
produces Polish decision records if that is the project's language.

## Considered and rejected

**Everything in English.** Would give reach, at the cost of writing the reasoning in a language
the author does not think in. The reasoning is the product here; a slightly awkward translation
of it is cheaper than a slightly shallower original.

**Everything in Polish.** Would make the plugin unusable outside Polish-speaking teams, and the
frontmatter `description` — the text a model matches a task against — genuinely needs to be
English.

**Bilingual everything, both canonical.** Two originals drift, and the drift is invisible until
somebody acts on the stale one. Naming one canonical costs nothing and settles every future
disagreement in advance.

## Consequences

**Positive.** Every file has an obvious language. The `description` / body mismatch cannot recur.
Translations have a tie-breaker.

**Costs, knowingly accepted.**

- **Two versions of the prose to maintain.** Mitigated by concentrating the reasoning in
  `RULES.md` and keeping templates deliberately thin, so there is less surface to drift.
- **The English reader lands on a translation.** Stated at the top of both READMEs rather than
  discovered.
- **Quoted Polish markers survive in English files.** `conform.py` must contain the Polish
  strings it matches, and the audit skill quotes them. Unavoidable, and marked as such.

## Implementation status

Done. Verified by grep: no Polish characters in any skill or script except the Polish marker
table in `conform.py`, its quotations in the audit skill, and the Polish half of the test data —
all three necessarily Polish.
