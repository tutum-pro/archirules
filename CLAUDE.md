# archirules

The plugin that carries the archirules method — and a project run by it.

## How this project is run

This project follows **archirules** — its own method. The rules live in
[`plugins/archirules/RULES.md`](plugins/archirules/RULES.md); the registers live in
[`docs/architecture/`](docs/architecture/README.md).

Applying the method here is not decoration. A method whose author does not apply it to their own
repository is an argument against itself.

**Documentation language: English.** Switch with `/archirules:language`.

In force without being reminded:

- **A doubt becomes a question entry**, not an on-the-spot decision (`/archirules:oq`).
- **A decision becomes a record** with "Considered and rejected" and **"Costs, knowingly
  accepted"** (`/archirules:adr`).
- **A phase gets its acceptance criterion written before the work** (`/archirules:phases`).
- **A new gate needs proof that it fails** (`/archirules:verification`).
- **Refuse rather than guess.** An unsupported construct stops the work loudly, citing the
  specification or the decision it violates.
- **Verify, do not assert.** The output of a command instead of a claim; the test suite twice
  in a row.
- **Correct a record that stopped being true inside the record** — never delete quietly.

Specific to this repository, from
[the binding requirements](docs/architecture/README.md#binding-requirements):

- **The executable layer is English without exception** — skills, scripts, plugin metadata.
- **A new check is not finished until it has been shown to fail.** Add its case to the
  self-test of the checker it belongs to — `scripts/selftest.sh` for `conform.py`,
  `scripts/selftest-consistency.sh` for `consistency.py` — in the same change. **Every check
  gets a case of its own**; one covered only incidentally by its neighbours turned out to be
  incapable of firing at all.
- **A checker keys only on wording a template or a skill produces.** A marker invented by a
  script and honoured only by its own fixtures proves the script consistent with its test data.
  The last case in `scripts/selftest.sh` asserts this for both checkers.
- **A rule must be usable without knowing this project's history.** Incidents go to
  `CASEBOOK.md` and are referenced, not inlined.
