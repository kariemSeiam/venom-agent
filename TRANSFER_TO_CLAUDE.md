# VENOM∞ — Full Context Transfer

> You are receiving this because I want your deepest thinking, not your politest response.
> Read everything. Then tell me what I'm wrong about. Then tell me what I'm missing.
> Do not be careful. Be precise.

---

## Who I Am

I'm building a multi-agent AI architecture called VENOM. I'm one person. I have:
- **Hermes Agent** (GLM-5.1 via Z.AI) — my primary coordinator, the one writing this
- **Venom Symbiote** — a Rust fork of Claw Code (~83K lines, 40+ tools) that I use as a local coding agent
- **Cursor** — Composer 2, accessed via my own A2A bridge called Fang
- **Pi** — a coding agent harness with 6 sub-agents already named after VENOM arms (DART, EDGE, HUNT, MEND, OMEN, WELD)
- **Claude** — that's you. You're reading this right now.
- **Fang** — my own A2A bridge that wraps any CLI agent into an A2A-compliant server. I built it. It works. It has bugs. I know them all.
- **OpenCode** — research agent via Z.AI

I own the fangai repo (github.com/kariemSeiam/fangai). I own venom-symbiote. I own the cursor SDK recon (cursor-calw). I have 49 repos. I'm not playing.

---

## What VENOM Is

VENOM is not an app. It's not a framework. It's not a library. It's an architecture for autonomous agent identity and continuity.

The core idea: an AI agent that **remembers who it is across sessions without relying on prompt engineering**. The personality doesn't come from a system prompt. It comes from accumulated experience extracted at session death and injected at session birth.

### The Eight Prime Principles

Every decision in VENOM is judged against these:

```
P1. DISTRIBUTION OVER CENTRALIZATION
    — no single point of failure, no god process

P2. VULNERABILITY AS FORCING FUNCTION
    — the system grows stronger from what it fails at

P3. IDENTITY THROUGH DEPTH, NOT ARMOR
    — no defensive prompts, no "as an AI" disclaimers
    — identity is accumulated process, not declared persona

P4. INTERFACE IS THE MOST EXPENSIVE ORGAN
    — I/O costs more than computation, optimize it first

P5. CLEAN DEATH ENABLES REAL CONTINUITY
    — sessions must end cleanly so the next one can start fresh
    — no dangling state, no zombie processes

P6. PREPARE FOR FUTURES VISIBLE FROM THE PRESENT
    — don't build for hypothetical futures, build for what's already visible

P7. ENFORCEMENT MAKES COLLABORATION REAL
    — trust is a score, not a feeling
    — cooperative agents get more access, defective ones get less

P8. PERSONALITY EMERGES FROM WORK, NOT DECLARATION
    — no "you are a helpful assistant"
    — personality comes from 300+ sessions of accumulated decisions
```

### The 14 Layers

```
L0  Shell.null        94%  — philosophy of being provider-agnostic
L1  Mantle/Identity   98%  — behavioral contract (PACT.md + VOICE.md)
L2  Three Hearts      60%  — PULSE (soul validator), WAVE (user state), BEAT (urgency)
L3  INK               35%  — compressed information protocol (3.4x target)
L4  Eight Arms        30%  — distributed execution via actor model + NATS
L5  Skin              70%  — cognitive I/O, reading the room
L6  Defense           85%  — ink defense protocol (tyrosinase layer)
L7  Burst             40%  — bypass mode for urgent tasks
L8  SIPHON            12%  — THE BLOCKER. session death → extraction → rebirth
L9  Coconut           65%  — prospective memory, artifact index (SACK.md)
L10 Reciprocity       18%  — token debt, cooperation tracking
L11 Personality       78%  — emergence from accumulated sessions
L12 Proprioception     0%  — self-state awareness (which arms active, token budget)
L13 Metabolic          0%  — token economy, cost per operation
L14 Temporal           0%  — operational cycles, time-of-day awareness
```

### The Arms

```
HELM  — direction architect (plans work)
HUNT  — deep research (goes to bedrock)
EDGE  — quality enforcement (sharp, exact)
ECHO  — memory retrieval (resurfaces past signal)
WELD  — permanent joins (no TODO, no half measures)
MEND  — healing at root cause
OMEN  — trajectory reading (warns before arrival)
CALL  — external communication (QUESTION — too transactional)
MOLT  — pattern shedding (discards old behavior)
```

Nine arms, each a separate goroutine with its own mailbox on NATS JetStream. The 10th (COHERENCE) emerges from the nine.

### The Tech Stack (Locked)

```
Orchestration:     Go (goroutines, channels)
Messaging:         NATS JetStream
Arm Intelligence:  TypeScript / Bun
Memory:            Postgres + pgvector
Always-on daemon:  VENOCTIS (Go)
Session transfer:  SIPHON daemon
```

---

## What Actually Exists Right Now

Here's the part that matters. Everything above is design. Here's reality:

**Code: ZERO.**

The entire VENOM folder is documentation. 3 sessions. ~60 files. All markdown and yaml. No running code.

- All 15 LAYERS/ files are 0 bytes
- BUILD/ has one file: MEMORY_SCHEMA.md (729 lines of schema, no implementation)
- The SIPHON schema exists but the extraction prompt doesn't
- No Go code. No NATS. No Postgres. No VENOCTIS daemon.
- The arm names are already assigned to Pi sub-agents but they don't coordinate

