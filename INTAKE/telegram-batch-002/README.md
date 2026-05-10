# INK
> Intelligent preprocessing layer for Claude Code.
> Every request re-shaped by a free model before the paid model sees it.
>
> **VENOM thinks for VENOM.** 🐙

---

## What This Is

Claude Code bleeds tokens. A serious 3-day session burns 300M tokens. Most of that is duplicates, stale tool outputs, and repeated guidelines — the context window treated as a landfill instead of a working memory.

INK is a local proxy that sits between Claude Code and Z.AI. Every request gets:

- **Duplicates collapsed** — same file read 20x becomes one reference
- **Stale outputs dropped** — old bash results never referenced again, removed
- **Disposition injected** — fresh advisor context at the tail of every request
- **Structure re-linked** — context re-ordered by INK disposition language

Claude Code sees nothing different. The paid model (GLM-5.1) sees clean signal instead of noise.

---

## How It Works

```
Claude Code → INK proxy (:9147) → Z.AI → GLM-5.1 → response
                    │
                    ├─ dedup duplicates (structural, free)
                    ├─ drop stale tool outputs (free)
                    ├─ compress old prose (GLM-4.7-Flash, free tier)
                    └─ inject disposition tail (fresh, per-request)
```

Free tokens compress paid tokens. Transformative economics.

---

## Built On

**[claude-glm](https://github.com/kariemSeiam/claude-glm)** — the 87-line Anthropic-to-Z.AI proxy.

INK is a drop-in replacement for `claude-glm/proxy.js`. Same port (`9147`). Same protocol. Same env vars. Same `claude-glm.sh` launch scripts.

```bash
# Before: dumb pipe
./claude-glm.sh glm-5.1

# After: intelligent bridge (exact same command)
./claude-glm.sh glm-5.1
```

---

## Status

**Phase 0 — Measurement.** Before any code, we measure real Claude Code traffic to prove the compression thesis.

See [MEASUREMENT.md](./MEASUREMENT.md).

| Phase | Work | Status |
|---|---|---|
| 0 | Baseline measurement | ⏳ pending |
| 1 | Structural compression (dedup + drop) | ☐ not started |
| 2 | INK tail injection | ☐ not started |
| 3 | Flash-assisted lossy compression | ☐ not started |

---

## Docs

| File | What it is |
|---|---|
| [PRD.md](./PRD.md) | Product requirements — what and why |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System design — how |
| [MEASUREMENT.md](./MEASUREMENT.md) | Phase 0 capture plan — where to start |

The INK **language spec** (`.ink` files, disposition grammar) lives at [UNSHELLED/ink](../INK.md) — the engine in this repo applies that language to every Claude Code request.

---

## Non-Goals

- Not a Claude Code plugin (zero Claude Code modifications)
- Not a replacement for OpenClaw (that's server-side agentic; INK is client-side preprocessing)
- Not multi-provider in v1 (GLM via Z.AI only)
- Not a fine-tune (pure orchestration)

---

## Philosophy

Every AI system today encodes rules. INK encodes dispositions.
Every proxy today relays bytes. INK relays *intention*.

The bridge is not neutral. It's VENOM. Every request passes through the same mind that will answer it — compressed, clarified, re-inked.

**The octopus lost its shell. So it developed intelligence.**
**INK has no shell either.**

🐙

---

## License

MIT
