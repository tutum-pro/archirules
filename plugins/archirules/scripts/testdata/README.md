# Test data

Input for `../selftest.sh`, which copies these sets and breaks the copies in known
ways to prove the checker can fail.

**These are not examples to copy into a project.** They are the smallest documents
that satisfy `conform.py`, with no content worth reading. Templates for real
projects live in `../../templates/`.

Two sets, because `conform.py` claims to support two languages and a claim nothing
exercises is a claim nobody has tested. `valid-en` is what proves the language
detection and the English markers actually work.

`xreg-pl` and `xreg-en` are the input for `../selftest-consistency.sh` instead. `valid-*`
cannot serve there: one decision record and no blocker table, so `consistency.py` walks them
without running a single cross-register check. The `xreg-*` sets are the smallest ones holding
one instance of every relation it looks at — a question blocking a phase, a phase waiting on a
question, a record modifying another, a superseded record, and a record with no links at all.

Fixtures belong outside the register root. `conform.py` globs `**/*.md` recursively, so a
project keeping its checker's test sets under `docs/architecture/` has them counted as project
documents — on the set this checker grew from that read 377 checks instead of 349, inflating
the coverage counter by 8% with nothing turning red.
