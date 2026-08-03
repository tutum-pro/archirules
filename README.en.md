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

## Install

```
/plugin marketplace add tutum-pro/archirules
/plugin install archirules@archirules
```

In a project:

```
/archirules:bootstrap
```

## Contents

- [`RULES.md`](plugins/archirules/RULES.md) — the rules, canonical version (PL)
- [`RULES.en.md`](plugins/archirules/RULES.en.md) — translation (EN)
- `plugins/archirules/skills/` — seven skills
- `plugins/archirules/templates/` — templates, PL and EN
- `plugins/archirules/scripts/` — structural conformance checker, with a self-test proving it
  can fail

## Where this came from

From a project where, after a few days of work, it turned out that: a check gate twice reported
"clean" against deliberately broken code, six tests passed despite a broken default
configuration, and the decision register spent a day announcing a technology choice that had
been reversed the day before.

Every one of those was found **by verifying, not by reading the code**. The rules in `RULES.md`
are the record of how you find them.

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
