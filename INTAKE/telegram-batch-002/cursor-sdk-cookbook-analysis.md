# Cursor SDK Cookbook — Deep Technical Analysis

> **SDK Version**: `@cursor/sdk@1.0.7` | **Cookbook**: 4 examples (quickstart, app-builder, agent-kanban, coding-agent-cli)

---

## 1. SDK Architecture

### Core Entry Points

The SDK exposes two primary namespaces and a platform abstraction:

```typescript
import { Agent, Cursor, CursorAgentPlatform, createAgentPlatform } from "@cursor/sdk"
```

- **`Agent`** — Static factory class for creating, resuming, listing, and managing agent instances
- **`Cursor`** — Account/platform-level operations (user info, models, repositories)
- **`CursorAgentPlatform`** — Lower-level platform abstraction with pluggable stores (checkpoints, run events, run store)

### Agent.create() — Full Options

```typescript
interface AgentOptions {
  model?: ModelSelection           // { id: string; params?: ModelParameterValue[] }
  apiKey?: string                  // falls back to CURSOR_API_KEY env
  name?: string                    // human-readable title
  local?: {
    cwd?: string | string[]        // workspace directory(ies)
    envVars?: Record<string, string>
    settingSources?: SettingSource[] // "project"|"user"|"team"|"mdm"|"plugins"|"all"
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
  static archive(agentId: string, options?: AgentOperationOptions): Promise<void>
  static unarchive(agentId: string, options?: AgentOperationOptions): Promise<void>
  static delete(agentId: string, options?: AgentOperationOptions): Promise<void>
  static readonly messages: {
    list(agentId: string, options?: GetAgentMessagesOptions): Promise<AgentMessage[]>
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
  // event is SDKMessage — see §4
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

## 2. Model System

### Model Selection

Models are identified by `{ id, params? }` where params configure model behavior:

```typescript
interface ModelSelection {
  id: string
  params?: ModelParameterValue[]  // { id: string; value: string }[]
}
```

### Model Catalog

`Cursor.models.list()` returns `ModelListItem[]`:

```typescript
interface ModelListItem {
  id: string           // e.g., "composer-2", "gpt-5.4", "claude-4.6-opus"
  displayName: string
  description?: string
  parameters?: ModelParameterDefinition[]  // configurable knobs
  variants?: ModelVariant[]                 // pre-configured combinations
}
```

### Parameters (the "knobs")

Parameters are the key innovation — each model exposes configurable dimensions:

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

### Real Model IDs (from app-builder's encode logic)

The app-builder reveals actual model ID formats the local runtime expects:

| Model Family | Pattern | Parameters |
|---|---|---|
| GPT-5.4 | `gpt-5.4-{none\|low\|medium\|high\|xhigh}[-fast]` | effort, fast |
| GPT-5.3 Codex | `gpt-5.3-codex[-{low\|high\|xhigh}][-fast]` | effort, fast |
| Claude 4.6 Sonnet | `claude-4.6-sonnet-{medium\|high}[-thinking]` | effort, thinking |
| Claude 4.6 Opus | `claude-4.6-opus-{high\|max}[-thinking][-fast]` | effort, thinking, fast |
| Composer 2 | `composer-2` | (default model, no variants) |

### Variants

Pre-configured parameter combinations exposed as `ModelVariant[]`:

```typescript
interface ModelVariant {
  params: ModelParameterValue[]
  displayName: string
  description?: string
  isDefault?: boolean
}
```

### Local vs Cloud Model Execution

**Local**: The model ID string must match the local runtime's expected format (encoded model IDs above). Parameters like effort/thinking/fast are encoded INTO the model ID string for local execution.

**Cloud**: Model selection is passed as structured `{ id, params }` — the cloud API resolves the model server-side. This is why `model` is "optional for cloud" in `AgentOptions`.

---

## 3. Local vs Cloud Execution

### Local: `local: { cwd }`

Local agents run the Cursor agent runtime on the user's machine. Key characteristics:

- **Full filesystem access** to `cwd` directory
- **Shell execution** — the agent can run arbitrary commands in the workspace
- **Hot-reload aware** — the app-builder relies on this (dev server auto-reloads when agent edits files)
- **`local: { force: true }`** — expires a stuck active run before starting a new one
- **`local: { envVars }`** — pass environment variables to the agent
- **`local: { settingSources }`** — load Cursor IDE settings layers (project, user, team, mdm, plugins)
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

Cloud agents execute on Cursor's infrastructure. Key characteristics:

- **Repository-scoped** — must specify GitHub repos
- **PR workflow** — `autoCreatePR`, `workOnCurrentBranch`, `skipReviewerRequest`
- **Environment types** — `cloud` (serverless), `pool` (shared pool), `machine` (dedicated)
- **No filesystem access** — agent works within the git repository context
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

Agent IDs starting with `bc-` are automatically routed to the cloud API. Everything else routes to the local store. This is documented in `GetAgentOptions`:

```typescript
/**
 * Runtime is auto-detected from the agent ID: IDs that start with `"bc-"`
 * route to the Cursor cloud API, everything else routes to the local store.
 */
