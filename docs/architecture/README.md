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
| [0006](decisions/ADR-0006-checker-speaks-the-methods-vocabulary.md) | A checker keys only on wording the method itself produces | Accepted |
| [0007](decisions/ADR-0007-explicit-version-as-the-migration-anchor.md) | An explicit version is what a migration moves between | Accepted |
| [0008](decisions/ADR-0008-help-comes-from-a-file-not-from-memory.md) | `--help` is routed by a sentence and answered by a file | Accepted |
| [0009](decisions/ADR-0009-updating-a-project-is-not-updating-the-plugin.md) | Updating a project's registers is separate from updating the plugin | Accepted |
| [0010](decisions/ADR-0010-traceability-derived-from-git-trailers.md) | Traceability is derived from commit trailers, never copied into a register | Accepted |
| [0011](decisions/ADR-0011-a-skill-that-explains-the-method.md) | The method explains itself in a skill, and every reference in it is checked | Accepted |
| [0012](decisions/ADR-0012-work-stops-on-a-contradicted-register.md) | Work stops when the register contradicts itself or a question blocks it | Accepted, not implemented |
| [0013](decisions/ADR-0013-a-register-earns-its-existence-by-a-defect.md) | A new register earns its existence by a defect its absence caused | Accepted |
| [0014](decisions/ADR-0014-reading-the-version-is-not-updating.md) | Reading which version a project stands at is a separate, read-only act | Accepted |
| [0015](decisions/ADR-0015-references-are-links-and-anchors-are-checked.md) | A reference to a register entry is a link, and the anchor is checked | Accepted |
| [0016](decisions/ADR-0016-the-converter-covers-header-fields-only.md) | The converter covers header fields, and the narrowing is the decision | Accepted |

## Binding requirements

Decisions that bind **every** change here, not only their own area.

- **The executable layer is English without exception** — skills, scripts, plugin metadata
  ([ADR-0001](decisions/ADR-0001-language-split.md)). A `SKILL.md` is consumed by a model at run
  time and read by everyone who installs the plugin; it is closer to code than to prose.
- **A new gate is not finished until it has been shown to fail**
  ([ADR-0004](decisions/ADR-0004-checker-ships-with-its-own-proof.md)). This applies to the
  tooling in this repository as forcefully as to anything it checks — arguably more, since a
  broken checker certifies broken projects. Each checker carries **its own** self-test; the
  obligation attaches to the check, not to a particular file
  ([ADR-0006](decisions/ADR-0006-checker-speaks-the-methods-vocabulary.md)).
- **A checker keys only on wording a template or a skill produces**
  ([ADR-0006](decisions/ADR-0006-checker-speaks-the-methods-vocabulary.md)). A marker invented by
  a script and honoured only by its own fixtures proves the script consistent with itself, which
  was never in doubt. The self-test asserts this; it is not left to review.
- **A new register earns its existence by a defect its absence caused**
  ([ADR-0013](decisions/ADR-0013-a-register-earns-its-existence-by-a-defect.md)). Not symmetry
  with another methodology, not tidiness — an event that happened and cannot be reconstructed
  today. The precedent is the verification register, which is created at the first defect caused
  by an unverified claim rather than on day one. This cannot be checked mechanically, so it is a
  review convention (rule W9) and is named as one.
- **A rule must be usable without knowing this project's history**
  ([ADR-0003](decisions/ADR-0003-casebook-apart-from-rules.md)). Incidents belong in the
  casebook, referenced, not inlined.

## Other documents

- [Open questions](open-questions.md) — what we do not know yet and what it blocks
- [Phase register](phases.md) — what is done, what is next
- [Verification register](verification.md) — what is verified, as opposed to asserted
- [Traceability](traceability.md) — which commits implement which entry (generated)
