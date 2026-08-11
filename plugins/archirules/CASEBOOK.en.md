# Casebook — where the rules came from

Every rule in [`RULES.md`](RULES.md) came out of a specific failure. The failures are collected
here, separately, for three reasons:

1. **A rule has to be readable without them.** Someone reaching for a method wants to know what
   to do, not to learn somebody else's project.
2. **The evidence has to stay.** A rule without its failure is a wish; with it, it is a
   conclusion. Deleting the cases would remove the only reason to follow the rules.
3. **A case is recognisable in your own work.** The point is not to know what happened
   elsewhere, but to see the same shape at home.

All of them come from one project — a leasing platform built in Go — but they are written so
they can be understood without knowing that codebase. Where a technical detail is needed, it is
explained.

---

## C-01 — A gate that could not fail

**Rule:** W4

A check was written to keep core libraries from importing infrastructure. It looked for
forbidden imports with a regular expression that required leading whitespace, because in many
languages grouped imports are indented.

Run against a deliberately broken library, it reported **"clean"**. A single-line import has no
indentation, so the pattern never saw it.

The fixed version asked the language toolchain instead of grepping source — and **passed
again**, because the tool's error went to stderr, which was redirected to `/dev/null`, and an
empty result read as no violations.

**How it surfaced:** by breaking the code on purpose and checking whether the gate failed. Not
by reading its implementation — both versions looked correct.

---

## C-02 — Six tests passed with a broken default

**Rule:** W6

Step retries with an attempt limit were added to an engine. Six tests were written: it retries,
it stops at the limit, the delay grows, a permanent error is not retried. All passed.

The attempt limit was **zero** and the injected clock was `nil`. Every first failure counted as
"out of attempts", and the backoff path would have panicked had it ever run.

The reason: **each of the six tests supplied its own configuration**. The default path — the one
production uses — never executed.

**How it surfaced:** incidentally, when one test started behaving differently from the
documentation. Without that, it would have shipped.

---

## C-03 — A suite passed once and failed on the second run

**Rule:** W7

Integration tests shared one database. They passed. Run again, they failed: one test left an
object behind that another counted as its own.

The first version of the suite **passed only on a clean database**, which is to say exactly
once.

**How it surfaced:** by running it twice in a row without cleaning up. There is no other way.

---

## C-04 — A decision register announced a choice reversed the day before

**Rule:** P7

An off-the-shelf workflow engine was chosen and the decision recorded. The next day an analysis
showed the engine **silently skips constructs it cannot execute** — a diagram with compensation
ran and compensated nothing. The decision was reversed and a compiler written instead.

For a full day the register still announced the first choice as current. Anyone reading it
would have concluded the opposite of what was being built.

Worse: the status field of the related open question pointed at the reversed decision **for
another day**, even though a correction notice sat directly above it. The notice corrected; the
field lied.

**How it surfaced:** during a completeness audit, on the question "if somebody read only this
document, would they conclude something consistent with what is built?"

---

## C-05 — A checker looked for the plural and missed the singular

**Rules:** W3, W9

A conformance audit reported that **six foundational decision records had no costs section**.
Adding one to all six was planned.

All of them had it. Six used the singular form of the word where the checker's pattern required
the plural.

Content was nearly written into documents that already contained it. What prevented it was one
condition set by the person commissioning the work: **fixes must follow from facts, not from
inference** — which forced opening the files instead of trusting the result.

**The conclusion it produced:** match **prefixes**, not full wordings. A wording variant is not
a deviation. The singular is correct when there is one cost.

---

## C-06 — Changing one punctuation mark switched off thirty-seven checks

**Rule:** W4

While rehearsing a switch of the documentation language, the translator wrote the open-question
headings with a hyphen `-` instead of an em dash `—`.

The checker parsed **zero of thirty-six** questions. Numbering, duplicate and status checks
stopped applying. It reported **"clean"**.

The number of checks executed fell from 168 to 131 and **nothing said so**.

**The fix is not a patch for the dash.** The checker now compares the number of headings that
*look like* questions against the number that *parsed* — coverage accounting for its own parser.
Any future drift in that format fails loudly instead of disabling the section.

**How it surfaced:** by rehearsing the procedure on a copy of a real register before anyone ran
it on the original.

---

## C-07 — Tightening the safety net blinded it

**Rule:** W4

Immediately after C-06, that coverage counter was added. At the same time the heading pattern
was tightened so it would not treat an archived entry as a duplicate.

The tightening applied to **both** counters — the parser and the net. On the next deformation of
the heading, a colon instead of a dash, both numbers fell to zero together, `0 == 0`, and the
check passed.

**A safety net has to count as loosely as it can.** It may exclude only known, deliberate
exceptions. Tightened along with the thing it watches, it stops watching anything.

**How it surfaced:** by testing the net against a deformation nobody had in mind when writing
it.

---

## C-08 — A private key survived the cleaning of the history

**Rule:** W3

A committed private key was removed from a repository's history. The operation was considered
finished.

A backup branch remained — created before the cleanup **precisely in order to have a copy**. It
still contained the key. One routine `git push --all` would have undone the whole operation.

**How it surfaced:** during a documentation completeness review, by checking the **actual state**
(`git branch`, whether the object still existed) rather than the memory of work done.

While removing that branch, the first two scans of the history also reported "clean" while being
worthless: once because a regex error was printed to stderr and ignored, once because the shell
did not word-split a variable and the loop ran once instead of eleven times. What caught it was
**coverage accounting** — a "scanned" versus "total" counter that refuses to conclude when the
two disagree.

---

## C-09 — An engine that executed less than was drawn

**Rules:** W1, W2

A candidate workflow engine accepted diagrams containing constructs it did not implement and
**skipped them without a word**. A diagram with a compensation event ran and compensated
nothing. Nothing in the log, nothing in the result — simply less than was drawn.

For a system where compensation is the basis of consistency, that was disqualifying.

**The conclusion is broader than a library choice:** a tool that meets something it does not
support must **stop loudly**. Silent degradation is worse than refusal, because it looks like
success.

---

## C-10 — Measuring your own measuring instrument

**Rule:** W8

Twice, a measured result was reported as a property of the system when it came from the test: a
supposed memory leak turned out to be an artefact of the test itself, and a supposed throughput
ceiling turned out to be a delay written into the test loop.

**How it surfaced:** by asking "what exactly does this measurement measure" before the number
reached the conclusions.

## C-11 — A check with no case of its own could not fire

**Rule:** W4, W8

The cross-register checker passed twenty-eight cases of its own self-test. One of the five
checks it advertised could not fire under any circumstances: it looked for a marker and a
question number **on one line**, a shape no template produces. It was also the only check
without a case of its own, so nothing noticed.

The cause ran deeper than a missing case. The checker used vocabulary it had invented — fields
and headings absent from the templates, the skills and the rules — and the fixtures were written
in that same vocabulary. They agreed with each other, and that agreement was the entire content
of the proof. A register built by following the method's own instructions was reported by that
checker as defective.

**How it surfaced:** by building a register from the instructions rather than from the fixtures.
The mechanism now guarding this is the only assertion that leaves the test files at all: the
self-test requires **every marker a checker keys on to occur in a template or in a skill**.

A footnote from the same repair: the new assertion passed when the checker it measures stopped
importing at all. An empty result read as "nothing is missing". An assertion about a tool's
output has to tell "I found nothing" apart from "I could not run" — a sentinel, not an empty
string.
