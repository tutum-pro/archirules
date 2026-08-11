---
name: language
description: Switch a project's architecture documentation from one language to another, end to end - decision records, open questions, phase register, verification register, file names, cross-links and the CLAUDE.md fragment. Use when the working language of the team changes.
---

# Switching the documentation language

**`--help`** — if `$ARGUMENTS` is `--help`, run
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/help.py language`, show its output, and stop there.

## Usage

```
/archirules:language <target language> [--help]
```

Switches an entire register set from one language to another: records, questions, phases,
verification, **file names**, cross-links, and the `CLAUDE.md` fragment.

**Needs from you:** the target language, and a clean git tree — file renames go through
`git mv`, and a half-finished switch is worse than none.

**Will not:** translate git history. The current state becomes one language; the past does not.

**Acceptance is the checker, not the prose:** `conform.py --lang <target>` must report zero
problems and detect the target language. A forced language contradicting the register's own
README is itself reported.

The case this exists for: a project started in one language because the team spoke it, and
somebody joined who does not. From that moment the register has to be readable by everyone, and
**a half-translated register is worse than an untranslated one** — nobody knows which part is
current.

## Say this first, before starting

**The invocation is one gesture. The work is not.** Translating an architecture register is a
careful rewrite of every document, done by reading each one, not by a script. For a project
with a dozen decision records and a few dozen open questions this is substantial work, and it
gets interrupted. Tell the user the size before you begin:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/conform.py docs/architecture
wc -l docs/architecture/*.md docs/architecture/decisions/*.md | tail -1
```

Report the number of documents and lines, and agree the order. **Do not start a switch you
cannot finish in the session unless you commit per document** — see below.

## The one rule that protects the record

**Evidence is not translated.** Verbatim things stay verbatim:

- command output, error messages, log lines;
- identifiers: element ids, table and column names, role names, file paths, commit hashes;
- quoted code, SQL, configuration;
- proper names and product names.

A register whose evidence has been translated has stopped being evidence. If a decision record
quotes `compiler: flow "Flow_toConverted" carries a condition`, that string stays exactly as
it is — it is what the tool actually printed, in the language the tool actually speaks.

Translate the prose around it, and where the surrounding sentence explains a quoted message,
keep the quote and translate the explanation.

## Terminology

`RULES.md` and `RULES.en.md` in this plugin are the **authoritative glossary**: they contain
the same argument in both languages, so the vocabulary of the method is already fixed there.
Take terms from them rather than inventing them — "faza"/"phase", "twarda bramka"/"hard gate",
"koszty przyjęte świadomie"/"costs, knowingly accepted", "rejestr weryfikacji"/"verification
register".

Consistency matters more than elegance. One term, one translation, throughout.

## Procedure

### 1. Inventory and plan

List every file that changes, including the renames:

| pl | en |
|---|---|
| `fazy-realizacji.md` | `phases.md` |
| `rejestr-weryfikacji.md` | `verification.md` |
| `README.md`, `open-questions.md`, `decisions/ADR-*.md` | same names |

Decision-record filenames carry a slug in the source language (`ADR-0013-rdzen-w-bibliotece.md`).
**Renaming them breaks every link and every reference in commit messages.** Default to leaving
slugs alone and translating only the content; rename only if the user asks, and then fix the
links in the same pass.

### 2. Rename with git, not with the filesystem

```
git mv docs/architecture/fazy-realizacji.md docs/architecture/phases.md
git mv docs/architecture/rejestr-weryfikacji.md docs/architecture/verification.md
```

`git mv` keeps the history attached to the file. A delete-plus-create loses it, and the history
of a decision register is a large part of its value.

### 3. Translate, one document at a time, committing as you go

Order: `README.md` first (it fixes the vocabulary and the index), then the decision records in
numerical order, then open questions, then the phase register, then the verification register.

**Commit after each document or small group.** A switch interrupted mid-way then leaves a
reviewable, resumable state rather than a working tree nobody can reason about.

Preserve exactly: record numbers, question numbers, statuses, dates, cross-reference numbers,
table structure, the order of everything.

### 4. Fix the cross-links

Renamed files are referenced from other documents. After renaming, search and repair:

```
grep -rn "fazy-realizacji.md\|rejestr-weryfikacji.md" docs/ --include="*.md"
```

Then let the checker confirm nothing dangles.

### 5. Switch the project's CLAUDE.md

Replace the archirules fragment with the target-language version — `CLAUDE.md.en.example` or
`CLAUDE.md.pl.example` — keeping any project-specific lines the user added around it.

### 6. Verify — this is the acceptance criterion, not the translation itself

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/conform.py docs/architecture --lang <target>
```

It must report zero problems, and the language it detects must be the target one. The checker
also verifies that **no internal link dangles**, which is what catches a rename whose
references were not updated.

Then check by counting, not by feeling:

- the same number of decision records as before;
- the same set of question numbers — `grep -oE "^### OQ-[0-9]+"` before and after must match;
- the same number of rows in the phase table.

Anything that changed count was lost or duplicated in translation.

## Traps found by running this procedure on a real register

The switch was rehearsed on a copy of a real 23-document register before this skill was
trusted. Three things went wrong, and all three were silent. Full write-ups:
[C-06](../../CASEBOOK.en.md#c-06--changing-one-punctuation-mark-switched-off-thirty-seven-checks),
[C-07](../../CASEBOOK.en.md#c-07--tightening-the-safety-net-blinded-it).

**A different dash switches off a whole section.** Translating `### OQ-01 — text` to
`### OQ-01 - text` made the checker parse **zero** questions out of thirty-six. Numbering and
status checks stopped applying and the gate reported success — the check count fell from 168
to 131 and nothing said so. The checker now accepts any dash and, more importantly, compares
**headings that look like questions** against **headings that parsed**, so any future drift in
that format fails loudly instead of disabling the section.

**A near-miss translation of one heading breaks language detection.** Writing "Mandatory
requirements" instead of "Binding requirements" made detection fall back to the source language
and produced 47 spurious findings about missing sections that were all there. The checker now
says explicitly that it could not detect the language, so the flood has a stated cause.

**Renaming files breaks links that live in other documents.** On the rehearsal register the
rename produced exactly three dangling links — in `README.md`, in `open-questions.md` and in a
decision record. This is why step 4 exists and why the checker verifies links at all.

The lesson underneath all three: **a translation defect does not look like a defect.** It looks
like a document that is merely worded differently, and the tooling goes quiet. Run the checker
after every document, not only at the end.

## What NOT to do

**Do not keep both languages.** Two parallel registers drift, and the drift is invisible until
somebody acts on the stale one. The previous language stays in git history, which is the right
place for it — a record that stopped being current is not deleted, it is superseded (rule P7).

**Do not translate the archirules plugin itself.** Its executable layer — skills, scripts,
metadata — is English by design, and `RULES.md` is canonically Polish. A project switching its
own documentation changes nothing about the method it follows.

**Do not translate git history or commit messages.** They are a record of what was said at the
time. Rewriting them would be falsifying it, and rewriting published history breaks every clone.

## Afterwards

Record the switch. It is a decision with a cost and it belongs in the register:

- a line in the phase register or a short decision record — when, why, who asked;
- the cost, stated plainly: **the history before the switch is in the previous language**, so
  anyone reading `git log -p` on an old document meets it there.

That last point is the honest limit of this operation. The current state becomes one language;
the past does not.
