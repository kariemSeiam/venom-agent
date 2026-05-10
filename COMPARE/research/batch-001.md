# Research Batch 001 — Agent Memory, Durable Arms, Metabolism

Date: 2026-05-10
Purpose: Find open-source projects and papers that move VENOM layer ratings or remove blockers.
Status: Canonical research artifact.

---

## Candidate Index

| # | Candidate | Link | Layers | Priority |
|---|-----------|------|--------|----------|
| 1 | Memento | https://github.com/diego-ninja/memento | L8+L9 | P0 |
| 2 | Context-Compactor | https://github.com/HalfEmptyDrum/Context-Compactor | L3+L8 | P0 |
| 3 | Agent-Memory-Compressor | https://github.com/dakshjain-1616/Agent-Memory-Compressor | L8+L13 | P0 |
| 4 | Letta | https://github.com/letta-ai/letta | L8+L11 | P0 |
| 5 | mem0 | https://github.com/mem0ai/mem0 | L9+L10 | P0 |
| 6 | Graphiti | https://github.com/getzep/graphiti | L9+L12 | P0 |
| 7 | Zep | https://github.com/getzep/zep | L9+L5 | P1 |
| 8 | SimpleMem | https://github.com/aiming-lab/SimpleMem | L9 | P1 |
| 9 | agentmemory | https://github.com/rohitg00/agentmemory | L9+L13 | P1 |
| 10 | Cognee | https://github.com/topoteretes/cognee | L9 | P1 |
| 11 | Supermemory | https://github.com/supermemoryai/supermemory | L9+L5 | P1 |
| 12 | DurableFuture | https://github.com/ngnhng/durablefuture | L4+L2 | P0 |
| 13 | NATS JetStream Go | https://github.com/nats-io/nats.go/tree/main/jetstream | L4 | P0 |
| 14 | LangGraph Postgres Checkpointer | https://github.com/langchain-ai/langgraph/tree/main/libs/checkpoint-postgres | L8 | P1 |
| 15 | Temporal Go SDK + agent-sdk-go | https://pkg.go.dev/go.temporal.io/sdk and https://pkg.go.dev/github.com/agenticenv/agent-sdk-go | L2+L4 | P1 |
| 16 | LiteLLM Router | https://github.com/BerriAI/litellm | L13 | P1 |
| 17 | ElizaOS Eliza | https://github.com/elizaOS/eliza | L4+L9 | P2 |
| 18 | Agent Memory Techniques | https://github.com/NirDiamant/Agent_Memory_Techniques | L9 | P2 |
| 19 | Hermes Agent | https://github.com/NousResearch/hermes-agent | L8+L11 | Already ingested |
| 20 | OpenClaw | https://github.com/openclaw/openclaw | L5+L8 | Already ingested |
| 21 | Pi Agent Harness | https://github.com/earendil-works/pi-mono | L4+L3 | Already ingested |
| 22 | MemGPT Paper | https://arxiv.org/abs/2310.08560 | L8+L3 | Paper |
| 23 | Voyager Paper | https://arxiv.org/abs/2305.16291 | L9+MOLT | Paper |

---

## Candidate Notes

### 1. Memento
- **Layer map:** L8+L9
- **Mechanic to steal:** Two-layer recall: structured memory for decisions/learnings/preferences plus transcript history with a hierarchical summary DAG and compaction-aware recovery.
- **VENOM reject / watch-out:** SQLite/Ollama defaults are not stack-aligned. Steal schema and lifecycle, not runtime.
- **Priority:** P0
- **Effort:** days

Memento is the closest SIPHON-shaped project in the batch: it captures session traces, indexes durable memory, and supports compaction recovery. VENOM should turn this into a Postgres + pgvector schema and extraction pipeline, not adopt the project whole.

### 2. Context-Compactor
- **Layer map:** L3+L8
- **Mechanic to steal:** Chunk long histories, summarize with stable identifiers, preserve continuity while freeing context.
- **VENOM reject / watch-out:** Summaries can hide false conclusions unless EDGE/MEND validation gates review them.
- **Priority:** P0
- **Effort:** hours

This is a direct primitive for SIPHON compression. The useful part is the invariant: every summary must preserve identifiers, decisions, unresolved blockers, and references back to raw trace boundaries.

### 3. Agent-Memory-Compressor
- **Layer map:** L8+L13
- **Mechanic to steal:** Importance scoring plus forgetting curve plus strategy selection: summarize, extract facts, or archive.
- **VENOM reject / watch-out:** Heuristics drift without Pact checks and explicit validation.
- **Priority:** P0
- **Effort:** days

VENOM needs metabolic awareness inside SIPHON. This candidate gives a policy for deciding what deserves memory write cost, what gets compressed, and what gets discarded.

