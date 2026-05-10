# Claude client snapshot — “ORIGINAL FILTRADO” (2026-03-31)

## Provenance

- **Origin:** Dump labeled `src [CLAUDE ORIGINAL FILTRADO] 31-03-2026` (third-party / leaked-style tree; treat as **competitive archaeology**, not a licensed dependency until verified).
- **Canon location:** `COMPARE/claude-filtrado-src-2026-03-31/` (ASCII path after promotion).
- **VENOM rule:** Extract **mechanics**, not wholesale UI or product clones. Do not paste this tree into `BUILD/` without license review and deliberate strip.

## What it is

Large TypeScript codebase: desktop/IDE-adjacent assistant — hooks, cost tracking, token budgets, memory directory (“memdir”), MCP wiring, notifications, migrations, REPL/sessions. Overlaps Skin (L5), Metabolic (L13), SIPHON-shaped memory pre-load (L8/L9 adjacent), not SOMA/L4.

## Mechanics to steal

| Mechanic | Path (in tree) | Maps to | Notes |
|----------|----------------|---------|--------|
| **Session cost + token aggregation** | `cost-tracker.ts`, `bootstrap/state` usage | L13 | Tracks USD, input/output tokens, cache tokens, tool duration, per-model usage — VENOCTIS-friendly metrics shape. |
| **Token budget continuation / stop** | `query/tokenBudget.ts` | L13 + L7 | `COMPLETION_THRESHOLD`, diminishing-returns stop after N continuations + low delta — avoids infinite burn. |
| **Selective memory recall (max 5)** | `memdir/findRelevantMemories.ts`, `memoryScan.ts` | L8 + L9 | Header scan + selector prompt; excludes `MEMORY.md`; `alreadySurfaced` + `mtimeMs` for freshness; telemetry hook for selection rate. |
| **MCP connectivity surface** | `hooks/notifs/useMcpConnectivityStatus.tsx` (and `services/mcp/`) | L5 | Pattern: user-visible degraded state when tools fail — feeds Skin + proprioception hooks. |
| **Internal event types** | `types/generated/events_mono/claude_code/v1/` | L12 | Structured events for debugging session shape — reference for VENOCTIS event schema. |

## VENOM reject / watch-outs

- **Central product shell:** importing the whole UI stack **centralizes** the agent (P1 tension).
- **License unknown:** do not ship copied files; **reimplement** contracts in Go/TS under VENOM-owned paths.
- **Different stack:** Bun/TS client ≠ locked SOMA+NATS; steals are **data shapes and policies**, not runtime merge.

## Next actions (no code this turn)

1. Add Postgres/VENOCTIS fields mirroring cost + budget decisions (schema extension in a later `BUILD/venoctis/` doc).
2. Optionally add `COMPARE/` one-pager per subsystem after reading more files (permissions, direct connect, swarm).