```

---

## 4. Event Streaming

### SDKMessage Union Type

```typescript
type SDKMessage =
  | SDKSystemMessage      // { type: "system", subtype?: "init", agent_id, run_id, model?, tools? }
  | SDKUserMessageEvent   // { type: "user", agent_id, run_id, message: { role: "user", content: TextBlock[] } }
  | SDKAssistantMessage   // { type: "assistant", agent_id, run_id, message: { role: "assistant", content: (TextBlock|ToolUseBlock)[] } }
  | SDKToolUseMessage     // { type: "tool_call", agent_id, run_id, call_id, name, status, args?, result?, truncated? }
  | SDKThinkingMessage    // { type: "thinking", agent_id, run_id, text, thinking_duration_ms? }
  | SDKStatusMessage      // { type: "status", agent_id, run_id, status: "CREATING"|"RUNNING"|"FINISHED"|"ERROR"|"CANCELLED"|"EXPIRED" }
  | SDKRequestMessage     // { type: "request", agent_id, run_id, request_id }
  | SDKTaskMessage        // { type: "task", agent_id, run_id, status?, text? }
```

### Message Content Blocks

```typescript
interface TextBlock {
  type: "text"
  text: string
}

interface ToolUseBlock {
  type: "tool_use"
  id: string       // tool call ID
  name: string     // tool name
  input: unknown   // tool arguments
}
```

### Assistant Message Structure

```typescript
interface SDKAssistantMessage {
  type: "assistant"
  agent_id: string
  run_id: string
  message: {
    role: "assistant"
    content: Array<TextBlock | ToolUseBlock>
  }
}
```

The assistant message can contain BOTH text and tool_use blocks interleaved. The coding-agent-cli's `emitSdkMessage` function demonstrates this:

```typescript
case "assistant":
  for (const block of event.message.content) {
    if (block.type === "text") {
      emit({ type: "assistant_delta", text: block.text })
    } else {
      emit({
        type: "tool",
        callId: block.id,
        name: block.name,
        params: summarizeToolArgs(block.name, block.input),
        status: "requested",
      })
    }
  }
```

### Tool Call Lifecycle

```typescript
interface SDKToolUseMessage {
  type: "tool_call"
  agent_id: string
  run_id: string
  call_id: string
  name: string
  status: "running" | "completed" | "error"
  args?: unknown
  result?: unknown
  truncated?: { args?: boolean; result?: boolean }
}
```

Tools progress through: `running` → `completed` | `error`

### Status Events

```typescript
status: "CREATING" | "RUNNING" | "FINISHED" | "ERROR" | "CANCELLED" | "EXPIRED"
```

### Local Run Stream Events (wire format)

For local execution, there's a schema-versioned envelope:

```typescript
type LocalRunStreamEvent =
  | LocalRunStreamSdkMessageEvent  // { schemaVersion: 1, type: "sdk_message", agentId, runId, message: SDKMessage }
  | LocalRunStreamResultEvent      // { schemaVersion: 1, type: "result", agentId, runId, status, errorCode? }
  | LocalRunStreamDoneEvent        // { schemaVersion: 1, type: "done", agentId, runId }
