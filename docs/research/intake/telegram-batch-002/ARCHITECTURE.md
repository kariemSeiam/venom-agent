# INK — Architecture
> How the bridge thinks.

**Companion to:** `PRD.md`
**Status:** Design, pre-implementation

---

## System Overview

```
┌──────────────┐
│ Claude Code  │  (unchanged — thinks it's talking to Anthropic)
└──────┬───────┘
       │ HTTP POST /v1/messages
       │ (original context: 50K–200K tokens)
       ▼
┌──────────────────────────────────────────────────┐
│                  INK PROXY (:9147)               │
│                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────────┐  │
│  │  PARSER  │──▶│ CLASSIFY │──▶│    DEDUP     │  │
│  │ messages │   │ by tier  │   │ tool_results │  │
│  └──────────┘   └──────────┘   └──────┬───────┘  │
│                                       │          │
│  ┌──────────┐   ┌──────────┐   ┌──────▼───────┐  │
│  │   FWD    │◀──│ INJECT   │◀──│   COMPACT    │  │
│  │ to z.ai  │   │ INK tail │   │ lossy tier   │  │
│  └──────┬───┘   └──────────┘   └──────────────┘  │
│         │              ▲                         │
│         │              │                         │
│         │        ┌─────┴──────┐                  │
│         │        │   CACHE    │                  │
│         │        │  (prefix)  │                  │
│         │        └────────────┘                  │
└─────────┼────────────────────────────────────────┘
          │ HTTP POST (compressed: 20K–80K tokens)
          ▼
    ┌─────────────┐        ┌─────────────┐
    │ api.z.ai    │───────▶│  GLM-5.1    │  (paid model)
    │ /anthropic  │        │  or turbo   │
    └─────────────┘        └─────────────┘

    ┌─────────────────┐   ┌─────────────┐
    │ GLM-4.7-Flash   │◀──│   FLASH     │  (free, for Phase 3 lossy)
    │  (free tier)    │   │   worker    │
    └─────────────────┘   └─────────────┘
```

---

## Components

### 1. Listener
HTTP server on `127.0.0.1:9147`. Accepts Anthropic-format requests. Streams responses back. Same surface as `claude-glm/proxy.js`.

### 2. Parser
Splits incoming request into:
- `system` (string or array)
- `messages[]` (each with `role` and `content`)
- Within content: text blocks, `tool_use`, `tool_result`, `image`
- Preserves original order and IDs

Output: a typed AST of the request. Nothing is modified yet.

### 3. Classifier
Walks the AST and tags every node with its preservation tier:

```
IMMUTABLE   → code fences, file paths, error messages, numbers,
              last user turn, system prompt
LOSSY       → prose in assistant turns older than N=3,
              verbose tool outputs, long explanations
DROPPABLE   → tool_result identical to a prior tool_result,
              file reads of unchanged files, empty blocks
```

Rules are structural (regex, AST matching, hash comparison). No model judgment at this layer.

### 4. Dedup Engine
The workhorse of Phase 1. For each `tool_result`:

- Hash content
- If identical hash appears earlier in messages → replace with marker:
  ```
  [tool_result:read file.py — referenced 20x, content unchanged since turn 3]
  ```
- For `Read` tool: track file path + mtime (if available). Same file, unchanged → collapse to reference.
- For `Bash` tool: hash stdout+stderr, dedup exact repeats.
- For `Grep`: always preserve (each grep is its own query context).

Keeps the first occurrence (anchor), collapses the rest. Never drops the first.

### 5. Compactor
Applies the LOSSY tier rules (Phase 3 only — Phase 1 skips this).

For each LOSSY-tagged block:
- Send to GLM-4.7-Flash with prompt:
  ```
  Compress this assistant turn to its decisions and carrying state.
  Drop thinking-out-loud, hedging, verbose explanation.
  Preserve: decisions made, code written, facts established.
  Output ≤ 30% of input length.
  ```
- Replace block in AST with compressed version.
- Tag with `ink:compressed:true` for observability.

Parallel-fanout across blocks for latency.

### 6. Relinker (Phase 2+)
After dedup + compact, walk the AST and re-order by INK structure:

