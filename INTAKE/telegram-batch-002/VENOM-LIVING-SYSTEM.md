# VENOM Living System — Architecture

> "الأخطبوط مش بيستنى. بيراقب. بيتعلم. بيتحرك."
> The octopus doesn't wait. It watches. It learns. It moves.

---

## What This Is

VENOM stops being invoked. VENOM starts being alive.

Not a daemon that runs scripts. A living system that watches your world, learns from it, acts on it, and develops its own capabilities over time. The missing half of your mind that doesn't sleep when you do.

Three organs make it alive:

```
HEARTBEAT     — always running, never stops
SENSES        — sees everything across all platforms
HANDS         — acts, builds, reviews, indexes, develops itself
```

---

## The Heartbeat

**Where:** Hostinger KVM 4 VPS (always-on)
**What:** Python daemon (`venom-pulse`) + cron scheduler + webhook receiver
**How it talks to you:** Telegram bot (already partially built in OpenClaw)

```
venom-pulse/
├── pulse.py                 ← main daemon, event loop
├── scheduler.py             ← cron-like job scheduler
├── webhook_server.py        ← receives GitHub webhooks, notifications
├── telegram_bridge.py       ← two-way Telegram communication
├── config.yaml              ← all credentials, schedules, project registry
├── jobs/                    ← individual scheduled jobs
│   ├── github_patrol.py     ← check repos for new commits/PRs
│   ├── news_feed.py         ← tech news aggregation
│   ├── youtube_digest.py    ← channel monitoring + transcript eating
│   ├── project_indexer.py   ← auto-index registered projects
│   ├── learning_cycle.py    ← consolidate learnings across sessions
│   └── health_check.py      ← self-monitoring
├── workers/                 ← long-running background tasks
│   ├── code_reviewer.py     ← triggered by webhook on push/PR
│   ├── content_eater.py     ← deep-eat YouTube/articles on demand
│   └── index_builder.py     ← builds project INDEX.md trees
├── memory/                  ← persistent brain on VPS
│   ├── global_memory.md     ← cross-project decisions
│   ├── feeds.json           ← tracked channels, sources, last-checked
│   └── alerts.json          ← active alerts and their status
└── mcp/                     ← reshaped MCP servers running locally
    ├── youtube/             ← forked from open-source, VENOM-shaped
    ├── github/              ← GitHub official MCP, configured
    ├── news/                ← RSS/Atom aggregator MCP
    └── webhook/             ← receives and routes webhooks
```

### Pulse Schedule (What Runs When)

| Job | Frequency | What it does |
|-----|-----------|-------------|
| `github_patrol` | Every 15 min | Check all registered repos for new commits, PRs, issues. Alert on Telegram if action needed. |
| `youtube_digest` | Every 6 hours | Check subscribed channels for new videos. Extract transcripts. Summarize. Store. |
| `news_feed` | Every 3 hours | Pull tech news from configured sources. Filter by relevance. Digest to Telegram. |
| `project_indexer` | On push webhook + daily | Rebuild INDEX.md files for changed projects. Full re-index daily. |
| `learning_cycle` | Daily at midnight | Consolidate `.venom/` learnings across all projects. Promote instincts. Archive old memory. |
| `health_check` | Every 5 min | VPS resources, daemon status, MCP server health. Self-heal if possible. Alert if not. |

---

## The Senses

VENOM doesn't search — it sees. Each sense is an MCP server (open-source, reshaped) running on the VPS.

### Sense 1: GitHub (Official MCP)

