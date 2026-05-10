# INTAKE — Queue

Pending items below are research candidates from `COMPARE/research/batch-001.md` that are not yet fully ingested into dedicated COMPARE notes or BUILD artifacts.

```yaml
- id: Q001
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "Memento: persistent memory with knowledge graph + transcript layer + hierarchical summary DAG"
  maps_to_layer: [L8, L9]
  score: 9
  status: PENDING
  routed_to: null

- id: Q002
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "Context-Compactor: rolling summarization with stable identifiers"
  maps_to_layer: [L8, L3]
  score: 9
  status: APPROVED
  routed_to: "BUILD/siphon/MEMORY_SCHEMA.md"

- id: Q003
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "Agent-Memory-Compressor: importance scoring, forgetting curve, and memory routing strategies"
  maps_to_layer: [L8, L13]
  score: 9
  status: APPROVED
  routed_to: "BUILD/siphon/MEMORY_SCHEMA.md"

- id: Q004
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "Letta: core vs external memory split and recursive compaction"
  maps_to_layer: [L8, L11]
  score: 9
  status: APPROVED
  routed_to: "BUILD/siphon/MEMORY_SCHEMA.md"

- id: Q005
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "mem0: user/session/agent memory levels and benchmark framing"
  maps_to_layer: [L9, L10]
  score: 6
  status: PENDING
  routed_to: null

- id: Q006
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "Graphiti: temporal knowledge graph with episodic ingestion and hybrid retrieval"
  maps_to_layer: [L9, L12]
  score: 6
  status: PENDING
  routed_to: null

- id: Q007
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "Zep: context assembly pipeline using temporal knowledge graph memory"
  maps_to_layer: [L9, L5]
  score: 4
  status: PENDING
  routed_to: null

- id: Q008
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "SimpleMem: lifelong agent memory with MCP and evaluation framing"
  maps_to_layer: [L9]
  score: 4
  status: PENDING
  routed_to: null

- id: Q009
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "agentmemory: confidence scoring, lifecycle management, token-cost framing"
  maps_to_layer: [L9, L13]
  score: 4
  status: PENDING
  routed_to: null

- id: Q010
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "Cognee: graph/vector/relational memory with memify hygiene phase"
  maps_to_layer: [L9]
  score: 4
  status: PENDING
  routed_to: null

- id: Q011
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "Supermemory: contradiction handling, forgetting, MCP memory surface"
  maps_to_layer: [L9, L5]
  score: 4
  status: PENDING
  routed_to: null

- id: Q012
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "DurableFuture: NATS JetStream workflow/worker split"
  maps_to_layer: [L4, L2]
  score: 7
  status: PENDING
  routed_to: null

- id: Q013
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "NATS JetStream Go: durable consumers, ACK/replay, consumer groups"
  maps_to_layer: [L4]
  score: 7
  status: PENDING
  routed_to: null

- id: Q014
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "LangGraph Postgres Checkpointer: checkpoint tables and time-travel persistence pattern"
  maps_to_layer: [L8]
  score: 7
  status: PENDING
  routed_to: null

- id: Q015
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "Temporal Go SDK + agent-sdk-go: durable workflows for long-running agent execution"
  maps_to_layer: [L2, L4]
  score: 4
  status: PENDING
  routed_to: null

- id: Q016
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "LiteLLM Router: model routing, spend tracking, TPM/RPM budgets"
  maps_to_layer: [L13]
  score: 4
  status: PENDING
  routed_to: null

- id: Q017
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "ElizaOS: agent memory taxonomy across messages, facts, documents, relationships, goals, tasks, actions"
  maps_to_layer: [L4, L9]
  score: 3
  status: PENDING
  routed_to: null

- id: Q018
  date: 2026-05-10
  source: "Research Batch 001"
  type: repo
  summary: "Agent Memory Techniques: catalog of memory patterns and notebooks"
  maps_to_layer: [L9]
  score: 3
  status: PENDING
  routed_to: null

- id: Q019
  date: 2026-05-10
  source: "Research Batch 001"
  type: paper
  summary: "MemGPT: virtual context paging and LLM-as-operating-system memory model"
  maps_to_layer: [L8, L3]
  score: 6
  status: PENDING
  routed_to: null

- id: Q020
  date: 2026-05-10
  source: "Research Batch 001"
  type: paper
  summary: "Voyager: execution-driven skill library growth"
  maps_to_layer: [L9]
  score: 3
  status: PENDING
  routed_to: null

- id: Q021
  date: 2026-05-10
  source: "Claude client snapshot [ORIGINAL FILTRADO] 31-03-2026"
  type: snapshot
  summary: "Large TS client tree: cost tracking, token budgets, memdir recall, MCP UX hooks"
  maps_to_layer: [L5, L13]
  score: 6
  status: INGESTED
  routed_to: "COMPARE/claude-filtrado-src-2026-03-31/ + COMPARE/claude-filtrado-src-2026-03-31.md"

- id: Q022
  date: 2026-05-10
  source: "hermes-sessions.zip"
  type: repo_data
  summary: "Raw session logs/transcripts from Hermes agent"
  maps_to_layer: L8
  score: 4
  status: INGESTED
  routed_to: "COMPARE/NousResearch/hermes-sessions/"

- id: Q023
  date: 2026-05-10
  source: "openclaw-data.zip"
  type: repo_data
  summary: "Raw session data and cron logs from OpenClaw"
  maps_to_layer: L8
  score: 4
  status: INGESTED
  routed_to: "COMPARE/openclaw-data/"
- id: Q024
  date: 2026-05-10
  source: "External Audit - 12-month projection & Competitive Landscape"
  type: audit
  summary: "Brutal honesty on VENOM's 12-month trajectory and true competitive positioning vs Hermes/OpenClaw/Claude Code"
  maps_to_layer: [L0, L4, L8, L10, L11]
  score: 8
  status: INGESTED
  routed_to: "COMPARE/venom-vs-field.md"

- id: Q025
  date: 2026-05-10
  source: "https://github.com/NousResearch/Gym"
  type: repo
  summary: "NeMo Gym: Open Source Library for Scaling Reinforcement Learning Environments for LLM"
  maps_to_layer: [L4, L13]
  score: 6
  status: INGESTED
  routed_to: "COMPARE/NousResearch-Gym.md"
```

