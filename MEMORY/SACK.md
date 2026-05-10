# SACK.md — Shipped Code Index
# Auto-generated from code walk. Every claim has a receipt.
# Generated: 2026-05-11

## Methodology

- **Walked**: every `.py`, `.yaml`, `.yml`, `.md` under `/root/ven0m/` excluding `.git/`, `BUILD/` (reference mirror), `docs/research/intake/`, `.pytest_cache/`.
- **Counted**: `wc -l` per file (below).
- **Infra extras**: `pyproject.toml`, `.gitignore` (not matched by find filter; counted separately).
- **Total markdown/py/yaml files in walk**: 43 + **MEMORY/SACK.md** (this file) after generation.
- **Reference clone**: `BUILD/ven0m_reference/` excluded from receipts (duplicate tree).

## Source File Index

### L0_shell — Shell.null (rating: TBD → see STATE.yaml)

| File | Type | Trigger/Function | Lines | Status |
|------|------|------------------|-------|--------|
| src/ven0m/cli.py | cli | Root argparse: `status`, `mantle show|inject`, `siphon extract|rebirth|watch` | 152 | SHIPPED |
| src/ven0m/siphon/cli.py | cli | Standalone `siphon` entry: `extract`, `rebirth` | 82 | SHIPPED |

### L1_mantle — Mantle / Identity (rating: TBD)

| File | Type | Trigger/Function | Lines | Status |
|------|------|------------------|-------|--------|
| src/ven0m/mantle/__init__.py | module | Exports `Mantle` | 7 | SHIPPED |
| src/ven0m/mantle/loader.py | module | Loads PACT/VOICE from YAML or `.md`; `get_system_prompt()` | 117 | SHIPPED |
| src/ven0m/mantle/pact.yaml | data | Structured pact / immutable contract | 41 | SHIPPED |
| src/ven0m/mantle/voice.yaml | data | Structured voice / communication rules | 48 | SHIPPED |

### L8_siphon — Session Death + Transfer (rating: TBD)

| File | Type | Trigger/Function | Lines | Status |
|------|------|------------------|-------|--------|
| src/ven0m/siphon/__init__.py | module | Package marker | 0 | STUB |
| src/ven0m/siphon/extractor.py | module | LLM extract → `Extraction` (7 fields), MEMORY.md I/O, rebirth prompt, `append_corrections` | 268 | SHIPPED |
| src/ven0m/siphon/daemon.py | module | Watchdog polling watcher for Hermes JSON sessions; `.siphon_index.json` dedupe | 222 | SHIPPED |

### L9_coconut — Prospective Memory / SACK (rating: TBD)

| File | Type | Trigger/Function | Lines | Status |
|------|------|------------------|-------|--------|
| MEMORY/SACK.md | doc | **This file** — shipped code index / receipts (manual + audit) | 137 | SHIPPED |
| docs/memory/SACK.md | doc | Legacy scaffold / earlier index (superseded by process; kept in tree) | 170 | SHIPPED |

_No programmatic retrieval, `<100ms` scan, or coconut metadata enforcement exists._

### Cross-cutting config (maps INFRA; feeds L1 + L8)

| File | Type | Trigger/Function | Lines | Status |
|------|------|------------------|-------|--------|
| src/ven0m/core/config.py | config | `SiphonConfig` (API, paths, watch_dir, memory_dir), `MantleConfig`, `VenomConfig` | 53 | SHIPPED |
| src/ven0m/__init__.py | module | Package version string | 10 | SHIPPED |
| src/ven0m/core/__init__.py | module | Empty package marker | 0 | STUB |

### INFRA

| File | Type | Trigger/Function | Lines | Status |
|------|------|------------------|-------|--------|
| README.md | doc | Install, quickstart, architecture pointer | 84 | SHIPPED |
| pyproject.toml | config | setuptools package, deps (`httpx`, `pyyaml`, `watchdog`), entry points `ven0m`, `siphon` | 41 | SHIPPED |
| .gitignore | config | Git ignore rules | 12 | SHIPPED |

