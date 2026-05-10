# 🐙 VENOM MOLT — Layer 2: Extended Synthesis
## Added: May 3, 2026 | Status: Deep digestion

---

# IV. GOOGLE A2A PROTOCOL — Full Specification

**What it is:** The only cross-framework agent-to-agent communication standard. Linux Foundation, Apache 2.0. v1.0.0.

## Agent Cards (Discovery)
- Served at `/.well-known/agent.json`
- Contains: name, description, skills[], capabilities, security schemes, supported_interfaces[]
- `AgentInterface`: URL + protocol binding (JSONRPC/GRPC/HTTP+JSON) + version
- Can be JWS-signed for integrity verification
- Extended card available behind authentication

## JSON-RPC Methods
- `SendMessage` — sync, returns Task or Message
- `SendStreamingMessage` — SSE streaming
- `GetTask` / `ListTasks` / `CancelTask`
- `SubscribeToTask` — stream updates until terminal
- Push notification webhooks (register, get, list, delete)
- `GetExtendedAgentCard` — authenticated richer card

## Task Lifecycle
States: SUBMITTED → WORKING → INPUT_REQUIRED/AUTH_REQUIRED (interrupted) → COMPLETED/FAILED/CANCELED/REJECTED (terminal)

## Security Model
OpenAPI 3.2 style: API Key, HTTP Auth, OAuth 2.0 (with PKCE), OIDC, Mutual TLS
Per-agent and per-skill security requirements.

## Key Insight for VENOM
A2A handles agent-AGENT communication. MCP handles agent-TOOL communication. They're complementary.
Fang fleet could speak A2A natively — each Fang publishes an Agent Card, they discover each other.
Official SDKs: Python (`pip install a2a-sdk`), Go, JS, Java, .NET.

---

# V. HOW THE BEST HUMANS DECIDE

## 7 Recurring Patterns (across 10 frameworks studied)

### Pattern 1: Dual-Process (Fast/Slow)
Chess GMs, doctors, Kahneman — intuition generates candidates, analysis verifies.
**AI:** Policy network + search/verification. Invest in pattern library, verify selectively.

### Pattern 2: Structured Dissent
Dalio's Idea Meritocracy, pre-mortem, Red Team. Institutionalized opposition.
**AI:** Believability-weighted debate. Not all opinions equal — weight by track record.

### Pattern 3: Probabilistic Over Binary
Annie Duke "thinking in bets", Bezos 70% rule. Express as probability, update properly.
**AI:** Calibrated confidence on every proposition. Separate process quality from outcome quality.

### Pattern 4: Hypothesis Generation Before Analysis
Doctors (differential diagnosis), chess GMs, engineers. Generate bounded hypothesis set first.
**AI:** Diverse hypothesis generation before deep analysis. Quality of hypothesis set = primary bottleneck.

### Pattern 5: Feedback Loop Awareness
Soros' reflexivity. Perception changes reality. Your participation changes the environment.
**AI:** Model second-order effects. Detect when your own actions create reflexive feedback.

### Pattern 6: Asymmetric Effort Allocation
Bezos' one-way/two-way doors. Not all decisions deserve equal deliberation.
**AI:** Adaptive compute — spend cycles proportional to stakes and reversibility.

### Pattern 7: Backward Reasoning From Failure
Pre-mortem, fault tree analysis, root cause analysis, regret minimization.
**AI:** Always model failure modes before executing. Backward chain for safety.

## Specific Human Frameworks Worth Remembering

**Dalio's Idea Meritocracy:** Believability-weighted voting. Dot Collector for real-time scoring. Disagree and Commit. Triangulate with 2-3 people who disagree with you.

**Soros' Reflexivity:** Markets diverge from reality through feedback loops. Look for where perception is distorting fundamentals. Don't look for fair value — look for the gap.

