# Phase register

A living document. **Updated whenever a phase completes** — this is where you check what is
done, what is next, and why something is stalled.

**Legend:** `☐` not started · `◐` in progress · `☑` complete · `⛔` blocked

## Track <name>

| | Phase | Status | Acceptance criterion |
|---|---|---|---|
| X1 | <name> | ☐ | <checkable and non-trivial — see below> |

<!-- The criterion must be settleable without discussion:
     bad:  "do persistence"
     good: "an instance survives a restart and resumes"        -->

**Hard gate after <phase>:** if <condition>, then <approach> was wrong.

<!-- The abandonment condition is written BEFORE starting. Without it, abandoning
     always looks like failure, so nobody proposes it. -->

### <phase> — what was delivered

What was built. What design decisions were taken along the way and why. What was deliberately
left out and under which OQ. **What surfaced incidentally** — especially defects found in your
own earlier work.
