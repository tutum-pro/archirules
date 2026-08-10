# ADR-0009 — Updating a project's registers is a separate act from updating the plugin

**Status:** Accepted (decided by Robert Sternal, 2026-08-11)
**Unblocks:** P10 · **Related:** [ADR-0007](ADR-0007-explicit-version-as-the-migration-anchor.md)

## Context

The question that started this was whether an update skill would duplicate the plugin manager.
It does not, and the boundary is worth stating because it is not obvious.

`/plugin update` and `claude plugin update` replace **the plugin's own files** on disk. Read
against the documentation and confirmed against the tool: they compute a version, fetch the new
copy, and stop. They do not read the user's project, do not migrate anything in
`docs/architecture/`, take no backup, and offer no rollback of anything the user wrote. The
previous version's directory survives on disk for about two weeks, which is cleanup scheduling,
not a restore path.

So a method that changes — a template gaining a field, a checker gaining a rule — arrives in a
project as **new rules applied to old documents**, with nothing to reconcile them. The user
finds out when a checker they did not change starts failing on a register they did not change.

## Decision

### 1. The skill migrates registers. It never touches the plugin

`/archirules:update` runs **after** `/plugin update`, and says so in its own usage text. The two
halves are: the manager moves the method, this moves the project.

### 2. The snapshot is a git branch, and restoring deletes before it restores

A branch at the pre-migration commit. No copied directory, no stash, nothing that moves `HEAD` —
the tree is required to be clean, so the current commit already **is** the snapshot and the
branch is only the name that keeps it findable.

Restoring is `rm -rf docs/architecture` followed by `git restore --source=<branch>`. The removal
is load-bearing: `git restore` alone puts tracked files back and **leaves whatever the migration
added**, so a register restored that way returns in its old shape while still carrying the new
version file. Undone in content, not undone in what it says about itself.

That was found by rehearsing the procedure on a real repository. Reading it would not have
found it; the naive command looks obviously correct.

### 3. Refuse without git, and refuse on a dirty tree

Both are stops, not warnings. Without a repository the snapshot has nowhere to live and the
skill's entire offer — that this can be undone — is false. On a dirty tree the snapshot would
not contain the uncommitted work, and the restore, which deletes the directory, would destroy
it. The safety of step 2 depends entirely on step 1 having run.

### 4. The project records the version it was written against

`docs/architecture/.archirules-version`, one line. Without it there is no "from", and a
migration with no starting point can only be guessed at.

Absent, it means 1.0.0 and every migration ever written gets listed. Safe and tedious, and
better than the alternative: a version inferred from the register's shape would be a guess that
looks like knowledge, and guessing too high skips a migration silently.

The file carries no `.md` suffix on purpose. The checkers glob `**/*.md`, and a version file
counted as a project document would inflate their coverage counters — the defect already
recorded about fixtures kept inside a register root.

### 5. `CHANGELOG.md` is the only input, and silence in it means "nothing to do"

`migrations.py` reads the `### Migration` blocks of the releases in range. A release without one
requires nothing of the reader, and the script **says that in words** rather than printing
nothing, because an empty output reads identically to a script that failed to find its input.

An unrecognised version is exit 2, not a skip. A migration that silently passes over a release
it did not understand leaves a half-converted register, which is the one outcome worse than not
migrating at all.

## Considered and rejected

### 1. A copied snapshot directory, `docs/architecture/.snapshots/`

Independent of git, works in a project with no repository, trivially understood. Rejected: it is
duplicated state of exactly the kind these checkers exist to police, it grows without bound, and
it invites the register and its copy to disagree. Git already holds every previous state of
these files and does it better than a directory of dated copies.

Its one real advantage — working without a repository — is answered by refusing, loudly, with an
instruction to initialise one.

### 2. No snapshot: demand a clean tree and let the user `git revert`

Least code, fewest promises, and technically sufficient. Rejected because "you can always revert
it" is only true for someone who knows which commit to revert to and remembers that this
happened. A named branch, printed before anything is modified, costs one ref and turns that into
something a person can act on six weeks later.

### 3. Migrations as scripts rather than prose

`migrations/1.1.0.py` mutating the register mechanically. Rejected: some migrations need a
judgement about what a record meant, and a script cannot ask. Worse, a script that guesses would
produce a register that satisfies the checker while saying something its author never said —
this method's specific nightmare. The mechanical parts are simple enough for a model to apply
with the register in front of it; the parts that are not, a script would get wrong silently.

### 4. Auto-detecting the project's version from the register's shape

No new file, no state to keep. Rejected: shape-based detection cannot distinguish "written at
1.0.0" from "written at 1.2.0 and missing a section", and guessing high skips migrations. A
recorded version is one line of duplicated state, knowingly accepted, in exchange for never
having to infer.

## Consequences

**Positive.** A method that changes can reach existing projects without their registers quietly
failing checks nobody changed. The change is reversible by a command printed before it starts,
and the reversibility was demonstrated rather than claimed. The boundary against the plugin
manager is written down, so the next person asking does not have to re-derive it.

**Costs, knowingly accepted.**

- **Git is required.** A project keeping registers outside version control cannot use this
  skill at all, and is told so rather than served a weaker version of it.
- **`rm -rf` in a documented procedure.** It is correct only because step 1 refused to start on
  a tree with untracked files. The two steps are one mechanism and anyone editing them must
  treat them as one.
- **One line of duplicated state** in every project: the version file can disagree with what the
  registers actually are, if someone edits registers by hand across a version boundary. Nothing
  detects that.
- **Migrations are applied by a model, not by a script.** They are prose instructions, so two
  runs may produce different wording for the same change. The acceptance test is the checkers,
  which constrain the result without constraining the path.
- **Snapshot branches accumulate.** One per update, never deleted, because deleting them is
  exactly what a user cannot undo. A repository updated twenty times carries twenty refs.

## Implementation status

Done. `skills/update/`, `scripts/migrations.py`, `.archirules-version` written by
`/archirules:bootstrap`, and seven self-test cases covering the ranges `migrations.py` must
distinguish — including the unrecognised version and the missing changelog, both exit 2.

**Rehearsed on a real repository**, not a fixture: a register written in the 1.0.0 vocabulary
(a bare supersession status, `Modifies:` where `Supersedes:` belongs) failed `conform.py` before
the migration, passed both checkers after it, and was restored byte-identical from the snapshot.
The rehearsal is what found the defect in decision 2.

Deliberately not done: deleting snapshot branches, and any attempt to update the plugin itself
from inside the skill. The second is the plugin manager's job and doing it here would mean
holding a copy of its behaviour that goes stale.
