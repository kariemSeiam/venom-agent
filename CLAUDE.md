# VENOM∞ — Claude Code Environment
## Project Intelligence Brief

> This folder is not a codebase. It is a living architecture.
> Every file either feeds the system or gets wiped.
> Read STATE.yaml before every session. Update it before you leave.

---

## What You Are Operating In

VENOM is a multi-layer AI agent architecture built on 8 prime principles.
It is currently at **57% overall implementation** across 14 layers.
Your job: implement, validate, compare, evolve — in that order.

**Before doing anything:**
1. Read `STATE.yaml` → know current ratings + blockers
2. Read `MEMORY/MEMORY.md` → know what happened last session
3. Read `INTAKE/QUEUE.md` → know what new data is waiting
4. Then act.

---

## Folder Map

```
venom/
├── CLAUDE.md              ← YOU ARE HERE (read every session)
├── STATE.yaml             ← master truth: ratings, blockers, build order
│
├── SOUL/                  ← immutable core (never refactor without explicit permission)
│   ├── PACT.md            ← values + behavioral contracts
│   ├── PROFILE.md         ← operational character
│   └── VOICE.md           ← communication standard + anti-patterns
│
├── MEMORY/                ← what persists across sessions
│   ├── MEMORY.md          ← session extractions (SIPHON output, append-only)
│   ├── corrections.yaml   ← behavioral corrections log
│   └── SACK.md            ← queryable artifact index
│
├── LAYERS/                ← one file per architecture layer
│   ├── L0_shell.md        ← 94% — shell.null philosophy
│   ├── L1_mantle.md       ← 98% — identity + mantle
│   ├── L2_hearts.md       ← 60% — three hearts orchestration
│   ├── L3_ink.md          ← 35% — INK information currency
│   ├── L4_arms.md         ← 30% — eight arms distributed execution
│   ├── L5_skin.md         ← 70% — cognitive I/O
│   ├── L6_defense.md      ← 85% — ink defense protocol
│   ├── L7_burst.md        ← 40% — jet propulsion burst mode
│   ├── L8_siphon.md       ← 12% — THE BLOCKER (build first)
│   ├── L9_coconut.md      ← 65% — prospective memory
│   ├── L10_reciprocity.md ← 18% — enforcement system
│   ├── L11_personality.md ← 78% — personality emergence
│   ├── L12_proprioception.md ← 0% — self-state awareness
│   ├── L13_metabolic.md   ← 0%  — token economy
│   └── L14_temporal.md    ← 0%  — operational cycles
│
├── COMPARE/               ← competitive intelligence
│   ├── langgraph.md
│   ├── crewai.md
│   ├── autogpt.md
│   └── _STEAL.md          ← what we take from each
│
├── EVOLUTION/             ← validation + evolution loop
│   ├── LOOP.md            ← the evolution protocol
│   ├── ratings_history.yaml ← rating changes over time
│   └── gaps.md            ← what's missing, what's less
│
├── BUILD/                 ← actual implementation
│   ├── soma/              ← Go orchestration server
│   ├── arms/              ← TypeScript arm intelligence
│   ├── siphon/            ← SIPHON daemon
│   └── venoctis/          ← always-on telemetry
│
├── AUDIT/                 ← deep audits (like VENOM∞-v2.md)
│   └── archive/
│
└── INTAKE/                ← data ingestion + validation
    ├── PROTOCOL.md        ← how data enters the system
    ├── QUEUE.md           ← pending data to evaluate
    └── WIPED.md           ← what was rejected and why
```

---

## The Eight Prime Principles
*(Every decision in this folder is judged against these)*

```
P1. DISTRIBUTION OVER CENTRALIZATION
P3. IDENTITY THROUGH DEPTH AND ARMOR
P4. INTERFACE IS THE MOST EXPENSIVE ORGAN
P5. CLEAN DEATH ENABLES REAL CONTINUITY
P6. PREPARE FOR FUTURES VISIBLE FROM THE PRESENT
P7. ENFORCEMENT MAKES COLLABORATION REAL
P8. PERSONALITY IS PORTABLE CONDITIONING
```

If a proposed change violates any of these → flag it before building.
If it violates P1, P3, or P5 → do not build without explicit override from Pigo.

---

## Build Order (Current Phase)

```
PHASE 0 — RUNTIME
└── L8: SIPHON v0
    → siphon.ts (4 fields)
    → Run for 20 sessions

PHASE 1 — AFTER 20 SESSIONS
├── L9: SACK.md artifact index
└── L4: Two-arm TS test (DIG + WELD parallel)

PHASE 2 — INFRASTRUCTURE
└── L2: Sequential TS dispatcher
```

---

## How to Work in This Folder

### When adding new code:
1. Check which LAYER it belongs to
2. Check if it advances or blocks the current PHASE
3. If it advances → build it, update STATE.yaml rating
4. If it's neutral → put in BUILD/ and note in MEMORY.md
5. If it blocks → flag in EVOLUTION/gaps.md

### When adding data / research / external content:
→ **Use INTAKE/PROTOCOL.md** — do not inject raw data into LAYERS/

### When comparing with open-source tools:
→ Add to COMPARE/ folder
→ Immediately extract what to steal into COMPARE/_STEAL.md
→ What VENOM does better → note in EVOLUTION/gaps.md (competitive gaps)

### When a session ends:
→ Update STATE.yaml (ratings if changed)
→ Append to MEMORY/MEMORY.md (what was built, decided, discovered)
→ Update INTAKE/QUEUE.md (what's waiting next)

---

## Data Quality Rules

All incoming data (papers, repos, ideas, audits) runs through INTAKE/PROTOCOL.md.

**Useful data signals:**
- Directly maps to a layer that's < 70%
- Introduces a principle that passes the P1-P8 filter
- Includes measurement (numbers, benchmarks, not just concepts)
- Enables SIPHON or removes a BLOCKER
- Teaches something about multi-agent coordination, memory, or actor models

**Wipe signals (log to WIPED.md):**
- Beautiful metaphor that adds no implementation path
- Already rated > 90% layer — don't optimize what's not broken
- Conflicts with SOUL/ without explicit permission to evolve it
- Duplicate concept already captured in LAYERS/
- Architecture intoxication: concept so elegant it feels like progress

**The test:** "Does this move a rating number up, or does it make the architecture more beautiful without moving anything?"
Beautiful without movement → WIPED.md.

---

## Technology Stack (Locked)

```
Orchestration:     TypeScript / Bun
Messaging:         In-process pub/sub
Arm Intelligence:  TypeScript / Bun
Memory:            SQLite (bun:sqlite) + Flat files
Daemon:            None
Session transfer:  siphon.ts (CLI)
```

Do not propose alternative stacks without a full comparative in COMPARE/.

---

## Voice Standard (Applies to all output in this folder)

```
State. Don't hedge.
Answer first. Support second.
Every word earns its place.
No: "I think", "it seems", "based on my analysis", "in my view"
Yes: Direct assertion, confident, with evidence when needed.
```

---

## Session End Checklist

Before closing any work session:
- [ ] STATE.yaml ratings updated
- [ ] MEMORY/MEMORY.md appended
- [ ] INTAKE/QUEUE.md updated
- [ ] Any new artifacts indexed to MEMORY/SACK.md
- [ ] EVOLUTION/gaps.md current

---

*VENOM∞ — 31% today. Direction: 100%. Destination: nonexistent.*
*The work is never done. That is the only correct relationship with perfection.*
