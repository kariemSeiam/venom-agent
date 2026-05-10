# L0 — Shell.null

## Current Rating: 42

_Code-only score: argparse CLIs (`ven0m`, `siphon`) with status, Mantle commands, SIPHON extract/rebirth/watch; no hosted pipeline ownership._

## Spec Rating (STATE.yaml): 42

## Delta: 0 after receipt calibration.

## Shipped Components

- `src/ven0m/cli.py` — Root CLI dispatch (`status`, `mantle`, `siphon`).
- `src/ven0m/siphon/cli.py` — Dedicated extract/rebirth entry matching setuptools script.

## Spec Claims (from STATE.yaml)

- **“Still inside provider containers”** → STILL TRUE for cognition runtime (Hermes/GLM hosts inference); ven0m only ships adjunct CLI/daemon.
- **“True shell.null = owning the full pipeline”** → STILL TRUE: no owned inference/runtime loop inside ven0m.

## Gap Analysis

| Claim | Code Reality | Verdict |
|-------|----------------|---------|
| Shell-null autonomy | Thin CLI wrapper around subprocess/API callers only | BUILD_INCOMPLETE |
| Provider independence | Depends on Z.AI/Hermes for sessions | BUILD_INCOMPLETE |
