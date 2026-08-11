# Architecture — decision register

Reference set for `consistency.py`. Holds one instance of every relation **between**
registers the checker looks at: a question blocking a phase, a phase waiting on a
question, a record superseded in part, a record superseded in whole, and a record
with no links at all.

Every field here is one a template produces or a skill prescribes. A fixture written in
vocabulary of the checker's own invention proves the checker consistent with the
fixture and nothing else — see the record on checker vocabulary in this plugin's own
architecture register.

The neighbouring `valid-en` set is too small for this — one decision record and no
blocker table, so the checker passes over it without running a single cross-register
check.

| ADR | Topic | Status |
|---|---|---|
| [0001](decisions/ADR-0001-base.md) | Base | SUPERSEDED in part by 0003 |
| [0002](decisions/ADR-0002-superseded.md) | Abandoned variant | SUPERSEDED by 0003 |
| [0003](decisions/ADR-0003-modification.md) | Reaches back to 0001 and 0002 | Accepted |
| [0004](decisions/ADR-0004-unconnected.md) | Record with no links | Accepted |

## Binding requirements

None. This heading has to be here — the checker reads the set's language from it.

See the [phase register](phases.md) and the [open questions](open-questions.md).
