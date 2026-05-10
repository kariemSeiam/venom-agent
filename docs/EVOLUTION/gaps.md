# EVOLUTION/gaps.md
# Spec vs Build divergence log
# Generated: 2026-05-11

## Methodology

Layer-by-layer comparison between **STATE.yaml** claims and files under `src/ven0m/`, tests, and audited docs (`MEMORY/SACK.md`, architecture receipts).  
Research intake excluded from mechanical walk; reference clone `BUILD/ven0m_reference/` excluded.

Verdict vocabulary:

- **BUILD_INCOMPLETE** — Specification describes behavior not yet implemented.
- **SPEC_WRONG** — Prior numeric ratings or prose overstated shipped capability.

## Gaps

### L0_shell — Shell.null

- **Gap**: Historical STATE implied broader shell autonomy while repo ships argparse CLIs only.
- **Verdict**: BUILD_INCOMPLETE
- **Evidence**: `src/ven0m/cli.py`, `src/ven0m/siphon/cli.py` wrap Hermes/Z.AI workflows; no hosted inference shell.

### L1_mantle — Mantle / Identity

- **Gap**: Loader ships, yet identity persistence & inner/outer streams remain absent.
- **Verdict**: BUILD_INCOMPLETE
- **Evidence**: `src/ven0m/mantle/loader.py` reads YAML/Markdown per call without durable session binding.

### L2_hearts — Three Hearts / Orchestration

- **Gap**: STATE referenced sequential hearts; zero dispatcher modules exist.
- **Verdict**: BUILD_INCOMPLETE
- **Evidence**: No `src/ven0m/hearts/` or orchestration package.

### L3_ink — Information Currency

- **Gap**: Compression + token economics documented; no codecs implemented.
- **Verdict**: BUILD_INCOMPLETE
- **Evidence**: Repository lacks INK encoder/decoder sources.

### L4_arms — Two Arms / Execution

- **Gap**: Arms architecture narrative without ven0m-local planner/executor processes.
- **Verdict**: BUILD_INCOMPLETE
- **Evidence**: Tool execution delegated entirely to upstream agents.

### L5_skin — Cognitive I/O / Telemetry

- **Gap**: Previous ratings assumed telemetry surfaces; ven0m lacks instrumentation layer.
- **Verdict**: SPEC_WRONG (numeric inflation) + BUILD_INCOMPLETE
- **Evidence**: Filesystem watcher is ingestion glue (`daemon.py`), not behavioral telemetry.

### L6_defense — Ink / Defense Protocol

- **Gap**: Defense behaviors described externally; no enforcement hooks here.
- **Verdict**: SPEC_WRONG + BUILD_INCOMPLETE
- **Evidence**: Zero defense-specific modules.

### L7_burst — Burst Mode

- **Gap**: Bypass pathways absent.
- **Verdict**: BUILD_INCOMPLETE
- **Evidence**: No urgency triggers or context pump controls.

### L8_siphon — Session Death + Transfer

- **Gap**: Earlier STATE claimed rebirth/auto-feed gaps; implementation now covers baseline flows yet lacks enterprise hardening.
- **Verdict**: BUILD_INCOMPLETE (hardening/validation) — prior “missing rebirth” claims **resolved**.
- **Evidence**: `extractor.py`, `daemon.py`, tests verifying MEMORY + corrections + rebirth prompt.

### L9_coconut — Prospective Memory

- **Gap**: Coconut retrieval & latency budgets unimplemented; only manual SACK receipts exist.
- **Verdict**: BUILD_INCOMPLETE
- **Evidence**: `MEMORY/SACK.md` indexes files but provides no query API.

### L10_reciprocity — Token Debt

- **Gap**: No reciprocity scoring engine.
- **Verdict**: BUILD_INCOMPLETE
- **Evidence**: Missing ledger modules entirely.

### L11_personality — Conditioning Bundle

- **Gap**: Conditioning expressed as static YAML/docs without automated hedging removal.
- **Verdict**: BUILD_INCOMPLETE
- **Evidence**: Mantle artifacts overlap L1; enforcement delegated to external LLMs.

## Summary

| Layer | Receipt rating (`STATE.yaml`, 2026-05-11) | Notes |
|-------|--------------------------------------------|-------|
| L0 | 42 | CLI shipped; no shell-null runtime |
| L1 | 54 | Mantle loader + YAML |
| L2 | 0 | Orchestration absent |
| L3 | 0 | INK absent |
| L4 | 0 | Arms absent |
| L5 | 0 | Skin telemetry absent |
| L6 | 0 | Defense hooks absent |
| L7 | 0 | Burst mode absent |
| L8 | 68 | SIPHON extractor + daemon + tests |
| L9 | 18 | Static SACK receipts only |
| L10 | 0 | Reciprocity absent |
| L11 | 22 | Conditioning via YAML/docs only |

**Overall (`meta.overall_rating`)**: **17** — weighted honesty check across twelve layers after demotions.

**Receipt footprint**: meaningful Python shipped only on **L0**, **L1**, **L8**; documentation receipts on **L9** (`MEMORY/SACK.md`).