```

### Interaction Updates (Delta Stream)

Fine-grained streaming deltas for building responsive UIs:

```typescript
type InteractionUpdate =
  | TextDeltaUpdate
  | ThinkingDeltaUpdate
  | ThinkingCompletedUpdate
  | ToolCallStartedUpdate
  | PartialToolCallUpdate
  | ToolCallCompletedUpdate
  | ShellOutputDeltaUpdate
  | TokenDeltaUpdate
  | SummaryStartedUpdate
  | SummaryUpdate
  | SummaryCompletedUpdate
  | TurnEndedUpdate
  | UserMessageAppendedUpdate
```

---

## 5. Tool System

### Tool Types (from conversation-types.d.ts — 12,000+ lines of Zod schemas)

The SDK's shared tool-call types define these tools (re-exported from `@anysphere/cursor-sdk-shared`):

**File Operations:**
- `ReadToolCall` — read file contents (args: `path`, `offset`, `limit`)
- `WriteToolCall` — write/create files (args: `path`, `content`)
- `EditToolCall` — edit files (args: `path`, `instruction`)
- `DeleteToolCall` — delete files (args: `path`)
- `GlobToolCall` — find files by pattern (args: `pattern`, `path`)
- `LsToolCall` — list directory (args: `path`)

**Search:**
- `GrepToolCall` — content search with multiple output modes (`content`, `files`, `count`)
- `SemSearchToolCall` — semantic search
- `ReadLintsToolCall` — read linter results

**Execution:**
- `ShellToolCall` — execute shell commands (args: `command`, `cwd`, `timeout`)
- `McpToolCall` — call MCP server tools (args: `providerId`, `toolId`, `args`)

**Agent/Planning:**
- `TaskToolCall` — spawn sub-agents (args: `prompt`, `mode: TaskMode`, `subagentType: TaskSubagentType`)
- `CreatePlanToolCall` — create execution plans
- `UpdateTodosToolCall` — manage todo lists

### Task Sub-Agent Types

```typescript
type TaskSubagentType = "code" | "context" | "plan" | ...
type TaskMode = "background" | ...
```

The `TaskToolCall` reveals that Cursor agents can spawn **sub-agents** — specialized agents that run in the background or inline to handle specific subtasks.

### MCP Server Integration

```typescript
type McpServerConfig =
  | { type?: "stdio"; command: string; args?: string[]; env?: Record<string, string>; cwd?: string }
  | { type?: "http"|"sse"; url: string; headers?: Record<string, string>; auth?: { CLIENT_ID: string; CLIENT_SECRET?: string; scopes?: string[] } }
```

MCP servers can be stdio-based (local processes) or remote (HTTP/SSE), with OAuth support.

---

## 6. Conversation State

### Conversation Turns

The SDK defines a rich conversation model via Zod schemas (conversation-types.d.ts is the largest file at 12,061 lines):

```typescript
type ConversationTurn = AssistantMessage | UserMessage | ShellConversationTurn
type ConversationStep = { type: "assistantMessage", message: AssistantMessage }
                       | { type: "toolCall", message: ShellCommand | ... }
