---
name: bootstrap
description: Scaffold the architecture documentation set (decision records, open questions, phase register) in a project that does not have one yet. Use when starting a new project or introducing the archirules method into an existing one.
---

# Setting up the registers

**`--help`** — if `$ARGUMENTS` is `--help`, run
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/help.py bootstrap`, show its output, and stop there.

## Usage

```
/archirules:bootstrap [--help]
```

Creates `docs/architecture/` with the four registers, the templates filled in for this project,
and the archirules fragment in `CLAUDE.md`.

**Needs from you:** the documentation language, and whatever decisions the project has already
made in practice. In a project that is not empty, those exist and are usually recorded only in
commit messages.

**Will not:** overwrite an existing register set. If `docs/architecture/` is there, the skill
stops and says so.

## Before creating anything

1. Check whether `docs/architecture/` already exists. **If it does, do not overwrite.**
   Report what you found and offer to fill in what is missing.
2. Agree the **documentation language** (`pl` or `en`) with the user — it decides which set of
   `templates/` you use, and which file names the register gets (`fazy-realizacji.md` or
   `phases.md`). Record the choice in the register's `README.md` so the next session does not
   have to guess.

   The choice is **not permanent**: `/archirules:language` switches an existing project end to
   end. Say so, so nobody picks English "just in case" for a team that thinks in Polish.
3. Agree whether the project **starts from a process model** (rule P1). If it does, create the
   directory for models and the first model file — the notation is the project's choice (BPMN,
   a state machine, a sequence diagram); the method only requires that it be versioned rather
   than living in a presentation.

## What to create

```
docs/architecture/
  README.md              index + "binding requirements" section
  decisions/             (empty, for decision records)
  open-questions.md      heading and empty numbering
  fazy-realizacji.md     legend and empty phase table   (or phases.md in English)
```

Create the verification register **only when** the first claim needs correcting. An empty
verification register teaches people that it can be ignored.

## The binding-requirements section

This is the most important part of `README.md` and the only part read on **every** task. Only
decisions that bind work outside their own area belong here — usually empty at the start, with
one sentence saying what will land in it.

## Finally

Offer to add the fragment from `CLAUDE.md.pl.example` or `CLAUDE.md.en.example` — whichever
matches the chosen language — to the project's `CLAUDE.md`, so the method
applies without being asked for in every session. **Do not add it without consent** — it
changes default behaviour across the whole project.
