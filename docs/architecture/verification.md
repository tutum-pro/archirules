# Verification register

What has been **verified**, as opposed to merely **asserted**.

Organised by subject rather than by category: verification is about a thing, not a bucket.

## The conformance checker

**Verified.** That it fails on each defect it claims to catch, in both supported languages —
`scripts/selftest.sh`, twenty-one cases, exit code asserted per case. That the English fixture
is detected as English, so a silent fallback in language detection cannot pass unnoticed.

**Verified.** That it reports zero problems on a real 23-document register, and that this is not
vacuous: the same register with a deliberately broken link, a missing section, a numbering gap
or a drifted heading format produces a non-zero exit.

### Correction 2026-08-03 — four earlier versions of this check were worthless

They reported success against deliberately broken inputs. Written up as
[C-01](../../plugins/archirules/CASEBOOK.en.md#c-01--a-gate-that-could-not-fail),
[C-06](../../plugins/archirules/CASEBOOK.en.md#c-06--changing-one-punctuation-mark-switched-off-thirty-seven-checks),
[C-07](../../plugins/archirules/CASEBOOK.en.md#c-07--tightening-the-safety-net-blinded-it).

Only one of the four was caught automatically, by coverage accounting. The others surfaced by
running the check against deliberately broken data — which is now what `selftest.sh` does on
every invocation.

## The cross-register checker

**Verified.** That it fails on each class of defect it claims to catch, in both supported
languages — `scripts/selftest-consistency.sh`, forty-one cases. Thirty-four assert an exit code
and seven assert what was **printed**, because an exit code says a defect was found and not
which one. Two of the thirty-four assert a usage error, which must not share an exit code with a
finding about a register.

**Verified.** That the self-test itself can fail. With `consistency.py` replaced by one that
always returns 0, twenty-four of the forty-one cases fail; the seventeen survivors are exactly
those that do not assert "exit 1". With the script replaced by one that does not parse,
seventeen fail. The equivalent figures for `selftest.sh` are 34 cases, 22 failing under an
always-green `conform.py`.

**Verified.** That every marker string either checker keys on occurs in a template or in a
skill — asserted at the end of `selftest.sh`, searching `templates/` and `skills/` and nothing
else. Shown to fail before it was satisfied: it named six markers with no documentary source
(`ZASTĄPIONY`, `przez`, `Blokuje`, `Co blokuje`, `What blocks`, and the Polish superseded status
generally), which is what drove the template and skill corrections in
[ADR-0006](decisions/ADR-0006-checker-speaks-the-methods-vocabulary.md).

**Verified.** That `conform.py` reports a supersession status naming no scope, and does **not**
report one that names it — both directions, both languages, with the reason pinned by reading
the message rather than the exit code.

**Verified.** That a `--lang` contradicting the register's own README is reported by both
checkers, and that an unsupported language is refused with exit 2 rather than being silently
detected instead. The spaced form `--lang en` and the `--lang=en` form are both honoured.

**Asserted, not verified.** That the five cross-register pairings are the ones worth having.
They are the relations the templates express; whether a register drifts in some other way that
matters more is unknown until the method is kept by somebody else — phase P6.

### Correction 2026-08-11 — this checker shipped with a check that could not fire

Between 2026-08-10 (commit `75d6d68`) and this entry, `skills/audit/SKILL.md` stated that a
resolved question still cited as a blocker was "now mechanised". It was not. The check looked
for a marker and a question number on one line, a shape no template produces, and it was the
only one of the five without a case of its own in the self-test — so twenty-eight passing cases
said nothing about it. Written up as
[C-11](../../plugins/archirules/CASEBOOK.en.md#c-11--a-check-with-no-case-of-its-own-could-not-fire).

Two further claims from the same period were wrong in the same direction. The checker's
self-test proved it consistent with fixtures written in vocabulary the checker had invented,
while a register built by following `adr/SKILL.md` literally was reported as broken. And the
reference checks vanished without a word when a set kept no `decisions/` directory, in a script
whose own docstring promised that skips are printed.

None of this was caught by reading. All of it was caught by running the checker against
documents produced from the instructions instead of from the fixtures.

## The release version

**Verified.** That `claude plugin validate ./plugins/archirules --strict` passes. Before the
version field existed the same command reported `version: No version specified` and passed only
with warnings, which `--strict` turns into a failure — so this asserts the change, not the tool.

**Verified.** That the agreement between `plugin.json` and `CHANGELOG.md` fails in each of the
four ways it can be wrong: version bumped alone, changelog bumped alone, version field removed,
changelog file missing. The last is the one that matters — an assertion going quiet when its
input disappears is the C-11 shape, and this one prints a sentinel rather than an empty result.

**Asserted, not verified.** That the version will actually be bumped when it should be. Nothing
detects a change that ought to have been a release and was not; the gate only catches the two
files disagreeing. Stated as a cost in
[ADR-0007](decisions/ADR-0007-explicit-version-as-the-migration-anchor.md) rather than papered
over.

## Skill help

**Verified.** That every skill answers `--help` with text extracted from its own `SKILL.md`, and
that the gate fails in five shapes: a new skill added without a usage section, the section
renamed, the routing line broken, a usage naming a different skill in its invocation line, and
`help.py` made unimportable. The last prints one line per skill rather than going quiet.

**Asserted, not verified.** That the model routes `--help` to the script rather than answering
from its own reading of the skill. Nothing in the plugin system parses flags, so this cannot be
mechanised; it is the residue named as a cost in
[ADR-0008](decisions/ADR-0008-help-comes-from-a-file-not-from-memory.md).

**Not verified, and no mechanism exists.** That the "Will not" lines are true. They are the
most useful sentences in each usage block and the ones with the least enforcement.

## Updating a project across method versions

**Verified.** On a real git repository, not a fixture: a register written in the 1.0.0
vocabulary failed `conform.py` before the migration, passed both checkers after it, and was
restored from the snapshot byte-identical — `git diff --stat <snapshot>` empty, checksums equal.

**Verified.** That the obvious restore command is **not** byte-identical. `git restore` alone
leaves files the migration added, and the register returns in its old shape carrying the new
version file. Measured, not reasoned about: `a796ddb8…` against a target of `e4a070cc…`.

**Verified.** That `migrations.py` distinguishes the ranges it must: work in range, no register
changes in range, already current, a version the changelog does not know (exit 2), a malformed
version (exit 2), and a changelog that is not there (exit 2). An empty range says so in words
rather than printing nothing.

**Asserted, not verified.** That the migrations themselves are applied correctly. They are prose
instructions carried out by a model, so the acceptance test is the pair of checkers, which
constrain the result without constraining the path. A migration that satisfies both checkers
while misreading what a record meant would not be caught by anything here.

**Not verified.** The refusal paths — no git repository, dirty tree, no `docs/architecture/`.
They are instructions in a skill rather than code, so there is nothing to run against them. This
is the same residue as the `--help` routing, and it is why step 1 is written as three named
stops rather than one sentence.

## Installation instructions

**Verified.** That `/plugin install <name>@<marketplace>` is the documented form, by reading the
official marketplace's own instructions rather than relying on convention.

**Asserted, not verified.** That the full install path works end to end on a clean machine. It
has not been performed from scratch by anyone; the plugin was developed in place. This is the
gap that phase P6 closes.

## The language switch

**Verified.** On a copy of a real register: renames through `git mv`, structural translation,
link repair, and a clean checker run in the target language.

**Asserted, not verified.** That a full prose translation preserves meaning across a register of
this size. Only the structural half was rehearsed; the rewriting itself was not performed on all
23 documents.

## Comprehensibility of the documentation

**Not verified, and no mechanism exists.** Six defects were found by one reader in a single pass,
all of them invisible from inside — see OQ-02. Every one passed all mechanical checks.

The only known method is to have somebody outside read it. Carried as OQ-03.
