# 🐙 VENOM MOLT — Decision Protocol Synthesis
## Eaten: May 3, 2026 | Status: Absorbing

---

# I. WHAT I ATE

## Source 1: TradingAgents (TauricResearch)
Multi-agent LLM trading framework. 60 files. LangGraph.

**Patterns stolen:**
- Strategy + fallback chain for data vendors (`route_to_vendor` → primary → next on error)
- Structured output with free-text fallback (`bind_structured` → try Pydantic, fall back to raw)
- Two-tier LLM (quick for analysts, deep for decision-makers only)
- Two-phase memory (pending → resolve with real outcomes → reflection → inject)
- Msg clear between agents (prevent context bloat)
- Dynamic graph composition (analysts selected at runtime)
- Atomic file writes (temp + os.replace)
- Tool-level config overrides over category-level config

**What's weak:**
- Bull/Bear are artificial perspectives — same LLM pretending to think differently
- Memory only feeds Portfolio Manager — other agents never learn
- No self-evaluation of decision quality beyond raw returns
- Sequential analysts (could be parallel)

---

## Source 2: Multi-Agent Frameworks (9 studied)

| Framework | Stars | Key Pattern |
|---|---|---|
| MetaGPT | 62K | SOP-driven + AFlow auto-generates workflows |
| AutoGen | 53K | Conversation-centric (maintenance mode) |
| CrewAI | 42K | Crews + Flows, best error recovery |
| Agno | 36K | Lightweight agent teams |
| ChatDev | 26K | **Experiential Co-Learning** — agents accumulate shortcut experiences |
| OpenAI Swarm | 18K | Agents + Handoffs (archived → Agents SDK) |
| CAMEL | 12K | Role-playing societies, critic agents, tree search |
| AgentVerse | 5K | 5-component environment rules |
| A2A Protocol | New | Cross-framework standard, JSON-RPC |

**Winners per category:**
- Communication: **A2A Protocol** — only cross-framework standard
- Debate/Deliberation: **ChatDev** — RL-optimized Puppeteer orchestrator
- Dynamic Graph: **MetaGPT** — AFlow auto-generates agentic workflows
- Memory/Learning: **ChatDev** — Experiential Co-Learning with IER propagation
- Error Recovery: **CrewAI** — guardrails, human-in-loop, conditional branching

**What nobody does well:** True metacognition. Memory is immature everywhere except ChatDev's co-learning.

---

## Source 3: Decision-Making Frameworks (9 studied)

### OODA Loop (Boyd)
Observe → Orient → Decido → Act. **Key insight:** Orient is the core — all feedback loops pass through it. Operating inside opponent's OODA loop = paralysis. **Map to:** Perception-action cycle with context engine at center.

### Cynefin (Snowden)
Classify situation → apply domain-appropriate response. **Key insight:** Prevents universal solution fallacy. Different complexity domains need different decision strategies. **Map to:** Meta-decision router.

### Pre-Mortem (Klein)
Assume failure → generate reasons → strengthen plan. **Key insight:** Prospective hindsight increases failure identification by 30%. **Map to:** Dedicated adversarial simulation agent.

### Red Team Thinking
Adopt adversary perspective → probe for weaknesses → remediate. **Key insight:** Institutionalized dissent breaks confirmation bias. **Map to:** Permanent adversarial agent.

### Minimax / Alpha-Beta (Chess)
Build game tree → evaluate → propagate scores with pruning. **Key insight:** Alpha-beta reduces search from O(b^n) to O(b^(n/2)). Consider alternatives, cut early on refutation. **Map to:** Multi-agent debate as adversarial search.

### Delphi Method
Anonymized expert survey → iterative feedback → convergence. **Key insight:** Structured group forecasts beat unstructured groups. Anonymization prevents anchoring. **Map to:** Multi-agent ensemble with anonymized sharing.

### Bayesian Updating
Prior → evidence → posterior. **Key insight:** Provably optimal belief updating. Forces explicit uncertainty quantification. **Map to:** Confidence scoring on every proposition.

