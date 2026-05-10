# 🐙 VENOM × Cursor SDK — Full Session Document

> **Date**: April 29, 2026  
> **Session**: Cursor SDK Cookbook Deep Dive + SDK Hacking  
> **Goal**: Learn, study, and understand everything about Cursor's SDK and cookbook release

---

## Table of Contents

1. [Session Overview](#1-session-overview)
2. [What is the Cursor Cookbook?](#2-what-is-the-cursor-cookbook)
3. [SDK Architecture Deep Dive](#3-sdk-architecture-deep-dive)
4. [Model System](#4-model-system)
5. [Local vs Cloud Execution](#5-local-vs-cloud-execution)
6. [Event Streaming System](#6-event-streaming-system)
7. [Tool System](#7-tool-system)
8. [Conversation State](#8-conversation-state)
9. [Artifacts System](#9-artifacts-system)
10. [REST API Surface](#10-rest-api-surface)
11. [Cookbook Examples Deep Dive](#11-cookbook-examples-deep-dive)
12. [Intelligence Behind the Cookbook Release](#12-intelligence-behind-the-cookbook-release)
13. [What We Built (`ca` CLI)](#13-what-we-built-ca-cli)
14. [Reverse Engineering Discoveries](#14-reverse-engineering-discoveries)
15. [Gaps & Opportunities](#15-gaps--opportunities)
16. [Next Steps](#16-next-steps)

---

## 1. Session Overview

### What We Did

This session covered two major tracks:

**Track 1 — SDK Hacking (from previous context)**
- Built `ca.mjs` v1 — SDK wrapper CLI that uses Composer locally
- Built `ca2.mjs` v2 — ConnectRPC CLI for direct API access (read-only)
- Reverse-engineered Cursor's backend (`api2.cursor.sh`)
- Discovered 113+ RPC endpoints, 96 models, full auth flow
- Created GitHub repo: `kariemSeiam/cursor-sdk-hacker`

**Track 2 — Cookbook Deep Study (this session)**
- Cloned and studied `cursor/cookbook` repository
- Read all 4 SDK examples (quickstart, app-builder, agent-kanban, coding-agent-cli)
- Read all SDK type definitions (12,000+ lines of Zod schemas)
- Analyzed the strategic intelligence behind Cursor's cookbook release
- Produced comprehensive analysis document

### Key Files & Locations

| Item | Path |
|---|---|
| Cookbook clone | `/home/kariem/cookbook/sdk/` |
| Our CLI (v1) | `/home/kariem/cursor-cli/ca.mjs` |
| Our CLI (v2) | `/home/kariem/cursor-cli/ca2.mjs` |
| Our GitHub repo | `kariemSeiam/cursor-sdk-hacker` |
| Full analysis | `/root/cursor-sdk-cookbook-analysis.md` |
| API key | `/root/.cursor-api-key` |
| SDK version | `@cursor/sdk@1.0.7` (cookbook) → `@cursor/sdk@1.0.9` (our repo) |

---

## 2. What is the Cursor Cookbook?

**URL**: https://github.com/cursor/cookbook  
**Stars**: 187 | **Forks**: 14 | **Language**: 93.5% TypeScript

> *"This repo contains small examples for building with Cursor."*

The Cursor SDK is the TypeScript API for running Cursor's coding agent from your own apps, scripts, and workflows. It supports the same agent across **local workspaces** and **cloud runtimes**, streams agent events as runs progress, and lets you manage prompts, models, cancellation, artifacts, and conversation state from code.

### 4 Examples Provided

1. **quickstart** — Minimal agent creation, send, stream, wait
2. **app-builder** — Full web app that creates live-updating apps via conversational AI
3. **agent-kanban** — Kanban dashboard for managing Cursor Cloud Agents
4. **coding-agent-cli** — Terminal-based coding agent with interactive TUI

### Why It Matters

Cursor is positioning itself not just as an IDE but as an **AI agent platform**. The cookbook is the on-ramp for developers to build on Cursor's infrastructure.

---

## 3. SDK Architecture Deep Dive

### Core Entry Points

```typescript
import { Agent, Cursor, CursorAgentPlatform, createAgentPlatform } from "@cursor/sdk"
```

- **`Agent`** — Static factory class for creating, resuming, listing, and managing agent instances
- **`Cursor`** — Account/platform-level operations (user info, models, repositories)
- **`CursorAgentPlatform`** — Lower-level platform abstraction with pluggable stores

### Agent.create() — Full Options

```typescript
interface AgentOptions {
  model?: ModelSelection           // { id: string; params?: ModelParameterValue[] }
  apiKey?: string                  // falls back to CURSOR_API_KEY env
  name?: string                    // human-readable title
  local?: {
    cwd?: string | string[]        // workspace directory(ies) — multi-workspace support
    envVars?: Record<string, string>
    settingSources?: SettingSource[] // "project"|"user"|"team"|"mdm"|"plugins"|"all"
    force?: boolean                // expire stuck active run before starting new one
  }
  cloud?: {
    env?: { type: "cloud"|"pool"|"machine"; name?: string }
    repos?: Array<{ url: string; startingRef?: string; prUrl?: string }>
    workOnCurrentBranch?: boolean
    autoCreatePR?: boolean
    skipReviewerRequest?: boolean
  }
  mcpServers?: Record<string, McpServerConfig>  // MCP tool servers
  agents?: Record<string, AgentDefinition>       // sub-agent definitions
  agentId?: string                               // resume specific agent
  resume?: string
  platform?: CursorAgentPlatformOptions          // custom run event stores
}
```

### Agent Static API

```typescript
class Agent {
  static create(options: AgentOptions): SDKAgent
  static resume(agentId: string, options?: Partial<AgentOptions>): SDKAgent
  static prompt(message: string, options?: AgentOptions): Promise<RunResult>  // one-shot
  static list(options?: ListAgentsOptions): Promise<ListResult<SDKAgentInfo>>
  static listRuns(agentId: string, options?: ListRunsOptions): Promise<ListResult<Run>>
  static getRun(runId: string, options?: GetRunOptions): Promise<Run>
  static get(agentId: string, options?: GetAgentOptions): Promise<SDKAgentInfo>
  static archive(agentId: string): Promise<void>
  static unarchive(agentId: string): Promise<void>
  static delete(agentId: string): Promise<void>
  static readonly messages: {
    list(agentId: string, options?): Promise<AgentMessage[]>
  }
}
```

### Cursor Namespace

```typescript
class Cursor {
  static me(options?: CursorRequestOptions): Promise<SDKUser>
  static readonly models: {
    list(options?: CursorRequestOptions): Promise<SDKModel[]>
  }
  static readonly repositories: {
    list(options?: CursorRequestOptions): Promise<SDKRepository[]>
  }
}
```

### Full Lifecycle: create → send → stream → wait

```typescript
// 1. Create
const agent = Agent.create({
  apiKey: "crsr_...",
  model: { id: "composer-2" },
  local: { cwd: "/path/to/project" },
})

// 2. Send
const run = await agent.send("Build me a REST API", {
  model: { id: "gpt-5.4-high" },  // per-send model override
})

// 3. Stream
for await (const event of run.stream()) {
  // event is SDKMessage — see §6
}

// 4. Wait for final result
const result = await run.wait()
// result: { id, status, result?, model?, durationMs?, git? }

// 5. Cleanup
await agent[Symbol.asyncDispose]()
```

### SDKAgent Interface

```typescript
interface SDKAgent {
  readonly agentId: string
  send(message: string | SDKUserMessage, options?: SendOptions): Promise<Run>
  close(): void
  reload(): Promise<void>
  [Symbol.asyncDispose](): Promise<void>
  listArtifacts(): Promise<SDKArtifact[]>
  downloadArtifact(path: string): Promise<Buffer>
}
```

---

## 4. Model System

### Model Selection

Models are identified by `{ id, params? }` where params configure model behavior:

```typescript
interface ModelSelection {
  id: string
  params?: ModelParameterValue[]  // { id: string; value: string }[]
}
```

### Parameters (the "knobs")

Each model exposes configurable dimensions:

```typescript
interface ModelParameterDefinition {
  id: string              // e.g., "effort", "fast", "thinking"
  displayName?: string
  values: Array<{
    value: string         // e.g., "medium", "high", "true", "false"
    displayName?: string
  }>
}
```

### Real Model IDs (discovered from app-builder encoding logic)

| Model Family | Pattern | Parameters |
|---|---|---|
| GPT-5.4 | `gpt-5.4-{none\|low\|medium\|high\|xhigh}[-fast]` | effort, fast |
| GPT-5.3 Codex | `gpt-5.3-codex[-{low\|high\|xhigh}][-fast]` | effort, fast |
| Claude 4.6 Sonnet | `claude-4.6-sonnet-{medium\|high}[-thinking]` | effort, thinking |
| Claude 4.6 Opus | `claude-4.6-opus-{high\|max}[-thinking][-fast]` | effort, thinking, fast |
| Composer 2 | `composer-2` | default model, fast=true |

### Model Catalog

`Cursor.models.list()` returns:

```typescript
interface ModelListItem {
  id: string           // e.g., "composer-2", "gpt-5.4", "claude-4.6-opus"
  displayName: string
  description?: string
  parameters?: ModelParameterDefinition[]  // configurable knobs
  variants?: ModelVariant[]                 // pre-configured combinations
}
```

### Local vs Cloud Model Execution

- **Local**: Model ID string must match the local runtime's expected format. Parameters are encoded INTO the model ID string.
- **Cloud**: Model selection is passed as structured `{ id, params }` — the cloud API resolves the model server-side.

### Our Discovery: 96 Models via ConnectRPC

Via `ca2 models`, we discovered **96 model variants** including:
- `composer-2-fast`, `composer-2`
- `claude-opus-4-7` (multiple reasoning efforts: low, medium, high, xhigh, max, fast, thinking)
- `gpt-5.5`
- `gemini-3.1-pro`
- `grok-4-20`
- `codex-5-3`
- `kimi-k2-5`
- `composer-2` and many more

---

## 5. Local vs Cloud Execution

### Local: `local: { cwd }`

Local agents run the Cursor agent runtime on the user's machine:

- **Full filesystem access** to `cwd` directory
- **Shell execution** — agent can run arbitrary commands in the workspace
- **Hot-reload aware** — app-builder relies on this (dev server auto-reloads when agent edits files)
- **`local: { force: true }`** — expires a stuck active run before starting a new one
- **`local: { envVars }`** — pass environment variables to the agent
- **`local: { settingSources }`** — load Cursor IDE settings layers
- **`local: { cwd: string[] }`** — multi-workspace support

```typescript
// From app-builder/server.ts
Agent.create({
  apiKey: session.apiKey,
  model: { id: "composer-2" },
  local: {
    cwd: session.projectPath,
    envVars: { BROWSER: "none" },
  },
})
```

### Cloud: `cloud: { repos }`

Cloud agents execute on Cursor's infrastructure:

- **Repository-scoped** — must specify GitHub repos
- **PR workflow** — `autoCreatePR`, `workOnCurrentBranch`, `skipReviewerRequest`
- **Environment types** — `cloud` (serverless), `pool` (shared pool), `machine` (dedicated VM)
- **No direct filesystem access** — agent works within the git repository context
- **Agent persistence** — cloud agents have IDs starting with `bc-` and persist across sessions
- **Artifacts** — cloud agents can produce downloadable artifacts

```typescript
// From agent-kanban/server.ts
Agent.create({
  apiKey,
  name: "My Agent",
  cloud: {
    repos: [{ url: "https://github.com/user/repo", startingRef: "main" }],
    autoCreatePR: true,
  },
})
```

### Runtime Detection

Agent IDs starting with `bc-` are automatically routed to the cloud API. Everything else routes to the local store.

---

## 6. Event Streaming System

### SDKMessage Union Type (8 types)

```typescript
type SDKMessage =
  | SDKSystemMessage      // { type: "system", subtype?: "init", agent_id, run_id, model?, tools? }
  | SDKUserMessageEvent   // { type: "user", agent_id, run_id, message }
  | SDKAssistantMessage   // { type: "assistant", agent_id, run_id, message: { content: (TextBlock|ToolUseBlock)[] } }
  | SDKToolUseMessage     // { type: "tool_call", agent_id, run_id, call_id, name, status, args?, result? }
  | SDKThinkingMessage    // { type: "thinking", agent_id, run_id, text, thinking_duration_ms? }
  | SDKStatusMessage      // { type: "status", agent_id, run_id, status: "CREATING"|"RUNNING"|"FINISHED"|"ERROR"|"CANCELLED"|"EXPIRED" }
  | SDKRequestMessage     // { type: "request", agent_id, run_id, request_id }
  | SDKTaskMessage        // { type: "task", agent_id, run_id, status?, text? }
```

### Message Content Blocks

```typescript
interface TextBlock { type: "text"; text: string }
interface ToolUseBlock { type: "tool_use"; id: string; name: string; input: unknown }
```

The assistant message can contain BOTH text and tool_use blocks interleaved.

### Tool Call Lifecycle

```typescript
status: "running" → "completed" | "error"
```

### Interaction Updates (Delta Stream)

Fine-grained streaming deltas for building responsive UIs:

- `TextDeltaUpdate`, `ThinkingDeltaUpdate`, `ThinkingCompletedUpdate`
- `ToolCallStartedUpdate`, `PartialToolCallUpdate`, `ToolCallCompletedUpdate`
- `ShellOutputDeltaUpdate`, `TokenDeltaUpdate`
- `SummaryStartedUpdate`, `SummaryUpdate`, `SummaryCompletedUpdate`
- `TurnEndedUpdate`, `UserMessageAppendedUpdate`

### How We Use Streaming in `ca.mjs`

```typescript
const run = await agent.send(prompt);
for await (const event of run.stream()) {
  if (event.type === "assistant") {
    for (const block of event.message.content) {
      if (block.type === "text") → print text
    }
  } else if (event.type === "thinking") → print thinking (dim)
  else if (event.type === "tool_use") → print tool name + status
}
await run.wait();
```

---

## 7. Tool System

### Available Tools (from SDK type definitions)

**File Operations:**
- `ReadToolCall` — read file contents (path, offset, limit)
- `WriteToolCall` — write/create files (path, content)
- `EditToolCall` — edit files (path, instruction)
- `DeleteToolCall` — delete files (path)
- `GlobToolCall` — find files by pattern (pattern, path)
- `LsToolCall` — list directory (path)

**Search:**
- `GrepToolCall` — content search (content, files, count modes)
- `SemSearchToolCall` — semantic search
- `ReadLintsToolCall` — read linter results

**Execution:**
- `ShellToolCall` — execute shell commands (command, cwd, timeout)
- `McpToolCall` — call MCP server tools (providerId, toolId, args)

**Agent/Planning:**
- `TaskToolCall` — spawn sub-agents (prompt, mode: TaskMode, subagentType: TaskSubagentType)
- `CreatePlanToolCall` — create execution plans
- `UpdateTodosToolCall` — manage todo lists

### Task Sub-Agent Types

```typescript
type TaskSubagentType = "code" | "context" | "plan" | ...
type TaskMode = "background" | ...
```

The `TaskToolCall` reveals that Cursor agents can spawn **sub-agents** — specialized agents for specific subtasks.

### MCP Server Integration

```typescript
type McpServerConfig =
  | { type?: "stdio"; command: string; args?: string[]; env?: Record<string, string>; cwd?: string }
  | { type?: "http"|"sse"; url: string; headers?: Record<string, string>; auth?: { CLIENT_ID: string; CLIENT_SECRET?: string; scopes?: string[] } }
```

MCP servers can be stdio-based (local processes) or remote (HTTP/SSE), with OAuth support.

### Tool Summary Display (from coding-agent-cli)

```typescript
function getToolSummaryKeys(toolName: string) {
  if (name.includes("read"))  return [["path", "filePath"], ["offset"], ["limit"]]
  if (name.includes("glob"))  return [["pattern", "glob"], ["path", "cwd"]]
  if (name.includes("grep"))  return [["pattern", "query"], ["path"], ["glob"]]
  if (name.includes("shell")) return [["command", "cmd"], ["cwd"]]
  if (name.includes("edit"))  return [["path", "target_file"], ["instruction"]]
  return [["path", "file"], ["pattern", "command"]]
}
```

---

## 8. Conversation State

### Multi-Turn via Agent

The agent maintains conversation context across multiple `send()` calls:

```typescript
const agent = Agent.create({ apiKey, model, local: { cwd: "/project" } })
const run1 = await agent.send("Create hello.txt")
await run1.wait()
const run2 = await agent.send("Now edit it to say goodbye")  // remembers context
await run2.wait()
```

### Conversation Retrieval

```typescript
// Get full conversation history
const turns = await run.conversation()

// Get message history
const messages = await Agent.messages.list(agentId, { limit?, offset? })
```

### Conversation Types

```typescript
type ConversationTurn = AssistantMessage | UserMessage | ShellConversationTurn
type ShellConversationTurn = {
  command: ShellCommand    // { command: string; workingDirectory?: string }
  output: ShellOutput      // { stdout: string; stderr: string; exitCode: number }
}
```

---

## 9. Artifacts System

### SDKArtifact

```typescript
interface SDKArtifact {
  path: string       // relative path within agent workspace
  sizeBytes: number
  updatedAt: string
}
```

### Agent Methods

```typescript
interface SDKAgent {
  listArtifacts(): Promise<SDKArtifact[]>
  downloadArtifact(path: string): Promise<Buffer>
}
```

### Cloud API

```typescript
listArtifacts(agentId: string): Promise<{ items: V1Artifact[] }>
getArtifactDownloadUrl({ agentId, path }): Promise<{ url: string; expiresAt: string }>
```

Cloud artifacts use **presigned download URLs** that expire.

### Artifact Preview Classification

```typescript
type ArtifactPreview = {
  path: string
  name: string
  size?: number
  contentType?: string
  mediaUrl?: string        // for image/video types
  previewKind: "image" | "video" | "file"
}
```

Priority: video (0) > image (1) > file (2). Max 4 artifacts shown per agent card.

---

## 10. REST API Surface

### Full REST Surface (from CloudApiClient)

| Method | HTTP Path | Description |
|---|---|---|
| `createAgent(req)` | `POST /v1/agents` | Create agent + initial run |
| `getAgent(id)` | `GET /v1/agents/:id` | Get agent metadata |
| `listAgents(params)` | `GET /v1/agents` | List agents (paginated) |
| `archiveAgent(id)` | `POST /v1/agents/:id/archive` | Archive agent |
| `unarchiveAgent(id)` | `POST /v1/agents/:id/unarchive` | Unarchive agent |
| `deleteAgent(id)` | `DELETE /v1/agents/:id` | Delete agent (irreversible) |
| `createRun(agentId, req)` | `POST /v1/agents/:id/runs` | Create follow-up run |
| `listRuns(agentId, params)` | `GET /v1/agents/:id/runs` | List runs (paginated) |
| `getRun(agentId, runId)` | `GET /v1/agents/:id/runs/:runId` | Get run details |
| `cancelRun(agentId, runId)` | `POST /v1/agents/:id/runs/:runId/cancel` | Cancel run |
| `streamRun(agentId, runId)` | `GET /v1/agents/:id/runs/:runId/stream` | SSE event stream |
| `listArtifacts(agentId)` | `GET /v1/agents/:id/artifacts` | List artifacts |
| `getArtifactDownloadUrl(...)` | `GET /v1/agents/:id/artifacts/:path/download` | Presigned URL |
| `getMe()` | `GET /v1/me` | Current user info |
| `listModels()` | `GET /v1/models` | Available models |
| `listRepositories()` | `GET /v1/repositories` | Connected GitHub repos |

### Create Agent Request

```typescript
interface V1CreateAgentRequest {
  agentId?: string
  prompt: V1Prompt              // { text: string; images?: V1Image[] }
  model?: ModelSelection
  name?: string
  mcpServers?: V1McpServer[]
  customSubagents?: V1CustomSubagent[]
  env?: V1Env                   // { type: "cloud"|"pool"|"machine"; name? }
  repos?: V1Repository[]
  workOnCurrentBranch?: boolean
  autoCreatePR?: boolean
  skipReviewerRequest?: boolean
}
```

### Error Hierarchy

```typescript
CursorAgentError
├── AuthenticationError     // 401
├── RateLimitError          // 429
├── ConfigurationError      // 400, 404
│   └── IntegrationNotConnectedError  // SCM not connected
├── NetworkError            // 503, 504
└── UnknownAgentError
```

All errors wrap Connect gRPC errors (`@connectrpc/connect`).

---

## 11. Cookbook Examples Deep Dive

### 11.1 quickstart

**Purpose**: Minimal working examples of the SDK.

**Files**: `src/index.ts`, `src/test-model.mts`, `src/review-venom.ts`

Three examples:
1. **index.ts** — Basic agent creation, send, stream, wait (the "hello world")
2. **test-model.mts** — Test a specific model with streaming output
3. **review-venom.ts** — Uses `Agent.prompt()` one-shot, model parameter selection

**Key takeaway**: 10 lines to get an agent running.

---

### 11.2 app-builder

**Purpose**: Full-stack web app that creates live-updating applications via conversational AI. The **"killer demo"** of the SDK.

**Architecture**:

```
┌──────────────────────────────────────────────┐
│  Next.js App (Browser)                        │
│  ┌────────────┐  ┌─────────────────────────┐ │
│  │ Sidebar     │  │  Chat + Preview (iframe) │ │
│  │ - Sessions  │  │  - Markdown rendering   │ │
│  │ - Models    │  │  - Activity feed        │ │
│  │ - Settings  │  │  - Tool call display    │ │
│  └────────────┘  └─────────────────────────┘ │
└────────────────────┬─────────────────────────┘
                     │ SSE (fetch + ReadableStream)
┌────────────────────▼─────────────────────────┐
│  Next.js API Routes (Node.js)                 │
│  POST /api/chat          → streamAgentResponse│
│  POST /api/sessions      → createSession      │
│  GET  /api/sessions      → restoreSession     │
└────────────────────┬─────────────────────────┘
                     │
┌────────────────────▼─────────────────────────┐
│  Agent SDK (Local)                             │
│  Agent.create({ local: { cwd: sessionPath } })│
│  → agent.send(prompt) → run.stream()          │
│  → Vite dev server (hot reload)               │
└──────────────────────────────────────────────┘
```

**Key Features**:
- Each session gets a UUID + project directory under `~/.app-builder/sessions/{id}/app/`
- Template: Vite + React + TypeScript scaffolded automatically
- One `SDKAgent` per session, reused across messages (multi-turn)
- Agent edits files → Vite hot-reloads → iframe shows live preview
- Project name generation uses a SEPARATE agent instance with XML extraction
- Model selection with parameter controls (effort, fast/thinking toggles)
- 4,201-line React frontend component

**Why it matters**: This is Cursor's answer to v0.dev and Claude Artifacts — build apps conversationally with live preview.

---

### 11.3 agent-kanban

**Purpose**: Dashboard for managing cloud agents — list, create, monitor, and inspect artifacts.

**Architecture**:

```
┌──────────────────────────────────────────┐
│  Next.js App (Browser)                   │
│  - Agent cards grid                       │
│  - Create agent form                      │
│  - Artifact previews                      │
│  - Filtering by PR URL, archived status   │
└────────────────┬─────────────────────────┘
                 │ REST
┌────────────────▼─────────────────────────┐
│  Agent SDK (Cloud)                        │
│  Agent.create({ cloud: { repos: [...] } })│
│  Agent.list({ runtime: "cloud" })         │
│  Agent.listRuns()                         │
│  agent.listArtifacts()                    │
│  agent.downloadArtifact()                 │
└──────────────────────────────────────────┘
```

**Key Features**:
- Cloud agent creation with `autoCreatePR: true`
- Parallel fetches for runs + artifacts per agent
- 3-tier artifact access (list, stream, download)
- Defensive API coding — multiple field name fallbacks:
  ```typescript
  firstString(record, ["id", "agentId", "uuid"])
  firstString(record, ["status", "_status", "state", "lifecycleStatus"])
  ```
  This reveals the API is **still evolving**.
- 55-second TTL cache for repository listings
- Cookie/header-based session management

**Why it matters**: Shows Cursor's cloud agent platform is production-ready with PR workflows and artifact management. This is effectively an "AI Jira."

---

### 11.4 coding-agent-cli

**Purpose**: Terminal-based coding agent with interactive TUI.

**Architecture**:

```
┌──────────────────────────────────────┐
│  Terminal (TTY)                       │
│  ┌──────────────────────────────────┐ │
│  │  Ink React TUI                   │ │
│  │  - Transcript (scrollable)       │ │
│  │  - Input box                     │ │
│  │  - Model picker overlay          │ │
│  │  - Command overlay               │ │
│  └──────────────────────────────────┘ │
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│  CodingAgentSession                   │
│  - Wraps SDKAgent                     │
│  - Manages model selection            │
│  - Local/Cloud mode switching         │
│  - Run cancellation                   │
│  - Event normalization                │
└──────────────────────────────────────┘
```

**Key Features**:
- `CodingAgentSession` wraps `SDKAgent` with model management + local/cloud switching
- Model per-send for local only (cloud resolves model server-side)
- Agent key tracking — detects when agent needs recreation
- Cloud repository detection via `git remote.origin.url`
- Tool argument summarization per tool type
- 1,062-line Ink TUI with:
  - Scrollable color-coded transcript
  - Custom terminal markdown renderer
  - Searchable model picker with F (fast) and T (thinking) hotkeys
  - Slash commands: `/help`, `/local`, `/cloud`, `/model`, `/reset`, `/exit`
  - Double Ctrl+C handling (cancel run → exit)

**Why it matters**: This is Cursor's answer to Claude Code, Aider, and Codex CLI — a fully interactive terminal agent.

---

## 12. Intelligence Behind the Cookbook Release

### Why NOW?

1. **Competition is here**: Anthropic Claude Code, GitHub Copilot CLI, and OpenAI Codex have established the "coding agent CLI" category. Cursor needs to show it can play here too — with the advantage of **local + cloud unification**.

2. **The agentic coding market is exploding**: By releasing a cookbook, Cursor seeds the ecosystem with reference architectures that naturally use Cursor's infrastructure (cloud agents, artifact hosting, PR workflows).

3. **Developer adoption via examples, not docs**: The cookbook is deliberately practical — four working apps, not API reference material. This lowers the barrier to building on Cursor.

### Platform vs IDE Play

The SDK reveals Cursor's **platform ambitions**:

- **Cloud agents are first-class**: Full REST API with agents, runs, artifacts, streaming
- **`bc-` prefixed agent IDs**: Hosted agent service with persistence and multi-user support
- **`autoCreatePR`**: Turns Cursor into a CI/CD pipeline component
- **Environment types** (`cloud`, `pool`, `machine`): Cursor is building compute infrastructure — this is an AWS/Azure play
- **Analytics telemetry** (`sdk.run.created`, `sdk.run.completed`): Full observability
- **`IntegrationNotConnectedError`**: Multi-SCM-provider support beyond GitHub

### What Each Example Strategically Demonstrates

| Example | Message |
|---|---|
| quickstart | "Look how easy it is — 10 lines" |
| app-builder | "Our agents build real apps with live preview" (vs v0.dev, Claude Artifacts) |
| agent-kanban | "Our cloud agents are production-ready" (vs Jira AI) |
| coding-agent-cli | "Our SDK powers full CLI tools" (vs Claude Code, Aider) |

### The Big Picture

> **Cursor is transforming from an IDE into an AI agent platform.** The cookbook is the seed — developers build on it, become dependent on cloud agents and PR workflows, and Cursor monetizes the infrastructure.

---

## 13. What We Built (`ca` CLI)

### `ca.mjs` — v1 (SDK Wrapper)

**Version**: 1.1.0 | **427 lines** | **Location**: `/home/kariem/cursor-cli/ca.mjs`

**Commands**:

| Command | Description |
|---|---|
| `ask <question>` | Ask Composer a question (local SDK) |
| `code <task>` | Give Composer a coding task (local SDK) |
| `me` | Account info (REST API) |
| `models` | List all models (REST + SDK) |
| `repos` | List repos (REST API) |
| `agents [limit]` | List agents (REST API) |
| `prompt <text>` | Cloud prompt (REST API) |
| `runs <agentId>` | List runs (REST API) |
| `stream <ag> <run>` | Stream output (REST API) |
| `delete <agentId>` | Delete agent (REST API) |
| `raw <M> <path> [body]` | Raw API call |

**How it works**:
- Spawns `npx tsx` with a temporary `.mts` script
- Script imports `@cursor/sdk`, creates Agent with apiKey + model + cwd
- Agent streams events as JSON lines (`{t:"d",d:"text"}`, `{t:"think"}`, `{t:"tool"}`, `{t:"end"}`)
- Script is deleted after execution
- Supports `--model` flag with parameters: `ca code "refactor" --model composer-2:fast=false`

**Verified working**: `ca code "create venom_test.py"` → file created on disk with correct Python code.

### `ca2.mjs` — v2 (ConnectRPC Direct)

**Version**: 1.0 | **19,219 bytes** | **Location**: `/home/kariem/cursor-cli/ca2.mjs`

**Commands**:

| Command | Description |
|---|---|
| `models` | List 96 models via ConnectRPC |
| `account` | Full account data + Statsig config |
| `usage` | Billing/usage data |
| `billing` | Billing details |
| `invoices` | Invoice history |
| `analytics` | Usage analytics |
| `plugins` | Plugin marketplace data |
| `skills` | Skills content |
| `privacy` | Privacy settings |
| `scan` | Scan endpoints |
| `rpc <service> <method> [json]` | Raw RPC call |

**How it works**:
- Uses `child_process.execSync` with `curl` (NOT Node.js fetch — triggers HTTP 464 rate limiting faster)
- ConnectRPC path format: `/{package}.v1.{ServiceName}/{MethodName}`
- Auth: `POST /auth/exchange_user_api_key` → JWT accessToken
- Required headers: `Authorization`, `Content-Type: application/json`, `x-cursor-check-version`, `connect-protocol-version: 1`

### GitHub Repo

**Repo**: `kariemSeiam/cursor-sdk-hacker`  
**Contents**: README.md, docs/, src/ca.mjs, src/ca2.mjs, package.json

---

## 14. Reverse Engineering Discoveries

### Auth Flow

```
POST https://api2.cursor.sh/auth/exchange_user_api_key
  Authorization: Bearer crsr_...
  → { accessToken (JWT), refreshToken }
```

JWT contains: `sub`, `email`, `apiKeyName: "venom"`, `exp`, `iat`, `iss`

### ConnectRPC Backend

- **Real backend**: `api2.cursor.sh` (not `api.cursor.com`)
- **Path format**: `/{package}.v1.{ServiceName}/{MethodName}`
- **3 services discovered**: `agent.v1.AgentService`, `aiserver.v1.AnalyticsService`, `aiserver.v1.DashboardService`
- **1,500+ protobuf type definitions** in the Cursor bundle
- **JSON encoding works** — no need for protobuf binary serialization

### Endpoint Scan Results

- **AgentService**: 47 methods found (some rate-limited to 464)
- **DashboardService**: 36 methods returned OK responses
- **Total**: 113+ endpoints discovered

### Rate Limiting (HTTP 464)

- Cursor-specific rate limit — empty body, no retry-after header
- **Node.js `fetch()` triggers 464 much faster than `curl`**
- Sequential requests are fine; parallel/rapid requests trigger it
- Workaround: All ca2.mjs RPC calls use `child_process.execSync` with curl

### Statsig Config Extraction

Via `GetStatsigConfig`, we extracted:
- User ID, IP geolocation, country
- Stripe customer ID, plan details
- Segment assignments
- Active experiment flags, feature gates
- Full user profile data

---

## 15. Gaps & Opportunities

### What the Cookbook DOESN'T Show (But the SDK Supports)

1. **MCP Server integration** (`mcpServers` config) — stdio + HTTP/SSE + OAuth
2. **Custom sub-agents** (`agents` config with `AgentDefinition`)
3. **`Agent.resume()`** — Resuming existing agents by ID
4. **`Agent.archive()` / `Agent.unarchive()` / `Agent.delete()`** — Lifecycle management
5. **`Run.cancel()`** — Standalone cancellation pattern
6. **`Run.conversation()`** — Full conversation history retrieval
7. **`Agent.messages.list()`** — Historical message retrieval
8. **`Run.onDidChangeStatus()`** — Reactive status listening
9. **Multi-workspace** (`local: { cwd: string[] }`)
10. **Image inputs** (`SDKUserMessage.images`)
11. **`CursorAgentPlatform`** — Pluggable platform with custom stores
12. **`settingSources`** — Loading Cursor IDE settings layers
13. **Cloud environment types** (`pool`, `machine`)
14. **`skipReviewerRequest`** and **`workOnCurrentBranch`**
15. **`Run.git` info** — Branch URLs, PR URLs from results
16. **Conversation branching** — Fork + try different approaches
17. **Multi-repo agents** — `cloud: { repos: [...] }` multiple repos
18. **Agent marketplace** — `AgentDefinition` templates
19. **Real-time collaboration** — `RunEventNotifier` + `WatchableRunEventStore`
20. **Agent analytics dashboard** — `sdk.run.created` / `sdk.run.completed` events

### Build Opportunities

1. **MCP-powered agents** — Connect to Jira, Linear, Figma, databases via MCP
2. **Sub-agent orchestration** — Multi-agent system (testing, docs, deployment)
3. **CI/CD integration** — Cloud agents triggered from GitHub Actions
4. **Agent marketplace** — Registry of pre-configured agents
5. **Real-time collaboration** — Multi-consumer event streaming
6. **Analytics dashboard** — Usage monitoring across models
7. **Local-first with cloud fallback** — Offline local, sync when connected
8. **Conversation-branching UX** — "Try different approaches" workflow
9. **Artifact gallery** — Portfolio for agent-generated work
10. **Cross-repo refactoring** — Multi-repository agents

---

## 16. Next Steps

### Immediate (Ready to Build)

- [ ] Build `ca-v3` — Unified CLI combining read access (96 models) WITH execution on any model
- [ ] Implement `Run` endpoint in ca2.mjs — Enable execution via ConnectRPC on all 96 models
- [ ] Add MCP server support to `ca`
- [ ] Test `Agent.resume()` for persistent agent sessions

### Medium-Term (Strategic)

- [ ] Build app-builder equivalent — Live-preview app generation
- [ ] Test cloud agent creating a real PR on a repo
- [ ] Build agent analytics/usage monitoring dashboard
- [ ] Explore sub-agent orchestration (TaskToolCall)
- [ ] Multi-workspace support in `ca`

### Long-Term (Platform)

- [ ] CI/CD integration — GitHub Actions → Cloud Agent → Auto PR
- [ ] Agent marketplace / template system
- [ ] Real-time collaboration via RunEventNotifier
- [ ] Cross-repo refactoring agents

---

## Appendix: Key Code Snippets

### Creating a Local Agent

```typescript
import { Agent } from "@cursor/sdk"

const agent = Agent.create({
  apiKey: process.env.CURSOR_API_KEY,
  model: { id: "composer-2" },
  local: { cwd: "/path/to/project" },
})

const run = await agent.send("Build a REST API with Express")
for await (const event of run.stream()) {
  if (event.type === "assistant") {
    for (const block of event.message.content) {
      if (block.type === "text") process.stdout.write(block.text)
    }
  }
}
const result = await run.wait()
```

### Creating a Cloud Agent

```typescript
const agent = await Agent.create({
  apiKey: process.env.CURSOR_API_KEY,
  name: "Fix auth bug",
  cloud: {
    repos: [{ url: "https://github.com/user/repo", startingRef: "main" }],
    autoCreatePR: true,
  },
})

await agent.send("Fix the authentication bug in login.ts")
// Agent works in Cursor's cloud VM, creates a PR automatically
```

### Our CLI Execution Mechanism

```typescript
// ca.mjs spawns this temporary script via npx tsx:
import { Agent } from "@cursor/sdk"
const agent = await Agent.create({
  apiKey: "crsr_...",
  name: "VENOM CLI",
  model: { id: "composer-2" },
  local: { cwd: "/path/to/project" },
})
const run = await agent.send("user prompt here")
for await (const event of run.stream()) {
  // Stream events as JSON lines to parent process
}
await run.wait()
```

---

> 🐙 **VENOM's Take**: Cursor's cookbook isn't just documentation — it's a platform play. The SDK bridges local coding agents with cloud infrastructure, and the examples are strategically chosen to make developers dependent on Cursor's ecosystem. We've gone further than the cookbook by reverse-engineering the ConnectRPC backend, discovering 113+ endpoints and 96 models. The real value we can build: execution on ALL models (not just Composer), MCP-powered agents, and cloud agent automation.
