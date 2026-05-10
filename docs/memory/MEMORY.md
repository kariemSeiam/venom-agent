# MEMORY.md — Session Extractions
## Append-only. Never edit old entries. Never delete.

> This file is the soul of SIPHON.
> Every session that matters leaves a trace here.
> The next session reads this first.

---

## Schema (per entry)

```yaml
session:
  id: "session-NNN"
  date: YYYY-MM-DD
  duration_turns: 0
  
  decisions:              # explicit choices made this session
    - ""
    
  corrections:            # something was wrong and got fixed
    - ""
    
  discoveries:            # something not known before
    - ""
    
  artifacts_produced:     # files, specs, code, designs created
    - path: ""
      type: "code | spec | schema | design | protocol"
      
  ratings_changed:        # layer ratings that moved
    - layer: ""
      before: 0
      after: 0
      reason: ""
      
  blockers_hit:           # what stopped progress
    - ""
    
  next_session_start:     # first thing to do next session
    - ""
    
  pact_notes:             # anything related to SOUL/ or values
    - ""
```

---

## LOG

---
### session-001
date: 2026-05-10
duration_turns: 1

decisions:
  - "VENOM folder initialized as active project"
  - "CLAUDE.md established as the Claude Code environment prompt"
  - "STATE.yaml established as single source of truth"
  - "INTAKE protocol designed to filter bad data from architecture"
  - "EVOLUTION/LOOP.md established as session rhythm"

corrections: []

discoveries:
  - "The folder structure IS the first layer of SIPHON — before SIPHON exists, the folder structure enforces session continuity manually"

artifacts_produced:
  - path: "CLAUDE.md"
    type: spec
  - path: "STATE.yaml"
    type: schema
  - path: "INTAKE/PROTOCOL.md"
    type: protocol
  - path: "INTAKE/QUEUE.md"
    type: schema
  - path: "INTAKE/WIPED.md"
    type: schema
  - path: "MEMORY/MEMORY.md"
    type: schema
  - path: "MEMORY/SACK.md"
    type: schema
  - path: "EVOLUTION/LOOP.md"
    type: protocol
  - path: "COMPARE/_STEAL.md"
    type: protocol

ratings_changed: []

blockers_hit:
  - "L8 SIPHON still at 12% — folder structure is manual workaround"

next_session_start:
  - "Design MEMORY.md schema: 7 field types, 6 bootstrap entries (SIPHON Week 1)"
  - "Start COMPARE/ — pick one open-source agent to analyze"

pact_notes: []

---
### session-003
date: 2026-05-10
duration_turns: 1

decisions:
  - "Promoted Research Batch 001 into canonical repo state at COMPARE/research/batch-001.md"
  - "Reduced COMPARE/_STEAL.md to only the five build-first mechanics from Research Batch 001"
  - "Moved remaining non-ingested candidates into INTAKE/QUEUE.md"
  - "Started SIPHON Week 1 with BUILD/siphon/MEMORY_SCHEMA.md"
  - "Kept ratings unchanged; schema artifact exists, daemon and automation do not"

corrections: []

discoveries:
  - "SIPHON schema needs memory tiers, validation gates, and explicit continuity seed before extraction prompt work starts"
  - "Context-Compactor, Agent-Memory-Compressor, and Letta directly inform the first SIPHON schema artifact"

artifacts_produced:
  - path: "COMPARE/research/batch-001.md"
    type: reference
  - path: "BUILD/siphon/MEMORY_SCHEMA.md"
    type: schema

artifacts_modified:
  - path: "COMPARE/_STEAL.md"
    type: protocol
  - path: "INTAKE/QUEUE.md"
    type: schema
  - path: "MEMORY/SACK.md"
    type: schema
  - path: "MEMORY/MEMORY.md"
    type: schema

ratings_changed: []

blockers_hit:
  - "L8 SIPHON still lacks extraction prompt template, manual trigger prototype, automation, and VENOCTIS hook"

next_session_start:
  - "Write BUILD/siphon/EXTRACTION_PROMPT.md using BUILD/siphon/MEMORY_SCHEMA.md"
  - "Design the first manual SIPHON trigger prototype after the prompt template"