### 4. Letta
- **Layer map:** L8+L11
- **Mechanic to steal:** Core memory vs external memory split, editable core blocks, pruning, and recursive summarization.
- **VENOM reject / watch-out:** Python-centric platform. Do not move the stack. Steal memory boundaries and tool contracts.
- **Priority:** P0
- **Effort:** weeks

Letta/MemGPT is the strongest architectural reference for stateful agents. VENOM should use it to define which memories are mantle-readable, which are external retrieval, and which are scratch artifacts.

### 5. mem0
- **Layer map:** L9+L10
- **Mechanic to steal:** User/session/agent memory levels with a disciplined memory API and benchmark framing.
- **VENOM reject / watch-out:** Managed memory service can centralize intelligence. Self-host or treat as reference.
- **Priority:** P0
- **Effort:** days

mem0 feeds two things: memory scope taxonomy and benchmark language. It is especially useful for deciding whether a memory belongs to user, session, or agent continuity.

### 6. Graphiti
- **Layer map:** L9+L12
- **Mechanic to steal:** Temporal knowledge graph with episodic ingestion, temporal invalidation, and hybrid search.
- **VENOM reject / watch-out:** Neo4j-heavy default. VENOM must map to Postgres/pgvector or isolate graph support behind an adapter.
- **Priority:** P0
- **Effort:** weeks

Graphiti is the strongest reference for SACK after SIPHON. Temporal validity matters because old corrections can expire, project status changes, and personality must evolve without stale facts poisoning the next session.

### 7. Zep
- **Layer map:** L9+L5
- **Mechanic to steal:** Context assembly pipeline that turns raw messages, business data, and events into LLM-ready context blocks.
- **VENOM reject / watch-out:** Overlaps Graphiti; do not run two graph memories.
- **Priority:** P1
- **Effort:** days

Zep is more useful as retrieval-product inspiration than as immediate code. Its main steal is context packaging: what gets loaded before first token.

### 8. SimpleMem
- **Layer map:** L9
- **Mechanic to steal:** Lifelong memory with MCP integration and LoCoMo-style evaluation framing.
- **VENOM reject / watch-out:** Too broad for Week 1 SIPHON. Use as eval reference.
- **Priority:** P1
- **Effort:** days

SimpleMem provides test vocabulary for measuring memory quality. VENOM should steal benchmarks, not another memory store.

### 9. agentmemory
- **Layer map:** L9+L13
- **Mechanic to steal:** Confidence scoring, lifecycle management, and retrieval cost framing.
- **VENOM reject / watch-out:** Keep TS code in arms if used; SOMA remains Go.
- **Priority:** P1
- **Effort:** days

This is useful for rating memory entries and minimizing token cost. It belongs after the schema exists.

### 10. Cognee
- **Layer map:** L9
- **Mechanic to steal:** `memify()` as a named graph hygiene phase: prune stale nodes and add derived facts.
- **VENOM reject / watch-out:** Extraction cost needs metabolic caps.
- **Priority:** P1
- **Effort:** days

Cognee’s strongest contribution is not RAG; it is memory maintenance as a first-class operation.

### 11. Supermemory
- **Layer map:** L9+L5
- **Mechanic to steal:** Contradiction handling, automatic forgetting, profile retrieval, and MCP surface.
- **VENOM reject / watch-out:** Cloud-first bias can violate clean death boundaries.
- **Priority:** P1
- **Effort:** days

Supermemory is useful for contradiction semantics: when newer memory defeats older memory, the system must mark rather than silently overwrite.

### 12. DurableFuture
- **Layer map:** L4+L2
- **Mechanic to steal:** Workflow/worker split backed by NATS JetStream persistence.
- **VENOM reject / watch-out:** Do not inherit Temporal-style central semantics. SOMA owns the mesh.
- **Priority:** P0
- **Effort:** days

This is the best stack-aligned candidate for two-arm execution. It maps directly to durable HUNT and WELD work loops.

### 13. NATS JetStream Go
- **Layer map:** L4
- **Mechanic to steal:** Durable consumers, ACK/replay, consumer groups, KV/object store patterns.
- **VENOM reject / watch-out:** The risk is making JetStream the brain. It is mailboxes only.
- **Priority:** P0
- **Effort:** hours

NATS is already locked. The research confirms it should be the first substrate for arms, not a later optimization.

### 14. LangGraph Postgres Checkpointer
- **Layer map:** L8
- **Mechanic to steal:** Checkpoint table discipline, time-travel/debugging model, sync/async saver split.
- **VENOM reject / watch-out:** LangGraph workflow graphs can become a shell. Do not adopt orchestration.
- **Priority:** P1
- **Effort:** days

