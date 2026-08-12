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

### OQ-07 — When should `--strict` traceability become the gate rather than an option
**Status:** OPEN · **Touches:** [ADR-0010](decisions/ADR-0010-traceability-derived-from-git-trailers.md)

`trace.py` always reports two things: a commit trailer naming a register entry that does not
exist, and a generated view that is not a faithful regeneration. Two more are behind `--strict`:
a closed phase no commit claims, and a view behind HEAD.

They are optional because this repository cannot satisfy them. Phases P1 to P10 closed before
the mechanism existed, so their commits carry no trailers and never will — history that is
already pushed. A gate that fails on day one for reasons nobody can fix is a gate people learn
to pass with `|| true`.

**If left unresolved:** the interesting half of traceability stays advisory. Nothing stops a
phase being closed with no commit behind it, which is the case the mechanism was built for.

**To resolve:** whether the untraced list actually shrinks. It is printed in `traceability.md`
under its own heading and can only shrink, never grow — P1–P10 are the whole of it. Once every
phase closed after this point carries a trailer, `--strict` costs nothing to switch on, and the
question becomes what to do about the ten historical entries: exempt them by name, or accept a
gate that names them every run. Revisit at P5, when a CI example has to decide which command it
runs.

### OQ-08 — Skills cite this repository's own registers, which a reader of the plugin cannot resolve
**Status:** OPEN · **Touches:** [ADR-0011](decisions/ADR-0011-a-skill-that-explains-the-method.md)

`audit/SKILL.md` and `verification/SKILL.md` point at `ADR-0006`, `OQ-05`, `OQ-06` and `C-11` as
justification for how a check behaves. Those entries live in **this** repository's registers,
which nobody who installs the plugin has.

It is a small violation of a binding requirement here — a rule must be usable without knowing
this project's history — and the reason the casebook was split from the rules in the first
place. The casebook references (`C-NN`) are fine: the casebook ships with the plugin. The
register references are not.

The new help skill is held to the rule mechanically and the older ones are not, because
enforcing it everywhere would turn the self-test red today with no time to fix it properly.
A rule enforced in one file and ignored in four is exactly the "pretends to be enforced" shape
rule W9 warns about, so this cannot stay as it is.

**If left unresolved:** a reader following a justification in a skill hits a dead reference and
learns that the plugin's documentation cites things it does not ship.

**To resolve:** nothing needs to be known — this is work, not a doubt about direction. Each
citation is either replaced by the reasoning itself, moved into the casebook where it ships, or
dropped. The question exists to hold it visibly rather than let it pass as acceptable. Close it
by extending the reference check to every skill and making them all pass.

### OQ-09 — How does somebody with authority sanction breaking the consistency rule
**Status:** OPEN · **Priority: high** · **Blocks:** P13 · **Touches:** [ADR-0012](decisions/ADR-0012-work-stops-on-a-contradicted-register.md)

[ADR-0012](decisions/ADR-0012-work-stops-on-a-contradicted-register.md) stops work on a register
that contradicts itself or on a phase whose blocking question is unanswered. Sometimes that stop
is wrong — a release is time-critical, the contradiction is cosmetic, the blocking question turns
out not to bear on the work after all. A lead, an architect or a project manager needs a way to
say "proceed anyway" that the mechanism honours.

**What is not known:** where the sanction lives so that it is both durable and hard to forge.
Candidates, none of them evaluated yet:

- **A commit trailer**, `Archirules-Override: <who> — <reason>`, in the same shape as the
  traceability trailers. Cheap and versioned. But a trailer is typed by whoever writes the
  commit, so it records a claim about who approved, not an approval.
- **A signed commit or tag.** Git can verify who, cryptographically. It cannot verify that the
  signer is entitled to override, which is OQ-10, and it requires every approver to keep a key.
- **An entry in the register itself** — a dated record naming what was overridden and why, which
  the gate reads. Auditable and readable, but a person who can edit the register can grant
  themselves the override, so it protects nothing on its own.
