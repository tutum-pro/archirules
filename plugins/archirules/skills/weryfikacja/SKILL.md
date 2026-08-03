---
name: weryfikacja
description: Verification discipline — prove a new gate can fail, avoid measuring your own test artifacts, run suites twice. Use when adding a check, a test, or before reporting any measured result.
---

# The discipline of evidence

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
