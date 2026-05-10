# SACK.md — Artifact Index
## Queryable store of reusable artifacts
## Loaded at session START. Relevant items pre-loaded before first response.

> Every artifact that survives session death lives here.
> Retrieval target: <100ms scan.

---

## Schema

```yaml
- artifact: "path/to/artifact"
  created: YYYY-MM-DD
  type: pattern | template | solution | reference | tool | schema | protocol
  summary: "one sentence — what is this"
  portable_to:
    - context: "describe when this is useful"
  trigger: "when to load this without being asked"
  status: active | deprecated | superseded
  session_origin: "session-NNN"
  superseded_by: null | "path/to/new"
```

---

## INDEX

- artifact: "CLAUDE.md"
  created: 2026-05-10
  type: protocol
  summary: "Master Claude Code environment prompt for the VENOM project"
  portable_to:
    - context: "any Claude Code session inside venom/"
  trigger: "always — read at session start"
  status: active
  session_origin: session-001

- artifact: "STATE.yaml"
  created: 2026-05-10
  type: schema
  summary: "Single source of truth: all layer ratings, blockers, build order"
  portable_to:
    - context: "any session that needs to know current VENOM state"
  trigger: "always — read at session start before any work"
  status: active
  session_origin: session-001

- artifact: "INTAKE/PROTOCOL.md"
  created: 2026-05-10
  type: protocol
  summary: "4-question filter + scoring system for all incoming data"
  portable_to:
    - context: "any system that needs to evaluate incoming knowledge quality"
    - context: "any AI agent that needs data validation"
  trigger: "when new data arrives before routing it anywhere"
  status: active
  session_origin: session-001

- artifact: "EVOLUTION/LOOP.md"
  created: 2026-05-10
  type: protocol
  summary: "7-step evolution rhythm: OBSERVE→MEASURE→COMPARE→STEAL→BUILD→VALIDATE→UPDATE"
  portable_to:
    - context: "any iterative architecture development project"
    - context: "any agent system that needs to self-improve"
  trigger: "at session start after STATE.yaml and MEMORY.md"
  status: active
  session_origin: session-001

- artifact: "COMPARE/NousResearch/"
  created: 2026-05-10
  type: tool
  summary: "Vendor-scoped OSS trees (Hermes + self-evolution) for competitive archaeology"
  portable_to:
    - context: "L4/L10/L13 steal-mining whenever Hermes changelog moves"
  trigger: "before claiming Hermes parity on memory or routing"
  status: active
  session_origin: session-002

- artifact: "COMPARE/research/batch-001.md"
  created: 2026-05-10
  type: reference
  summary: "Structured research batch covering memory, compaction, durable execution, routing, and agent-memory papers"
  portable_to:
    - context: "when choosing new COMPARE targets for SIPHON, SACK, SOMA, or metabolic routing"
    - context: "when validating whether a new idea has an implementation mechanic or is architecture intoxication"
  trigger: "before expanding COMPARE/ or updating INTAKE/QUEUE.md from memory/agent research"
  status: active
  session_origin: session-003
  superseded_by: null

- artifact: "BUILD/siphon/MEMORY_SCHEMA.md"
  created: 2026-05-10
  type: schema
  summary: "SIPHON Week 1 concrete session extraction schema with validation rules and six bootstrap examples"
  portable_to:
    - context: "when implementing SIPHON extraction, validation, compression, or MEMORY.md append logic"
    - context: "when evaluating whether L8 rating can move beyond schema design"
  trigger: "before any code is written in BUILD/siphon/"
  status: active
  session_origin: session-003
  superseded_by: null

- artifact: "COMPARE/_STEAL.md"
  created: 2026-05-10
  type: protocol
  summary: "Build-first steal ledger narrowed to the five mechanics that matter after Research Batch 001"
  portable_to:
    - context: "when selecting the next artifact to build from competitive research"
  trigger: "after reading STATE.yaml and before starting non-SIPHON implementation"
  status: active
  session_origin: session-003
  superseded_by: null

- artifact: "COMPARE/claude-filtrado-src-2026-03-31.md"
  created: 2026-05-10
  type: reference
  summary: "Steal map for Claude desktop/client snapshot — cost aggregates, token budget stop, memdir selective recall, MCP degraded UX"
  portable_to:
    - context: "when designing VENOCTIS metrics and L13 metabolic policy"
    - context: "when tightening SIPHON pre-load vs on-demand MEMORY selection"
  trigger: "before implementing cost/budget dashboards or automatic memory prefetch"
  status: active
  session_origin: session-004
  superseded_by: null

- artifact: "COMPARE/claude-filtrado-src-2026-03-31/"
  created: 2026-05-10
  type: tool
  summary: "Read-only reference tree (~1.9k files); license unknown — mechanics only"
  portable_to:
    - context: "grep-level archaeology for session UX, telemetry, migrations"
  trigger: "only when extracting a named mechanic into VENOM-owned BUILD docs or code after license gate"
  status: active
  session_origin: session-004
  superseded_by: null

- artifact: "COMPARE/NousResearch/hermes-sessions/"
  created: 2026-05-10
  type: reference
  summary: "Raw session transcripts from Hermes agent"
  portable_to:
    - context: "when analyzing how Hermes structures its memory and conversational logs"
  trigger: "before finalizing SIPHON extraction formats or memory recall mechanisms"
  status: active
  session_origin: session-006
  superseded_by: null

- artifact: "COMPARE/openclaw-data/"
  created: 2026-05-10
  type: reference
  summary: "Raw session data and cron logs from OpenClaw"
  portable_to:
    - context: "when analyzing background task persistence and session state in OpenClaw"
  trigger: "before implementing temporal rhythms or background cron-like execution"
  status: active
  session_origin: session-006
  superseded_by: null

- artifact: "COMPARE/venom-vs-field.md"
  created: 2026-05-10
  type: reference
  summary: "Honest competitive positioning matrix vs Hermes, OpenClaw, Claude Code, Pi, and OpenCode"
  portable_to:
    - context: "when evaluating whether to build a feature or adopt an existing tool"
  trigger: "before expanding scope beyond VENOM's core differentiators (reciprocity, siphon, pact-voice)"
  status: active
  session_origin: session-009
  superseded_by: null
