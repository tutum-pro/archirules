# archirules — meta-rules for running a software project

**Version:** 1.0 · **Canonical language:** Polish. This is a translation of `RULES.md`; **if
the two disagree, the Polish version wins.**

A method developed in practice. **Every rule below exists because its absence broke
something** — not because it sounds good.

The failures the rules came from are described in [`CASEBOOK.en.md`](CASEBOOK.en.md) and
referenced as `C-NN`. The separation is deliberate: **a rule must be readable and usable
without knowing somebody else's project**, while the evidence stays for those who want to know
why it is worded the way it is.

---

## What this is for

A software project rarely loses to hard decisions. It loses to decisions **made silently**: by
the order in which someone touched files, by a default value, by nobody writing down the
alternative. Six months later nobody can say whether something was a choice or an accident.

This method turns decisions, doubts and evidence into **first-class artefacts** — versioned
with the code, reviewed like code, and just as capable of going stale, which is also recorded.

---

## Artefacts

Everything lives in `docs/architecture/`, versioned with the code.

| file | answers |
|---|---|
| `README.md` | what binds **every** piece of work, not just its own area |
| `decisions/ADR-NNNN-*.md` | what was decided, what was not, and at what cost |
| `open-questions.md` | what we do not know yet and what it blocks |
| `fazy-realizacji.md` | what is done, what is next, how we will know it is finished |
| `rejestr-weryfikacji.md` | what is verified, as opposed to asserted |
| `analiza-*.md` | options weighed **before** a decision |

The first three are mandatory from day one. The verification register is started at the first
defect caused by an unverified claim — and it is then obviously needed.

---

## Rules of conduct

### P1. Process before implementation

A project starts from a model of the business process, not from a schema or an API. The model
is a versioned artefact, not a picture in a deck.

In practice: if something cannot be shown on the process model, it is probably not yet clear
what is being built.

### P2. A decision has costs, and they are written down too

Every ADR has a **"Costs, knowingly accepted"** section. Not "risks", not "to consider" —
costs, in the indicative, accepted.

*Why:* a document listing only benefits is not a decision, it is a post-hoc justification. Six
months later, when the cost materialises, the only question is "did we know?". This section is
the answer.

### P3. A rejected option is recorded together with its reason

**"Considered and rejected"** belongs inside the ADR. Without it, someone proposes the
rejected option again and nobody can say why it fell.

### P4. Register the question rather than settling it silently

A doubt with no answer yet gets an **OQ-NN** entry with status, priority and dependencies
(*blocks / depends on / touches*).

*Why:* an unrecorded question gets settled by the order in which someone touches files. That
is a resolution — just one nobody made.

Numbering is **contiguous and free of duplicates**. An OQ number is a public reference; two
questions sharing one make every reference to it ambiguous.

### P5. A phase has an acceptance criterion agreed **before** the work

Not "do persistence", but "**an instance survives a restart and resumes**". A criterion
written afterwards is always met.

### P6. Hard gate

For an approach that is expensive, or reversible only expensively, write the condition for
abandoning it **before** starting: *"if phases B1–B5 do not fit in a week of work, option C was
wrong"*.

*Why:* without a gate agreed in advance, abandoning always looks like failure, so nobody
proposes it.

### P7. A record that stopped being true is corrected in the record

When a document says something that no longer holds, **do not delete the sentence quietly**.
Write that it was untrue for a period, and since when. A superseded ADR gets the status
**Superseded by ADR-NNNN** and stays in the register — it documents the reasoning that led to
the change.

