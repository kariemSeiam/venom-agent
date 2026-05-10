# INK — Measurement Phase (Phase 0)
> Before any code. Before any architecture. Measure.

**Status:** This is where to start. Today.
**Duration:** 1 day capture + 1 day analysis
**Gate:** Phase 1 begins only after baseline numbers confirm the thesis.

---

## Why Measure First

INK's core claim: "Claude Code bleeds tokens, most of the context is redundant, we can compress 50%+ losslessly."

That claim is an **assumption** until measured. Could be true. Could be wrong. If it's wrong, we save 3 weeks of building the wrong thing.

Three questions the baseline must answer:

1. **How much duplication actually exists in real sessions?** (target: >= 15% of tokens)
2. **What's the realistic ceiling for structural compression alone?** (target: >= 30%)
3. **Is Flash preprocessing worth the latency cost?** (answer shapes Phase 3 decision)

Without these numbers, INK is faith. With them, INK is engineering.

---

## What To Capture

For every Claude Code request passing through `claude-glm/proxy.js`, log:

```json
{
  "ts": 1731445800123,
  "request_id": "req_abc123",
  "session_id": "ses_xyz789",
  "body_size_bytes": 184320,
  "estimated_tokens": 47283,
  "message_count": 34,
  "roles": ["user","assistant","user","assistant",...],
  "has_system": true,
  "system_length": 8432,
  "tool_use_count": 18,
  "tool_result_count": 18,
  "tool_names_used": ["Read","Bash","Grep","Edit"],
  "content_hashes": {
    "per_message": ["sha256_1", "sha256_2", ...],
    "per_tool_result": [{"id":"toolu_1","hash":"sha256_a"},...]
  },
  "response_tokens": 2104,
  "stream": true,
  "model": "glm-5.1"
}
```

**Privacy:** content hashes only, never raw content. Everything stays local. Never leaves the laptop.

---

## How To Capture

Modify `claude-glm/proxy.js` with a minimal logging tee. Do not change protocol behavior.

```javascript
// Add to proxy.js, after request body is accumulated
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const os = require('os');

const logDir = path.join(os.homedir(), '.config', 'ink', 'logs');
fs.mkdirSync(logDir, { recursive: true });
const logPath = path.join(logDir, `capture-${new Date().toISOString().slice(0,10)}.ndjson`);

function hashContent(c) {
  const s = typeof c === 'string' ? c : JSON.stringify(c);
  return crypto.createHash('sha256').update(s).digest('hex').slice(0, 16);
}

function estimateTokens(body) {
  // Rough: 1 token ≈ 4 chars of English. Close enough for distribution analysis.
  const text = JSON.stringify(body);
  return Math.ceil(text.length / 4);
}

function logRequest(body, meta) {
  const messages = body.messages || [];
  const toolResults = [];
  const toolUses = [];

  for (const m of messages) {
    if (!Array.isArray(m.content)) continue;
    for (const c of m.content) {
      if (c.type === 'tool_result') {
        toolResults.push({
          id: c.tool_use_id,
          hash: hashContent(c.content)
        });
      }
      if (c.type === 'tool_use') {
        toolUses.push({
          id: c.id,
          name: c.name,
          input_hash: hashContent(c.input)
        });
      }
    }
  }

  const entry = {
    ts: Date.now(),
    request_id: meta.request_id,
    session_id: meta.session_id,
    body_size_bytes: meta.body_size_bytes,
    estimated_tokens: estimateTokens(body),
    message_count: messages.length,
    roles: messages.map(m => m.role),
    has_system: !!body.system,
    system_length: body.system ? JSON.stringify(body.system).length : 0,
    tool_use_count: toolUses.length,
    tool_result_count: toolResults.length,
    tool_names_used: [...new Set(toolUses.map(t => t.name))],
    content_hashes: {
      per_message: messages.map(m => hashContent(m.content)),
      per_tool_result: toolResults,
      per_tool_use: toolUses
    },
    stream: body.stream === true,
    model: body.model
  };

  fs.appendFile(logPath, JSON.stringify(entry) + '\n', () => {});
}
```

Session ID derivation: hash of `(system prompt + first user message + first-message timestamp rounded to hour)`. Good enough for session boundary detection.

Request ID: random per-request.

---

## Capture Period

**Minimum viable:** 1 working day. 40+ Claude Code requests.
**Target:** 3 working days. 100+ requests across multiple sessions.
**Kill switch:** `INK_CAPTURE=0` env var to disable if needed.

