# ven0m — VENOM's First Product

## What This Is

ven0m is a Python package for AI agent identity and session persistence. It provides:
- **Siphon** — Extract knowledge from conversation transcripts, rebirth sessions
- **Mantle** — Load agent identity (PACT, VOICE) as injectable system prompts
- **Core** — Configuration management for all ven0m components

## Project Structure

```
src/ven0m/
├── __init__.py          # Package entry, version
├── cli.py               # Root CLI: ven0m siphon|mantle|status
├── core/
│   └── config.py        # SiphonConfig, MantleConfig, VenomConfig
├── mantle/
│   ├── __init__.py
│   └── loader.py        # Load PACT.md + VOICE.md as system prompts
└── siphon/
    ├── __init__.py
    ├── cli.py           # siphon extract|rebirth subcommands
    └── extractor.py     # Transcript parsing + memory extraction

SOUL/                     # Agent identity documents
├── PACT.md              # Behavioral contract
└── VOICE.md             # Communication style

MEMORY/                   # Persistent memory
├── MEMORY.md            # Long-term memory store
└── SACK.md              # Corrections and learnings

tests/                    # pytest
├── test_siphon.py       # Extraction + memory I/O
└── test_mantle.py       # Mantle loading
```

## Development

```bash
pip install -e ".[dev]"
pytest                    # Run tests
ven0m status              # CLI smoke test
ven0m mantle load         # Test mantle loading
ven0m siphon extract <file>  # Extract from transcript
```

## Conventions

- Python 3.11+, type hints everywhere
- pytest for testing, no other framework
- Commit prefix: `🐺` (wolf emoji)
- Follow existing patterns — don't introduce new dependencies without discussion
