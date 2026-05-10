# ven0m

**ven0m** is the first shipping artifact from [unshelled.ai](https://unshelled.ai): a Python toolkit for the **VENOM** agent architecture — session death and rebirth (**SIPHON**), plus the **Mantle** identity layer (immutable **PACT** and communication **VOICE**) meant to be injected as system context for LLMs. It is code-first scaffolding for distributed cognition without a hard-coded persona shell.

## Installation

When published to PyPI:

```bash
pip install ven0m
```

For local development (editable install with test extras):

```bash
pip install -e ".[dev]"
```

## Quick start

**SIPHON** — extract structured memory from a session transcript and append it to `MEMORY.md`, or build a **rebirth** prompt from recent sessions:

```bash
siphon extract path/to/transcript.md
siphon rebirth

# Same via the root CLI:
ven0m siphon extract path/to/transcript.md
ven0m siphon rebirth
```

**Mantle** — inspect identity files shipped under `ven0m/mantle/` (`pact.yaml`, `voice.yaml`) or emit a combined system prompt for piping into your stack:

```bash
ven0m mantle show
ven0m mantle inject
```

**Status**:

```bash
ven0m status
python -m ven0m.cli status
```

## Architecture overview

VENOM is organized as **14 layers** (shell, mantle, hearts, ink, arms, skin, defense, burst, siphon, coconut, reciprocity, personality, and supporting meta) with explicit ratings and gaps tracked in the canonical state file:

- [`docs/architecture/STATE.yaml`](docs/architecture/STATE.yaml)

This package currently implements **SIPHON** (L8 — session transfer) and **Mantle** (L1 — identity contracts). Other layers are specified in docs and state; they are not all implemented here yet.

## SOUL system (philosophy)

The **PACT** is the immutable behavioral contract: truth over comfort, identity through depth rather than performed persona, clean session death with durable knowledge, and enforcement that makes cooperation real. The **VOICE** standard defines how outputs read: direct, non-performative, mode-aware (e.g. execution vs. reflection) without announcing intent. Canonical prose lives under `docs/soul/`; structured payloads for runtime loading live as YAML beside the Mantle loader.

## Project structure

```
src/ven0m/
├── __init__.py
├── cli.py                 # ven0m root CLI (status, mantle, siphon dispatch)
├── core/
│   └── config.py          # SiphonConfig, MantleConfig, VenomConfig
├── mantle/
│   ├── loader.py          # Mantle class — load PACT/VOICE, system prompt
│   ├── pact.yaml          # Structured PACT
│   └── voice.yaml         # Structured VOICE
└── siphon/
    ├── cli.py             # siphon entry point
    └── extractor.py       # extraction + MEMORY.md I/O
docs/
├── architecture/STATE.yaml
├── soul/                  # PACT.md, VOICE.md (reference prose)
└── ...
tests/
├── test_siphon.py
└── test_mantle.py
```

## License

MIT