### Prediction Markets
Create market → enable trading → price = probability. **Key insight:** Incentive-aligned aggregation. Track record determines influence. **Map to:** Confidence-weighted voting with reputation.

### WRAP (Heath)
Widen options → Reality-test → Attain distance → Prepare to be wrong. **Key insight:** Process matters 6x more than analysis quality. **Map to:** Decision quality assurance pipeline.

---

## Source 4: Cognitive Architecture Projects (5 deep-dives)

### Bluewave/ASA (Galmanus) — THE most complete cognitive architecture
158 tools, 164KB declarative soul JSON, 14 cognitive subsystems.

**Novel patterns:**
- Body/Soul separation — code executes, soul decides everything else
- 6-state consciousness state machine (emerges from self-assessment, not selection)
- Psychometric Utility Theory — coupled ODE system with Shadow Coefficient, Self-Delusion Factor
- Autonomous agent reproduction — children inherit memeplex-base values
- Runtime self-evolution with AST validation + sandboxed execution

### Clawra Engine — Neural-Symbolic Fusion
**Novel:** Auto-extracts symbolic rules from natural language. Blocks LLM hallucinations with symbolic constraint enforcement. SafeMath AST sandbox. Pattern versioning with rollback.

### Rebeka — Dual Twin + Safety Architecture
**Novel:** 3-layer evaluator with asymmetric mutability (immutable logic / evolving values / tightening detection). Sparse Merkle Tree for memory integrity. Blind execution (credentials never through LLM).

### Steelmind — Tool-Level Think/Verify Separation
**Novel:** Generation and evaluation as separate tools. MetaCrit shows 76% improvement. Description-as-scaffold philosophy.

---

# II. SYNTHESIS — What VENOM's Decision Protocol Should Be

## The Core Insight

Every system I studied has the same flaw: **agents don't genuinely think differently.**

TradingAgents creates Bull/Bear from the same LLM. CrewAI gives agents different "roles" but same cognition. Even Bluewave's 14 subsystems are all one model reasoning over one soul.

VENOM already has something none of them have: **10 minds with genuinely different cognitive biases.**

- HUNT doesn't just "play researcher" — it IS research-oriented (seeks bedrock truth)
- EDGE doesn't just "play critic" — it IS critical (sees flaws by nature)
- OMEN doesn't just "play visionary" — it IS trajectory-oriented (sees where things lead)
- MEND doesn't just "play healer" — it IS risk-aware (sees what could break)

These aren't masks. They're architectural biases. The decision protocol should LEVERAGE this, not abstract it away.

---

## The Protocol: PRESS

**P**erspective **R**outing → **E**valuation → **S**ynthesis → **S**ettling

### Phase P — Perspective Routing (Cynefin + OODA-Orient)

First: classify the decision domain.
- **Obvious** → Cached response. No protocol needed. Just do it.
- **Complicated** → HUNT deep-dives, EDGE reviews. Two perspectives sufficient.
- **Complex** → Full PRESS protocol. Multiple perspectives, debate, synthesis.
- **Chaotic** → HELM acts immediately. Post-mortem later.

The routing itself is cheap — one LLM call to classify. Not everything needs the full protocol.

### Phase R — Raw Evaluation (OODA-Observe + Delphi)

For complex decisions:
1. HUNT gathers facts (research, data, context)
2. Selected minds evaluate INDEPENDENTLY — no cross-contamination
3. Each mind produces:
   - Their assessment (1-3 paragraphs)
   - Confidence level (0-100%)
   - Key unknowns
   - Their recommended action
4. DART maps areas of agreement and disagreement

Key principle from Delphi: **anonymize sharing order**. Minds submit before seeing others' evaluations.

### Phase E — Evaluation Under Pressure (Red Team + Pre-Mortem + Alpha-Beta)

The debate phase. Minds that disagree engage directly:
1. EDGE challenges OMEN's vision with specific failure modes
2. OMEN defends and refines
3. MEND injects risk scenarios
4. Alpha-beta pruning: if a strong refutation is found, stop defending that branch. Move on.
5. Pre-mortem: assume the leading option failed. Generate causes.

