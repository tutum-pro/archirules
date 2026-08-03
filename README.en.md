# archirules

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-orange.svg)](https://github.com/tutum-pro/archirules)

🇵🇱 [Polski](README.md) — **canonical version**

**Meta-rules for running a software project** — as a Claude Code plugin.

A method developed in practice, while building a leasing platform. **Every rule exists because
its absence broke something**, not because it sounds good — most of them carry the failure they
prevent written alongside.

## What it does

Turns architectural decisions, doubts, phases and evidence into **first-class artefacts**:
versioned with the code, reviewed like code, and — like code — capable of going stale, which is
also recorded.

A software project rarely loses to hard decisions. It loses to decisions **made silently** — by
the order of refactors, by a default value, by nobody writing down the alternative.

## Getting started — from nothing to a working register

### What you need

- **Claude Code** (CLI, desktop app or IDE extension),
- a project directory, preferably a git repository.

Nothing else. The plugin installs no dependencies and starts no services.

### 1. Add the marketplace — once per machine

In Claude Code:

```
/plugin marketplace add tutum-pro/archirules
```

This registers a **source** of plugins. Done once; further projects on the same machine do not
need it again.

### 2. Install the plugin

```
/plugin install archirules@archirules
```

The form is `plugin-name@marketplace-name`. Both names are the same here, and that is not a
mistake — the repository holds one marketplace called `archirules` and one plugin of the same
name.

Alternatively, `/plugin` opens a browser where it can be found in the list.

After installing, check the skills are visible: type `/archirules:` and a completion list of
seven entries should appear.

### 3. Run bootstrap **inside the project directory**

Open Claude Code in the project and type:

```
/archirules:bootstrap
```

**What happens.** You will be asked two things:

- **the documentation language** — Polish or English; it decides the templates and the file
  names, and it is not a permanent choice (see `/archirules:language`);
- **whether the project starts from a business process model** — if so, a place for models is
  created too.

Then this appears:

```
docs/architecture/
  README.md              decision index + "binding requirements" section
  decisions/             empty, for decision records
  open-questions.md      the open-questions register
  phases.md              phase register with acceptance criteria
```

**A project that already has `docs/architecture/` will not be overwritten.** Bootstrap reports
what it found and offers to fill in what is missing.

### 4. Accept the entry in `CLAUDE.md`

Bootstrap offers to add a fragment to the project's `CLAUDE.md`. **This is the step that makes
the method apply without being asked for in every session** — without it the skills exist, but
you have to invoke them by hand.

The fragment is short and you can read it first: `CLAUDE.md.en.example` in the plugin.

### 5. Check that it worked

```
/archirules:audyt
```

or directly:

```
python3 ~/.claude/plugins/marketplaces/archirules/plugins/archirules/scripts/conform.py docs/architecture
```

Zero problems and exit code 0 means the register is structurally complete. A freshly created
one always is — this check earns its keep later, once there are documents to get wrong.

### What next

| you want to | type |
|---|---|
| record a decision | `/archirules:adr` |
| record a doubt with no answer yet | `/archirules:oq` |
| open a phase with an acceptance criterion | `/archirules:fazy` |
| check whether the register has started lying | `/archirules:audyt` |
| add a gate and prove it fails | `/archirules:weryfikacja` |
| switch the project to another language | `/archirules:language` |

## Where this came from

From a project where, after a few days of work, it turned out that: a check gate twice reported
"clean" against deliberately broken code, six tests passed despite a broken default
configuration, and the decision register spent a day announcing a technology choice that had
been reversed the day before.

Every one of those was found **by verifying, not by reading the code**.

Ten such cases are written up in [`CASEBOOK.en.md`](plugins/archirules/CASEBOOK.en.md) —
deliberately kept apart from the rules. **A rule has to be usable without knowing somebody
else's project**, while the case is the evidence for anyone who wants to know why it is worded
the way it is.

## A note on language

Polish is the canonical language of this method: it is the language it was written and argued
in, and where a translation disagrees with the original, **the Polish version wins**. The
English texts are faithful translations, not independent documents.

Templates ship in both languages and `/archirules:bootstrap` asks which one a project should
use. Reasoning is concentrated in `RULES.md` and the templates are deliberately thin on prose,
so that the two versions have as little room to drift as possible.

## License

**[CC BY-SA 4.0](LICENSE)** — Attribution · ShareAlike 4.0 International.

Copyright © 2026 Robert Sternal (tutum-pro).

You may copy, distribute and adapt this work, including commercially, under two conditions:
**attribution** and **licensing derivative works under the same terms**.

What that means in practice:

- **Internal use carries no obligations.** ShareAlike is triggered by distribution, not by use.
  Adapting the method for a team's or a client's internal needs creates no duty to publish.
- **Publishing an adaptation — under CC BY-SA 4.0.** If you release a modified version, you
  release it on the same terms.
- **Documents produced with the method are not derivative works.** The ADRs, registers and
  plans written in your project are yours. The license covers the method itself — the rules,
  skills and templates — not what you write using them.

## Trademarks

**The license grants no rights to the names "archirules" or "tutum-pro".**

Derivative works may not use these names, nor suggest that they are endorsed, supported or
approved by the author. Name your adaptation something else — crediting the source ("based on
archirules") is required by the license and is fine; **taking the name as your own is not**.

That distinction, rather than the copyleft clause, is what actually protects the identity of
the method.