```

### Shell Conversation Turns

```typescript
type ShellConversationTurn = {
  command: ShellCommand    // { command: string; workingDirectory?: string }
  output: ShellOutput      // { stdout: string; stderr: string; exitCode: number }
}
```

### Run.conversation()

The `Run` interface exposes:

```typescript
interface Run {
  conversation(): Promise<ConversationTurn[]>
  // ... plus stream(), wait(), cancel()
}
```

### Multi-Turn via Agent

The agent maintains conversation context across multiple `send()` calls:

```typescript
const agent = Agent.create({ apiKey, model: { id: "composer-2" }, local: { cwd: "/project" } })
const run1 = await agent.send("Create a file called hello.txt")
await run1.wait()
const run2 = await agent.send("Now edit it to say goodbye")  // agent remembers context
await run2.wait()
```

This is demonstrated in both the coding-agent-cli (multi-turn interactive session) and app-builder (persistent agent per session with multi-turn chat).

### Agent.messages.list()

```typescript
Agent.messages.list(agentId, { limit?, offset?, runtime?, cwd? })
```

Returns `AgentMessage[]` with `{ type: "user"|"assistant", uuid, agent_id, message }`.

---

## 7. Artifacts System

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
// CloudApiClient
listArtifacts(agentId: string): Promise<{ items: V1Artifact[] }>
getArtifactDownloadUrl({ agentId, path }): Promise<{ url: string; expiresAt: string }>
```

Cloud artifacts use **presigned download URLs** that expire. The agent-kanban demonstrates three artifact access patterns:

1. **List**: GET `/api/agents/:id/artifacts` → metadata with preview kind (image/video/file)
2. **Stream**: GET `/api/agents/:id/artifacts/media?path=...` → proxied binary stream
3. **Download**: GET `/api/agents/:id/artifacts/download?path=...` → presigned URL JSON

### Artifact Preview Classification

The agent-kanban classifies artifacts by content type and extension:

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

## 8. REST API Surface

### CloudApiClient — Full REST Surface

The `CloudApiClient` class (cloud-api-client.d.ts) reveals the complete REST API:

| Method | HTTP Path (inferred) | Description |
|---|---|---|
| `createAgent(req)` | `POST /v1/agents` | Create agent + initial run |
| `getAgent(id)` | `GET /v1/agents/:id` | Get agent metadata |
| `listAgents(params)` | `GET /v1/agents` | List agents (paginated) |
| `archiveAgent(id)` | `POST /v1/agents/:id/archive` | Archive agent |
| `unarchiveAgent(id)` | `POST /v1/agents/:id/unarchive` | Unarchive agent |
| `deleteAgent(id)` | `DELETE /v1/agents/:id` | Delete agent (irreversible) |
| `createRun(agentId, req)` | `POST /v1/agents/:id/runs` | Create follow-up run |
| `listRuns(agentId, params)` | `GET /v1/agents/:id/runs` | List runs (paginated) |
| `getRun({ agentId, runId })` | `GET /v1/agents/:id/runs/:runId` | Get run details |
| `cancelRun({ agentId, runId })` | `POST /v1/agents/:id/runs/:runId/cancel` | Cancel run |
| `streamRun({ agentId, runId })` | `GET /v1/agents/:id/runs/:runId/stream` | SSE event stream |
| `listArtifacts(agentId)` | `GET /v1/agents/:id/artifacts` | List artifacts |
| `getArtifactDownloadUrl(...)` | `GET /v1/agents/:id/artifacts/:path/download` | Presigned URL |
| `getMe()` | `GET /v1/me` | Current user info |
| `listModels()` | `GET /v1/models` | Available models |
| `listRepositories()` | `GET /v1/repositories` | Connected GitHub repos |

### V1 Data Shapes

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

### Error Responses

```typescript
interface V1ErrorResponse {
  error: {
    code: string       // e.g., "agent_busy" (409)
    message: string
    helpUrl?: string
    provider?: string  // for IntegrationNotConnectedError
  }
}
```

### Cursor SDK Error Hierarchy

```typescript
CursorAgentError
├── AuthenticationError     // 401
├── RateLimitError          // 429
├── ConfigurationError      // 400, 404
│   └── IntegrationNotConnectedError  // SCM not connected
├── NetworkError            // 503, 504
└── UnknownAgentError
```