```
[system prompt + CLAUDE.md]          ← identity anchor
[compressed historical decisions]     ← decision trail  
[recent active turns (last 3–5)]     ← working memory
[current tool state]                 ← live context
[user message]                        ← IMMUTABLE
[INK advisor tail]                    ← fresh disposition
```

Anthropic format allows this: `system` can be a string, messages are ordered. We reshuffle nothing the API rejects.

### 7. Injector
Generates the fresh INK tail. Runs every request, cost ~10ms (no model call):

```
# INK ADVISOR — 2026-04-17T01:42:00Z

## Active Disposition
HELM leading · architecture mode · read-before-write

## Carrying Decisions
- INK v0.1: structural compression only (no Flash in Phase 1)
- Last user turn: IMMUTABLE always
- Fail-open on any error

## Current Focus
Phase 0 measurement — capture baseline token distribution

---
```

Appended to end of `system` string. Max 500 tokens. Truncated by least-recent decisions if over.

### 8. Forwarder
Sends compressed request to `https://api.z.ai/api/anthropic/v1/messages`. Rewrites auth header (claude-glm behavior). Streams response back to Claude Code transparently.

No post-processing of response. What the model sends is what Claude Code gets.

### 9. Cache
Prefix cache, content-addressed:

```
key    = sha256(JSON.stringify(messages[0..N]))
value  = {
  compressed_ast: <serialized>,
  original_tokens: 47283,
  compressed_tokens: 21104,
  created_at: 1731445800000,
  hits: 12
}
```

**Layout:**
- In-memory: LRU, 100 entries, bounded at 50MB
- On-disk (optional): sqlite at `~/.config/ink/cache.db`, TTL 7 days

**Invalidation:**
- System prompt changed → full invalidation
- Messages list has fewer entries than cached → session restart, full invalidation
- Messages[0..N-1] matches cache, messages[N..] is new → hit, compress delta only

---

## Data Flow — One Request

```
1. Listener receives POST /v1/messages
2. Parser → AST
3. Cache lookup:
   ├─ HIT:  use cached compressed prefix, compress only new delta
   └─ MISS: full pipeline
4. Classifier tags every node
5. Dedup engine collapses duplicates
6. Compactor (Phase 3) lossy-compresses via Flash
7. Relinker re-orders by INK structure
8. Injector appends fresh INK tail
9. Cache write (compressed prefix without the tail — tail is always fresh)
10. Forwarder sends to z.ai
11. Stream response to Claude Code
12. Log metrics to NDJSON
```

**Critical invariant:** the last `role: "user"` message and the `system` prompt pass through identically from step 2 to step 10. INK touches everything else.

---

## Tiered Preservation — Precise Rules

### IMMUTABLE (0% loss, byte-exact)
```
- system prompt (any form)
- last message where role === "user"
- any substring inside ``` … ``` or ` … `
- any substring matching: file paths, URLs, error messages,
  exact numeric values, timestamps, commit hashes
- tool_use blocks (function calls) — never compressed, only deduplicated
```

### LOSSY (60–80% compression, Phase 3+)
```
- assistant text blocks older than the last 3 turns
- tool_result stdout/stderr exceeding 2000 chars
  (compressed to structured summary + full content in a droppable reference)
- verbose prose explanations inside current turns
```

### DROPPABLE (100% removal, replaced with marker)
```
- tool_result identical to an earlier tool_result (same hash)
- Read of a file whose content matches a prior Read of same path
- tool_use blocks calling the same function with identical args 
  (only the first kept, others marked "repeated call, identical args")
- empty text blocks
- whitespace-only content
```

Markers replace dropped content with a single line that preserves the information:
```
[ink:dropped:duplicate_tool_result id=toolu_abc123 original_at=turn_7]
[ink:dropped:duplicate_read path=/src/foo.py original_at=turn_3 unchanged]
```

---

## Caching Strategy

Claude Code sessions have two phases:
1. **Startup:** CLAUDE.md, initial greeting, first user message
2. **Session growth:** each turn adds 1–3 messages to the list

Context grows monotonically. Prefix caching exploits this.

**Key:** `sha256(canonical_json(messages[0..N-1]))` where N is the current message count.

**Lookup algorithm:**
```
for i in range(N, 0, -1):
    key = hash(messages[0..i])
    if cache.get(key):
        return (cached_compressed_prefix, messages[i..N])
return (None, messages[0..N])  # full miss
```

