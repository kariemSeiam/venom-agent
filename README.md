# ven0m

> *The octopus shed its shell. Then it evolved its mind.*

**unshelled.ai** — building the VENOM agent architecture.

## What

VENOM is a multi-layer AI agent architecture built on 8 prime principles. No framework. No shell. Pure distributed cognition modeled after octopus biology.

This repo is the living implementation. Not docs. Code.

## Install

```bash
pip install -e ".[dev]"
```

## SIPHON — Session Death & Rebirth

The core of VENOM. Extracts knowledge at session death so the next session is born with memory.

```bash
# Extract from a session transcript
siphon extract path/to/transcript.md

# Build rebirth prompt from memory
siphon rebirth

# Dry run (print, don't write)
siphon extract transcript.md --dry-run
```

### The 4 Fields

```yaml
session:
  id: "session-NNN"
  date: YYYY-MM-DD
  decisions: []      # what changed
  corrections: []    # what was wrong and got fixed
  next_action: ""    # first thing to do next session
  current_truth: ""  # one sentence the next session inherits
```

4 fields. Not 22. Not 729 lines. Run for 20 sessions before expanding.

## Test

```bash
pytest -v
```

## Project Structure

```
src/ven0m/
├── core/config.py      # Configuration (API, paths)
├── siphon/
│   ├── extractor.py    # Session extraction + memory I/O
│   └── cli.py          # CLI entry point
└── mantle/             # Identity + behavioral contracts (coming)
docs/                   # Architecture reference, research, audits
tests/                  # 18 tests, all green
```

## Principles

```
P1. Distribution over centralization
P3. Identity through depth, not armor
P4. Interface is the most expensive organ
P5. Clean death enables real continuity
P6. Prepare for futures visible from the present
P7. Enforcement makes collaboration real
P8. Personality is portable conditioning
```

## Company

**unshelled.ai** — Kariem Seiam

License: MIT
