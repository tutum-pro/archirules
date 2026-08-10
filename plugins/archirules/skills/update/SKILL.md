---
name: update
description: Bring a project's registers up to a newer version of the archirules method — read what changed, take a restorable snapshot first, apply the migrations, and prove the result with both checkers. Use after the plugin has been updated, or when the registers were written against an older version.
---

# Updating a project to a new method version

**`--help`** — if `$ARGUMENTS` is `--help`, run
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/help.py update`, show its output, and stop there.

## Usage

```
/archirules:update [--help]
```

Adapts **this project's registers** to a newer version of the method: reads what changed between
the version the registers were written against and the version now installed, takes a snapshot
that can be restored, applies the changes, and proves the result with both checkers.

**Needs from you:** a git repository with a clean working tree, and decisions where a migration
needs one. Some changes are mechanical; some ask what a record actually meant.

**Will not:** update the plugin. That is `/plugin update archirules@<marketplace>`, which
replaces the plugin's own files and **does not touch your project at all** — no register
migration, no backup, no rollback of anything you wrote. This skill is the other half, and it
runs after.

**Will not:** run on a dirty tree. The snapshot is a git ref, so uncommitted work would not be in
it, and a restore would silently discard it.

**Restoring:** `rm -rf docs/architecture && git restore --source=<snapshot branch> -- docs/architecture`.
The branch name is printed before anything is modified, and the restore touches the registers
only — your code is untouched.

## 1. Refuse before you start

Three conditions, checked in this order. **Stop on the first that fails and say which** — do not
proceed with a degraded version of the procedure.

```
git rev-parse --is-inside-work-tree     # must print true
git status --porcelain                  # must print nothing
```

- **Not a git repository.** Stop. The snapshot has nowhere to live, and this skill's whole offer
  is that the change can be undone. Tell the user to initialise a repository, or to copy
  `docs/architecture/` aside by hand and migrate without the safety net knowingly.
- **Dirty tree.** Stop, and list what is uncommitted. A snapshot taken now would not contain
  that work, so a later restore would delete it.
- **No `docs/architecture/`.** Stop. There is nothing to migrate; the skill they want is
  `/archirules:bootstrap`.

## 2. Find both versions

**The project's version** is in `docs/architecture/.archirules-version`, one line, nothing else.

If that file does not exist, the registers predate version tracking. Treat the project as
**1.0.0**, and **say so out loud** — every migration since then will be listed, and some may
already have been done by hand. Never guess a later version to shorten the list: a migration
skipped because it looked done is exactly the half-converted register this skill exists to
avoid.

**The method's version** is `version` in `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`.

If the two are equal, there is nothing to do. Say that and stop; do not take a snapshot for a
change you are not making.

## 3. Read what actually changed

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/migrations.py --from <project> --to <method>
```

This reads `CHANGELOG.md` and prints the `### Migration` block of every release in the range.
**A release with no such block requires nothing** — that is what its absence means, and the
script says so in words rather than printing nothing.

Exit 2 means a version it does not recognise. Do not work around it: a range the script cannot
read is a range you cannot apply correctly.

**Show the output to the user before touching anything.** They are about to authorise edits to
their own decision register.

## 4. Snapshot, and verify it exists

```
git branch archirules-snapshot-<from>-to-<to>-<date>
git rev-parse --verify archirules-snapshot-<from>-to-<to>-<date>
```

A branch at the current commit — no empty commit, no stash, nothing that moves `HEAD`. The tree
is clean, so the current commit already **is** the snapshot; the branch is the name that keeps
it findable after twenty more commits.

**Verify the ref resolves before continuing.** A snapshot that was not created, in a skill whose
offer is that the change can be undone, is the hard gate at P10 failing. If it did not, stop and
say so.

Print the restore command now, not at the end:

```
rm -rf docs/architecture
git restore --source=archirules-snapshot-<from>-to-<to>-<date> -- docs/architecture
```

**The `rm -rf` is not optional and is not belt-and-braces.** `git restore` on its own puts
tracked files back and leaves behind anything the migration *added* — including
`.archirules-version`. A register restored that way comes back in its old shape while claiming
the new version: undone in content, not undone in what it says about itself. That was found by
rehearsing this procedure rather than by reading it.

It is safe here for one reason only: step 1 refused to start on a tree with untracked files, so
nothing in `docs/architecture/` is unversioned except what this skill just wrote. **If you skip
step 1, this command destroys work.**

## 5. Apply the migrations, oldest release first

In order. A later migration may assume an earlier one has run.

Mechanical changes — a renamed field, a status line gaining a scope — apply directly. Where a
migration needs a judgement about what a record meant, **ask**; do not choose the reading that
makes the checker happy. That is the same rule as the audit skill's: matching a document to
whatever satisfies a script is how a register gains a second untrue sentence instead of none.

**A migration that changes what a record says is a change to the register**, so rule P7 applies:
if something stated in the register stops being true, say so in the record rather than deleting
it quietly.

## 6. Write the new version

`docs/architecture/.archirules-version` gets the method's version, one line. Do this **after**
the migrations and **before** the checkers, so that a failing check leaves a project whose
recorded version matches what the registers were actually migrated to.

## 7. Prove it, or restore it

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/conform.py docs/architecture
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/consistency.py docs/architecture
```

Both must report zero problems and exit 0. **This is the acceptance test for the migration**,
not the fact that the edits were made.

If either fails and the cause is not obvious, restore rather than improvise:

```
rm -rf docs/architecture
git restore --source=<snapshot branch> -- docs/architecture
```

Then confirm the restore actually restored: `git status --porcelain docs/architecture` must
print nothing. A restore reported but not verified is a claim, and this skill's whole offer is
that the change can be undone.

Then report what failed. A half-migrated register that passes because it was patched until the
checker went quiet is worse than one that was never migrated.

## 8. Report

- the version moved from and to;
- which releases had migrations and what was changed in which file;
- **what needed a decision, and what was decided**;
- the checker output, as output;
- the snapshot branch name and the restore command, again.

The snapshot branch is not deleted. It costs one ref and it is the only thing standing behind
the claim that this can be undone.