- **Outside the repository entirely** — a CI approval, a protected branch, a review requirement.
  The only place where the mechanism is genuinely not the thing being overridden, and the only
  one this plugin cannot ship.

**If left unresolved:** the rule in ADR-0012 cannot ship at all. A gate with no sanctioned way
past it is removed the first time it is wrong, and the removal takes the whole mechanism, not the
one case that was mistaken. This is why the question blocks P13 rather than being noted as a
future improvement.

**Three properties the answer has to have**, whatever it turns out to be. They are already
clear, so they are recorded now rather than rediscovered later:

1. **The override leaves a record**, naming who, when and why — an override nobody can find
   afterwards is indistinguishable from the rule not having existed.
2. **It is per-occurrence, not a mode.** A switch that turns the rule off stays off.
3. **It cannot be granted by the person it unblocks**, or it is not an override, it is a comment.

**To resolve:** whether this plugin should carry it at all. The honest possibility is that
authorisation belongs to the forge — branch protection, required reviewers — and that archirules
should read a decision made there rather than make one. Settle it before designing a mechanism,
because the answer decides whether there is a mechanism to design.

### OQ-10 — How is the list of people who may sanction it defined and protected
**Status:** OPEN · **Priority: high** · **Blocks:** P13 · **Depends on:** OQ-09 · **Touches:** [ADR-0012](decisions/ADR-0012-work-stops-on-a-contradicted-register.md)

If an override needs authority, something has to say who has it. That list is the mechanism's
weak point: whoever can edit it can grant themselves the right to bypass every consistency rule
in the project.

**What is not known:** where a list of approvers can live such that editing it is harder than
the thing it guards. The tension is exact — a file in the repository is versioned, reviewable and
readable, and can be edited by anyone who can commit, which is everybody the rule applies to.

Candidates, none evaluated:

- **A file in the repository** (`docs/architecture/approvers.md` or similar). Auditable, in the
  same review flow as everything else, and self-serving to edit. Would need the forge to protect
  that path — which puts the real protection outside the plugin again.
- **The forge's own roles** — a GitHub team, a `CODEOWNERS` entry, branch protection. Already
  administered, already outside a contributor's reach, and not portable: it exists only where the
  project is hosted, and the plugin cannot read it without becoming a client of one forge.
- **Signature keys**, with the list being "whoever holds a key in this set". Moves the problem to
  key distribution and revocation, which is heavier than most projects will accept.
- **No list at all** — any human approval counts, and the record of who approved is the control.
  Weakest technically, and possibly correct: it makes the override auditable rather than
  restricted, and social consequence does the rest.

**If left unresolved:** OQ-09 has no answer either, and P13 stays blocked. This question is the
harder of the two, because the first is about a mechanism and this one is about who guards the
guard.

**To resolve:** first, whether a protected list is needed at all. The last candidate deserves a
serious hearing rather than dismissal: on a team where everyone can already push, a list that
everyone can edit protects nothing, and an override that is merely **visible** may protect more.
Answering that settles whether the remaining work is design or nothing.

Also needed: whether roles belong in this method at all. Nothing in `RULES.md` mentions a lead, an
architect or a project manager, and every artefact so far is role-blind — a decision is a decision
whoever wrote it. Introducing authority would be the first exception, and that is a change to the
method, not a feature of a checker.

### OQ-11 — Where does an external fact live when it is neither a decision nor a doubt
**Status:** OPEN · **Touches:** [ADR-0013](decisions/ADR-0013-a-register-earns-its-existence-by-a-defect.md)

A vendor deprecates a library. A regulation changes. A budget moves. The fact constrains the
project, is nobody's decision, and raises no doubt that anyone has yet phrased as a question.