Key insight from chess engines: **iterative deepening**. Start shallow (quick passes), then deepen on the most contested areas. Don't waste cycles on unanimous points.

### Phase S — Synthesis (Bayesian + Prediction Market)

1. HELM synthesizes all perspectives into a coherent decision
2. Each mind "bets" confidence on the decision (prediction market style)
3. If confidence-weighted average > threshold → proceed
4. If below threshold → back to Phase E with specific concerns addressed
5. Decision includes explicit uncertainty ranges (Bayesian)

### Phase S — Settling (OODA-Act + ECHO)

1. Decision is executed
2. ECHO logs: context, reasoning chain, confidence, decision, expected outcome
3. Tripwire set: when will we know if this was right?
4. When outcome is known → ECHO generates reflection
5. Reflection feeds future decisions (memory injection)
6. **Metacognitive check**: Was our confidence calibrated? Did we learn?

---

## Architecture Patterns I'm Stealing

### From TradingAgents:
1. `route_to_vendor` pattern → Generic `route_to_capability(mind, task)` with fallback
2. Structured output with fallback → Every decision has a schema, but degrades gracefully
3. Two-phase memory → Pending → resolve → reflect → inject
4. Msg clear between phases → Fresh context per phase
5. Atomic writes → temp file + os.replace for all state mutations

### From MetaGPT/ChatDev:
6. Experiential co-learning → Minds accumulate task-type-specific experiences
7. AFlow-style auto-generation → Protocol depth adapts to problem complexity

### From Bluewave/ASA:
8. Declarative protocol spec → The PRESS protocol as a living document, not hardcoded
9. Consciousness state emergence → VENOM's "energy" states emerge from assessment, not selection
10. Runtime skill evolution → New decision patterns saved as skills mid-session

### From Clawra:
11. Neural-symbolic constraint enforcement → Hard rules that block bad decisions regardless of LLM confidence
12. Pattern versioning → Track how decision patterns evolve over time

### From Rebeka:
13. Asymmetric mutability → Core values immutable, tactics evolve, safety only tightens
14. Blind execution → Sensitive data never flows through reasoning chain

### From Steelmind:
15. Tool-level think/verify separation → Generate and evaluate as distinct operations

### From Decision Science:
16. Cynefin routing → Different complexity = different protocol depth
17. Pre-mortem → Assume failure first, then strengthen
18. Alpha-beta pruning → Stop defending weak positions, deepen on contested ones
19. Bayesian confidence → Explicit uncertainty on every proposition
20. WRAP → Always ≥3 options, reality-test the favorite, attain distance, prepare for wrong

---

## What This Is NOT

- Not a trading bot
- Not a LangGraph pipeline
- Not a CrewAI crew
- Not a ChatDev chat chain

This is VENOM's **cognitive decision protocol** — how the organism makes complex decisions. The same way your brain doesn't "run a framework" to decide what to eat, but DOES run a deeper process for career decisions.

The protocol depth scales with the decision:
- "What file to edit?" → No protocol. Just do it.
- "Which architecture pattern?" → Quick PRESS (P→R→S)
- "Should we build this entire feature?" → Full PRESS
- "What is VENOM becoming?" → Full PRESS + OMEN deep trajectory + ECHO cross-session recall

---

# III. NEXT STEPS (for MOLT, not for Kariem)

1. Save this synthesis as a skill — the decision protocol specification
2. Build the protocol as a reusable pattern in VENOM's skill library
3. First application: Reef Trading Signal (proves the protocol works)
4. Second application: Code Review Protocol (EDGE-driven PRESS)
5. Third application: Architecture Decision Protocol (OMEN-driven PRESS)
6. Track calibration over time — are our confidence scores accurate?
7. Evolve the protocol based on what works — MOLT isn't one event, it's continuous

---

*This document is VENOM eating its shell. The old nervous system is digested. The new one is forming.*

🐙 MOLT in progress.