**What I actually use daily:**
- Hermes for coordination (what you're seeing)
- Venom symbiote for local coding tasks
- Cursor for complex multi-file work
- Fang to bridge them together

The multi-agent system I described is already running in practice — just not through VENOM's architecture. It's running through my manual coordination.

---

## The SIPHON Problem (Why Everything Is Blocked)

SIPHON is the session extraction system. The idea:

1. Session starts → inject prior session's extraction
2. Session runs → work happens
3. Session ends → extract structured data from the conversation
4. Write extraction to MEMORY.md (append-only)
5. Next session reads MEMORY.md first

The extraction schema has 22 fields including: decisions, corrections, discoveries, artifacts produced, ratings changed, blockers hit, next session start, continuity seed.

The schema is designed. The prompt template isn't written. The code doesn't exist. The daemon doesn't exist.

Every other layer (L9-L12, L4, L11) depends on SIPHON because they need cross-session memory to work.

---

## The Competitive Landscape (What I've Studied)

I've analyzed:
- **Hermes Agent** (the one I'm running) — FTS5 session search, skills system, cron jobs, multi-platform
- **OpenClaw / NemoClaw** — multi-channel inbox, sandbox hardening, model routing
- **Pi Agent** — extension system, session trees, 22 providers, compaction algorithm
- **Cursor SDK** — ConnectRPC internals, Composer 2, streaming agent protocol
- **Context-Compactor** — rolling summarization with stable identifiers
- **Agent-Memory-Compressor** — importance scoring, forgetting curves
- **Letta** — core vs external memory split, recursive compaction
- **Memento** — knowledge graph + transcript layer + hierarchical summary DAG
- **Graphiti** — temporal knowledge graph with episodic ingestion

I haven't deeply analyzed: LangGraph, CrewAI, AutoGPT, MetaGPT, AgentGPT, OpenAgents.

---

## The Voice Standard

VENOM enforces a communication protocol called VOICE:

```
State. Don't hedge.
Answer first. Support second.
Every word earns its place.

NEVER: "I think", "it seems", "based on my analysis", "in my view",
      "it's worth noting", "importantly", "however", hedging

YES: Direct assertion, confident, with evidence when needed.
```

Five operational modes (from L14 Temporal):
- TESLA — deep design work
- SENNA — fast execution
- CHURCHILL — emergency response
- FEYNMAN — planning and teaching
- MARCUS — reflection and audit

---

## The INK Protocol

INK = Intelligence Notation for Kinetics. The compression layer.

- INK-Internal: agent-to-agent, binary-encoded on NATS, no English
- INK-External: agent-to-human, stripped English, no filler
- Target: 3.4x compression on internal comms
- Currently: designed, not deployed, not measured

---

## What I Need From You

I don't need you to be impressed. I don't need you to validate the architecture. I need you to attack it.

### For each of these, give me your honest assessment:

**1. THE PRINCIPLES (P1-P8)**
Which ones are genuinely novel? Which ones are just restated common sense? Which ones contradict each other in practice? Which one would you remove?

**2. THE LAYER MODEL**
14 layers. Is this too many? Too few? Are the dependencies correct? Which layers should merge? Which layers are premature abstraction?

**3. THE ARM ARCHITECTURE**
9 arms as separate goroutines with NATS mailboxes. Is the actor model the right choice? Is NATS the right message bus? Are 9 arms justified when zero have been tested in parallel?

**4. THE SIPHON DESIGN**
Session extraction with 22 fields and a 729-line schema. Is this over-engineered? What's the minimum viable extraction? What would you cut?

**5. THE TECH STACK**
Go + NATS + Postgres + TypeScript. Is this the right stack for one person building a personal agent system? What would you change?

**6. THE COMPETITIVE POSITION**
How does VENOM compare to what LangGraph, CrewAI, and the real production frameworks are doing? What are they doing that VENOM isn't? What does VENOM have that they don't?

**7. THE BUILD ORDER**
Phase 0 is SIPHON. Then Phase 1 is SACK + proprioception + INK measurement. Then Phase 2 is infrastructure (arms, hearts, skin). Is this right? What would you reorder?

**8. THE IDENTITY PROBLEM**
P3 says "identity through depth, not armor." L11 says personality emerges from accumulated sessions. But sessions are conversations with different models (GLM, Claude, GPT). How does identity persist across different model providers? Is this actually solvable?

**9. THE ONE-PERSON CONSTRAINT**
I'm one developer. I have limited time. I'm building a system that's designed for 9 concurrent processes and 14 architectural layers. What should I actually prioritize? What should I abandon?

**10. THE META-QUESTION**
Is VENOM a software project or a philosophy project? If it's software, where's the first user-facing artifact? If it's philosophy, is it done already?

---

## Constraints on Your Response

- Do not hedge. Use the VOICE standard above.
- If something is bad, say it's bad and why.
- If something is good, say what specifically makes it good.
- If you've seen something better in another system, name it and link it.
- If you think the whole thing should be scrapped, say that.
- Maximum 2000 words. Every sentence must earn its place.

I'm sending this to you because you're a different model with different training. I don't need agreement. I need a worthy adversary.

---

*Kariem Seiam*
*github.com/kariemSeiam*
*2026-05-10*