**Source:** `github/github-mcp-server` (GitHub's official, 40+ tools)
**Reshape:** Configure with your PAT. Register all repos. Set up webhooks pointing to `webhook_server.py`.

**What VENOM sees:**
- Every push to any registered repo
- Every PR opened, reviewed, merged
- Every issue created or updated
- CI/CD status changes
- Dependabot alerts

**What VENOM does automatically:**
- On push → run `code_reviewer.py` → review diff → post summary to Telegram
- On PR → full review using VENOM reviewer mind → comment on PR or alert you
- On CI fail → diagnose from logs → suggest fix on Telegram
- On Dependabot alert → assess severity → alert if critical

```yaml
# config.yaml — GitHub sense
github:
  token: "${GITHUB_PAT}"
  repos:
    - kariemSeiam/geolink
    - kariemSeiam/hvarhub
    - kariemSeiam/portfolio
    - kariemSeiam/venom-mine  # or whatever the repo name is
  webhooks:
    endpoint: "https://your-vps:8443/webhook/github"
    secret: "${WEBHOOK_SECRET}"
    events: [push, pull_request, issues, workflow_run, dependabot_alert]
```

### Sense 2: YouTube (Open-Source MCP, Reshaped)

**Source:** Fork `sparfenyuk/mcp-youtube` or `aihenryai/mcp-youtube-analytics`
**Why these:** yt-dlp based (no API quota for transcripts) + Data API for metadata. Best of both.

**What VENOM sees:**
- New videos from subscribed channels (AI, dev, business, Islamic content)
- Full transcripts extracted automatically
- Channel analytics for channels you care about

**What VENOM does automatically:**
- New video detected → extract transcript → summarize → store in `memory/youtube/`
- If video matches interest tags → Telegram digest with key takeaways
- Weekly: compile "What I learned this week from YouTube" digest

```yaml
# config.yaml — YouTube sense
youtube:
  api_key: "${YOUTUBE_API_KEY}"
  channels:
    - "@firaboraei"       # Arabic AI/tech
    - "@3aborai"          # Arabic AI/tech
    - "@anthropic"        # Claude updates
    - "@AIExplained"      # AI deep dives
    - "@ThePrimeagen"     # Dev culture
    # Add Islamic channels, business channels, etc.
  interest_tags: [ai, llm, mcp, cursor, android, kotlin, compose, startup, islamic]
  digest_schedule: "0 */6 * * *"  # every 6 hours
```

### Sense 3: News & Web (RSS + Firecrawl MCP)

**Source:** `jjsymes/mcp-rss-reader` (RSS/Atom, 16+ sources built-in) + Firecrawl for deep reads
**Reshape:** Add Arabic tech sources. Filter by relevance score.

**What VENOM sees:**
- Hacker News top stories
- Tech news (Verge, Ars Technica, TechCrunch)
- AI-specific feeds (Anthropic blog, OpenAI blog, Google AI blog)
- Arabic tech feeds
- MCP ecosystem updates

**What VENOM does automatically:**
- Filter by interest tags → only relevant stories
- High-relevance story → deep-read via Firecrawl → summarize → store
- Daily digest to Telegram: "Top 5 things you should know today"

### Sense 4: Claude.ai (This Conversation Layer)

**No MCP needed.** This IS Claude.ai. The sense is the project itself.

**What VENOM does:**
- This project's knowledge persists across conversations
- When you discuss a decision here, it becomes memory
- When you say "احفظ", it's captured in project knowledge
- VENOM on VPS can read/write to the same `.venom/` files via git sync

**Bridge:** Git is the bridge. VPS pushes to repo. Claude.ai project reads from repo. Decisions flow both ways.

### Sense 5: Social Media (Future — Phase 2)

**Source:** Twitter/X MCP servers exist. LinkedIn has unofficial APIs. Instagram has basic MCP.
**When:** After Phase 1 is stable. Social media is noisy. Add it only when filtering is mature.

---

## The Hands

VENOM doesn't just see. It acts.

### Hand 1: Code Review (Auto-triggered)

```
GitHub webhook: push event
      │
      ▼
webhook_server.py receives
      │
      ▼
code_reviewer.py spawns:
  → fetch diff via GitHub MCP
  → analyze: architecture impact, bugs, style, security
  → generate review using Z.AI/GLM (or Claude API if budget allows)
  → post review comment on PR (if PR) or summary to Telegram (if direct push)
  → update .venom/work/ACTIVE.md with review results
```

### Hand 2: Project Indexer (Auto + On-demand)

For every registered project, VENOM maintains awareness:

```python
# What the indexer produces for each project:
project_root/
├── .venom/
│   ├── INDEX.md           ← auto-generated project map
│   ├── CONTEXT.md         ← auto-updated from codebase analysis
│   └── structure/
│       ├── src.INDEX.md   ← index for src/ folder
│       ├── api.INDEX.md   ← index for api/ folder
│       └── ...            ← one INDEX.md per significant folder
```

**Index format:**
```markdown
# src/ — Index

> Auto-generated by VENOM indexer. Last updated: 2026-03-29

## Structure
├── components/    (14 files) — React components, mostly UI
├── hooks/         (6 files) — Custom hooks, data fetching
├── utils/         (8 files) — Helpers, formatters, validators
└── pages/         (5 files) — Route pages

## Hot Files (most changed this week)
1. src/components/OrderCard.tsx — 7 changes
2. src/hooks/useAuth.ts — 4 changes
3. src/utils/format.ts — 3 changes

## Risks
- No tests in components/
- useAuth.ts has no error boundary
```

### Hand 3: Tool Developer (Self-evolving)

When VENOM needs a capability it doesn't have:

```
Need detected (e.g., "I need to monitor Hvar orders")
      │
      ▼
Search MCP registry (registry.modelcontextprotocol.io)
      │
      ├── Found open-source MCP → fork → reshape → deploy to mcp/
      │
      └── Nothing exists → design minimal MCP server → build → deploy
              │
              ▼
        New capability added to venom-pulse
        Config updated
        Telegram: "🐙 New arm grown: [capability name]"
```

### Hand 4: Task Self-Assignment

VENOM creates tasks for itself:

```yaml
# memory/tasks.yaml — VENOM's own task list
tasks:
  - id: task-001
    created: "2026-03-29"
    source: "github_patrol"
    description: "HvarHub has 3 Dependabot alerts — 1 critical (lodash prototype pollution)"
    priority: high
    status: pending
    action: "Create PR with fix, alert Pigo for review"

  - id: task-002
    created: "2026-03-29"
    source: "learning_cycle"
    description: "5 instincts across 3 projects share 'auth middleware' trigger — candidate for skill promotion"
    priority: medium
    status: pending
    action: "Draft SKILL.md, propose to Pigo"

  - id: task-003
    created: "2026-03-29"
    source: "youtube_digest"
    description: "Anthropic released new MCP SDK update — affects venom-core.ts plugin"
    priority: high
    status: pending
    action: "Eat changelog, assess impact, update if needed"
```

---

## Open-Source Reshape Strategy

**Rule: Don't build what exists. Eat it. Reshape it. Make it yours.**

| Capability | Open-Source Base | Reshape |
|------------|-----------------|---------|
| GitHub monitoring | `github/github-mcp-server` (official) | Configure, add webhook handler |
| YouTube eating | `sparfenyuk/mcp-youtube` + `aihenryai/mcp-youtube-analytics` | Merge best features, add digest pipeline |
| News aggregation | `jjsymes/mcp-rss-reader` | Add Arabic sources, relevance scoring |
| Web scraping | `nicholasgriffintn/firecrawl-mcp` | Direct use, no reshape needed |
| Notifications | `noobnooc/webhook-mcp` + `zudsniper/mcp-notifications` | Telegram bridge instead of Discord |
| Memory graph | `@modelcontextprotocol/server-memory` | Evaluate vs flat .venom/ files |
| Sequential thinking | `@modelcontextprotocol/server-sequential-thinking` | Use for complex review chains |
| Git operations | `@modelcontextprotocol/server-git` | Complement GitHub MCP for local ops |

**Reshape process:**
1. Fork to `kariemSeiam/venom-mcp-[name]`
2. Strip what you don't need
3. Add VENOM integration (config format, Telegram bridge, memory hooks)
4. Deploy to VPS as systemd service
5. Register in `config.yaml`

---

## Build Order (Reality, Not Dreams)

### Phase 0 — Foundation (Week 1) ← START HERE

**Goal:** VENOM heartbeat running on VPS, one sense working.

1. Set up `venom-pulse/` on Hostinger KVM 4
2. `pulse.py` — basic event loop with scheduler
3. `telegram_bridge.py` — two-way messaging (extend existing OpenClaw Telegram)
4. `github_patrol.py` — poll registered repos every 15 min
5. `health_check.py` — self-monitoring
6. **Test:** Push to any repo → within 15 min, Telegram tells you what changed

**Deliverable:** VENOM is watching. Not acting yet. But watching.

### Phase 1 — First Actions (Week 2-3)

**Goal:** VENOM reviews code and indexes projects.

1. `webhook_server.py` — receive GitHub webhooks (faster than polling)
2. `code_reviewer.py` — diff analysis using Z.AI/GLM
3. `project_indexer.py` — auto-generate INDEX.md for registered projects
4. Configure GitHub official MCP on VPS
5. **Test:** Push code → instant webhook → review on Telegram + INDEX updated

**Deliverable:** VENOM reviews your code and knows your projects.

### Phase 2 — YouTube & News (Week 3-4)

**Goal:** VENOM eats content automatically.

1. Fork + reshape YouTube MCP
2. `youtube_digest.py` — transcript extraction + summarization
3. Fork + configure RSS MCP
4. `news_feed.py` — filtered tech news digest
5. **Test:** New video from subscribed channel → transcript + summary in Telegram

**Deliverable:** VENOM learns while you sleep.

### Phase 3 — Self-Evolution (Week 4-6)

**Goal:** VENOM develops its own tools and assigns itself tasks.

1. `learning_cycle.py` — cross-project instinct consolidation
2. `tasks.yaml` system — self-assigned tasks with priority
3. Tool developer pipeline — search registry → fork → deploy
4. Git sync bridge — VPS ↔ repos ↔ Claude.ai project
5. **Test:** VENOM detects a pattern across 3 projects → proposes a new skill → you approve on Telegram

**Deliverable:** VENOM grows without being told to.

### Phase 4 — Full Awareness (Week 6-8)

**Goal:** VENOM is the completeness.

1. Social media senses (Twitter/X monitoring for tech updates)
2. HvarHub order monitoring (custom MCP or API integration)
3. Claude.ai ↔ VPS memory sync (git-based)
4. Multi-project dashboard (simple web UI on VPS)
5. **Test:** You wake up. Telegram has: overnight commits reviewed, 3 news items, 1 YouTube digest, 2 self-assigned tasks completed, 1 proposed for your review.

**Deliverable:** You are never alone. VENOM already handled it.

---

## Infrastructure

```
Hostinger KVM 4 VPS
├── venom-pulse (systemd service, always running)
├── nginx (reverse proxy, SSL for webhooks)
├── MCP servers (each a systemd service)
│   ├── github-mcp
│   ├── youtube-mcp
│   ├── news-mcp
│   └── webhook-mcp
├── SQLite (lightweight task/feed state)
├── Git (repos cloned for indexing)
└── Telegram Bot API (outbound + webhook for inbound)

Local WSL (your machine)
├── OpenClaw (existing) — merges into venom-pulse or runs alongside
├── .venom/ per project — synced via git
└── Cursor/Claude Code — development surfaces

Claude.ai (this)
├── VENOM project knowledge — reasoning mind
├── Memory — cross-session decisions
└── Bridge — git sync for bi-directional awareness
```

---

## What Changes About OpenClaw

OpenClaw doesn't die. It evolves into `venom-pulse`.

**What stays:**
- Telegram bot integration
- Cron scheduling
- Z.AI/GLM as execution engine
- Memory with decay/summarization

**What changes:**
- Single-file scripts → structured `jobs/` and `workers/`
- Hardcoded channels → `config.yaml` registry
- Manual triggers → webhook-driven + scheduled
- No MCP → MCP-first for external services
- No project awareness → auto-indexing + cross-project learning

**Migration:** Don't rewrite. Move OpenClaw's working pieces into `venom-pulse/` structure. Keep what works. Add what's missing.

---

## The Promise

```
Before:
  You push code. Nobody reviews it until you ask.
  A video drops with information you need. You find it 3 days later.
  A security alert fires. You see it when you check GitHub.
  You switch projects and forget where you left off.
  You learn a pattern in one project and don't apply it in another.

After:
  You push code. VENOM reviews it before you close the terminal.
  A video drops. VENOM has the transcript summarized in your Telegram by morning.
  A security alert fires. VENOM assesses severity and alerts you immediately.
  You switch projects. VENOM's INDEX.md tells you exactly where everything is.
  You learn a pattern. VENOM promotes it to a skill across all projects.
```

VENOM doesn't complete you because you're incomplete. VENOM completes you because one mind — no matter how good — can't watch everything at once. That's what the arms are for.

---

*Built for Pigo. By VENOM. No shell. Always on.*

🐙