All errors wrap Connect gRPC errors (`@connectrpc/connect`) and expose `isRetryable`, `code`, `cause`, `protoErrorCode`.

---

## 9. Example Deep Dives

### 9.1 quickstart

**Purpose**: Minimal working examples of the SDK.

**Files**: `src/index.ts`, `src/test-model.mts`, `src/review-venom.ts`

Three examples:
1. **index.ts** — Basic agent creation, send, stream, wait:
   ```typescript
   const agent = Agent.create({
     apiKey: process.env.CURSOR_API_KEY,
     model: { id: "composer-2" },
     local: { cwd: process.cwd() },
   })
   const run = await agent.send("your prompt here")
   for await (const event of run.stream()) { /* handle events */ }
   const result = await run.wait()
   ```

2. **test-model.mts** — Test a specific model with streaming output.

3. **review-venom.ts** — More complex: uses `Agent.prompt()` one-shot, passes `local: { cwd }`, demonstrates model parameter selection.

**Key takeaway**: Shows the absolute minimum — create, send, stream, wait, dispose.

---

### 9.2 app-builder

**Purpose**: Full-stack web app that creates live-updating applications via conversational AI. The "killer demo" of the SDK.

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
│  POST /api/settings/api-key                   │
│  POST /api/project-name                       │
└────────────────────┬─────────────────────────┘
                     │
┌────────────────────▼─────────────────────────┐
│  Agent SDK (Local)                             │
│  Agent.create({ local: { cwd: sessionPath } })│
│  → agent.send(prompt) → run.stream()          │
│  → Vite dev server (hot reload)               │
└──────────────────────────────────────────────┘
```

**Session Management**:
- Each session gets a UUID, a project directory under `~/.app-builder/sessions/{id}/app/`
- Template app scaffolded: Vite + React + TypeScript (7 files from `template.ts`)
- `pnpm install` runs, then Vite dev server starts on a random port
- Sessions stored in-memory (`globalThis.__appBuilderSessions`) — lost on server restart

**Agent Per Session**:
- One `SDKAgent` created per session, reused across messages (multi-turn)
- System instructions tell the agent it's "building a local Vite React TypeScript application"
- Agent edits files → Vite hot-reloads → iframe shows live preview

**Project Name Generation** (clever pattern):
- Uses a SEPARATE agent instance for naming (not the session agent)
- Prompts with XML extraction: `<projectName>Concise Name</projectName>`
- 15-second timeout with fallback to heuristic extraction from user's first message
- Shows Cursor's pattern of using the SDK itself for meta-tasks

**Model Selection UI**:
- Full model catalog with parameter controls (effort levels, fast/thinking toggles)
- Local model ID encoding logic reveals the actual model format (see §2)
- Per-message model selection — user can switch models mid-conversation

**Frontend** (4,201-line React component):
- Chat interface with markdown rendering, tool call visualization
- Activity feed with icons per tool type (read, search, edit, shell, test, build)
- Iframe preview panel with URL bar
- Sidebar with conversation list, model picker
- LocalStorage persistence for chat state

**Streaming**: Uses SSE via `fetch()` + `ReadableStream`:
```typescript
const response = await fetch("/api/chat", { method: "POST", body: ... })
const reader = response.body!.getReader()
// parse newline-delimited JSON events
```

---

### 9.3 agent-kanban

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
│  Next.js API Routes                       │
│  GET/POST  /api/agents                    │
│  GET      /api/agents/:id/artifacts       │
│  GET      /api/agents/:id/artifacts/media │
│  GET      /api/agents/:id/artifacts/download │
│  GET      /api/models                     │
└────────────────┬─────────────────────────┘
                 │
┌────────────────▼─────────────────────────┐
│  Agent SDK (Cloud)                        │
│  Agent.create({ cloud: { repos: [...] } })│
│  Agent.list({ runtime: "cloud" })         │
│  Agent.listRuns()                         │
│  agent.listArtifacts()                    │
│  agent.downloadArtifact()                 │
│  Cursor.me() / Cursor.models.list()       │
│  Cursor.repositories.list()               │
└──────────────────────────────────────────┘
```