*Why:* a decision register that quietly rewrites the past stops being evidence of anything. A
practical note: **the status field and the notice above it are two different places** — a
correction sitting above a field that still lies is not a correction.
[C-04](CASEBOOK.en.md#c-04--a-decision-register-announced-a-choice-reversed-the-day-before)

---

## Rules of execution

These govern the work itself. **Each comes from a specific failure** — described in the
[casebook](CASEBOOK.en.md).

### W1. Refuse rather than guess

A tool that meets something it does not support **stops loudly** and says what the problem is —
ideally citing a specification, standard or decision.

Silent degradation is worse than refusal because it **looks like success**. A tool that does
less than it was asked and says nothing is indistinguishable from one that did everything.
[C-09](CASEBOOK.en.md#c-09--an-engine-that-executed-less-than-was-drawn)

### W2. Distinguish "not implemented" from "impossible by design"

Two different messages for two different conversations. "Not supported yet" invites a feature
request. "Has no execution semantics and never will" ends the topic.

The same applies to domain boundaries: an unknown operation is a typo and needs the list of
what exists; an operation **deliberately withheld** needs to say **whose rule it is** and where
to go for it.

### W3. Verify, do not assert

A claim about system behaviour is worth exactly the command that demonstrates it. Before
writing "it works" — run it. Before writing "it is safe" — inspect the object, not a reference
to it.

Applies to your **own checking tools** as well: the result of a check is a claim about a
document or about code, so the same rule governs it. Open the file before reporting something
missing.
[C-05](CASEBOOK.en.md#c-05--a-checker-looked-for-the-plural-and-missed-the-singular) ·
[C-08](CASEBOOK.en.md#c-08--a-private-key-survived-the-cleaning-of-the-history)

### W4. A check that cannot fail looks exactly like a check that passes

**A new gate is not finished until it has been shown to fail.** Break it deliberately, run it,
read the error, revert. Record in the commit which shapes of violation it was proven against.

This covers **safety nets** too: a counter that watches whether a check ran at all must be
looser than the check it watches. Tightened along with it, it stops watching anything.
[C-01](CASEBOOK.en.md#c-01--a-gate-that-could-not-fail) ·
[C-06](CASEBOOK.en.md#c-06--changing-one-punctuation-mark-switched-off-thirty-seven-checks) ·
[C-07](CASEBOOK.en.md#c-07--tightening-the-safety-net-blinded-it) ·
[C-11](CASEBOOK.en.md#c-11--a-check-with-no-case-of-its-own-could-not-fire)

### W5. Do not silence errors inside a gate

`2>/dev/null`, `|| true` and an ignored exit status turn a tool failure into a pass. If the
tool failed, **that is itself a violation**.

### W6. A test must not configure the thing it tests

If every test sets a parameter explicitly, none of them checks the default — and the default is
what production uses.

[C-02](CASEBOOK.en.md#c-02--six-tests-passed-with-a-broken-default)

### W7. Run it twice in a row

A first run on clean state says nothing about the second. Tests sharing a database, a directory
or a queue are only exposed by repetition.

[C-03](CASEBOOK.en.md#c-03--a-suite-passed-once-and-failed-on-the-second-run)

### W8. Do not measure your own artefact

Before attributing an observation to the system, check that it does not come from the
measurement, from a stub, or from a neighbouring test. Scope assertions to the thing under
test, not to global state.
[C-10](CASEBOOK.en.md#c-10--measuring-your-own-measuring-instrument) ·
[C-11](CASEBOOK.en.md#c-11--a-check-with-no-case-of-its-own-could-not-fire)

### W9. Mechanism over convention — and when you cannot, name it as a convention

A rule that can be checked mechanically should be. A rule that cannot should be recorded
**explicitly as a review convention**, together with the warning sign by which it is
recognised.

*Why:* a rule pretending to be enforced but not enforced is worse than an explicit convention —
nobody watches it, and everybody assumes somebody else does.

### W10. Library boundary: it computes, it does not reach for the world

A computational core does not touch I/O. What it needs from the world it **declares as an
interface of its own**; the deployment supplies it.

*One-sentence test:* **if a library's tests need a port-forward, the boundary is in the wrong
place.**

---

## Rhythm

1. **Before a phase** — write its acceptance criterion in the phase register.
2. **On meeting a doubt** — an OQ, not an on-the-spot decision.
3. **On making a decision** — an ADR with costs and rejected options.
4. **On building a gate** — prove it fails.
5. **On closing a phase** — evidence, not a claim; two runs.
6. **Periodically** — a completeness audit (`/archirules:audit`).

---

## What this method does **not** do

- **It does not replace code review.** The registers govern decisions, not implementations.
- **It does not survive neglect.** An unmaintained register is worse than none, because it
  looks current. Hence rule P7 and the audit skill.
- **It does not carry mechanical gates between projects.** Concrete checks are code belonging
  to a repository; the method carries the pattern and the checklist.
- **It does not prevent a bad decision.** It only makes a bad decision visible, dated, and
  accompanied by the alternative that was rejected.
