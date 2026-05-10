# NousResearch/Gym (NeMo Gym) Analysis
## Open Source Repo Analysis

**Source:** https://github.com/NousResearch/Gym (forked from NVIDIA-NeMo/Gym)
**Date Analyzed:** 2026-05-10
**Maps to Layer:** L4 (Arms / Local Execution) & L13 (Metabolic Awareness / Token Economy)

---

## 1. What it is
NeMo Gym is a library for building reinforcement learning (RL) training environments for large language models (LLMs). It provides infrastructure to develop environments, scale rollout collection, and integrate with training frameworks. It includes a large collection of environments for Reinforcement Learning from Verifiable Reward (RLVR) across domains like math, coding, agentic tool use, and SWE tasks.

## 2. What it does better than VENOM
- **Verifiable Reward Infrastructure:** It has a standardized way to define tasks with verifiable rewards (binary or continuous) without relying solely on LLM-as-a-judge.
- **Environment Isolation:** It separates the environment execution and rollout collection from the actual RL training loop, allowing independent testing and throughput scaling.
- **Curated Agentic Environments:** It provides ready-to-use environments for multi-step tool use, session state management, and software engineering (SWE) tasks.

## 3. What VENOM does better than it
- **Continuous Identity:** NeMo Gym is for episodic training; VENOM is designed for continuous, persistent identity across sessions (SIPHON).
- **Soul and Enforcement:** VENOM has a defined SOUL (PACT) and a Token Debt system for enforcement, whereas Gym is just a training sandbox.
- **Multi-Arm Actor Model:** VENOM's arms (WELD, DIG, etc.) are specialized actors, whereas Gym evaluates a single policy model or a simple orchestrator.

## 4. What we STEAL (The Mechanic)
**Isolated Verifiable Reward Environments for Arm Evaluation**
- **Mechanic:** Instead of evaluating VENOM's arms (L4) subjectively, we build isolated "Gym" environments for each arm (e.g., a SWE-bench style environment for WELD, a search/retrieval environment for DIG). These environments provide a verifiable reward (success/fail) independent of the main orchestration loop.
- **Application:** This will be used to validate L4 (Arms) and feed into L13 (Metabolic / Token Economy) to assign Token Debt based on verifiable performance.

---

## INTAKE Filter Score: 6
- Passes Q2 (Principles): +2 (Aligns with P2 Constraints and P6 Visible Futures)
- Maps to layer < 70%: +2 (L4 is 10%, L13 is 0%)
- Measurement present: +2 (Includes benchmarks and verifiable rewards)
- **Status:** APPROVED & ROUTED
