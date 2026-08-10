# Open questions

Numbering is contiguous and free of duplicates. A number is a public reference.

### OQ-01 — Is an MCP server worth adding
**Status:** OPEN · **Touches:** [ADR-0005](decisions/ADR-0005-distribution-as-a-plugin.md)

Everything the method does — read files, run a checker, write documents — is already possible
with the built-in file and shell tools. An MCP server would wrap `python3 conform.py` in a
protocol: a layer, not a capability, and it would cost the property that this plugin starts no
processes and installs nothing.

The state involved is files in the user's own repository, deliberately so. There is no remote
system to reach, which is what the MCP servers in the public catalogue are actually for.

**One scenario would change the answer:** queries *across* projects — "every critical open
question in all my repositories", "which projects have superseded decisions still marked
current". Files and `grep` do not give that cheaply; an indexing server would. That is a
capability rather than a wrapper.

**To resolve:** whether several unrelated projects are using the method. Today there is one, so
the question cannot be answered honestly yet. Revisit when there are three.

**Cheaper first:** `conform.py --json` for structured results, and a CI workflow example. Most
of the practical value, a fraction of the cost. Recorded as phase P5.

### OQ-02 — How do we learn what a newcomer cannot understand
**Status:** RESOLVED → [ADR-0003](decisions/ADR-0003-casebook-apart-from-rules.md), 2026-08-03

**The answer: only by asking somebody who was not there.** The author cannot test their own
documentation on themselves.

Six defects were found by a reader in a single pass, none of them visible from inside: no
getting-started path, source-project context assumed in comments, Polish descriptions in plugin
metadata, a Polish landing page under English metadata, unexplained naming in the install
command, and Polish skill names. All obvious once pointed at.

The structural half of the answer is ADR-0003. The procedural half has no mechanism yet and is
carried by OQ-03.

### OQ-03 — Nothing checks whether the prose is understandable
**Status:** OPEN · **Priority: medium** · **Depends on:** OQ-02

`conform.py` checks structure. Structure was never the problem — the six defects in OQ-02 all
passed every mechanical check, because a document can be perfectly well-formed and still
assume knowledge the reader does not have.

There is no known mechanical check for this, and inventing a weak one would be worse than
having none: it would create the impression that comprehensibility is covered.

**To resolve:** whether anything cheap exists beyond "have somebody outside read it". Candidates
worth trying rather than assuming: flag references to proper nouns that appear nowhere else in
the repository; flag skills that mention a concept absent from `RULES.md`. Both are heuristics
and would need the treatment in
[ADR-0004](decisions/ADR-0004-checker-ships-with-its-own-proof.md) before being trusted.

### OQ-04 — Will the two language versions drift
**Status:** OPEN · **Touches:** [ADR-0001](decisions/ADR-0001-language-split.md)

The Polish original wins by rule, which settles disagreements but does not prevent them. Today
the translation is fresh; the risk is a Polish edit that never reaches the English side, leaving
a reader of the translation with a rule that no longer holds.

Mitigation in place is structural, not procedural: reasoning is concentrated in `RULES.md` and
the templates are deliberately thin, so there is less surface to drift.

**To resolve:** whether a check is possible at all — comparing section counts and heading
structure between `RULES.md` and `RULES.en.md` would catch a whole section added on one side
only, though not a changed sentence. Worth doing if the pair ever diverges in practice; there
is no evidence yet that it will.

### OQ-05 — Is a stale blocker findable anywhere except the question's own field
**Status:** OPEN · **Touches:** [ADR-0006](decisions/ADR-0006-checker-speaks-the-methods-vocabulary.md)

`consistency.py` check C reads one thing: a question whose status is no longer OPEN while its
own `Blocks:` field is still filled in. That is a **field**, so the check is exact — no prose is
searched and nothing is inferred.

Its predecessor tried to be general, searched for a marker and a question number on one line,
and could not fire at all. The narrow version is the deliberate reaction to that, and the
question is whether narrow is enough.

The wider reading would search prose: a phase register saying *"held up by OQ-02"*, a decision
record explaining what it waited for. Both are places a stale blocker can hide. Both are also
places where the past tense is correct writing — *"this waited on OQ-02 until it was
resolved"* — and a check that reports that sentence as a defect costs more trust than the
defect it catches.

**If left unresolved:** a blocker recorded only in prose stays stale without anything noticing.
The field version catches the case the templates actually produce, which is the common one.

**To resolve:** whether the past-tense case is routine or rare, settleable by counting rather
than by argument — run the wider pattern over a register with real history and read every hit.
No false positives, or one, and the check widens; routine ones, and the narrow version stands
and gets recorded as a review convention (rule W9). Needs a register with a history longer than
this one's.

### OQ-06 — Should the blocker table be part of the method or stay a project convention
**Status:** OPEN · **Touches:** [ADR-0006](decisions/ADR-0006-checker-speaks-the-methods-vocabulary.md)

Two of the cross-register checks — a question's `Blocks:` against the phase register, and a
phase's blockers against the questions they name — can only run when the phase register keeps a
"what blocks" table. No template produces one. Where there is no table, the checks are skipped
and the skip is printed.

So the method has a rule that only some projects can have enforced. Rule W9 says that is
exactly the situation to name rather than to leave ambiguous, and it is named — but naming it
is not the same as deciding it.

**If left unresolved:** most registers keep two of the five cross-register checks permanently
switched off and see a `~ skipped` line they have no instruction for.

**To resolve:** whether the table earns its cost on a register that is not this one. It is
duplicated state — the same fact written in the question and in the phase register — and
duplicated state is what the checker exists to police. Worth deciding once a phase register
other than this repository's has been kept for long enough to say whether blockers drift.
Depends on the same evidence as [OQ-01](#oq-01--is-an-mcp-server-worth-adding): more than one
project using the method.
