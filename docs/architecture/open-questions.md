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
