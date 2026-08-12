# ADR-0005 — Distribution as a Claude Code plugin, not a template repository

**Status:** Accepted (2026-08-03)
**Related:** [ADR-0001](ADR-0001-language-split.md), [ADR-0002](ADR-0002-licence-and-name.md)

## Context

The method had to become reusable across unrelated projects, including work for third-party
clients. The material is instructions, templates and one checking script.

## Decision

**A public repository that is a Claude Code plugin marketplace**: `.claude-plugin/marketplace.json`
at the root, the plugin under `plugins/archirules/`.

Adding the source is a one-off per machine; from then on any project on that machine can install
it and invoke seven skills. The registers it creates live in the user's own repository, as files,
versioned with their code — never in a service.

## Considered and rejected

**A template repository to copy.** Copies do not receive corrections. Six documentation defects
were found and fixed in the first days; every copy made before them would still carry all six.

**A document to read.** The method's value is largely in being applied at the right moment —
when a doubt appears, when a phase opens. A document is consulted after the fact, if at all.

**An MCP server.** Deferred rather than rejected outright; see OQ-01. In short: everything the
method does is already possible with the built-in file and shell tools, so a server would wrap a
script in a protocol and cost the property that the plugin starts no processes and installs
nothing.

## Consequences

**Positive.** Corrections reach every user on update. Skills are invoked at the moment they
apply. Nothing runs in the background.

**Costs, knowingly accepted.**

- **It binds the method to one tool.** The rules are portable prose, but the delivery is not.
- **A marketplace must be added before installing**, which is one more step than a copy, and
  the naming of that step is not self-evident — it needed explaining in the README after a
  reader asked how a plugin on somebody's own GitHub would ever be found.
- **The checker needs `python3`.** Present nearly everywhere, and invoked only on demand.

## Implementation status

Done and installable. The install syntax was verified against the official marketplace's
documentation rather than written from convention.
