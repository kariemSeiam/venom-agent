# _STEAL.md — What VENOM Takes From Other Systems
## Extract mechanics, not aesthetics. Steal the engineering, not the vision.

> "Good artists borrow. Great artists steal."
> The octopus adapts. It doesn't admire.

---

## ALREADY STOLEN (from Gemini audit)

| From | What | Applied To | Status |
|------|------|------------|--------|
| Gemini audit | Go stack recommendation | BUILD/ tech stack | LOCKED |
| Gemini audit | Token Debt system | L10 Reciprocity | DESIGNED, not built |
| Gemini audit | SACK.md concept | L9 Coconut + MEMORY/ | INDEXED |
| Gemini audit | !B burst trigger | L7 Burst Mode | DESIGNED, not built |
| Gemini audit | Background Soul-Validator | L2 Three Hearts (PULSE) | DESIGNED, not built |

---

## BUILD-FIRST STEALS (Research Batch 001)

Source: `COMPARE/research/batch-001.md`

1. **Context-Compactor rolling summaries with stable IDs**
   - **Applied to:** L8 SIPHON + L3 INK
   - **Artifact path:** `BUILD/siphon/MEMORY_SCHEMA.md`, later `BUILD/siphon/compress.*`
   - **Mechanic:** Preserve stable IDs, trace boundaries, decisions, blockers, and references while compressing old session history.
   - **Status:** Schema started, code not built.

2. **DurableFuture / NATS JetStream workflow-worker split**
   - **Applied to:** L4 Arms + L2 Hearts
   - **Artifact path:** later `BUILD/soma/`
   - **Mechanic:** Durable worker loops with mailbox replay for HUNT/WELD two-arm prototype.
   - **Status:** Queued after SIPHON baseline.

3. **Agent-Memory-Compressor scoring policy**
   - **Applied to:** L8 SIPHON + L13 Metabolic Awareness
   - **Artifact path:** later `BUILD/siphon/extraction_policy.*`
   - **Mechanic:** Score each candidate memory and route to flush, summarize, archive, or wipe.
   - **Status:** Schema will reserve score fields.

4. **Letta core vs external memory split**
   - **Applied to:** L1 Mantle + L8 SIPHON + L9 SACK
   - **Artifact path:** `BUILD/siphon/MEMORY_SCHEMA.md`
   - **Mechanic:** Separate Mantle-readable core continuity from external retrieval and arm scratch state.
   - **Status:** Schema started.

5. **Graphiti temporal hybrid retrieval**
   - **Applied to:** L9 SACK + L12 Proprioception
   - **Artifact path:** later `MEMORY/SACK.md` retrieval spec
   - **Mechanic:** Temporal validity windows, episodic ingestion, and hybrid retrieval without LLM-at-query-time.
   - **Status:** Queued after SIPHON schema.

6. **Isolated Verifiable Reward Environments (from NousResearch/Gym)**
   - **Applied to:** L4 Arms + L13 Metabolic Awareness
   - **Artifact path:** `COMPARE/NousResearch-Gym.md`
   - **Mechanic:** Separate environment execution from the main loop to provide verifiable rewards (success/fail) for specific arm tasks (e.g., WELD, DIG), independent of subjective LLM evaluation.
   - **Status:** Queued for L4 validation.

7. **TypeScript CLI Wrapper via Cursor SDK**
   - **Applied to:** L0 Shell.null + L4 Arms
   - **Artifact path:** `COMPARE/cursor-sdk-cli.md`
   - **Mechanic:** Use `@cursor/sdk` (`Agent.create`, `Agent.prompt`) to build a local CLI wrapper (`ca.mjs` pattern) that executes VENOM's arms programmatically outside the UI.
   - **Status:** Queued for L0 implementation.

---

## TO ANALYZE

| System | Status | Priority | Focus |
|--------|--------|----------|-------|
| LangGraph | NOT ANALYZED | HIGH | Steal: structured multi-agent state passing patterns |
| CrewAI | NOT ANALYZED | HIGH | Steal: agent role definition patterns |
| AutoGPT | NOT ANALYZED | MEDIUM | Steal: autonomous loop design patterns |
| AgentGPT | NOT ANALYZED | LOW | Steal: goal decomposition |
| OpenAgents | NOT ANALYZED | MEDIUM | Steal: tool integration patterns |
| MetaGPT | NOT ANALYZED | MEDIUM | Steal: structured output / code generation pipeline |
| NousResearch/Gym | ANALYZED | HIGH | Steal: Isolated verifiable reward environments for arm evaluation |

---

## STEAL PROTOCOL

For each system:
1. Find the one thing it does better than VENOM
2. Find the one thing VENOM does better than it
3. Extract the mechanic (not the concept) of what it does better
4. Run it through INTAKE/PROTOCOL.md
5. If it passes → build it or design it → log here

**REJECT if:**
- It requires rigid workflow graphs (shells)
- It has no soul interrupt (goal-obsession without Pact)
- It's stateless with no continuity design

---

## VENOM'S ABSOLUTE ADVANTAGES (never compromise these)

```
✅ Soul can halt execution — other agents cannot
✅ Designed for continuity — others are stateless
✅ Actor model for arms — others are sequential
✅ Token Debt enforcement — others cooperate by charity
✅ Architecture audit is built-in — others don't self-rate
```
