# Phase register

A living document. **Updated whenever a phase completes.**

**Legend:** `☐` not started · `◐` in progress · `☑` complete · `⛔` blocked

## Track — the method as a reusable plugin

| | Phase | Status | Acceptance criterion |
|---|---|---|---|
| P1 | Rules, skills, templates | ☑ 2026-08-03 | a project with no register gets one from `/archirules:bootstrap` |
| P2 | Conformance checker | ☑ 2026-08-03 | **the checker fails on every defect it claims to catch** — proven, not asserted |
| P3 | Bilingual method and a language switch | ☑ 2026-08-03 | the switch rehearsed on a copy of a real register, not on a fixture |
| P4 | The method applied to this repository | ☑ 2026-08-03 | `conform.py` reports zero problems **on this repository's own register** — 60 checks |
| P5 | `--json` output and a CI example | ☐ | a pull request with a malformed register fails its check |
| P6 | A second, unrelated project | ☐ | **someone who did not co-create the method uses it without asking its author how** |
| P7 | Cross-register consistency checker | ☑ 2026-08-11 | **a register built by following `adr/SKILL.md` and the templates literally passes both checkers** — and every marker string either checker keys on is found in a template or a skill, asserted by the self-test rather than by reading |
| P8 | A version users can migrate from | ☑ 2026-08-11 | `claude plugin validate --strict` passes, and **the version in `plugin.json` and the newest `CHANGELOG.md` heading agree** — asserted by the self-test, which fails when one moves without the other |
| P9 | `--help` on every skill | ☑ 2026-08-11 | every skill in `skills/` prints usage naming what it needs and what it will not do, from **one script rather than from the model's memory** — and **a skill added without one turns the self-test red** |
| P10 | Updating a project to a new method version | ☑ 2026-08-11 | **a register created at an earlier version is brought to the current one, both checkers pass, and restoring the snapshot returns the registers byte-identical** — rehearsed on a copy of a real register, not on a fixture |
| P11 | Traceability from registers to commits | ☑ 2026-08-11 | **a commit trailer naming a register entry that does not exist fails the gate**, and the generated traceability section is a faithful regeneration of git history as of the commit it records — byte-compared, not eyeballed |
| P12 | An explanation of the method itself | ☑ 2026-08-11 | **every rule, casebook case, script and skill the text names exists**, and it names no entry from this repository's own registers — both asserted by the self-test, which goes red on an invented reference |
| P13 | Consistency stops the work | ⛔ | **a phase whose blocking question is open cannot be closed, and a register that contradicts itself cannot have a phase opened against it** — proven both ways: the same phase closes cleanly once the question is resolved |

**Hard gate at P6:** if the method cannot be applied by somebody who was not part of writing it,
it is a private working habit and not a method. Publishing it would then be a marketing claim
rather than a description.

**Hard gate at P7:** if aligning the checker with the method turns out to require adding fields
to the templates whose only purpose is to be checked, then the checker was measuring its own
fixtures (rule W8) and the cross-register checks in question are to be **dropped** — the method
does not grow vocabulary to keep a script happy.

**Hard gate at P10:** if the snapshot cannot be restored byte-identical, the skill must
refuse to run at all rather than offer a restore it cannot perform. An update that says it
can be undone and cannot is worse than one that never offered.

**Hard gate at P13:** if the override in OQ-09 turns out to belong outside this plugin — in
the forge, in branch protection, in required reviewers — then this method reads an
authorisation made elsewhere and does not make one. Building a permission system inside a
documentation plugin would be the wrong artefact carrying the wrong responsibility.

### P2 — what was delivered

The checker exists, and so does the proof that it can fail: twenty-one cases across both
languages, each breaking a known-good set in one specific way.

