# Phase register

**Legend:** `☐` not started · `◐` in progress · `☑` done · `⛔` blocked

| | Phase | Status | Acceptance criterion |
|---|---|---|---|
| X1 | The reference set exists | ☑ | `consistency.py` exits 0 on this directory |
| X2 | Phase waiting on a resolution | ⛔ | not startable while OQ-01 stays open |

### What blocks the phases of path X

| phase | blocker |
|---|---|
| X1 | — nothing |
| X2 | [OQ-01](open-questions.md#oq-01--is-the-blocker-table-kept-together-with-the-phase-table) — while it is open, the phase does not start |

**Hard gate:** if this set stops passing, the checker has changed its behaviour.
