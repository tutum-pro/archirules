---
name: version
description: Report which version of the archirules method is installed and which version this project's registers stand at, and whether the two agree. Use when you want to know where a project stands before deciding whether to update it.
---

# Which version this project stands at

**`--help`** — if `$ARGUMENTS` is `--help`, run
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/help.py version`, show its output, and stop there.

## Usage

```
/archirules:version [--help]
```

Reports two versions and whether they agree: the **method** installed, and the version this
project's **registers** were last brought up to.

**Needs from you:** nothing. It reads two files and writes nothing.

**Will not:** change anything, migrate anything, or take a snapshot. That is
`/archirules:update`, and this exists partly so that you do not have to invoke something called
"update" in order to ask a question.

**Will not:** require a clean working tree or a git repository. `/archirules:update` refuses
without both, which is correct for a command that edits registers and wrong for one that reads
them — and mid-task, with a dirty tree, is exactly when the question gets asked.

### Examples

```
/archirules:version                        run from the project root
/archirules:version docs/architecture      when the registers are somewhere else
```

## What to run

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/version.py docs/architecture
```

Show its output. Do not paraphrase the numbers — they are the answer.

## What the exit codes mean, and what to say about each

**0 — the two agree.** Say so and stop. Nothing to do.

**1 — they disagree**, in one of three ways, and they are not interchangeable:

- **Registers behind the method.** The usual case after a plugin update. Point at
  `/archirules:update`, and at `migrations.py` if they want to see what changed before
  committing to it. Do not run either without being asked.
- **Registers ahead of the method.** No migration runs backwards. This means the plugin was
  downgraded, or these registers came from a machine with a newer archirules. The fix is to
  update the **plugin**, not the project — say that plainly rather than offering `update`, which
  cannot help and would take a snapshot for nothing.
- **No version recorded.** The registers predate version tracking. Say what the consequence is:
  `/archirules:update` will treat the project as 1.0.0 and list every migration ever written.
  Offer to record the correct version if the user knows it — and **only** if they do. Writing a
  guess into that file is worse than leaving it absent, because a guess that is too high skips
  migrations silently.

**2 — a usage error**, not a finding about the project: the register directory does not exist, or
the plugin manifest cannot be read. Report it as a problem with the invocation or the
installation, never as a statement about the project's registers.

## What this does not tell you

That the registers are **correct** — only which version they claim. A project can sit at the
current version with a register that contradicts itself; that is what `conform.py` and
`consistency.py` are for, and `/archirules:audit` runs them.