The number matters less than the reason it grew. Every case after the first six was added
because a real defect slipped past the previous version — see
[C-01](../../plugins/archirules/CASEBOOK.en.md#c-01--a-gate-that-could-not-fail),
[C-06](../../plugins/archirules/CASEBOOK.en.md#c-06--changing-one-punctuation-mark-switched-off-thirty-seven-checks)
and [C-07](../../plugins/archirules/CASEBOOK.en.md#c-07--tightening-the-safety-net-blinded-it).

### P3 — what was delivered

`/archirules:language` switches a project end to end. It was rehearsed on a copy of a
23-document register before being trusted, which is where C-06 and C-07 were found.

Deliberately out of scope: translating git history. The current state becomes one language; the
past does not. That limit is stated in the skill rather than discovered by a user.

### P4 — why this phase exists at all

This repository had no register of its own until 2026-08-03. Its decisions — the language split,
the licence, the casebook, the checker's self-test — lived only in commit messages.

That is not a small omission for a project whose entire proposition is that decisions belong in
a register. It was raised, correctly, as self-defeating: a method its author does not apply is
an argument against itself.

The five decision records here were reconstructed from what actually happened, not invented to
fill a template. Each one's rejected alternatives are the alternatives that were really weighed.

**Closed with evidence:** `conform.py docs/architecture` reports `language: en · checks: 60 ·
problems: 0`, exit code 0. This is also the first run of `/archirules:bootstrap` against a
project that was **not** empty — every earlier exercise used either a fresh directory or the
synthetic fixture.

One thing this phase did not settle: whether the register is any good. The checker verifies that
every decision record has a costs section, not that the costs are true. That distinction is the
whole reason [OQ-03](open-questions.md#oq-03--nothing-checks-whether-the-prose-is-understandable)
stays open.

### P7 — what was delivered

A second checker, `consistency.py`, reading the relations **between** registers that `conform.py`
cannot see because every file is well-formed on its own: a question against the phase it blocks,
a phase against the questions it waits on, a closed question that still declares a blocker,
references to decision records, and supersession written in both directions.

**Closed with evidence.** The criterion was checked literally rather than in spirit. A register
built by following `adr/SKILL.md` word for word — a decision reversed, the old record given the
status line the skill prescribes — was constructed and run through both checkers:

```
conform.py      language: en · checks: 93 · problems: 0                exit 0
consistency.py  language: en · cross-register checks: 59 · problems: 0  exit 0
```

**The same construction produced `exit 1` before this phase**, which is the entire reason the
phase exists. Its second half is asserted by `selftest.sh`, whose last case requires every
marker string either checker keys on to occur in a template or in a skill; run against the
scripts as they were, it named six markers with no documentary source at all.

This repository's own register: `conform.py` 85 checks, `consistency.py` 52 cross-register
checks, zero problems, identical on two consecutive runs (rule W7). Self-tests: 34 and 41 cases,
all passing, twice. One finding on the way to that: the checker rejected a sentence **in this
phase's own decision record** that referred to a record number the register does not contain.

**Design decisions taken along the way.** The two scripts were given a stated axis — inside one
file, between files — and the supersession-scope check was moved to `conform.py` to respect it,
at the cost of a second fixture set. The reasoning, and the four alternatives that fell, are in
[ADR-0006](decisions/ADR-0006-checker-speaks-the-methods-vocabulary.md).

**The hard gate fired once**, on the blocker table. Two cross-register checks need one, no
template produces one, and adding it would have meant growing the method to keep a script happy.
Nothing was added; the question is
[OQ-06](open-questions.md#oq-06--should-the-blocker-table-be-part-of-the-method-or-stay-a-project-convention).
The limit of the closed-question check is
[OQ-05](open-questions.md#oq-05--is-a-stale-blocker-findable-anywhere-except-the-questions-own-field).

**What surfaced incidentally — the valuable part.** All of it was defects in this phase's own
first draft, and none of it was visible from reading:

- **A check that could not fire in any circumstance**, in either language, advertised in the
  audit skill as mechanised. It was the only one of the five without a self-test case of its
  own. Twenty-eight passing cases said nothing about it —
  [C-11](../../plugins/archirules/CASEBOOK.en.md#c-11--a-check-with-no-case-of-its-own-could-not-fire).
- **A self-test that measured its own fixtures.** The checker and the fixtures agreed because
  the same invention wrote both, while a register built from the instructions was rejected.
- **Reference checks that vanished silently** when a set kept no `decisions/` directory — in a
  script whose own docstring promised that skips are printed.
- **`--lang pl` silently ignored** because only the `--lang=pl` spelling was parsed, in a
  checker whose sibling documents the spaced form. Silent degradation looks like success.
- **A forced language that contradicts the register's own README** switched every check off
  without a word. The language skill already asked a human to confirm this; it is now mechanised
  in both checkers.
- **Two defects in the new gates themselves**: a `grep` pipeline where `pipefail` let the
  checker's exit code outrank the match, so cases reading output reported "printed nothing"; and
  a vocabulary assertion that passed when the module it measures failed to import, because an
  empty result read as "nothing missing".

### P8 — what was delivered

An explicit `version` in `plugin.json`, a `CHANGELOG.md` inside the plugin, and a self-test case
requiring the two to agree. The reasoning and the four rejected alternatives are in
[ADR-0007](decisions/ADR-0007-explicit-version-as-the-migration-anchor.md).

**Closed with evidence.** Both halves of the criterion, checked literally:

```
claude plugin validate ./plugins/archirules --strict   ✔ Validation passed
selftest.sh   ok  plugin version and changelog agree   1.1.0
```

Before this phase the same validation reported `version: No version specified` and passed only
with warnings — `--strict` turns that into a failure, which is why the criterion names it.

**Shown to fail, in four directions** rather than one, because a version check has more than one
way of being wrong:

| broken how | what the gate says |
|---|---|
| version bumped, changelog not | `plugin.json says 1.2.0, newest CHANGELOG heading is 1.1.0` |
| changelog bumped, version not | `plugin.json says 1.1.0, newest CHANGELOG heading is 1.2.0` |
| version field removed | `plugin.json declares no version` |
| changelog missing entirely | `unreadable: No such file or directory` |

The fourth matters most and is the reason the check prints a sentinel instead of returning an
empty result. An assertion that goes quiet when the file it reads disappears is the defect
recorded as C-11 in the casebook, and it was introduced and fixed once already in P7.

**A design decision along the way.** `CHANGELOG.md` lives in the plugin root, not the repository
root. Only the plugin directory is distributed, so a changelog outside it would be invisible to
every installed user — and to `/archirules:update`, which reads it. The gate would then have
passed here and been unrunnable everywhere else.

**Deliberately not done:** git tags. The version, the changelog heading and a tag would be three
places for one fact, and Claude Code reads none of the third.

### P9 — what was delivered

`--help` on all seven skills. `scripts/help.py` extracts a `## Usage` section from the skill's
own `SKILL.md`; the skill's only job is to route `--help` to it. Reasoning and four rejected
alternatives in [ADR-0008](decisions/ADR-0008-help-comes-from-a-file-not-from-memory.md).

**Closed with evidence.** Both halves of the criterion. Every skill answers:

```
selftest.sh   ok  every skill answers --help from the script   7 skills
```

And the second half — a skill added without usage turns the self-test red — checked by actually
adding one, not by reading the code:

| broken how | what the gate says |
|---|---|
| a new skill dropped in with no usage | `newthing: no ## Usage section` |
| the section renamed in an existing skill | `oq: no ## Usage section` |
| the routing line broken | `phases: SKILL.md does not route --help to help.py phases` |
| usage naming another skill in its invocation | `adr: its usage names another skill` |
| `help.py` made unimportable | one line per skill: `help.py prints nothing usable (exit 1)` |

The fourth is the one worth having. A usage block copied from a neighbouring skill reads
perfectly and sends the reader to the wrong command; nothing about it looks wrong.

**A design decision along the way.** Usage is written for a person and the rest of `SKILL.md`
for the model that executes it. They stay in one file under separate headings, so they cannot
drift into two documents that disagree. Every usage block states a **"Will not"** — a skill's
limits are what a reader cannot infer and what costs them an afternoon.

**Deliberately not done:** an eighth `/archirules:help` skill. It would answer "what skills are
there", which `/help` already answers, rather than "what does this one need from me". The
listing survives as `help.py` with no argument.

**What this does not guarantee.** The routing is a sentence a model reads, so it remains
probabilistic — nothing in the plugin system can make it otherwise. What the mechanism
guarantees is that routing correctly produces a current answer. And the "Will not" lines,
the most useful part of the text, are prose that nothing verifies. Both are stated in the
record rather than left for a user to discover.

### P10 — what was delivered

`/archirules:update`, `scripts/migrations.py`, and `.archirules-version` written by
`/archirules:bootstrap`. The boundary against the plugin manager, and the four rejected
alternatives, are in
[ADR-0009](decisions/ADR-0009-updating-a-project-is-not-updating-the-plugin.md).

**Closed with evidence, rehearsed on a real repository.** A git repository was created holding a
register written in the 1.0.0 vocabulary — a supersession status with a bare pointer, and
`Modifies:` where the method says `Supersedes:`. The procedure was then executed step by step:

```
before   conform.py       problems: 1   x ADR-0001: status says SUPERSEDED but names no scope
         consistency.py   problems: 0

after    conform.py       language: en · checks: 31 · problems: 0        exit 0
         consistency.py   cross-register checks: 11 · problems: 0        exit 0

restore  git diff --stat <snapshot> -- docs/architecture   (no output — byte-identical)
```

The "before" line matters as much as the "after": it shows the migration was needed, so the
"after" is not a register that would have passed anyway.

**The rehearsal found a defect in this phase's own instructions.** The restore command was
`git restore --source=<snapshot> -- docs/architecture`, which is what anyone would write and is
wrong. It puts tracked files back and leaves whatever the migration **added** — here
`.archirules-version`. The register came back in its 1.0.0 shape still claiming to be 1.2.0:
undone in content, not undone in what it says about itself. Checksums differed; the naive
restore produced `a796ddb8…` against a target of `e4a070cc…`.

Corrected to `rm -rf docs/architecture` followed by the restore, which is byte-identical. That
command is only safe because step 1 refuses to start on a tree with untracked files — the two
steps are one mechanism, and the skill says so where someone editing it will see it.

**The hard gate held.** It required that a snapshot which cannot be restored byte-identical
means the skill must refuse to run rather than offer a restore it cannot perform. The first
draft was in exactly that state. It was fixed rather than the gate being relaxed.

**Deliberately not done:** deleting snapshot branches, migrations as executable scripts, and any
attempt to update the plugin from inside the skill. The second is the interesting one — a script
cannot ask what a record meant, and one that guessed would produce a register satisfying the
checker while saying something its author never said.

### P11 — what was delivered

Traceability from register entries to the commits implementing them: trailers in commit
messages, `scripts/trace.py` deriving the mapping, and a generated `traceability.md`. The
reasoning and four rejected alternatives are in
[ADR-0010](decisions/ADR-0010-traceability-derived-from-git-trailers.md).

**Closed with evidence.** Both halves of the criterion, proven against a throwaway git
repository built by the self-test — a fixture directory could not serve, because the thing under
test is what history says and a fixture has no history:

| broken how | outcome |
|---|---|
| a trailer naming an entry no register holds | `Archirules-Phase: T9 names T9, which is not in the register` |
| the generated view edited by hand | `not a faithful regeneration at 5c744d0` |
| the view deleted | `traceability.md does not exist` |
| the view's "generated at" line removed | `records no commit it was generated at` |
| a trailered commit newer than the view, `--strict` | reported, exit 1 |
| an unknown option, or a directory outside a repository | exit 2 |

Usage errors exit 2 throughout, so a broken invocation cannot be read as a finding about a
register.

**The design problem worth recording.** The obvious check — regenerate and compare against
`HEAD` — cannot ever pass: the commit that writes the view cannot contain its own identifier, so
the file is stale the instant it is committed. A gate nobody can satisfy is a gate everybody
switches off. The view therefore records the commit it was generated at and is checked against
**that**, and the working pattern is: commit the work with trailers, regenerate, commit the view
in a commit carrying no trailer.

**Two checks are behind `--strict` and that is deliberate.** A closed phase no commit claims, and
a view behind HEAD. This repository cannot satisfy either: P1 to P10 closed before the mechanism
existed and their history is already pushed. Shipping them as defaults would mean a gate failing
on day one for reasons nobody can fix. Carried as
[OQ-07](open-questions.md#oq-07--when-should---strict-traceability-become-the-gate-rather-than-an-option).

**What surfaced incidentally.** Extending the vocabulary assertion to `trace.py` immediately
went red on all three trailers: they existed in the script and in no skill. That is the same
defect ADR-0006 was written for, caught this time by the mechanism rather than by a user — which
is the first evidence that the assertion works on something other than the case it was built
from.

### P12 — what was delivered

`/archirules:help` — an explanation of the method rather than a listing of skills. Reasoning and
four rejected alternatives in
[ADR-0011](decisions/ADR-0011-a-skill-that-explains-the-method.md).

**Closed with evidence.** The criterion had a mechanical half and it was checked by breaking it
six ways, not by reading the text:

| broken how | what the gate says |
|---|---|
| an invented casebook case | `names C-99, which is not in the casebook` |
| a rule identifier that was never written | `names rule P9, which is not in RULES.en.md` |
| a script renamed | `names conformance.py, which is not in scripts/` |
| a skill that does not exist | `names /archirules:setup, which is not a skill` |
| a reference to this repository's registers | `names ADR-0004 — this repository's own register` |
| the casebook removed so the check cannot run | `unreadable: No such file or directory` |

**What the gate does and does not claim.** It verifies that the text is not made of things that
are not there. It does not verify that the text is true. The distinction matters because the
sentences worth most in that skill — what the method costs, what it does not do, how much
evidence exists — are prose, and prose is where an untrue explanation would actually live. Said
in the record rather than left to be assumed.

**A record was corrected, not overwritten.**
[ADR-0008](decisions/ADR-0008-help-comes-from-a-file-not-from-memory.md) had rejected a skill of
this name and stated flatly that none existed. The rejection still holds for what it rejected —
a skill listing the other skills — and the sentence that stopped being true was corrected inside
the record with the date and the reason, per rule P7. Its implementation status said "all seven
skills" and now says seven when written, nine since.

**What surfaced incidentally.** Writing the register-reference rule made it obvious that
`audit/SKILL.md` and `verification/SKILL.md` already break it: they cite this repository's
`ADR-0006`, `OQ-05` and `OQ-06` as justification, and nobody installing the plugin has those.
The new skill is held to the rule and the older ones are not, which is a rule enforced in one
file and ignored in four — the shape rule W9 warns about. Registered as
[OQ-08](open-questions.md#oq-08--skills-cite-this-repositorys-own-registers-which-a-reader-of-the-plugin-cannot-resolve)
rather than left as an acceptable inconsistency.
