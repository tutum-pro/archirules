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

**Hard gate at P6:** if the method cannot be applied by somebody who was not part of writing it,
it is a private working habit and not a method. Publishing it would then be a marketing claim
rather than a description.

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
