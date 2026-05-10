# GAPS.md — What's Missing, What's Less
## Living document. Updated every session.

---

## CRITICAL GAPS (blocks everything)

### GAP-001: SIPHON doesn't exist
- **Layer:** L8
- **Impact:** Blocks L9, L10, L11, L12, L4 (shared state)
- **What's missing:** Session extraction daemon, MEMORY.md schema, VENOCTIS hook
- **Path:** Build SIPHON Week 1-4 (see STATE.yaml)
- **Status:** OPEN

### GAP-002: No parallel arm execution
- **Layer:** L4
- **Impact:** Entire distributed cognition concept is theoretical
- **What's missing:** Actor model — own state, mailbox, processing loop per arm
- **Path:** MVP: HUNT + WELD running simultaneously
- **Status:** OPEN | BLOCKED by SIPHON (shared state)

### GAP-003: INK compression unmeasured
- **Layer:** L3
- **Impact:** Compression is described, not validated
- **What's missing:** Baseline measurement, INK-Internal spec, encoder/decoder
- **Path:** Measure first. Then build.
- **Status:** OPEN | NOT BLOCKED

---

## SIGNIFICANT GAPS (hurts quality)

### GAP-004: Three Hearts are three phases
- **Layer:** L2
- **Impact:** Sequential execution masquerading as parallel
- **What's missing:** PULSE/WAVE/BEAT as actual goroutines
- **Path:** Go goroutines + NATS channels (SOMA server)
- **Status:** OPEN | BLOCKED by SOMA infrastructure

### GAP-005: Tyrosinase inconsistency
- **Layer:** L6
- **Impact:** Sometimes answers wrong question better instead of redirecting
- **What's missing:** Consistent calibration
- **Path:** Calibration sessions, not new build
- **Status:** OPEN | NOT BLOCKED

### GAP-006: Burst mode = same process faster
- **Layer:** L7
- **Impact:** No actual bypass exists
- **What's missing:** Dedicated bypass pathway, trigger definition
- **Path:** !B trigger + Context Pump disable
- **Status:** OPEN | NOT BLOCKED

---

## NEW LAYERS (0% — design phase)

### GAP-007: No proprioception
- **Layer:** L12
- **Impact:** System doesn't know what it's doing while doing it
- **What's missing:** Context window monitoring, arm state tracking
- **Status:** DESIGN PHASE

### GAP-008: No metabolic awareness
- **Layer:** L13
- **Impact:** Token cost not tracked — infinite budget assumed
- **What's missing:** Cost tracking per operation type
- **Status:** DESIGN PHASE

### GAP-009: No temporal rhythm
- **Layer:** L14
- **Impact:** No session type detection, no mode pre-setting
- **What's missing:** Observation data first, then encoding
- **Status:** OBSERVATION PHASE

---

## COMPETITIVE GAPS (VENOM vs others)

### vs Pi Agent Harness
- **Soul (L1):** Pi targets a generic developer harness; VENOM binds an immutable Mantle/Pact into decisions.

### vs NemoClaw / OpenClaw (Gateway stack)
- **Shell.null (L0):** OpenClaw favors a heavy local Gateway + onboarding; VENOM optimizes for distributed arms and avoidance of crystallized central shells.

### vs Hermes Agent + Hermes Agent Self-Evolution
- **Metabolic awareness (L13):** Hermes leans on infra (serverless hibernation); VENOM tracks token economy and output cost as first-class cognition.
- **Proprioception (L12):** Hermes evolves skills offline from traces; VENOM still needs live self-state during execution.
- **Reciprocity (L10):** Hermes assumes cooperative channels; VENOM enforces Token Debt and defection economics.

Mechanics harvested from OSS live in `COMPARE/_STEAL.md`; repo trees live under `COMPARE/` (Pi, NVIDIA NemoClaw, OpenClaw, NousResearch/Hermes*).

---

## CLOSED GAPS

*(none yet)*