LangGraph’s checkpointer is valuable as schema inspiration for resumable state, not as VENOM’s execution model.

### 15. Temporal Go SDK + agent-sdk-go
- **Layer map:** L2+L4
- **Mechanic to steal:** Durable execution that survives crash/deploy, with workflows, activities, signals, and queries.
- **VENOM reject / watch-out:** Heavy operations and central orchestration pressure. Requires full COMPARE before any stack decision.
- **Priority:** P1
- **Effort:** weeks

Temporal is the serious alternative to a JetStream-only durable workflow model. It should stay in compare until SOMA proves whether it needs more.

### 16. LiteLLM Router
- **Layer map:** L13
- **Mechanic to steal:** Cost-aware routing, TPM/RPM budgets, fallbacks, retries, lowest-cost strategy.
- **VENOM reject / watch-out:** Gateway can become a fixed shell. If used, it stays sidecar or reference.
- **Priority:** P1
- **Effort:** days

LiteLLM is the obvious source for metabolic model routing. VENOM should translate routing policy into its own arm model-selection logic.

### 17. ElizaOS Eliza
- **Layer map:** L4+L9
- **Mechanic to steal:** Memory taxonomy: MESSAGE, FACT, DOCUMENT, RELATIONSHIP, GOAL, TASK, ACTION.
- **VENOM reject / watch-out:** Social-agent sprawl. Do not import the world.
- **Priority:** P2
- **Effort:** hours

ElizaOS is useful as a taxonomy check against SIPHON’s session extraction schema.

### 18. Agent Memory Techniques
- **Layer map:** L9
- **Mechanic to steal:** Catalog of memory patterns and notebooks for graph memory experimentation.
- **VENOM reject / watch-out:** Tutorial material, not production substrate.
- **Priority:** P2
- **Effort:** hours

Use this as study material when designing SACK retrieval modes.

### 19. Hermes Agent
- **Layer map:** L8+L11
- **Mechanic to steal:** FTS session search, self-improving skills, cross-platform continuity.
- **VENOM reject / watch-out:** Already ingested under `COMPARE/NousResearch/`.
- **Priority:** ingested
- **Effort:** n/a

Hermes remains the main comparison for skill growth and cross-session personality.

### 20. OpenClaw
- **Layer map:** L5+L8
- **Mechanic to steal:** Gateway/session tools and multi-channel skin.
- **VENOM reject / watch-out:** Heavy gateway can conflict with shell.null.
- **Priority:** ingested
- **Effort:** n/a

OpenClaw is a useful Skin and always-on runtime comparison.

### 21. Pi Agent Harness
- **Layer map:** L4+L3
- **Mechanic to steal:** Session trace exports and differential TUI rendering.
- **VENOM reject / watch-out:** Already ingested; do not duplicate.
- **Priority:** ingested
- **Effort:** n/a

Pi remains useful for trace capture and developer feedback loops.

### 22. MemGPT Paper
- **Layer map:** L8+L3
- **Mechanic to steal:** Virtual context paging and explicit control transfer between context and external storage.
- **VENOM reject / watch-out:** Academic chat framing; must be measured against VENOM sessions.
- **Priority:** P1
- **Effort:** days

MemGPT is the theoretical spine behind Letta. It should inform schema vocabulary and memory paging.

### 23. Voyager Paper
- **Layer map:** L9+MOLT
- **Mechanic to steal:** Skill library growth from execution feedback.
- **VENOM reject / watch-out:** Game-domain bias. Only the skill-accretion mechanic survives.
- **Priority:** P2
- **Effort:** days

Voyager is a later-stage MOLT/SACK reference, not a Week 1 SIPHON dependency.

---

## Top 5 Build-First Steals

1. **Context-Compactor rolling summaries with stable IDs** -> `BUILD/siphon/MEMORY_SCHEMA.md` and later `BUILD/siphon/compress.*`; moves L8/L3 by defining loss boundaries.
2. **DurableFuture / NATS JetStream workflow-worker split** -> `BUILD/soma/` two-arm HUNT/WELD actor prototype; moves L4/L2 after SIPHON baseline.
3. **Agent-Memory-Compressor scoring policy** -> `BUILD/siphon/` extraction policy for what gets flushed, summarized, archived, or wiped; feeds L8/L13.
4. **Letta core vs external memory split** -> `BUILD/siphon/MEMORY_SCHEMA.md` memory tiers and Mantle-safe field rules; feeds L1/L8/L9.
5. **Graphiti temporal hybrid retrieval** -> later `MEMORY/SACK.md` retrieval design and Postgres/pgvector-compatible indexing plan; feeds L9/L12.
