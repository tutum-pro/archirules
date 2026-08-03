---
name: audyt
description: Audit the architecture documentation for completeness and truthfulness — numbering defects, missing index entries, superseded records still claiming to be current, statuses that reality has overtaken. Use periodically and before any milestone.
---

# Auditing the registers

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

Fifteen cases across both languages: each defect the checker claims to find is introduced into
a copy of a known-good set and must be caught.

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

## 2. Records that stopped being true

The most dangerous category and the hardest to find:

- a record marked *Accepted* whose decision was in practice reversed;
- a question *blocked by* a question that has since been resolved;
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
