# ADR-0007 — The plugin carries an explicit version, and that version is what a migration moves between

**Status:** Accepted (decided by Robert Sternal, 2026-08-11)
**Unblocks:** P8, P10 · **Related:** [ADR-0005](ADR-0005-distribution-as-a-plugin.md)

## Context

`plugin.json` has no `version` field. Claude Code then resolves the version from the next
source available, which for a git-hosted marketplace is **the commit SHA of the source**. The
consequences are two, and only the second one matters:

- users receive an update on **every commit**, including one that only fixes a typo in a README;
- there is **no name for what they are moving between**. A SHA is an identity, not a position.
  "Migrate a register from `e589f5f` to `33d2d36`" is not a sentence a migration note can be
  written against, because nothing about those two strings says what changed or which one is
  older.

This blocks phase P10 outright. A skill that adapts a project's registers to changes in the
method has to answer "which changes" — and that question needs an ordered version, not a hash.

The gap was found by running the tool that already checks for it:

```
claude plugin validate ./plugins/archirules
  ❯ version: No version specified. Consider adding a version following semver
✔ Validation passed with warnings
```

## Decision

### 1. `plugin.json` carries an explicit semver

Bumped by hand, following the usual reading: MAJOR when a register that conformed stops
conforming, MINOR for a new skill or check, PATCH for anything a user's register cannot notice.

### 2. `CHANGELOG.md` is the register of releases, and it is the migration's input

Each version gets an entry, and an entry that changes anything about **registers** — a template,
a marker, a required section — says so in a `### Migration` block. Phase P10 reads those blocks
and nothing else. A release with no such block requires no work from the user, and saying that
explicitly is the point.

### 3. The two are checked against each other

`selftest.sh` asserts that the version in `plugin.json` equals the newest heading in
`CHANGELOG.md`. Neither can move without the other. This is the same reasoning as the vocabulary
assertion in [ADR-0006](ADR-0006-checker-speaks-the-methods-vocabulary.md): two files that must
agree, and no reason to leave the agreement to attention.

### 4. The first explicit version is 1.1.0, and the record says why it is not 1.0.0

`1.0.0` was released as a commit and never tagged. Everything between it and today — the
conformance checker, the language switch, the casebook split, the cross-register checker — went
out unversioned. Numbering the current state `1.1.0` and stating plainly that the intermediate
states had no version is more honest than inventing a release history nobody can verify.

## Considered and rejected

### 1. Keep SHA-based versioning

It is what the tool does with no configuration, and it delivers changes fastest. Rejected
because it makes P10 impossible to specify: migrations move between positions, and a hash has no
position. The delivery speed is also not obviously a benefit — a method changing under a user's
register on every typo commit is not a property to protect.

### 2. Version in the marketplace entry rather than in `plugin.json`

Claude Code accepts either, and `plugin.json` wins where both are set. Rejected because the
marketplace file is about distribution and the plugin file is about the plugin; a version placed
in the catalogue is invisible to anyone reading the plugin itself, including the migration.

### 3. Date-based versioning, `2026.08.11`

Immune to arguments about what counts as a breaking change, and the ordering is free. Rejected
because it carries no signal: a user seeing a new date cannot tell whether their register is
about to stop conforming. The whole reason for the field is to answer that question.

### 4. Generate `CHANGELOG.md` from git history

The commit messages here are long and already explain their reasoning, so a generator would have
material to work with. Rejected: a changelog is written for someone deciding whether to update,
a commit message for someone reading the diff. The audiences want different things, and the
generated file would be a third copy of the same facts going stale in its own way.

## Consequences

**Positive.** There is a name for what a register is at, and therefore a name for what it can be
migrated to. `claude plugin validate --strict` passes, which is the check the submission pipeline
runs. Users stop receiving an update every time a comment changes.

**Costs, knowingly accepted.**

- **The bump is manual and forgettable.** Pushing without it means users get nothing, silently.
  The self-test catches a version that disagrees with the changelog; it cannot catch a change
  that should have been a release and was not.
- **Judging MAJOR is a judgement.** "A register that conformed stops conforming" is clearer than
  most such rules but still needs someone to apply it. Recorded here rather than pretended away.
- **A second file to keep true.** `CHANGELOG.md` joins the registers as a document that can go
  stale, and the method's own warning about unmaintained registers applies to it.
- **The version history before 1.1.0 is not reconstructible.** Anyone bisecting the method's
  behaviour across that range has commits and nothing else.

## Implementation status

Done. `plugin.json` at 1.1.0, `CHANGELOG.md` written back to the 1.0.0 release with the
unversioned range stated as such, and the agreement between them asserted by `selftest.sh` —
shown to fail on a version bumped in one file only. `claude plugin validate --strict` passes.

Deliberately not done: tagging the repository. Git tags and the plugin version would be a third
place for the same fact, and Claude Code reads neither. Reconsider if releases ever need to be
fetched by tag.
