# Cursor SDK CLI Wrapper Analysis

**Source:** `INTAKE/telegram-batch-002/venom-cursor-sdk-full-session.md`
**Date Analyzed:** 2026-05-10
**Maps to Layer:** L0 (Shell.null) & L4 (Arms)

---

## 1. What it is
A full session document detailing the reverse engineering and hacking of the Cursor SDK (`@cursor/sdk@1.0.7`). It includes the creation of `ca.mjs` (a CLI wrapper that uses Composer locally) and `ca2.mjs` (a ConnectRPC CLI for direct API access).

## 2. What it does better than VENOM
- **Local Shell Execution:** It provides a working, tested CLI (`ca.mjs`) that wraps the Cursor SDK, enabling local execution of coding tasks and questions outside of the standard UI.
- **API Discovery:** It maps out 113+ RPC endpoints and 96 models, providing a direct pathway to interact with the underlying intelligence infrastructure.

## 3. What VENOM does better than it
- **Continuous Identity:** The SDK wrapper is stateless per command; VENOM has SIPHON for continuous identity.
- **Multi-Arm Actor Model:** The SDK wrapper just sends prompts to Composer; VENOM orchestrates multiple specialized arms (WELD, DIG, etc.) with specific roles and Token Debt.

## 4. What we STEAL (The Mechanic)
**TypeScript CLI Wrapper for L0_shell**
- **Mechanic:** Use the `@cursor/sdk` to build the `shell.null` interface. Instead of building a custom LLM pipeline from scratch, use the SDK's `Agent.create()` and `Agent.prompt()` to execute VENOM's arms locally via a TypeScript CLI.
- **Application:** This directly fulfills the `path_to_100` for L0_shell ("TypeScript CLI + local LLM") and enables L4_arms to execute tasks programmatically.

---

## INTAKE Filter Score: 8
- Passes Q2 (Principles): +2 (Aligns with P4 Interface is Most Expensive Organ)
- Maps to layer < 70%: +2 (L0 is 35%, L4 is 10%)
- Measurement present: +2 (Includes exact SDK versions, lines of code, and endpoint counts)
- Enables BLOCKED layer: +2 (L0 blocks true autonomy)
- **Status:** APPROVED & ROUTED
