---
name: audit
description: Audit the architecture documentation for completeness and truthfulness — numbering defects, missing index entries, superseded records still claiming to be current, statuses that reality has overtaken. Use periodically and before any milestone.
---

# Auditing the registers

**`--help`** — if `$ARGUMENTS` is `--help`, run
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/help.py audit`, show its output, and stop there.

## Usage

```
/archirules:audit [--help]
```

Reads the whole register set and reports what is defective or has stopped being true. Runs both
checkers and their self-tests first, because a checker nobody has proven can fail says nothing.

**Needs from you:** nothing. It reads; it does not edit.

**Will not:** correct anything. Which side of a disagreement between two registers is wrong is a
decision, and matching a status to whatever the other file says is how a register gains a second
untrue sentence instead of none.

**Result:** either a list of findings or a count of what was checked. Never a reassurance.

**Check, do not reassure.** The result of an audit is a list of findings, or the sentence "I
checked N things and found nothing" — never "everything looks fine".

## 1. Structural conformance — run the checker, do not rewrite it

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/conform.py docs/architecture
```

It checks the artefacts, the sections of every decision record, agreement between the index and
the directory, the numbering and shape of open questions, and the phase register. It detects
the Polish and English variants from `README.md`. Exit code 1 on any problem, so it works as a
CI gate.

**Before trusting it**, run the proof that it can fail:

```
bash ${CLAUDE_PLUGIN_ROOT}/scripts/selftest.sh
```

Each defect the checker claims to find is introduced into a copy of a known-good set and must be
caught, in both languages. The run prints the case count; a number quoted here would go stale
the first time a case is added.

The last assertion in that script is not about a register at all: it requires **every marker
string either checker keys on to occur in a template or in a skill**. A marker invented by a
script and honoured only by its own fixtures proves the script consistent with its test data,
which was never in doubt — and that is exactly how a check that could not fire once survived a
full passing self-test. See ADR-0006 in this plugin's own register.

### Why the checker looks the way it does

Four successive versions of this check produced false results, each for a different reason:

| defect | effect |
|---|---|
| a pattern matching only the plural form of a word | missed the singular; reported six sections absent that were all present |
| a keyword list for "rejected alternatives" | missed a rejection phrased as "we do not create X, because…" |
| a regular expression the tool refused to compile | the error went to stderr, the script printed "clean" |
| a loop over an unquoted variable in a shell that does not word-split | one iteration instead of eleven, reported as full coverage |

Full write-ups: [C-05](../../CASEBOOK.en.md#c-05--a-checker-looked-for-the-plural-and-missed-the-singular),
[C-08](../../CASEBOOK.en.md#c-08--a-private-key-survived-the-cleaning-of-the-history).

Hence three rules, already built into `conform.py`:

1. **Match prefixes, not full wordings.** A wording variant — singular for plural, a longer
   heading that carries extra meaning — is not a deviation.
2. **Open the file before reporting something missing.** Content is often under a different
   heading, or in prose. "Section missing" is a claim about a document, so rule W3 applies.
3. **Account for coverage.** Count what you checked against what exists and **refuse to
   conclude** when they disagree. That is the only one of the four traps above that was caught
   automatically — precisely by that counter.

Divergent heading wording is **not in itself a defect in a document**. A singular form is
correct when there is one item, and a heading like "Costs and preconditions" may carry meaning
that shortening would delete. The defect is only that it cannot be checked mechanically — and that
is fixed in the checker and in the template for new documents, not by rewriting history.

## 1b. Agreement between registers — the second checker

`conform.py` reads one register at a time. Two registers can contradict each other while both
stay well-formed, so that contradiction is invisible to it.

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/consistency.py docs/architecture
```

**Before trusting it**, the same proof:

```
bash ${CLAUDE_PLUGIN_ROOT}/scripts/selftest-consistency.sh
```

It checks five pairings:

| | |
|---|---|
| **A** | a question declaring it blocks a phase, against that phase's status **and** the blocker table |
| **B** | a phase waiting on a question, against that question's existence and status |
| **C** | a question that is no longer open and still declares what it blocks |
| **D** | references to decision records — existence, and entries pointing at a superseded one |
| **E** | non-contradiction of decision records: a supersession link written in both directions, and two records not resolving one question in ignorance of each other |

**It points at a pair, not at a culprit.** Which side of a disagreement is wrong is a decision;
matching a status to whatever the other file happens to say is how a register gains a second
untrue sentence instead of none. Read both, then correct in the record — rule P7.

Category **E** has no other home in this method. `adr/SKILL.md` tells the author to write the
supersession in both directions — `Supersedes:` on the new record, the status line on the old
one — and until this existed, nothing checked that the second direction was written.

What is **not** here: whether the supersession names its scope. That is readable inside a single
file, so it belongs to `conform.py`, and putting it here would erase the only line that
distinguishes the two scripts (ADR-0006).

### The blocker table is a convention, and that is said out loud

Checks A(ii) and B need the phase register to keep a table of what blocks what, under a heading
beginning **`### What blocks`** — `### Co blokuje` in Polish. No template produces one, and no
rule requires it: this is a project convention (rule W9), open as OQ-06.

A set that keeps none has those two checks skipped — **and the skip is printed**, because
otherwise "0 problems" silently means "0 checks ran". The same applies where there is no
`decisions/` directory: checks D and E say they did not run rather than reporting nothing.

## 1c. Registers against the code that implements them

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/trace.py docs/architecture
```

Commits claim register entries with trailers — `Archirules-Phase:`, `Archirules-ADR:`,
`Archirules-OQ:` — and this derives the mapping from git history. **The history is the truth**;
`traceability.md` is a generated view of it, and the checker recomputes that view to confirm it
was not edited by hand.

Two findings it always reports: a trailer naming an entry no register holds, and a view that is
not a faithful regeneration of the commit it records.

`--strict` adds two more: a closed phase no commit claims, and a view behind HEAD. **Off by
default on purpose.** A repository whose history predates the mechanism cannot satisfy them, and
a gate everybody has to switch off teaches people to switch gates off. When it should become the
default is OQ-07.

## 2. Records that stopped being true

The most dangerous category and the hardest to find:

- a record marked *Accepted* whose decision was in practice reversed;
- a question that is closed and still declares what it blocks — **mechanised**, check C in section 1b, but only for the question's own `Blocks:` field; a blocker written into prose is still yours to spot (OQ-05);
- a question *blocked by* a question that has since been resolved — **not mechanised**; `Depends on:` is not cross-checked, and attention does not scale past twenty records;
- a question still *open* whose subject has been built;
- a sentence describing behaviour the code does not have.

For every record ask: **if somebody read only this document, would they conclude something
consistent with what is built?**

## 3. Code with no trace in the documentation

List what has been introduced since the last audit — migrations, gates, modules, public types —
and check each has a mention. Look for the **concept**, not the filename: a migration
`0007_retry.sql` is often described as "migration `0007`".

## 4. Decisions that never reached the register

Go through the commit history and the phase register looking for choices that live only in the
code. **This is the most common and most serious finding.** A decision taken mid-work rarely
asks to be written down.

## 5. Risks discovered and never recorded

Security and operations especially: keys in history, repositories with no backup, credentials
in manifests, configuration that exists on one machine only. Check the **actual state**
(`git ls-remote`, `git branch`, whether an object exists), not your memory of it.

## Reporting

Report by severity, **with evidence for each finding**. Commit the fixes separately from
feature work — a history with a single "feature + docs" commit hides the fact that the audit
found anything.