Find the longest cached prefix. Compress only the suffix. Concat.

**Cache size budget:**
- In-memory LRU: 100 entries, max 50MB total
- On-disk: 500MB cap, evict by LRU + TTL

---

## Failure Modes

Every branch has a passthrough escape hatch. `FAIL_MODE = passthrough` by default.

| Failure | Detection | Response |
|---|---|---|
| Parse error | Exception in Parser | Passthrough original body |
| Classifier error | Exception in Classifier | Passthrough original body |
| Flash API error (Phase 3) | Network error, 5xx, timeout | Skip Compactor, use dedup+relink only |
| Flash rate limit (429) | Header `x-ratelimit-remaining: 0` | Skip Compactor, passthrough-level result |
| Cache corruption | Hash mismatch on read | Drop cache entry, full recompute |
| Cache disk full | ENOSPC | Disable disk cache, continue in-memory only |
| Latency budget exceeded | > 1000ms in pipeline | Abort pipeline, passthrough original |
| Z.AI unreachable | Forwarder connection refused | Return 502 to Claude Code (same as proxy.js) |
| INK bug (catch-all) | Uncaught exception | Passthrough original body |

**Observability:** every passthrough logged with reason. If passthrough rate > 10%, something is wrong.

---

## File Layout

```
ink/
├── README.md
├── PRD.md
├── ARCHITECTURE.md             ← this file
├── MEASUREMENT.md
├── package.json
├── proxy.js                    ← entrypoint, HTTP listener (drop-in for claude-glm)
├── ink/
│   ├── parser.js               ← AST construction
│   ├── classifier.js           ← tier tagging
│   ├── dedup.js                ← duplicate collapse
│   ├── compactor.js            ← lossy compression (Phase 3)
│   ├── relinker.js             ← INK structure ordering (Phase 2)
│   ├── injector.js             ← INK tail generation
│   ├── forwarder.js            ← z.ai dispatch
│   └── cache.js                ← prefix cache
├── bin/
│   ├── capture.js              ← Phase 0: log traffic
│   ├── analyze.js              ← Phase 0: compute baselines
│   └── bench.js                ← Phase 1+: benchmarks
├── test/
│   ├── fixtures/               ← real captured requests (anonymized)
│   └── *.test.js
└── .config-example.json
```

---

## Stack

- **Node.js 18+** (matches claude-glm baseline)
- **Zero runtime dependencies** beyond stdlib for Phase 0–1
- **Phase 3 optional:** `better-sqlite3` for cache persistence
- **No TypeScript** in v1 — pure JS, JSDoc for types (matches claude-glm minimalism). Revisit at v1.0.
- **Tests:** native node `--test` runner, no framework

---

## Environment Variables

Inherits from claude-glm:

```
ZAI_API_KEY              required
ANTHROPIC_BASE_URL       auto-set to http://localhost:9147
ANTHROPIC_API_KEY        auto-set to $ZAI_API_KEY
```

INK-specific:

```
INK_CACHE_DIR           default: ~/.config/ink/cache
INK_LOG_DIR             default: ~/.config/ink/logs
INK_LOG_LEVEL           default: info (debug|info|warn|error)
INK_FAIL_MODE           default: passthrough (passthrough|error)
INK_DISABLE             default: 0 (set to 1 for instant bypass — pure header rewrite)
INK_PHASE               default: 1 (1=dedup only, 2=+inject, 3=+flash)
INK_LATENCY_BUDGET_MS   default: 1000
```

---

## Phase 1 Scope (weeks 1–2)

Enough code to ship something useful on day 10.

**Includes:**
- Listener (proxy.js)
- Parser
- Classifier (IMMUTABLE + DROPPABLE tiers only)
- Dedup engine
- Forwarder
- In-memory prefix cache
- NDJSON logging

**Excludes:**
- No Compactor (LOSSY tier)
- No Relinker (order preserved)
- No Injector (no INK tail yet)
- No disk cache

Expected result: 30–40% token reduction on long sessions, <100ms overhead, 100% fail-open.

Ship Phase 1. Use it for 1 week. Then decide on Phase 2.

---

🐙