pact_notes:
  - "No rating inflation: Week 1 materially started, but L8 remains 12 until validation or executable prototype exists"

---
### session-002
date: 2026-05-10
duration_turns: 1

decisions:
  - "Imported one-time canonical bundle — master STATE.yaml, PROTOCOL, LOOP, SOUL/Voice+Pact, SACK scaffold, MEMORY schema"
  - "Merged OSS competitive steals (Pi, NemoClaw, OpenClaw, Hermes, Hermes self-evolution) into COMPARE/_STEAL.md"
  - "Restructured competitive gaps narrative into EVOLUTION/gaps.md COMPETITIVE GAPS section"
  - "Kept Hermes repos under COMPARE/NousResearch/ directory layout"
  - "Deleted zip + staging after promotion — canon only"

corrections: []

discoveries:
  - "One-time zip intake: promote into canon, then delete payload — lingering copies violate single-source truth"

artifacts_produced:
  - path: "COMPARE/pi.md"
    type: reference
  - path: "COMPARE/nemoclaw.md"
    type: reference
  - path: "COMPARE/openclaw.md"
    type: reference
  - path: "COMPARE/hermes-agent.md"
    type: reference
  - path: "COMPARE/hermes-agent-self-evolution.md"
    type: reference

ratings_changed: []

blockers_hit:
  - "L8 SIPHON daemon still unrealized — ingestion improved, execution unchanged"

next_session_start:
  - "SIPHON Week 1: finalize MEMORY.md field-level schema + bootstrap entries in BUILD/siphon/"
  - "Pick ONE repo from TO ANALYZE in _STEAL.md and ship a comparative note"

pact_notes: []

---
### session-004
date: 2026-05-10
duration_turns: 1

decisions:
  - "Promoted Claude [ORIGINAL FILTRADO] 31-03-2026 src tree into COMPARE/claude-filtrado-src-2026-03-31"
  - "Added COMPARE/claude-filtrado-src-2026-03-31.md steal map — reference only until license clarified"

corrections: []

discoveries:
  - "memdir/findRelevantMemories pairs header scan + selective recall (≤5) + mtime freshness — relevant to SACK preload limits"
  - "query/tokenBudget encodes diminishing-returns termination — transferable to arm continuation without importing UI shell"

artifacts_produced:
  - path: "COMPARE/claude-filtrado-src-2026-03-31.md"
    type: reference

artifacts_modified:
  - path: "INTAKE/QUEUE.md"
    type: schema
  - path: "MEMORY/SACK.md"
    type: schema
  - path: "STATE.yaml"
    type: schema

ratings_changed: []

blockers_hit:
  - "L8 daemon still unrealized; snapshot informs VENOCTIS and metabolic shapes only"

next_session_start:
  - "Optional: BUILD/venoctis/telemetry.md fields mirroring cost-tracker + tokenBudget decisions"

pact_notes:
  - "Third-party snapshot — reimplement mechanics in VENOM-owned BUILD paths after explicit license/legal gate"

---
### session-005
date: 2026-05-10
decisions:
  - "Accepted adversarial audit: architecture intoxication is real."
  - "Excised Go, NATS, and Postgres from the stack. Pivoted to TypeScript and flat files."
  - "Collapsed SIPHON schema from 22 fields to 4: decisions, corrections, next_action, current_truth."
  - "Deleted L12, L13, L14 from active tracking."
corrections:
  - "P2 (Vulnerability as forcing function) cut as excuse for brokenness."
  - "P8 vs P3 resolved: Identity is configured armor updated by work, not purely emergent."
  - "L11 (Personality) rating slashed from 78% to 10% — it's a portable conditioning bundle, not emergence."
next_action: "Run siphon.ts locally for the next 20 sessions before expanding architecture."
current_truth: "VENOM is a TypeScript runtime built around a 4-field memory extraction loop, stripped of all distributed systems theater."