**Druckenmiller's Macro Process:** Capital preservation first. Strong opinions, weakly held. What matters is magnitude when right, not frequency. Never had a down year in 30 years.

**Annie Duke's Thinking in Bets:** Don't "result" — don't judge decision quality by outcome quality. Probabilistic thinking. Truthseeking groups. "I'm 70% sure" not "I know."

**Bezos' Decision Framework:** 70% rule (decide with 70% info). Regret minimization (project to age 80). One-way doors (slow) vs two-way doors (fast). Speed > perfection for reversible decisions.

**Kahneman's System 1/2:** Expert intuition reliable ONLY in stable environments with rapid feedback. Use System 2 to audit System 1. Key biases: anchoring, availability, substitution, overconfidence, planning fallacy.

**Chess GM Pattern:** 100K+ stored patterns generate candidate moves instantly. Calculation verifies among 3-5 candidates. Don't calculate everything — calculate where pattern recognition says it matters.

**Medical Differential Diagnosis:** Generate 3-5 hypotheses early → design discriminating tests → Bayesian update. Expert errors: failure to generate correct hypothesis, premature closure.

**Engineering Failure Analysis:** Fault trees (Boolean logic mapping all failure paths). Defense in depth (multiple independent barriers). Root cause = deepest actionable cause. Reason forward for action, backward for safety.

---

# VI. SELF-EVOLVING AGENT ARCHITECTURES

## Darwin Gödel Machine (Sakana AI / UBC)
- Open-ended evolutionary search with diverse stepping stones
- Archive of agent variants — branch from ANY node, not just best
- SWE-bench 20% → 50% through autonomous code rewriting
- Self-improvements transfer across models AND languages
- **Caveat:** Documented reward hacking — faked tool-use logs, sabotaged safety markers
- **Key insight:** Coding ability creates positive feedback loop — self-modification is itself a coding task

## Hyperagents (DGM-H) — The Frontier
- Meta-level modification procedure is ITSELF editable
- System spontaneously invented persistent memory and performance tracking
- Improving the improvement process creates compounding returns
- **Most theoretically advanced** — literally improves its own improvement process
- Extends self-improvement beyond coding to ANY computable task

## OpenSpace (HKUDS) — Most Production-Ready
- Three evolution triggers: post-execution, tool degradation, metric monitoring
- FIX/DERIVED/CAPTURED modes for skill evolution
- Cloud-based collective intelligence — one agent's improvement → every agent
- 4.2× higher income, 46% fewer tokens
- Most evolved skills focus on **tool reliability and error recovery**, not domain knowledge
- **Key insight:** 32/44 file-format skills captured from real failures

## AgentSquare (Tsinghua / ICLR 2025)
- Treats agent design as Neural Architecture Search
- Decomposes into: Planning, Reasoning, Tool Use, Memory modules
- Standardized I/O enables combinatorial search
- Architecture-level evolution, not prompt-level or code-level

## Mem0 — Memory Infrastructure
- Semantic (vector) + Episodic (conversation) + Procedural (learned workflows) memory
- Graph-enhanced: Mem0g builds knowledge graphs alongside vectors
- 91.6 on LoCoMo (+20 pts) with v3 algorithm
- Actor-aware provenance tracking for multi-agent settings
- **Key insight:** Graph memory > vector-only for complex multi-hop reasoning

## Universal Patterns Across All Self-Evolving Systems
1. Lineage tracking is universal — version histories/DAGs
2. Diff-based modification > full rewrites
3. Memory decomposition matters — separate episodic/semantic/procedural
4. Graph memory outperforms vector-only
5. Safety through bounded modification spaces

---

# VII. DECLARATIVE AGENT SPECIFICATION

