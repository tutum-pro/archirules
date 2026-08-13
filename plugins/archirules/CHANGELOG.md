# Changelog

Versions follow [semantic versioning](https://semver.org). For this plugin the readings are:

- **MAJOR** — a register that conformed stops conforming;
- **MINOR** — a new skill, a new check, a new template field;
- **PATCH** — anything a user's register cannot notice.

An entry that requires the reader to change something in their own registers carries a
`### Migration` block. **An entry without one requires nothing** — that is what its absence
means, and `/archirules:update` relies on it.

## 2.1.0 — 2026-08-13

**Added**

- `scripts/relink.py` — turns bare `ADR-NNNN` and `OQ-NN` references in **header fields** into
  links. A dry run reports and changes nothing; `--write` applies. Prose is deliberately out of
  scope
  ([ADR-0016](../../docs/architecture/decisions/ADR-0016-the-converter-covers-header-fields-only.md)).

### Migration

**Optional in this release, and worth doing before the next major one.**

A future major version will require references in header fields to be links. This release ships
the tool for it first, on purpose: a requirement that arrives with no means to satisfy it is a
gate that punishes people for lacking something the method never gave them.

```
python3 <plugin>/scripts/relink.py docs/architecture           # shows what it would change
python3 <plugin>/scripts/relink.py docs/architecture --write   # applies it
```

Read the diff before committing — `--write` edits many files at once. Nothing breaks if you
skip this: bare references still pass every check today.

## 2.0.0 — 2026-08-12

**Changed — breaking**

- `conform.py` now checks the **anchor** of a link, not only the file it points at. A link that
  resolves to the right document and to no heading inside it is a finding. This is the half that
  rots in silence: rename a heading and every link to it lands at the top of the document, with
  the file still present and the checker still green
  ([ADR-0015](../../docs/architecture/decisions/ADR-0015-references-are-links-and-anchors-are-checked.md)).
- A reference to a register entry is a link, in every field and every direction. The templates
  show the link form; they previously prescribed plain text.

**Fixed**

- An example link written between backticks, or inside a fenced code block, is no longer read as
  a real link. The checker used to report a document as broken for showing what a link looks
  like.

### Migration

**Run the checker first — it tells you exactly what to repair.**

```
python3 <plugin>/scripts/conform.py docs/architecture
```

Two kinds of finding are new in this release:

1. **`link resolves to the file but not to a heading in it: #something`.** The heading was
   renamed, or the anchor was abbreviated. Anchors come from the heading text: lowercase, drop
   anything that is not a letter, digit, space, hyphen or underscore, spaces become hyphens. An
   em dash disappears and leaves the hyphens from the spaces around it, which is why anchors to
   `### OQ-01 — Some question` read `#oq-01--some-question`. Shortening one to `#oq-01` renders
   as a link and lands nowhere.

2. Nothing else. Existing plain-text references keep working; turning them into links is
   recommended by the templates but is not required and is not checked.

If a repair is not obvious, the finding names the file and the line.

## 1.7.0 — 2026-08-11

**Added**

- `/archirules:version` — reports the installed method version and the version this project's
  registers stand at, and whether they agree. Read-only: no clean tree and no git repository
  required, which is where `/archirules:update` refuses. Registers **ahead** of the method are a
  distinct outcome from behind, because no migration runs backwards
  ([ADR-0014](../../docs/architecture/decisions/ADR-0014-reading-the-version-is-not-updating.md)).

No migration. Nothing in a register changes.

## 1.6.1 — 2026-08-11

**Fixed**

- `/archirules:help` said "four documents in `docs/architecture/`" and then listed the four
  registers, omitting the index that sits beside them. Four is the number of registers, not of
  files. Corrected, and the closed-set rule now stated where a reader meets it.

No migration. Nothing in a register changes.

## 1.6.0 — 2026-08-11

**Changed**

- Every skill's `--help` now ends in an `### Examples` block with real invocations, not only the
  `/archirules:<skill> [--help]` form. The form says how to type the command; the examples say
  what to type into it, which is the question people arrive with. The self-test requires one,
  so a skill cannot ship without
  ([ADR-0008](../../docs/architecture/decisions/ADR-0008-help-comes-from-a-file-not-from-memory.md)).

No migration. Nothing in a register changes.

## 1.5.0 — 2026-08-11

**Added**

- `/archirules:help` — explains the method itself: the problem it addresses, what it consists
  of, what is mechanised and what is not, what it costs, what it does not do, and how much
  evidence there actually is. Every casebook case, rule, script and skill it names is verified to
  exist by the self-test
  ([ADR-0011](../../docs/architecture/decisions/ADR-0011-a-skill-that-explains-the-method.md)).

No migration. Nothing in a register changes.

## 1.4.0 — 2026-08-11

**Added**

- Traceability from registers to the commits that implement them. Commits carry
  `Archirules-Phase:`, `Archirules-ADR:` and `Archirules-OQ:` trailers; `scripts/trace.py`
  derives the mapping and writes `docs/architecture/traceability.md`. The git history is the
  truth and the file is a verified view of it — never a hand-maintained list
  ([ADR-0010](../../docs/architecture/decisions/ADR-0010-traceability-derived-from-git-trailers.md)).
- `trace.py --strict` additionally fails on a closed phase no commit claims and a view behind
  HEAD. Off by default; see OQ-07 in this plugin's own register.

### Migration

**Optional, and nothing breaks if you skip it.** To start tracing:

1. Add a trailer to commits that implement a register entry:

   ```
   Archirules-Phase: P3
   ```

2. Generate the view, in a commit of its own that carries **no** trailer:

   ```
   python3 <plugin>/scripts/trace.py docs/architecture --write
   ```

Phases closed before you start will be listed under "Closed phases no commit claims" and stay
there. That list can only shrink and never grow, which is what makes it readable.

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
