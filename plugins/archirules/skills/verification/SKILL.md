---
name: verification
description: Verification discipline — prove a new gate can fail, avoid measuring your own test artifacts, run suites twice. Use when adding a check, a test, or before reporting any measured result.
---

# The discipline of evidence

**`--help`** — if `$ARGUMENTS` is `--help`, run
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/help.py verification`, show its output, and stop there.

## Usage

```
/archirules:verification [--help]
```

The discipline for anything that claims to check something: prove the gate can fail before
trusting it, and give every check a case of its own.

**Needs from you:** the check you are about to add or the result you are about to report.

**Will not:** accept "the tests pass" as evidence. A gate that has never been seen to fail looks
exactly like one that passes.

**The rules it applies:** break it deliberately and watch it go red; never silence an error
inside a gate; run the suite twice; and do not measure your own test artefact — a self-test that
agrees with fixtures written by the same hand proves only that.

### Examples

```
/archirules:verification
/archirules:verification I added a check that rejects an empty config
/archirules:verification the suite is green — can I report the phase done
```

The second form walks you through breaking the check on purpose and watching it go red. The
third one is the question this skill exists to answer with something other than yes.

## A new gate is not finished until it has been shown to fail

The procedure, every time:

1. Run it on a clean tree — it must pass.
2. **Break it deliberately**, in every shape of violation the gate claims to catch.
3. Run it — it must fail, with a readable message and a **non-zero exit code**.
4. Undo the damage, run it — it must pass.
5. Record in the commit which shapes it was proven against.

*Why:* an architecture gate twice reported "clean" against a deliberately broken library. Once
because a regex required leading whitespace — it saw grouped imports and missed single-line
ones. Once because `2>/dev/null` turned a tool error into an empty result read as success.

**A check that cannot fail looks exactly like a check that passes.**

Worked example in this plugin: `scripts/selftest-consistency.sh`. Each class of defect
`consistency.py` claims to catch is introduced into a copy of a reference set and must produce
exit 1; the untouched copy must produce 0. Several cases assert the opposite — a reworded
heading, an absent blocker table, a missing `decisions/` directory are **not** findings —
because a checker that reports a sound set as broken fails in the direction nobody tests for.

**Give every check a case of its own.** One check here had none: it was covered incidentally by
whatever else its fixtures happened to trigger, and it turned out to be incapable of firing at
all — under any input, in either language. A full green self-test said nothing about it. See
C-11 in the casebook.

**A passing self-test is evidence about the fixtures, not about the world.** The same checker
was consistent with test data written in vocabulary it had invented, while rejecting a register
built by following this method's own instructions. The assertion that now prevents that is the
only one in the file that leaves the fixtures: every marker string a checker keys on must occur
in a template or a skill.

The self-tests are themselves checked the same way, by replacing each checker with one that
always returns 0:

| self-test | cases | fail under an always-green checker | survive |
|---|---|---|---|
| `selftest-consistency.sh` | 41 | 24 | 17 |
| `selftest.sh` | 34 | 22 | 12 |

The survivors are exactly the cases that do not assert "exit 1": those expecting exit 0, those
reading printed output, and those expecting a usage error. **Re-derive these numbers whenever a
case is added** — a self-test is a gate too, and a table copied forward is a claim.

Both figures were measured, and measuring them is what found the next defect: the vocabulary
assertion passed while the checker it measures failed to import at all, because an empty result
read as "nothing missing". An assertion about a tool's output has to distinguish *I found
nothing* from *I could not run* — print a sentinel, never an empty string.

## Do not silence errors inside a gate

`2>/dev/null`, `|| true`, an ignored exit status. If the tool failed, **that is itself a
violation**, not an absence of violations.

## Check the default path

If every test configures the parameter under test, **none of them checks the default** — and
the default is what production uses. Add at least one test that takes the object with no
options.

Normalise configuration **after** applying options, not only before, or an absurd value passed
from outside reintroduces the same defect through a different door.

## Run it twice in a row

A first run on clean state says nothing about the second. Shared state — a database, a
directory, a queue — is only exposed by repetition.

Scope assertions to **the thing under test**. A global counter will also count somebody else's
work.

## Do not measure your own artefact

Before attributing an observation to the system, check that it does not come from a stub, from
the measurement itself, or from a neighbouring test.

*Failure:* a phantom memory leak turned out to be an artefact of the test; a throughput ceiling
turned out to be the test's own timer.

## A clock-dependent test is a test of the clock

If an assertion depends on something completing inside a time window, **remove the time**.
Expire leases explicitly, inject the clock, advance it in the test. A sleep in a test measures
the network.

## Reporting

Give the command and its output, not the conclusion. When a test failed, show the output. When
something was skipped, say so. When it is done and verified, say it plainly, without hedging.