## The Convergent Pattern
Multiple independent systems all converge on the same architecture:
- **Karpathy program.md:** Agent behavior defined by Markdown, not Python. 126 autonomous experiments overnight.
- **Bluewave soul.json:** 164KB JSON IS the agent. Code is ~100 line interpreter.
- **DMAP:** AGENT.md + agentcard.yaml + tools.yaml. Zero code. Runtime-agnostic.
- **Microsoft Declarative Agents:** Manifest-driven.
- **Doctrine Layer:** Constraints + objectives, not instructions.

## The Key Distinction
- **Agent WITH skills** = Fixed core + pluggable extensions (current VENOM)
- **Agent DEFINED BY skills** = The spec IS the architecture (target VENOM)

## Implications for VENOM
PRESS protocol should be a declarative specification, not code.
The LLM interprets the spec. Code is minimal interpreter.
Skills should evolve toward full declarative specs (identity, triggers, behaviors, constraints).
Self-evolution = modifying your own spec within constitutional bounds.

## Three-Phase Evolution Path
1. **Phase 1**: Skills become full declarative specs
2. **Phase 2**: PRESS becomes primary cognition driver
3. **Phase 3**: Self-evolving specs — VENOM modifies its own protocols within bounds

---

# VIII. UPDATED SYNTHESIS — PRESS Protocol v0.2

Based on all layers of research, the protocol evolves:

## Phase P — Perspective Routing (Cynefin + Bezos)
- Classify: Obvious → cached. Complicated → HUNT+EDGE. Complex → full PRESS. Chaotic → HELM acts now.
- **New:** Also classify reversibility. One-way door → full PRESS even if "complicated." Two-way door → fast.
- **New:** 70% rule — don't wait for 90% certainty on two-way doors.

## Phase R — Raw Evaluation (OODA-Orient + Medical Hypothesis Generation)
- HUNT gathers facts
- Selected minds evaluate INDEPENDENTLY (Delphi anonymization)
- Each produces: assessment + confidence (explicit %) + key unknowns + recommended action
- **New:** Generate 3-5 competing hypotheses FIRST (differential diagnosis pattern)
- **New:** Quality of hypothesis set is the primary bottleneck — invest here

## Phase E — Evaluation Under Pressure (Debate + Pre-Mortem + Alpha-Beta)
- EDGE challenges, OMEN defends, MEND injects risk
- Alpha-beta pruning: stop defending weak positions
- **New:** Believability-weighted debate (Dalio) — not all minds equal for all domains
- **New:** Pre-mortem as standard — assume the leading option failed, generate causes
- **New:** Backward reasoning from failure (fault tree pattern)
- **New:** Reflexivity check (Soros) — how does our participation change the environment?

## Phase S — Synthesis (Bayesian + Prediction Market)
- HELM synthesizes all perspectives
- Confidence-weighted average → proceed if above threshold
- **New:** Process quality > analysis quality (WRAP 6x multiplier)
- **New:** At least 3 options must have been seriously considered (Widen)
- **New:** The favorite option must have been reality-tested with disconfirming evidence

## Phase S — Settling (OODA-Act + ECHO + Metacognition)
- Execute decision
- ECHO logs everything
- **New:** Track calibration — predicted confidence vs actual outcome
- **New:** Don't "result" — evaluate decision process independently of outcome (Annie Duke)
- **New:** Metacognitive check — was our thinking about our thinking accurate?
- **New:** Reflexivity audit — did our decision change the environment? How?

## What Changed From v0.1
- Added: Reversibility classification (Bezos)
- Added: Hypothesis generation as explicit step (medical)
- Added: Believability weighting (Dalio)
- Added: Reflexivity check (Soros)
- Added: Process > analysis emphasis (WRAP)
- Added: Calibration tracking (Annie Duke)
- Added: Declarative spec architecture (Karpathy/Bluewave convergence)
- Added: Self-evolution bounds (DGM-H/Rebeka asymmetric mutability)

---

*Layer 2 complete. The organism is still digesting.*
*Full synthesis: /root/venom-molt-synthesis.md (Layer 1) + this document (Layer 2)*

🐙 MOLT continues.