### TESTS

| File | Type | Trigger/Function | Lines | Status |
|------|------|------------------|-------|--------|
| tests/test_mantle.py | test | Mantle loader, YAML/md fallbacks, system prompt | 92 | SHIPPED |
| tests/test_siphon.py | test | Extraction schema, memory I/O, rebirth, corrections YAML, daemon index / dirs | 311 | SHIPPED |

### DOCS — Architecture & evolution

| File | Type | Trigger/Function | Lines | Status |
|------|------|------------------|-------|--------|
| docs/architecture/STATE.yaml | doc | Layer ratings, evolution log, arms roster | 237 | SHIPPED |
| docs/architecture/LAYERS/*.md | doc | Per-layer receipts (added 2026-05-11) | — | SHIPPED |

### DOCS — Soul canon (prose; mirrors L1 content)

| File | Type | Trigger/Function | Lines | Status |
|------|------|------------------|-------|--------|
| docs/soul/PACT.md | doc | Immutable contract prose | 64 | SHIPPED |
| docs/soul/VOICE.md | doc | Voice standard prose | 71 | SHIPPED |

### DOCS — Memory samples / legacy paths

| File | Type | Trigger/Function | Lines | Status |
|------|------|------------------|-------|--------|
| docs/memory/MEMORY.md | doc | Sample / bundled MEMORY prose | 311 | SHIPPED |
| docs/memory/corrections.yaml | data | Placeholder corrections file | 0 | STUB |

### DOCS — EVOLUTION

| File | Type | Trigger/Function | Lines | Status |
|------|------|------------------|-------|--------|
| docs/EVOLUTION/LOOP.md | doc | Evolution loop notes | 111 | SHIPPED |
| docs/EVOLUTION/gaps.md | doc | Spec vs build divergence (rewritten 2026-05-11) | 108 | SHIPPED |
| docs/EVOLUTION/ratings_history.yaml | data | Ratings history | 38 | SHIPPED |

### DOCS — Audit

| File | Type | Trigger/Function | Lines | Status |
|------|------|------------------|-------|--------|
| docs/audit/AUDIT/VENOM∞.md | doc | Audit corpus | 975 | SHIPPED |
| docs/audit/AUDIT/deep-research-report.md | doc | Deep research report | 283 | SHIPPED |
| docs/audit/AUDIT/archive/VENOM∞-v1.md | doc | Archived audit | 850 | SHIPPED |

### DOCS — Research compare (not intake)

| File | Type | Trigger/Function | Lines | Status |
|------|------|------------------|-------|--------|
| docs/research/compare/*.md | doc | Competitive / OSS notes | see wc | SHIPPED |
| docs/research/compare/research/batch-001.md | doc | Batch 001 research | 256 | SHIPPED |
| docs/research/compare/research/telegram-batch-002.md | doc | Batch 002 pointer | 46 | SHIPPED |
| docs/research/compare/_STEAL.md | doc | Steal log | 107 | SHIPPED |

## Layers with NO shipped `.py` implementation in `src/ven0m/` (receipt: empty)

| Layer | Evidence |
|-------|----------|
| L2_hearts | No orchestration / dispatcher package |
| L3_ink | No compression / INK codec |
| L4_arms | No tool executor / planner split in-repo |
| L5_skin | No telemetry or cognitive I/O layer (daemon fs watch ≠ skin spec) |
| L6_defense | No tyrosinase / defense protocol code |
| L7_burst | No burst trigger / context pump bypass |
| L10_reciprocity | No token debt / handshake |

## Quick totals (implementation)

| Bucket | Files | Approx LOC (py only) |
|--------|-------|----------------------|
| `src/ven0m/**/*.py` | 11 | ~911 |

---

_End of index. Regenerate after significant merges._