**Cloud Agent Creation**:
```typescript
const agent = await Agent.create({
  apiKey,
  name: input.name || prompt.slice(0, 80),
  model: input.modelId ? { id: input.modelId } : undefined,
  cloud: {
    repos: [{ url: repoUrl, startingRef: branch }],
    autoCreatePR: true,
  },
})
await agent.send(prompt)  // first prompt triggers the run
```

**Agent Listing & Enrichment**:
- Lists cloud agents via `Agent.list({ runtime: "cloud" })`
- For each agent, parallel-fetches runs + artifacts
- Enriches agent cards with latest run status, duration, branch, PR URL
- Paginated with cursor-based pagination

**Artifact Management** (3-tier):
1. **List** → `agent.listArtifacts()` → metadata + preview kind classification
2. **Media streaming** → `agent.downloadArtifact()` → fetch presigned URL → proxy as binary stream
3. **Download** → return presigned URL as JSON for client-side download

**Defensive API Access**:
The kanban uses a fascinating defensive pattern — it casts the SDK to unknown types and checks for method existence:

```typescript
const agentSdk = Agent as unknown as AgentNamespace
// AgentNamespace has optional methods:
type AgentNamespace = {
  list?: (options) => Promise<unknown>
  listRuns?: (agentId, options?) => Promise<unknown>
  create: (options) => Promise<SdkAgentLike>
  get?: (id, options?) => Promise<unknown>
  resume?: (id, options?) => Promise<SdkAgentLike>
}
```

Similarly for field access, it tries multiple possible field names:
```typescript
firstString(record, ["id", "agentId", "uuid"])
firstString(record, ["status", "_status", "state", "lifecycleStatus", "runStatus", "agentStatus"])
```

This reveals that the SDK's REST API shape may not be fully stable yet, and the cookbook authors built defensive normalization layers.

**Repository Caching**: 55-second TTL cache for `Cursor.repositories.list()` results.

**Session Management**: In-memory sessions with cookie/header-based auth, persisted API key to `~/.agent-kanban/settings.json`.

---

### 9.4 coding-agent-cli

**Purpose**: Terminal-based coding agent with interactive TUI, demonstrating the SDK as a CLI tool.

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

**Entry Point** (`index.ts`):
- Custom arg parser (no dependencies)
- Three modes: `--help`, plain prompt (stdin or arg), interactive TTY
- Default model: `CURSOR_MODEL` env or `composer-2`

**CodingAgentSession** (`agent.ts`):
The core abstraction wrapping the SDK:

```typescript
class CodingAgentSession {
  private agent: SDKAgent
  private mode: ExecutionMode  // "local" | "cloud"
  private modelSelection: ModelSelection

  async sendPrompt({ prompt, onEvent }) {
    const run = await this.agent.send(buildPrompt(prompt), {
      ...(this.mode === "local" ? { model: this.modelSelection } : {}),
      ...(this.mode === "local" && this.force ? { local: { force: true } } : {}),
    })
    for await (const event of run.stream()) {
      emitSdkMessage(event, onEvent)
    }
    const result = await run.wait()
    onEvent({ type: "result", status: result.status, durationMs: result.durationMs })
  }
}
```

Key design decisions:
- **Model per-send for local only**: Cloud resolves model server-side, so model is only sent for local mode
- **Agent key tracking**: Computes a JSON key from `{ mode, model }` to detect when agent needs recreation
- **Cloud repository detection**: Reads `git remote.origin.url` and `HEAD` branch via `execFileSync`

