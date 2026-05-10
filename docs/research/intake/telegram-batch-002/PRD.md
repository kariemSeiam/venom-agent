# INK — Product Requirements Document
> Intelligent preprocessing layer for Claude Code.
> Not a plugin. Not a config. A bridge that thinks.

**Version:** 0.1 (draft)
**Status:** Phase 0 — measurement pending
**Target:** Claude Code (Anthropic's CLI)
**Bridge partner:** claude-glm → Z.AI GLM models

---

## One Line

Every Claude Code request gets re-shaped by a free GLM model before the paid GLM model sees it. Duplicates collapsed, stale context compacted, disposition injected — losslessly at the anchors, aggressively at the noise.

**VENOM thinks for VENOM.**

---

## The Problem

Claude Code bleeds tokens. A serious 3-day session burns 300M tokens. The breakdown is not what people assume:

| Category | % of context (estimated) | What it actually is |
|---|---|---|
| Duplicate file reads | 15–25% | Same file opened 10–20x across turns, content unchanged |
| Stale tool outputs | 20–30% | Bash/grep results from 15 turns ago, never referenced again |
| Guideline repetition | 10–15% | CLAUDE.md, system prompts echoed every turn |
| Assistant "thinking out loud" | 10–20% | Old turns that drifted, decisions that got reversed |
| Active conversation | 25–40% | What the model actually needs |

**Three quarters of every request is landfill.** The model doesn't re-read it meaningfully — it just pays for the weight to cross the wire.

---

## The Insight

If a free model can preprocess the context before the paid model sees it, the economics flip.

```
GLM-4.7-Flash: $0 / 1M tokens (free tier)
GLM-5.1:       $1.40 / $4.40 per 1M tokens
```

Burning free tokens to compress paid tokens is strictly dominant if the compression is faithful. Latency rises slightly. Cost falls massively. **Quality rises** — the paid model sees clean signal instead of noise.

---

## The Disposition Layer

Compression alone is commodity. What makes INK unique: every compressed context gets **re-organized by INK structure** — the disposition language from `INK.md` (v1.1).

The preprocessor is not neutral. It's VENOM. Every request gets re-inked:
- **Who** the system is (identity anchor)
- **Where** it's focused (current scope)
- **What** matters right now (active disposition)
- **Why** this path (decision trail)

Injected as a fresh advisor tail at the end of the system context. The model doesn't just see compressed history — it sees compressed history pointed in the right direction.

---

## Users

| Tier | Who | Use case |
|---|---|---|
| Primary | Pigo | Long Claude Code sessions, 300M+ tokens/week |
| Secondary | Claude Code power users | Any session that routinely hits 100K+ context |
| Tertiary | Any Anthropic-protocol client (Cursor, Continue, etc.) | Drop-in via same proxy port |

---

## Non-Goals (v1)

- ❌ Not a Claude Code plugin — zero modifications to Claude Code itself
- ❌ Not a new CLI — works with existing `claude-glm.sh` launch scripts
- ❌ Not OpenClaw — OpenClaw handles agentic server work; INK is client-side preprocessing
- ❌ Not multi-provider — GLM via Z.AI only
- ❌ Not a fine-tune — pure orchestration, no model training
- ❌ Not multi-user — single local daemon per machine

---

## Requirements

### R1 — Drop-in replacement for claude-glm/proxy.js
Same port (`9147`). Same protocol (Anthropic `/v1/messages`). Same env vars (`ZAI_API_KEY`, `ANTHROPIC_BASE_URL`). Swap one file, change nothing else. User still runs `./claude-glm.sh glm-5.1`.

### R2 — Last user turn is IMMUTABLE
The most recent `role: "user"` message passes through byte-for-byte. No compression, no rewrite, no "helpful" restructuring. Any mutation is a contract violation → INK fails closed → passthrough mode.

**Why:** the moment INK rewrites user intent, it's vandalism, not advisory. Hard red line.

### R3 — Tiered preservation

| Tier | Policy | Applies to |
|---|---|---|
| **IMMUTABLE** | 0% loss, byte-exact | Code in fences, error messages, file paths, exact numbers, last user turn, system prompt |
| **LOSSY** | 60–80% compression via Flash | Old assistant prose, verbose explanations, redundant context |
| **DROPPABLE** | 100% removal, replaced with marker | Duplicate file reads, identical tool results, stale bash outputs |

The compressor must know the tier of every token before touching it. Tier classification is structural (regex + AST), not semantic (no model judgment needed for tiering).

### R4 — Compression via GLM-4.7-Flash
All preprocessing uses the free tier. Zero incremental cost. If Flash errors or rate-limits → passthrough.

### R5 — Prefix caching
Context grows monotonically within a session. Cache compressed prefixes:

```
key   = sha256(first_N_messages_serialized)
value = { compressed_form, original_tokens, compressed_tokens, created_at }
```

New turn = compress delta only, concat onto cached prefix, inject fresh INK tail. Target: after 10 turns, cache hit >= 70%.

### R6 — INK tail injection
Every request gets a fresh advisor block appended to system context. Not compressed (it's freshly generated each time). Contents:
- Current crew disposition (e.g. "HELM leading, architecture mode")
- Recent decisions carried forward (last 3–5 non-drifted decisions)
- Active focus (what we're building right now)

Max 500 tokens. Budget is hard — overflow gets trimmed by least-recent.

### R7 — Observability
Every request logs to NDJSON:
```json
{
  "ts": 1731445800000,
  "session_id": "...",
  "original_tokens": 47283,
  "compressed_tokens": 21104,
  "compression_ratio": 0.446,
  "latency_ms": 187,
  "cache_hit": true,
  "fail_mode": null
}
```

Log path: `~/.config/ink/logs/requests.ndjson`. Rotates daily.

### R8 — Fail-open, always
Any error in INK = passthrough mode. Network error → passthrough. Parse error → passthrough. Cache corruption → passthrough. Flash 429 → passthrough. Timeout → passthrough.

**Claude Code never sees INK fail.** It sees a slightly slower normal request.

---

## Success Metrics

| Metric | Target | Measured by |
|---|---|---|
| Compression ratio (contexts >20K tokens) | >= 50% reduction | Logs: `compressed / original` |
| Latency overhead p50 | < 300ms | Logs: `latency_ms` |
| Latency overhead p95 | < 800ms | Logs: `latency_ms` |
| Cache hit rate after 10 turns | >= 70% | Logs: `cache_hit` |
| Fail-open rate | 100% | Manual: no Claude Code blocked by INK |
| Output quality degradation | None perceptible | Pigo's subjective read over 1 week |

---

## Constraints

- **Stack:** Node.js 18+, zero runtime deps beyond stdlib (match claude-glm philosophy). Exception: `better-sqlite3` for cache persistence — optional, starts in-memory.
- **Protocol:** Anthropic `/v1/messages` format, streaming + non-streaming. Tool use, images, system prompts all supported.
- **Platform:** Mac, Linux. Windows = Phase 3+.
- **Rate limits:** Z.AI free tier caps on GLM-4.7-Flash. Design assumes worst-case passthrough behavior.
- **Local only:** daemon binds `127.0.0.1:9147`, never exposed to network.

---

## Risks

| Risk | Mitigation |
|---|---|
| Compression silently loses load-bearing context | Tiered preservation; IMMUTABLE tier is structural, not judgment-based |
| Latency degrades interactive feel | Prefix caching; delta-only compression after first turn |
| Flash hallucinates during summarization | v1 does **no generative summarization** — only structural dedup/drop. Generative pass is Phase 3+ behind a flag. |
| Z.AI rate-limits the free tier | Fail-open to passthrough, local cache handles repeat contexts |
| Prefix cache poisoning | Content-hashed keys, TTL + size-bounded LRU |
| User debugging "why is context weird" | Full observability logs + `INK_DISABLE=1` env var for instant passthrough |

---

## Phases

### Phase 0 — Measurement (before any code)
Capture real claude-glm traffic for 1 day. Compute baselines. See `MEASUREMENT.md`.

**Gate:** baseline numbers prove a >= 30% compression potential from pure structural dedup. If not, INK's thesis is wrong — revisit.

### Phase 1 — Structural compression (weeks 1–2)
- Parser + tier classifier
- Duplicate file-read collapse (`"file.py read 20x, unchanged"`)
- Stale tool output drop
- Zero model calls. Pure string/hash work.
- Expected reduction: 30–40% alone.

### Phase 2 — INK tail injection (week 3)
- Fresh advisor block generator
- Crew disposition context
- Decision trail extraction
- Still zero Flash calls. Runs in <50ms.

### Phase 3 — Flash-assisted compression (week 4+)
- GLM-4.7-Flash call for LOSSY tier
- Prefix cache with sqlite persistence
- Metrics dashboard (TUI or web)
- Expected additional reduction: 20–30% on top of Phase 1.

Each phase ships standalone. Phase 1 alone is already worth using.

---

## Open Questions

1. **Streaming preprocessing?** If we compress before forwarding, do we lose stream-start latency? → measure in Phase 0.
2. **Where does INK tail live?** End of `system` param, or injected as last assistant turn, or as a synthetic user message? → test all three, pick empirically.
3. **Tool use preservation:** do we dedup `tool_use` blocks the same as text? → yes, by `tool_use_id`, but careful with result ordering.
4. **Session boundary:** how does INK know a new session started? → heuristic: system prompt hash + first message timestamp gap > 1h.

All four answered by end of Phase 1.

---

🐙
