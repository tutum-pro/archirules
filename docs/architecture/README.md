# Architecture — decision register

This project follows its own method. That is not decoration: a method whose author does not
apply it to their own repository is an argument against itself.

Documentation language: **English**. The method's own text (`RULES.md`, templates) is
canonically Polish, but this register explains decisions *about the plugin* to people who use
and contribute to it, and those are international. It also exercises the English templates in
anger rather than only against a synthetic fixture.

## Decision register

| ADR | Subject | Status |
|---|---|---|
| [0001](decisions/ADR-0001-language-split.md) | Polish for the method, English for the executable layer | Accepted |
| [0002](decisions/ADR-0002-licence-and-name.md) | CC BY-SA 4.0 and a reserved name | Accepted |
| [0003](decisions/ADR-0003-casebook-apart-from-rules.md) | The casebook is separate from the rules | Accepted |
| [0004](decisions/ADR-0004-checker-ships-with-its-own-proof.md) | The checker ships with a proof that it fails | Accepted |
| [0005](decisions/ADR-0005-distribution-as-a-plugin.md) | Distribution as a Claude Code plugin, not a template repository | Accepted |

## Binding requirements

Decisions that bind **every** change here, not only their own area.

- **The executable layer is English without exception** — skills, scripts, plugin metadata
  ([ADR-0001](decisions/ADR-0001-language-split.md)). A `SKILL.md` is consumed by a model at run
  time and read by everyone who installs the plugin; it is closer to code than to prose.
- **A new gate is not finished until it has been shown to fail**
  ([ADR-0004](decisions/ADR-0004-checker-ships-with-its-own-proof.md)). This applies to the
  tooling in this repository as forcefully as to anything it checks — arguably more, since a
  broken checker certifies broken projects.
- **A rule must be usable without knowing this project's history**
  ([ADR-0003](decisions/ADR-0003-casebook-apart-from-rules.md)). Incidents belong in the
  casebook, referenced, not inlined.

## Other documents

- [Open questions](open-questions.md) — what we do not know yet and what it blocks
- [Phase register](phases.md) — what is done, what is next
- [Verification register](verification.md) — what is verified, as opposed to asserted