Today it lives in exactly one place: the `## Context` of whichever decision record it forced. If
it forced none yet, it lives nowhere, and six months later the reason a constraint exists is
reconstructed from memory — which is the failure this whole method addresses, occurring inside
the method.

This is the one real gap that survived the analysis rejecting the CHR and Errors registers
([ADR-0013](decisions/ADR-0013-a-register-earns-its-existence-by-a-defect.md)). It is recorded
because it survived, not because a register is the answer.

**Candidates, none yet evaluated:**

- **Nothing new.** An external fact nobody has acted on is arguably a doubt — *what do we do
  about this* — and belongs here as an OQ. Costs nothing, and may be the whole answer.
- **`analiza-*.md`**, which the artefact table already allows for material weighed before a
  decision. Exists, is unused in this repository, and may be the intended home.
- **A section of the index**, alongside the binding requirements: facts that constrain every
  piece of work, which is what that file is for.
- **A register of its own** — which ADR-0013 permits only against a named defect, and this
  question is precisely the search for one.

**If left unresolved:** nothing breaks visibly, which is the difficulty. A constraint whose
origin was never written down is only discovered when somebody proposes violating it and cannot
be told why they should not.

**To resolve:** find one. A single external fact, in this or another project, whose origin is
already unreconstructible. That is the standard ADR-0013 sets for any new artefact, and this
question is held to it as strictly as the proposal it came from. If none can be produced, the
first candidate wins by default and the question closes as "an OQ is enough".

### OQ-12 — Nothing explains how to write in the verification register
**Status:** OPEN

The method has four registers. Three of them have a skill that explains how to keep them:
`/archirules:adr` for decision records, `/archirules:oq` for open questions,
`/archirules:phases` for the phase register.

The fourth is the verification register — the document that separates what has actually been
**demonstrated** from what is merely **claimed**. It has no such skill.

`/archirules:verification` sounds like it would be that skill. It is not. It teaches a working
discipline — break a check on purpose and watch it fail before you trust it — and it never
mentions the register at all. That was checked, not assumed: the file contains no reference to
the verification register anywhere in it.

So somebody starting a verification register has nothing to follow, and invents a shape.

**This has already happened here, and it can be counted.** This repository's own verification
register holds **37 entries across 11 subjects**, written during a single working session with
the format made up as the work went along. The labels have already drifted inside that one file:

| label written | times |
|---|---|
| Verified. | 22 |
| Asserted, not verified. | 7 |
| Not verified. | 2 |
| Not verified, and no mechanism exists. | 2 |
| Not verified, and no mechanism is claimed. | 1 |
| Not traceable, permanently. | 1 |

Three different wordings for "not verified" in one document is not a matter of style. A reader
cannot tell whether the three mean the same thing or three different things, and no checker can
be written against them either.

**One of those labels matters more than the others.** "Asserted, not verified" is the entry that
says: *we believe this, we have not shown it, and we are telling you so.* It is the most useful
line in the register and the easiest to leave out, because writing it means admitting a gap out
loud. Nothing in the method tells a newcomer that this kind of entry exists, let alone that it is
expected.

**If this stays unresolved:** every project that starts a verification register invents its own
shape. The registers cannot be compared with each other, nothing can ever check them, and the
"asserted, not verified" line — the one worth having — will usually be missing, because nobody
was told to write it.

**To resolve** there is one real question and one piece of work.

The question: does keeping this register belong to the existing `/archirules:verification`
skill, or to a skill of its own? Both have a cost. Folding it in means one skill doing two jobs,
under a name that already misleads people about which job it does. Splitting it out means an
eleventh skill, which is one more thing to learn before finding the one you wanted.

The work, needed either way: write down what an entry looks like — which labels exist, what each
one means, and the fact that "asserted, not verified" is a normal, expected entry rather than a
confession of failure.

The question is settleable by doing the work first. Draft the entry format, then see whether it
fits inside the existing skill without turning it into two documents stapled together. If it
does, fold it in; if it does not, that is the answer.