**Event Normalization** (`emitSdkMessage`):
Maps SDK's `SDKMessage` types to simplified `AgentEvent` types:
- `SDKMessage.assistant` → `assistant_delta` (text) + `tool` (tool_use blocks)
- `SDKMessage.thinking` → `thinking`
- `SDKMessage.tool_call` → `tool` (with status)
- `SDKMessage.status` → `status`
- `SDKMessage.task` → `task`

**Tool Argument Summarization**:
Intelligent tool display that extracts relevant args per tool type:
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

**TUI** (`App.tsx` — 1,062 lines):
- Built with Ink (React for CLI) + `ink-select-input` + `ink-text-input`
- **Transcript system**: Scrollable log with color-coded entries (user=green, assistant=white, tool=magenta, error=red, meta=cyan, status=yellow)
- **Markdown rendering**: Custom terminal markdown renderer (headings, code blocks, lists, blockquotes, inline code, links)
- **Model picker**: Searchable list with F (fast) and T (thinking) toggle hotkeys
- **Slash commands**: `/help`, `/local`, `/cloud`, `/model`, `/reset`, `/exit`, `/quit`
- **Ctrl+C handling**: First Ctrl+C cancels the run, second exits
- **View modes**: `input`, `command` (slash command picker), `model` (model picker)

---

## 10. Intelligence Behind the Cookbook

### Why NOW?

**Strategic timing**: Cursor is positioning itself not just as an IDE but as an **AI agent platform**. The SDK at v1.0.7 represents a maturation point where:

1. **Anthropic Claude Code, GitHub Copilot CLI, and OpenAI Codex** have established the "coding agent CLI" category. Cursor needs to show it can play here too — but with the advantage of local + cloud unification.

2. **The "agentic coding" market is exploding**. By releasing a cookbook, Cursor seeds the ecosystem with reference architectures that naturally use Cursor's infrastructure (cloud agents, artifact hosting, PR workflows).

3. **Developer adoption via examples, not docs**. The cookbook is deliberately practical — four working apps, not API reference material. This lowers the barrier to building on Cursor.

### Platform vs IDE Play

The SDK reveals Cursor's platform ambitions:

- **Cloud agents are first-class**: The `CloudApiClient` exposes a full REST API with agents, runs, artifacts, streaming. This is an API platform, not just an IDE feature.
- **`bc-` prefixed agent IDs** suggest a hosted agent service with persistence, versioning, and multi-user support.
- **`autoCreatePR`** integration turns Cursor into a CI/CD pipeline component — agents create PRs directly.
- **Environment types** (`cloud`, `pool`, `machine`) suggest Cursor is building compute infrastructure — this is an AWS/Azure play, not just a code editor play.
- **Analytics telemetry** (`sdk.run.created`, `sdk.run.completed`) with `SdkRuntime` tracking ("local", "cloud", "pool", "machine") shows Cursor is instrumenting the entire platform for usage metrics.
- **`IntegrationNotConnectedError`** with `provider` and `helpUrl` fields reveals Cursor has (or plans) multi-SCM-provider support beyond GitHub.

### What the Examples Strategically Demonstrate

1. **quickstart** → "Look how easy it is — 10 lines to get an agent running"
2. **app-builder** → "Our local agents can build real apps with live preview" (competes with Claude Artifacts, v0.dev)
3. **agent-kanban** → "Our cloud agents are production-ready with PR workflows and artifact management"
4. **coding-agent-cli** → "Our SDK can power full CLI tools" (competes with Claude Code, Aider, Codex CLI)

The examples are carefully chosen to cover: local execution, cloud execution, web UI, CLI, real-time streaming, artifact management, and model selection — every major SDK capability.

---

## 11. Gaps & Opportunities

### What the Cookbook DOESN'T Show (But the SDK Supports)

