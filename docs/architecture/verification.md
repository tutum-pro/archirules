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
