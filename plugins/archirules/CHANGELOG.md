# Changelog

Versions follow [semantic versioning](https://semver.org). For this plugin the readings are:

- **MAJOR** — a register that conformed stops conforming;
- **MINOR** — a new skill, a new check, a new template field;
- **PATCH** — anything a user's register cannot notice.

An entry that requires the reader to change something in their own registers carries a
`### Migration` block. **An entry without one requires nothing** — that is what its absence
means, and `/archirules:update` relies on it.

## 1.3.0 — 2026-08-11

**Added**

- `/archirules:update` — brings a project's registers up to a newer method version. Reads what
  changed, takes a git snapshot that can be restored, applies the migrations, and proves the
  result with both checkers. It does **not** update the plugin; that is `/plugin update`, which
  in turn does not touch your project
  ([ADR-0009](../../docs/architecture/decisions/ADR-0009-updating-a-project-is-not-updating-the-plugin.md)).
- `scripts/migrations.py` — prints the migration work between two versions, and says so in words
  when there is none.
- `/archirules:bootstrap` now writes `docs/architecture/.archirules-version`.

### Migration

**Only if your registers predate this release.** Create
`docs/architecture/.archirules-version` holding one line: the version your registers were last
brought up to. If you do not know, leave the file out — `/archirules:update` then treats the
project as 1.0.0 and lists every migration, which is safe.

Nothing else changes. No record, template or checker rule moved in this release.

## 1.2.0 — 2026-08-11

**Added**

- `--help` on every skill. `/archirules:<skill> --help` prints what the skill needs from you and
  what it will not do, extracted by `scripts/help.py` from a `## Usage` section of that skill —
  not recited from the model's memory
  ([ADR-0008](../../docs/architecture/decisions/ADR-0008-help-comes-from-a-file-not-from-memory.md)).
- `help.py` with no argument lists every skill with its one-line description.

No migration. Nothing in a register changes.

## 1.1.0 — 2026-08-11

The first explicitly versioned release. Everything between 1.0.0 and this entry shipped
unversioned, keyed on commit SHA; that range is not reconstructible as releases and is listed
below as one block rather than invented as a sequence
([ADR-0007](../../docs/architecture/decisions/ADR-0007-explicit-version-as-the-migration-anchor.md)).

**Added**

- `conform.py` — structural conformance checker, with `selftest.sh` proving it can fail.
- `consistency.py` — cross-register checker: a question against the phase it blocks, a phase
  against the questions it waits on, a closed question still declaring a blocker, references to
  decision records, and supersession written in both directions. `selftest-consistency.sh`
  proves it can fail.
- `/archirules:language` — switches a project's documentation language end to end.
- `/archirules:verification` — verification discipline as a skill.
- English translations: `RULES.en.md`, `CASEBOOK.en.md`, `README.en.md`, English templates.
- `CASEBOOK.md` separated from `RULES.md`, so a rule is readable without knowing this
  project's history.

**Changed**

- Skill names and all plugin metadata are English.
- The self-test asserts that every marker either checker keys on occurs in a template or a
  skill, rather than only in its own fixtures
  ([ADR-0006](../../docs/architecture/decisions/ADR-0006-checker-speaks-the-methods-vocabulary.md)).
- `--lang` is accepted in both the `--lang en` and `--lang=en` forms, refuses an unsupported
  language with exit 2, and reports a language that contradicts the register's own README.

**Fixed**

- A cross-register check that could not fire under any input, in either language — it searched
  for a marker and a question number on one line, a shape no template produces (casebook C-11).
- Reference checks disappearing without a word when a set kept no `decisions/` directory.

### Migration

**From 1.0.0, or from any unversioned state after it.** Two changes reach registers that
already exist:

1. **Supersession must name its scope.** A record whose status says `SUPERSEDED by ADR-NNNN`
   with nothing further is now a finding. Add the date and what stopped holding:

   ```
   **Status:** SUPERSEDED by ADR-NNNN, <date> — <what stopped holding>
   ```

   Registers with no superseded records need no action.

2. **`Modifies:` and `Modified by:` are gone.** They were never produced by any template, so a
   register written from the templates cannot contain them. If yours does — it was written
   against a pre-release of the cross-register checker — replace them with `Supersedes:` on the
   newer record and the status line above on the older one.

Everything else is additive. Run both checkers after migrating; that is the acceptance test.

## 1.0.0

Initial release: rules, skills, templates, the casebook, and distribution as a Claude Code
plugin. Registers created at this version conform to 1.1.0 after the migration above.