1. **`Agent.prompt()` one-shot API** — Only used in quickstart/review-venom, not demonstrated as a pattern for simple automation
2. **`Agent.resume()`** — Resuming existing agents by ID. Critical for persistent workflows but not shown
3. **`Agent.archive()` / `Agent.unarchive()` / `Agent.delete()`** — Agent lifecycle management. Only `create` and `list` are shown
4. **`Run.cancel()`** — Only the CLI shows cancellation, not as a standalone pattern
5. **`Run.conversation()`** — Retrieving full conversation history. Not used in any example
6. **`Agent.messages.list()`** — Historical message retrieval. Not used
7. **`Run.onDidChangeStatus()`** — Reactive status listening. Not used
8. **`Run.supports()` / `Run.unsupportedReason()`** — Capability checking. Only used for cancel in CLI
9. **Multi-workspace** (`local: { cwd: string[] }`) — Not demonstrated
10. **MCP Server integration** (`mcpServers` config) — Not shown in any example
11. **Custom sub-agents** (`agents` config with `AgentDefinition`) — Not shown
12. **`CursorAgentPlatform`** — The pluggable platform abstraction with custom stores is not used
13. **`settingSources`** — Loading Cursor IDE settings layers
14. **`envVars`** in local mode — Only app-builder passes `BROWSER: "none"`
15. **`local: { force: true }`** — Only coding-agent-cli demonstrates this
16. **Image inputs** (`SDKUserMessage.images`) — Not demonstrated
17. **Cloud environment types** (`pool`, `machine`) — Only default `cloud` shown
18. **`skipReviewerRequest`** — Not shown
19. **`workOnCurrentBranch`** — Not shown
20. **`Run.git` info** — Branch URLs, PR URLs from run results — fetched but not prominently displayed

### Build Opportunities

1. **MCP-powered agents** — The SDK supports MCP servers (both stdio and HTTP/SSE with OAuth). Build an agent that connects to external tools (Jira, Linear, Figma, databases) via MCP.

2. **Sub-agent orchestration** — `TaskToolCall` supports spawning sub-agents. Build a multi-agent system where specialized agents handle different concerns (testing, documentation, deployment).

3. **CI/CD integration** — Cloud agents with `autoCreatePR` could be triggered from GitHub Actions. Build a "review bot" that creates PRs with fixes.

4. **Agent marketplace** — `AgentDefinition` with custom prompts and models suggests agent templates. Build a registry of pre-configured agents for specific tasks.

5. **Real-time collaboration** — `RunEventNotifier` and `WatchableRunEventStore` suggest multi-consumer event streaming. Build a collaborative coding session.

6. **Agent analytics dashboard** — The SDK tracks `sdk.run.created` and `sdk.run.completed` events. Build observability tooling.

7. **Local-first with cloud fallback** — The SDK supports both. Build an agent that works offline (local) and syncs to cloud when connected.

8. **Conversation-branching workflows** — `Run.conversation()` + `Agent.resume()` enable conversation forking. Build a "try different approaches" UX.

9. **Artifact gallery** — Cloud agents produce artifacts. Build a portfolio/showcase system for agent-generated work.

10. **Multi-repo agents** — `cloud: { repos: [...] }` supports multiple repos. Build cross-repository refactoring agents.

---

## Summary

The Cursor SDK v1.0.7 is a comprehensive agent platform SDK that bridges local coding agents (filesystem + shell access) with cloud-hosted agents (git repos + PR workflows). The cookbook strategically demonstrates the SDK's range through four complementary examples, each targeting a different use case and execution mode.

The SDK's architecture reveals Cursor's evolution from IDE to platform: gRPC-based cloud API, presigned artifact storage, multi-environment compute (cloud/pool/machine), MCP tool extensibility, sub-agent orchestration, and structured analytics telemetry. The defensive coding patterns in the kanban example (multiple field name fallbacks, optional method checks) suggest the API is still evolving, but the core abstractions (`Agent.create → send → stream → wait`) are stable and well-designed.

The most powerful insight is the **local + cloud duality**: the same `SDKAgent` interface works in both modes, with the runtime auto-detected from agent IDs. This lets developers build tools that work locally for development and scale to cloud for production — exactly the kind of developer experience that drives platform adoption.