---
session:
  id: "session-001"
  date: 2025-06-17
  decisions:
    - Reduced architecture from 9 arms to 2 arms (Planner and Executor) running in same process
    - Updated STATE.yaml to reflect L4 as "Two Arms / Local Execution" with MVP being HUNT and WELD running simultaneously
    - Removed P2 (Vulnerability as forcing function) from principles in CLAUDE.md and STATE.yaml
  corrections:
    - P2 was a flawed principle that rationalized broken code
    - 9-arm architecture was over-engineered for current needs
  next_action: "Build the sequential TypeScript dispatcher for L2"
  current_truth: "System runs a 2-arm architecture (Planner and Executor) in a single process, with HUNT and WELD as the simultaneous MVP and P2 removed from principles."

---
session:
  id: "session-001"
  date: 2025-01-20
  decisions:
    - Unzipped hermes-sessions.zip into COMPARE/NousResearch/hermes-sessions
    - Unzipped openclaw-data.zip into COMPARE/openclaw-data
    - Added both archives to INTAKE/QUEUE.md as Q022 and Q023
    - Indexed both as reference artifacts in MEMORY/SACK.md
  corrections: []
  next_action: "Process Q022 and Q023 from INTAKE/QUEUE.md according to INTAKE/PROTOCOL.md"
  current_truth: "Two archives (hermes-sessions, openclaw-data) are unzipped, queued as Q022/Q023, and indexed in MEMORY/SACK.md for session log analysis."

---
session:
  id: "session-008"
  date: 2025-05-09
  decisions:
    - Updated CLAUDE.md footer to reflect new 31% rating
    - Renamed DIG arm in documentation
    - Updated Phase 1 MVP to align with Session 007 audit
  corrections:
    - Previous documentation was out of alignment with Session 007 audit results
  next_action: "Proceed to next development phase or await further direction"
  current_truth: "CLAUDE.md and Phase 1 MVP are fully aligned with Session 007 audit, reflecting the 31% rating and renamed DIG arm."

---
session:
  id: "session-001"
  date: 2025-07-09
  decisions: ["VENOM positioned as specialized personal exocortex, not mass-market product", "Identified four unique VENOM advantages: reciprocity enforcement, session death/transfer via SIPHON, PACT-locked voice, true parallel execution", "Comparative framework established against OpenClaw, Claude Code, Hermes Agent, Pi, and OpenCode"]
  corrections: []
  next_action: "Deepen comparison on any specific axis if user requests, or proceed to next VENOM development task"
  current_truth: "VENOM differentiates from all alternatives through reciprocity enforcement, SIPHON session continuity, PACT-locked voice, and parallel execution, existing as a specialized personal exocortex rather than a general tool."

---
session:
  id: "session-009"
  date: 2026-05-10
  decisions:
    - "Ingested NousResearch/Gym repository into COMPARE/NousResearch-Gym.md"
    - "Extracted mechanic: Isolated verifiable reward environments for arm evaluation"
    - "Added steal to COMPARE/_STEAL.md for L4 (Arms) and L13 (Metabolic Awareness)"
    - "Logged Q025 in INTAKE/QUEUE.md as INGESTED"
  corrections: []
  next_action: "Run siphon.ts locally for the next 20 sessions before expanding architecture."
  current_truth: "NeMo Gym separates environment execution from the RL training loop, allowing independent testing and throughput scaling, which is directly applicable to evaluating VENOM's arms (WELD, DIG) with verifiable rewards."

---
session:
  id: "session-010"
  date: 2026-05-10
  decisions:
    - "Ingested 37 historical artifact files from Telegram Desktop into INTAKE/telegram-batch-002/"
    - "Generated canonical research index at COMPARE/research/telegram-batch-002.md"
    - "Extracted mechanic: TypeScript CLI Wrapper via Cursor SDK for L0_shell"
    - "Added steal to COMPARE/_STEAL.md for L0 (Shell.null) and L4 (Arms)"
    - "Logged Q026 in INTAKE/QUEUE.md as PENDING (partially ingested)"
  corrections: []
  next_action: "Run siphon.ts locally for the next 20 sessions before expanding architecture."
  current_truth: "The external reviews from May 4th are the exact source of the 'architecture intoxication' adversarial audit that triggered the current 31% rating. A working CLI wrapper for the Cursor SDK (ca.mjs) was already built by Kariem, providing a direct path to implement L0_shell."