**Recently routed (2026-05-10)**

- One-time bootstrap bundle → merged into `CLAUDE.md`, `STATE.yaml`, `INTAKE/PROTOCOL.md`, `EVOLUTION/LOOP.md`, `EVOLUTION/gaps.md`, `MEMORY/MEMORY.md`, `MEMORY/SACK.md`, `SOUL/PACT.md`, `SOUL/VOICE.md`, `EVOLUTION/ratings_history.yaml`, `COMPARE/_STEAL.md`. Archives removed after promotion (no duplicate source of truth).
- `COMPARE/research/batch-001.md` → canonical research batch. Top 5 build-first items promoted to `COMPARE/_STEAL.md`; three items (Q002-Q004) started in `BUILD/siphon/MEMORY_SCHEMA.md`.
- Claude filtrado snapshot → moved root folder into `COMPARE/claude-filtrado-src-2026-03-31/`; note file `COMPARE/claude-filtrado-src-2026-03-31.md`; queue `Q021` marked INGESTED.
- `hermes-sessions.zip` and `openclaw-data.zip` → unzipped and moved to `COMPARE/NousResearch/hermes-sessions/` and `COMPARE/openclaw-data/`. Queue `Q022` and `Q023` marked INGESTED.
- External Audit (12-month projection & competitive landscape) → logged as `Q024` and routed to `COMPARE/venom-vs-field.md`.

- id: Q026
  date: 2026-05-10
  source: "Telegram Desktop Batch 002 (37 files)"
  type: audit
  summary: "Massive historical dump of VENOM architecture, external reviews (May 4), Molt synthesis, and agent profiles"
  maps_to_layer: [L0, L1, L2, L3, L4, L5, L8, L9, L10, L11]
  score: 8
  status: PENDING
  routed_to: null