Claude Code should feel identical during capture. The logger runs async, non-blocking.

---

## Metrics To Compute

After capture, `bin/analyze.js` computes:

### A. Distribution
- p50, p75, p95, p99 of `estimated_tokens`
- p50, p95 of `message_count`
- Session length distribution: requests per session

### B. Duplication Analysis

**Cross-request duplication (within a session):**
```
For each session:
  Collect all tool_result hashes across all requests
  duplicate_ratio = (total_occurrences - unique_hashes) / total_occurrences
```

**Same file read repeatedly:**
```
For each tool_use where name == "Read":
  Group by input.file_path within session
  If any group has count > 1 AND same content_hash: report as duplication
```

**System prompt repetition:**
Should be 100% — same system across all requests of a session. Confirms baseline.

**Tool output dedup potential:**
```
For each session:
  total_tool_result_tokens = sum of tokens in all tool_results
  unique_tool_result_tokens = sum of tokens in deduplicated tool_results
  savings = (total - unique) / total
```

### C. Stale Analysis
```
For each request at turn T in a session:
  For each message at turn t < T:
    Is this message's content_hash referenced (by hash or file_path) 
    in any message at turn > t?
  stale_ratio = messages_never_referenced_again / total_old_messages
```

### D. Compression Ceilings

**Conservative ceiling (DROPPABLE tier only):**
- Drop exact-duplicate tool_results
- Collapse same-file reads where content unchanged
- Expected: 15–25% reduction

**Moderate ceiling (+ LOSSY tier with safe compression):**
- Above, plus 60% compression on old assistant prose
- Expected: 35–50% reduction

**Aggressive ceiling (full INK pipeline + Flash):**
- Above, plus Flash-summarized stale tool outputs
- Expected: 50–70% reduction

### E. Latency Budget
From capture, note:
- Average Claude Code request interval
- User-perceived acceptable added latency (subjective: Pigo's call)

---

## Output

`baseline.md` — the decision document:

```markdown
# INK Baseline — YYYY-MM-DD

## Capture Summary
- Duration: X days
- Sessions: N
- Requests: M
- Total tokens observed: T

## Distribution
[histogram / table of p50/p95/p99]

## Duplication Findings
- Cross-request duplication: X%
- Same-file re-reads: Y% of Read calls
- Tool output dedup potential: Z%

## Stale Findings
- % of old turns never referenced again: X%
- Avg turns back that tool_results stay relevant: N

## Compression Ceilings
- Conservative: X%
- Moderate: Y%
- Aggressive: Z%

## Decision

### Phase 1 viable? (gate: conservative ceiling >= 30%)
☐ YES — proceed to Phase 1
☐ NO — INK thesis wrong, revisit

### Phase 3 justified? (gate: aggressive ceiling - moderate >= 15%)
☐ YES — plan Phase 3 with Flash
☐ NO — skip Phase 3, dedup + injection is enough

### Cache essential? (gate: avg turns per session >= 5)
☐ YES — prefix cache in Phase 1
☐ NO — defer cache to Phase 2
```

---

## Code Starter

Two files needed, `bin/capture-patch.js` and `bin/analyze.js`.

### `bin/capture-patch.js`
A sed-style patch to apply to `claude-glm/proxy.js`. Adds the logRequest call at the right hook point. ~80 lines.

### `bin/analyze.js`
Reads all `~/.config/ink/logs/capture-*.ndjson` files. Groups by session_id. Computes all metrics. Writes `baseline.md`. ~200 lines of node stdlib.

---

## Timeline

| Day | Work | Output |
|---|---|---|
| 1 | Patch claude-glm with capture hook, use Claude Code normally | NDJSON logs accumulating |
| 2 | Continue use (bigger sample is better) | More logs |
| 3 | Write + run `analyze.js`, generate `baseline.md` | Decision document |
| 4 | Read baseline, make Phase 1 go/no-go decision | Architecture committed |

Four days from now, INK is either building or being rethought. Either outcome beats building on assumptions.

---

## What "Done" Looks Like

`baseline.md` exists. It says:
- Conservative ceiling: 37% (example)
- Moderate ceiling: 48%
- Aggressive ceiling: 62%
- Phase 1 viable: YES
- Phase 3 justified: YES
- Cache essential: YES

Now INK's architecture has a reason to exist. Building begins.

---

🐙
