# L1 — Mantle / Identity

## Current Rating: 54

_Loader reads YAML or Markdown pact/voice, renders structured YAML into prompt-safe text, exposes `get_system_prompt()` for injection._

## Spec Rating (STATE.yaml): 54

## Delta: 0 post calibration.

## Shipped Components

- `src/ven0m/mantle/loader.py` — PACT/VOICE loading, warnings on missing/invalid files.
- `src/ven0m/mantle/pact.yaml` — Structured pact rules.
- `src/ven0m/mantle/voice.yaml` — Structured voice rules.
- `src/ven0m/mantle/__init__.py` — Public export surface.

## Spec Claims (from STATE.yaml)

- **“Identity does not survive session restart”** → STILL TRUE: loader loads files per invocation; no durable identity store inside ven0m.
- **“Inner reasoning not separated from outer response”** → STILL TRUE: single composed system prompt string only.

## Gap Analysis

| Claim | Code Reality | Verdict |
|-------|----------------|---------|
| Persistent identity across sessions | Files on disk read each time; no session-bound wallet | BUILD_INCOMPLETE |
| Inner/outer split | Not implemented | BUILD_INCOMPLETE |
